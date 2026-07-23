"""Convert full narration prose into concise on-screen slide bullets.

Slides show **summaries**; the transcript (and outline ``notes``) keep the full,
natural narration for TTS. Bullets are compressed by meaning, never mid-sentence
truncation with an ellipsis.
"""

from __future__ import annotations

import re

MAX_BULLETS = 6
MAX_BULLET_CHARS = 90
MAX_SUBTITLE_CHARS = 120

# Openers that add spoken warmth but not slide value.
_FILLER_OPENERS: tuple[str, ...] = (
    r"^In tabular data,?\s+",
    r"^In modern data work,?\s+",
    r"^Unlike raw operational logs,?\s+a dataset\s+",
    r"^Unlike [^,]+,\s+",
    r"^By the end of this part,?\s+you should\s+",
    r"^Three goals guide this part\.?\s*",
    r"^Remember three points\.?\s*",
    r"^With [^,]+ defined,?\s+",
    r"^Example \d+\.\d+ is (?:the chapter'?s )?",
    r"^Datasets are not only tables\.?\s*",
    r"^Pause for the quiz,?\s+then\s+",
)

# Phrase-level compressions (long spoken form → shorter slide form).
_PHRASE_SHORTCUTS: tuple[tuple[str, str], ...] = (
    (
        r"something curated for analysis, not merely a raw stream of events",
        "curated for analysis, not raw event streams",
    ),
    (
        r"often organized as records and attributes, that serves as input to "
        r"analysis, modeling, or decision-making",
        "records and attributes for analysis and decisions",
    ),
    (
        r"^usually has defined scope, structure, and ideally documentation that makes it interpretable",
        "Has scope, structure, and documentation",
    ),
    (
        r"the dataset is the basic unit—whether the task is machine learning, statistics, or business intelligence",
        "The dataset is the basic unit for ML, statistics, and BI",
    ),
    (
        r"the dataset is the basic unit, whether the task is machine learning, statistics, or business intelligence",
        "The dataset is the basic unit for ML, statistics, and BI",
    ),
    (
        r"each record is one observation—one sale, one patient, one sensor reading—and each attribute describes a property of that observation",
        "each record is one observation; each attribute describes it",
    ),
    (
        r"separate records from attributes so every later example has a shared language",
        "Distinguish records from attributes (shared vocabulary)",
    ),
    (
        r"see that the same idea appears in both flat CSV tables and nested JSON",
        "same idea in CSV tables and nested JSON",
    ),
    (
        r"stores housing listings as JSON with nested fields—still records with attributes, but in a flexible schema",
        "JSON listings with nested fields (flexible schema)",
    ),
    (
        r"provide meaningful data that can be turned into insight",
        "meaningful, analyzable data",
    ),
)

_META_ONLY = re.compile(
    r"^(?:three goals guide(?:\s+this part)?|remember three points)[\s.]*$",
    re.IGNORECASE,
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).strip(" .")


def _strip_fillers(text: str) -> str:
    for pat in _FILLER_OPENERS:
        text = re.sub(pat, "", text, flags=re.IGNORECASE)
    return _normalize(text)


def _apply_shortcuts(text: str) -> str:
    for pattern, replacement in _PHRASE_SHORTCUTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def _fit_length(text: str, max_chars: int) -> str:
    """Shorten at a word boundary without adding an ellipsis."""
    text = _normalize(text)
    if len(text) <= max_chars:
        return text
    for sep in (": ", "; ", " — ", " - ", ", and ", ", "):
        if sep in text:
            left, right = text.split(sep, 1)
            for candidate in (left, right):
                candidate = _normalize(candidate)
                if 12 <= len(candidate) <= max_chars:
                    return candidate
    words = text.split()
    kept: list[str] = []
    for word in words:
        trial = " ".join(kept + [word])
        if len(trial) > max_chars and kept:
            break
        kept.append(word)
    return " ".join(kept) if kept else text[:max_chars].rsplit(" ", 1)[0]


