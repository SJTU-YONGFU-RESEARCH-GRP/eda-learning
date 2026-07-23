"""Extract example listing snippets from book chapter LaTeX sources."""

from __future__ import annotations

import re
from pathlib import Path

_EXAMPLE_BLOCK = re.compile(
    r"\\begin\{example\}\{eg:(\d+)\.(\d+)\}\{[^}]*\}(.*?)\\end\{example\}",
    re.DOTALL,
)
_LISTING = re.compile(
    r"\\begin\{lstlisting\}(?:\[[^\]]*\])?\s*(.*?)\\end\{lstlisting\}",
    re.DOTALL,
)


def _clean_listing(text: str) -> str:
    """Normalize whitespace in extracted listing text."""
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").splitlines()]
    # Drop leading/trailing blank lines.
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def extract_chapter_listings(chapter_tex: Path) -> dict[str, str]:
    """Return ``{"1.1": snippet, ...}`` from ``author/chapterN.tex``."""
    if not chapter_tex.is_file():
        return {}
    text = chapter_tex.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for ch, ex, body in _EXAMPLE_BLOCK.findall(text):
        key = f"{ch}.{ex}"
        listings = _LISTING.findall(body)
        if listings:
            out[key] = _clean_listing(listings[0])
    return out


def example_key(chapter: int, example_num: int) -> str:
    """Canonical example id string."""
    return f"{chapter}.{example_num}"


def snippet_asset_name(chapter: int, example_num: int) -> str:
    """Filename for a rendered snippet image."""
    return f"eg-{chapter}-{example_num}.png"
