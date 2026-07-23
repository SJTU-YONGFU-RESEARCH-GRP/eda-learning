---
name: module-slides
description: >-
  Builds per-module PPTX, PDF, natural TTS audio, and short narrated videos for
  lab-driven courses under courses/ (e.g. learn_unix, learn_git, learn_clustering).
  Runs in Unix or WSL only (not Windows PowerShell/cmd). Keeps course and module
  README.md consistent with the learn_unix public-repo pattern. Revises transcripts
  for spoken English, syncs outline/slides, dual Track A/B callouts, captures
  browser-lab UI snapshots and algorithm walkthrough frames (Playwright) into
  assets/steps/, requires full media (pptx→pdf→audio→video), clustering-depth
  content (algorithm-specific transcripts, walkthrough frames, Track A common/
  solvers), and publishes the course into platform/ at digital_learning quality
  (catalog + pages.js lab shells, tools with starter+challenges) when media and
  tools are ready. Use when the user mentions module-slides, module PPT/pptx, PDF,
  transcript, narration, TTS, video clips, quiz.json, lab screenshot/snapshot,
  algorithm walkthrough, step frames, platform publish, course/module README, or
  media for a course module.
---

# Module Slides

Turn **one course module** into a short teaching clip: **slides (PPTX) → PDF → natural narration → MP4**, plus optional quiz.

**Unit of work:** `courses/<course_id>/moduleNN-<slug>/` (lab-driven syllabus).  
**Not** book chapters under `lectures/` — that legacy layout is retired; use this skill for the monorepo courses.

Work **one module at a time** unless the user asks for a course bulk run.

## Runtime host (required)

**All module-slides commands run in Unix or WSL — not native Windows** (not PowerShell, not cmd, not Windows Python for media).

| Do | Don’t |
|----|--------|
| Open a **WSL** (or Linux/macOS) shell, `cd` to the repo | Run `narrate_clips.sh` / `pptx_to_pdf.sh` / `build_video.sh` from PowerShell |
| Use `python3` and `bash` on that host | Rely on Windows LibreOffice / Windows ffmpeg |
| Install deps in WSL: `soffice`, `ffmpeg`, `pdftoppm`, `edge-tts`, Playwright Chromium | Mix Windows Python PPTX with a one-off `wsl soffice` unless debugging |

```bash
# From WSL (example path — adjust drive/mount)
cd /mnt/d/proj/designs/eda_learning

# One module end-to-end:
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/<course>/moduleNN-slug

# Whole course:
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  --course-dir courses/<course>
```

Bash entry points source `_require_unix.sh` and **exit** if they detect MSYS/Cygwin/Windows.

**Agent rule:** when building PDF, audio, or video, invoke tools via `wsl -e bash -lc 'cd … && …'` only if the agent shell is Windows; prefer a WSL terminal. Prefer `python3` over `python` in all skill examples.

## Scope

| In | Out |
|----|-----|
| `transcript.md` (spoken source of truth) | Inventing new labs or syllabus modules |
| Course + module `README.md` (learn_unix pattern) | Rewriting CHECKLIST / EXAMPLES body unless asked |
| `outline.yaml` + `slides.md` | Fake PDFs without LibreOffice |
| `slides.pptx` / `slides.pdf` / `audio/` / `video.mp4` | Stopping at PPTX when PDF/audio/video toolchain exists |
| Algorithm walkthrough frames (`assets/steps/`) | Hand-authored static lab HTML (use publish script) |
| Platform publish (`platform/courses/…`) when course is ready | Committing large binaries unless asked |
| Optional `quiz.json` | — |

**Dual tracks (when the module has them):** narration may mention Track A (implement / real shell) and Track B (browser lab) — say them as “implement track” / “browser lab track” (or “real Unix track”), never as raw URLs in speech.

## Definition of done

### One module is done when

1. Natural `transcript.md` with `## Slide N`
2. Synced `outline.yaml` + `slides.pptx`
3. `slides.pdf` (LibreOffice in WSL)
4. `audio/full.mp3` + `audio/slide_timings.json`
5. `video.mp4`
6. Optional `quiz.json`
7. Track B: `assets/lab-starter.png` when a browser tool exists
8. Algorithm labs: `assets/steps/*.png` + walkthrough region in transcript

**Do not stop at PPTX.** PDF, audio, and video are required whenever `soffice` / `edge-tts` / `ffmpeg` are available in WSL.

