"""Build outline.yaml and slides.md from transcript.md (source of truth)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from build_example_assets import build_clip_example_snippets, example_nums_from_title
from prose_to_bullets import (
    MAX_BULLETS,
    example_module_command,
    prose_to_bullets,
    summarize_subtitle,
)
from transcript_parse import chapter_number_from_path, load_transcript_sections


def _part_footer(part_dir: Path) -> str:
    name = part_dir.name
    m = re.match(r"module(\d+)-(.+)$", name)
    if m:
        course = None
        parts = part_dir.resolve().parts
        for i, p in enumerate(parts):
            if p == "courses" and i + 1 < len(parts):
                course = parts[i + 1]
                break
        slug = m.group(2).replace("-", " ")
        if course:
            return f"{course} — {slug}"
        return f"Module {m.group(1)} — {slug}"
    if name.startswith("part-"):
        rest = name[len("part-") :]
        pieces = rest.split("-", 1)
        label = (
            pieces[1].replace("-", " ").title()
            if len(pieces) > 1
            else rest.replace("-", " ").title()
        )
    else:
        label = name.replace("-", " ").title()
    ch = chapter_number_from_path(part_dir)
    if ch is not None:
        return f"Chapter {ch} — {label}"
    return label


def _deck_title(sections: list[Any]) -> str:
    if sections:
        return sections[0].title
    return "Part"


_IMG_MD = re.compile(
    r"!\[([^\]]*)\]\((assets/[^)\s]+\.(?:png|jpe?g|webp|gif))\)",
    re.IGNORECASE,
)
_CODE_FENCE = re.compile(
    r"```(?:bash|sh|shell|zsh|console|text)?\n(.*?)```",
    re.IGNORECASE | re.DOTALL,
)


def _strip_images(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (body without image markdown, list of (alt, path))."""
    found: list[tuple[str, str]] = []

    def _collect(m: re.Match[str]) -> str:
        found.append((m.group(1).strip(), m.group(2).strip()))
        return ""

    cleaned = _IMG_MD.sub(_collect, body)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned, found


def _strip_code_fences(body: str) -> tuple[str, list[str]]:
    """Return (body without fenced blocks, list of code strings)."""
    blocks: list[str] = []

    def _collect(m: re.Match[str]) -> str:
        blocks.append(m.group(1).rstrip() + "\n")
        return ""

    cleaned = _CODE_FENCE.sub(_collect, body)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned, blocks


