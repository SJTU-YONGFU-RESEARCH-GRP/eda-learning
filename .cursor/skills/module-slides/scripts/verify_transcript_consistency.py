"""Verify transcript.md stays aligned with outline.yaml / slides.md."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from transcript_parse import load_transcript_sections
from transcript_to_outline import _strip_code_fences, _strip_html_comments, _strip_images


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())


def _normalize_notes(text: str) -> str:
    """Compare spoken body ignoring snapshots, fences, and HTML markers."""
    cleaned = _strip_html_comments(text)
    cleaned, _ = _strip_images(cleaned)
    cleaned, _ = _strip_code_fences(cleaned)
    return cleaned.strip()


def _load_outline(clip_dir: Path) -> dict[str, Any]:
    path = clip_dir / "outline.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"Missing outline.yaml in {clip_dir}")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return data


def verify_transcript_consistency(clip_dir: Path) -> list[str]:
    """Return error messages when transcript and outline/slides diverge."""
    clip_dir = clip_dir.resolve()
    transcript_path = clip_dir / "transcript.md"
    errors: list[str] = []

    if not transcript_path.is_file():
        return [f"Missing transcript.md in {clip_dir}"]

    sections = load_transcript_sections(transcript_path)
    if not sections:
        return ["transcript.md has no ## Slide N headings"]

    try:
        outline = _load_outline(clip_dir)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]

    slides = outline.get("slides", [])
    # Example sections can produce 2 outline slides (bullets + code),
    # so outline may have more slides than transcript sections.
    n_content_slides = len([s for s in slides if s.get("type") != "code"
                           or not str(s.get("title", "")).endswith("— listing")])
    # Simplified: just check that every transcript section has a matching
    # outline slide with the same title (ignoring bonus code-listing slides).
    outline_titles = [_normalize_title(str(s.get("title", ""))) for s in slides]
    for section in sections:
        t = _normalize_title(section.title)
        # Allow "Next" normalization
        matched = t in outline_titles or (
            section.title.lower().startswith("next")
            and any(ot.startswith("next") for ot in outline_titles)
        )
        if not matched:
            errors.append(
                f"transcript section '{section.title}' has no matching outline slide "
                "— run transcript_to_outline.py"
            )

    # Check notes on content slides (skip pure code-listing slides).
    for spec in slides:
        notes = str(spec.get("notes", "") or "")
        if not notes.strip():
            continue
        stype = spec.get("type", "")
        if stype == "code" and str(spec.get("title", "")).endswith("— listing"):
            continue
        title_norm = _normalize_title(str(spec.get("title", "")))
        matching_section = next(
            (s for s in sections if _normalize_title(s.title) == title_norm
             or (s.title.lower().startswith("next") and title_norm.startswith("next"))),
            None,
        )
        if matching_section and _normalize_notes(notes) != _normalize_notes(
            matching_section.body
        ):
            errors.append(
                f"outline notes for '{spec.get('title')}' do not match transcript "
                f"(re-run transcript_to_outline.py)"
            )

    slides_md = clip_dir / "slides.md"
    if slides_md.is_file():
        body = slides_md.read_text(encoding="utf-8")
        if body.startswith("---"):
            end = body.find("---", 3)
            body = body[end + 3 :] if end != -1 else body
        md_slide_count = len([c for c in body.split("\n---\n") if c.strip()])
        # Outline may have bonus code-listing slides, so md count >= sections.
        if md_slide_count < len(sections):
            errors.append(
                f"slides.md has {md_slide_count} slides but transcript has "
                f"{len(sections)} — re-run transcript_to_outline.py"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clip_dir", type=Path)
    args = parser.parse_args(argv)
    errors = verify_transcript_consistency(args.clip_dir)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: transcript consistent with outline ({args.clip_dir})")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
