#!/usr/bin/env python3
"""Verify clip media: outline, images, bullet limits before PPTX/PDF/video."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc

from md_to_outline import md_to_outline

try:
    from verify_transcript_consistency import verify_transcript_consistency
except ImportError:  # pragma: no cover
    verify_transcript_consistency = None  # type: ignore[misc, assignment]

MAX_BULLETS = 6
MAX_CHARS = 110


def _load_outline(clip_dir: Path) -> dict[str, Any]:
    o_path = clip_dir / "outline.yaml"
    if o_path.is_file():
        with o_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError(f"{o_path}: root must be a mapping")
        return data
    slides = clip_dir / "slides.md"
    if slides.is_file():
        return md_to_outline(slides, footer=clip_dir.name)
    raise FileNotFoundError(f"No outline.yaml or slides.md in {clip_dir}")


def verify_clip(clip_dir: Path) -> list[str]:
    """Return list of error messages (empty if OK)."""
    clip_dir = clip_dir.resolve()
    errors: list[str] = []

    try:
        outline = _load_outline(clip_dir)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]

    slides = outline.get("slides", [])
    if not slides:
        errors.append("outline has no slides")

    for i, spec in enumerate(slides, start=1):
        if not isinstance(spec, dict):
            errors.append(f"slide {i}: not a mapping")
            continue
        stype = spec.get("type", "bullets")
        title = spec.get("title", "")
        if title and len(str(title)) > 70:
            errors.append(f"slide {i}: title exceeds 70 chars")

        if stype == "bullets":
            bullets = spec.get("bullets", [])
            if not bullets:
                errors.append(f"slide {i}: bullets slide has no bullets")
            if len(bullets) > MAX_BULLETS:
                errors.append(f"slide {i}: more than {MAX_BULLETS} bullets")
            for j, b in enumerate(bullets, start=1):
                if len(str(b)) > MAX_CHARS:
                    errors.append(f"slide {i} bullet {j}: exceeds {MAX_CHARS} chars")
        elif stype == "image":
            img = spec.get("image")
            if not img:
                errors.append(f"slide {i}: image slide missing path")
            elif not _resolve_image(clip_dir, str(img)).is_file():
                errors.append(f"slide {i}: missing image {img}")
        elif stype == "two_column":
            right = spec.get("right")
            if right and not _resolve_image(clip_dir, str(right)).is_file():
                errors.append(f"slide {i}: missing image {right}")
        elif stype == "code":
            if not spec.get("code"):
                errors.append(f"slide {i}: code slide missing code")
        elif stype == "demo":
            if not spec.get("command"):
                errors.append(f"slide {i}: demo slide missing command")
            shot = spec.get("screenshot")
            if shot and not (clip_dir / shot).is_file():
                errors.append(f"slide {i}: missing screenshot {shot}")

    pptx = clip_dir / "slides.pptx"
    if not pptx.is_file():
        pptx = clip_dir / "clip.pptx"
    if not pptx.is_file():
        errors.append("slides.pptx (or clip.pptx) not built yet — run build_pptx.py")

    if verify_transcript_consistency is not None:
        errors.extend(verify_transcript_consistency(clip_dir))

    return errors


def _resolve_image(clip_dir: Path, rel: str) -> Path:
    p = (clip_dir / rel).resolve()
    if p.is_file():
        return p
    return Path(rel).resolve()


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clip_dir", type=Path, help="Path to clip folder")
    args = parser.parse_args(argv)

    errors = verify_clip(args.clip_dir)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: {args.clip_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
