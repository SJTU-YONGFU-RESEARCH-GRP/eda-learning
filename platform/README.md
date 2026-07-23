# EDA Algorithms Platform

Static companion site for `eda_learning`: **browser concept labs** for clustering / PD algorithms.

## Quick start

```bash
# from eda_learning repo root (WSL/Linux preferred)
python3 -m http.server 8080 --directory platform
```

Open http://127.0.0.1:8080/ → **Courses** (path-map ladder) or **Tools**.

The courses index matches **digital_learning** `platform/courses/index.html`: hero + `data-render="path-map"` ladder (ready nodes link in; planned show “Soon”).

## Publish a course (after media + tools)

When `learn_clustering` modules have PPTX/PDF/video and tools are shipped:

```bash
python3 platform/scripts/publish_course_platform.py learn_clustering
```

That matches **digital_learning** course quality: catalog sync, `pages.js` lab shells (progress, quiz, prev/next, tool CTA, video), and `course-media/` symlink for local clips.

## Layout

```text
platform/
├── index.html
├── tools.md
├── README.md
├── assets/          # site.css, catalog.json, clustering-*.js
├── course-media/    # symlinks to courses/<id> for local clips
├── courses/         # guided lab pages (video + tool links)
│   └── learn_clustering/
└── tools/           # browser concept labs
```

## Principles (same shelf idea as digital_learning)

- Labs live under `platform/tools/` by **concept id**
- Course modules link here (Track B)
- Client-side only; starter example required on first visit
- Real engines / OSS compare stay offline in `courses/learn_clustering`

## Course link

- Track A: `courses/learn_clustering/`
- Module index: `courses/learn_clustering/docs/MODULES.md`
