/**
 * STA algorithm walkthrough steps (5 each).
 * Consumed by algorithm-walkthrough/walkthrough.js.
 */
import {
  GOLDENS,
  PROP_GOLDENS,
  TINY_TIMING,
  cloneTiming,
  criticalPathTo,
  incrementalArrival,
  levelize,
  propagateArrival,
  propagateRequired,
  setupSlack,
  withCycle,
} from "../../assets/sta-core.js";

const levels = levelize(TINY_TIMING);
const arr = propagateArrival(TINY_TIMING);
const req = propagateRequired(TINY_TIMING);
const path = criticalPathTo(TINY_TIMING, arr, "out");
const pathArcs = [];
for (let i = 0; i < path.length - 1; i++) pathArcs.push(`${path[i]}|${path[i + 1]}`);
const baseArr = propagateArrival(TINY_TIMING);
const inc = incrementalArrival(TINY_TIMING, {
  from: PROP_GOLDENS.incremental.editFrom,
  to: PROP_GOLDENS.incremental.editTo,
  delay: PROP_GOLDENS.incremental.newDelay,
}, baseArr);

function tagMap(m, prefix) {
  const o = {};
  for (const [k, v] of Object.entries(m || {})) o[k] = `${prefix}${v}`;
  return o;
}

/** @typedef {{ id: string, title: string, caption: string, bullets: string[], metrics?: string[], timing?: object|null, levels?: object|null, highlightPins?: string[], highlightArcs?: string[], tags?: object, empty?: boolean }} StaStep */

