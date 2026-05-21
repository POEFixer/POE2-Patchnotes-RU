"""Tests for tools/split_patchnote.py."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from split_patchnote import split_by_h2, Chunk  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "sample_patchnote.md"


def test_split_by_h2_yields_one_chunk_per_h2_section() -> None:
    text = FIXTURE.read_text(encoding="utf-8")
    chunks = split_by_h2(text)
    assert len(chunks) == 5, f"got {len(chunks)} chunks: {[c.title for c in chunks]}"


def test_split_by_h2_first_chunk_is_intro() -> None:
    text = FIXTURE.read_text(encoding="utf-8")
    chunks = split_by_h2(text)
    assert chunks[0].title == "intro"
    assert "Intro paragraph" in chunks[0].body


def test_split_by_h2_titles_in_order() -> None:
    text = FIXTURE.read_text(encoding="utf-8")
    chunks = split_by_h2(text)
    titles = [c.title for c in chunks]
    assert titles == ["intro", "Overview", "New Mechanics", "Skill Balance", "Bug Fixes"]


def test_chunk_body_preserves_subsections() -> None:
    text = FIXTURE.read_text(encoding="utf-8")
    chunks = split_by_h2(text)
    new_mechanics = next(c for c in chunks if c.title == "New Mechanics")
    assert "### Tinctures" in new_mechanics.body
    assert "### Charms" in new_mechanics.body
    assert "Tincture description line 1." in new_mechanics.body


def test_slugify_titles_for_filenames() -> None:
    from split_patchnote import slugify
    assert slugify("New Mechanics") == "new-mechanics"
    assert slugify("Skill Balance") == "skill-balance"
    assert slugify("Bug Fixes") == "bug-fixes"
    assert slugify("intro") == "intro"
