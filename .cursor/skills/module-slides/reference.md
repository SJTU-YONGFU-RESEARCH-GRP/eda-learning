# Module Slides — Reference

Schemas and patterns for **module-slides** (per-module PPT/PDF/TTS/video under `courses/`).

**Runtime:** Unix or WSL only. Bash entry points source `_require_unix.sh` and refuse native Windows shells. Prefer `python3`.

## Agent checklist (must not skip)

When the user asks for module media or “build the course,” complete this chain in WSL:

| Phase | Required outputs |
|-------|------------------|
| Author | Natural **algorithm-specific** `transcript.md`; sync `outline.yaml` |
| Depth | Track A `common/` solvers + goldens; **`EXAMPLES.md` ## Pseudocode**; interactive browser challenges |
| Captures | Lab snapshot / walkthrough `assets/steps/` (≈5 frames/lab) / real-shell as applicable |
| Deck | `slides.pptx` + `slides.pdf` |
| Narrate | `audio/full.mp3` + `video.mp4` |
| Tools | **Interactive** labs under `platform/tools/` — Check scores learner state; Reveal golden is study-only; **HiDPI canvases** via `canvas-hires.js` (≈480px tall) |
| Docs | `MODULES.md` + **`WALKTHROUGHS.md`** for algorithm courses |
| Publish | `publish_course_platform.py` → catalog + `data-render="lab"` shells |

**Do not** stop after PPTX. **Do not** ship thin static lab HTML. Match **digital_learning** course page quality.

**Do not** ship demo labs whose challenges only pass after “Show golden / Show arrival / Trace path.”

**Do not** call a course ready with scaffold-only transcripts, missing pseudocode, or zero walkthrough frames when clustering-depth is expected — see SKILL.md Content depth parity.

