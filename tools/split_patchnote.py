"""Split a POE2 patchnote markdown file into per-section chunks.

Usage:
    python tools/split_patchnote.py <input.md> <output_dir>

Outputs files like 00-intro.md, 01-overview.md, 02-new-mechanics.md, ...
matching each H2 section. Content before the first H2 becomes 00-intro.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Chunk:
    title: str
    body: str


_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def split_by_h2(text: str) -> list[Chunk]:
    """Split markdown by ## headings. Pre-first-H2 content becomes 'intro'."""
    matches = list(_H2.finditer(text))
    chunks: list[Chunk] = []

    if not matches:
        return [Chunk(title="intro", body=text.strip())]

    intro_body = text[: matches[0].start()].strip()
    if intro_body:
        chunks.append(Chunk(title="intro", body=intro_body))

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunks.append(Chunk(title=m.group(1).strip(), body=text[start:end].strip()))

    return chunks


def slugify(title: str) -> str:
    """Lowercase, replace non-alnum runs with single hyphen, trim hyphens."""
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "section"


def write_chunks(chunks: list[Chunk], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, chunk in enumerate(chunks):
        name = f"{i:02d}-{slugify(chunk.title)}.md"
        path = out_dir / name
        path.write_text(chunk.body + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="Path to patchnote markdown")
    p.add_argument("output_dir", type=Path, help="Directory to write chunks")
    args = p.parse_args(argv)

    text = args.input.read_text(encoding="utf-8")
    chunks = split_by_h2(text)
    paths = write_chunks(chunks, args.output_dir)
    for path in paths:
        print(path)
    print(f"\n{len(paths)} chunks written to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
