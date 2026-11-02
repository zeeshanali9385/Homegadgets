#!/usr/bin/env bash
# Seeds HORIZON PK smart collections + navigation menus via Shopify CLI.
#
# BEFORE RUNNING (required confirmation):
#   store:  YOUR_STORE.myshopify.com
#   auth:   shopify store auth --store YOUR_STORE.myshopify.com
#   side effects: creates collections + menus (--allow-mutations)
#
# Then:
#   STORE=YOUR_STORE.myshopify.com ./scripts/seed-horizon-catalog.sh
#   Import data/horizon-products.csv in Admin (Products → Import)

set -euo pipefail

STORE="${STORE:-}"
if [[ -z "$STORE" ]]; then
  echo "Set STORE=your-store.myshopify.com"
  exit 1
fi

run_q() {
  SHOPIFY_CLI_AGENT_INFO="n:cursor|v:1.0|p:cursor|m:composer" \
  shopify store execute \
    --store "$STORE" \
    --allow-mutations \
    --json \
    --query "$1"
}

create_smart_collection() {
  local handle="$1"
  local title="$2"
  local tag="$3"
  echo "Collection: $title (tag=$tag)"
  run_q "mutation {
    collectionCreate(input: {
      title: \"$title\",
      handle: \"$handle\",
      ruleSet: {
        appliedDisjunctively: false,
        rules: [{ column: TAG, relation: EQUALS, condition: \"$tag\" }]
      }
    }) {
      collection { id handle }
      userErrors { field message }
    }
  }" || true
}

echo "==> Creating smart collections..."
create_smart_collection "sale" "Sale" "sale"
create_smart_collection "men" "Men" "men"
create_smart_collection "men-stainless-steel" "Men Stainless Steel" "men-stainless-steel"
create_smart_collection "men-leather" "Men Leather" "men-leather"
create_smart_collection "men-sports" "Men Sports" "men-sports"
create_smart_collection "men-formal" "Men Formal" "men-formal"
create_smart_collection "women" "Women" "women"
create_smart_collection "women-bracelet" "Women Bracelet" "women-bracelet"
create_smart_collection "women-stainless-steel" "Women Stainless Steel" "women-stainless-steel"
create_smart_collection "women-leather" "Women Leather" "women-leather"
create_smart_collection "smart-watches" "Smart Watches" "smart-watches"
create_smart_collection "couples" "Couples" "couples"
create_smart_collection "best-sellers" "Best Sellers" "best-sellers"
create_smart_collection "new-arrival" "New Arrival" "new-arrival"

echo "==> Creating / updating navigation menus..."
run_q 'mutation {
  menuCreate(title: "Main menu", handle: "main-menu", items: [
    { title: "Sale", type: HTTP, url: "/collections/sale" },
    { title: "Best Sellers", type: HTTP, url: "/collections/best-sellers" },
    { title: "New Arrival", type: HTTP, url: "/collections/new-arrival" },
    { title: "Men", type: HTTP, url: "/collections/men", items: [
      { title: "Stainless Steel", type: HTTP, url: "/collections/men-stainless-steel" },
      { title: "Leather", type: HTTP, url: "/collections/men-leather" },
      { title: "Sports", type: HTTP, url: "/collections/men-sports" },
      { title: "Formal & Dress", type: HTTP, url: "/collections/men-formal" }
    ]},
    { title: "Women", type: HTTP, url: "/collections/women", items: [
      { title: "Bracelet", type: HTTP, url: "/collections/women-bracelet" },
      { title: "Stainless Steel", type: HTTP, url: "/collections/women-stainless-steel" },
      { title: "Leather", type: HTTP, url: "/collections/women-leather" }
    ]},
    { title: "Smart Watches", type: HTTP, url: "/collections/smart-watches" },
    { title: "For Couples", type: HTTP, url: "/collections/couples" },
    { title: "Track Order", type: HTTP, url: "/pages/track-order" }
  ]) {
    menu { id handle }
    userErrors { field message }
  }
}' || true

run_q 'mutation {
  menuCreate(title: "Footer shop", handle: "footer-shop", items: [
    { title: "Sale", type: HTTP, url: "/collections/sale" },
    { title: "Smartwatches", type: HTTP, url: "/collections/smart-watches" },
    { title: "New Arrival", type: HTTP, url: "/collections/new-arrival" },
    { title: "Men Watches", type: HTTP, url: "/collections/men" },
    { title: "Ladies Watches", type: HTTP, url: "/collections/women" },
    { title: "Couple Watches", type: HTTP, url: "/collections/couples" }
  ]) {
    menu { id handle }
    userErrors { field message }
  }
}' || true

run_q 'mutation {
  menuCreate(title: "Footer care", handle: "footer-care", items: [
    { title: "FAQs", type: HTTP, url: "/pages/faqs" },
    { title: "Contact Us", type: HTTP, url: "/pages/contact" },
    { title: "Returns & Exchange Policy", type: HTTP, url: "/policies/refund-policy" },
    { title: "Shipping Policy", type: HTTP, url: "/policies/shipping-policy" },
    { title: "Modes of Payment", type: HTTP, url: "/pages/payments" },
    { title: "Privacy Policy", type: HTTP, url: "/policies/privacy-policy" },
    { title: "Terms of Service", type: HTTP, url: "/policies/terms-of-service" }
  ]) {
    menu { id handle }
    userErrors { field message }
  }
}' || true

echo "==> Catalog seed finished for $STORE"
echo "Import products: Admin → Products → Import → data/horizon-products.csv"
echo "Upload your own logo + hero/category images in Theme editor (no competitor brand media)."
