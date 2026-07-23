#!/usr/bin/env python3
"""Scaffold clustering browser tools under platform/tools/."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

TOOLS_META = [
    ("affinity-metrics", "Affinity metrics", "Rank node pairs by edge-weight and shared-neighbor affinity."),
    ("greedy-pair-merge", "Greedy pair merge", "Step heaviest-edge merges down to K clusters and watch cutsize."),
    ("label-propagation", "Label propagation", "Async label updates until communities stabilize."),
    ("kernighan-lin", "Kernighan–Lin", "Pair-swap refinement with rollback from a bad seed (12→3)."),
    ("fiduccia-mattheyses", "Fiduccia–Mattheyses", "Single-vertex FM moves with rollback from a bad seed."),
]


def page(tool_id: str, title: str, lead: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — EDA Algorithms Platform</title>
  <link rel="stylesheet" href="../../assets/site.css">
  <link rel="stylesheet" href="../../assets/tools-shared.css">
  <link rel="stylesheet" href="../../assets/clustering-lab.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="site-header-inner">
      <p class="brand"><a href="../../index.html">EDA Algorithms Platform</a></p>
      <nav class="site-nav" aria-label="Site">
        <a href="../../index.html">Home</a>
        <a href="../index.html" class="is-active" aria-current="page">Tools</a>
      </nav>
    </div>
    <div class="site-header-crumb">
      <nav aria-label="Breadcrumb">
        <a href="../../index.html">Home</a>
        <a href="../index.html">Tools</a>
        <span class="here">{title}</span>
      </nav>
    </div>
  </header>
  <main id="main">
    <div class="eyebrow">Interactive tool</div>
    <section class="hero">
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </section>
    <div id="lab-root"></div>
  </main>
  <footer class="site-footer">EDA Algorithms Platform — client-side concept labs.</footer>
  <script type="module" src="{tool_id}.js"></script>
  <script src="../../assets/site.js"></script>
</body>
</html>
"""


AFFINITY_JS = r'''import {
  TINY_GRAPH,
  affinityEdgeWeight,
  affinitySharedNeighbors,
  cloneGraph,
} from "../../assets/clustering-core.js";
import { drawGraph, el, mountShell } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let mode = "edge";
let graph = cloneGraph();

const ui = mountShell(root, {
  title: "Affinity metrics",
  starterNote: "Starter example: 5-node weighted graph — A–B and D–E are heaviest (weight 5).",
  onLoadStarter: loadStarter,
});

ui.actions.append(
  el("button", {
    className: "btn btn-primary",
    type: "button",
    text: "Edge-weight ranking",
    onClick: () => {
      mode = "edge";
      render();
      check();
    },
  }),
  el("button", {
    className: "btn btn-primary",
    type: "button",
    text: "Shared-neighbor ranking",
    onClick: () => {
      mode = "shared";
      render();
      check();
    },
  })
);

function loadStarter() {
  graph = cloneGraph();
  mode = "edge";
  ui.challengePrompt.textContent =
    "Show edge-weight ranking with A–B (or D–E) on top at score 5, then switch to shared-neighbor and confirm A–B becomes 6.";
  ui.setStatus("idle", "Idle");
  render();
}

function render() {
  const ranked =
    mode === "edge"
      ? affinityEdgeWeight(graph.edges)
      : affinitySharedNeighbors(graph.nodes, graph.edges);
  const top = ranked[0];
  const highlight = top ? [`${top[0]}|${top[1]}`] : [];
  drawGraph(ui.canvas, graph, { highlightPairs: highlight });
  ui.metrics.innerHTML = "";
  ui.metrics.append(
    el("p", { text: `Mode: ${mode === "edge" ? "edge-weight" : "shared-neighbor + edge"}` })
  );
  const table = el("table", { className: "rank-table" });
  table.innerHTML =
    "<thead><tr><th>Pair</th><th>Score</th></tr></thead>" +
    "<tbody>" +
    ranked
      .map(([u, v, s]) => `<tr><td>${u}–${v}</td><td>${s}</td></tr>`)
      .join("") +
    "</tbody>";
  ui.metrics.append(table);
}

function check() {
  const edge = affinityEdgeWeight(graph.edges);
  const shared = affinitySharedNeighbors(graph.nodes, graph.edges);
  const okEdge = edge[0][2] === 5 && edge[0][0] === "A" && edge[0][1] === "B";
  const okShared = shared[0][2] === 6 && shared.find((r) => r[0] === "A" && r[1] === "B")[2] === 6;
  if (okEdge && okShared) ui.setStatus("pass", "PASS — rankings match course goldens");
  else ui.setStatus("fail", "Keep exploring both modes");
}

loadStarter();
'''

