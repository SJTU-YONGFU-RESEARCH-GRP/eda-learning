"""Parse clip transcript.md into structured slide sections."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TranscriptSection:
    """One slide's narration block from a clip transcript."""

    index: int
    title: str
    body: str


_SLIDE_HEADING = re.compile(r"^##\s+Slide\s+(\d+)\s*[—–-]\s*(.+?)\s*$", re.MULTILINE)


def parse_transcript(transcript: str) -> list[TranscriptSection]:
    """Split transcript markdown into ordered slide sections.

    Args:
        transcript: Full contents of ``transcript.md``.

    Returns:
        Sections ordered by slide index. Metadata and the H1 title are ignored.
    """
    matches = list(_SLIDE_HEADING.finditer(transcript))
    if not matches:
        return []

    sections: list[TranscriptSection] = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(transcript)
        body = transcript[start:end].strip()
        sections.append(
            TranscriptSection(
                index=int(match.group(1)),
                title=match.group(2).strip(),
                body=body,
            )
        )
    return sections


def load_transcript_sections(path: Path) -> list[TranscriptSection]:
    """Load and parse a transcript file."""
    return parse_transcript(path.read_text(encoding="utf-8"))


def chapter_number_from_path(clip_dir: Path) -> int | None:
    """Extract chapter number from ``.../chapterN/...`` in the clip path."""
    for part in clip_dir.parts:
        m = re.fullmatch(r"chapter(\d+)", part)
        if m:
            return int(m.group(1))
    return None
