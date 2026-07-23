#!/usr/bin/env python3
"""Build static HTML website from lectures/ content for GitHub Pages."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

BOOK_TITLE = "Fundamental of Dataset: Collection, Annotation, and Management"
BOOK_SHORT = "Dataset Fundamentals"
# Learner-facing label for unit folders under parts/part-*.
UNIT_LABEL = "Part"
UNIT_LABEL_LOWER = "part"
SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_SRC = SCRIPT_DIR / "site_assets"
MAX_PREVIEW_CHARS = 8_000
RESULT_FILE_NAMES = (
    "output.txt",
    "outputs.txt",
    "result.txt",
    "results.txt",
    "expected_output.txt",
)
PREVIEW_FILE_NAMES = (
    *RESULT_FILE_NAMES,
    "data.csv",
    "metadata.json",
    "query.sql",
    "schema.sql",
    "main.py",
)
PREVIEW_SUFFIXES = (".csv", ".json", ".sql", ".py", ".txt")

# Loaded from lectures/site.json at build start (GA4 measurement id, etc.).
_SITE_CONFIG: dict[str, object] = {}


def _esc(text: str) -> str:
    """Escape HTML entities."""
    return html.escape(text, quote=True)


def _md_inline(text: str) -> str:
    """Minimal inline markdown: bold, code, links."""
    text = _esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    return text


def _is_table_row(line: str) -> bool:
    """Return True when a line looks like a markdown table row."""
    stripped = line.strip()
    return (
        stripped.startswith("|")
        and stripped.endswith("|")
        and stripped.count("|") >= 2
    )


def _is_table_separator(line: str) -> bool:
    """Return True for markdown table separator rows."""
    stripped = line.strip().strip("|")
    return bool(stripped) and bool(re.fullmatch(r"[\s\-:|]+", stripped)) and "-" in stripped


def _parse_table_cells(line: str) -> list[str]:
    """Split one markdown table row into cells."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _render_table(rows: list[str]) -> str:
    """Render markdown table rows as an HTML table."""
    if len(rows) < 2:
        return f"<p>{_md_inline(rows[0])}</p>" if rows else ""

    header = _parse_table_cells(rows[0])
    body_rows: list[list[str]] = []
    for row in rows[1:]:
        if _is_table_separator(row):
            continue
        body_rows.append(_parse_table_cells(row))

    head_html = "".join(f"<th>{_md_inline(cell)}</th>" for cell in header)
    body_html = "".join(
        "<tr>" + "".join(f"<td>{_md_inline(cell)}</td>" for cell in row) + "</tr>"
        for row in body_rows
    )
    return (
        '<div class="md-table-wrap"><table class="md-table">'
        f"<thead><tr>{head_html}</tr></thead>"
        f"<tbody>{body_html}</tbody>"
        "</table></div>"
    )