GREEDY_JS = r'''import {
  TINY_GRAPH,
  cloneGraph,
  cutsize,
  greedyPairMerge,
} from "../../assets/clustering-core.js";
import { drawGraph, el, mountShell, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let state = { assignment: null, mergeLog: [] };

const ui = mountShell(root, {
  title: "Greedy pair merge",
  starterNote: "Starter example: merge to K=2 — expect clusters {A,B,C} vs {D,E}, cutsize 3.",
  onLoadStarter: loadStarter,
});

ui.actions.append(
  el("button", {
    className: "btn btn-primary",
    type: "button",
    text: "Run merge K=2",
    onClick: () => {
      state = greedyPairMerge(graph.nodes, graph.edges, graph.sizes, 2);
      render();
      const parts = {};
      for (const [n, c] of Object.entries(state.assignment)) {
        (parts[c] ||= []).push(n);
      }
      const sets = Object.values(parts).map((a) => a.sort().join("")).sort();
      const cut = cutsize(state.assignment, graph.edges);
      if (cut === 3 && sets.join("|") === "ABC|DE") ui.setStatus("pass", "PASS — cutsize 3");
      else ui.setStatus("fail", `cut=${cut}; check merges`);
    },
  })
);

function loadStarter() {
  graph = cloneGraph();
  state = { assignment: null, mergeLog: [] };
  ui.challengePrompt.textContent = "Run merge to K=2 and match cutsize 3 with {A,B,C}/{D,E}.";
  ui.setStatus("idle", "Idle");
  render();
}

function render() {
  drawGraph(ui.canvas, graph, { assignment: state.assignment });
  const lines = [];
  if (!state.assignment) {
    lines.push("Click Run merge K=2");
  } else {
    lines.push(`cutsize: ${cutsize(state.assignment, graph.edges)}`);
    lines.push("merges:");
    for (const m of state.mergeLog) lines.push(`  ${m.u}-${m.v} (w=${m.w}) -> ${m.into}`);
    lines.push("assignment: " + JSON.stringify(state.assignment));
  }
  ui.metrics.innerHTML = "";
  ui.metrics.append(metricsBlock(lines));
}

loadStarter();
'''

LP_JS = r'''import { cloneGraph, cutsize, labelPropagation } from "../../assets/clustering-core.js";
import { drawGraph, el, mountShell, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;

const ui = mountShell(root, {
  title: "Label propagation",
  starterNote: "Starter example: async LP — stabilize in 2 iters, cutsize 3.",
  onLoadStarter: loadStarter,
});

ui.actions.append(
  el("button", {
    className: "btn btn-primary",
    type: "button",
    text: "Run label propagation",
    onClick: () => {
      result = labelPropagation(graph.nodes, graph.edges);
      render();
      const cut = cutsize(result.labels, graph.edges);
      if (result.iters === 2 && cut === 3) ui.setStatus("pass", "PASS — iters 2, cut 3");
      else ui.setStatus("fail", `iters=${result.iters} cut=${cut}`);
    },
  })
);

function loadStarter() {
  graph = cloneGraph();
  result = null;
  ui.challengePrompt.textContent = "Run LP and match iters=2, cutsize=3.";
  ui.setStatus("idle", "Idle");
  render();
}

function render() {
  drawGraph(ui.canvas, graph, { assignment: result ? result.labels : null });
  const lines = result
    ? [
        `iters_to_stable: ${result.iters}`,
        `cutsize: ${cutsize(result.labels, graph.edges)}`,
        `labels: ${JSON.stringify(result.labels)}`,
        `num_clusters: ${new Set(Object.values(result.labels)).size}`,
      ]
    : ["Click Run label propagation"];
  ui.metrics.innerHTML = "";
  ui.metrics.append(metricsBlock(lines));
}

loadStarter();
'''

