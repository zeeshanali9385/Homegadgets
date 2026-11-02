#!/usr/bin/env python3
"""Seed HORIZON PK collections, products (royalty-free images), and menus."""
from __future__ import annotations

import json
import subprocess
import sys

STORE = "home-gadget-2kk1camr.myshopify.com"

COLLECTIONS = [
    ("sale", "Sale", "sale"),
    ("men", "Men", "men"),
    ("men-stainless-steel", "Men Stainless Steel", "men-stainless-steel"),
    ("men-leather", "Men Leather", "men-leather"),
    ("men-sports", "Men Sports", "men-sports"),
    ("men-formal", "Men Formal", "men-formal"),
    ("women", "Women", "women"),
    ("women-bracelet", "Women Bracelet", "women-bracelet"),
    ("women-stainless-steel", "Women Stainless Steel", "women-stainless-steel"),
    ("women-leather", "Women Leather", "women-leather"),
    ("smart-watches", "Smart Watches", "smart-watches"),
    ("couples", "Couples", "couples"),
    ("best-sellers", "Best Sellers", "best-sellers"),
    ("new-arrival", "New Arrival", "new-arrival"),
]

# Royalty-free Unsplash watch photos (NOT Sveston assets)
PRODUCTS = [
    {
        "title": "Northline | 40mm",
        "handle": "horizon-northline-40",
        "type": "Male Formal",
        "tags": ["men", "men-formal", "men-stainless-steel", "best-sellers", "sale", "new-arrival"],
        "price": "7999.00",
        "compare": "10999.00",
        "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Vector | 41mm",
        "handle": "horizon-vector-41",
        "type": "Male Formal",
        "tags": ["men", "men-formal", "men-stainless-steel", "best-sellers", "sale"],
        "price": "8999.00",
        "compare": "16999.00",
        "image": "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Regalia | 35mm",
        "handle": "horizon-regalia-35",
        "type": "Male Formal",
        "tags": ["men", "men-formal", "sale"],
        "price": "8499.00",
        "compare": "18999.00",
        "image": "https://images.unsplash.com/photo-1533139502658-0198f920d8e8?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Ascent | 41mm",
        "handle": "horizon-ascent-41",
        "type": "Male Formal",
        "tags": ["men", "men-formal", "sale"],
        "price": "7499.00",
        "compare": "10999.00",
        "image": "https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Velo | 42mm",
        "handle": "horizon-velo-42",
        "type": "Male Sports",
        "tags": ["men", "men-sports", "sale"],
        "price": "6999.00",
        "compare": "11999.00",
        "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Trail | 44mm",
        "handle": "horizon-trail-44",
        "type": "Male Sports",
        "tags": ["men", "men-sports", "new-arrival"],
        "price": "7599.00",
        "compare": "12999.00",
        "image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Velvet | 19mm",
        "handle": "horizon-velvet-19",
        "type": "Female Fancy",
        "tags": ["women", "sale"],
        "price": "6999.00",
        "compare": "10999.00",
        "image": "https://images.unsplash.com/photo-1612817159949-195b6eb9e31a?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Cielo | 22mm",
        "handle": "horizon-cielo-22",
        "type": "Female Fancy",
        "tags": ["women", "best-sellers", "sale"],
        "price": "10999.00",
        "compare": "17999.00",
        "image": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Lumen | 25mm",
        "handle": "horizon-lumen-25",
        "type": "Female Fancy",
        "tags": ["women", "sale"],
        "price": "10999.00",
        "compare": "19999.00",
        "image": "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Rosa | 23mm",
        "handle": "horizon-rosa-23",
        "type": "Female Fancy",
        "tags": ["women", "sale"],
        "price": "10999.00",
        "compare": "17999.00",
        "image": "https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Aura Bracelet Watch",
        "handle": "horizon-aura-bracelet",
        "type": "Female Bracelet",
        "tags": ["women", "women-bracelet", "best-sellers", "sale"],
        "price": "12999.00",
        "compare": "27999.00",
        "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Pulse Smart",
        "handle": "horizon-pulse-smart",
        "type": "Smart Watch",
        "tags": ["smart-watches", "sale", "new-arrival"],
        "price": "9999.00",
        "compare": "15999.00",
        "image": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Nova Smart",
        "handle": "horizon-nova-smart",
        "type": "Smart Watch",
        "tags": ["smart-watches", "best-sellers"],
        "price": "11999.00",
        "compare": "18999.00",
        "image": "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?auto=format&fit=crop&w=1000&q=80",
    },
    {
        "title": "Duo Empire Set",
        "handle": "horizon-duo-empire",
        "type": "Couple Set",
        "tags": ["couples", "best-sellers", "sale"],
        "price": "20999.00",
        "compare": "32999.00",
        "image": "https://images.unsplash.com/photo-1600003014755-ba31aa59c4b6?auto=format&fit=crop&w=1000&q=80",
    },
]


