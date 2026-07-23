#!/usr/bin/env python3
"""Synthesize per-slide TTS from transcript.md and build slide_timings.json."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from transcript_parse import load_transcript_sections
from transcript_to_speech import clean_narration_prose

# When one transcript section expands to bullets + code, hold the code slide
# for this many seconds carved from the spoken duration (remainder on bullets).
_CODE_HOLD_SEC = 5.0


def _probe_duration(path: Path) -> float:
    """Return media duration in seconds; fall back to size/bitrate estimate."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip())
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        # edge-tts MP3 ~48kbps; rough fallback when ffprobe is missing
        size = path.stat().st_size
        return max(1.0, size * 8 / 48000)


def _norm_title(title: str) -> str:
    t = re.sub(r"\s+", " ", title.strip().lower())
    t = re.sub(r"\s*[—–-]\s*try these.*$", "", t)
    t = re.sub(r"\s*[—–-]\s*more.*$", "", t)
    t = re.sub(r"\s*[—–-]\s*listing.*$", "", t)
    t = re.sub(r"\s*\(\d+/\d+\)\s*$", "", t)
    return t.strip()


def _outline_slide_counts(clip_dir: Path, n_sections: int) -> list[int]:
    """How many deck slides each transcript section owns (default 1 each)."""
    counts = [1] * n_sections
    outline_path = clip_dir / "outline.yaml"
    if not outline_path.is_file():
        return counts
    try:
        data = yaml.safe_load(outline_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return counts
    if not isinstance(data, dict):
        return counts
    slides = data.get("slides") or []
    if not isinstance(slides, list) or not slides:
        return counts

    sections = load_transcript_sections(clip_dir / "transcript.md")
    title_to_idx = {_norm_title(s.title): i for i, s in enumerate(sections)}
    counts = [0] * n_sections
    for spec in slides:
        if not isinstance(spec, dict):
            continue
        key = _norm_title(str(spec.get("title", "")))
        idx = title_to_idx.get(key)
        if idx is None:
            continue
        counts[idx] += 1
    for i, c in enumerate(counts):
        if c <= 0:
            counts[i] = 1
    return counts


def _expand_timings(
    section_durations: list[float],
    slide_counts: list[int],
) -> list[dict[str, float | int]]:
    """One timing row per PPTX/PDF frame (splits multi-slide sections)."""
    timings: list[dict[str, float | int]] = []
    slide_no = 1
    for dur, n in zip(section_durations, slide_counts, strict=False):
        n = max(1, int(n))
        if n == 1:
            timings.append({"slide": slide_no, "duration": round(dur, 3)})
            slide_no += 1
            continue
        holds = [_CODE_HOLD_SEC] * (n - 1)
        first = max(1.5, dur - sum(holds))
        if first < 1.5 or dur < _CODE_HOLD_SEC * (n - 1) + 1.5:
            piece = dur / n
            parts = [piece] * n
        else:
            parts = [first, *holds]
        for part in parts:
            timings.append({"slide": slide_no, "duration": round(part, 3)})
            slide_no += 1
    return timings


async def _tts_file(text: str, out_path: Path, voice: str) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))


async def synthesize_clip_audio(clip_dir: Path, *, voice: str) -> Path:
    """Generate per-slide MP3s, concat to full.mp3, write slide_timings.json."""
    clip_dir = clip_dir.resolve()
    transcript_path = clip_dir / "transcript.md"
    audio_dir = clip_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    sections = load_transcript_sections(transcript_path)
    if not sections:
        raise ValueError(f"No slide sections in {transcript_path}")

    slide_files: list[Path] = []
    section_durations: list[float] = []

    for section in sections:
        speech = clean_narration_prose(section.body)
        if not speech:
            continue
        out = audio_dir / f"slide_{section.index:03d}.mp3"
        await _tts_file(speech, out, voice)
        duration = _probe_duration(out)
        slide_files.append(out)
        section_durations.append(duration)

    counts = _outline_slide_counts(clip_dir, len(section_durations))
    timings = _expand_timings(section_durations, counts)

    full_audio = audio_dir / "full.mp3"
    timings_path = audio_dir / "slide_timings.json"

    if len(slide_files) == 1:
        slide_files[0].replace(full_audio)
    else:
        list_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as list_file:
                list_path = Path(list_file.name)
                for sf in slide_files:
                    list_file.write(f"file '{sf.resolve().as_posix()}'\n")
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(list_path),
                    "-c",
                    "copy",
                    str(full_audio),
                ],
                check=True,
                capture_output=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            with full_audio.open("wb") as out:
                for sf in slide_files:
                    out.write(sf.read_bytes())
        finally:
            if list_path is not None:
                list_path.unlink(missing_ok=True)

    timings_path.write_text(json.dumps(timings, indent=2) + "\n", encoding="utf-8")
    total = sum(float(t["duration"]) for t in timings)
    print(
        f"Wrote {full_audio} ({len(timings)} deck slides / "
        f"{len(section_durations)} spoken, {total:.1f}s) "
        f"and {timings_path}"
    )
    return full_audio


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clip_dir", type=Path)
    parser.add_argument("--voice", default="en-US-JennyNeural")
    args = parser.parse_args(argv)
    try:
        asyncio.run(synthesize_clip_audio(args.clip_dir, voice=args.voice))
    except Exception as exc:  # noqa: BLE001 — surface pipeline errors to CLI
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
