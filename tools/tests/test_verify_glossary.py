"""Tests for tools/verify_glossary.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verify_glossary import (  # noqa: E402
    parse_glossary,
    find_keep_term_violations,
    find_unresolved_markers,
    Violation,
)

FIX = Path(__file__).parent / "fixtures"


def test_parse_glossary_returns_categorised_terms() -> None:
    g = parse_glossary(FIX / "mini_glossary.md")
    keep = {t.en for t in g if t.category == "keep"}
    translate = {t.en for t in g if t.category == "translate"}
    assert keep == {"Volatile Dead", "Spark", "Fire Damage"}
    assert translate == {"increased", "added"}


def test_verify_ok_file_has_no_keep_violations() -> None:
    g = parse_glossary(FIX / "mini_glossary.md")
    violations = find_keep_term_violations(FIX / "translated_ok.md", g)
    assert violations == []


def test_verify_bad_file_flags_translated_keep_terms() -> None:
    g = parse_glossary(FIX / "mini_glossary.md")
    violations = find_keep_term_violations(FIX / "translated_bad.md", g)
    flagged = {v.term for v in violations}
    assert "Spark" in flagged
    assert "Fire Damage" in flagged


def test_find_unresolved_markers_detects_placeholders() -> None:
    markers = find_unresolved_markers(FIX / "translated_bad.md")
    found_kinds = {m.kind for m in markers}
    assert "[?]" in found_kinds
    assert "TODO" in found_kinds


def test_find_unresolved_markers_ok_file_clean() -> None:
    markers = find_unresolved_markers(FIX / "translated_ok.md")
    assert markers == []
