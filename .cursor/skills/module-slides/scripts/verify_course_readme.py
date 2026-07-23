#!/usr/bin/env python3
"""Verify course + module README.md match the learn_unix / module-slides pattern.

Usage (from monorepo root, Unix/WSL preferred):

  python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \\
    courses/learn_clustering

  python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \\
    courses/learn_unix --strict-github

Exit 0 = pass; 1 = missing required sections / patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

COURSE_REQUIRED_HEADINGS = [
    "Table of contents",
    "Contents",
    "Browse or clone",
    "Consume from the parent",
    "Author: publish or update",
    "Two learning tracks",
    "Module landings",
    "Browser labs",
    "License",
]

COURSE_REQUIRED_SNIPPETS = [
    (r"License:\s*CC\s*BY\s*4\.0", "CC BY 4.0 license badge"),
    (r"module-slides", "module-slides author workflow mention"),
    (r"docs/MODULES\.md", "link to docs/MODULES.md"),
    (r"docs/TWO_TRACKS\.md", "link to docs/TWO_TRACKS.md"),
]

MODULE_LAB_REQUIRED = [
    (r"\*\*Kind:\*\*\s*`lab`", "Kind: lab"),
    (r"Primary lab:", "Primary lab"),
    (r"## Outcomes", "Outcomes section"),
    (r"## Two tracks", "Two tracks section"),
    (r"### Track A", "Track A subsection"),
    (r"### Track B", "Track B subsection"),
    (r"## Media", "Media section"),
    (r"Course README", "nav link to course README"),
]

MODULE_INTRO_REQUIRED = [
    (r"\*\*Kind:\*\*\s*`intro`", "Kind: intro"),
    (r"## Media", "Media section"),
    (r"Course README", "nav link to course README"),
]

MODULE_WRAP_REQUIRED = [
    (r"\*\*Kind:\*\*\s*`wrap`", "Kind: wrap"),
    (r"## Media", "Media section"),
    (r"Course README", "nav link to course README"),
]


def _heading_present(text: str, title: str) -> bool:
    return bool(re.search(rf"^##\s+{re.escape(title)}\s*$", text, re.M))


def _check_patterns(text: str, patterns: list[tuple[str, str]]) -> list[str]:
    missing: list[str] = []
    for pat, label in patterns:
        if not re.search(pat, text, re.I | re.M):
            missing.append(label)
    return missing


def verify_course_readme(course_dir: Path, *, strict_github: bool) -> list[str]:
    readme = course_dir / "README.md"
    if not readme.is_file():
        return [f"missing {readme}"]

    text = readme.read_text(encoding="utf-8")
    course_id = course_dir.name
    issues: list[str] = []

    if not re.search(rf"^#\s+{re.escape(course_id)}\s*$", text, re.M):
        issues.append(f"H1 must be exactly `# {course_id}`")

    for h in COURSE_REQUIRED_HEADINGS:
        if not _heading_present(text, h):
            issues.append(f"missing ## {h}")

    for pat, label in COURSE_REQUIRED_SNIPPETS:
        if not re.search(pat, text, re.I | re.M):
            issues.append(f"missing {label}")

    if strict_github:
        if "img.shields.io/badge/GitHub-" not in text:
            issues.append("missing GitHub badge (strict)")
        if "Consume from the parent" in text and "submodule" not in text.lower():
            issues.append("Consume from the parent should mention submodule (strict)")

    # Module landings table should have at least one module link
    if not re.search(r"\]\(module[^)/]+/README\.md\)", text):
        issues.append("Module landings: no moduleNN…/README.md links")

    return [f"course README: {i}" for i in issues]


def _infer_kind(text: str) -> str | None:
    m = re.search(r"\*\*Kind:\*\*\s*`([^`]+)`", text)
    return m.group(1).strip() if m else None


def verify_module_readme(module_dir: Path) -> list[str]:
    readme = module_dir / "README.md"
    if not readme.is_file():
        return [f"{module_dir.name}: missing README.md"]

    text = readme.read_text(encoding="utf-8")
    kind = _infer_kind(text)
    issues: list[str] = []

    if not re.search(r"^#\s+Module\s+", text, re.M):
        # Allow either "Module NN: Title" or hierarchical "Module SS-AA: Title"
        issues.append("H1 should start with `# Module …:` (learn_unix style)")

    if kind == "lab":
        issues.extend(_check_patterns(text, MODULE_LAB_REQUIRED))
        if "127.0.0.1:8080/tools/" not in text and "Primary lab:" in text:
            # Soft: warn via issue only if Track B section exists without local URL
            if "### Track B" in text and "tools/" not in text:
                issues.append("Track B should link local and/or live tools URL")
    elif kind == "intro":
        issues.extend(_check_patterns(text, MODULE_INTRO_REQUIRED))
    elif kind == "wrap":
        issues.extend(_check_patterns(text, MODULE_WRAP_REQUIRED))
    elif kind == "offline":
        if not re.search(r"## Media", text):
            issues.append("Media section")
        if "Course README" not in text:
            issues.append("nav link to course README")
    elif kind is None:
        issues.append("missing **Kind:** `…` metadata line")
    else:
        # Unknown kind — still require Media + course nav
        if not re.search(r"## Media", text):
            issues.append("Media section")
        if "Course README" not in text:
            issues.append("nav link to course README")

    return [f"{module_dir.name}: {i}" for i in issues]


def iter_modules(course_dir: Path) -> list[Path]:
    mods = [
        p
        for p in sorted(course_dir.iterdir())
        if p.is_dir() and p.name.startswith("module")
    ]
    return mods


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "course_dir",
        type=Path,
        help="Path to courses/<course_id>",
    )
    ap.add_argument(
        "--modules",
        action="store_true",
        help="Also verify each module*/README.md",
    )
    ap.add_argument(
        "--strict-github",
        action="store_true",
        help="Require public-repo badge / submodule wording (learn_unix gold)",
    )
    args = ap.parse_args()
    course_dir = args.course_dir.resolve()
    if not course_dir.is_dir():
        print(f"Not a directory: {course_dir}", file=sys.stderr)
        return 1

    issues = verify_course_readme(course_dir, strict_github=args.strict_github)
    if args.modules:
        for mod in iter_modules(course_dir):
            issues.extend(verify_module_readme(mod))

    if issues:
        print(f"FAIL — {course_dir.name} README checks ({len(issues)}):")
        for i in issues:
            print(f"  - {i}")
        return 1

    scope = "course + modules" if args.modules else "course"
    print(f"OK — {course_dir.name} README ({scope})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
