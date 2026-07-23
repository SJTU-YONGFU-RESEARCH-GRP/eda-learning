"""Render monospace snippet images for example slides."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required. pip install Pillow") from exc

# Match pptx_theme code-slide palette.
BG_COLOR = (244, 244, 244)
FG_COLOR = (51, 51, 51)
BORDER_COLOR = (210, 210, 210)
CAPTION_COLOR = (102, 102, 102)

FONT_SIZE = 17
LINE_HEIGHT = 22
PADDING = 18
CAPTION_HEIGHT = 28
MAX_LINES = 18
MAX_COLS = 56


def _load_font(size: int, *, mono: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a monospace font with sensible fallbacks."""
    candidates = (
        "consola.ttf",
        "Consolas.ttf",
        "DejaVuSansMono.ttf",
        "LiberationMono-Regular.ttf",
        "cour.ttf",
        "Courier New.ttf",
    )
    if mono:
        for name in candidates:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _wrap_lines(code: str, max_cols: int, max_lines: int) -> list[str]:
    lines_out: list[str] = []
    for raw in code.splitlines():
        line = raw.rstrip()
        if not line and not lines_out:
            continue
        while len(line) > max_cols:
            lines_out.append(line[:max_cols])
            line = line[max_cols:]
        lines_out.append(line)
        if len(lines_out) >= max_lines:
            break
    if len(code.splitlines()) > max_lines:
        if lines_out:
            lines_out[-1] = lines_out[-1][: max_cols - 4] + " ..."
        lines_out.append("# ...")
    return lines_out[:max_lines] or [""]


def render_snippet_png(
    code: str,
    out_path: Path,
    *,
    caption: str | None = None,
) -> Path:
    """Render listing text to a PNG suitable for ``two_column`` slides.

    Args:
        code: Snippet body (CSV, JSON, SQL, etc.).
        out_path: Destination ``.png`` path.
        caption: Optional short label above the code block.

    Returns:
        ``out_path`` after writing.
    """
    font = _load_font(FONT_SIZE)
    lines = _wrap_lines(code, MAX_COLS, MAX_LINES)

    # Measure text block.
    probe = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(probe)
    widths = [int(draw.textlength(ln, font=font)) for ln in lines]
    text_w = int(max(widths + [200]))
    text_h = LINE_HEIGHT * len(lines)

    cap_h = CAPTION_HEIGHT if caption else 0
    img_w = text_w + PADDING * 2
    img_h = text_h + PADDING * 2 + cap_h

    img = Image.new("RGB", (img_w, img_h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, img_w - 1, img_h - 1), outline=BORDER_COLOR, width=1)

    y = PADDING
    if caption:
        cap_font = _load_font(13, mono=False)
        draw.text((PADDING, y), caption, fill=CAPTION_COLOR, font=cap_font)
        y += CAPTION_HEIGHT

    for line in lines:
        draw.text((PADDING, y), line, fill=FG_COLOR, font=font)
        y += LINE_HEIGHT

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    return out_path