def run_query(query: str, allow_mutations: bool = False) -> dict:
    cmd = [
        "shopify",
        "store",
        "execute",
        "--store",
        STORE,
        "--json",
        "--version",
        "2026-01",
        "--query",
        query,
    ]
    if allow_mutations:
        cmd.append("--allow-mutations")
    env = {
        **dict(**{k: v for k, v in __import__("os").environ.items()}),
        "SHOPIFY_CLI_AGENT_INFO": "n:cursor|v:1.0|p:cursor|m:composer",
    }
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    out = proc.stdout.strip() or proc.stderr.strip()
    # CLI may print spinners/progress; find JSON object
    start = out.find("{")
    end = out.rfind("}")
    if start == -1 or end == -1:
        print("RAW:", out[-2000:])
        raise RuntimeError(f"No JSON in response (exit {proc.returncode})")
    data = json.loads(out[start : end + 1])
    if proc.returncode != 0 and "userErrors" not in json.dumps(data):
        print("ERR:", out[-2000:])
    return data


def create_collections() -> None:
    print("==> Collections")
    for handle, title, tag in COLLECTIONS:
        q = f"""
        mutation {{
          collectionCreate(input: {{
            title: "{title}"
            handle: "{handle}"
            ruleSet: {{
              appliedDisjunctively: false
              rules: [{{ column: TAG, relation: EQUALS, condition: "{tag}" }}]
            }}
          }}) {{
            collection {{ id handle }}
            userErrors {{ field message }}
          }}
        }}
        """
        data = run_query(q, allow_mutations=True)
        errs = data.get("collectionCreate", {}).get("userErrors", [])
        col = data.get("collectionCreate", {}).get("collection")
        if errs:
            print(f"  ! {handle}: {errs}")
        else:
            print(f"  ✓ {handle} -> {col and col.get('id')}")


def create_products() -> None:
    print("==> Products")
    for p in PRODUCTS:
        tags = ", ".join(f'"{t}"' for t in p["tags"])
        # Escape quotes in title
        title = p["title"].replace('"', '\\"')
        q = f"""
        mutation {{
          productSet(synchronous: true, input: {{
            title: "{title}"
            handle: "{p['handle']}"
            vendor: "HORIZON PK"
            productType: "{p['type']}"
            tags: [{tags}]
            status: ACTIVE
            descriptionHtml: "<p>HORIZON PK {title}. Cash on delivery available across Pakistan. 1-year warranty.</p>"
            productOptions: [{{ name: "Title", values: [{{ name: "Default Title" }}] }}]
            variants: [{{
              optionValues: [{{ optionName: "Title", name: "Default Title" }}]
              price: "{p['price']}"
              compareAtPrice: "{p['compare']}"
            }}]
            files: [{{
              originalSource: "{p['image']}"
              contentType: IMAGE
              alt: "{title}"
            }}]
          }}) {{
            product {{ id handle }}
            userErrors {{ field message code }}
          }}
        }}
        """
        data = run_query(q, allow_mutations=True)
        errs = data.get("productSet", {}).get("userErrors", [])
        prod = data.get("productSet", {}).get("product")
        if errs:
            print(f"  ! {p['handle']}: {errs}")
        else:
            print(f"  ✓ {p['handle']} -> {prod and prod.get('id')}")


