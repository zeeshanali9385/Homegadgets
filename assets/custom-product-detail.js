(() => {
  class KhyberProductDetail extends HTMLElement {
    connectedCallback() {
      this.mainImage = this.querySelector('[data-kg-main-image]');
      this.thumbs = Array.from(this.querySelectorAll('[data-kg-thumb]'));
      this.qtyInput = this.querySelector('[data-kg-qty-input]');
      this.qtyMinus = this.querySelector('[data-kg-qty-minus]');
      this.qtyPlus = this.querySelector('[data-kg-qty-plus]');
      this.sticky = this.querySelector('[data-kg-sticky-cta]');
      this.buyAnchor = this.querySelector('[data-kg-buy-anchor]');
      this.variantInput = this.querySelector('[data-kg-variant-id]');
      this.checkoutVariantInput = this.querySelector('[data-kg-checkout-variant-id]');
      this.buyNowQtyInput = this.querySelector('[data-kg-buy-now-qty]');
      this.optionInputs = Array.from(this.querySelectorAll('[data-kg-option-input]'));
      this.addButtons = Array.from(this.querySelectorAll('.kg-pdp__add, [data-kg-buy-now]'));
      this.priceEl = this.querySelector('.kg-pdp__price');
      this.compareEl = this.querySelector('.kg-pdp__compare');

      try {
        const raw = this.querySelector('[data-kg-variant-json]');
        this.variants = raw ? JSON.parse(raw.textContent) : [];
      } catch (e) {
        this.variants = [];
      }

      this.thumbs.forEach((thumb) => {
        thumb.addEventListener('click', () => this.setActiveThumb(thumb));
      });

      if (this.qtyMinus && this.qtyInput) {
        this.qtyMinus.addEventListener('click', () => this.adjustQty(-1));
      }
      if (this.qtyPlus && this.qtyInput) {
        this.qtyPlus.addEventListener('click', () => this.adjustQty(1));
      }
      if (this.qtyInput) {
        this.qtyInput.addEventListener('change', () => this.syncBuyNowQty());
        this.syncBuyNowQty();
      }

      this.optionInputs.forEach((input) => {
        input.addEventListener('change', () => this.syncVariant());
      });

      if (this.sticky && this.buyAnchor) {
        this.onScroll = this.onScroll.bind(this);
        window.addEventListener('scroll', this.onScroll, { passive: true });
        this.onScroll();
      }
    }

    syncVariant() {
      if (!this.variants.length || !this.variantInput) return;
      const selected = Array.from(this.querySelectorAll('[data-kg-option-input]:checked')).map(
        (input) => input.value
      );
      const match = this.variants.find((variant) =>
        selected.every((value, index) => variant[`option${index + 1}`] === value)
      );
      if (!match) return;

      this.variantInput.value = match.id;
      this.variantInput.disabled = !match.available;
      if (this.checkoutVariantInput) {
        this.checkoutVariantInput.value = match.id;
        this.checkoutVariantInput.disabled = !match.available;
      }
      this.addButtons.forEach((button) => {
        button.disabled = !match.available;
      });
      if (this.priceEl && typeof Shopify !== 'undefined' && Shopify.formatMoney) {
        this.priceEl.textContent = Shopify.formatMoney(match.price);
      }
      if (this.compareEl) {
        if (match.compare_at_price && match.compare_at_price > match.price) {
          this.compareEl.hidden = false;
          if (typeof Shopify !== 'undefined' && Shopify.formatMoney) {
            this.compareEl.textContent = Shopify.formatMoney(match.compare_at_price);
          }
        } else {
          this.compareEl.hidden = true;
        }
      }
    }

    disconnectedCallback() {
      if (this.onScroll) {
        window.removeEventListener('scroll', this.onScroll);
      }
    }

    setActiveThumb(thumb) {
      const src = thumb.getAttribute('data-full-src');
      const srcset = thumb.getAttribute('data-full-srcset');
      if (!this.mainImage || !src) return;

      this.mainImage.src = src;
      if (srcset) this.mainImage.srcset = srcset;

      this.thumbs.forEach((item) => {
        item.classList.toggle('is-active', item === thumb);
        if (item === thumb) item.setAttribute('aria-current', 'true');
        else item.removeAttribute('aria-current');
      });
    }

    adjustQty(delta) {
      if (!this.qtyInput) return;
      const min = Number(this.qtyInput.min || 1);
      const max = Number(this.qtyInput.max || 99);
      const next = Math.min(max, Math.max(min, Number(this.qtyInput.value || 1) + delta));
      this.qtyInput.value = String(next);
      this.qtyInput.dispatchEvent(new Event('change', { bubbles: true }));
      this.syncBuyNowQty();
    }

    syncBuyNowQty() {
      if (!this.qtyInput || !this.buyNowQtyInput) return;
      this.buyNowQtyInput.value = this.qtyInput.value || '1';
    }

    onScroll() {
      if (!this.sticky || !this.buyAnchor) return;
      const rect = this.buyAnchor.getBoundingClientRect();
      const shouldShow = rect.bottom < 0;
      this.sticky.classList.toggle('is-visible', shouldShow);
    }
  }

  if (!customElements.get('khyber-product-detail')) {
    customElements.define('khyber-product-detail', KhyberProductDetail);
  }
})();
