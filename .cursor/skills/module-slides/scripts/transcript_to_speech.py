#!/usr/bin/env python3
"""Extract listener-friendly narration text from a clip transcript.md.

Spoken output contains only narration paragraphs. Skipped entirely:
the H1 title, the metadata block (**Clip id:** etc.), and every
"## Slide N" heading. Repo paths and awkward symbols are rewritten
into words as a safety net; authored prose should already avoid them.

Usage:
    python transcript_to_speech.py transcript.md [output.txt]

Without an output path, the speech text is printed to stdout (preview).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def clean_narration_prose(text: str) -> str:
    """Rewrite one narration paragraph for TTS (markdown, paths, symbols)."""
    # Drop HTML authoring markers (algorithm-walkthrough regions, etc.)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Drop lab snapshot embeds — spoken prose orients the learner separately.
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    # Drop fenced try-these blocks — commands live on slides, not in speech.
    text = re.sub(r"```[\w-]*\n.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(
        r"`?modules/chapter(\d+)/example(\d+)/?`?",
        r"the chapter \1, example \2 module",
        text,
    )
    text = re.sub(r"`?author/chapter(\d+)\.tex`?", r"chapter \1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.replace("\u00a7", "Section ")
    text = re.sub(r"\s*[\u2014\u2013]\s*", ", ", text)
    text = re.sub(r"(?<=\w)\s*/\s*(?=\w)", " or ", text)
    return text.strip()


def transcript_to_speech(transcript: str) -> str:
    """Convert transcript markdown into plain narration text for TTS.

    Args:
        transcript: Raw contents of a clip ``transcript.md``.

    Returns:
        Narration-only text with markdown, paths, and symbols rewritten
        for natural speech.
    """
    paragraphs: list[str] = []
    for block in transcript.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        # Headings are author/site anchors, never spoken.
        if block.startswith("#"):
            continue
        # Metadata block: every line looks like **Key:** value.
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if lines and all(re.match(r"\*\*[^*]+:\*\*", ln) for ln in lines):
            continue
        paragraphs.append(block)

    text = "\n\n".join(paragraphs)
    cleaned = clean_narration_prose(text)
    return cleaned + "\n" if cleaned else "\n"


def main(argv: list[str]) -> int:
    """CLI entry point."""
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    speech = transcript_to_speech(Path(argv[1]).read_text(encoding="utf-8"))
    if len(argv) >= 3:
        Path(argv[2]).write_text(speech, encoding="utf-8")
    else:
        print(speech)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