def update_menus() -> None:
    print("==> Menus")
    menus = run_query("query { menus(first: 20) { nodes { id handle title } } }")
    by_handle = {n["handle"]: n["id"] for n in menus["menus"]["nodes"]}

    main_id = by_handle.get("main-menu")
    if main_id:
        q = f"""
        mutation {{
          menuUpdate(
            id: "{main_id}"
            title: "Main menu"
            items: [
              {{ title: "Sale", type: HTTP, url: "/collections/sale" }}
              {{ title: "Best Sellers", type: HTTP, url: "/collections/best-sellers" }}
              {{ title: "New Arrival", type: HTTP, url: "/collections/new-arrival" }}
              {{ title: "Men", type: HTTP, url: "/collections/men", items: [
                {{ title: "Stainless Steel", type: HTTP, url: "/collections/men-stainless-steel" }}
                {{ title: "Leather", type: HTTP, url: "/collections/men-leather" }}
                {{ title: "Sports", type: HTTP, url: "/collections/men-sports" }}
                {{ title: "Formal & Dress", type: HTTP, url: "/collections/men-formal" }}
              ]}}
              {{ title: "Women", type: HTTP, url: "/collections/women", items: [
                {{ title: "Bracelet", type: HTTP, url: "/collections/women-bracelet" }}
                {{ title: "Stainless Steel", type: HTTP, url: "/collections/women-stainless-steel" }}
                {{ title: "Leather", type: HTTP, url: "/collections/women-leather" }}
              ]}}
              {{ title: "Smart Watches", type: HTTP, url: "/collections/smart-watches" }}
              {{ title: "For Couples", type: HTTP, url: "/collections/couples" }}
              {{ title: "Track Order", type: HTTP, url: "/pages/track-order" }}
            ]
          ) {{
            menu {{ id handle }}
            userErrors {{ field message }}
          }}
        }}
        """
        data = run_query(q, allow_mutations=True)
        print("  main-menu:", data.get("menuUpdate", {}))

    # Create footer-shop / footer-care if missing
    for handle, title, items in [
        (
            "footer-shop",
            "Footer shop",
            [
                ("Sale", "/collections/sale"),
                ("Smartwatches", "/collections/smart-watches"),
                ("New Arrival", "/collections/new-arrival"),
                ("Men Watches", "/collections/men"),
                ("Ladies Watches", "/collections/women"),
                ("Couple Watches", "/collections/couples"),
            ],
        ),
        (
            "footer-care",
            "Footer care",
            [
                ("FAQs", "/pages/faqs"),
                ("Contact Us", "/pages/contact"),
                ("Returns & Exchange Policy", "/policies/refund-policy"),
                ("Shipping Policy", "/policies/shipping-policy"),
                ("Privacy Policy", "/policies/privacy-policy"),
                ("Terms of Service", "/policies/terms-of-service"),
            ],
        ),
    ]:
        if handle in by_handle:
            print(f"  {handle} already exists")
            continue
        item_str = "\n".join(
            f'{{ title: "{t}", type: HTTP, url: "{u}" }}' for t, u in items
        )
        q = f"""
        mutation {{
          menuCreate(title: "{title}", handle: "{handle}", items: [{item_str}]) {{
            menu {{ id handle }}
            userErrors {{ field message }}
          }}
        }}
        """
        data = run_query(q, allow_mutations=True)
        print(f"  {handle}:", data.get("menuCreate", {}))


def main() -> int:
    create_collections()
    create_products()
    update_menus()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
