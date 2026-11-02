#!/usr/bin/env bash
# Requires: shopify store auth with write_content,write_online_store_pages
set -euo pipefail
STORE="${STORE:-home-gadget-2kk1camr.myshopify.com}"
export SHOPIFY_CLI_AGENT_INFO="n:cursor|v:1.0|p:cursor|m:composer"

auth_hint() {
  echo "If ACCESS_DENIED, run:"
  echo "shopify store auth --store $STORE --scopes write_content,write_online_store_pages,read_content,read_online_store_pages,write_products,write_online_store_navigation"
}

create_page() {
  local title="$1" handle="$2" template="$3"
  echo "Creating page: $title ($handle) template=$template"
  shopify store execute --store "$STORE" --allow-mutations --version 2026-01 --json --query \
    "mutation { pageCreate(page: { title: \"$title\", handle: \"$handle\", body: \"<p>$title</p>\", isPublished: true, templateSuffix: \"$template\" }) { page { id handle } userErrors { field message } } }" \
    || true
}

auth_hint
create_page "About Us" "about" "about"
create_page "Contact Us" "contact" "contact"
create_page "Shipping Policy" "shipping-policy" "shipping-policy"
create_page "Refund & Exchange Policy" "refund-policy" "refund-policy"
create_page "Privacy Policy" "privacy-policy" "privacy-policy"
create_page "Terms of Service" "terms-of-service" "terms-of-service"
create_page "Track Your Order" "track-order" "track-order"
echo "Done. Assign templates in Admin if needed: Online Store → Pages → [page] → Theme template."
