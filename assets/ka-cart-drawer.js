/* Nomtech custom cart drawer: instant quantity/delete, instant open on Add to bag.
   Used by sections/cart-drawer.liquid */
(() => {
  if (window.kaCartDrawer) return;

  const ROOT = window.Shopify?.routes?.root || '/';
  const DEBOUNCE = 350;
  const timers = new Map();
  const targets = new Map();
  let queue = Promise.resolve();
  let inFlight = 0;

  const getDrawer = () => document.getElementById('cart-drawer');
  const getSectionId = () => getDrawer()?.dataset.sectionId;

  const formatMoney = (cents) => {
    const format = window.themeVariables?.settings?.moneyFormat || '${{amount}}';
    const value = (Number(cents) || 0) / 100;
    const fmt = (decimals, thousands, decimal) => {
      const parts = value.toFixed(decimals).split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousands);
      return parts.join(decimal);
    };
    return format.replace(/\{\{\s*(\w+)\s*\}\}/, (_, key) => {
      switch (key) {
        case 'amount_no_decimals': return fmt(0, ',', '.');
        case 'amount_with_comma_separator': return fmt(2, '.', ',');
        case 'amount_no_decimals_with_comma_separator': return fmt(0, '.', ',');
        case 'amount_with_apostrophe_separator': return fmt(2, "'", '.');
        default: return fmt(2, ',', '.');
      }
    });
  };

  const setSyncing = () => getDrawer()?.classList.toggle('ka-is-syncing', inFlight > 0 || timers.size > 0);

  const showError = (message) => {
    const box = getDrawer()?.querySelector('[data-ka-error]');
    if (!box) return;
    box.textContent = message;
    box.hidden = false;
    clearTimeout(box._kaTimer);
    box._kaTimer = setTimeout(() => (box.hidden = true), 4000);
  };

  const findItem = (key) => [...(getDrawer()?.querySelectorAll('.ka-item') || [])].find((el) => el.dataset.key === key);

  /* Instant on-screen update, before the server answers */
  const paintItem = (key, qty) => {
    const item = findItem(key);
    if (!item) return;

    if (qty <= 0) {
      item.style.height = item.offsetHeight + 'px';
      item.style.overflow = 'hidden';
      item.classList.add('is-removing');
      requestAnimationFrame(() => {
        item.style.transition = 'height .25s ease, padding .25s ease, margin .25s ease, opacity .2s ease';
        item.style.height = '0px';
        item.style.paddingTop = item.style.paddingBottom = '0px';
        item.style.marginBottom = '0px';
        item.style.borderBottomWidth = '0px';
      });
      return;
    }

    const unit = Number(item.dataset.unit) || 0;
    const compareUnit = Number(item.dataset.compareUnit) || 0;
    const input = item.querySelector('[data-ka-input]');
    const [minus, plus] = item.querySelectorAll('.ka-qty__btn');
    const max = item.dataset.max === '' ? Infinity : Number(item.dataset.max);

    if (input) input.value = qty;
    if (minus) minus.dataset.kaQty = qty - 1;
    if (plus) {
      plus.dataset.kaQty = qty + 1;
      plus.disabled = qty >= max;
    }

    const price = item.querySelector('[data-ka-price]');
    if (price) price.textContent = formatMoney(unit * qty);

    const compare = item.querySelector('[data-ka-compare]');
    if (compare) compare.textContent = formatMoney(compareUnit * qty);

    const save = item.querySelector('[data-ka-save]');
    if (save && compareUnit > unit) {
      save.textContent = (save.dataset.template || '[amount]').replace('[amount]', formatMoney((compareUnit - unit) * qty));
    }
  };

  const render = (html) => {
    const drawer = getDrawer();
    if (!drawer || !html) return;

    const fresh = new DOMParser().parseFromString(html, 'text/html').querySelector('cart-drawer');
    if (!fresh) return;

    const body = drawer.shadowRoot?.querySelector('[part~="body"]');
    const scrollTop = body ? body.scrollTop : 0;

    drawer.replaceChildren(...document.importNode(fresh, true).childNodes);
    drawer.classList.toggle('drawer--center-body', fresh.classList.contains('drawer--center-body'));
    if (body) body.scrollTop = scrollTop;
  };

  const refresh = async () => {
    const sectionId = getSectionId();
    if (!sectionId) return;
    const response = await fetch(`${ROOT}?sections=${encodeURIComponent(sectionId)}`);
    const data = await response.json();
    render(data[sectionId]);
  };

  const send = (key, qty) => {
    inFlight++;
    setSyncing();

    queue = queue.then(async () => {
      const sectionId = getSectionId();

      try {
        const response = await fetch(`${ROOT}cart/change.js`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ id: key, quantity: qty, sections: sectionId ? [sectionId] : [] })
        });
        const cart = await response.json();

        if (!response.ok) {
          await refresh();
          showError(cart.description || cart.message || 'Sorry, that quantity is not available.');
          return;
        }

        /* Redraw only after the last pending change, so quick taps are never undone mid-way.
           The theme's cart-drawer listens to cart:change and swaps in cart.sections; it also updates the header count. */
        if (inFlight === 1 && timers.size === 0) {
          if (cart.sections?.[sectionId]) {
            document.documentElement.dispatchEvent(new CustomEvent('cart:change', {
              bubbles: true,
              detail: { baseEvent: 'line-item:change', cart }
            }));
          } else {
            await refresh();
          }
        }
      } catch (error) {
        console.error(error);
        await refresh().catch(() => {});
        showError('Something went wrong, please try again.');
      } finally {
        inFlight--;
        setSyncing();
      }
    });
  };

  const change = (key, qty, immediate = false) => {
    if (!key || Number.isNaN(qty)) return;
    qty = Math.max(0, qty);

    targets.set(key, qty);
    paintItem(key, qty);

    clearTimeout(timers.get(key));
    const fire = () => {
      timers.delete(key);
      send(key, targets.get(key));
    };

    if (immediate || qty === 0) {
      fire();
    } else {
      timers.set(key, setTimeout(fire, DEBOUNCE));
    }
    setSyncing();
  };

  document.addEventListener('click', (event) => {
    const button = event.target.closest('#cart-drawer [data-ka-change]');
    if (!button || button.disabled) return;
    event.preventDefault();
    event.stopPropagation();
    change(button.dataset.kaChange, parseInt(button.dataset.kaQty, 10));
  }, true);

  document.addEventListener('change', (event) => {
    const input = event.target.closest('#cart-drawer [data-ka-input]');
    if (!input) return;
    change(input.dataset.kaInput, parseInt(input.value, 10), true);
  }, true);

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && event.target.closest('#cart-drawer [data-ka-input]')) {
      event.preventDefault();
      event.target.blur();
    }
  });

  /* ---------- Add to bag: open the drawer instantly, then fill it ---------- */
  let addTimer;
  let addSeq = 0;

  const clearAdding = () => {
    const drawer = getDrawer();
    clearTimeout(addTimer);
    if (!drawer) return;
    drawer.classList.remove('ka-is-adding');
    drawer.querySelector('[data-ka-skeleton]')?.remove();
    const empty = drawer.querySelector('.ka-cart__empty');
    if (empty) {
      empty.hidden = false;
      drawer.classList.add('drawer--center-body');
    }
  };

  const showAdding = () => {
    const drawer = getDrawer();
    if (!drawer || window.themeVariables?.settings?.cartType !== 'drawer') return;

    addSeq++;
    drawer.classList.add('ka-is-adding');

    if (!drawer.querySelector('[data-ka-skeleton]')) {
      const skeleton = document.createElement('div');
      skeleton.className = 'ka-skeleton';
      skeleton.setAttribute('data-ka-skeleton', '');
      skeleton.setAttribute('aria-hidden', 'true');
      skeleton.innerHTML = '<span class="ka-sk ka-sk--img"></span><div class="ka-sk-lines"><span class="ka-sk"></span><span class="ka-sk ka-sk--short"></span><span class="ka-sk ka-sk--qty"></span></div>';

      const items = drawer.querySelector('.ka-cart__items');
      if (items) {
        items.prepend(skeleton);
      } else {
        const empty = drawer.querySelector('.ka-cart__empty');
        if (empty) empty.hidden = true;
        drawer.classList.remove('drawer--center-body');
        drawer.append(skeleton);
      }

      const body = drawer.shadowRoot?.querySelector('[part~="body"]');
      if (body) body.scrollTop = 0;
    }

    if (typeof drawer.show === 'function' && !drawer.open) drawer.show();

    clearTimeout(addTimer);
    addTimer = setTimeout(clearAdding, 10000);
  };

  /* The theme fires this the moment Add to bag is pressed, before the request goes out */
  document.addEventListener('cart:prepare-bundled-sections', showAdding);

  /* Add failed (sold out, limit reached...): the theme shows the error on the product form */
  document.addEventListener('cart:error', () => {
    clearAdding();
    getDrawer()?.hide?.();
  });

  /* Shopify's add response already contains the rendered drawer. The theme fires
     cart:prepare-bundled-sections synchronously right before it calls fetch('/cart/add.js'),
     so we wrap fetch at that exact moment (other scripts replace window.fetch after page load,
     so a wrapper installed at load time is not reliable) and unwrap after that one request. */
  const handleAddResponse = (request) => {
    request.then((response) => {
      if (!response.ok) return;
      response.clone().json().then((data) => {
        const sectionId = getSectionId();
        if (data && data.sections && data.sections[sectionId]) {
          render(data.sections[sectionId]);
          getDrawer()?.classList.remove('ka-is-adding');
        }
      }).catch(() => {});
    }).catch(() => {});
  };

  const armAddIntercept = () => {
    const current = window.fetch;
    if (current && current.__kaAdd) return;

    const wrapper = function (input, init) {
      const url = typeof input === 'string' ? input : (input && input.url) || '';
      const request = current.apply(this, arguments);
      if (url.includes('/cart/add')) {
        if (window.fetch === wrapper) window.fetch = current;
        handleAddResponse(request);
      }
      return request;
    };
    wrapper.__kaAdd = true;
    window.fetch = wrapper;
    setTimeout(() => { if (window.fetch === wrapper) window.fetch = current; }, 3000);
  };

  document.addEventListener('cart:prepare-bundled-sections', armAddIntercept);

  /* Backup: render straight from the event instead of waiting for the theme's own
     extra /cart.js request and fade animation. */
  document.addEventListener('cart:change', (event) => {
    const html = event.detail?.cart?.sections?.[getSectionId()];
    if (html && event.detail.baseEvent !== 'line-item:change') {
      render(html);
      getDrawer()?.classList.remove('ka-is-adding');
    }

    const seq = addSeq;
    setTimeout(() => { if (seq === addSeq) clearAdding(); }, 1500);
  });

  window.kaCartDrawer = { change, refresh, showAdding };
})();
