#!/usr/bin/env python3
"""NEXTART 뉴스 자동 수집 — AI/XR/서울링/한탄강 키워드 RSS/검색"""
import json, os, re, urllib.request
from datetime import datetime

KEYWORDS = ["AI 이미지", "XR 인터랙티브", "서울링", "한탄강", "VFX", "ComfyUI", "Runway", "Pika", "LIDAR"]
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "news.json")

def fetch_rss(url, source_name):
    """Simple RSS fetch (no external deps)."""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NEXTART-NewsBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode("utf-8", errors="replace")
        # Minimal XML parse for <item><title>...<link>...<pubDate>
        for m in re.finditer(r"<item>(.*?)</item>", text, re.DOTALL):
            block = m.group(1)
            title = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", block)
            link = re.search(r"<link>(.*?)</link>", block)
            date = re.search(r"<pubDate>(.*?)</pubDate>", block)
            if title:
                items.append({
                    "source": source_name,
                    "title": title.group(1).strip(),
                    "url": link.group(1).strip() if link else "",
                    "date": date.group(1).strip()[:16] if date else "",
                })
    except Exception as e:
        print(f"[{source_name}] RSS fetch failed: {e}")
    return items

def main():
    all_items = []
    # Example RSS feeds (replace with actual feeds)
    feeds = [
        ("https://news.google.com/rss/search?q=AI+이미지+생성&hl=ko&gl=KR&ceid=KR:ko", "Google News"),
        ("https://news.google.com/rss/search?q=XR+인터랙티브&hl=ko&gl=KR&ceid=KR:ko", "Google News"),
    ]
    for url, name in feeds:
        items = fetch_rss(url, name)
        all_items.extend(items[:5])

    # Dedupe by title
    seen = set()
    unique = []
    for item in all_items:
        key = item["title"][:50]
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Save
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(unique[:20], f, ensure_ascii=False, indent=2)
    print(f"Saved {len(unique)} news items to {OUTPUT}")

if __name__ == "__main__":
    main()
