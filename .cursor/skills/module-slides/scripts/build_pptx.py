#!/usr/bin/env python3
"""Build themed clip.pptx or chapterN.pptx from outline.yaml or slides.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc

from md_to_outline import md_to_outline, merge_outlines
from pptx_theme import build_deck


def _load_outline(path: Path) -> dict:
    """Load outline YAML."""
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "slides" not in data:
        raise ValueError(f"{path}: expected mapping with 'slides' list")
    return data


def _write_outline(path: Path, outline: dict) -> None:
    """Write outline YAML for inspection/editing."""
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(outline, f, sort_keys=False, allow_unicode=True)


def _module_footer(target_dir: Path) -> str:
    """Derive footer from courses/<course>/moduleNN-slug/..."""
    parts = target_dir.parts
    course = None
    for i, p in enumerate(parts):
        if p == "courses" and i + 1 < len(parts):
            course = parts[i + 1]
            break
    name = target_dir.name
    m = re.match(r"module(\d+)-(.+)$", name)
    if m:
        slug = m.group(2).replace("-", " ")
        if course:
            return f"{course} — {slug}"
        return f"Module {m.group(1)} — {slug}"
    return _chapter_footer(target_dir)


def _chapter_footer(target_dir: Path) -> str:
    """Derive footer string from path lectures/chapterN/..."""
    parts = target_dir.parts
    ch = "Chapter"
    for p in parts:
        m = re.match(r"chapter(\d+)$", p)
        if m:
            ch = f"Chapter {m.group(1)}"
            break
    if target_dir.name.startswith(("clip-", "part-")):
        prefix = "clip-" if target_dir.name.startswith("clip-") else "part-"
        rest = target_dir.name[len(prefix) :]
        pieces = rest.split("-", 1)
        label = (
            pieces[1].replace("-", " ").title()
            if len(pieces) > 1
            else rest.replace("-", " ").title()
        )
        return f"{ch} — {label}"
    return ch


def build_pptx(
    target_dir: Path,
    *,
    write_outline: bool = False,
    outline_path: Path | None = None,
) -> Path:
    """Create slides.pptx, clip.pptx, or chapterN.pptx using themed renderer."""
    target_dir = target_dir.resolve()
    slides_path = target_dir / "slides.md"
    default_outline = target_dir / "outline.yaml"
    name = target_dir.name

    if re.match(r"module\d+-", name):
        footer = _module_footer(target_dir)
        out_path = target_dir / "slides.pptx"
    else:
        footer = _chapter_footer(target_dir)
        if name.startswith(("clip-", "part-")):
            out_path = target_dir / "clip.pptx"
        else:
            match = re.search(r"chapter(\d+)$", name)
            if not match:
                raise ValueError(
                    f"Expected folder named moduleNN-slug, chapterN, "
                    f"clip-NN-slug, or part-NN-slug, got: {name}"
                )
            out_path = target_dir / f"chapter{match.group(1)}.pptx"

    o_path = outline_path or default_outline
    if o_path.is_file():
        outline = _load_outline(o_path)
    elif slides_path.is_file():
        outline = md_to_outline(slides_path, footer=footer)
        if write_outline:
            _write_outline(default_outline, outline)
    else:
        raise FileNotFoundError(f"Missing slides.md or outline.yaml in {target_dir}")

    # Prefer module footer in outline if absent
    outline.setdefault("footer", footer)

    count = build_deck(target_dir, outline, out_path)
    log = target_dir / "build.log"
    log.write_text(
        f"built {out_path.name}\nslides={count}\nsource={o_path if o_path.is_file() else slides_path}\n",
        encoding="utf-8",
    )
    return out_path


def _merge_chapter_slides(chapter_dir: Path, meta: dict) -> Path:
    """Aggregate per-clip ``slides.md`` into ``chapterN/slides.md``."""
    ch_num = meta["chapter"]
    chunks: list[str] = []
    for clip in meta.get("parts", []):
        clip_dir = chapter_dir / str(clip["path"]).rstrip("/")
        slides_path = clip_dir / "slides.md"
        if not slides_path.is_file():
            continue
        text = slides_path.read_text(encoding="utf-8")
        if text.startswith("---"):
            end = text.find("---", 3)
            if end != -1:
                text = text[end + 3 :].strip()
        chunks.append(text.strip())
    if not chunks:
        raise FileNotFoundError(f"No clip slides.md files in {chapter_dir}")

    merged = "\n\n---\n\n".join(chunks)
    header = (
        "---\n"
        "marp: true\n"
        f"title: {meta.get('title', f'Chapter {ch_num}')}\n"
        "paginate: true\n"
        "---\n\n"
    )
    out_path = chapter_dir / "slides.md"
    out_path.write_text(header + merged + "\n", encoding="utf-8")
    return out_path


def build_chapter_deck(chapter_dir: Path, *, write_outline: bool = False) -> Path:
    """Build chapterN.pptx by merging all clip outlines in chapter.json order."""
    chapter_dir = chapter_dir.resolve()
    meta_path = chapter_dir / "chapter.json"
    if not meta_path.is_file():
        raise FileNotFoundError(f"Missing {meta_path}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    ch_num = meta["chapter"]
    outlines: list[dict] = []

    for clip in meta.get("parts", []):
        clip_dir = chapter_dir / str(clip["path"]).rstrip("/")
        footer = _chapter_footer(clip_dir)
        o_path = clip_dir / "outline.yaml"
        if o_path.is_file():
            outlines.append(_load_outline(o_path))
        elif (clip_dir / "slides.md").is_file():
            outline = md_to_outline(clip_dir / "slides.md", footer=footer)
            if write_outline:
                _write_outline(o_path, outline)
            outlines.append(outline)

    if not outlines:
        raise FileNotFoundError(f"No clip slides in {chapter_dir}")

    merged = merge_outlines(outlines, str(meta.get("title", f"Chapter {ch_num}")))
    _merge_chapter_slides(chapter_dir, meta)
    out_path = chapter_dir / f"chapter{ch_num}.pptx"
    build_deck(chapter_dir, merged, out_path)
    return out_path


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target_dir",
        type=Path,
        help="Path to lectures/chapterN or lectures/chapterN/parts/part-NN-slug",
    )
    parser.add_argument(
        "--outline",
        type=Path,
        default=None,
        help="Explicit outline.yaml path",
    )
    parser.add_argument(
        "--write-outline",
        action="store_true",
        help="Write generated outline.yaml from slides.md",
    )
    parser.add_argument(
        "--chapter-deck",
        action="store_true",
        help="Build merged chapterN.pptx from all clips (target must be chapter dir)",
    )
    args = parser.parse_args(argv)

    try:
        if args.chapter_deck:
            out = build_chapter_deck(args.target_dir, write_outline=args.write_outline)
        else:
            out = build_pptx(
                args.target_dir,
                write_outline=args.write_outline,
                outline_path=args.outline,
            )
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