KL_JS = r'''import { BAD_SEED, cloneGraph, cutsize, kernighanLin } from "../../assets/clustering-core.js";
import { drawGraph, el, mountShell, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let seed = { ...BAD_SEED };
let result = null;

const ui = mountShell(root, {
  title: "Kernighan–Lin",
  starterNote: "Starter example: bad seed cutsize 12 — KL accepts swap (A,D) → cutsize 3.",
  onLoadStarter: loadStarter,
});

ui.actions.append(
  el("button", {
    className: "btn btn-secondary",
    type: "button",
    text: "Show seed only",
    onClick: () => {
      result = null;
      render();
      ui.setStatus("idle", `Seed cutsize ${cutsize(seed, graph.edges)}`);
    },
  }),
  el("button", {
    className: "btn btn-primary",
    type: "button",
    text: "Run KL",
    onClick: () => {
      result = kernighanLin(graph.nodes, graph.edges, seed);
      render();
      const after = cutsize(result.assignment, graph.edges);
      const before = cutsize(seed, graph.edges);
      if (before === 12 && after === 3) ui.setStatus("pass", "PASS — 12 → 3");
      else ui.setStatus("fail", `${before} → ${after}`);
    },
  })
);

function loadStarter() {
  graph = cloneGraph();
  seed = { ...BAD_SEED };
  result = null;
  ui.challengePrompt.textContent = "Show seed cut 12, run KL, reach cut 3.";
  ui.setStatus("idle", "Idle");
  render();
}

function render() {
  const asn = result ? result.assignment : seed;
  drawGraph(ui.canvas, graph, { assignment: asn });
  const lines = [];
  lines.push(`cutsize now: ${cutsize(asn, graph.edges)}`);
  if (result) {
    for (const h of result.history) {
      lines.push(
        `pass ${h.pass}: best_k=${h.bestK} cum=${h.bestCum} cut ${h.cutBefore}→${h.cutAfter}`
      );
      if (h.swaps?.length) lines.push(`  swaps: ${h.swaps.map((s) => `${s.a}/${s.b}(${s.g})`).join(", ")}`);
    }
  } else {
    lines.push("assignment: seed " + JSON.stringify(seed));
  }
  ui.metrics.innerHTML = "";
  ui.metrics.append(metricsBlock(lines));
}

loadStarter();
'''

FM_JS = r'''import { BAD_SEED, cloneGraph, cutsize, fiducciaMattheyses } from "../../assets/clustering-core.js";
import { drawGraph, el, mountShell, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let seed = { ...BAD_SEED };
let result = null;

const ui = mountShell(root, {
  title: "Fiduccia–Mattheyses",
  starterNote: "Starter example: same bad seed (cut 12) — FM moves reach cutsize 3.",
  onLoadStarter: loadStarter,
});

ui.actions.append(
  el("button", {
    className: "btn btn-primary",
    type: "button",
    text: "Run FM",
    onClick: () => {
      result = fiducciaMattheyses(graph.nodes, graph.edges, seed);
      render();
      const after = cutsize(result.assignment, graph.edges);
      if (cutsize(seed, graph.edges) === 12 && after === 3) ui.setStatus("pass", "PASS — 12 → 3");
      else ui.setStatus("fail", `after=${after}`);
    },
  })
);

function loadStarter() {
  graph = cloneGraph();
  seed = { ...BAD_SEED };
  result = null;
  ui.challengePrompt.textContent = "Run FM from the bad seed and reach cutsize 3.";
  ui.setStatus("idle", "Idle");
  render();
}

function render() {
  const asn = result ? result.assignment : seed;
  drawGraph(ui.canvas, graph, { assignment: asn });
  const lines = [`cutsize now: ${cutsize(asn, graph.edges)}`];
  if (result) {
    for (const h of result.history) {
      lines.push(
        `pass ${h.pass}: best_k=${h.bestK} cum=${h.bestCum} cut ${h.cutBefore}→${h.cutAfter}`
      );
      if (h.moves?.length) lines.push(`  moves: ${h.moves.map((m) => `${m.v}(${m.g})`).join(", ")}`);
    }
  }
  ui.metrics.innerHTML = "";
  ui.metrics.append(metricsBlock(lines));
}

loadStarter();
'''

