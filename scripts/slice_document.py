#!/usr/bin/env python3
"""Print bounded, line-addressable windows from a Markdown/LaTeX document.

Use this after extracting a spine.  The command intentionally returns a small
window rather than a whole source file, and labels truncation so a caller does
not mistake an excerpt for a complete proof or specification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ATX_RE = re.compile(r"^( {0,3})(#{1,6})\s+(.+?)\s*#*\s*$")
SETEXT_RE = re.compile(r"^( {0,3})(=+|-+)\s*$")


def _clean_title(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).strip("# ")


def _prose_title(text: str) -> bool:
    if not text or len(text) > 200:
        return False
    return not any(token in text for token in ("$", "\\", "{", "}", "=", "|", "`"))


def headings(lines: list[str]) -> list[dict[str, int | str]]:
    result: list[dict[str, int | str]] = []
    in_fence = False
    in_math = False
    in_front = bool(lines and lines[0].strip() == "---")
    for number, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if in_front:
            if number > 1 and stripped == "---":
                in_front = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped == "$$":
            in_math = not in_math
            continue
        if in_math:
            continue
        match = ATX_RE.match(line)
        if match:
            result.append({"level": len(match.group(2)), "title": _clean_title(match.group(3)), "line": number})
            continue
        if SETEXT_RE.match(line) and number >= 2:
            previous = lines[number - 2].strip()
            if _prose_title(previous) and not previous.startswith(("#", "-", "*", ">")):
                result.append({"level": 1 if line.lstrip().startswith("=") else 2, "title": _clean_title(previous), "line": number - 1})
    return result


def _section_range(items: list[dict[str, int | str]], index: int, line_count: int, children: bool) -> tuple[int, int]:
    selected = items[index]
    level = int(selected["level"])
    start = int(selected["line"])
    end = line_count
    for later in items[index + 1 :]:
        later_level = int(later["level"])
        if (children and later_level <= level) or (not children):
            end = int(later["line"]) - 1
            break
    return start, max(start, end)


def _parse_range(value: str, line_count: int) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*(?::|-)\s*(\d+)\s*", value)
    if not match:
        raise ValueError("line range must look like START:END (1-indexed, inclusive)")
    start, end = int(match.group(1)), int(match.group(2))
    if start < 1 or end < start:
        raise ValueError("line range must satisfy 1 <= START <= END")
    return min(start, line_count), min(end, line_count)


def _bounded(lines: list[str], start: int, end: int, max_chars: int) -> tuple[list[tuple[int, str]], bool]:
    selected = [(number, lines[number - 1]) for number in range(start, end + 1)]
    if max_chars <= 0:
        return selected, False
    # `_render` uses an eight-character line-number prefix (`"%6d: "`).
    # Reserve that prefix even when the caller later asks for unnumbered text;
    # a conservative cap is preferable to an accidentally oversized excerpt.
    def cost(item: tuple[int, str]) -> int:
        number, text = item
        return len(text) + (8 if number else 1)

    def rendered_cost(items: list[tuple[int, str]]) -> int:
        # `_render` joins lines with one newline but does not add a trailing one.
        return sum(cost(item) for item in items) + max(0, len(items) - 1)

    rendered = rendered_cost(selected)
    if rendered <= max_chars:
        return selected, False

    # Keep a larger prefix because it normally contains declarations, and a
    # suffix because it often contains the local consequence/boundary. Reserve
    # space for the omission marker before selecting either side.
    marker_reserve = min(120, max(1, max_chars // 5))
    available = max(1, max_chars - marker_reserve)
    head_budget = max(1, int(available * 0.60))
    tail_budget = max(1, available - head_budget)

    def take_front(budget: int) -> list[tuple[int, str]]:
        result: list[tuple[int, str]] = []
        used = 0
        for number, text in selected:
            item_cost = cost((number, text))
            if result and used + item_cost > budget:
                break
            if not result and item_cost > budget:
                keep = max(1, budget - 8)
                result.append((number, text[:keep] + " …[line truncated]"))
                break
            result.append((number, text))
            used += item_cost
        return result

    def take_back(budget: int) -> list[tuple[int, str]]:
        result: list[tuple[int, str]] = []
        used = 0
        for number, text in reversed(selected):
            item_cost = cost((number, text))
            if result and used + item_cost > budget:
                break
            if not result and item_cost > budget:
                keep = max(1, budget - 8)
                result.append((number, "…[line truncated] " + text[-keep:]))
                break
            result.append((number, text))
            used += item_cost
        result.reverse()
        return result

    head = take_front(head_budget)
    tail = take_back(tail_budget)

    omitted_start = head[-1][0] + 1 if head else start
    omitted_end = tail[0][0] - 1 if tail else end
    marker_text = f"…[{omitted_start}-{omitted_end} lines omitted; retrieve that range for exact detail]…"
    marker = [(0, marker_text)]

    # Tighten the result if long line-number prefixes or a short max_chars
    # value left it above the advertised soft cap. Remove context lines before
    # shortening the retained boundary lines.
    while True:
        cost_items = rendered_cost(head + marker + tail)
        if cost_items <= max_chars:
            break
        if len(head) > 1:
            head.pop()
        elif len(tail) > 1:
            tail.pop(0)
        else:
            # The remaining boundary lines may themselves be unusually long.
            # Shorten one line by the measured excess so every iteration makes
            # progress; for an extremely tiny cap, a locator-only marker is
            # more honest than returning an over-sized or unlabeled excerpt.
            excess = cost_items - max_chars
            shortened = False
            for collection, position in ((head, -1), (tail, 0)):
                if not collection:
                    continue
                number, text = collection[position]
                if len(text) > 1:
                    suffix = " …"
                    keep = max(1, len(text) - max(excess, len(suffix)))
                    shortened_text = text[:keep] + suffix
                    if len(shortened_text) >= len(text):
                        shortened_text = text[: max(1, len(text) - 1)]
                    collection[position] = (number, shortened_text)
                    shortened = True
                    break
            if not shortened:
                marker_text = marker[0][1]
                marker_limit = max(1, max_chars - 2)
                marker[0] = (0, marker_text[:marker_limit] + "…")
                if rendered_cost(head + marker + tail) > max_chars:
                    # No retained line can fit alongside the marker. Return a
                    # bounded locator; callers can request the omitted range.
                    if max_chars == 1:
                        return [(0, "")], True
                    return [(0, marker[0][1][: max(1, max_chars - 1)])], True
    return head + marker + tail, True


def _render(items: list[tuple[int, str]], line_numbers: bool) -> str:
    if line_numbers:
        return "\n".join(("…" if number == 0 else f"{number:>6}: ") + text for number, text in items)
    return "\n".join(text for number, text in items if number != 0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Markdown/LaTeX/text document")
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--heading", help="regular expression matched against heading titles")
    selector.add_argument("--lines", help="inclusive 1-indexed range, e.g. 120:180")
    selector.add_argument("--list", action="store_true", help="list headings and their approximate ranges")
    parser.add_argument("--all", action="store_true", help="return all matching headings (default: first)")
    parser.add_argument("--no-children", action="store_true", help="for --heading, stop at the next heading of any level")
    parser.add_argument("--context", type=int, default=0, help="extra lines before/after the selected range")
    parser.add_argument("--max-chars", type=int, default=16000, help="soft cap on returned, numbered text")
    parser.add_argument("--no-line-numbers", action="store_true", help="omit source line labels")
    parser.add_argument("--json", action="store_true", help="emit metadata and excerpt as JSON")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists() or not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    if not lines:
        print("error: document is empty", file=sys.stderr)
        return 2
    items = headings(lines)

    if args.list:
        output: list[dict[str, int | str]] = []
        for index, item in enumerate(items):
            start, end = _section_range(items, index, len(lines), True)
            output.append({**item, "start_line": start, "end_line": end, "char_count": sum(len(x) + 1 for x in lines[start - 1 : end])})
        if args.json:
            json.dump({"path": str(path), "line_count": len(lines), "headings": output}, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"{path} ({len(lines)} lines, {len(output)} headings)")
            for item in output:
                print(f"L{item['line']:<6} H{item['level']} {item['title']}  [{item['start_line']}–{item['end_line']}, {item['char_count']} chars]")
        return 0

    try:
        if args.lines:
            start, end = _parse_range(args.lines, len(lines))
            selections = [(start, end, f"lines {start}:{end}")]
        elif args.heading:
            pattern = re.compile(args.heading, re.IGNORECASE)
            matches = [index for index, item in enumerate(items) if pattern.search(str(item["title"]))]
            if not matches:
                print(f"error: no heading matched {args.heading!r}", file=sys.stderr)
                return 1
            if not args.all:
                matches = matches[:1]
            selections = []
            for index in matches:
                start, end = _section_range(items, index, len(lines), not args.no_children)
                selections.append((start, end, f"heading {items[index]['title']!r} @L{items[index]['line']}"))
        else:
            parser.error("choose one of --heading, --lines, or --list")
            return 2
    except (ValueError, re.error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.context < 0:
        print("error: --context must be nonnegative", file=sys.stderr)
        return 2
    records: list[dict[str, object]] = []
    rendered_parts: list[str] = []
    for original_start, original_end, label in selections:
        start = max(1, original_start - args.context)
        end = min(len(lines), original_end + args.context)
        excerpt, truncated = _bounded(lines, start, end, args.max_chars)
        text = _render(excerpt, not args.no_line_numbers)
        records.append(
            {
                "path": str(path),
                "selector": label,
                "requested_start_line": original_start,
                "requested_end_line": original_end,
                "returned_start_line": start,
                "returned_end_line": end,
                "max_chars": args.max_chars,
                "truncated": truncated,
                "excerpt": text,
            }
        )
        rendered_parts.append(f"# {path} — {label} ({start}:{end}; truncated={str(truncated).lower()})\n{text}")
    if args.json:
        result: object = records[0] if len(records) == 1 else records
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print("\n\n".join(rendered_parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
