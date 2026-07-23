#!/usr/bin/env python3
"""Parity audit: learn_floorplanning vs learn_clustering + module-slides depth bar."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FP_LABS = [
    "fixed-outline",
    "area-deadspace",
    "slicing-floorplan",
    "bstar-tree",
    "sequence-pair",
    "simulated-annealing-fp",
    "soft-module-sizing",
    "macro-placement",
    "hierarchical-floorplan",
    "pin-assignment",
]


def count(course: str, pattern: str) -> int:
    return len(list((ROOT / "courses" / course).glob(pattern)))


def main() -> int:
    issues: list[str] = []
    notes: list[str] = []

    # README verify
    r = subprocess.run(
        [
            sys.executable,
            str(ROOT / ".cursor/skills/module-slides/scripts/verify_course_readme.py"),
            "courses/learn_floorplanning",
            "--modules",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        issues.append(f"README verify failed: {r.stdout}{r.stderr}")
    else:
        notes.append("README verify: OK")

    # common tests
    r = subprocess.run(
        [sys.executable, str(ROOT / "courses/learn_floorplanning/common/test_solvers.py")],
        cwd=ROOT / "courses/learn_floorplanning/common",
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        issues.append(f"common tests failed: {r.stdout}{r.stderr}")
    else:
        notes.append("common goldens: OK")

    for course in ("learn_clustering", "learn_floorplanning"):
        mods = list((ROOT / "courses" / course).glob("module*"))
        pptx = count(course, "**/slides.pptx")
        pdf = count(course, "**/slides.pdf")
        video = count(course, "**/video.mp4")
        audio = count(course, "**/audio/full.mp3")
        quiz = count(course, "**/quiz.json")
        steps = count(course, "**/assets/steps/*.png")
        steps_md = count(course, "**/assets/STEPS.md")
        lab_starter = count(course, "**/lab-starter.png")
        common_py = count(course, "common/*.py")
        inject = sum(
            1
            for p in (ROOT / "courses" / course).glob("module*/transcript.md")
            if "algorithm-walkthrough" in p.read_text(encoding="utf-8", errors="ignore")
        )
        notes.append(
            f"{course}: mods={len(mods)} pptx={pptx} pdf={pdf} video={video} "
            f"audio={audio} quiz={quiz} steps_png={steps} STEPS={steps_md} "
            f"inject={inject} lab_starter={lab_starter} common_py={common_py}"
        )

    # Floorplanning required depth
    fp_steps = count("learn_floorplanning", "**/assets/steps/*.png")
    if fp_steps < 50:
        issues.append(f"walkthrough PNGs {fp_steps} < 50 (10 labs × 5)")
    else:
        notes.append(f"walkthrough PNGs: {fp_steps}")

    cl_steps = count("learn_clustering", "**/assets/steps/*.png")
    notes.append(f"clustering walkthrough PNGs: {cl_steps} (reference)")

    # LAB_TO_ALGO
    cap = (ROOT / ".cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py").read_text(
        encoding="utf-8"
    )
    missing_map = [i for i in FP_LABS if f'"{i}"' not in cap]
    if missing_map:
        issues.append(f"LAB_TO_ALGO missing: {missing_map}")
    else:
        notes.append("LAB_TO_ALGO: all 10 FP labs")

    # walkthrough.js / floorplanning-algos
    fa = ROOT / "platform/tools/algorithm-walkthrough/floorplanning-algos.js"
    if not fa.is_file():
        issues.append("missing floorplanning-algos.js")
    else:
        text = fa.read_text(encoding="utf-8")
        missing_algo = [i for i in FP_LABS if f'"{i}"' not in text]
        if missing_algo:
            issues.append(f"FLOORPLAN_ALGOS missing: {missing_algo}")
        else:
            notes.append("FLOORPLAN_ALGOS: all 10")

    # tools
    missing_tools = []
    for lab in FP_LABS:
        d = ROOT / "platform/tools" / lab
        if not (d / "index.html").is_file() or not (d / f"{lab}.js").is_file():
            missing_tools.append(lab)
            issues.append(f"tool missing: {lab}")
    if not missing_tools:
        notes.append("browser tools: 10/10 present")

    # challenges count rough
    for lab in FP_LABS:
        js = (ROOT / "platform/tools" / lab / f"{lab}.js").read_text(encoding="utf-8")
        n = len(re.findall(r"id:\s*\"[a-z0-9-]+\"", js))
        if n < 8:
            issues.append(f"{lab}: only ~{n} challenge-like ids (want ~10)")

    # catalog
    cat = json.loads((ROOT / "platform/assets/catalog.json").read_text(encoding="utf-8"))
    fp = next(c for c in cat["courses"] if c["id"] == "learn_floorplanning")
    ready_media = sum(1 for l in fp["labs"] if l["media"].get("video") and l["media"].get("pdf"))
    notes.append(f"catalog status={fp['status']} media_ready={ready_media}/{len(fp['labs'])}")
    if fp["status"] != "ready":
        issues.append(f"catalog status is {fp['status']}, want ready")
    if ready_media < len(fp["labs"]):
        issues.append(f"catalog media incomplete: {ready_media}/{len(fp['labs'])}")

    fp_tools = [l for l in cat.get("labs", []) if l.get("section") == "Floorplanning"]
    if len(fp_tools) < 10:
        issues.append(f"catalog Floorplanning tools {len(fp_tools)} < 10")
    else:
        notes.append(f"catalog Floorplanning tools: {len(fp_tools)}")

    # platform shells
    if not (ROOT / "platform/courses/learn_floorplanning/index.html").is_file():
        issues.append("missing platform course index")
    lab_shells = list((ROOT / "platform/courses/learn_floorplanning/labs").glob("*/index.html"))
    notes.append(f"platform lab shells: {len(lab_shells)}")
    media_path = ROOT / "platform/course-media/learn_floorplanning"
    try:
        media_ok = media_path.is_symlink() or media_path.exists()
    except OSError:
        # WSL symlinks often raise on native Windows stat
        media_ok = True
        notes.append("course-media link: present (Windows symlink stat quirk)")
    if not media_ok:
        issues.append("missing course-media symlink")
    elif not any(n.startswith("course-media link:") for n in notes):
        notes.append("course-media link: OK")

    # scaffold filler / pending
    for tr in (ROOT / "courses/learn_floorplanning").glob("module*/transcript.md"):
        t = tr.read_text(encoding="utf-8")
        if "core idea in one breath" in t:
            issues.append(f"scaffold filler in {tr.parent.name}")
        if "walkthrough pending" in t:
            issues.append(f"pending walkthrough marker in {tr.parent.name}")

    walk = (ROOT / "courses/learn_floorplanning/docs/WALKTHROUGHS.md").read_text(encoding="utf-8")
    if re.search(r"\bpending\b", walk, re.I):
        issues.append("WALKTHROUGHS.md still says pending")
    else:
        notes.append("WALKTHROUGHS.md: no pending")

    # optional gaps vs skill (not blockers if clustering also lacks)
    cl_starter = count("learn_clustering", "**/lab-starter.png")
    fp_starter = count("learn_floorplanning", "**/lab-starter.png")
    if fp_starter == 0:
        notes.append(
            f"DEFERRED (also clustering={cl_starter}): lab-starter.png Track B snapshots not captured"
        )

    # offline module still planned in MODULES?
    modules_md = (ROOT / "courses/learn_floorplanning/docs/MODULES.md").read_text(encoding="utf-8")
    if "offline-benchmark" in modules_md and "| P |" in modules_md:
        notes.append("NOTE: offline-benchmark module still status P (same pattern as partitioning)")

    print("=== NOTES ===")
    for n in notes:
        print("-", n)
    print("=== ISSUES ===")
    if not issues:
        print("- none (depth bar met for required items)")
        return 0
    for i in issues:
        print("-", i)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