def summarize_bullet(text: str, *, max_chars: int = MAX_BULLET_CHARS) -> str:
    """Compress one narration sentence into a slide bullet."""
    text = _strip_fillers(text)
    text = _apply_shortcuts(text)
    text = text.replace("—", ", ")
    text = _fit_length(text, max_chars)
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def summarize_subtitle(text: str) -> str:
    """One-line deck subtitle from opening narration."""
    return summarize_bullet(text, max_chars=MAX_SUBTITLE_CHARS)


def _split_sentences(body: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+", body.strip())
    return [c.strip() for c in chunks if len(c.strip()) >= 10]


def _split_objectives(body: str) -> list[str]:
    """Split and summarize learning-objective narration."""
    if re.search(r"\bFirst,?\s+", body, re.IGNORECASE):
        body = re.split(r"\bFirst,?\s+", body, maxsplit=1, flags=re.IGNORECASE)[-1]
        chunks = re.split(
            r"\b(?:Second|Third|Fourth|Fifth|Finally),?\s+",
            body,
            flags=re.IGNORECASE,
        )
        parts: list[str] = []
        for chunk in chunks:
            chunk = chunk.strip(" .")
            if chunk:
                parts.append(summarize_bullet(chunk))
        return [p for p in parts if p][:MAX_BULLETS]

    if "you should" in body.lower():
        tail = re.split(r"you should\s+", body, maxsplit=1, flags=re.IGNORECASE)[-1]
        clauses = re.split(r",\s+and\s+|\s+and\s+(?=explain|name|contrast|identify)", tail)
        return [summarize_bullet(c.strip(" .")) for c in clauses if c.strip()][:MAX_BULLETS]

    return [summarize_bullet(s) for s in _split_sentences(body) if not _META_ONLY.match(s)][
        :MAX_BULLETS
    ]


def _example_bullets(title: str, body: str) -> list[str]:
    """Structured short bullets for example slides."""
    bullets: list[str] = []
    m = re.search(r"Example\s+(\d+)\.(\d+)", title, re.IGNORECASE)
    if m:
        bullets.append(f"Example {m.group(1)}.{m.group(2)} — hands-on module")

    for sentence in _split_sentences(body):
        if _META_ONLY.match(sentence):
            continue
        if "module" in sentence.lower() and len(bullets) >= 2:
            bullets.append("Explore the chapter example module")
            break
        summarized = summarize_bullet(sentence)
        if summarized:
            bullets.append(summarized)
        if len(bullets) >= MAX_BULLETS - 1:
            break

    return [b for b in bullets if b.strip()][:MAX_BULLETS]


def prose_to_bullets(title: str, body: str) -> list[str]:
    """Derive concise slide bullets from full narration prose.

    Args:
        title: Slide title (used for heuristics).
        body: Full narration for this slide (also used for TTS / speaker notes).

    Returns:
        Up to ``MAX_BULLETS`` summarized bullets — never ellipsis-truncated copies.
    """
    title_lower = title.lower()

    if "learning objectives" in title_lower:
        bullets = _split_objectives(body)
        if bullets:
            return bullets

    if "takeaway" in title_lower:
        sentences = [
            s for s in _split_sentences(body) if not _META_ONLY.match(s)
        ]
        return [summarize_bullet(s) for s in sentences[:MAX_BULLETS]]

    if title_lower == "next" or title_lower.startswith("next "):
        return [
            "Complete the quiz for this part",
            summarize_bullet(_split_sentences(body)[0]) if _split_sentences(body) else "Continue to the next part",
        ]

    if re.search(r"Example\s+\d+\.\d+", title, re.IGNORECASE):
        return _example_bullets(title, body)

    sentences = [s for s in _split_sentences(body) if not _META_ONLY.match(s)]
    bullets = [summarize_bullet(s) for s in sentences[:MAX_BULLETS]]
    return bullets or [summarize_bullet(body)]


def example_module_command(title: str, chapter: int | None) -> str | None:
    """Return a demo command when the slide title names an example module."""
    if chapter is None:
        return None
    m = re.search(r"Example\s+(\d+)\.(\d+)", title, re.IGNORECASE)
    if not m:
        return None
    ex_ch, ex_num = m.group(1), m.group(2)
    if int(ex_ch) != chapter:
        return None
    return f"cd modules/chapter{chapter}/example{ex_num}/ && bash run.sh"