/** @type {Record<string, { title: string, module: string, kind: 'sta', steps: StaStep[] }>} */
export const STA_ALGOS = {
  "timing-graph": {
    title: "Timing graph",
    module: "module01-01-timing-graph",
    kind: "sta",
    steps: [
      {
        id: "tiny-chain",
        title: "Start with a tiny timing chain",
        caption:
          "Six pins form one path from primary input in through two cells to out. Net arcs are dashed; cell arcs are solid. This is the shared starter for every STA lab.",
        bullets: [
          "Pins = ports and cell pins",
          "Directed arcs carry delay",
          "One path keeps goldens easy to check by hand",
        ],
        metrics: [
          `Pins: ${GOLDENS.pinCount}`,
          `Arcs: ${GOLDENS.arcCount} (${GOLDENS.cellArcs} cell / ${GOLDENS.netArcs} net)`,
          "Clock period: 10 (for later labs)",
        ],
        timing: cloneTiming(TINY_TIMING),
        levels: null,
        highlightPins: ["in", "out"],
      },
      {
        id: "sources-sinks",
        title: "Name sources and sinks",
        caption:
          "A source has no incoming arc; a sink has no outgoing arc. On this chain, in is the only source and out is the only sink.",
        bullets: [
          "Source = no predecessor arc",
          "Sink = no successor arc",
          "Arrival starts at sources; required at sinks",
        ],
        metrics: [`sources: ${GOLDENS.sources.join(", ")}`, `sinks: ${GOLDENS.sinks.join(", ")}`],
        timing: cloneTiming(TINY_TIMING),
        levels: null,
        highlightPins: ["in", "out"],
      },
      {
        id: "levelize",
        title: "Levelize with Kahn's algorithm",
        caption:
          "Process pins with indegree zero, then peel successors. out lands at level 5 on this chain.",
        bullets: [
          "Queue pins with indegree 0",
          "level(v) = 1 + max(level of preds)",
          "If some pins never finish, there is a cycle",
        ],
        metrics: ["in: L0", "u1/A: L1 · u1/Y: L2", "u2/A: L3 · u2/Y: L4", "out: L5"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
      {
        id: "topo-delays",
        title: "Topo order and delay sums",
        caption:
          "Sorting pins by level gives the topo order. Path delay sums to 3.2; cell arcs alone sum to 2.7.",
        bullets: [
          "Topo order follows increasing level",
          "Path delay Σ = sum of every arc",
          "Cell delay Σ ignores net arcs",
        ],
        metrics: [
          `topo: ${GOLDENS.topo.join(" → ")}`,
          `path delay Σ: ${GOLDENS.pathDelay}`,
          `cell delay Σ: ${GOLDENS.cellDelaySum}`,
        ],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightArcs: ["u1/A|u1/Y", "u2/A|u2/Y"],
      },
      {
        id: "cycle-reject",
        title: "A cycle fails levelize",
        caption:
          "Add a back-edge from out to in and Kahn's algorithm stalls. Timing graphs for STA must be acyclic.",
        bullets: [
          "Back-edge out→in creates a cycle",
          "levelize returns null",
          "Fix the graph before propagating arrival",
        ],
        metrics: ["acyclic: false", "levels: null"],
        timing: withCycle(TINY_TIMING),
        levels: null,
        highlightArcs: ["out|in"],
        highlightPins: ["out", "in"],
      },
    ],
  },

  "arrival-required": {
    title: "Arrival and required times",
    module: "module01-03-arrival-required",
    kind: "sta",
    steps: [
      {
        id: "seed-arrival",
        title: "Seed arrival at the source",
        caption:
          "Set arrival at in to zero for the launch edge. Every other pin waits for its predecessors.",
        bullets: ["Arrival at sources starts the wavefront", "Here A(in) = 0", "No delay yet on the first net"],
        metrics: ["A(in) = 0"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: { in: "A:0" },
        highlightPins: ["in"],
      },
      {
        id: "forward-wave",
        title: "Propagate arrival forward",
        caption:
          "For each pin in topo order, arrival is the max over predecessors of A(pred) + delay. At out the wavefront reaches 3.2.",
        bullets: [
          "A(v) = max(A(u) + d(u→v))",
          "Cell delays dominate this toy path",
          "Golden A(out) = 3.2",
        ],
        metrics: [
          "A(u1/Y)=1.2",
          "A(u2/A)=1.5",
          "A(u2/Y)=3.0",
          "A(out)=3.2",
        ],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: tagMap(arr, "A:"),
        highlightPins: ["out"],
      },
      {
        id: "seed-required",
        title: "Seed required at the sink",
        caption:
          "For a single-cycle setup check, required at out equals the clock period—here 10.",
        bullets: ["Setup capture edge sets R(out)", "R(out) = period × cycles", "Default cycles = 1 → 10"],
        metrics: ["period = 10", "R(out) = 10"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: { out: "R:10" },
        highlightPins: ["out"],
      },
      {
        id: "backward-wave",
        title: "Propagate required backward",
        caption:
          "Walk reverse topo order. Required at a pin is the min over successors of R(succ) − delay. At in, required becomes 6.8.",
        bullets: [
          "R(u) = min(R(v) − d(u→v))",
          "Tightest successor wins",
          "Golden R(in) = 6.8",
        ],
        metrics: ["R(u2/Y)=9.8", "R(u1/Y)=8.0", "R(u1/A)=6.8", "R(in)=6.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: tagMap(req, "R:"),
        highlightPins: ["in"],
      },
      {
        id: "both-tags",
        title: "Keep both tags on every pin",
        caption:
          "Arrival and required live together. Slack at a pin is R − A for setup. Next labs turn those tags into slack and a critical path.",
        bullets: ["Forward then backward", "Same graph, two tag maps", "A(out)=3.2 and R(out)=10"],
        metrics: ["A(out)=3.2", "R(out)=10", "next: slack = 6.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: Object.fromEntries(
          Object.keys(arr).map((p) => [p, `A:${arr[p]} R:${req[p]}`])
        ),
        highlightPins: ["out"],
      },
    ],
  },

  "slack-setup-hold": {
    title: "Slack, setup, and hold",
    module: "module02-01-slack-setup-hold",
    kind: "sta",
    steps: [
      {
        id: "setup-formula",
        title: "Setup slack is required minus arrival",
        caption:
          "At the endpoint out, setup slack equals R − A. With R=10 and A=3.2, slack is 6.8—positive means the path meets the single-cycle check.",
        bullets: ["setup_slack = R − A", "Positive → meets setup", "Golden at out: 6.8"],
        metrics: ["R(out)=10", "A(out)=3.2", "setup slack=6.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: { out: "S:6.8" },
        highlightPins: ["out"],
      },
      {
        id: "hold-formula",
        title: "Hold slack uses a different required",
        caption:
          "For this lite hold model, required at out is 0 on the same edge. Hold slack is A − R_hold = 3.2 − 0 = 3.2.",
        bullets: ["hold_slack = A − R_hold", "Do not reuse setup required", "Golden hold at out: 3.2"],
        metrics: ["R_hold(out)=0", "A(out)=3.2", "hold slack=3.2"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: { out: "H:3.2" },
        highlightPins: ["out"],
      },
      {
        id: "sign-matters",
        title: "The sign tells you pass or fail",
        caption:
          "Negative setup slack means the path is too slow for the period. Negative hold means data changes too soon. Read the sign before you chase the path.",
        bullets: ["Setup fail → slow path", "Hold fail → fast path / race", "Both can be true on different checks"],
        metrics: ["setup +6.8 (pass)", "hold +3.2 (pass)"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
      {
        id: "endpoint-habit",
        title: "Report slack at endpoints first",
        caption:
          "Engineers scan worst negative slack at endpoints, then open the path. On this toy netlist there is one sink—out—so both checks live there.",
        bullets: ["Endpoints first", "Then open the path", "One sink keeps the lesson clear"],
        metrics: ["sink: out", "checks: setup + hold"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
      {
        id: "period-knob",
        title: "Period changes setup, not hold lite",
        caption:
          "If the period were tighter, setup required would drop and setup slack would shrink. Hold in this lite model stays tied to arrival versus zero.",
        bullets: ["Period feeds setup required", "Hold lite ignores period here", "Full STA hold uses more edges"],
        metrics: ["period=10 → R_setup=10", "hold R=0 (lite)"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
    ],
  },

  "critical-path": {
    title: "Critical path",
    module: "module02-03-critical-path",
    kind: "sta",
    steps: [
      {
        id: "worst-sink",
        title: "Start from the worst endpoint",
        caption:
          "Critical-path traceback begins at the endpoint with the worst setup slack. Here that is out with slack 6.8—still the only sink.",
        bullets: ["Pick the worst slack sink", "Trace into arrival tags", "Do not guess from the source"],
        metrics: ["sink: out", "setup slack: 6.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
        tags: { out: "S:6.8" },
      },
      {
        id: "match-pred",
        title: "Step to the matching predecessor",
        caption:
          "At each pin, choose a predecessor u where A(u) + delay equals A(v). That arc is on the critical path.",
        bullets: ["Match A(u)+d to A(v)", "Ties: prefer larger A(u)", "Walk until a source"],
        metrics: ["out ← u2/Y (+0.2)", "u2/Y ← u2/A (+1.5)"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out", "u2/Y", "u2/A"],
        highlightArcs: ["u2/Y|out", "u2/A|u2/Y"],
        tags: tagMap(arr, "A:"),
      },
      {
        id: "full-path",
        title: "The full golden path",
        caption:
          "The complete critical path is in → u1/A → u1/Y → u2/A → u2/Y → out. Arrival at out equals the sum of arc delays along this path: 3.2.",
        bullets: ["Six pins on one path", "Path delay = A(out)", "Golden list matches PROP_GOLDENS"],
        metrics: [path.join(" → "), "path delay = 3.2"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: path,
        highlightArcs: pathArcs,
        tags: tagMap(arr, "A:"),
      },
      {
        id: "why-it-matters",
        title: "Fix the path, not a random gate",
        caption:
          "Optimization and ECO work chase critical paths. Tag matching keeps you honest when reconvergence exists—on this chain there is only one route.",
        bullets: ["Trace before you resize", "Reconvergence needs care", "Toy chain has one route"],
        metrics: ["reconvergence: none", "cells on path: u1, u2"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["u1/Y", "u2/Y"],
        highlightArcs: ["u1/A|u1/Y", "u2/A|u2/Y"],
      },
      {
        id: "slack-path",
        title: "Slack and path travel together",
        caption:
          "Reports pair worst slack with its path. Next labs edit delays and exceptions—always re-trace after the tags change.",
        bullets: ["Slack names the problem", "Path names where to look", "Re-trace after edits"],
        metrics: ["slack 6.8 @ out", "path length 6"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: path,
        highlightArcs: pathArcs,
      },
    ],
  },

  "incremental-update": {
    title: "Incremental timing update",
    module: "module03-01-incremental-update",
    kind: "sta",
    steps: [
      {
        id: "base-tags",
        title: "Start from a full analysis",
        caption:
          "Base arrival at out is 3.2 with setup slack 6.8. Incremental update never starts from an empty graph—it starts from valid tags.",
        bullets: ["Full propagate first", "A(out)=3.2", "setup slack=6.8"],
        metrics: ["A(out)=3.2", "S(out)=6.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: tagMap(arr, "A:"),
        highlightPins: ["out"],
      },
      {
        id: "local-edit",
        title: "Edit one cell delay",
        caption:
          "Bump the u1 cell arc from 1.2 to 2.0. Only the fanout cone of u1/Y can change—everything upstream of the edit stays put.",
        bullets: ["Edit u1/A → u1/Y delay", "1.2 → 2.0", "Upstream tags stay"],
        metrics: ["edit arc: u1/A|u1/Y", "new delay: 2.0"],
        timing: cloneTiming(inc.timing),
        levels: levelize(inc.timing),
        highlightArcs: ["u1/A|u1/Y"],
        highlightPins: ["u1/Y"],
      },
      {
        id: "invalidate-cone",
        title: "Invalidate the fanout cone",
        caption:
          "Mark u1/Y, u2/A, u2/Y, and out dirty. Do not touch in or u1/A—their arrivals are still valid.",
        bullets: ["BFS successors from edit.to", "Delete dirty arrivals", "Keep clean tags"],
        metrics: ["invalidated: u1/Y, u2/A, u2/Y, out", "clean: in, u1/A"],
        timing: cloneTiming(inc.timing),
        levels: levelize(inc.timing),
        highlightPins: inc.invalidated,
      },
      {
        id: "recompute",
        title: "Recompute only the dirty pins",
        caption:
          "Replay topo order on dirty pins. Arrival at out becomes 4.0; setup slack drops to 6.0. Same answer as a full rebuild, less work.",
        bullets: ["Recompute dirty only", "A(out)=4.0", "setup slack=6.0"],
        metrics: ["A(out)=4.0", "S(out)=6.0", "ΔA = +0.8"],
        timing: cloneTiming(inc.timing),
        levels: levelize(inc.timing),
        tags: tagMap(inc.arrival, "A:"),
        highlightPins: ["out"],
      },
      {
        id: "why-incremental",
        title: "Why timers insist on incremental",
        caption:
          "Place, CTS, and ECO change tiny regions millions of times. Full-chip rebuilds every edit would not finish. Cone invalidate-and-repair is the habit.",
        bullets: ["Edits are local", "Cones stay small", "Correctness = same as full rebuild"],
        metrics: ["cone size: 4 pins", "full graph: 6 pins"],
        timing: cloneTiming(inc.timing),
        levels: levelize(inc.timing),
        highlightPins: inc.invalidated,
      },
    ],
  },

  "false-multicycle-lite": {
    title: "False and multicycle paths",
    module: "module03-03-false-multicycle-lite",
    kind: "sta",
    steps: [
      {
        id: "normal-check",
        title: "Normal single-cycle setup",
        caption:
          "Without exceptions, required at out is one period (10) and setup slack is 6.8. That is the baseline the exceptions will change.",
        bullets: ["cycles = 1", "R(out)=10", "slack=6.8"],
        metrics: ["setup slack=6.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: { out: "S:6.8" },
        highlightPins: ["out"],
      },
      {
        id: "multicycle",
        title: "Multicycle widens the required window",
        caption:
          "A setup multicycle of 2 means required = 2 × period = 20. Slack becomes 16.8. The graph did not change—only the endpoint budget did.",
        bullets: ["R = period × cycles", "cycles=2 → R=20", "slack=16.8"],
        metrics: ["required out=20", "setup slack=16.8"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        tags: { out: "R:20 S:16.8" },
        highlightPins: ["out"],
      },
      {
        id: "false-path",
        title: "False path disables an arc",
        caption:
          "Marking the bridge net u1/Y→u2/A as false removes it from propagation. Downstream pins no longer see the real wavefront—u2/A falls back to 0 in this lite engine.",
        bullets: ["Disable arc u1/Y|u2/A", "Propagation skips it", "Lite model: orphan pin → 0"],
        metrics: ["disabled: u1/Y|u2/A", "A(u1/Y)=1.2", "A(u2/A)=0"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightArcs: ["u1/Y|u2/A"],
        highlightPins: ["u1/Y", "u2/A"],
      },
      {
        id: "engine-data",
        title: "Exceptions are engine data",
        caption:
          "SDC authoring lives in learn_sdc. Here you only consume false-path and multicycle as flags the timer reads—same idea as production engines.",
        bullets: ["Constraints → engine inputs", "Not GUI click-paths", "Wrong exception → wrong slack"],
        metrics: ["false-path: remove arc", "multicycle: scale required"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
      {
        id: "recheck",
        title: "Always recheck after exceptions",
        caption:
          "Apply exceptions, then recompute tags and slack. Never keep a stale 6.8 after a multicycle or false-path change.",
        bullets: ["Apply → recompute → report", "Stale tags lie", "Next: offline compare habit"],
        metrics: ["normal 6.8", "multicycle 16.8", "false-path breaks the bridge"],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
    ],
  },
};

// silence unused in case tree-shaking worries
void setupSlack;
void PROP_GOLDENS;
