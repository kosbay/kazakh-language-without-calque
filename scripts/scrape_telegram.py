"""Scrape text posts from a public Telegram channel via its web preview (t.me/s/<channel>).

Usage: python3 scripts/scrape_telegram.py kalkastop data/raw/kalkastop.jsonl
No login needed. Only text is saved; posts with photos are flagged.
"""
import html
import json
import re
import sys
import subprocess
import time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def fetch(url):
    # curl uses the system certificate store, which is more reliable than Python's on macOS.
    for attempt in range(5):
        r = subprocess.run(["curl", "-sSfL", "--max-time", "30", "-A", UA, url], capture_output=True)
        if r.returncode == 0:
            return r.stdout.decode("utf-8")
        print(f"  retry {attempt + 1}: {r.stderr.decode().strip()}", file=sys.stderr)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"failed: {url}")


def inner_div(chunk, start):
    """Return the inner HTML of the <div> opening at `start`, handling nested divs."""
    i = chunk.index(">", start) + 1
    depth, pos = 1, i
    for m in re.finditer(r"<(/?)div\b", chunk[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return chunk[i : i + m.start()]
    return chunk[i:]


def to_text(fragment):
    fragment = re.sub(r"<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(fragment).strip()


def parse(page, channel):
    posts = []
    parts = re.split(rf'(?=<div class="tgme_widget_message [^"]*"[^>]*data-post="{channel}/)', page)
    for chunk in parts[1:]:
        pid = int(re.search(rf'data-post="{channel}/(\d+)"', chunk).group(1))
        m = re.search(r'<div class="tgme_widget_message_text[^"]*"', chunk)
        text = to_text(inner_div(chunk, m.start())) if m else ""
        date = re.search(r'<time datetime="([^"]+)"', chunk)
        posts.append({
            "id": pid,
            "url": f"https://t.me/{channel}/{pid}",
            "date": date.group(1) if date else None,
            "text": text,
            "has_photo": "tgme_widget_message_photo" in chunk,
            "is_forward": "tgme_widget_message_forwarded_from" in chunk,
        })
    return posts


def main(channel, out_path):
    seen, before = {}, None
    while True:
        url = f"https://t.me/s/{channel}" + (f"?before={before}" if before else "")
        posts = [p for p in parse(fetch(url), channel) if p["id"] not in seen]
        if not posts:
            break
        for p in posts:
            seen[p["id"]] = p
        before = min(p["id"] for p in posts)
        print(f"before={before} total={len(seen)}", file=sys.stderr)
        time.sleep(1.0)
    with open(out_path, "w", encoding="utf-8") as f:
        for pid in sorted(seen):
            f.write(json.dumps(seen[pid], ensure_ascii=False) + "\n")
    print(f"saved {len(seen)} posts to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