JS = {
    "affinity-metrics": AFFINITY_JS,
    "greedy-pair-merge": GREEDY_JS,
    "label-propagation": LP_JS,
    "kernighan-lin": KL_JS,
    "fiduccia-mattheyses": FM_JS,
}


def main() -> None:
    items = []
    for tid, title, lead in TOOLS_META:
        d = TOOLS / tid
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(tid, title, lead), encoding="utf-8")
        (d / f"{tid}.js").write_text(JS[tid], encoding="utf-8")
        items.append(f'        <li>\n          <a href="{tid}/index.html">{title}</a>\n          <div class="chapter-meta">{lead}</div>\n        </li>')

    index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tools — EDA Algorithms Platform</title>
  <link rel="stylesheet" href="../assets/site.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="site-header-inner">
      <p class="brand"><a href="../index.html">EDA Algorithms Platform</a></p>
      <nav class="site-nav" aria-label="Site">
        <a href="../index.html">Home</a>
        <a href="index.html" class="is-active" aria-current="page">Tools</a>
      </nav>
    </div>
  </header>
  <main id="main">
    <div class="eyebrow">Tools</div>
    <section class="hero">
      <h1>Interactive labs</h1>
      <p class="lead">Clustering / PD algorithm labs — concept shelf for <code>learn_clustering</code>.</p>
    </section>
    <section class="tools-stage" id="clustering">
      <h2>Clustering &amp; refinement</h2>
      <ul class="chapter-list">
{chr(10).join(items)}
      </ul>
    </section>
  </main>
  <footer class="site-footer">EDA Algorithms Platform — client-side concept labs.</footer>
  <script src="../assets/site.js"></script>
</body>
</html>
"""
    (TOOLS / "index.html").write_text(index, encoding="utf-8")

    tools_md = """# Platform tools catalog

Browser labs for **eda_learning**. Serve with:

```bash
python -m http.server 8080 --directory platform
```

## Clustering & refinement

| Tool | Starter | Status |
|------|---------|--------|
| `affinity-metrics` | 5-node graph; edge-weight vs shared-neighbor rankings | **Shipped** |
| `greedy-pair-merge` | Merge to K=2 → cutsize 3 | **Shipped** |
| `label-propagation` | Async LP → iters 2, cutsize 3 | **Shipped** |
| `kernighan-lin` | Bad seed cut 12 → KL → 3 | **Shipped** |
| `fiduccia-mattheyses` | Same seed → FM → 3 | **Shipped** |

## Planned (course modules ready)

`size-constrained-agglomerative`, `spectral-bisection`, `multilevel-clustering`, `hypergraph-clustering`, `congestion-aware-clustering`, `timing-aware-clustering`
"""
    (ROOT / "tools.md").write_text(tools_md, encoding="utf-8")

    catalog = {
        "site": {"title": "EDA Algorithms Platform"},
        "labs": [{"id": t[0], "title": t[1], "section": "Clustering & refinement"} for t in TOOLS_META],
    }
    import json

    (ROOT / "assets" / "catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print(f"Scaffolded {len(TOOLS_META)} tools")


if __name__ == "__main__":
    main()
