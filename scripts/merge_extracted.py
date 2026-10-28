"""Merge data/extracted/batch_*.jsonl into data/calques.jsonl, validating and de-duplicating.

Usage: python3 scripts/merge_extracted.py
"""
import glob
import json
import re
import sys
from collections import Counter

CATEGORIES = {"lexical", "phrase", "grammar", "word-order", "bureaucratic", "spelling", "style"}
KINDS = {"pair", "rule"}
CONFIDENCE = {"high", "medium", "low"}


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower().strip(".,!?…\"'«»"))


def main():
    entries, problems = [], []
    for path in sorted(glob.glob("data/extracted/batch_*.jsonl")):
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError as err:
                problems.append(f"{path}:{n} bad json: {err}")
                continue
            if e.get("kind") not in KINDS:
                problems.append(f"{path}:{n} kind={e.get('kind')!r}")
            if e.get("category") not in CATEGORIES:
                problems.append(f"{path}:{n} category={e.get('category')!r}")
            if e.get("confidence") not in CONFIDENCE:
                problems.append(f"{path}:{n} confidence={e.get('confidence')!r}")
            if not isinstance(e.get("correct", []), list):
                e["correct"] = [e["correct"]] if e.get("correct") else []
            e["source"] = f"https://t.me/kalkastop/{e['post']}"
            entries.append(e)

    # Drop exact duplicate pairs; keep the earliest post, remember the others as extra sources.
    by_key, merged = {}, []
    for e in sorted(entries, key=lambda e: e["post"]):
        if e["kind"] == "pair" and e.get("wrong"):
            key = norm(e["wrong"])
            if key in by_key:
                first = by_key[key]
                first.setdefault("also", []).append(e["source"])
                for c in e.get("correct", []):
                    if norm(c) not in {norm(x) for x in first["correct"]}:
                        first["correct"].append(c)
                continue
            by_key[key] = e
        merged.append(e)

    with open("data/calques.jsonl", "w", encoding="utf-8") as f:
        for e in merged:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"raw entries: {len(entries)}  after dedupe: {len(merged)}")
    print("kind:", dict(Counter(e["kind"] for e in merged)))
    print("category:", dict(Counter(e.get("category") for e in merged)))
    print("confidence:", dict(Counter(e.get("confidence") for e in merged)))
    print("posts covered:", len({e["post"] for e in merged}))
    if problems:
        print(f"\n{len(problems)} problems:", *problems[:30], sep="\n  ", file=sys.stderr)


if __name__ == "__main__":
    main()
