"""Verify that translated patchnote files respect the glossary.

Usage:
    python tools/verify_glossary.py <glossary.md> <translated_dir>

Reports:
  - Translated files where a `keep`-category term from the glossary is
    referenced (by topic) but does NOT appear in its English form.
  - Unresolved placeholder markers: `[?]`, `TODO`, `TBD`.

Exit code: 0 if clean, 1 if any violations.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Term:
    en: str
    ru: str
    category: str  # "keep" | "translate"


@dataclass(frozen=True)
class Violation:
    file: Path
    term: str
    reason: str


@dataclass(frozen=True)
class Marker:
    file: Path
    line_number: int
    kind: str  # "[?]" | "TODO" | "TBD"
    line: str


_TABLE_ROW = re.compile(
    r"^\|[ \t]*([^|\n]+?)[ \t]*\|[ \t]*([^|\n]+?)[ \t]*\|[ \t]*(keep|translate)[ \t]*\|[ \t]*$",
    re.MULTILINE,
)


def parse_glossary(path: Path) -> list[Term]:
    """Extract terms from a markdown glossary's pipe tables."""
    text = path.read_text(encoding="utf-8")
    terms: list[Term] = []
    for m in _TABLE_ROW.finditer(text):
        en, ru, cat = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if en.upper() == "EN" or en.startswith("---"):
            continue
        terms.append(Term(en=en, ru=ru, category=cat))
    return terms


def find_keep_term_violations(translated: Path, glossary: list[Term]) -> list[Violation]:
    """Flag a keep-term as violated if its RU/translated form appears
    in the file but its English form does not appear AT ALL.

    Detection is conservative. Standard case (RU == EN) is skipped — we
    can't easily detect topic-referenced terms without LLM-level context.

    For known common bad translations we use a small hardcoded list. This
    is a heuristic ("review hint"), not a hard failure.
    """
    text = translated.read_text(encoding="utf-8")
    violations: list[Violation] = []
    for t in glossary:
        if t.category != "keep":
            continue
        if t.en == t.ru:
            continue
        if t.ru in text and t.en not in text:
            violations.append(Violation(
                file=translated,
                term=t.en,
                reason=f"RU form '{t.ru}' appears but EN form '{t.en}' not found",
            ))
    known_bad_translations = {
        "Изменчивая Смерть": "Volatile Dead",
        "Спарк": "Spark",
        "Огненный Урон": "Fire Damage",
        "Огненного Урона": "Fire Damage",
        "Холодный Урон": "Cold Damage",
        "Холодного Урона": "Cold Damage",
        "Сфера Хаоса": "Chaos Orb",
    }
    keep_en_set = {t.en for t in glossary if t.category == "keep"}
    for bad_ru, expected_en in known_bad_translations.items():
        if bad_ru in text and expected_en in keep_en_set:
            already_flagged = any(v.term == expected_en for v in violations)
            if not already_flagged:
                violations.append(Violation(
                    file=translated,
                    term=expected_en,
                    reason=f"found likely RU translation '{bad_ru}' of keep-term '{expected_en}'",
                ))
    return violations


_MARKER = re.compile(r"\[\?\]|\bTODO\b|\bTBD\b")
_MARKER_KIND = {"[?]": "[?]", "TODO": "TODO", "TBD": "TBD"}


def find_unresolved_markers(translated: Path) -> list[Marker]:
    """Find lines containing [?], TODO, or TBD."""
    markers: list[Marker] = []
    for lineno, line in enumerate(translated.read_text(encoding="utf-8").splitlines(), start=1):
        for m in _MARKER.finditer(line):
            raw = m.group(0)
            kind = _MARKER_KIND.get(raw, raw)
            markers.append(Marker(file=translated, line_number=lineno, kind=kind, line=line.rstrip()))
    return markers


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("glossary", type=Path)
    p.add_argument("translated_dir", type=Path)
    args = p.parse_args(argv)

    glossary = parse_glossary(args.glossary)
    print(f"Loaded {len(glossary)} terms from {args.glossary}")

    files = sorted(args.translated_dir.glob("*.md"))
    if not files:
        print(f"No .md files in {args.translated_dir}", file=sys.stderr)
        return 1

    total_violations = 0
    total_markers = 0

    for f in files:
        v = find_keep_term_violations(f, glossary)
        m = find_unresolved_markers(f)
        if v or m:
            print(f"\n=== {f.name} ===")
            for vi in v:
                print(f"  VIOLATION: {vi.term} - {vi.reason}")
            for mk in m:
                print(f"  MARKER L{mk.line_number} [{mk.kind}]: {mk.line}")
        total_violations += len(v)
        total_markers += len(m)

    print(f"\nTotal: {total_violations} glossary violations, {total_markers} unresolved markers across {len(files)} files")
    return 0 if (total_violations == 0 and total_markers == 0) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