**Do** keep course + module `README.md` aligned with public [learn_unix](https://github.com/universal-verification-methodology/learn_unix) (Step 1b + `verify_course_readme.py`).

Full workflow: [SKILL.md](SKILL.md) Steps 1–9 + Definition of done.

## README schema (learn_unix pattern)

Gold standard: https://github.com/universal-verification-methodology/learn_unix

| Artifact | Template | Verify |
|----------|----------|--------|
| `courses/<id>/README.md` | [`templates/course_README.md.example`](templates/course_README.md.example) | `verify_course_readme.py courses/<id>` |
| Lab / intro / wrap module README | `templates/module_README.*.md.example` | `verify_course_readme.py courses/<id> --modules` |

### Course README — required `##` headings (order)

`Table of contents` → `Contents` → `Browse or clone` → `Consume from the parent` → `Author: publish or update` → `Two learning tracks` → `Module landings` → `Browser labs` → `License`

Also required: H1 `# <course_id>`, CC BY 4.0 badge, `module-slides` in Author section, links to `docs/MODULES.md` and `docs/TWO_TRACKS.md`, at least one `module…/README.md` landing link.

### Module README — lab minimum

```markdown
# Module NN: Title

**Kind:** `lab` · Primary lab: `lab-id` · **Shipped**

[← prev](../module-prev/README.md) · [Course README](../README.md) · [next →](../module-next/README.md)

## Outcomes
…

## Two tracks (pick one or both)
### Track A — …
### Track B — Browser lab (online)
… local 127.0.0.1:8080/tools/<lab-id>/ … and live Pages URL when shipped …

## Media
| Artifact | Path |
| … transcript / outline / slides / video / quiz …

## Files
```

Intro/wrap use their templates (welcome + setup, or recap + next course). Prefer `# Module …: Title` over a bare topic H1.

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/<course_id> --modules
```

## Platform publish (after media)

When a course’s modules have media and tools are shipped, publish into `platform/` (catalog + course lab pages + local `course-media` symlink) — same role as digital_learning’s `platform/courses/`:

```bash
python3 platform/scripts/publish_course_platform.py learn_clustering
python3 -m http.server 8080 --directory platform
# → /courses/learn_clustering/
```

| Must be true after publish | Why |
|----------------------------|-----|
| `platform/courses/index.html` uses `data-render="path-map"` | Same courses-map ladder as digital_learning |
| Lab pages use `data-render="lab"` | `pages.js` fills progress, tool CTA, video, quiz |
| Catalog has `moduleId` for hierarchical folders | Media path resolves under `course-media/` |
| Catalog lists ladder courses (ready + planned stubs) | Path-map nodes render; unpublished show “Soon” |
| Tools listed in catalog `labs[]` | Open tool button works |
| No hand-written static `<video>` tags | Regenerating publish keeps quality |

Course bulk builders (e.g. `courses/learn_clustering/scripts/build_all_media.sh`) should call publish after narrate.

## Planning

| Rule | Default |
|------|---------|
| Unit | One `moduleNN-slug` → one clip |
| Duration | Target **3–8 min**; cap **~10 min** spoken |
| Estimate | `word_count / 140` ≈ minutes |
| Video | Per module `video.mp4` (beside `slides.pptx` / `slides.pdf`) |
| Quiz | Optional 3–5 items |

## Natural transcript checklist

Before TTS, the transcript should pass:

1. **Read aloud** — sounds like a teacher, not a README  
2. **No paths in prose** — no `http://`, no `courses/…`, no `` `cmd` `` spam  
3. **Slide headings only as anchors** — TTS skips `## Slide N`  
4. **Contractions, spoken English** — “you’ll open”, not “The user shall proceed to”  
5. **One job per slide** — concept / Track B / Track A / pitfall / your turn  
6. **Commands on slides** — speech points at them (“run the list command shown here”)

### Before → after (examples)

| Stub / robotic | Natural |
|----------------|---------|
| “Outcomes: After this module you can explain `path-abs-rel`.” | “By the end of this short clip, you’ll know when a path is absolute and when it’s relative — and why that matters after you change directories.” |
| “Open http://127.0.0.1:8080/tools/path-abs-rel/index.html” | “In the browser lab track, open the absolute-versus-relative paths lab from the tools page, and load the starter example.” |
| “cd module03-path-abs-rel/examples/paths” | “In the real terminal track, go into this module’s paths example folder and print the working directory.” |
| “Kind: lab · Primary lab: vfs-terminal · Shipped” | *(delete from speech — metadata is not narration)* |

## `outline.yaml` (PPTX machine source)

```yaml
title: "Module 03 — Absolute vs relative paths"
footer: "learn_unix — paths"
slides:
  - type: title
    title: "Absolute vs relative paths"
    subtitle: "Module 03 · learn_unix"
    notes: |
      Full spoken paragraph for slide 1…
  - type: bullets
    title: "Absolute paths"
    bullets:
      - "Start from the filesystem root"
      - "Do not depend on your current directory"
    notes: |
      Matching transcript body for this slide…
```

| `type` | Fields |
|--------|--------|
| `title` | `title`, optional `subtitle`, `notes` |
| `section` | `title` |
| `bullets` | `title`, `bullets` (max 6), `notes` |
| `image` | `title`, `image`, optional `caption`, `notes` |
| `two_column` | `title`, `left` bullets, `right` image |
| `code` | `title`, `code`, optional `source_file`, `notes` |

**Code slide budget:** at most **12 lines** per slide after wrap (constant `CODE_SLIDE_MAX_LINES` in `pptx_theme.py`). Longer listings auto-split to titled parts `(1/N)` `(2/N)` — never crop. Prefer dense pseudocode without a blank after every line; bash try-these may keep blanks before `#` comment groups only.

**Notes field** must match the transcript body for that slide (verify script enforces this).

## Transcript shape

```markdown
# Module 03 — Absolute vs relative paths

**Module id:** module03-path-abs-rel
**Lab:** path-abs-rel
**Tracks:** A · B

## Slide 1 — Absolute vs relative paths

Spoken opener…

## Slide 2 — Why paths break after cd

…
```

Metadata lines after the H1 are **not** spoken (skipped by TTS prep). Keep them for authors.

## `quiz.json` (optional)

```json
{
  "module": "module03-path-abs-rel",
  "title": "Paths check",
  "passing_score": 0.67,
  "items": [
    {
      "id": "q1",
      "type": "multiple_choice",
      "prompt": "A path that starts with / is…",
      "choices": ["relative", "absolute", "a glob", "a symlink"],
      "answer": 1,
      "explain": "Leading slash means from the filesystem root."
    }
  ]
}
```

Types: `multiple_choice` | `true_false` | `short_answer`. Keep items inside this module’s teaching — no trivia from later modules.

## Dual-track slide map (lab modules)

| Slide role | Content |
|------------|---------|
| Title | Module promise |
| Concept | One idea |
| Track B | **Orient** + full-slide **lab** snapshot |
| Track A | **Real-shell** frame (`assets/real-shell.png`) + try-these `code` slide |
| Pitfall | Common mistake |
| Close | Checklist / quiz nudge |

`intro` / `wrap`: title → tools map (optional snapshot) → next module.

### Track B vs Track A depth

- **B:** Lab UI snapshot + short orient. Then “explore the challenges.”
- **A:** Prefer **real terminal** frames (WSL/Linux) — matches later Icarus/Verilator/Make/Git work. Capture with `capture_real_shell.py`.
- **Commands:** Every try-these line needs a **purpose** in speech and a `#` comment (or prior bullets). Never show unexplained flags.

```bash
python3 .cursor/skills/module-slides/scripts/capture_real_shell.py \
  courses/learn_unix/module01-vfs-terminal \
  --example-subdir navigation
```

Track A try-these fence (TTS skips it; sync emits a `code` slide after the image):

~~~~bash
# pwd — print working directory
pwd

# ls -la — list all, long format
ls -la

# cd sample_repo — enter this folder
cd sample_repo
~~~~

## Lab UI snapshots

Capture the live lab page into `assets/` for Track B slides.

```bash
# Serve platform/ locally, then:
python3 .cursor/skills/module-slides/scripts/capture_lab_snapshot.py \
  courses/learn_unix/module03-path-abs-rel \
  --patch-outline
# → assets/lab-starter.png + image slide in outline.yaml
```

| Flag | Purpose |
|------|---------|
| `--lab ID` | Override README primary lab (`index` = tools catalog) |
| `--base URL` | Default `http://127.0.0.1:8080/tools`; or live Pages tools URL |
| `--name file.png` | Output under `assets/` (default `lab-starter.png`) |
| `--selector CSS` | Crop to element (e.g. `main`, `#path-root`) |
| `--full-page` | Tall full-page capture |
| `--patch-outline` | Insert/update `type: image` slide |

**Transcript embed (survives re-sync):** put the image in the Track B section body:

```markdown
## Slide 3 — Browser lab

![Browser lab starter](assets/lab-starter.png)

In the browser lab track, open this lab from the tools page and load the starter…
```

`transcript_to_outline.py` turns that into an `image` (or `two_column`) slide; image markdown is stripped from TTS notes.

Requires: `pip install playwright` + `playwright install chromium`.

## Algorithm walkthrough frames

For algorithm labs (e.g. `learn_clustering`), capture step-by-step teaching frames from `platform/tools/algorithm-walkthrough/`.

```bash
python3 -m http.server 8080 --directory platform

python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
  courses/learn_clustering/module02-07-fiduccia-mattheyses \
  --inject-transcript
# → assets/steps/*.png + assets/STEPS.md
# → transcript.md region <!-- algorithm-walkthrough --> … <!-- /algorithm-walkthrough -->
```

| Flag | Purpose |
|------|---------|
| `--algo ID` | Override lab→walkthrough mapping |
| `--inject-transcript` | Insert/replace walkthrough slides in `transcript.md` |
| `--skip-capture` | Re-inject from existing `assets/STEPS.md` only |
| `--base URL` | Default `http://127.0.0.1:8080/tools/algorithm-walkthrough` |

**Transcript embed (survives re-sync):**

```markdown
<!-- algorithm-walkthrough -->

## Slide 3 — Move 1: flip D (gain 3)

![Move 1: flip D](assets/steps/02-move-d.png)

Highest legal move sends D to the other side with gain 3…

<!-- /algorithm-walkthrough -->
```

`transcript_to_outline.py` treats `assets/steps/` images as **full-slide `image`** (same as lab/shell shots). Interactive viewer: `/tools/algorithm-walkthrough/?algo=<lab>&step=N`.

## Build commands

```bash
SKILL=.cursor/skills/module-slides/scripts
MOD=courses/learn_unix/module03-path-abs-rel

python3 $SKILL/capture_lab_snapshot.py "$MOD" --patch-outline   # after http.server
python3 $SKILL/transcript_to_outline.py "$MOD"
python3 $SKILL/build_pptx.py "$MOD"
python3 $SKILL/verify_clip.py "$MOD"
python3 $SKILL/verify_transcript_consistency.py "$MOD"
bash $SKILL/pptx_to_pdf.sh "$MOD/slides.pptx"   # or clip.pptx
bash $SKILL/narrate_clips.sh "$MOD"
```

## Footer / naming

`build_pptx.py` accepts folders named `moduleNN-slug` and writes **`slides.pptx`** with footer `course — slug words` when it can detect `courses/<course>/` in the path.

Also accepts legacy `part-*` / `clip-*` / `chapterN` folder names if those trees still exist in a repo.

## Course: learn_git (pass 2 notes)

**Path:** `courses/learn_git/module00-intro` … `module22-wrap` (23 clips).

| Module kind | Track B lab snapshot | Track A real-shell | Notes |
|-------------|---------------------|-------------------|-------|
| `lab` (01–20) | `assets/lab-starter.png` | `assets/_demo_mNN.sh` → `real-shell.png` | Dual-track slide map |
| `offline` (21) | — | `assets/_demo_mNN.sh` | Sandbox rehearsal; Track A only in clip |
| `wrap` (22) | `assets/tools-index.png` (`--lab index`) | — | No real-shell frame |
| `intro` (00) | tools index snapshot | — | Course welcome |

### Track A demo scripts (`assets/_demo_mNN.sh`)

- Run under WSL; strip CRLF first: `sed -i 's/\r$//' assets/_demo_mNN.sh`
- Use a demo identity so commits work in temp dirs:

```bash
GIT=(git -c user.email=demo@local -c user.name=Demo)
"${GIT[@]}" commit -m "message"
```

- Prefer `mktemp -d` practice repos over mutating `examples/` trees (many are command lists only).
- After `git init`, use `git branch -M main` when later modules assume `main`.
- **Capture:** `capture_real_shell.py … --bash-script assets/_demo_mNN.sh` (not `--session-script`).

### Remotes / submodules demos (15–18)

- Bare file remotes: after first push, set default branch on the bare repo:  
  `git -C "$BARE" symbolic-ref HEAD refs/heads/main`
- Local `file://` URLs and `git submodule add` need:  
  `git -c protocol.file.allow=always …`

### Host: Unix / WSL only

Do **not** run module-slides media from native Windows (PowerShell/cmd). Use WSL or Linux:

```bash
cd /mnt/d/proj/designs/eda_learning   # adjust
bash .cursor/skills/module-slides/scripts/narrate_clips.sh courses/<course>/moduleNN-slug
```

Strip CRLF on demo scripts before capture: `sed -i 's/\r$//' assets/_demo_mNN.sh`.

Install Playwright Chromium **inside** the same Unix/WSL environment used for captures — do not fall back to Windows Python for snapshots.

### Bulk verify (whole course)

```bash
SKILL=.cursor/skills/module-slides/scripts
for d in courses/learn_git/module*/; do
  python3 $SKILL/verify_clip.py "$d" || break
  python3 $SKILL/verify_transcript_consistency.py "$d" || break
done
```

### Spoken length (learn_git pass 2)

Target **~2–3 min** for early concept labs (00–13), **~2.5–3 min** for remotes/submodules (14–20), **~2–2.5 min** for offline/wrap (21–22). All clips stayed under the 10-minute cap.

## Course: learn_uvm2017 (pass 2 notes)

**Path:** `courses/learn_uvm2017/module00-intro` … `module23-wrap` (24 clips).

| Module kind | Track B lab snapshot | Track A real-shell | Notes |
|-------------|---------------------|-------------------|-------|
| `intro` (00) | tools index (`lab-tools-index.png`) | — | Course welcome |
| `lab` (01–21) | `assets/lab-starter.png` | `assets/_demo_mNN.sh` → `real-shell.png` | Dual-track; sketch under `examples/*-sketch/` |
| `offline` (22) | — | `assets/_demo_m22.sh` | Makefile rehearsal; Track A only |
| `wrap` (23) | `assets/tools-index.png` (`--lab index`) | — | Recap + next courses |

### Pass 2 checklist (done)

- Bulk `verify_clip.py` + `verify_transcript_consistency.py` on all 24 modules
- Harden `_demo_m*.sh` `grep | head` under `set -o pipefail` with `|| true`
- Strip CRLF before WSL capture: `sed -i 's/\r$//' assets/_demo_mNN.sh`
- Spoken length ~2.5–3.6 min (labs denser than git; all under 10-min cap)
- Prefer “UVM twenty seventeen” in speech; avoid spelling IEEE clause numbers aloud
- Course README Contents/media note updated once media ships

### Spoken length (learn_uvm2017 pass 2)

Target **~2.5–3.5 min** for labs 01–21, **~2.5–3 min** for intro/offline/wrap. Longest clips stayed ~3.6 min.

## Course: learn_pyuvm (pass 2 notes)

**Path:** `courses/learn_pyuvm/module00-intro` … `module11-wrap` (12 clips).

| Module kind | Track B lab snapshot | Track A real-shell | Notes |
|-------------|---------------------|-------------------|-------|
| `intro` (00) | `lab-tools-index.png` | — | Course welcome |
| `lab` (01–09) | `assets/lab-starter.png` | `assets/_demo_mNN.sh` → `real-shell.png` | Dual-track; sketches under `examples/*-sketch/` |
| `offline` (10) | — | `assets/_demo_m10.sh` | Legacy `learn_uvm_pyuvm` Makefile; Track A only |
| `wrap` (11) | `assets/tools-index.png` (`#pyuvm`) | — | Recap + next courses |

### Pass 2 checklist

- Bulk `verify_clip.py` + `verify_transcript_consistency.py` on all 12 modules
- Expand Track A speech (pwd / ls -la / sed / python3 or make) to name each command’s purpose
- Soften pitfalls cadence (vary openings; drop robotic “Do not… And remember…”)
- Course README / `docs/TWO_TRACKS.md`: Track B marked **shipped** (not “mostly planned”)
- Offline m10: harden PATH + cocotb 2.x Makefile (`VERILOG_SOURCES`); rewrite stale `.venv` shebangs if the tree moved
- Prefer “UVM twenty seventeen” / “cocotb to UVM roles” in speech; avoid raw URLs and “module 0X”

### Spoken length (learn_pyuvm pass 2)

Target **~2.8–3.5 min** for labs 01–09, **~2.5–3.5 min** for intro/offline/wrap. All clips under the 10-minute cap.
