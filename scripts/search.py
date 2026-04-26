#!/usr/bin/env python3
"""Search the knowledge graph.

Usage:
    search.py [QUERY] [--type T] [--tag T] [--links-to ID] [--paths]

QUERY is a case-insensitive substring matched against name + body.
With no QUERY, the flags act as pure filters.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip3 install pyyaml")

DOCS = Path(__file__).resolve().parent.parent / "docs"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
ID_FIELDS = ("related", "influenced_by", "influenced")
TYPES = ("thinker", "school", "concept", "event", "topic")


def load_docs():
    docs = []
    for path in sorted(DOCS.rglob("*.md")):
        if path.name.startswith("_"):
            continue
        m = FRONTMATTER.match(path.read_text())
        if not m:
            continue
        meta = yaml.safe_load(m.group(1)) or {}
        body = m.group(2)
        docs.append((path, meta, body))
    return docs


def doc_links_to(meta, body, target):
    for field in ID_FIELDS:
        if target in (meta.get(field) or []):
            return True
    for link in WIKILINK.findall(body):
        if link == target:
            return True
    return False


def find_snippet(body, query, width=80):
    idx = body.lower().find(query.lower())
    if idx < 0:
        return None
    start = max(0, idx - width // 2)
    end = min(len(body), idx + len(query) + width // 2)
    snippet = body[start:end].replace("\n", " ").strip()
    snippet = re.sub(r"\s+", " ", snippet)
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(body) else ""
    return f"{prefix}{snippet}{suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="Search the knowledge graph.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               '  search.py "racial capitalism"\n'
               "  search.py --tag theology --type thinker\n"
               "  search.py --links-to rawls-john\n"
               '  search.py "abundance" --paths | xargs $EDITOR',
    )
    parser.add_argument("query", nargs="?", help="case-insensitive substring (name + body)")
    parser.add_argument("--type", choices=TYPES, help="filter by doc type")
    parser.add_argument("--tag", help="filter by tag")
    parser.add_argument("--links-to", metavar="ID", help="docs that reference this id (related/influenced_by/influenced or wikilink)")
    parser.add_argument("--paths", action="store_true", help="print only file paths")
    args = parser.parse_args()

    if not any([args.query, args.type, args.tag, args.links_to]):
        parser.error("provide a query or at least one filter")

    hits = []
    for path, meta, body in load_docs():
        if args.type and meta.get("type") != args.type:
            continue
        if args.tag and args.tag not in (meta.get("tags") or []):
            continue
        if args.links_to and not doc_links_to(meta, body, args.links_to):
            continue

        snippet = None
        if args.query:
            q = args.query.lower()
            name = (meta.get("name") or "").lower()
            if q in name:
                snippet = None  # name match — no body snippet needed
            elif q in body.lower():
                snippet = find_snippet(body, args.query)
            else:
                continue

        hits.append((path, meta, snippet))

    if args.paths:
        for path, _, _ in hits:
            print(path)
        return

    if not hits:
        print("No matches.", file=sys.stderr)
        sys.exit(1)

    width = max((len(m.get("id") or "") for _, m, _ in hits), default=0)
    for _, meta, snippet in hits:
        doc_type = meta.get("type") or "?"
        doc_id = meta.get("id") or "?"
        name = meta.get("name") or ""
        print(f"{doc_type:<8} {doc_id:<{width}}  {name}")
        if snippet:
            print(f"           ↳ {snippet}")


if __name__ == "__main__":
    main()
