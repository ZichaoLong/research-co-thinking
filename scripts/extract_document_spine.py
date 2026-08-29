#!/usr/bin/env python3
"""Extract a lightweight heading/paragraph spine from Markdown documents.

This is a navigation aid, not a Markdown or LaTeX parser.  It deliberately
reports candidates (headings, links, formulas, and first sentences) for human
review instead of claiming to understand mathematical semantics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


ATX_RE = re.compile(r"^( {0,3})(#{1,6})\s+(.+?)\s*#*\s*$")
SETEXT_RE = re.compile(r"^( {0,3})(=+|-+)\s*$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MDLINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORMULA_RE = re.compile(r"(?<![A-Za-z])(?:\$\$.*?\$\$|\$[^$\n]+\$|\\\([^\n]+?\\\))")


def _clean_inline(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _first_sentence(lines: list[str]) -> str:
    """Return a compact prose snippet from the first non-empty paragraph."""
    paragraph: list[str] = []
    in_fence = False
    in_front_matter = bool(lines and lines[0].strip() == "---")
    for number, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if in_front_matter:
            if number > 1 and line.strip() == "---":
                in_front_matter = False
            continue
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            in_fence = not in_fence
            if paragraph:
                break
            continue
        if in_fence:
            continue
        if not line.strip():
            if paragraph:
                break
            continue
        if ATX_RE.match(line) or line.lstrip().startswith("> [!"):
            if paragraph:
                break
            continue
        paragraph.append(line.strip())
    snippet = _clean_inline(" ".join(paragraph))
    if len(snippet) > 240:
        snippet = snippet[:237].rstrip() + "..."
    return snippet


def _looks_like_setext_title(text: str) -> bool:
    """Avoid treating an equation/table row as a setext heading."""
    if not text or len(text) > 200:
        return False
    # A genuine setext title is prose.  Mathematical display rows commonly
    # contain these delimiters; requiring their absence removes the noisy
    # false positives while retaining ordinary Markdown setext headings.
    return not any(token in text for token in ("$", "\\", "{", "}", "=", "|", "`"))


def extract(path: Path, *, include_formulas: bool = False, include_tree: bool = False) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    headings: list[dict] = []
    links: list[str] = []
    formulas: list[str] = []
    in_fence = False
    in_math_block = False
    in_front_matter = bool(lines and lines[0].strip() == "---")
    math_buffer: list[str] = []

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if in_front_matter:
            if number > 1 and stripped == "---":
                in_front_matter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped == "$$":
            if in_math_block:
                if math_buffer:
                    formulas.append("$$\n" + "\n".join(math_buffer) + "\n$$")
                    math_buffer = []
            in_math_block = not in_math_block
            continue
        if in_math_block:
            math_buffer.append(line.strip())
            continue
        match = ATX_RE.match(line)
        if match:
            headings.append(
                {
                    "level": len(match.group(2)),
                    "title": _clean_inline(match.group(3)),
                    "line": number,
                }
            )
            continue
        # Setext headings are represented by the preceding line.
        if SETEXT_RE.match(line) and headings is not None and number >= 2:
            previous = lines[number - 2].strip()
            if _looks_like_setext_title(previous) and not previous.startswith(("#", "-", "*", ">")):
                level = 1 if line.lstrip().startswith("=") else 2
                if not headings or headings[-1].get("line") != number - 1:
                    headings.append({"level": level, "title": _clean_inline(previous), "line": number - 1})
        links.extend(WIKILINK_RE.findall(line))
        links.extend(MDLINK_RE.findall(line))
        formulas.extend(FORMULA_RE.findall(line))

    record = {
        "path": str(path),
        "line_count": len(lines),
        "heading_count": len(headings),
        "max_heading_level": max((h["level"] for h in headings), default=0),
        "headings": headings,
        "first_snippet": _first_sentence(lines),
        "links": sorted(set(links)),
        "formula_candidate_count": len(formulas),
    }
    # These optional payloads can be large; keep them out of the normal
    # inventory so a long source does not consume the caller's context budget.
    if include_formulas:
        record["formula_candidates"] = [
            formula if len(formula) <= 400 else formula[:397] + "..."
            for formula in formulas[:20]
        ]
    if include_tree:
        tree: list[dict] = []
        stack: list[dict] = []
        for heading in headings:
            node = {**heading, "children": []}
            while stack and stack[-1]["level"] >= heading["level"]:
                stack.pop()
            if stack:
                stack[-1]["children"].append(node)
            else:
                tree.append(node)
            stack.append(node)
        record["tree"] = tree
    return record


def _iter_paths(items: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for item in items:
        path = Path(item)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.md")))
        elif path.exists():
            paths.append(path)
        else:
            print(f"warning: not found: {path}", file=sys.stderr)
    # Preserve user order while removing duplicates.
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            result.append(path)
    return result


def _limit_headings(record: dict, maximum: int) -> None:
    """Bound the serialized heading list while retaining both ends of a map."""
    headings = record.get("headings", [])
    if maximum <= 0 or len(headings) <= maximum:
        return
    keep_front = maximum // 2
    keep_back = maximum - keep_front
    omitted = len(headings) - keep_front - keep_back
    marker = {"level": 0, "title": f"…[{omitted} headings omitted; query a section with slice_document.py]…", "line": 0}
    record["headings"] = headings[:keep_front] + [marker] + headings[-keep_back:]
    record["headings_truncated"] = True
    record["headings_omitted"] = omitted


def _limit_links(record: dict, maximum: int) -> None:
    links = record.get("links", [])
    if maximum <= 0 or len(links) <= maximum:
        return
    keep_front = maximum // 2
    keep_back = maximum - keep_front
    omitted = len(links) - keep_front - keep_back
    record["links"] = links[:keep_front] + [f"…[{omitted} links omitted; query exact references as needed]…"] + links[-keep_back:]
    record["links_truncated"] = True
    record["links_omitted"] = omitted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown files or directories")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a readable outline")
    parser.add_argument("--include-formulas", action="store_true", help="include up to 20 truncated formula candidates")
    parser.add_argument("--tree", action="store_true", help="include a nested heading tree in JSON")
    parser.add_argument("--max-headings", type=int, default=300, help="maximum headings serialized per file; 0 means all")
    parser.add_argument("--max-links", type=int, default=100, help="maximum links serialized per file; 0 means all")
    args = parser.parse_args()
    paths = _iter_paths(args.paths)
    if not paths:
        return 2
    records = [extract(path, include_formulas=args.include_formulas, include_tree=args.tree) for path in paths]
    for record in records:
        _limit_headings(record, args.max_headings)
        _limit_links(record, args.max_links)
    if args.json:
        json.dump(records if len(records) > 1 else records[0], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    for index, record in enumerate(records):
        if index:
            print()
        print(f"{record['path']} ({record['line_count']} lines, {record['heading_count']} headings)")
        if record["first_snippet"]:
            print(f"  intro: {record['first_snippet']}")
        for heading in record["headings"]:
            if heading["level"] == 0:
                print(f"  {heading['title']}")
            else:
                print(f"  {'  ' * (heading['level'] - 1)}- L{heading['line']}: {heading['title']}")
        if record["links"]:
            print(f"  links: {', '.join(record['links'][:12])}")
        if record["formula_candidate_count"]:
            print(f"  formula candidates: {record['formula_candidate_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
