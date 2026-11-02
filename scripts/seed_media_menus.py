#!/usr/bin/env python3
"""Upload theme media, assign collection images, rebuild menus with nested links."""
from __future__ import annotations

import json
import subprocess
import sys
import time

STORE = "home-gadget-2kk1camr.myshopify.com"
AGENT = "n:cursor|v:1.0|p:cursor|m:composer"

# Royalty-free Unsplash (already used for products) + extras for banners/trust
MEDIA = [
    ("hz-hero-1.jpg", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1800&q=80", "Hero luxury watch wrist"),
    ("hz-hero-2.jpg", "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?auto=format&fit=crop&w=1800&q=80", "Hero sale watch close-up"),
    ("hz-banner-men.jpg", "https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1400&q=80", "Men watches collection"),
    ("hz-banner-women.jpg", "https://images.unsplash.com/photo-1611652022419-a9419f74343d?auto=format&fit=crop&w=1400&q=80", "Women watches collection"),
    ("hz-banner-couples.jpg", "https://images.unsplash.com/photo-1600003014755-ba31aa59c4b6?auto=format&fit=crop&w=1400&q=80", "Couple watches"),
    ("hz-banner-gifts.jpg", "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1400&q=80", "Gift / best sellers"),
    ("hz-cat-sale.jpg", "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80", "Sale category"),
    ("hz-cat-formal.jpg", "https://images.unsplash.com/photo-1533139502658-0198f920d8e8?auto=format&fit=crop&w=800&q=80", "Men formal"),
    ("hz-cat-sports.jpg", "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&w=800&q=80", "Sports / smart"),
    ("hz-cat-women.jpg", "https://images.unsplash.com/photo-1612817159949-195b6eb9e31a?auto=format&fit=crop&w=800&q=80", "Women category"),
    ("hz-cat-bracelet.jpg", "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80", "Bracelet watches"),
    ("hz-cat-smart.jpg", "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?auto=format&fit=crop&w=800&q=80", "Smart watches"),
    ("hz-cat-couples.jpg", "https://images.unsplash.com/photo-1600003014755-ba31aa59c4b6?auto=format&fit=crop&w=800&q=80", "Couples category"),
    ("hz-tile-quartz.jpg", "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1000&q=80", "Classic quartz tile"),
    ("hz-tile-men.jpg", "https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1000&q=80", "Men quartz tile"),
    ("hz-tile-elite.jpg", "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?auto=format&fit=crop&w=1000&q=80", "Elite quartz tile"),
    ("hz-tile-smart.jpg", "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&w=1000&q=80", "Smart tile"),
    ("hz-tile-women.jpg", "https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?auto=format&fit=crop&w=1000&q=80", "Women quartz tile"),
    ("hz-tile-couples.jpg", "https://images.unsplash.com/photo-1600003014755-ba31aa59c4b6?auto=format&fit=crop&w=1000&q=80", "Couples tile"),
    ("hz-review-1.jpg", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80", "Review avatar Ayesha"),
    ("hz-review-2.jpg", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80", "Review avatar Bilal"),
    ("hz-review-3.jpg", "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=400&q=80", "Review avatar Sana"),
    ("hz-trust-cod.png", "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=400&q=80", "Trust COD"),
    ("hz-trust-ship.png", "https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?auto=format&fit=crop&w=400&q=80", "Trust shipping"),
    ("hz-trust-secure.png", "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=400&q=80", "Trust secure"),
    ("hz-trust-warranty.png", "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=400&q=80", "Trust warranty"),
    ("hz-video-poster.jpg", "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=1600&q=80", "Watch shop video poster"),
]

COLLECTION_IMAGES = {
    "frontpage": "hz-hero-1.jpg",
    "sale": "hz-cat-sale.jpg",
    "men": "hz-banner-men.jpg",
    "men-stainless-steel": "hz-banner-men.jpg",
    "men-leather": "hz-tile-men.jpg",
    "men-sports": "hz-cat-sports.jpg",
    "men-formal": "hz-cat-formal.jpg",
    "women": "hz-banner-women.jpg",
    "women-bracelet": "hz-cat-bracelet.jpg",
    "women-stainless-steel": "hz-cat-women.jpg",
    "women-leather": "hz-tile-women.jpg",
    "smart-watches": "hz-cat-smart.jpg",
    "couples": "hz-banner-couples.jpg",
    "best-sellers": "hz-banner-gifts.jpg",
    "new-arrival": "hz-hero-2.jpg",
}


def run_gql(query: str, allow_mutations: bool = False) -> dict:
    import os

    cmd = [
        "shopify",
        "store",
        "execute",
        "--store",
        STORE,
        "--version",
        "2026-01",
        "--json",
        "--query",
        query,
    ]
    if allow_mutations:
        # Insert after "execute"
        cmd.insert(3, "--allow-mutations")
    full_env = {**os.environ, "SHOPIFY_CLI_AGENT_INFO": AGENT}
    proc = subprocess.run(cmd, capture_output=True, text=True, env=full_env)
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    blob = out or err
    start = blob.find("{")
    end = blob.rfind("}")
    if start == -1 or end == -1:
        print("CMD:", " ".join(cmd[:8]), "...", file=sys.stderr)
        print(err or out, file=sys.stderr)
        raise RuntimeError(f"No JSON in response (exit {proc.returncode})")
    data = json.loads(blob[start : end + 1])
    return data


def upload_files() -> dict[str, str]:
    """Returns filename -> shopify://shop_images/filename"""
    files_payload = []
    for filename, url, alt in MEDIA:
        files_payload.append(
            {
                "originalSource": url,
                "filename": filename,
                "alt": alt,
                "contentType": "IMAGE",
                "duplicateResolutionMode": "REPLACE",
            }
        )

    # Batch in chunks of 10
    mapping: dict[str, str] = {}
    for i in range(0, len(files_payload), 10):
        chunk = files_payload[i : i + 10]
        # Build inline mutation without variables (CLI limitation)
        items = []
        for f in chunk:
            items.append(
                "{ originalSource: %s, filename: %s, alt: %s, contentType: IMAGE, duplicateResolutionMode: REPLACE }"
                % (
                    json.dumps(f["originalSource"]),
                    json.dumps(f["filename"]),
                    json.dumps(f["alt"]),
                )
            )
        mutation = (
            "mutation { fileCreate(files: [%s]) { files { id fileStatus alt ... on MediaImage { image { url } } } userErrors { field message } } }"
            % ", ".join(items)
        )
        print(f"Uploading files {i+1}-{i+len(chunk)}...")
        data = run_gql(mutation, allow_mutations=True)
        errs = data.get("fileCreate", {}).get("userErrors") or []
        if errs:
            print("fileCreate errors:", errs, file=sys.stderr)
        for f in data.get("fileCreate", {}).get("files") or []:
            # filename from URL path after ready
            pass
        for fmeta in chunk:
            mapping[fmeta["filename"]] = f"shopify://shop_images/{fmeta['filename']}"
        time.sleep(1)
    return mapping


def wait_files_ready(filenames: list[str], tries: int = 20) -> None:
    for _ in range(tries):
        q = (
            'query { files(first: 100, query: "filename:hz-*") { nodes { ... on MediaImage { id fileStatus alt image { url } } } } }'
        )
        data = run_gql(q)
        nodes = data.get("files", {}).get("nodes") or []
        statuses = {}
        for n in nodes:
            url = (n.get("image") or {}).get("url") or ""
            for name in filenames:
                if name in url or name.replace(".", "_") in url:
                    statuses[name] = n.get("fileStatus")
        ready = sum(1 for name in filenames if statuses.get(name) == "READY")
        print(f"Files ready: {ready}/{len(filenames)} tracked")
        if ready >= min(5, len(filenames) // 2):
            # enough for collections; continue even if some still processing
            if ready >= len(filenames) * 0.7 or _ > 12:
                return
        time.sleep(2)


def set_collection_images() -> None:
    q = "query { collections(first: 50) { nodes { id handle } } }"
    cols = {n["handle"]: n["id"] for n in run_gql(q)["collections"]["nodes"]}
    for handle, filename in COLLECTION_IMAGES.items():
        cid = cols.get(handle)
        if not cid:
            print(f"skip missing collection {handle}")
            continue
        src = f"shopify://shop_images/{filename}"
        # collectionUpdate image via CollectionInput.image.src — often needs CDN URL after READY
        # Use original Unsplash URL as fallback source for collection image
        unsplash = next((u for f, u, _ in MEDIA if f == filename), None)
        if not unsplash:
            continue
        mutation = (
            'mutation { collectionUpdate(input: { id: %s, image: { src: %s, altText: %s } }) { collection { id handle image { url } } userErrors { field message } } }'
            % (json.dumps(cid), json.dumps(unsplash), json.dumps(handle))
        )
        print(f"Collection image: {handle}")
        data = run_gql(mutation, allow_mutations=True)
        errs = data.get("collectionUpdate", {}).get("userErrors") or []
        if errs:
            print("  errors:", errs)


def update_menus() -> None:
    # Fetch page + collection IDs for COLLECTION/PAGE types when possible
    pages = {
        n["handle"]: n["id"]
        for n in run_gql('query { pages(first: 50) { nodes { id handle } } }')["pages"]["nodes"]
    }
    cols = {
        n["handle"]: n["id"]
        for n in run_gql("query { collections(first: 50) { nodes { id handle } } }")["collections"]["nodes"]
    }
    products = {
        n["handle"]: n["id"]
        for n in run_gql("query { products(first: 50) { nodes { id handle } } }")["products"]["nodes"]
    }

    def http(title: str, path: str) -> str:
        return '{ title: %s, type: HTTP, url: %s }' % (json.dumps(title), json.dumps(path))

    def page_item(title: str, handle: str) -> str:
        if handle in pages:
            return '{ title: %s, type: PAGE, resourceId: %s }' % (
                json.dumps(title),
                json.dumps(pages[handle]),
            )
        return http(title, f"/pages/{handle}")

    def col_item(title: str, handle: str, children: list[str] | None = None) -> str:
        kids = ""
        if children:
            kids = ", items: [%s]" % ", ".join(children)
        if handle in cols:
            return '{ title: %s, type: COLLECTION, resourceId: %s%s }' % (
                json.dumps(title),
                json.dumps(cols[handle]),
                kids,
            )
        return '{ title: %s, type: HTTP, url: %s%s }' % (
            json.dumps(title),
            json.dumps(f"/collections/{handle}"),
            kids,
        )

    def prod_item(title: str, handle: str) -> str:
        if handle in products:
            return '{ title: %s, type: PRODUCT, resourceId: %s }' % (
                json.dumps(title),
                json.dumps(products[handle]),
            )
        return http(title, f"/products/{handle}")

    main_items = [
        http("Home", "/"),
        col_item(
            "Men Watches",
            "men",
            [
                col_item("All Men", "men"),
                col_item("Stainless Steel", "men-stainless-steel"),
                col_item("Leather", "men-leather"),
                col_item("Sports", "men-sports"),
                col_item("Formal", "men-formal"),
            ],
        ),
        col_item(
            "Women Watches",
            "women",
            [
                col_item("All Women", "women"),
                col_item("Bracelet", "women-bracelet"),
                col_item("Stainless Steel", "women-stainless-steel"),
                col_item("Leather", "women-leather"),
            ],
        ),
        col_item("Smart Watches", "smart-watches"),
        col_item("For Couples", "couples"),
        col_item("Best Sellers", "best-sellers"),
        col_item("New Arrival", "new-arrival"),
        col_item("Sale", "sale"),
        http("All Products", "/collections/all"),
        page_item("Track Order", "track-order"),
        page_item("Contact Us", "contact"),
        page_item("About Us", "about"),
    ]

    footer_shop = [
        col_item("Sale", "sale"),
        col_item("Smartwatches", "smart-watches"),
        col_item("New Arrival", "new-arrival"),
        col_item("Men Watches", "men"),
        col_item("Ladies Watches", "women"),
        col_item("Couple Watches", "couples"),
        col_item("Best Sellers", "best-sellers"),
        http("All Products", "/collections/all"),
    ]

    footer_care = [
        page_item("About Us", "about"),
        page_item("Contact Us", "contact"),
        page_item("Track Order", "track-order"),
        page_item("Shipping Policy", "shipping-policy"),
        page_item("Refund & Exchange Policy", "refund-policy"),
        page_item("Privacy Policy", "privacy-policy"),
        page_item("Terms of Service", "terms-of-service"),
    ]

    footer_about = [
        page_item("About Us", "about"),
        http("All Collections", "/collections"),
        prod_item("Northline | 40mm", "horizon-northline-40"),
        prod_item("Pulse Smart", "horizon-pulse-smart"),
        prod_item("Duo Empire Set", "horizon-duo-empire"),
        http("Search", "/search"),
    ]

    menus = run_gql('query { menus(first: 20) { nodes { id handle } } }')["menus"]["nodes"]
    by_handle = {m["handle"]: m["id"] for m in menus}

    updates = [
        ("main-menu", "Main menu", main_items),
        ("footer-shop", "Footer shop", footer_shop),
        ("footer-care", "Footer care", footer_care),
        ("footer", "Footer menu", footer_about),
    ]

    for handle, title, items in updates:
        mid = by_handle.get(handle)
        if not mid:
            print(f"menu missing: {handle}")
            continue
        mutation = (
            "mutation { menuUpdate(id: %s, title: %s, items: [%s]) { menu { id handle items { title url items { title url } } } userErrors { field message } } }"
            % (json.dumps(mid), json.dumps(title), ", ".join(items))
        )
        print(f"Updating menu {handle}...")
        data = run_gql(mutation, allow_mutations=True)
        errs = data.get("menuUpdate", {}).get("userErrors") or []
        if errs:
            print("  errors:", errs)
        else:
            print("  ok")


def main() -> None:
    mapping = upload_files()
    print("Image mapping:", json.dumps(mapping, indent=2))
    wait_files_ready(list(mapping.keys()))
    set_collection_images()
    update_menus()
    # Write mapping for theme JSON wiring
    out_path = "/Users/digixoft/Documents/random thing images/homegadget/data/hz-shop-images.json"
    with open(out_path, "w") as f:
        json.dump(mapping, f, indent=2)
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
