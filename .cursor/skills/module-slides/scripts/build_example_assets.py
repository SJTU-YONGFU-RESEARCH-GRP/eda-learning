"""Extract example listing text for clip slides from LaTeX or module files.

Returns raw code strings (not images) so the PPTX renderer uses the same
Consolas 20pt as every other slide — no font-size mismatch.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from extract_tex_snippets import example_key, extract_chapter_listings


def _modules_root_from_clip(clip_dir: Path) -> Path:
    """Locate packaged modules from a clip path (book or lectures repo)."""
    for parent in [clip_dir, *clip_dir.parents]:
        mod = parent / "modules"
        if mod.is_dir() and any(mod.glob("chapter*")):
            return mod
        lectures_mod = parent / "lectures" / "modules"
        if lectures_mod.is_dir():
            return lectures_mod
    raise FileNotFoundError(f"Could not locate modules root from {clip_dir}")


def _author_root_from_clip(clip_dir: Path) -> Path | None:
    """Locate ``author/`` when building from the full book repo."""
    for parent in [clip_dir, *clip_dir.parents]:
        if (parent / "author").is_dir():
            return parent
    return None


def _module_snippet(modules_root: Path, chapter: int, example_num: int) -> str | None:
    """Fallback snippet from packaged module data when LaTeX has no listing."""
    mod = modules_root / f"chapter{chapter}" / f"example{example_num}"
    if not mod.is_dir():
        return None

    for name in ("data.csv", "query.sql", "schema.sql", "metadata.json"):
        path = mod / name
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            if name.endswith(".json"):
                try:
                    text = json.dumps(json.loads(text), indent=2)
                except json.JSONDecodeError:
                    pass
            return text.strip()

    for path in sorted(mod.glob("*.json")):
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            return json.dumps(json.loads(text), indent=2)
        except json.JSONDecodeError:
            return text.strip()

    main_py = mod / "main.py"
    if main_py.is_file():
        lines = main_py.read_text(encoding="utf-8").splitlines()
        return "\n".join(lines[:20])

    return None


def example_nums_from_title(title: str) -> tuple[int, int] | None:
    """Parse ``Example N.M`` from a slide title."""
    m = re.search(r"Example\s+(\d+)\.(\d+)", title, re.IGNORECASE)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def get_example_code(
    chapter: int,
    example_num: int,
    *,
    listings: dict[str, str] | None = None,
    modules_root: Path | None = None,
    clip_dir: Path | None = None,
) -> str | None:
    """Return raw listing text for an example, or None."""
    mod_root = modules_root or (
        _modules_root_from_clip(clip_dir) if clip_dir else None
    )
    if mod_root is None:
        return None
    if listings is None and clip_dir is not None:
        author_root = _author_root_from_clip(clip_dir)
        if author_root is not None:
            tex = author_root / "author" / f"chapter{chapter}.tex"
            listings = extract_chapter_listings(tex)
    listings = listings or {}
    key = example_key(chapter, example_num)
    return listings.get(key) or _module_snippet(mod_root, chapter, example_num)


def build_clip_example_snippets(clip_dir: Path) -> dict[str, str]:
    """Collect raw code text for every Example slide in a clip transcript.

    Returns:
        Mapping ``"N.M"`` → code string.
    """
    from transcript_parse import chapter_number_from_path, load_transcript_sections

    clip_dir = clip_dir.resolve()
    transcript = clip_dir / "transcript.md"
    if not transcript.is_file():
        return {}

    chapter = chapter_number_from_path(clip_dir)
    if chapter is None:
        return {}

    modules_root = _modules_root_from_clip(clip_dir)
    author_root = _author_root_from_clip(clip_dir)
    listings: dict[str, str] = {}
    if author_root is not None:
        listings = extract_chapter_listings(
            author_root / "author" / f"chapter{chapter}.tex"
        )
    sections = load_transcript_sections(transcript)

    found: dict[str, str] = {}
    for section in sections:
        parsed = example_nums_from_title(section.title)
        if not parsed:
            continue
        ch, ex = parsed
        if ch != chapter:
            continue
        code = get_example_code(
            chapter, ex, listings=listings, modules_root=modules_root
        )
        if code:
            found[example_key(ch, ex)] = code
    return found


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clip_dir", type=Path)
    args = parser.parse_args(argv)
    try:
        snippets = build_clip_example_snippets(args.clip_dir)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if not snippets:
        print(f"No example snippets found for {args.clip_dir}")
        return 0
    for key, code in sorted(snippets.items()):
        n_lines = len(code.splitlines())
        print(f"Example {key}: {n_lines} lines")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