def _extract_module_meta(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    """Pull title metadata lines out of the README body."""
    meta_line = re.compile(r"^\*\*([^*]+):\*\*\s*(.+)$")
    lines = markdown.splitlines()
    kept: list[str] = []
    meta: list[tuple[str, str]] = []
    past_title = False

    for line in lines:
        if line.startswith("# "):
            past_title = True
            continue
        if past_title and not line.startswith("##"):
            match = meta_line.match(line.strip())
            if match:
                meta.append((match.group(1), match.group(2)))
                continue
        kept.append(line)

    return "\n".join(kept).strip(), meta


def _module_meta_html(meta: list[tuple[str, str]]) -> str:
    """Render extracted README metadata as a compact grid."""
    if not meta:
        return ""
    items = "".join(
        f'<div class="module-meta-item"><span>{_esc(label)}</span>'
        f"<strong>{_md_inline(value)}</strong></div>"
        for label, value in meta
    )
    return f'<div class="module-meta">{items}</div>'


def _md_to_html(md: str) -> str:
    """Convert a subset of markdown to HTML."""
    lines = md.strip().splitlines()
    out: list[str] = []
    in_ul = False
    in_ol = False
    in_code = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            close_lists()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            index += 1
            continue

        if in_code:
            out.append(_esc(line))
            index += 1
            continue

        if not stripped:
            close_lists()
            index += 1
            continue

        if _is_table_row(stripped):
            close_lists()
            table_rows: list[str] = []
            while index < len(lines) and _is_table_row(lines[index].strip()):
                table_rows.append(lines[index].strip())
                index += 1
            out.append(_render_table(table_rows))
            continue

        if stripped.startswith("# "):
            close_lists()
            out.append(f"<h1>{_md_inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_lists()
            out.append(f"<h2>{_md_inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_lists()
            out.append(f"<h3>{_md_inline(stripped[4:])}</h3>")
        elif stripped.startswith("- "):
            if in_ol:
                close_lists()
            if not in_ul:
                out.append("<ul class='objectives'>")
                in_ul = True
            out.append(f"<li>{_md_inline(stripped[2:])}</li>")
        elif (ol_match := re.match(r"^\d+\.\s+(.*)$", stripped)):
            if in_ul:
                close_lists()
            if not in_ol:
                out.append("<ol class='objectives'>")
                in_ol = True
            out.append(f"<li>{_md_inline(ol_match.group(1))}</li>")
        else:
            close_lists()
            out.append(f"<p>{_md_inline(stripped)}</p>")

        index += 1

    close_lists()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def _first_heading(markdown: str, fallback: str) -> str:
    """Return the first top-level markdown heading, or a fallback."""
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _section_excerpt(markdown: str, heading: str) -> str:
    """Extract a short prose excerpt from a named markdown section."""
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    rest = markdown[match.end() :].strip()
    next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
    section = rest[: next_heading.start()].strip() if next_heading else rest
    lines = [line.strip("- ").strip() for line in section.splitlines() if line.strip()]
    return " ".join(lines[:3])


def _expected_output_from_readme(markdown: str) -> str:
    """Extract the fenced block under ``## Expected output`` if present."""
    pattern = re.compile(r"^##\s+Expected output\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    rest = markdown[match.end() :].strip()
    next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
    section = rest[: next_heading.start()].strip() if next_heading else rest
    fenced = re.search(r"```(?:\w*)?\n(.*?)```", section, re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    return section.strip()


def _drop_markdown_sections(markdown: str, headings: set[str]) -> str:
    """Remove named level-2 sections from markdown before website rendering."""
    lines = markdown.splitlines()
    kept: list[str] = []
    skipping = False
    normalized = {heading.lower() for heading in headings}
    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            skipping = match.group(1).strip().lower() in normalized
            if skipping:
                continue
        if not skipping:
            kept.append(line)
    return "\n".join(kept)


def _chapter_sort_key(path: Path) -> int:
    """Sort chapter folders by their printed chapter number."""
    match = re.search(r"chapter(\d+)$", path.name, re.IGNORECASE)
    if not match:
        return 10_000
    return int(match.group(1))


def _example_sort_key(path: Path) -> tuple[int, str]:
    """Sort example folders by their printed example number."""
    match = re.search(r"example(\d+)([a-z]?)$", path.name, re.IGNORECASE)
    if not match:
        return (10_000, path.name)
    return (int(match.group(1)), match.group(2))


def _module_dir_from_label(lectures_root: Path, label: str) -> Path | None:
    """Resolve ``eg:N.M`` to ``lectures/modules/chapterN/exampleM``."""
    match = re.fullmatch(r"eg:(\d+)\.(\d+[a-z]?)", label.strip(), re.IGNORECASE)
    if not match:
        return None
    chapter, example = match.groups()
    return lectures_root / "modules" / f"chapter{chapter}" / f"example{example}"


def _module_label(module_dir: Path) -> str:
    """Return an ``eg:N.M`` label for a module path."""
    chapter = module_dir.parent.name.replace("chapter", "")
    example = module_dir.name.replace("example", "")
    return f"eg:{chapter}.{example}"


def _module_title(module_dir: Path) -> str:
    """Return module title from README or a generated label."""
    label = _module_label(module_dir)
    readme = module_dir / "README.md"
    if readme.is_file():
        return _first_heading(readme.read_text(encoding="utf-8"), f"Example {label[3:]}")
    return f"Example {label[3:]}"


def _preview_candidates(module_dir: Path) -> list[Path]:
    """Return learner-facing files worth previewing on static pages."""
    files = [path for path in module_dir.iterdir() if path.is_file() and not path.name.startswith(".")]
    selected: list[Path] = []
    for name in PREVIEW_FILE_NAMES:
        path = module_dir / name
        if path.is_file():
            selected.append(path)
    selected.extend(
        path
        for path in files
        if path.suffix.lower() in PREVIEW_SUFFIXES
        and path.name not in {"README.md", "install.sh", "run.sh"}
        and path not in selected
    )

    def score(path: Path) -> tuple[int, str]:
        result_rank = 0 if path.name in RESULT_FILE_NAMES else 1
        return (result_rank, path.name)

    return sorted(selected, key=score)[:4]


def _file_preview_html(path: Path, from_dir: Path, label: str | None = None) -> str:
    """Render one static file preview with a download/open link."""
    title = label or path.name
    text = path.read_text(encoding="utf-8", errors="replace")
    truncated = len(text) > MAX_PREVIEW_CHARS
    if truncated:
        text = text[:MAX_PREVIEW_CHARS].rstrip() + "\n..."
    href_text = Path(os.path.relpath(path, from_dir)).as_posix()
    return f"""
<details class="module-file" open>
  <summary>{_esc(title)}</summary>
  <div class="module-file-actions"><a href="{_esc(href_text)}">Open raw file</a></div>
  <pre><code>{_esc(text)}</code></pre>
</details>
"""


def _slides_to_html(slides_path: Path) -> str:
    """Render Marp slides.md as HTML slide cards."""
    if not slides_path.is_file():
        return "<p>Slides not found.</p>"
    text = slides_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3 :].strip()
    chunks = [c.strip() for c in text.split("\n---\n") if c.strip()]
    cards: list[str] = []
    for chunk in chunks:
        lines = chunk.splitlines()
        title = "Slide"
        bullets: list[str] = []
        code_lines: list[str] = []
        in_fence = False
        for line in lines:
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                code_lines.append(line)
                continue
            if line.startswith("# "):
                title = line[2:].strip()
            elif line.startswith("## "):
                title = line[3:].strip()
            elif line.startswith("- "):
                bullets.append(_md_inline(line[2:]))
            elif line.strip() and not line.startswith("#"):
                bullets.append(_md_inline(line.strip()))
        if code_lines:
            body = f"<pre><code>{_esc(chr(10).join(code_lines))}</code></pre>"
        elif bullets:
            lis = "".join(f"<li>{b}</li>" for b in bullets)
            body = f"<ul>{lis}</ul>"
        else:
            body = ""
        cards.append(f'<div class="slide-card"><h3>{_esc(title)}</h3>{body}</div>')
    return '<div class="slides-deck">' + "".join(cards) + "</div>"


def _transcript_to_html(transcript_path: Path) -> str:
    """Render transcript.md sections as HTML."""
    if not transcript_path.is_file():
        return ""
    text = transcript_path.read_text(encoding="utf-8")
    parts = re.split(r"\n## ", text)
    blocks: list[str] = []
    for part in parts[1:]:
        lines = part.splitlines()
        heading = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        if not body:
            continue
        paras = "".join(
            f"<p>{_md_inline(p)}</p>" for p in body.split("\n\n") if p.strip()
        )
        blocks.append(
            f'<div class="transcript"><h3>{_esc(heading)}</h3>{paras}</div>'
        )
    return "".join(blocks)


def _rel_site_path(from_dir: Path, lectures_root: Path) -> str:
    """Relative path prefix from HTML file directory to lectures root."""
    depth = len(from_dir.relative_to(lectures_root).parts)
    if depth == 0:
        return ""
    return "/".join([".."] * depth) + "/"


def _rel_asset_path(from_dir: Path, lectures_root: Path) -> str:
    """Relative path from HTML file directory to lectures/assets/."""
    site = _rel_site_path(from_dir, lectures_root)
    return f"{site}assets" if site else "assets"


def _load_site_config(lectures_root: Path) -> dict[str, object]:
    """Load optional lectures/site.json (GA4 id, owner email)."""
    global _SITE_CONFIG
    path = lectures_root / "site.json"
    if not path.is_file():
        _SITE_CONFIG = {}
        return _SITE_CONFIG
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    _SITE_CONFIG = data
    return _SITE_CONFIG


def _ga4_measurement_id() -> str:
    """Return configured GA4 Measurement ID (G-…) or empty string."""
    raw = str(_SITE_CONFIG.get("ga4_measurement_id") or "").strip()
    if raw.startswith("G-") and len(raw) >= 4:
        return raw
    return ""


def _ga4_head_html() -> str:
    """gtag.js snippet for the page <head>, or empty when GA4 is not configured."""
    mid = _ga4_measurement_id()
    if not mid:
        return ""
    safe = _esc(mid)
    return f"""  <script async src="https://www.googletagmanager.com/gtag/js?id={safe}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{safe}', {{ send_page_view: true }});
  </script>
"""


def _tool_extra_head(asset_prefix: str, tool_css: str) -> str:
    """Tool CSS plus shared report (PDF / figure export) stylesheet."""
    return (
        f'  <link rel="stylesheet" href="{tool_css}">\n'
        f'  <link rel="stylesheet" href="{asset_prefix}/tools-report.css">'
    )


def _tool_footer_scripts(asset_prefix: str, scripts: str) -> str:
    """Handoff + axis helpers + report API first, then tool scripts."""
    return (
        f'  <script src="{asset_prefix}/tools-handoff.js"></script>\n'
        f'  <script src="{asset_prefix}/tools-charts-axis.js"></script>\n'
        f'  <script src="{asset_prefix}/tools-report.js"></script>\n'
        + scripts.rstrip()
        + "\n"
    )


def _primary_nav_html(site_root: str, section: str = "") -> str:
    """Platform top nav. section is lectures|tools|project|examples|community|''."""
    prefix = f"{site_root}/" if site_root else ""
    items = (
        ("lectures", f"{prefix}index.html#lectures", "Lectures"),
        ("tools", f"{prefix}tools/index.html", "Tools"),
        ("project", f"{prefix}project/index.html", "Project"),
        ("examples", f"{prefix}modules/index.html", "Examples"),
        ("community", f"{prefix}community/index.html", "Community"),
    )
    bits: list[str] = []
    for key, href, label in items:
        if key == section:
            bits.append(
                f'<a href="{_esc(href)}" class="is-active" aria-current="page">'
                f"{_esc(label)}</a>"
            )
        else:
            bits.append(f'<a href="{_esc(href)}">{_esc(label)}</a>')
    return "\n        ".join(bits)


def _page_shell(
    title: str,
    body: str,
    asset_prefix: str,
    nav: str,
    *,
    eyebrow: str = "",
    extra_head: str = "",
    footer_scripts: str = "",
    section: str = "",
) -> str:
    """Wrap content in site HTML shell."""
    # When asset_prefix is "assets" (home), brand points to index.html.
    # When asset_prefix is "../assets" (chapter), brand should be ../index.html.
    # When asset_prefix is "../../../assets" (clip), brand should be ../../../index.html.
    site_root = asset_prefix.replace("assets", "").rstrip("/")
    if site_root:
        brand_href = f"{site_root}/index.html"
    else:
        brand_href = "index.html"

    eyebrow_html = f'<div class="eyebrow">{_esc(eyebrow)}</div>' if eyebrow else ""
    crumb = ""
    if nav.strip():
        crumb = (
            f'\n    <div class="site-header-crumb">'
            f'<nav aria-label="Breadcrumb">{nav}</nav></div>'
        )
    ga_head = _ga4_head_html()
    privacy = ""
    if _ga4_measurement_id():
        privacy = (
            '\n  <p class="site-footer-privacy">Anonymous usage analytics '
            "(Google Analytics) help improve these materials.</p>"
        )
    # Keep extra_head after GA so page-specific tags can override if needed.
    head_bits = "\n".join(part for part in (ga_head.rstrip(), extra_head.strip()) if part)
    head_block = f"\n  {head_bits}" if head_bits else ""
    primary = _primary_nav_html(site_root, section)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_esc(title)} — {_esc(BOOK_SHORT)}</title>
  <link rel="stylesheet" href="{asset_prefix}/site.css">{head_block}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="site-header-inner">
      <p class="brand"><a href="{brand_href}">{_esc(BOOK_SHORT)}</a></p>
      <nav class="site-nav" aria-label="Site">
        {primary}
      </nav>
    </div>{crumb}
  </header>
  <main id="main">
    {eyebrow_html}
    {body}
  </main>
  <footer class="site-footer">Open learning platform for {_esc(BOOK_TITLE)}{privacy}</footer>
  {footer_scripts}
  <script src="{asset_prefix}/site.js"></script>
</body>
</html>
"""


def _video_html(video_rel: str) -> str:
    """Video embed with graceful placeholder."""
    return f"""<section class="video-panel" aria-label="{UNIT_LABEL} video">
  <div class="video-wrap">
    <video controls preload="metadata" playsinline>
      <source src="{_esc(video_rel)}" type="video/mp4">
    </video>
    <div class="video-placeholder" hidden>
      Video not available yet. Download the PPTX/PDF and continue with the quiz.
    </div>
  </div>
</section>"""


def _copy_assets(lectures_root: Path) -> None:
    """Copy CSS/JS into lectures/assets/."""
    dest = lectures_root / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("site.css", "quiz.js", "site.js"):
        shutil.copy2(ASSETS_SRC / name, dest / name)
    (lectures_root / ".nojekyll").write_text("", encoding="utf-8")


def _clip_neighbors(
    clips: list[dict[str, object]], clip_id: str
) -> tuple[dict[str, object] | None, dict[str, object] | None, int]:
    """Return previous clip, next clip, and 1-based index."""
    for i, clip in enumerate(clips):
        if clip.get("id") == clip_id:
            prev_clip = clips[i - 1] if i > 0 else None
            next_clip = clips[i + 1] if i + 1 < len(clips) else None
            return prev_clip, next_clip, i + 1
    return None, None, 1


def _unit_page_href(clip: dict[str, object]) -> str:
    """Return relative href to a part/clip page from the chapter directory."""
    path = str(clip.get("path", "")).rstrip("/")
    if path:
        return f"{path}/index.html"
    return f"parts/{clip['id']}/index.html"


def _module_card_html(module_dir: Path, from_dir: Path) -> str:
    """Render a compact card for one example module."""
    readme = module_dir / "README.md"
    markdown = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    title = _module_title(module_dir)
    label = _module_label(module_dir)
    objective = _section_excerpt(markdown, "Learning objective")
    files = _preview_candidates(module_dir)
    href = Path(os.path.relpath(module_dir / "index.html", from_dir)).as_posix()
    file_list = ""
    if files:
        names = ", ".join(f"<code>{_esc(path.name)}</code>" for path in files[:3])
        file_list = f"<p class='module-files-inline'>Preview files: {names}</p>"
    objective_html = f"<p>{_md_inline(objective)}</p>" if objective else ""
    return f"""
<article class="module-card">
  <div>
    <span class="pill pill-muted">{_esc(label)}</span>
    <h3>{_esc(title)}</h3>
    {objective_html}
    {file_list}
  </div>
  <a class="btn btn-secondary" href="{_esc(href)}">View files and result</a>
</article>
"""


def _clip_examples_html(
    clip: dict[str, object], lectures_root: Path, from_dir: Path
) -> str:
    """Render static module cards for the examples attached to a clip."""
    labels = [str(label) for label in clip.get("examples", [])]
    cards: list[str] = []
    for label in labels:
        module_dir = _module_dir_from_label(lectures_root, label)
        if module_dir is None or not module_dir.is_dir():
            continue
        cards.append(_module_card_html(module_dir, from_dir))
    if not cards:
        return ""
    return f"""
<section class="examples-panel" id="examples">
  <h2>Example files and results</h2>
  <p class="lead">These examples are shown as static files for GitHub Pages. Open the module
  to inspect the data, source files, and any saved expected result.</p>
  <div class="module-grid">{''.join(cards)}</div>
</section>
"""


def build_module_page(module_dir: Path, lectures_root: Path) -> Path:
    """Build one static example module page."""
    module_dir.mkdir(parents=True, exist_ok=True)
    asset_prefix = _rel_asset_path(module_dir, lectures_root)
    site_prefix = _rel_site_path(module_dir, lectures_root)
    label = _module_label(module_dir)
    title = _module_title(module_dir)
    chapter = module_dir.parent.name.replace("chapter", "")
    readme = module_dir / "README.md"
    readme_html = ""
    expected_output_html = ""
    meta_html = ""
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        expected = _expected_output_from_readme(readme_text)
        if expected:
            expected_output_html = f"""
<div class="expected-result">
  <h2>Expected result</h2>
  <pre><code>{_esc(expected)}</code></pre>
</div>
"""
        readme_text, meta = _extract_module_meta(readme_text)
        meta_html = _module_meta_html(meta)
        readme_text = _drop_markdown_sections(
            readme_text,
            {"Prerequisites", "Setup", "Run", "Expected output"},
        )
        readme_html = _md_to_html(readme_text)

    previews = "".join(
        _file_preview_html(path, module_dir, "Expected result" if path.name in RESULT_FILE_NAMES else None)
        for path in _preview_candidates(module_dir)
    )
    if not previews:
        previews = "<p>No previewable data or result files are packaged for this module yet.</p>"

    nav = (
        f'<a href="{site_prefix}index.html">Home</a>'
        f'<a href="{site_prefix}modules/index.html">Examples</a>'
        f'<a href="../index.html">Chapter {chapter}</a>'
        f'<span class="here">{_esc(label)}</span>'
    )
    body = f"""
<section class="hero">
  <h1>{_esc(title)}</h1>
  <div class="clip-meta">
    <span class="pill">{_esc(label)}</span>
    <span class="pill pill-muted">Chapter {chapter}</span>
    <span class="pill pill-muted">Static preview</span>
  </div>
  <p class="lead">GitHub Pages cannot execute this module, so the site presents the
  packaged notes, source/data files, and saved expected result when available.</p>
  {meta_html}
</section>

<details class="panel" open>
  <summary>Module notes</summary>
  <div class="panel-body module-readme">{readme_html}</div>
</details>

<section class="module-previews">
  <h2>Files and expected result</h2>
  {expected_output_html}
  {previews}
</section>
"""
    out_file = module_dir / "index.html"
    out_file.write_text(
        _page_shell(
            title,
            body,
            asset_prefix,
            nav,
            eyebrow="Example module",
            section="examples",
        ),
        encoding="utf-8",
    )
    return out_file


def build_module_chapter_page(chapter_dir: Path, lectures_root: Path) -> Path:
    """Build a chapter-level index of example modules."""
    chapter = chapter_dir.name.replace("chapter", "")
    asset_prefix = _rel_asset_path(chapter_dir, lectures_root)
    site_prefix = _rel_site_path(chapter_dir, lectures_root)
    examples = sorted(
        [path for path in chapter_dir.glob("example*") if path.is_dir()],
        key=_example_sort_key,
    )
    cards = "".join(_module_card_html(path, chapter_dir) for path in examples)
    nav = (
        f'<a href="{site_prefix}index.html">Home</a>'
        f'<a href="../index.html">Examples</a>'
        f'<span class="here">Chapter {chapter}</span>'
    )
    body = f"""
<section class="hero">
  <h1>Chapter {chapter} examples</h1>
  <p class="lead">Browse the packaged files and expected outputs for this chapter's
  hands-on examples. These pages are static previews for GitHub Pages.</p>
</section>
<div class="module-grid">{cards}</div>
"""
    out_file = chapter_dir / "index.html"
    out_file.write_text(
        _page_shell(
            f"Chapter {chapter} examples",
            body,
            asset_prefix,
            nav,
            eyebrow="Examples",
            section="examples",
        ),
        encoding="utf-8",
    )
    return out_file


def build_modules_pages(lectures_root: Path, chapter: int | None = None) -> list[Path]:
    """Build the static examples section under ``lectures/modules``."""
    modules_root = lectures_root / "modules"
    if not modules_root.is_dir():
        return []

    written: list[Path] = []
    chapter_dirs = sorted(
        [path for path in modules_root.glob("chapter*") if path.is_dir()],
        key=_chapter_sort_key,
    )
    if chapter is not None:
        chapter_dirs = [path for path in chapter_dirs if path.name == f"chapter{chapter}"]

    for chapter_dir in chapter_dirs:
        written.append(build_module_chapter_page(chapter_dir, lectures_root))
        for module_dir in sorted(chapter_dir.glob("example*"), key=_example_sort_key):
            if module_dir.is_dir():
                written.append(build_module_page(module_dir, lectures_root))

    all_chapters = sorted(
        [path for path in modules_root.glob("chapter*") if path.is_dir()],
        key=_chapter_sort_key,
    )
    items = ""
    for path in all_chapters:
        examples = len([p for p in path.glob("example*") if p.is_dir()])
        chapter_num = path.name.replace("chapter", "")
        items += (
            "<li>"
            f'<a href="{path.name}/index.html">Chapter {chapter_num} examples</a>'
            f'<div class="chapter-meta">{examples} packaged modules · static files and results</div>'
            "</li>"
        )

    asset_prefix = _rel_asset_path(modules_root, lectures_root)
    site_prefix = _rel_site_path(modules_root, lectures_root)
    nav = f'<a href="{site_prefix}index.html">Home</a><span class="here">Examples</span>'
    body = f"""
<section class="hero">
  <h1>Examples and files</h1>
  <p class="lead">Browse the companion modules as static teaching artifacts: README
  notes, source/data files, and saved expected outputs where available.</p>
</section>
<ul class="chapter-list">{items}</ul>
"""
    out_file = modules_root / "index.html"
    out_file.write_text(
        _page_shell(
            "Examples and files",
            body,
            asset_prefix,
            nav,
            eyebrow="Examples",
            section="examples",
        ),
        encoding="utf-8",
    )
    written.append(out_file)
    return written


def build_clip_page(
    chapter_dir: Path,
    clip: dict[str, object],
    lectures_root: Path,
    all_clips: list[dict[str, object]],
) -> Path:
    """Build HTML page for one clip."""
    clip_path = chapter_dir / str(clip["path"]).rstrip("/")
    out_dir = clip_path
    out_dir.mkdir(parents=True, exist_ok=True)
    asset_prefix = _rel_asset_path(out_dir, lectures_root)
    site_prefix = _rel_site_path(out_dir, lectures_root)

    slides_html = _slides_to_html(clip_path / "slides.md")
    transcript_body = _transcript_to_html(clip_path / "transcript.md")

    quiz_path = clip_path / "quiz.json"
    quiz_json = quiz_path.read_text(encoding="utf-8") if quiz_path.is_file() else "{}"

    objectives = ""
    page_md = clip_path / "page.md"
    if page_md.is_file():
        md = page_md.read_text(encoding="utf-8")
        if "## Objectives" in md:
            obj_block = md.split("## Objectives", 1)[1].split("##", 1)[0]
            objectives = _md_to_html("## Learning objectives\n" + obj_block.strip())

    ch_num = chapter_dir.name.replace("chapter", "")
    prev_clip, next_clip, index = _clip_neighbors(all_clips, str(clip["id"]))
    total = len(all_clips)

    nav = (
        f'<a href="{site_prefix}index.html">Home</a>'
        f'<a href="{site_prefix}chapter{ch_num}/index.html">Chapter {ch_num}</a>'
        f'<span class="here">{UNIT_LABEL} {index}/{total}</span>'
    )

    downloads: list[str] = []
    if (clip_path / "clip.pptx").is_file():
        downloads.append('<a class="btn btn-secondary" href="clip.pptx">Download PPTX</a>')
    if (clip_path / "clip.pdf").is_file():
        downloads.append('<a class="btn btn-secondary" href="clip.pdf">Download PDF</a>')
    if clip.get("examples"):
        downloads.append('<a class="btn btn-secondary" href="#examples">View examples</a>')
    for tool in clip.get("tools", []):
        href = str(tool.get("href", ""))
        label = str(tool.get("label", "Open tool"))
        if href:
            downloads.append(f'<a class="btn btn-secondary" href="{_esc(href)}">{_esc(label)}</a>')
    downloads.append('<a class="btn btn-ghost" href="#quiz">Jump to quiz</a>')

    prev_html = (
        f'<a class="btn btn-secondary clip-toolbar-prev" href="../{_esc(str(prev_clip["id"]))}/index.html">← Previous</a>'
        if prev_clip
        else '<span class="btn btn-secondary clip-toolbar-prev is-disabled">← Previous</span>'
    )
    if next_clip:
        next_href = f'../{_esc(str(next_clip["id"]))}/index.html'
        next_title = str(next_clip["title"])
        next_html = (
            f'<a class="btn clip-toolbar-next" href="{next_href}"'
            f' title="{_esc(next_title)}">Next →</a>'
        )
        quiz_next_attrs = (
            f' data-next-href="{next_href}"'
            f' data-next-label="Continue to {_esc(str(next_clip["title"]))}"'
        )
    else:
        next_html = (
            f'<a class="btn clip-toolbar-next" href="{site_prefix}chapter{ch_num}/index.html"'
            ' title="Back to chapter learning path">Finish →</a>'
        )
        quiz_next_attrs = (
            f' data-next-href="{site_prefix}chapter{ch_num}/index.html"'
            ' data-next-label="Back to chapter learning path"'
        )

    transcript_panel = ""
    if transcript_body:
        transcript_panel = f"""
<details class="panel" data-persist="transcript">
  <summary>Transcript</summary>
  <div class="panel-body">{transcript_body}</div>
</details>
"""

    examples_html = _clip_examples_html(clip, lectures_root, out_dir)
    tools_callout = ""
    tool_links = clip.get("tools", [])
    if tool_links:
        items = "".join(
            f'<a class="btn btn-secondary" href="{_esc(str(t.get("href", "")))}">'
            f'{_esc(str(t.get("label", "Open tool")))}</a>'
            for t in tool_links
            if t.get("href")
        )
        if items:
            tools_callout = f"""
<section class="panel sp-tool-callout" id="tools">
  <h2>Try it</h2>
  <p class="lead">Practice this part's ideas in the browser.</p>
  <div class="deck-links">{items}</div>
</section>
"""
    toolbar_items = [prev_html, *downloads, next_html]

    body = f"""
<section class="hero">
  <h1>{_esc(str(clip["title"]))}</h1>
  <div class="clip-meta">
    <span class="pill">~{clip.get("estimate_min", "?")} min</span>
    <span class="pill pill-muted">Chapter {ch_num}</span>
    <span class="pill pill-muted">{UNIT_LABEL} {index} of {total}</span>
  </div>
  <nav class="clip-toolbar" aria-label="{UNIT_LABEL} actions and navigation">
    {"".join(toolbar_items)}
  </nav>
</section>

{_video_html("video.mp4")}

{objectives}

{tools_callout}

{examples_html}

<details class="panel" data-persist="slides">
  <summary>Slides overview</summary>
  <div class="panel-body">{slides_html}</div>
</details>

{transcript_panel}

<section class="quiz-section" id="quiz">
  <div id="quiz-root"{quiz_next_attrs}></div>
  <script id="quiz-data" type="application/json">{quiz_json}</script>
  <script src="{asset_prefix}/quiz.js"></script>
</section>
"""
    out_file = out_dir / "index.html"
    out_file.write_text(
        _page_shell(
            str(clip["title"]),
            body,
            asset_prefix,
            nav,
            eyebrow=f"Chapter {ch_num} · Guided {UNIT_LABEL_LOWER}",
            section="lectures",
        ),
        encoding="utf-8",
    )
    return out_file


def build_chapter_page(chapter_dir: Path, lectures_root: Path) -> Path:
    """Build chapter learning-path HTML from chapter.json."""
    meta_path = chapter_dir / "chapter.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
    ch_num = meta["chapter"]
    out_dir = chapter_dir
    asset_prefix = _rel_asset_path(out_dir, lectures_root)
    site_prefix = _rel_site_path(out_dir, lectures_root)
    clips = list(meta.get("parts", []))

    nav = (
        f'<a href="{site_prefix}index.html">Home</a>'
        f'<span class="here">Chapter {ch_num}</span>'
    )

    intro = (
        f"<p class='lead'>Follow the path in order: read the bridge, watch the {UNIT_LABEL_LOWER}, "
        "then take the quiz before moving on. Downloads are available if you prefer "
        "to study offline.</p>"
    )

    deck_links = ['<div class="deck-links">']
    if (chapter_dir / f"chapter{ch_num}.pptx").is_file():
        deck_links.append(
            f'<a class="btn" href="chapter{ch_num}.pptx">Full chapter PPTX</a>'
        )
    if (chapter_dir / f"chapter{ch_num}.pdf").is_file():
        deck_links.append(
            f'<a class="btn btn-secondary" href="chapter{ch_num}.pdf">Full chapter PDF</a>'
        )
    if clips:
        first = clips[0]
        deck_links.append(
            f'<a class="btn btn-ghost" href="{_esc(_unit_page_href(first))}">'
            f"Start first {UNIT_LABEL_LOWER} →</a>"
        )
    if (lectures_root / "modules" / f"chapter{ch_num}").is_dir():
        deck_links.append(
            f'<a class="btn btn-secondary" href="../modules/chapter{ch_num}/index.html">'
            "Browse examples</a>"
        )
    deck_links.append("</div>")

    objectives = "<h2>What you will learn</h2><ul class='objectives'>"
    for obj in meta.get("objectives", []):
        objectives += f"<li>{_esc(str(obj))}</li>"
    objectives += "</ul>"

    progress = '<div class="path-progress" aria-hidden="true">'
    for _ in clips:
        progress += '<div class="path-dot"></div>'
    progress += "</div>"

    path_html = f"<h2>Learning path</h2>{progress}"
    total_min = 0
    for i, clip in enumerate(clips, start=1):
        bridge = clip.get("bridge_in", "")
        clip_url = _unit_page_href(clip)
        estimate = int(clip.get("estimate_min", 0) or 0)
        total_min += estimate
        clip_root = chapter_dir / str(clip["path"]).rstrip("/")
        has_video = (clip_root / "video.mp4").is_file() or (
            clip_root / "video" / "clip.mp4"
        ).is_file()
        video_pill = (
            '<span class="pill">Video ready</span>'
            if has_video
            else '<span class="pill pill-muted">Slides + quiz</span>'
        )
        examples = [str(label) for label in clip.get("examples", [])]
        example_links = ""
        if examples:
            example_links = "<div class='example-pills'>" + "".join(
                f'<a class="pill pill-muted" href="../modules/chapter{ch_num}/example{label.split(".")[1]}/index.html">{_esc(label)}</a>'
                for label in examples
                if "." in label
            ) + "</div>"
        path_html += f"""
<div class="learning-step" id="step-{i}">
  <div class="bridge">
    <span class="bridge-label">Before {UNIT_LABEL_LOWER} {i}</span>
    {_esc(str(bridge))}
  </div>
  <div class="clip-card">
    <div class="clip-card-top">
      <div>
        <div class="clip-index">{UNIT_LABEL} {i} of {len(clips)}</div>
        <h3>{_esc(str(clip["title"]))}</h3>
      </div>
      <div class="clip-meta">
        <span class="pill">~{clip.get("estimate_min", "?")} min</span>
        {video_pill}
      </div>
    </div>
    <div class="clip-links">
      <a class="btn" href="{_esc(clip_url)}">Open {UNIT_LABEL_LOWER}</a>
      <a class="btn btn-secondary" href="{_esc(clip_url)}#quiz">Go to quiz</a>
    </div>
    {example_links}
  </div>
</div>
"""

    wrap_up = f"""
<section class="wrap-up">
  <h2>Wrap-up</h2>
  <p>After about {total_min or "45"} minutes across {len(clips)} {UNIT_LABEL_LOWER}s, you should be ready
  for the next chapter when it is published. Return to the course home anytime.</p>
  <p><a href="{site_prefix}index.html">← All chapters</a></p>
</section>
"""

    body = (
        f"<section class='hero'><h1>{_esc(meta['title'])}</h1>{intro}"
        f"{''.join(deck_links)}</section>"
        f"{objectives}{path_html}{wrap_up}"
    )
    out_file = out_dir / "index.html"
    out_file.write_text(
        _page_shell(
            meta["title"],
            body,
            asset_prefix,
            nav,
            eyebrow=f"Chapter {ch_num} · Learning path",
            section="lectures",
        ),
        encoding="utf-8",
    )

    for clip in clips:
        build_clip_page(chapter_dir, clip, lectures_root, clips)

    return out_file


_PROFILE_LABELS = {
    "linkedin": "LinkedIn",
    "faculty": "Faculty page",
    "website": "Website",
    "facebook": "Facebook",
    "other": "Profile",
}


def _safe_https_url(raw: object) -> str:
    """Return a sanitized https URL, or empty string if invalid."""
    url = str(raw or "").strip()
    if not url:
        return ""
    if not re.match(r"^https://[^\s<>\"']+$", url, re.IGNORECASE):
        return ""
    return url


def _profile_link_html(item: dict[str, object]) -> str:
    """Render an optional profile link for a testimonial card."""
    url = _safe_https_url(item.get("profile_url") or item.get("url"))
    if not url:
        return ""
    kind = str(item.get("profile_type") or "other").strip().lower()
    label = _PROFILE_LABELS.get(kind, _PROFILE_LABELS["other"])
    return (
        f'<a class="comm-profile-link" href="{_esc(url)}" '
        f'target="_blank" rel="noopener noreferrer">{_esc(label)}</a>'
    )


def _render_testimonials(
    testimonials: list[dict[str, object]], *, feedback_href: str
) -> str:
    """Render curated reader testimonials or an empty-state prompt."""
    published = [t for t in testimonials if t.get("published", True) and t.get("quote")]
    if not published:
        return f"""
<div class="comm-empty">
  <p>No published testimonials yet. If this site helped your course or project, share your experience — we review submissions before posting them here.</p>
  <p><a class="btn btn-secondary" href="{_esc(feedback_href)}">Share your story</a></p>
</div>"""
    cards = []
    for item in published:
        quote = _esc(str(item.get("quote", "")))
        name = _esc(str(item.get("name", "Reader")))
        role = _esc(str(item.get("role", "")))
        role_html = f"<span>{role}</span>" if role else ""
        profile_html = _profile_link_html(item)
        cards.append(
            f'<blockquote class="panel comm-testimonial">'
            f'<p class="comm-quote">{quote}</p>'
            f'<footer class="comm-attribution"><strong>{name}</strong>{role_html}'
            f"{profile_html}</footer>"
            f"</blockquote>"
        )
    return f'<div class="comm-testimonials">{"".join(cards)}</div>'


def _community_tool_form_html() -> str:
    """HTML for the tool feedback form."""
    return """
<section class="comm-section panel" id="tool-feedback">
  <h2>Suggest a tool improvement</h2>
  <p>Missing feature? Confusing workflow? Tell us which tool and what would help learners.</p>
  <form class="comm-form" data-form="tool" novalidate>
    <input type="hidden" name="subject" value="[Dataset Fundamentals] Tool feedback">
    <input type="hidden" name="form_type" value="tool_feedback">
    <label class="comm-hp" aria-hidden="true">Leave blank<input type="text" name="botcheck" tabindex="-1" autocomplete="off"></label>
    <div class="comm-field">
      <label for="tool-name">Tool</label>
      <select id="tool-name" name="tool" required>
        <option value="">Select a tool…</option>
        <option value="general">General / new tool idea</option>
        <option value="sampling">Sampling tool (Ch.2)</option>
        <option value="image-annotation">Image annotation (Ch.4)</option>
        <option value="text-annotation">Text annotation (Ch.4)</option>
        <option value="iaa">IAA calculator (Ch.4)</option>
        <option value="storage-format">Storage &amp; format chooser (Ch.12)</option>
        <option value="cleaning">Cleaning workbench (Ch.5)</option>
        <option value="scaling-encoding">Scaling / encoding lab (Ch.5)</option>
        <option value="class-imbalance">Class imbalance explorer (Ch.5)</option>
        <option value="eda-dashboard">EDA dashboard (Ch.1 / Ch.6)</option>
        <option value="schema-format">Schema / format translator (Ch.1)</option>
        <option value="pii-scrubber">Consent &amp; PII scrubber (Ch.3)</option>
        <option value="deid-risk">De-identification risk checker (Ch.3)</option>
        <option value="ethical-decision">Ethical decision tree (Ch.3)</option>
        <option value="train-test-split">Train/test splitter (Ch.1)</option>
        <option value="fairness">Bias &amp; fairness meter (Ch.7)</option>
        <option value="representation">Representation visualizer (Ch.7)</option>
        <option value="datasheet">Datasheet builder (Ch.8)</option>
        <option value="metadata-checker">Metadata checker (Ch.8)</option>
        <option value="version-timeline">Version timeline (Ch.8)</option>
        <option value="text-augmentation">Text augmentation lab (Ch.10)</option>
        <option value="image-augmentation">Image augmentation lab (Ch.10)</option>
        <option value="media-augmentation">Media augmentation lab (Ch.10)</option>
      </select>
    </div>
    <div class="comm-field">
      <label for="tool-name-input">Your name <span class="hint">(optional)</span></label>
      <input id="tool-name-input" name="name" type="text" autocomplete="name">
    </div>
    <div class="comm-field">
      <label for="tool-email">Email <span class="hint">(optional, for follow-up)</span></label>
      <input id="tool-email" name="email" type="email" autocomplete="email">
    </div>
    <div class="comm-field">
      <label for="tool-kind">Feedback type</label>
      <select id="tool-kind" name="feedback_type" required>
        <option value="enhancement">Enhancement idea</option>
        <option value="bug">Bug or confusing step</option>
        <option value="new-tool">Proposal for a new tool</option>
      </select>
    </div>
    <div class="comm-field">
      <label for="tool-message">Message</label>
      <textarea id="tool-message" name="message" required placeholder="What would help learners? Include chapter or example if relevant."></textarea>
    </div>
    <div class="comm-actions">
      <button type="submit" class="btn">Send tool feedback</button>
    </div>
    <div class="comm-status" hidden role="status"></div>
    <p class="comm-privacy">Submissions are sent by email to the site authors via Web3Forms. We do not store them on this static site.</p>
  </form>
</section>"""


def _community_testimonial_form_html() -> str:
    """HTML for the testimonial submission form."""
    return """
<section class="comm-section panel" id="share-testimonial">
  <h2>Share a testimonial</h2>
  <p>Tell us how the book, lectures, or tools helped you. We may publish a short quote on the <a href="../stories/index.html">Reader stories</a> page after review.</p>
  <form class="comm-form" data-form="testimonial" novalidate>
    <input type="hidden" name="subject" value="[Dataset Fundamentals] Testimonial submission">
    <input type="hidden" name="form_type" value="testimonial">
    <label class="comm-hp" aria-hidden="true">Leave blank<input type="text" name="botcheck" tabindex="-1" autocomplete="off"></label>
    <div class="comm-field">
      <label for="test-name">Name</label>
      <input id="test-name" name="name" type="text" required autocomplete="name">
    </div>
    <div class="comm-field">
      <label for="test-role">Role / affiliation <span class="hint">(e.g. course, organization)</span></label>
      <input id="test-role" name="role" type="text" placeholder="Instructor, CS department">
    </div>
    <div class="comm-field">
      <label for="test-email">Email <span class="hint">(optional)</span></label>
      <input id="test-email" name="email" type="email" autocomplete="email">
    </div>
    <div class="comm-field">
      <label for="test-profile-type">Profile link type <span class="hint">(optional — helps readers verify who you are)</span></label>
      <select id="test-profile-type" name="profile_type">
        <option value="">No profile link</option>
        <option value="linkedin">LinkedIn</option>
        <option value="faculty">Faculty / university page</option>
        <option value="website">Personal or lab website</option>
        <option value="facebook">Facebook</option>
        <option value="other">Other</option>
      </select>
    </div>
    <div class="comm-field">
      <label for="test-profile-url">Profile URL <span class="hint">(https:// only)</span></label>
      <input id="test-profile-url" name="profile_url" type="url" inputmode="url" placeholder="https://www.linkedin.com/in/…" autocomplete="url">
    </div>
    <div class="comm-field">
      <label for="test-quote">Your testimonial</label>
      <textarea id="test-quote" name="message" required placeholder="What worked well for you or your students?"></textarea>
    </div>
    <label class="comm-check">
      <input type="checkbox" name="publish_ok" value="yes" required>
      <span>I agree that my quote may be edited for length and published on the Reader stories page with my name, role, and optional profile link.</span>
    </label>
    <div class="comm-actions">
      <button type="submit" class="btn">Submit testimonial</button>
    </div>
    <div class="comm-status" hidden role="status"></div>
    <p class="comm-privacy">We review every submission before publishing. Do not submit if you do not want public attribution.</p>
  </form>
</section>"""


def build_community_pages(lectures_root: Path) -> list[Path]:
    """Build community hub, reader stories, and feedback pages."""
    _load_site_config(lectures_root)
    community_dir = lectures_root / "community"
    config_path = community_dir / "community.json"
    if not config_path.is_file():
        return []

    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    access_key = _esc(str(config.get("web3forms_access_key", "REPLACE_WITH_YOUR_KEY")))
    testimonials = config.get("testimonials", [])
    written: list[Path] = []

    hub_dir = community_dir
    stories_dir = community_dir / "stories"
    feedback_dir = community_dir / "feedback"
    stories_dir.mkdir(parents=True, exist_ok=True)
    feedback_dir.mkdir(parents=True, exist_ok=True)

    hub_asset_prefix = _rel_asset_path(hub_dir, lectures_root)
    hub_site_prefix = _rel_site_path(hub_dir, lectures_root)
    hub_nav = (
        f'<a href="{hub_site_prefix}index.html">Home</a>'
        '<span class="here">Community</span>'
    )
    hub_body = """
<section class="hero comm-hero">
  <h1>Community</h1>
  <p class="lead">Read how others use this platform, or send tool feedback and testimonials to the authors.</p>
</section>
<ul class="chapter-list">
  <li>
    <a href="stories/index.html">Reader stories</a>
    <div class="chapter-meta">Curated testimonials from instructors, students, and practitioners</div>
  </li>
  <li>
    <a href="feedback/index.html">Share feedback</a>
    <div class="chapter-meta">Suggest tool improvements or submit a testimonial for review</div>
  </li>
</ul>
"""
    hub_file = hub_dir / "index.html"
    hub_file.write_text(
        _page_shell(
            "Community",
            hub_body,
            hub_asset_prefix,
            hub_nav,
            eyebrow="Community",
            extra_head='  <link rel="stylesheet" href="community.css">',
            section="community",
        ),
        encoding="utf-8",
    )
    written.append(hub_file)

    stories_asset_prefix = _rel_asset_path(stories_dir, lectures_root)
    stories_site_prefix = _rel_site_path(stories_dir, lectures_root)
    stories_nav = (
        f'<a href="{stories_site_prefix}index.html">Home</a>'
        f'<a href="{stories_site_prefix}community/index.html">Community</a>'
        '<span class="here">Reader stories</span>'
    )
    testimonials_html = _render_testimonials(
        testimonials,
        feedback_href="../feedback/index.html?type=testimonial",
    )
    stories_body = f"""
<section class="hero comm-hero">
  <h1>Reader stories</h1>
  <p class="lead">Experiences from instructors, students, and practitioners using the lectures and interactive tools. Quotes are reviewed before publishing; many include a LinkedIn, faculty page, or other profile link so readers can verify the author.</p>
  <div class="deck-links">
    <a class="btn btn-secondary" href="../feedback/index.html?type=testimonial">Share your story</a>
  </div>
</section>
<section class="comm-section">
  {testimonials_html}
</section>
"""
    stories_file = stories_dir / "index.html"
    stories_file.write_text(
        _page_shell(
            "Reader stories",
            stories_body,
            stories_asset_prefix,
            stories_nav,
            eyebrow="Community",
            extra_head='  <link rel="stylesheet" href="../community.css">',
            section="community",
        ),
        encoding="utf-8",
    )
    written.append(stories_file)

    feedback_asset_prefix = _rel_asset_path(feedback_dir, lectures_root)
    feedback_site_prefix = _rel_site_path(feedback_dir, lectures_root)
    feedback_nav = (
        f'<a href="{feedback_site_prefix}index.html">Home</a>'
        f'<a href="{feedback_site_prefix}community/index.html">Community</a>'
        '<span class="here">Share feedback</span>'
    )
    feedback_body = f"""
<section class="hero comm-hero">
  <h1>Share feedback</h1>
  <p class="lead">Suggest tool improvements or submit a testimonial. Tool feedback is emailed to the authors; testimonials are reviewed before appearing on the <a href="../stories/index.html">Reader stories</a> page.</p>
  <nav class="comm-nav" aria-label="On this page">
    <a href="#tool-feedback">Tool feedback</a>
    <a href="#share-testimonial">Share a testimonial</a>
  </nav>
</section>

<div id="community-root" data-access-key="{access_key}"></div>

<div class="panel comm-setup" id="comm-setup" hidden>
  <strong>Author setup:</strong> Get a free access key at
  <a href="https://web3forms.com" target="_blank" rel="noopener">web3forms.com</a>,
  then set <code>web3forms_access_key</code> in
  <code>lectures/community/community.json</code> and run
  <code>python .cursor/skills/module-slides/scripts/build_site.py lectures/</code>.
</div>

{_community_tool_form_html()}
{_community_testimonial_form_html()}
"""
    feedback_footer = """
  <script src="../community.js"></script>"""
    feedback_file = feedback_dir / "index.html"
    feedback_file.write_text(
        _page_shell(
            "Share feedback",
            feedback_body,
            feedback_asset_prefix,
            feedback_nav,
            eyebrow="Community",
            extra_head='  <link rel="stylesheet" href="../community.css">',
            footer_scripts=feedback_footer,
            section="community",
        ),
        encoding="utf-8",
    )
    written.append(feedback_file)
    return written


def build_tools_pages(lectures_root: Path) -> list[Path]:
    """Build interactive tools hub and tool entry pages."""
    def _tool_shell(*args, **kwargs):
        kwargs.setdefault("section", "tools")
        return _page_shell(*args, **kwargs)

    tools_root = lectures_root / "tools"
    if not tools_root.is_dir():
        return []

    written: list[Path] = []
    asset_prefix = _rel_asset_path(tools_root, lectures_root)
    site_prefix = _rel_site_path(tools_root, lectures_root)
    nav = (
        f'<a href="{site_prefix}index.html">Home</a>'
        '<span class="here">Tools</span>'
    )

    sampling_dir = tools_root / "sampling"
    if sampling_dir.is_dir():
        sampling_asset_prefix = _rel_asset_path(sampling_dir, lectures_root)
        sampling_site_prefix = _rel_site_path(sampling_dir, lectures_root)
        sampling_nav = (
            f'<a href="{sampling_site_prefix}index.html">Home</a>'
            f'<a href="{sampling_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Sampling</span>'
        )
        body = """
<div id="sampling-root"></div>
"""
        footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/rng.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/schema.js"></script>
  <script src="lib/sample.js"></script>
  <script src="lib/stats.js"></script>
  <script src="lib/export.js"></script>
  <script src="sampling.js"></script>"""
        out_file = sampling_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Sampling tool",
                body,
                sampling_asset_prefix,
                sampling_nav,
                eyebrow="Interactive tool · Chapter 2",
                extra_head=_tool_extra_head(sampling_asset_prefix, 'sampling.css'),
                footer_scripts=_tool_footer_scripts(sampling_asset_prefix, footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    image_annotation_dir = tools_root / "image-annotation"
    if image_annotation_dir.is_dir():
        image_annotation_asset_prefix = _rel_asset_path(image_annotation_dir, lectures_root)
        image_annotation_site_prefix = _rel_site_path(image_annotation_dir, lectures_root)
        image_annotation_nav = (
            f'<a href="{image_annotation_site_prefix}index.html">Home</a>'
            f'<a href="{image_annotation_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Image annotation</span>'
        )
        image_annotation_body = """
<div id="annotation-root"></div>
"""
        image_annotation_footer = """
  <script src="data/images-bundle.js"></script>
  <script src="data/guidelines.js"></script>
  <script src="lib/boxes.js"></script>
  <script src="lib/voc.js"></script>
  <script src="lib/coco.js"></script>
  <script src="lib/export.js"></script>
  <script src="annotation.js"></script>"""
        out_file = image_annotation_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Image annotation",
                image_annotation_body,
                image_annotation_asset_prefix,
                image_annotation_nav,
                eyebrow="Interactive tool · Chapter 4",
                extra_head=_tool_extra_head(image_annotation_asset_prefix, 'annotation.css'),
                footer_scripts=_tool_footer_scripts(image_annotation_asset_prefix, image_annotation_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    text_annotation_dir = tools_root / "text-annotation"
    if text_annotation_dir.is_dir():
        text_annotation_asset_prefix = _rel_asset_path(text_annotation_dir, lectures_root)
        text_annotation_site_prefix = _rel_site_path(text_annotation_dir, lectures_root)
        text_annotation_nav = (
            f'<a href="{text_annotation_site_prefix}index.html">Home</a>'
            f'<a href="{text_annotation_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Text annotation</span>'
        )
        text_annotation_body = """
<div id="text-annotation-root"></div>
"""
        text_annotation_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/spans.js"></script>
  <script src="lib/export.js"></script>
  <script src="text-annotation.js"></script>"""
        out_file = text_annotation_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Text annotation",
                text_annotation_body,
                text_annotation_asset_prefix,
                text_annotation_nav,
                eyebrow="Interactive tool · Chapter 4",
                extra_head=_tool_extra_head(text_annotation_asset_prefix, 'text-annotation.css'),
                footer_scripts=_tool_footer_scripts(text_annotation_asset_prefix, text_annotation_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    # Legacy path redirect for bookmarks to tools/annotation/
    legacy_annotation_dir = tools_root / "annotation"
    legacy_annotation_dir.mkdir(parents=True, exist_ok=True)
    legacy_out = legacy_annotation_dir / "index.html"
    legacy_out.write_text(
        """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=../image-annotation/index.html">
  <title>Redirecting…</title>
  <link rel="canonical" href="../image-annotation/index.html">
</head>
<body>
  <p>The annotation tool moved to <a href="../image-annotation/index.html">image annotation</a>.</p>
</body>
</html>
""",
        encoding="utf-8",
    )
    written.append(legacy_out)

    cleaning_dir = tools_root / "cleaning"
    if cleaning_dir.is_dir():
        cleaning_asset_prefix = _rel_asset_path(cleaning_dir, lectures_root)
        cleaning_site_prefix = _rel_site_path(cleaning_dir, lectures_root)
        cleaning_nav = (
            f'<a href="{cleaning_site_prefix}index.html">Home</a>'
            f'<a href="{cleaning_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Cleaning</span>'
        )
        cleaning_body = """
<div id="cleaning-root"></div>
"""
        cleaning_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/profile.js"></script>
  <script src="lib/clean.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="cleaning.js"></script>"""
        out_file = cleaning_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Cleaning workbench",
                cleaning_body,
                cleaning_asset_prefix,
                cleaning_nav,
                eyebrow="Interactive tool · Chapter 5",
                extra_head=_tool_extra_head(cleaning_asset_prefix, 'cleaning.css'),
                footer_scripts=_tool_footer_scripts(cleaning_asset_prefix, cleaning_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    eda_dashboard_dir = tools_root / "eda-dashboard"
    if eda_dashboard_dir.is_dir():
        eda_asset_prefix = _rel_asset_path(eda_dashboard_dir, lectures_root)
        eda_site_prefix = _rel_site_path(eda_dashboard_dir, lectures_root)
        eda_nav = (
            f'<a href="{eda_site_prefix}index.html">Home</a>'
            f'<a href="{eda_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">EDA dashboard</span>'
        )
        eda_body = """
<div id="eda-root"></div>
"""
        eda_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/profile.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="eda.js"></script>"""
        out_file = eda_dashboard_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "EDA dashboard",
                eda_body,
                eda_asset_prefix,
                eda_nav,
                eyebrow="Interactive tool · Chapters 1 & 6",
                extra_head=_tool_extra_head(eda_asset_prefix, 'eda.css'),
                footer_scripts=_tool_footer_scripts(eda_asset_prefix, eda_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    train_test_split_dir = tools_root / "train-test-split"
    if train_test_split_dir.is_dir():
        split_asset_prefix = _rel_asset_path(train_test_split_dir, lectures_root)
        split_site_prefix = _rel_site_path(train_test_split_dir, lectures_root)
        split_nav = (
            f'<a href="{split_site_prefix}index.html">Home</a>'
            f'<a href="{split_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Train/test splitter</span>'
        )
        split_body = """
<div id="split-root"></div>
"""
        split_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/split.js"></script>
  <script src="lib/leakage.js"></script>
  <script src="lib/export.js"></script>
  <script src="train-test-split.js"></script>"""
        out_file = train_test_split_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Train / val / test splitter",
                split_body,
                split_asset_prefix,
                split_nav,
                eyebrow="Interactive tool · Chapter 1",
                extra_head=_tool_extra_head(split_asset_prefix, 'train-test-split.css'),
                footer_scripts=_tool_footer_scripts(split_asset_prefix, split_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    scaling_encoding_dir = tools_root / "scaling-encoding"
    if scaling_encoding_dir.is_dir():
        scale_asset_prefix = _rel_asset_path(scaling_encoding_dir, lectures_root)
        scale_site_prefix = _rel_site_path(scaling_encoding_dir, lectures_root)
        scale_nav = (
            f'<a href="{scale_site_prefix}index.html">Home</a>'
            f'<a href="{scale_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Scaling / encoding</span>'
        )
        scale_body = """
<div id="scale-root"></div>
"""
        scale_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/transform.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="scaling-encoding.js"></script>"""
        out_file = scaling_encoding_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Scaling / encoding lab",
                scale_body,
                scale_asset_prefix,
                scale_nav,
                eyebrow="Interactive tool · Chapter 5",
                extra_head=_tool_extra_head(scale_asset_prefix, 'scaling-encoding.css'),
                footer_scripts=_tool_footer_scripts(scale_asset_prefix, scale_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    class_imbalance_dir = tools_root / "class-imbalance"
    if class_imbalance_dir.is_dir():
        imb_asset_prefix = _rel_asset_path(class_imbalance_dir, lectures_root)
        imb_site_prefix = _rel_site_path(class_imbalance_dir, lectures_root)
        imb_nav = (
            f'<a href="{imb_site_prefix}index.html">Home</a>'
            f'<a href="{imb_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Class imbalance</span>'
        )
        imb_body = """
<div id="imb-root"></div>
"""
        imb_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/stats.js"></script>
  <script src="lib/resample.js"></script>
  <script src="lib/model.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="class-imbalance.js"></script>"""
        out_file = class_imbalance_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Class imbalance explorer",
                imb_body,
                imb_asset_prefix,
                imb_nav,
                eyebrow="Interactive tool · Chapter 5",
                extra_head=_tool_extra_head(imb_asset_prefix, "class-imbalance.css"),
                footer_scripts=_tool_footer_scripts(imb_asset_prefix, imb_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    schema_format_dir = tools_root / "schema-format"
    if schema_format_dir.is_dir():
        schema_asset_prefix = _rel_asset_path(schema_format_dir, lectures_root)
        schema_site_prefix = _rel_site_path(schema_format_dir, lectures_root)
        schema_nav = (
            f'<a href="{schema_site_prefix}index.html">Home</a>'
            f'<a href="{schema_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Schema / format</span>'
        )
        schema_body = """
<div id="schema-root"></div>
"""
        schema_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/schema.js"></script>
  <script src="lib/export.js"></script>
  <script src="schema-format.js"></script>"""
        out_file = schema_format_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Schema / format translator",
                schema_body,
                schema_asset_prefix,
                schema_nav,
                eyebrow="Interactive tool · Chapter 1",
                extra_head=_tool_extra_head(schema_asset_prefix, "schema-format.css"),
                footer_scripts=_tool_footer_scripts(schema_asset_prefix, schema_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    pii_scrubber_dir = tools_root / "pii-scrubber"
    if pii_scrubber_dir.is_dir():
        pii_asset_prefix = _rel_asset_path(pii_scrubber_dir, lectures_root)
        pii_site_prefix = _rel_site_path(pii_scrubber_dir, lectures_root)
        pii_nav = (
            f'<a href="{pii_site_prefix}index.html">Home</a>'
            f'<a href="{pii_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">PII scrubber</span>'
        )
        pii_body = """
<div id="pii-root"></div>
"""
        pii_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/detect.js"></script>
  <script src="lib/scrub.js"></script>
  <script src="lib/export.js"></script>
  <script src="pii-scrubber.js"></script>"""
        out_file = pii_scrubber_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Consent & PII scrubber",
                pii_body,
                pii_asset_prefix,
                pii_nav,
                eyebrow="Interactive tool · Chapter 3",
                extra_head=_tool_extra_head(pii_asset_prefix, "pii-scrubber.css"),
                footer_scripts=_tool_footer_scripts(pii_asset_prefix, pii_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    deid_risk_dir = tools_root / "deid-risk"
    if deid_risk_dir.is_dir():
        deid_asset_prefix = _rel_asset_path(deid_risk_dir, lectures_root)
        deid_site_prefix = _rel_site_path(deid_risk_dir, lectures_root)
        deid_nav = (
            f'<a href="{deid_site_prefix}index.html">Home</a>'
            f'<a href="{deid_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">De-id risk</span>'
        )
        deid_body = """
<div id="deid-root"></div>
"""
        deid_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/kanon.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="deid-risk.js"></script>"""
        out_file = deid_risk_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "De-identification risk checker",
                deid_body,
                deid_asset_prefix,
                deid_nav,
                eyebrow="Interactive tool · Chapter 3",
                extra_head=_tool_extra_head(deid_asset_prefix, "deid-risk.css"),
                footer_scripts=_tool_footer_scripts(deid_asset_prefix, deid_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    ethical_decision_dir = tools_root / "ethical-decision"
    if ethical_decision_dir.is_dir():
        eth_asset_prefix = _rel_asset_path(ethical_decision_dir, lectures_root)
        eth_site_prefix = _rel_site_path(ethical_decision_dir, lectures_root)
        eth_nav = (
            f'<a href="{eth_site_prefix}index.html">Home</a>'
            f'<a href="{eth_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Ethical decision</span>'
        )
        eth_body = """
<div id="eth-root"></div>
"""
        eth_footer = """
  <script src="data/scenarios-bundle.js"></script>
  <script src="lib/tree.js"></script>
  <script src="lib/export.js"></script>
  <script src="ethical-decision.js"></script>"""
        out_file = ethical_decision_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Ethical decision tree",
                eth_body,
                eth_asset_prefix,
                eth_nav,
                eyebrow="Interactive tool · Chapter 3",
                extra_head=_tool_extra_head(eth_asset_prefix, "ethical-decision.css"),
                footer_scripts=_tool_footer_scripts(eth_asset_prefix, eth_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    fairness_dir = tools_root / "fairness"
    if fairness_dir.is_dir():
        fairness_asset_prefix = _rel_asset_path(fairness_dir, lectures_root)
        fairness_site_prefix = _rel_site_path(fairness_dir, lectures_root)
        fairness_nav = (
            f'<a href="{fairness_site_prefix}index.html">Home</a>'
            f'<a href="{fairness_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Fairness</span>'
        )
        fairness_body = """
<div id="fairness-root"></div>
"""
        fairness_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/metrics.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="fairness.js"></script>"""
        out_file = fairness_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Bias & fairness meter",
                fairness_body,
                fairness_asset_prefix,
                fairness_nav,
                eyebrow="Interactive tool · Chapter 7",
                extra_head=_tool_extra_head(fairness_asset_prefix, 'fairness.css'),
                footer_scripts=_tool_footer_scripts(fairness_asset_prefix, fairness_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    datasheet_dir = tools_root / "datasheet"
    if datasheet_dir.is_dir():
        datasheet_asset_prefix = _rel_asset_path(datasheet_dir, lectures_root)
        datasheet_site_prefix = _rel_site_path(datasheet_dir, lectures_root)
        datasheet_nav = (
            f'<a href="{datasheet_site_prefix}index.html">Home</a>'
            f'<a href="{datasheet_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Datasheet</span>'
        )
        datasheet_body = """
<div id="datasheet-root"></div>
"""
        datasheet_footer = f"""
  <script src="{datasheet_asset_prefix}/licenses-bundle.js"></script>
  <script src="{datasheet_asset_prefix}/licenses.js"></script>
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/profile.js"></script>
  <script src="lib/templates.js"></script>
  <script src="lib/export.js"></script>
  <script src="datasheet.js"></script>"""
        out_file = datasheet_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Datasheet / data-card builder",
                datasheet_body,
                datasheet_asset_prefix,
                datasheet_nav,
                eyebrow="Interactive tool · Chapter 8",
                extra_head=_tool_extra_head(datasheet_asset_prefix, 'datasheet.css'),
                footer_scripts=_tool_footer_scripts(datasheet_asset_prefix, datasheet_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    license_chooser_dir = tools_root / "license-chooser"
    if license_chooser_dir.is_dir():
        lc_asset_prefix = _rel_asset_path(license_chooser_dir, lectures_root)
        lc_site_prefix = _rel_site_path(license_chooser_dir, lectures_root)
        lc_nav = (
            f'<a href="{lc_site_prefix}index.html">Home</a>'
            f'<a href="{lc_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">License chooser</span>'
        )
        lc_body = """
<div id="license-chooser-root"></div>
"""
        lc_footer = f"""
  <script src="{lc_asset_prefix}/licenses-bundle.js"></script>
  <script src="{lc_asset_prefix}/licenses.js"></script>
  <script src="lib/recommend.js"></script>
  <script src="license-chooser.js"></script>"""
        out_file = license_chooser_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "License chooser",
                lc_body,
                lc_asset_prefix,
                lc_nav,
                eyebrow="Interactive tool · Chapter 13",
                extra_head=_tool_extra_head(lc_asset_prefix, "license-chooser.css"),
                footer_scripts=_tool_footer_scripts(lc_asset_prefix, lc_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    metadata_checker_dir = tools_root / "metadata-checker"
    if metadata_checker_dir.is_dir():
        mc_asset_prefix = _rel_asset_path(metadata_checker_dir, lectures_root)
        mc_site_prefix = _rel_site_path(metadata_checker_dir, lectures_root)
        mc_nav = (
            f'<a href="{mc_site_prefix}index.html">Home</a>'
            f'<a href="{mc_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Metadata checker</span>'
        )
        mc_body = """
<div id="metadata-checker-root"></div>
"""
        mc_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/checklist.js"></script>
  <script src="lib/score.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/export.js"></script>
  <script src="metadata-checker.js"></script>"""
        out_file = metadata_checker_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Metadata completeness checker",
                mc_body,
                mc_asset_prefix,
                mc_nav,
                eyebrow="Interactive tool · Chapter 8",
                extra_head=_tool_extra_head(mc_asset_prefix, 'metadata-checker.css'),
                footer_scripts=_tool_footer_scripts(mc_asset_prefix, mc_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    version_timeline_dir = tools_root / "version-timeline"
    if version_timeline_dir.is_dir():
        vt_asset_prefix = _rel_asset_path(version_timeline_dir, lectures_root)
        vt_site_prefix = _rel_site_path(version_timeline_dir, lectures_root)
        vt_nav = (
            f'<a href="{vt_site_prefix}index.html">Home</a>'
            f'<a href="{vt_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Version timeline</span>'
        )
        vt_body = """
<div id="version-timeline-root"></div>
"""
        vt_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/diff.js"></script>
  <script src="lib/export.js"></script>
  <script src="version-timeline.js"></script>"""
        out_file = version_timeline_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Version timeline",
                vt_body,
                vt_asset_prefix,
                vt_nav,
                eyebrow="Interactive tool · Chapter 8",
                extra_head=_tool_extra_head(vt_asset_prefix, 'version-timeline.css'),
                footer_scripts=_tool_footer_scripts(vt_asset_prefix, vt_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    representation_dir = tools_root / "representation"
    if representation_dir.is_dir():
        rp_asset_prefix = _rel_asset_path(representation_dir, lectures_root)
        rp_site_prefix = _rel_site_path(representation_dir, lectures_root)
        rp_nav = (
            f'<a href="{rp_site_prefix}index.html">Home</a>'
            f'<a href="{rp_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Representation</span>'
        )
        rp_body = """
<div id="representation-root"></div>
"""
        rp_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/distribution.js"></script>
  <script src="lib/performance.js"></script>
  <script src="lib/charts.js"></script>
  <script src="lib/export.js"></script>
  <script src="representation.js"></script>"""
        out_file = representation_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Representation bias visualizer",
                rp_body,
                rp_asset_prefix,
                rp_nav,
                eyebrow="Interactive tool · Chapter 7",
                extra_head=_tool_extra_head(rp_asset_prefix, 'representation.css'),
                footer_scripts=_tool_footer_scripts(rp_asset_prefix, rp_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    iaa_dir = tools_root / "iaa"
    if iaa_dir.is_dir():
        iaa_asset_prefix = _rel_asset_path(iaa_dir, lectures_root)
        iaa_site_prefix = _rel_site_path(iaa_dir, lectures_root)
        iaa_nav = (
            f'<a href="{iaa_site_prefix}index.html">Home</a>'
            f'<a href="{iaa_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">IAA</span>'
        )
        iaa_body = """
<div id="iaa-root"></div>
"""
        iaa_footer = """
  <script src="data/presets-bundle.js"></script>
  <script src="lib/parse.js"></script>
  <script src="lib/kappa.js"></script>
  <script src="lib/match.js"></script>
  <script src="lib/export.js"></script>
  <script src="iaa.js"></script>"""
        out_file = iaa_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "IAA calculator",
                iaa_body,
                iaa_asset_prefix,
                iaa_nav,
                eyebrow="Interactive tool · Chapter 4",
                extra_head=_tool_extra_head(iaa_asset_prefix, 'iaa.css'),
                footer_scripts=_tool_footer_scripts(iaa_asset_prefix, iaa_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    storage_format_dir = tools_root / "storage-format"
    if storage_format_dir.is_dir():
        sf_asset_prefix = _rel_asset_path(storage_format_dir, lectures_root)
        sf_site_prefix = _rel_site_path(storage_format_dir, lectures_root)
        sf_nav = (
            f'<a href="{sf_site_prefix}index.html">Home</a>'
            f'<a href="{sf_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Storage &amp; format</span>'
        )
        sf_body = """
<div id="storage-format-root"></div>
"""
        sf_footer = """
  <script src="lib/core.js"></script>
  <script src="storage-format.js"></script>"""
        out_file = storage_format_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Storage & format chooser",
                sf_body,
                sf_asset_prefix,
                sf_nav,
                eyebrow="Interactive tool · Chapter 12",
                extra_head=_tool_extra_head(sf_asset_prefix, "storage-format.css"),
                footer_scripts=_tool_footer_scripts(sf_asset_prefix, sf_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    text_augmentation_dir = tools_root / "text-augmentation"
    if text_augmentation_dir.is_dir():
        tau_asset_prefix = _rel_asset_path(text_augmentation_dir, lectures_root)
        tau_site_prefix = _rel_site_path(text_augmentation_dir, lectures_root)
        tau_nav = (
            f'<a href="{tau_site_prefix}index.html">Home</a>'
            f'<a href="{tau_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Text augmentation</span>'
        )
        tau_body = """
<div id="stx-root"></div>
"""
        tau_footer = """
  <script src="data/presets-bundle.js?v=20260718d"></script>
  <script src="lib/parse.js?v=20260718d"></script>
  <script src="lib/generate.js?v=20260718d"></script>
  <script src="lib/export.js?v=20260718d"></script>
  <script src="text-augmentation.js?v=20260718d"></script>"""
        out_file = text_augmentation_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Text augmentation lab",
                tau_body,
                tau_asset_prefix,
                tau_nav,
                eyebrow="Interactive tool · Chapter 10",
                extra_head=_tool_extra_head(tau_asset_prefix, "text-augmentation.css"),
                footer_scripts=_tool_footer_scripts(tau_asset_prefix, tau_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    # Legacy redirect from synthetic-text → text-augmentation
    legacy_synth_dir = tools_root / "synthetic-text"
    legacy_synth_dir.mkdir(parents=True, exist_ok=True)
    legacy_synth_out = legacy_synth_dir / "index.html"
    legacy_synth_out.write_text(
        """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=../text-augmentation/index.html">
  <title>Redirecting…</title>
  <link rel="canonical" href="../text-augmentation/index.html">
</head>
<body>
  <p>This tool was renamed. <a href="../text-augmentation/index.html">Open Text augmentation lab</a>.</p>
</body>
</html>
""",
        encoding="utf-8",
    )
    written.append(legacy_synth_out)

    image_augmentation_dir = tools_root / "image-augmentation"
    if image_augmentation_dir.is_dir():
        ima_asset_prefix = _rel_asset_path(image_augmentation_dir, lectures_root)
        ima_site_prefix = _rel_site_path(image_augmentation_dir, lectures_root)
        ima_nav = (
            f'<a href="{ima_site_prefix}index.html">Home</a>'
            f'<a href="{ima_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Image augmentation</span>'
        )
        ima_body = """
<div id="ima-root"></div>
"""
        ima_footer = """
  <script src="data/images-bundle.js?v=20260718e"></script>
  <script src="data/presets-bundle.js?v=20260718e"></script>
  <script src="lib/transforms.js?v=20260718e"></script>
  <script src="lib/export.js?v=20260718e"></script>
  <script src="image-augmentation.js?v=20260718e"></script>"""
        out_file = image_augmentation_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Image augmentation lab",
                ima_body,
                ima_asset_prefix,
                ima_nav,
                eyebrow="Interactive tool · Chapter 10",
                extra_head=_tool_extra_head(ima_asset_prefix, "image-augmentation.css"),
                footer_scripts=_tool_footer_scripts(ima_asset_prefix, ima_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    media_augmentation_dir = tools_root / "media-augmentation"
    if media_augmentation_dir.is_dir():
        med_asset_prefix = _rel_asset_path(media_augmentation_dir, lectures_root)
        med_site_prefix = _rel_site_path(media_augmentation_dir, lectures_root)
        med_nav = (
            f'<a href="{med_site_prefix}index.html">Home</a>'
            f'<a href="{med_site_prefix}tools/index.html">Tools</a>'
            '<span class="here">Media augmentation</span>'
        )
        med_body = """
<div id="media-root"></div>
"""
        med_footer = """
  <script src="lib/audio.js?v=20260718k"></script>
  <script src="lib/video.js?v=20260718k"></script>
  <script src="lib/analyze-audio.js?v=20260718k"></script>
  <script src="lib/analyze-video.js?v=20260718k"></script>
  <script src="lib/playback.js?v=20260718k"></script>
  <script src="lib/export.js?v=20260718k"></script>
  <script src="media-augmentation.js?v=20260718k"></script>"""
        out_file = media_augmentation_dir / "index.html"
        out_file.write_text(
            _tool_shell(
                "Media augmentation lab",
                med_body,
                med_asset_prefix,
                med_nav,
                eyebrow="Interactive tool · Chapter 10",
                extra_head=_tool_extra_head(med_asset_prefix, "media-augmentation.css"),
                footer_scripts=_tool_footer_scripts(med_asset_prefix, med_footer),
            ),
            encoding="utf-8",
        )
        written.append(out_file)

    # Hub cards ordered by dataset workflow (collect → privacy → augment →
    # annotate → explore → clean → split → fairness → document → license).
    def _tool_card(href: str, title: str, meta: str) -> str:
        return (
            "<li>"
            f'<a href="{href}">{title}</a>'
            f'<div class="chapter-meta">{meta}</div>'
            "</li>"
        )

    stages: list[tuple[str, str]] = []

    collect_cards = ""
    if sampling_dir.is_dir():
        collect_cards += _tool_card(
            "sampling/index.html",
            "Sampling tool",
            "SRS, stratified, cluster, systematic, convenience, snowball · Chapter 2",
        )
    if collect_cards:
        stages.append(("1 · Collect", collect_cards))

    privacy_cards = ""
    if pii_scrubber_dir.is_dir():
        privacy_cards += _tool_card(
            "pii-scrubber/index.html",
            "Consent &amp; PII scrubber",
            "Purpose / consent gate · minimize · detect · mask / tokenize / suppress · scrub log · Chapter 3",
        )
    if deid_risk_dir.is_dir():
        privacy_cards += _tool_card(
            "deid-risk/index.html",
            "De-identification risk checker",
            "k-anonymity · quasi-identifiers · ZIP/age generalization · risk report · Chapter 3",
        )
    if ethical_decision_dir.is_dir():
        privacy_cards += _tool_card(
            "ethical-decision/index.html",
            "Ethical decision tree",
            "Consent / purpose / harm walkthrough · proceed · revise · stop · Chapter 3",
        )
    if privacy_cards:
        stages.append(("2 · Privacy before share", privacy_cards))

    augment_cards = ""
    if text_augmentation_dir.is_dir():
        augment_cards += _tool_card(
            "text-augmentation/index.html",
            "Text augmentation lab",
            "Templates, EDA, noise, mixup, Markov · recipe export · Chapter 10",
        )
    if image_augmentation_dir.is_dir():
        augment_cards += _tool_card(
            "image-augmentation/index.html",
            "Image augmentation lab",
            "Flip, crop, jitter, noise · before/after grid · ZIP + recipe · Chapter 10",
        )
    if media_augmentation_dir.is_dir():
        augment_cards += _tool_card(
            "media-augmentation/index.html",
            "Media augmentation lab",
            "Audio + video · WebM clips (Chromium) · analytics · ZIP · Chapter 10",
        )
    if augment_cards:
        stages.append(("3 · Augment", augment_cards))

    annotate_cards = ""
    if image_annotation_dir.is_dir():
        annotate_cards += _tool_card(
            "image-annotation/index.html",
            "Image annotation",
            "Upload images, draw boxes, custom classes, download annotated dataset · Chapter 4",
        )
    if text_annotation_dir.is_dir():
        annotate_cards += _tool_card(
            "text-annotation/index.html",
            "Text annotation",
            "Sentiment labels and NER spans on short texts · export JSON/CSV · Chapter 4",
        )
    if iaa_dir.is_dir():
        annotate_cards += _tool_card(
            "iaa/index.html",
            "IAA calculator",
            "Category κ · span/box IoU F1 · text, audio, video, image presets · Chapter 4",
        )
    if annotate_cards:
        stages.append(("4 · Annotate &amp; agree", annotate_cards))

    prepare_cards = ""
    if schema_format_dir.is_dir():
        prepare_cards += _tool_card(
            "schema-format/index.html",
            "Schema / format translator",
            "CSV ↔ JSON ↔ inferred schema · nested vs flat · Chapter 1",
        )
    if eda_dashboard_dir.is_dir():
        prepare_cards += _tool_card(
            "eda-dashboard/index.html",
            "EDA dashboard",
            "Schema, missingness, group-by, scatter, Pearson · findings · handoff to cleaning · Chapters 1 &amp; 6",
        )
    if cleaning_dir.is_dir():
        prepare_cards += _tool_card(
            "cleaning/index.html",
            "Cleaning workbench",
            "Missing values, duplicates, inconsistent categories, outliers · cleaned CSV + change log · Chapter 5",
        )
    if scaling_encoding_dir.is_dir():
        prepare_cards += _tool_card(
            "scaling-encoding/index.html",
            "Scaling / encoding lab",
            "Min–max, z-score, log · one-hot / label / target · histograms + scatter · Chapter 5",
        )
    if class_imbalance_dir.is_dir():
        prepare_cards += _tool_card(
            "class-imbalance/index.html",
            "Class imbalance explorer",
            "Accuracy trap · oversample / undersample / class weights · holdout metrics · Chapter 5",
        )
    if train_test_split_dir.is_dir():
        prepare_cards += _tool_card(
            "train-test-split/index.html",
            "Train / val / test splitter",
            "Random, stratified, time-based splits · ID &amp; temporal leakage checks · Chapter 1",
        )
    if prepare_cards:
        stages.append(("5 · Explore, clean, scale &amp; split", prepare_cards))

    fairness_cards = ""
    if representation_dir.is_dir():
        fairness_cards += _tool_card(
            "representation/index.html",
            "Representation bias visualizer",
            "Population vs dataset bars · representation gaps · optional per-group accuracy · Chapter 7",
        )
    if fairness_dir.is_dir():
        fairness_cards += _tool_card(
            "fairness/index.html",
            "Bias &amp; fairness meter",
            "Demographic parity, 80% rule, EO, equalized odds · trade-off curve · per-group thresholds · Chapter 7",
        )
    if fairness_cards:
        stages.append(("6 · Check bias &amp; fairness", fairness_cards))

    docs_cards = ""
    if datasheet_dir.is_dir():
        docs_cards += _tool_card(
            "datasheet/index.html",
            "Datasheet / data-card builder",
            "Guided documentation · sample-data profile · data dictionary · export MD + JSON metadata · Chapter 8",
        )
    if metadata_checker_dir.is_dir():
        docs_cards += _tool_card(
            "metadata-checker/index.html",
            "Metadata completeness checker",
            "Score dataset cards against §8.2 checklist · remediation hints · import datasheet-metadata.json · Chapter 8",
        )
    if version_timeline_dir.is_dir():
        docs_cards += _tool_card(
            "version-timeline/index.html",
            "Version timeline",
            "Step v1 → v2 → v3 · schema and label drift · export version manifest · Chapter 8",
        )
    if docs_cards:
        stages.append(("7 · Document &amp; version", docs_cards))

    scale_cards = ""
    if storage_format_dir.is_dir():
        scale_cards += _tool_card(
            "storage-format/index.html",
            "Storage &amp; format chooser",
            "Workload → object/block + Avro/Parquet/ORC stack · toy scan demo · Chapter 12",
        )
    if scale_cards:
        stages.append(("8 · Scale &amp; store", scale_cards))

    open_cards = ""
    if license_chooser_dir.is_dir():
        open_cards += _tool_card(
            "license-chooser/index.html",
            "License chooser",
            "Use-case questionnaire → CC / ODC / software / restricted · export recommendation + LICENSE · Chapter 13",
        )
    if open_cards:
        stages.append(("9 · Share &amp; license", open_cards))

    stages_html = ""
    for title, cards in stages:
        stages_html += (
            '<section class="tools-stage">'
            f"<h2>{title}</h2>"
            f'<ul class="chapter-list">{cards}</ul>'
            "</section>"
        )

    hub_body = f"""
<section class="hero">
  <h1>Interactive tools</h1>
  <p class="lead">Browser-based labs along the dataset workflow: collect → privacy → augment → annotate → explore/clean/scale/split → check fairness → document &amp; version → scale &amp; store → license. No install required.</p>
  <div class="deck-links">
    <a class="btn btn-secondary" href="{site_prefix}community/feedback/index.html?type=tool">Suggest a tool improvement</a>
  </div>
</section>
{stages_html}
"""
    hub_file = tools_root / "index.html"
    hub_file.write_text(
        _tool_shell(
            "Interactive tools",
            hub_body,
            asset_prefix,
            nav,
            eyebrow="Tools",
        ),
        encoding="utf-8",
    )
    written.append(hub_file)
    return written


def _project_step(
    num: int,
    title: str,
    blurb: str,
    links: list[tuple[str, str]],
    *,
    optional: bool = False,
    export_hint: str = "",
) -> str:
    """One step on the raw → ready project path."""
    opt = ' <span class="pill pill-muted">Optional</span>' if optional else ""
    link_html = "".join(
        f'<a class="btn btn-secondary" href="{_esc(href)}">{_esc(label)}</a>'
        for href, label in links
    )
    export = (
        f'<p class="project-export"><strong>Take with you:</strong> {_esc(export_hint)}</p>'
        if export_hint
        else ""
    )
    return f"""
<article class="project-step" id="step-{num}">
  <div class="project-step-head">
    <span class="project-step-num" aria-hidden="true">{num}</span>
    <h3>{_esc(title)}{opt}</h3>
  </div>
  <p>{_esc(blurb)}</p>
  <div class="deck-links">{link_html}</div>
  {export}
</article>
"""


def build_project_pages(lectures_root: Path) -> list[Path]:
    """Build the guided raw → ready project path."""
    project_dir = lectures_root / "project"
    project_dir.mkdir(parents=True, exist_ok=True)
    asset_prefix = _rel_asset_path(project_dir, lectures_root)
    site_prefix = _rel_site_path(project_dir, lectures_root)
    tools = f"{site_prefix}tools"

    nav = (
        f'<a href="{site_prefix}index.html">Home</a>'
        '<span class="here">Project</span>'
    )

    steps = "".join(
        [
            _project_step(
                1,
                "Ingest and explore",
                "Load a CSV or JSON sample, check the schema, and profile the data before you change anything.",
                [
                    (f"{tools}/schema-format/index.html", "Schema / format translator"),
                    (f"{tools}/eda-dashboard/index.html", "EDA dashboard"),
                ],
                export_hint="Findings notes; handoff into cleaning when ready.",
            ),
            _project_step(
                2,
                "Protect before you share",
                "Confirm purpose and consent, scrub direct identifiers, and check re-identification risk on quasi-identifiers.",
                [
                    (f"{tools}/ethical-decision/index.html", "Ethical decision tree"),
                    (f"{tools}/pii-scrubber/index.html", "Consent & PII scrubber"),
                    (f"{tools}/deid-risk/index.html", "De-identification risk checker"),
                ],
                export_hint="Scrub log and risk report alongside the minimized table.",
            ),
            _project_step(
                3,
                "Clean, encode, and split",
                "Fix missing values and duplicates, scale or encode features, then create train / val / test splits without leakage.",
                [
                    (f"{tools}/cleaning/index.html", "Cleaning workbench"),
                    (f"{tools}/scaling-encoding/index.html", "Scaling / encoding lab"),
                    (f"{tools}/class-imbalance/index.html", "Class imbalance explorer"),
                    (f"{tools}/train-test-split/index.html", "Train / val / test splitter"),
                ],
                export_hint="Cleaned CSV, transform report, and split manifests.",
            ),
            _project_step(
                4,
                "Annotate and agree",
                "If your release needs labels, annotate images or text and measure agreement before you freeze a gold set.",
                [
                    (f"{tools}/image-annotation/index.html", "Image annotation"),
                    (f"{tools}/text-annotation/index.html", "Text annotation"),
                    (f"{tools}/iaa/index.html", "IAA calculator"),
                ],
                optional=True,
                export_hint="Annotated ZIP/JSON/CSV and an IAA summary.",
            ),
            _project_step(
                5,
                "Check representation and fairness",
                "Compare who is in the data to who should be, and inspect simple group metrics before publication.",
                [
                    (f"{tools}/representation/index.html", "Representation bias visualizer"),
                    (f"{tools}/fairness/index.html", "Bias & fairness meter"),
                ],
                export_hint="Gap charts and fairness report exports.",
            ),
            _project_step(
                6,
                "Document and version",
                "Write a datasheet, score metadata completeness, and record how this release differs from the last one.",
                [
                    (f"{tools}/datasheet/index.html", "Datasheet / data-card builder"),
                    (f"{tools}/metadata-checker/index.html", "Metadata completeness checker"),
                    (f"{tools}/version-timeline/index.html", "Version timeline"),
                ],
                export_hint="Datasheet (MD/JSON), scorecard, and version manifest.",
            ),
            _project_step(
                7,
                "Choose format and license",
                "Pick a storage stack that fits the workload, then choose a license that matches how others may reuse the data.",
                [
                    (f"{tools}/storage-format/index.html", "Storage & format chooser"),
                    (f"{tools}/license-chooser/index.html", "License chooser"),
                ],
                export_hint="Stack recommendation and a LICENSE text file.",
            ),
        ]
    )

    body = f"""
<section class="hero">
  <h1>Raw → ready</h1>
  <p class="lead">A guided path from your raw sample to a documented, licensed release kit.
  Work stays in the browser — nothing is uploaded to our servers. Host the finished files
  on Zenodo, Hugging Face, GitHub, or your institution when you are ready to publish.</p>
  <div class="deck-links">
    <a class="btn" href="#step-1">Start with ingest</a>
    <a class="btn btn-secondary" href="{tools}/index.html">Browse all tools</a>
  </div>
</section>

<div class="panel project-note" role="note">
  <strong>How this works.</strong> Use a small CSV, JSON, or image sample first.
  Each tool can export files you carry to the next step (some tools also hand off via
  <code>sessionStorage</code> in the same browser tab). Augmentation labs are optional
  and not required for a public release.
</div>

<section class="project-path" aria-label="Project steps">
  <h2>Path</h2>
  {steps}
</section>

<section class="project-kit" id="release-kit">
  <h2>Your release kit</h2>
  <p class="lead">Before you publish elsewhere, check that you can download:</p>
  <ul class="project-checklist">
    <li>Final data files (cleaned table, splits, and labels if any)</li>
    <li>Datasheet or data card (Markdown / JSON)</li>
    <li>Metadata scorecard and version note</li>
    <li>LICENSE (or a clear reuse statement)</li>
    <li>Short README pointing to purpose, contact, and known limitations</li>
  </ul>
  <p class="lead">This site does not host your dataset for the public. It prepares the package;
  you choose where it lives.</p>
  <div class="deck-links">
    <a class="btn btn-secondary" href="{site_prefix}community/feedback/index.html?type=tool">Suggest a path improvement</a>
  </div>
</section>
"""
    out_file = project_dir / "index.html"
    out_file.write_text(
        _page_shell(
            "Project — Raw to ready",
            body,
            asset_prefix,
            nav,
            eyebrow="Project",
            section="project",
        ),
        encoding="utf-8",
    )
    return [out_file]


def build_home(lectures_root: Path) -> Path:
    """Build lectures/index.html platform home."""
    chapters: list[tuple[int, str, str, int]] = []
    for ch_dir in sorted(lectures_root.glob("chapter*")):
        if not ch_dir.is_dir():
            continue
        meta_path = ch_dir / "chapter.json"
        if not meta_path.is_file():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        n_clips = len(meta.get("parts", []))
        chapters.append((int(meta["chapter"]), meta["title"], ch_dir.name, n_clips))

    chapters.sort(key=lambda x: x[0])
    asset_prefix = "assets"

    items = ""
    for num, title, slug, n_clips in chapters:
        items += (
            f"<li>"
            f'<a href="{slug}/index.html">{_esc(title)}</a>'
            f'<div class="chapter-meta">{n_clips} short {UNIT_LABEL_LOWER}s · guided path + quizzes</div>'
            f"</li>"
        )

    body = f"""
<section class="hero">
  <h1>Learn, practice, and share datasets</h1>
  <p class="lead">Open companion platform for <em>{_esc(BOOK_TITLE)}</em>.
  Short lectures, browser tools, a raw-to-ready project path, packaged examples,
  and a reader community — all in one place.</p>
</section>

<section class="home-pillars" aria-label="Explore the platform">
  <ul class="pillar-grid">
    <li>
      <a class="pillar-card" href="#lectures">
        <h2>Lectures</h2>
        <p>Guided chapter paths with short videos, bridges, quizzes, and downloadable decks.</p>
      </a>
    </li>
    <li>
      <a class="pillar-card" href="tools/index.html">
        <h2>Tools</h2>
        <p>In-browser labs along the dataset workflow — upload, transform, document, and export.</p>
      </a>
    </li>
    <li>
      <a class="pillar-card" href="project/index.html">
        <h2>Project</h2>
        <p>Turn raw data into a documented, licensed release kit — step by step in the browser.</p>
      </a>
    </li>
    <li>
      <a class="pillar-card" href="modules/index.html">
        <h2>Examples</h2>
        <p>Packaged chapter examples with notes, data files, and expected results.</p>
      </a>
    </li>
    <li>
      <a class="pillar-card" href="community/index.html">
        <h2>Community</h2>
        <p>Reader stories and feedback for the authors and the tool set.</p>
      </a>
    </li>
  </ul>
</section>

<section id="lectures" class="home-lectures">
  <h2>Lectures</h2>
  <p class="lead">Each chapter is a guided path: short videos, bridge text between {UNIT_LABEL_LOWER}s,
  a quiz after each {UNIT_LABEL_LOWER}, and a downloadable full deck.</p>
  <ul class="chapter-list">{items}</ul>
</section>
"""
    out_file = lectures_root / "index.html"
    out_file.write_text(
        _page_shell(
            "Home",
            body,
            asset_prefix,
            "",
            eyebrow="Open learning platform",
            section="lectures",
        ),
        encoding="utf-8",
    )
    return out_file


def build_site(lectures_root: Path, chapter: int | None = None) -> list[Path]:
    """Build full site or one chapter. Returns list of written index.html paths."""
    lectures_root = lectures_root.resolve()
    if not lectures_root.is_dir():
        raise FileNotFoundError(f"lectures root not found: {lectures_root}")

    _load_site_config(lectures_root)
    _copy_assets(lectures_root)
    written: list[Path] = []

    if chapter is not None:
        ch_dir = lectures_root / f"chapter{chapter}"
        if not ch_dir.is_dir():
            raise FileNotFoundError(f"chapter folder not found: {ch_dir}")
        written.append(build_chapter_page(ch_dir, lectures_root))
    else:
        for ch_dir in sorted(
            lectures_root.glob("chapter*"),
            key=_chapter_sort_key,
        ):
            if (ch_dir / "chapter.json").is_file():
                written.append(build_chapter_page(ch_dir, lectures_root))

    written.extend(build_modules_pages(lectures_root, chapter))
    written.extend(build_tools_pages(lectures_root))
    written.extend(build_project_pages(lectures_root))
    written.extend(build_community_pages(lectures_root))
    written.append(build_home(lectures_root))
    return written


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "lectures_root",
        type=Path,
        nargs="?",
        default=Path("lectures"),
        help="Path to lectures/ (default: lectures)",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Build only this chapter (still refreshes home + assets)",
    )
    parser.add_argument(
        "--community-only",
        action="store_true",
        help="Rebuild only lectures/community/ pages (for testimonial PRs)",
    )
    args = parser.parse_args(argv)
    try:
        if args.community_only:
            if args.chapter is not None:
                raise SystemExit("--community-only cannot be combined with --chapter")
            paths = build_community_pages(args.lectures_root.resolve())
        else:
            paths = build_site(args.lectures_root, args.chapter)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1
    for path in paths:
        print(f"Wrote {path}")
    print(f"Site ready: open {args.lectures_root.resolve() / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