### A course is ready when (in addition)

1. All modules meet the module bar (or deferred items are listed explicitly)
2. **Content depth parity** with `learn_clustering` (see [Content depth parity](#content-depth-parity-learn_clustering-bar)) — walkthroughs, algorithm-specific transcripts, `common/` solvers
3. **Course `README.md`** matches the [learn_unix](https://github.com/universal-verification-methodology/learn_unix) pattern (badges, TOC, Contents, Browse/clone, Consume from parent, Author/module-slides, Two tracks, Module landings, Browser labs, License) — see [README conventions](#readme-conventions-learn_unix-pattern) and `templates/course_README.md.example`
4. **Each module `README.md`** matches kind-specific templates (`lab` / `intro` / `wrap`) — Media table, prev/next, Track A/B when lab
5. `python3 .cursor/skills/module-slides/scripts/verify_course_readme.py courses/<course_id> --modules` passes
6. Browser tools shipped under `platform/tools/<lab-id>/` with **starter example + challenges** (digital_learning pattern)
7. `python3 platform/scripts/publish_course_platform.py <course_id>` has been run
8. Platform course pages use **catalog + `pages.js` shells** (progress, prev/next, tool CTA, video, quiz) — not thin static video tags
9. `platform/course-media/<course_id>` symlink works for local media
10. Smoke: `python3 -m http.server 8080 --directory platform` → `/courses/<id>/` and one lab page render correctly

Reference quality bar: **learn_unix** course README + **digital_learning** lab shells + **learn_clustering** content depth (walkthroughs, solvers, algorithm-specific narration).

## Content depth parity (learn_clustering bar)

Scaffold + media alone is **not** enough. Every new algorithm course must reach **clustering-depth** before calling the course “ready.” Reference: `courses/learn_clustering/`.

### Non-negotiable depth

| Layer | Required | Anti-pattern (reject) |
|-------|----------|------------------------|
| **Transcripts (lab)** | Algorithm-specific speech: named moves, gains, goldens (e.g. “cut 12 → 3”, “swap A↔D”) | One generic 6-slide template reused for every lab |
| **Walkthrough frames** | `assets/steps/*.png` + `STEPS.md` + `<!-- algorithm-walkthrough -->` in transcript for **every** algorithm lab | PPTX with only Track B/A prose slides |
| **Walkthrough map** | Lab id registered in `platform/tools/algorithm-walkthrough/` **and** `capture_algorithm_walkthrough.py` `LAB_TO_ALGO` | Capture that fails “No walkthrough mapping” |
| **Track A `common/`** | Real reference helpers/solvers + tiny golden instance (Python); not just README | Empty `common/` or JSON-only stub |
| **Browser tools** | Starter example + ~10 challenges via `createChallengeLab` | Tool chrome with no checks |
| **Docs** | `docs/MODULES.md`, `SCOPE.md`, `TWO_TRACKS.md`, **`WALKTHROUGHS.md`** listing every algo lab | Missing walkthrough index |
| **Quizzes** | 3–5 items tied to **this** algorithm’s goldens / pitfalls | Identical quiz text across all labs |

### Authoring order (depth first)

```
1. common/ solvers + goldens
2. Browser tool (starter + challenges) using same goldens
3. algorithm-walkthrough ALGOS entry (5 teaching steps)
4. Capture frames → inject transcript (Step 2c)
5. Revise surrounding speech so it is algorithm-specific (not scaffold boilerplate)
6. Sync → PPTX → PDF → narrate (WSL)
7. docs/WALKTHROUGHS.md + publish
```

### Parity self-check (vs learn_clustering)

Before marking a course ready, compare to clustering:

- [ ] Lab transcript median length and specificity ≈ clustering (concrete metrics in speech)
- [ ] Walkthrough PNG count ≈ 5 × (number of algorithm labs)
- [ ] `common/` has importable solvers / metrics, not only a README
- [ ] No lab still using the scaffold “Here’s the core idea in one breath: {algorithm}” filler

**Do not** ship a course as ready if tools + video exist but walkthroughs / solvers / specific transcripts are missing — list them under Deferred in the packaging report.

```
courses/<course>/moduleNN-slug/
  README.md              # outcomes, Track A/B links (existing)
  CHECKLIST.md
  EXAMPLES.md
  examples/              # Track A trees
  transcript.md          # SOURCE OF TRUTH for slides + TTS
  outline.yaml           # machine deck (synced from transcript)
  slides.md              # Marp view (synced)
  quiz.json              # optional 3–5 formative items
  slides.pptx            # primary deck (also accept clip.pptx)
  slides.pdf
  video.mp4              # narrated clip (module root, beside slides)
  audio/full.mp3
  audio/slide_timings.json
  assets/
    lab-starter.png      # Track B UI (optional)
    real-shell.png       # Track A terminal (optional)
    steps/               # algorithm walkthrough frames
    STEPS.md             # captions for steps/
```

| Convention | Rule |
|------------|------|
| Module folder | `module{NN}-{slug}/` or hierarchical `module{SS}-{AA}-{slug}/` (e.g. clustering) |
| Transcript | `## Slide N — Title` blocks; prose under each = TTS |
| Deck filenames | Prefer `slides.pptx` / `slides.pdf`; scripts may still write `clip.pptx` — rename or copy if needed |
| Course map | [`syllabus.md`](../../../syllabus.md) · course `docs/MODULES.md` |
| Catalog `moduleId` | Must match folder name when hierarchical (publish script reads MODULES.md) |
| Course README | Same section set as public [learn_unix](https://github.com/universal-verification-methodology/learn_unix) |
| Module README | `# Module …: Title` + Kind/lab metadata + Media; lab modules include Track A/B |

## README conventions (learn_unix pattern)

**Canonical reference:** https://github.com/universal-verification-methodology/learn_unix (`README.md` + any `module*/README.md`).

Templates (fill placeholders; do not invent a different section order):

| File | Template |
|------|----------|
| `courses/<id>/README.md` | [`templates/course_README.md.example`](templates/course_README.md.example) |
| Lab module | [`templates/module_README.lab.md.example`](templates/module_README.lab.md.example) |
| Intro module | [`templates/module_README.intro.md.example`](templates/module_README.intro.md.example) |
| Wrap module | [`templates/module_README.wrap.md.example`](templates/module_README.wrap.md.example) |

### Course README — required sections (in order)

1. `# <course_id>` + badge row (GitHub · License CC BY 4.0 · Role · Parent · Labs · Domain)
2. One-sentence tagline (`**<id>** is the open learning path for *…*.`)
3. Short reader/author/submodule blurb
4. `## Table of contents`
5. `## Contents` (tree; note optional media + module-slides)
6. `## Browse or clone`
7. `## Consume from the parent`
8. `## Author: publish or update` (module-slides commands; prefer `python3`)
9. `## Two learning tracks` (table + link `docs/TWO_TRACKS.md`)
10. `## Module landings` (table → each `module…/README.md`; point at `docs/MODULES.md`)
11. `## Browser labs` (Track B lab ids / links)
12. `## License` (CC BY 4.0 + `LICENSE`)

**Adaptations allowed:** Track A label may be “Real Unix”, “Implement”, etc.; hierarchical module ids; courses not yet a public submodule still keep the same headings (Role badge may say `course` until published).

**Not allowed:** Dropping TOC / Browse / Consume / Author / Browser labs; replacing Module landings with only a link to MODULES.md and no table; using `python` instead of `python3` in Author examples.

### Module README — by kind

| Kind | Must include |
|------|----------------|
| `lab` | `# Module …: Title` · Kind + Primary lab + Shipped/Planned · prev/next · Outcomes · Two tracks (A + B; **local + live** tool URLs when **Shipped**; planned labs say so explicitly) · Media · Files tree |
| `intro` | Kind intro · dual-track welcome · Setup A/B · How to move · Media · Next |
| `wrap` | Kind wrap · You can now · Dual-track recap · Next course · Checklist · Media |
| `offline` | Kind offline · Outcomes · Track A (or offline harness) · Media · prev/next |

Media table rows: Transcript · Outline · Slides (pptx+pdf) · Video · Quiz (link even if optional).

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/<course_id> --modules
# Public submodule gold:
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_unix --modules --strict-github
```

## Design principles

1. **One module ≈ one clip** — Target **3–8 minutes** spoken; hard cap **~10 minutes**.
2. **Transcript first** — Write/revise `transcript.md` for the **ear**, then sync slides. Never shorten speech to fit bullets.
3. **Bullets ≠ narration** — Slides summarize; transcript teaches.
4. **Natural speech** — Revise stub/robotic transcripts before TTS (see below).
5. **Re-sync after edits** — transcript → outline → PPTX → PDF → narrate.

## Workflow

End-to-end order (do not skip media steps when toolchain is present):

```
Module-Slides Progress:
- [ ] 1. Inventory — README + MODULES.md / syllabus + lab status (S/P)
- [ ] 1b. Align course + module README.md to learn_unix pattern (verify_course_readme.py)
- [ ] 2. Draft or revise transcript.md (natural speech + ## Slide N)
- [ ] 2a. Revise for natural audio (required before TTS)
- [ ] 2b. Capture lab UI snapshot → assets/lab-starter.png (Track B / intro)
- [ ] 2c. Capture algorithm walkthrough → assets/steps/ + inject transcript (algo labs)
- [ ] 2d. Capture real-shell frame → assets/real-shell.png (Track A when useful)
- [ ] 3. Sync outline.yaml + slides.md from transcript
- [ ] 4. Build slides.pptx; verify_clip.py + verify_transcript_consistency.py
- [ ] 5. Export slides.pdf (LibreOffice) — required in WSL when soffice exists
- [ ] 6. TTS + narrated MP4 (narrate_clips.sh) — required when edge-tts/ffmpeg exist
- [ ] 7. Optional quiz.json
- [ ] 8. Packaging report for this module
- [ ] 9. Course ready: READMEs OK + tools (starter+challenges) + platform publish
```

### Step 1: Inventory

From the module folder and course docs:

| Field | Source |
|-------|--------|
| Title / kind | `README.md` (`intro` / `lab` / `wrap` / …) |
| Primary lab | README lab id + shipped/planned |
| Track A examples | `examples/`, `EXAMPLES.md` |
| Track B URL | tools index / lab path |
| Existing stubs | `outline.yaml`, `transcript.md` |
| Course README | Matches learn_unix section set? (Step 1b) |

### Step 1b: README consistency (course + modules)

When scaffolding a course, publishing, or when the user asks for README alignment:

1. Diff course `README.md` against [`templates/course_README.md.example`](templates/course_README.md.example) / public learn_unix — restore missing sections; keep course-specific domain/track wording.
2. For each `module*/README.md`, match kind template (`lab` / `intro` / `wrap`). Prefer `# Module …: Title` (not a bare title H1). Lab modules: local + live Track B URLs when shipped.
3. Keep Module landings in the **course** README in sync with `docs/MODULES.md` (same modules, same order).
4. Verify:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/<course_id> --modules
```

Do this **before** calling the course “ready” (Step 9). Updating READMEs does not replace media work — it is a parallel readiness gate.

### Step 2: Transcript (source of truth)

Replace scaffold stubs with a full clip transcript:

```markdown
# Module NN — Title

**Module id:** moduleNN-slug
**Lab:** lab-id or none
**Tracks:** A (real shell) · B (browser lab) · or intro/wrap only

## Slide 1 — Title

Spoken prose for slide 1…

## Slide 2 — Why this matters

…
```

**Consistency (non-negotiable):**

- Every `## Slide N — Title` = one PPTX slide = one TTS segment.
- Outline `notes` for slide N = transcript body for that slide.
- After edits: re-sync → rebuild PPTX/PDF → re-narrate.

### Step 2a: Revise for natural audio (required before TTS)

Scaffold transcripts often sound like READMEs. **Revise before synthesizing.**

| Do | Don’t |
|----|--------|
| Short sentences; contractions OK (“you’ll”, “it’s”) | Wall of markdown / checklist language |
| Spoken transitions (“Next,” “Here’s the idea,” “Try this”) | “Outcomes:” / “Kind: lab” read aloud |
| Say “browser lab” / “real terminal” | Read URLs, `http://…`, or `~/unix_practice` paths as code |
| Say “module three” or “this module” | “Module 03” with leading zero in speech |
| Name each demo command and what it does | Bare command dumps with no purpose |
| One idea per slide; 45–90 seconds aloud | Cramming Track A and B demos into one breath |
| Impersonal teaching voice with warmth | Hype (“amazing”, “crucial”) or slang overload |

**Read-aloud test:** If it sounds like documentation, rewrite. Prefer:

> “In a real terminal, change into the examples folder for this module and list the files.”

over:

> “Open `examples/` under `module03-path-abs-rel` and run `ls -la`.”

Paths and commands belong on **slides** (and Track A EXAMPLES), not in every spoken sentence. Mention one demo command only when it helps the learner hear it.

**Dual-track slide pattern (lab modules):**

1. Opener + promise  
2. Concept  
3. Browser lab (Track B) — **orient, don’t tour** + UI snapshot  
4. Real shell (Track A) — **introduce examples** + try-these commands on slide  
5. Pitfall  
6. Your turn + quiz nudge  

Intro/wrap modules skip lab / examples demos.

### Pedagogy: how much to teach in the clip

| Track | Clip job | Leave for the learner |
|-------|----------|------------------------|
| **B — Browser lab** | Orient: name 2–3 UI regions (challenge, terminal/tree, Check), show **lab** snapshot (`assets/lab-starter.png`), one first action | Full challenge walkthrough, every button |
| **A — Real Unix** | Introduce `examples/`, show a **real-shell** frame (`assets/real-shell.png`) + try-these `code` slide — same environment as later Icarus/Verilator/Git work | Exhaustive EXAMPLES.md tour |

**Track B rule of thumb:** lab screenshot teaches the layout; speech says “open the lab, use the challenge panel, explore.” Do **not** narrate a full UI manual.

**Track A rule of thumb (default visual = real terminal):** Prefer a captured WSL/Linux session over the browser lab UI. EDA tools (Icarus, Verilator, Make, Git) run in a real shell — slides should look like that early. Capture with:

```bash
python3 .cursor/skills/module-slides/scripts/capture_real_shell.py \
  courses/<course>/moduleNN-slug \
  --example-subdir <folder> \
  --commands "pwd,ls -la,…"

# Or run a prepared demo script (learn_git pattern):
python3 .cursor/skills/module-slides/scripts/capture_real_shell.py \
  courses/learn_git/module02-git-graph \
  --bash-script assets/_demo_m02.sh
# → assets/real-shell.png (+ .txt)
```

### Explain every demo command (required)

Do **not** dump a bare command list. For each try-these line, the learner must hear (and preferably see) **what it does**.

| Where | Rule |
|-------|------|
| **Speech** | Name the command in spoken English and give a one-beat purpose (“print working directory”, “list including hidden files”) |
| **Code slide** | `#` comment above each command; **one blank line between command groups** |
| **Flags** | Explain non-obvious flags (`-la`, `--help`, pipes like `head`) in the same breath or comment |
| **Don’t** | Read punctuation aloud (`ls dash ell ay`); say “list with a long listing that includes hidden files” |

`build_pptx` also auto-inserts a blank line after each command when the fence omitted one, so spacing stays readable.

Pattern for Track A sections:

~~~~markdown
## Slide 4 — Real shell practice

![Real shell session](assets/real-shell.png)

In the real Unix track, open this module’s navigation example.
First, print the working directory so you know where you are.
Then list everything here, including hidden files, in the long format.
Change into the sample project folder, list again, then move up one level with two dots.

~~~~bash
# pwd — print working directory (where am I?)
pwd

# ls -la — list all entries, long format (what is here?)
ls -la

# cd sample_repo — change into this directory
cd sample_repo

# ls — list names only
ls

# cd .. — go up one directory
cd ..
~~~~
~~~~

Lab `assets/lab*` images stay full **`image`** slides (Track B). `assets/real-shell*.png` are full **`image`** slides (Track A); a following bash fence still emits a **`code`** slide. TTS skips the fence (including `#` comments); explanations live in the spoken prose above.

### Step 2b: Lab UI snapshot (Track B / intro)

*(Natural-speech revise is Step 2a above — do that before TTS even if captures come first.)*

For lab modules (and intro “tools map” beats), capture a real screenshot of the browser lab so the Track B slide shows the UI — not only a description.

**Prereqs**

```bash
pip install -r .cursor/skills/module-slides/scripts/requirements.txt
playwright install chromium   # in the same Unix/WSL environment

# Local preferred (matches Track B URLs in CHECKLIST):
python3 -m http.server 8080 --directory platform
```

**Capture**

```bash
# Lab id from README "Primary lab: `…`"
python3 .cursor/skills/module-slides/scripts/capture_lab_snapshot.py \
  courses/<course>/moduleNN-slug \
  --patch-outline

# Or explicit lab / live site:
python3 .cursor/skills/module-slides/scripts/capture_lab_snapshot.py \
  courses/learn_unix/module03-path-abs-rel \
  --lab path-abs-rel \
  --base https://universal-verification-methodology.github.io/learning/tools \
  --patch-outline

# Intro tools index:
python3 .cursor/skills/module-slides/scripts/capture_lab_snapshot.py \
  courses/learn_unix/module00-intro \
  --lab index \
  --name tools-index.png \
  --patch-outline
```

Writes `assets/lab-starter.png` (or `--name`). With `--patch-outline`, inserts/updates an `image` slide in `outline.yaml`.

**Authoring rules**

- Prefer embedding in `transcript.md` so re-sync keeps the image:

```markdown
## Slide 3 — Browser lab

![Browser lab starter](assets/lab-starter.png)

In the browser lab track, open this lab and load the starter example…
```

- Lab snapshots under `assets/lab*` become a **full-slide `image`** (not a cramped two-column) so they read clearly in PPTX/PDF/video.
- Or use `--patch-outline` after sync; re-run patch if you re-sync without the markdown image.
- Narration orients the learner (“look at the starter panel”) — do **not** read the URL aloud.
- Re-capture after lab UI changes; commit PNGs only when the user wants media in git.
- Crop with `--selector main` when chrome/header is noisy; use `--full-page` sparingly.

If Playwright/Chromium is unavailable, leave `(screenshot pending: …)` via a missing path and continue — do not invent fake UI art.

### Step 2c: Algorithm walkthrough frames (visual PPT)

For algorithm / EDA labs that have a browser walkthrough (`platform/tools/algorithm-walkthrough/`), capture **step frames** so the deck shows how the algorithm moves—not only a lab chrome shot.

**When to use:** clustering (and similar) modules whose primary lab is in the walkthrough map (`affinity-metrics`, `greedy-pair-merge`, `label-propagation`, `kernighan-lin`, `fiduccia-mattheyses`, …). Skip for pure shell/tools-map modules.

**Prereqs:** same Playwright install + `python3 -m http.server 8080 --directory platform`.

**Capture + inject into transcript**

```bash
python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
  courses/learn_clustering/module02-07-fiduccia-mattheyses \
  --inject-transcript
```

Writes:

| Output | Role |
|--------|------|
| `assets/steps/NN-<id>.png` | Full-slide teaching frames |
| `assets/STEPS.md` | Captions + bullets (authoring source) |
| `transcript.md` region between `<!-- algorithm-walkthrough -->` markers | Spoken captions + `![…](assets/steps/…)` embeds |

Re-run capture after walkthrough UI/copy changes; `--skip-capture --inject-transcript` rebuilds slides from existing `STEPS.md`.

**Authoring rules**

- Prefer the injected region so re-sync keeps images as **full-slide `image`** slides (`assets/steps/` is treated like lab snapshots—not a cramped two-column).
- Spoken prose = walkthrough **caption** (natural, one idea per step). Do **not** read metrics dumps aloud.
- Keep total clip ≤ ~10 minutes: typically **3–5** algorithm steps + opener + Track B orient + Track A + pitfall + your turn.
- Interactive preview: `http://127.0.0.1:8080/tools/algorithm-walkthrough/?algo=<lab>&step=1`
- Course index (clustering): `courses/learn_clustering/docs/WALKTHROUGHS.md`

**Dual-track slide pattern (algorithm lab modules):**

1. Opener + promise  
2. Algorithm step frames (walkthrough PNGs) — teach the move  
3. Browser lab (Track B) — orient + `lab-starter.png` when available  
4. Implement / real shell (Track A) — examples + try-these  
5. Pitfall  
6. Your turn + quiz nudge  

### Step 3: Sync slides from transcript

```bash
pip install -r .cursor/skills/module-slides/scripts/requirements.txt

python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/<course>/moduleNN-slug
```

Writes/updates `outline.yaml` + `slides.md`. Slide bullets are summaries of prose (`prose_to_bullets.py`).

### Step 4: Build and verify PPTX

```bash
python3 .cursor/skills/module-slides/scripts/build_pptx.py \
  courses/<course>/moduleNN-slug

python3 .cursor/skills/module-slides/scripts/verify_clip.py \
  courses/<course>/moduleNN-slug
```

Also run transcript consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_transcript_consistency.py \
  courses/<course>/moduleNN-slug
```

**Layout rules:** 20 pt body / 28 pt headings; max 6 bullets; ~100 chars/bullet; no auto-shrink; footer like `learn_unix — paths`.

### Step 5: PDF

```bash
bash .cursor/skills/module-slides/scripts/pptx_to_pdf.sh \
  courses/<course>/moduleNN-slug/slides.pptx
```

Needs LibreOffice (`soffice`) **in WSL/Linux**. If missing: `sudo apt install libreoffice-impress default-jre-headless`. Do not fake PDFs.

### Step 6: Audio + video

```bash
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/<course>/moduleNN-slug
```

Or:

```bash
bash .cursor/skills/module-slides/scripts/synthesize_audio.sh courses/<course>/moduleNN-slug
bash .cursor/skills/module-slides/scripts/build_video.sh --target-dir courses/<course>/moduleNN-slug
```

Outputs: `audio/full.mp3`, timings, `video.mp4` (module root). Default voice `en-US-JennyNeural` (`VOICE=...` to override).

TTS skips H1 / metadata / `## Slide` headings — only narration paragraphs are spoken. Still write path-free prose; rewriting in `transcript_to_speech.py` is a safety net.

### Step 7: Quiz (optional)

`quiz.json` — 3–5 items tied to **this module’s** objectives (see [reference.md](reference.md)).

### Step 8: Packaging report

```
Course: <course_id>
Module: NN — title (kind)
Lab: id (S|P|none)
Artifacts: transcript / outline / slides.md / pptx / pdf / audio / video / quiz
Natural-speech revise: yes/no
Deferred: …
```

### Step 9: Platform publish (course ready)

When **tools are shipped** and **module media exists** (`slides.pptx` / `slides.pdf` / `video.mp4`), publish into `platform/` at **digital_learning quality**.

#### 9a. Browser tools (before or with media)

Each lab tool under `platform/tools/<lab-id>/` should match the digital_learning pattern:

| Requirement | Notes |
|-------------|--------|
| Starter example loaded by default | Learner sees a working graph/netlist immediately |
| Challenges (typically ~10) | Progressive tasks with Check / feedback |
| Shared UI helpers when applicable | e.g. clustering `createChallengeLab` |
| Linked from MODULES.md / catalog `labs[]` | Lab id matches tool folder |

Algorithm courses also keep `platform/tools/algorithm-walkthrough/` in sync with lab ids used by `capture_algorithm_walkthrough.py`.

#### 9b. Publish script

**Host:** Unix/WSL. From repo root:

```bash
python3 platform/scripts/publish_course_platform.py <course_id>
# e.g. learn_clustering

python3 -m http.server 8080 --directory platform
# → http://127.0.0.1:8080/courses/<course_id>/
# → lab page e.g. …/labs/fiduccia-mattheyses/
```

| Output | Role |
|--------|------|
| `platform/assets/catalog.json` | `courses[]` (+ `moduleId` for hierarchical folders) + tools `labs[]` |
| `platform/assets/site-config.js` · `pages.js` · `quiz.js` | Same renderer stack as digital_learning |
| `platform/courses/<id>/index.html` | Course map + progress (`data-render="course-labs"`) |
| `platform/courses/index.html` | **Courses map** (`data-render="path-map"`) — same ladder UI as digital_learning |
| `platform/courses/<id>/labs/<slug>/` | Lab shell (`data-render="lab"`) — progress, prev/next, Open tool, video, quiz |
| `platform/course-media/<id>` | Symlink → `../../courses/<id>` for local video/pdf/quiz |

**Quality rules (non-negotiable):**

- Do **not** hand-author static `<video>` tags on lab pages — regenerate with the publish script.
- Lab shells must be `data-render="lab"` so `pages.js` fills media from catalog + `course-media/`.
- Hierarchical module folders need `moduleId` in catalog (publish reads course `docs/MODULES.md`).
- After publish, smoke one course page and one lab page in the browser.

## Bulk (when asked)

For a whole course:

1. Revise transcripts (and walkthrough injects) **per module** before TTS — do not batch-narrate stubs.
2. Prefer the course helper when it exists, e.g.:

```bash
# WSL — clustering example (PDF + audio + video for all modules)
bash courses/learn_clustering/scripts/build_all_media.sh

# Then publish platform shells
python3 platform/scripts/publish_course_platform.py learn_clustering
```

3. Otherwise loop syllabus order: sync → PPTX → PDF → `narrate_clips.sh` per module.
4. Always finish with Step 9 when tools + media are ready.

## Quality bar

### Media (per module)

- [ ] Transcript uses `## Slide N — Title` and passes read-aloud test
- [ ] No raw URLs or repo paths in spoken prose
- [ ] Dual tracks described in speech when module is `lab`
- [ ] Track B: orient + **lab** snapshot (not a full UI tour)
- [ ] Algorithm labs: **walkthrough** frames in `assets/steps/` embedded in transcript
- [ ] Track A: **real-shell** / implement frame + examples / try-these when applicable
- [ ] Every demo command explained (speech + `#` comments or bullets) — not a bare dump
- [ ] `verify_transcript_consistency.py` + `verify_clip.py` pass
- [ ] Spoken length estimate ≤ 10 minutes (`words / 140`)
- [ ] `slides.pptx` + `slides.pdf` exist (PDF via LibreOffice in WSL)
- [ ] `audio/full.mp3` + `video.mp4` exist (only after natural transcript)
- [ ] Host was Unix/WSL for all media scripts (never native Windows)

### Platform (per course, when ready)

- [ ] Course + module READMEs pass `verify_course_readme.py --modules`
- [ ] Course README section order matches learn_unix (TOC → … → License)
- [ ] Tools have starter example + challenges (~10)
- [ ] Algorithm labs: walkthrough frames + `WALKTHROUGHS.md` + `LAB_TO_ALGO` mapping
- [ ] Lab transcripts are algorithm-specific (goldens/moves), not scaffold boilerplate
- [ ] Track A `common/` has solvers/metrics (not README-only)
- [ ] `publish_course_platform.py <course_id>` regenerated catalog + shells
- [ ] Lab pages are `data-render="lab"` (digital_learning quality — not thin static HTML)
- [ ] Catalog entries include `moduleId` when folders are hierarchical
- [ ] `course-media/<id>` symlink resolves; local preview shows video + quiz
- [ ] Smoke `/courses/<id>/` and one `/labs/<slug>/` page in browser
- [ ] Depth parity self-check vs `learn_clustering` passed (or gaps listed as Deferred)

## Scripts (skill root)

| Script | Role |
|--------|------|
| `transcript_to_outline.py` | Transcript → outline + slides.md |
| `build_pptx.py` | outline → `slides.pptx` / `clip.pptx` |
| `verify_clip.py` | Bullet/image/deck checks |
| `verify_transcript_consistency.py` | Transcript ↔ outline notes |
| `verify_course_readme.py` | Course + module README vs learn_unix pattern |
| `pptx_to_pdf.sh` | LibreOffice export (Unix/WSL) |
| `capture_lab_snapshot.py` | Track B lab UI → `assets/lab-starter.png` |
| `capture_algorithm_walkthrough.py` | Algorithm steps → `assets/steps/` + optional transcript inject |
| `capture_real_shell.py` | Track A real WSL/bash session → `assets/real-shell.png` |
| `narrate_clips.sh` | TTS + timings + MP4 (Unix/WSL entry) |
| `_require_unix.sh` | Guard: refuse native Windows shells |
| `synthesize_audio.sh` / `build_video.sh` | Manual media steps |
| `prose_to_bullets.py` / `transcript_to_speech.py` | Helpers |

**Platform (repo `platform/scripts/`, not under skill):** `publish_course_platform.py` — after media+tools, sync catalog and generate `platform/courses/<id>/` (see Step 9).

**Course helpers (example):** `courses/learn_clustering/scripts/build_all_media.sh` — bulk PPTX→PDF→audio→video in WSL; call publish afterward.

Install (in WSL/Linux): `pip install -r .cursor/skills/module-slides/scripts/requirements.txt` then `playwright install chromium`. System: `sudo apt install libreoffice-impress ffmpeg poppler-utils`.

## Related

- Syllabus: [`syllabus.md`](../../../syllabus.md)
- README gold standard: [learn_unix](https://github.com/universal-verification-methodology/learn_unix)
- Example courses: `courses/learn_unix/` · `courses/learn_git/` · `courses/learn_clustering/`
- Platform preview: `python3 -m http.server 8080 --directory platform`
- Schemas/templates: [reference.md](reference.md) · `templates/*_README*.example`
