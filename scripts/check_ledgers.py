#!/usr/bin/env python3
"""Validate the small, project-local ledgers used by research-co-thinking.

The loader accepts JSON and a deliberately limited YAML subset (lists/maps,
quoted or plain scalars, and inline lists).  It checks bookkeeping invariants;
it cannot prove mathematical correctness or semantic equivalence.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    severity: str
    file: str
    message: str
    entry: str | None = None

    def as_dict(self) -> dict[str, Any]:
        value = {"severity": self.severity, "file": self.file, "message": self.message}
        if self.entry:
            value["entry"] = self.entry
        return value


def _strip_comment(text: str) -> str:
    quoted: str | None = None
    escaped = False
    depth = 0
    for i, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quoted:
            escaped = True
            continue
        if quoted:
            if char == quoted:
                quoted = None
            continue
        if char in "'\"":
            quoted = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth = max(0, depth - 1)
        elif char == "#" and depth == 0 and (i == 0 or text[i - 1].isspace()):
            return text[:i].rstrip()
    return text.rstrip()


def _scalar(value: str) -> Any:
    value = _strip_comment(value.strip())
    if not value:
        return None
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        # Split commas outside quotes/brackets; recurse so plain YAML strings
        # such as [C-one, C-two] work without a YAML package.
        parts: list[str] = []
        start = 0
        quote: str | None = None
        depth = 0
        for i, char in enumerate(inner):
            if char in "'\"":
                if quote == char:
                    quote = None
                elif quote is None:
                    quote = char
            elif quote is None and char in "[{":
                depth += 1
            elif quote is None and char in "]}":
                depth -= 1
            elif quote is None and char == "," and depth == 0:
                parts.append(inner[start:i])
                start = i + 1
        parts.append(inner[start:])
        return [_scalar(part) for part in parts]
    if value.startswith("{") and value.endswith("}"):
        # JSON-like inline maps are enough for occasional metadata.
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value[1:-1]
    try:
        if re.fullmatch(r"[-+]?\d+", value):
            return int(value)
        if re.fullmatch(r"[-+]?(?:\d+\.\d*|\.\d+)(?:[eE][-+]?\d+)?", value):
            return float(value)
    except ValueError:
        pass
    return value


def _split_mapping(text: str) -> tuple[str, str] | None:
    quote: str | None = None
    depth = 0
    for i, char in enumerate(text):
        if char in "'\"":
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        elif quote is None and char in "[{":
            depth += 1
        elif quote is None and char in "]}":
            depth -= 1
        elif quote is None and char == ":" and depth == 0:
            key = text[:i].strip()
            if key:
                return key.strip("'\""), text[i + 1 :].strip()
    return None


def _yaml_lines(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for raw in text.splitlines():
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ValueError("tabs are not supported in the YAML subset")
        content = _strip_comment(raw).strip()
        if not content or content == "---" or content == "...":
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        result.append((indent, content))
    return result


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines) or lines[index][0] < indent:
        return None, index
    is_list = lines[index][1] == "-" or lines[index][1].startswith("- ")
    if is_list:
        values: list[Any] = []
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent != indent or not (content == "-" or content.startswith("- ")):
                break
            rest = content[1:].strip()
            index += 1
            if not rest:
                if index < len(lines) and lines[index][0] > indent:
                    child_indent = lines[index][0]
                    value, index = _parse_block(lines, index, child_indent)
                else:
                    value = None
            else:
                mapping = _split_mapping(rest)
                if mapping:
                    key, raw_value = mapping
                    value = {key: _scalar(raw_value)} if raw_value else {key: None}
                    # Merge continuation mapping fields belonging to this list item.
                    if index < len(lines) and lines[index][0] > indent:
                        child_indent = lines[index][0]
                        child, index = _parse_block(lines, index, child_indent)
                        if isinstance(child, dict):
                            value.update(child)
                        elif child is not None:
                            raise ValueError("list mapping continuation must be a mapping")
                    # A blank `key:` in a list item can itself have a nested block;
                    # this common case is handled by a second pass below only when
                    # the value is still None and the continuation is a sequence.
                    if value.get(key) is None and index < len(lines) and lines[index][0] > indent:
                        child_indent = lines[index][0]
                        child, index = _parse_block(lines, index, child_indent)
                        value[key] = child
                else:
                    value = _scalar(rest)
                    if index < len(lines) and lines[index][0] > indent:
                        raise ValueError("scalar list item cannot have an indented child")
            values.append(value)
        return values, index

    result: dict[str, Any] = {}
    while index < len(lines):
        current_indent, content = lines[index]
        if current_indent != indent or content.startswith("- "):
            break
        mapping = _split_mapping(content)
        if not mapping:
            raise ValueError(f"expected key: value, got {content!r}")
        key, raw_value = mapping
        index += 1
        if raw_value:
            result[key] = _scalar(raw_value)
        elif index < len(lines) and lines[index][0] > indent:
            child_indent = lines[index][0]
            result[key], index = _parse_block(lines, index, child_indent)
        else:
            result[key] = None
    return result, index


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        lines = _yaml_lines(text)
        if not lines:
            return None
        value, index = _parse_block(lines, 0, lines[0][0])
        if index != len(lines):
            raise ValueError(f"could not parse line {index + 1}")
        return value


def _entries(data: Any) -> list[dict[str, Any]]:
    if data is None:
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("items", "entries", "nodes", "records"):
            if isinstance(data.get(key), list):
                return [item for item in data[key] if isinstance(item, dict)]
        if data and all(isinstance(value, dict) for value in data.values()):
            result = []
            for key, value in data.items():
                item = dict(value)
                item.setdefault("id", key)
                result.append(item)
            return result
        return [data]
    return []


FILE_KIND = {
    "concepts": "concept",
    "symbols": "symbol",
    "claims": "claim",
    "evidence": "evidence",
    "decisions": "decision",
    "source-map": "artifact",
    "sources": "artifact",
    "terms": "term",
}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    files = sorted(
        p for p in root.iterdir() if p.is_file() and p.suffix.lower() in {".json", ".yaml", ".yml"}
    ) if root.exists() else []
    all_ids: dict[str, tuple[Path, str]] = {}
    loaded: dict[str, list[dict[str, Any]]] = {}

    if not root.exists():
        findings.append(Finding("error", str(root), "ledger directory does not exist"))
        return findings
    if not root.is_dir():
        findings.append(Finding("error", str(root), "ledger path is not a directory"))
        return findings

    for path in files:
        try:
            data = _load(path)
        except (OSError, ValueError, SyntaxError) as exc:
            findings.append(Finding("error", str(path), f"cannot parse ledger: {exc}"))
            continue
        entries = _entries(data)
        key = path.stem.lower()
        kind = FILE_KIND.get(key)
        loaded[key] = entries
        for number, entry in enumerate(entries, start=1):
            entry_id = entry.get("id")
            label = str(entry_id) if entry_id is not None else f"entry#{number}"
            if not entry_id:
                findings.append(Finding("error", str(path), "entry has no nonempty id", label))
            elif entry_id in all_ids:
                other_path, other_label = all_ids[entry_id]
                findings.append(Finding("error", str(path), f"duplicate id {entry_id!r}; already in {other_path} ({other_label})", label))
            else:
                all_ids[str(entry_id)] = (path, label)
            if kind == "symbol":
                for field in ("glyph", "object_id", "scope", "declared_in", "first_use"):
                    if not entry.get(field):
                        findings.append(Finding("error", str(path), f"symbol missing {field}", label))
            elif kind == "claim":
                if not entry.get("modality"):
                    findings.append(Finding("error", str(path), "claim missing modality", label))
                if "boundary" not in entry:
                    findings.append(Finding("warning", str(path), "claim has no explicit boundary (use none if genuinely unbounded)", label))
                if entry.get("status") in {"supported", "bounded"} and not (_as_list(entry.get("evidence_ids")) or _as_list(entry.get("qualifies_by"))):
                    findings.append(Finding("error", str(path), "supported/bounded claim has no evidence_ids or qualifies_by", label))
            elif kind == "evidence":
                for field in ("artifact_id", "conditions"):
                    if not entry.get(field):
                        findings.append(Finding("error", str(path), f"evidence missing {field}", label))
                if not entry.get("limitations"):
                    findings.append(Finding("warning", str(path), "evidence has no limitations field", label))
            elif kind == "decision":
                if not _as_list(entry.get("options")):
                    findings.append(Finding("error", str(path), "decision has no options", label))
                if not entry.get("rationale") and entry.get("status") not in {"open", "deferred"}:
                    findings.append(Finding("warning", str(path), "closed decision has no rationale", label))
                if "reversible" not in entry:
                    findings.append(Finding("warning", str(path), "decision should state reversible: true|false", label))
            elif kind == "term":
                if not entry.get("canonical_meaning") and not entry.get("meaning"):
                    findings.append(Finding("error", str(path), "term missing canonical_meaning/meaning", label))
                if "aliases" in entry and not isinstance(entry["aliases"], list):
                    findings.append(Finding("error", str(path), "term aliases must be a list", label))

    # Cross-reference checks are warnings: a branch may intentionally reference
    # an entry in a ledger not created yet, but the author should see it.
    reference_fields = {
        "object_id", "term_id", "artifact_id", "claim_id", "supports",
        "evidence_ids", "qualifies_by", "depends_on", "source_ids",
        "prerequisites", "next_section", "decision_id",
    }
    for key, entries in loaded.items():
        path = next((p for p in files if p.stem.lower() == key), root)
        for number, entry in enumerate(entries, start=1):
            label = str(entry.get("id") or f"entry#{number}")
            for field in reference_fields:
                if field not in entry:
                    continue
                for target in _as_list(entry[field]):
                    if isinstance(target, str) and target and target not in all_ids and not target.startswith(("http://", "https://", "#")):
                        findings.append(Finding("warning", str(path), f"{field} references unknown id {target!r}", label))

    # Source paths are checked without making them fatal: many ledgers point to
    # a repository root outside the state directory.
    for key in ("source-map", "sources"):
        for entry in loaded.get(key, []):
            source = entry.get("path")
            if not source or not isinstance(source, str) or source.startswith(("http://", "https://")):
                continue
            if not Path(source).expanduser().exists() and not (root / source).exists():
                findings.append(Finding("warning", str(root / f"{key}.yaml"), f"source path not found: {source}", str(entry.get("id") or "entry")))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="project-local .research-co-thinking directory")
    parser.add_argument("--json", action="store_true", help="emit machine-readable findings")
    parser.add_argument("--strict", action="store_true", help="return failure for warnings as well as errors")
    args = parser.parse_args()
    findings = validate(Path(args.directory))
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    if args.json:
        json.dump([item.as_dict() for item in findings], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if not findings:
            print("No ledger violations found (semantic correctness still needs human review).")
        else:
            for item in findings:
                suffix = f" [{item.entry}]" if item.entry else ""
                print(f"{item.severity.upper()}: {item.file}{suffix}: {item.message}")
        print(f"Summary: {errors} error(s), {warnings} warning(s)")
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

