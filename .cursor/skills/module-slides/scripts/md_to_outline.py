#!/usr/bin/env python3
"""Convert clip slides.md (Marp) to outline.yaml structure for themed PPTX."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def _parse_marp_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return frontmatter dict and body without frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end].strip()
    body = text[end + 3 :].strip()
    meta: dict[str, str] = {}
    for line in fm_block.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    return meta, body


def _split_slides(body: str) -> list[str]:
    return [c.strip() for c in body.split("\n---\n") if c.strip()]


def _parse_slide_chunk(chunk: str) -> dict[str, Any]:
    """Parse one Marp slide chunk into structural parts."""
    lines = chunk.splitlines()
    title = ""
    subtitle_lines: list[str] = []
    bullets: list[str] = []
    images: list[str] = []
    code_blocks: list[str] = []
    slide_type_hint: str | None = None

    in_code = False
    code_buf: list[str] = []

    for line in lines:
        hint = re.match(r"^<!--\s*type:\s*(\w+)\s*-->", line.strip())
        if hint:
            slide_type_hint = hint.group(1)
            continue
        if line.strip().startswith("```"):
            if in_code:
                code_blocks.append("\n".join(code_buf))
                code_buf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        img = re.match(r"^!\[[^\]]*\]\(([^)]+)\)\s*$", line.strip())
        if img:
            images.append(img.group(1).strip())
            continue

        heading = re.match(r"^(#{1,3})\s+(.*)$", line)
        bullet = re.match(r"^[-*]\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1 and not title:
                title = text
            elif level >= 2 and not title:
                title = text
            elif level >= 2 and title and not bullets:
                pass  # title already set
        elif bullet:
            bullets.append(bullet.group(1).strip())
        elif line.strip() and not line.strip().startswith("#"):
            if not title:
                title = line.strip()
            elif not bullets:
                subtitle_lines.append(line.strip())

    subtitle = " ".join(subtitle_lines) if subtitle_lines else None
    return {
        "title": title or "Slide",
        "subtitle": subtitle,
        "bullets": bullets,
        "images": images,
        "code_blocks": code_blocks,
        "type_hint": slide_type_hint,
    }


def _infer_slide_type(parsed: dict[str, Any]) -> str:
    """Infer outline slide type from parsed chunk."""
    if parsed.get("type_hint"):
        return str(parsed["type_hint"])

    title = str(parsed["title"])
    title_lower = title.lower()
    bullets: list[str] = parsed.get("bullets", [])
    images: list[str] = parsed.get("images", [])
    code_blocks: list[str] = parsed.get("code_blocks", [])

    if title_lower in ("next",) or title_lower.startswith("next "):
        return "skip"
    if title_lower.startswith("section:"):
        return "section"
    if not bullets and not images and not code_blocks and parsed.get("subtitle"):
        return "title"
    if not bullets and not code_blocks and len(images) == 1:
        return "image"
    if code_blocks and not images:
        return "code"
    if images and bullets:
        return "two_column"
    if any("try it:" in b.lower() or "modules/" in b for b in bullets):
        for b in bullets:
            cmd = re.search(r"`(modules/[^`]+)`", b)
            if cmd:
                return "demo_bullets"
    return "bullets"


def md_to_outline(
    slides_path: Path,
    *,
    footer: str = "",
    deck_title: str | None = None,
) -> dict[str, Any]:
    """Convert slides.md to an outline dict for pptx_theme.build_deck."""
    text = slides_path.read_text(encoding="utf-8")
    meta, body = _parse_marp_frontmatter(text)
    chunks = _split_slides(body)

    title = deck_title or meta.get("title", slides_path.parent.name)
    outline: dict[str, Any] = {
        "title": title,
        "footer": footer or title,
        "slides": [],
    }

    first = True
    for chunk in chunks:
        parsed = _parse_slide_chunk(chunk)
        stype = _infer_slide_type(parsed)
        if stype == "skip":
            continue

        slide_title = parsed["title"]
        if stype == "section":
            slide_title = re.sub(r"^section:\s*", "", slide_title, flags=re.I).strip()
            outline["slides"].append({"type": "section", "title": slide_title})
            continue

        if first and stype == "title" or (
            first and not parsed["bullets"] and parsed.get("subtitle")
        ):
            outline["slides"].append(
                {
                    "type": "title",
                    "title": parsed["title"],
                    "subtitle": parsed.get("subtitle"),
                }
            )
            first = False
            continue
        first = False

        if stype == "image" and parsed["images"]:
            outline["slides"].append(
                {
                    "type": "image",
                    "title": slide_title,
                    "image": parsed["images"][0],
                }
            )
        elif stype == "code" and parsed["code_blocks"]:
            outline["slides"].append(
                {
                    "type": "code",
                    "title": slide_title,
                    "code": parsed["code_blocks"][0],
                }
            )
        elif stype == "two_column" and parsed["images"]:
            outline["slides"].append(
                {
                    "type": "two_column",
                    "title": slide_title,
                    "left": parsed["bullets"],
                    "right": parsed["images"][0],
                }
            )
        elif stype == "demo_bullets":
            command = ""
            bullets_out: list[str] = []
            for b in parsed["bullets"]:
                m = re.search(r"`(modules/[^`]+)`", b)
                if m and not command:
                    command = f"cd {m.group(1)} && bash run.sh"
                else:
                    bullets_out.append(b)
            spec: dict[str, Any] = {
                "type": "demo",
                "title": slide_title,
                "command": command or "bash run.sh",
            }
            if bullets_out:
                spec["notes"] = "\n".join(bullets_out)
            outline["slides"].append(spec)
        else:
            outline["slides"].append(
                {
                    "type": "bullets",
                    "title": slide_title,
                    "bullets": parsed["bullets"],
                }
            )

    return outline


def merge_outlines(outlines: list[dict[str, Any]], chapter_title: str) -> dict[str, Any]:
    """Merge clip outlines into one chapter deck (skip duplicate title slides)."""
    merged: dict[str, Any] = {
        "title": chapter_title,
        "footer": chapter_title,
        "slides": [],
    }
    for i, outline in enumerate(outlines):
        slides = outline.get("slides", [])
        for spec in slides:
            if i > 0 and spec.get("type") == "title":
                continue
            if spec.get("type") == "skip":
                continue
            merged["slides"].append(spec)
    return merged