def section_to_slide_spec(
    section: Any,
    *,
    chapter: int | None,
    is_first: bool,
    snippet_code: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Map one transcript section to one or more outline slide specs.

    Example slides produce two slides: a bullets slide + a code slide
    showing the book listing, keeping font size consistent across the deck.

    Lab snapshots: a markdown image ``![…](assets/….png)`` in the section
    body becomes an ``image`` slide (or ``two_column`` if bullets remain).

    Track A try-these: a fenced ``bash``/``sh`` block becomes a ``code`` slide
    after the bullets (or alone if that is the whole slide).
    """
    title = section.title
    body_raw = section.body
    body, images = _strip_images(body_raw)
    body, code_blocks = _strip_code_fences(body)
    title_lower = title.lower()
    code_map = snippet_code or {}

    if is_first:
        first = _split_sentences(body)[0] if body else ""
        return [{
            "type": "title",
            "title": title,
            "subtitle": summarize_subtitle(first) if first else None,
            "notes": body,
        }]

    if images and not is_first:
        img_path = images[0][1]
        caption = images[0][0] or None
        # Lab UI snapshots need a full-slide image so they read in video;
        # keep spoken notes from the prose (bullets are optional caption only).
        norm = img_path.replace("\\", "/")
        is_lab_shot = norm.startswith("assets/lab")
        is_shell_shot = "real-shell" in norm
        # Algorithm walkthrough frames — full-bleed teaching visuals
        is_step_shot = "/steps/" in norm or norm.startswith("assets/steps/")
        bullets = prose_to_bullets(title, body) if body else []
        specs: list[dict[str, Any]] = []
        if (
            not is_lab_shot
            and not is_shell_shot
            and not is_step_shot
            and bullets
            and len(bullets) >= 2
        ):
            specs.append({
                "type": "two_column",
                "title": title,
                "left": bullets[:MAX_BULLETS],
                "right": img_path,
                "notes": body,
            })
        else:
            specs.append({
                "type": "image",
                "title": title,
                "image": img_path,
                "caption": caption,
                "notes": body,
            })
        for i, block in enumerate(code_blocks):
            code_title = f"{title} — try these" if i == 0 else f"{title} — more"
            specs.append({"type": "code", "title": code_title, "code": block})
        return specs

    if title_lower == "next" or title_lower.startswith("next "):
        bullets = prose_to_bullets(title, body)
        return [{"type": "bullets", "title": "Next", "bullets": bullets, "notes": body}]

    bullets = prose_to_bullets(title, body)
    parsed = example_nums_from_title(title)

    if parsed and chapter is not None:
        ch, ex = parsed
        if ch == chapter:
            code = code_map.get(f"{ch}.{ex}")
            if code:
                clean_bullets = [b for b in bullets if b.strip()][:4]
                if not any("modules/chapter" in b for b in clean_bullets):
                    clean_bullets.append(
                        f"View files: `modules/chapter{chapter}/example{ex}/`"
                    )
                return [
                    {
                        "type": "bullets",
                        "title": title,
                        "bullets": clean_bullets[:MAX_BULLETS],
                        "notes": body,
                    },
                    {
                        "type": "code",
                        "title": f"Example {ch}.{ex} — listing",
                        "code": code,
                    },
                ]

    command = example_module_command(title, chapter)

    if command and chapter is not None:
        m = re.search(r"Example\s+\d+\.(\d+)", title, re.IGNORECASE)
        if m and not any("modules/chapter" in b for b in bullets):
            bullets = bullets[: MAX_BULLETS - 1]
            bullets.append(
                f"View files: `modules/chapter{chapter}/example{m.group(1)}/`"
            )

    specs: list[dict[str, Any]] = []
    if bullets:
        specs.append({
            "type": "bullets",
            "title": title,
            "bullets": bullets[:MAX_BULLETS],
            "notes": body,
        })
    if code_blocks:
        code_title = title if not specs else f"{title} — try these"
        specs.append({
            "type": "code",
            "title": code_title,
            "code": code_blocks[0],
            "notes": body if not specs else "",
        })
        for extra in code_blocks[1:]:
            specs.append({"type": "code", "title": f"{title} — more", "code": extra})
    if not specs:
        specs.append({
            "type": "bullets",
            "title": title,
            "bullets": bullets[:MAX_BULLETS],
            "notes": body,
        })
    return specs


def _split_sentences(body: str) -> list[str]:
    import re as _re

    return [
        c.strip()
        for c in _re.split(r"(?<=[.!?])\s+", body.strip())
        if len(c.strip()) >= 8
    ]


def transcript_to_outline(
    clip_dir: Path,
    *,
    snippet_code: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Generate an outline dict from ``clip_dir/transcript.md``."""
    transcript_path = clip_dir / "transcript.md"
    sections = load_transcript_sections(transcript_path)
    if not sections:
        raise ValueError(f"No slide sections found in {transcript_path}")

    chapter = chapter_number_from_path(clip_dir)
    deck_title = _deck_title(sections)
    code_map = snippet_code if snippet_code is not None else build_clip_example_snippets(
        clip_dir
    )
    slides: list[dict[str, Any]] = []

    for i, section in enumerate(sections):
        specs = section_to_slide_spec(
            section,
            chapter=chapter,
            is_first=(i == 0),
            snippet_code=code_map,
        )
        slides.extend(specs)

    return {
        "title": deck_title,
        "footer": _part_footer(clip_dir),
        "slides": slides,
    }


def outline_to_slides_md(outline: dict[str, Any]) -> str:
    """Render a Marp ``slides.md`` from an outline dict."""
    title = outline.get("title", "Clip")
    lines = [
        "---",
        "marp: true",
        f"title: {title}",
        "paginate: true",
        "---",
        "",
    ]

    for spec in outline.get("slides", []):
        stype = spec.get("type", "bullets")
        slide_title = spec.get("title", "Slide")

        if stype == "title":
            lines.append(f"# {slide_title}")
            subtitle = spec.get("subtitle")
            if subtitle:
                lines.append("")
                lines.append(subtitle)
        elif stype == "two_column":
            lines.append(f"## {slide_title}")
            for b in spec.get("left", []):
                lines.append(f"- {b}")
            right = spec.get("right")
            if right:
                lines.append(f"![snippet]({right})")
        elif stype == "code":
            lines.append(f"## {slide_title}")
            lines.append("")
            lines.append("```")
            lines.append(str(spec.get("code", "")))
            lines.append("```")
        elif stype == "image":
            lines.append(f"## {slide_title}")
            img = spec.get("image")
            caption = spec.get("caption") or ""
            if img:
                lines.append(f"![{caption}]({img})")
        else:
            lines.append(f"## {slide_title}")
            bullets = spec.get("bullets") or []
            for b in bullets:
                lines.append(f"- {b}")

        lines.extend(["", "---", ""])

    if lines[-1] == "":
        lines.pop()
    if lines[-1] == "---":
        lines.pop()
    return "\n".join(lines) + "\n"


def sync_clip_from_transcript(clip_dir: Path, *, dry_run: bool = False) -> dict[str, Any]:
    """Write ``outline.yaml`` and ``slides.md`` from ``transcript.md``.

    Args:
        part_dir: Path to ``parts/part-NN-slug/``.
        dry_run: If True, return outline without writing files.

    Returns:
        The generated outline mapping.
    """
    clip_dir = clip_dir.resolve()
    code_map = build_clip_example_snippets(clip_dir)
    outline = transcript_to_outline(clip_dir, snippet_code=code_map)
    if dry_run:
        return outline

    outline_path = clip_dir / "outline.yaml"
    slides_path = clip_dir / "slides.md"
    with outline_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(outline, f, sort_keys=False, allow_unicode=True)
    slides_path.write_text(outline_to_slides_md(outline), encoding="utf-8")
    return outline


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clip_dir", type=Path, help="Clip directory")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        outline = sync_clip_from_transcript(args.clip_dir, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    n = len(outline.get("slides", []))
    if args.dry_run:
        print(yaml.safe_dump(outline, sort_keys=False, allow_unicode=True))
    else:
        print(f"Synced {n} slides from transcript -> outline.yaml + slides.md")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
