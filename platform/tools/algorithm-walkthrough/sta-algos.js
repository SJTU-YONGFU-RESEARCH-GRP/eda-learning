/**
 * STA algorithm walkthrough steps (timing-graph first).
 * Consumed by algorithm-walkthrough/walkthrough.js.
 */
import {
  GOLDENS,
  TINY_TIMING,
  cloneTiming,
  levelize,
  withCycle,
} from "../../assets/sta-core.js";

const levels = levelize(TINY_TIMING);

/** @typedef {{ id: string, title: string, caption: string, bullets: string[], metrics?: string[], timing?: object|null, levels?: object|null, highlightPins?: string[], highlightArcs?: string[], empty?: boolean }} StaStep */

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
          "A source has no incoming arc; a sink has no outgoing arc. On this chain, in is the only source and out is the only sink. Later arrival starts at sources; required starts at sinks.",
        bullets: [
          "Source = no predecessor arc",
          "Sink = no successor arc",
          "Registers will add more endpoints in later courses",
        ],
        metrics: [
          `sources: ${GOLDENS.sources.join(", ")}`,
          `sinks: ${GOLDENS.sinks.join(", ")}`,
        ],
        timing: cloneTiming(TINY_TIMING),
        levels: null,
        highlightPins: ["in", "out"],
      },
      {
        id: "levelize",
        title: "Levelize with Kahn's algorithm",
        caption:
          "Process pins with indegree zero, then peel successors. Each pin's level is one more than the max predecessor level. out lands at level 5 on this chain.",
        bullets: [
          "Queue pins with indegree 0",
          "level(v) = 1 + max(level of preds)",
          "If some pins never reach indegree 0, there is a cycle",
        ],
        metrics: [
          "in: L0",
          "u1/A: L1 · u1/Y: L2",
          "u2/A: L3 · u2/Y: L4",
          "out: L5",
        ],
        timing: cloneTiming(TINY_TIMING),
        levels,
        highlightPins: ["out"],
      },
      {
        id: "topo-delays",
        title: "Topo order and delay sums",
        caption:
          "Sorting pins by level gives the unique topo order on this DAG. Summing all arc delays gives path delay 3.2; cell arcs alone sum to 2.7. Those numbers are the lab goldens.",
        bullets: [
          "Topo order follows increasing level",
          "Path delay Σ = sum of every arc on the chain",
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
          "Add a back-edge from out to in and Kahn's algorithm stalls—some pins never reach indegree zero. Timing graphs for STA must be acyclic (or broken into acyclic timing windows).",
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
};
