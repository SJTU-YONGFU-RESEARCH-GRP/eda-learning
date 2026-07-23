import {
  GOLDENS,
  TINY_TIMING,
  arcKindCounts,
  cellDelaySum,
  levelize,
  near,
  pathDelaySum,
  sinks,
  sources,
} from "../../assets/sta-core.js";
import {
  createInteractiveStaLab,
  emptyLevels,
  levelsMatchGolden,
} from "../../assets/interactive-sta-lab.js";

const root = document.getElementById("lab-root");

createInteractiveStaLab(root, {
  mode: "levels",
  allowCycleToggle: true,
  revealLevels: GOLDENS.levels,
  starterHtml: `
    <p><strong>Your workspace:</strong> tiny chain <code>in → u1 → u2 → out</code>
    (${GOLDENS.pinCount} pins, ${GOLDENS.arcCount} arcs). Assign a level to each pin
    (Level +/−), or use <em>Run levelize</em>. Challenges check <strong>your</strong> levels.
    <em>Reveal golden (study)</em> is optional. Try <em>Add cycle edge</em> to see levelize fail.</p>
  `,
  challenges: [
    {
      id: "source-level-0",
      title: "Source at level 0",
      level: "Intro",
      prompt: "Assign level 0 to pin in (the only source).",
      hint: "Select in, Level + until 0, or Run levelize.",
      check: (_c, api) => api.getLevels().in === 0,
    },
    {
      id: "out-level-5",
      title: "Sink at level 5",
      level: "Intro",
      prompt: "Assign level 5 to out.",
      hint: "Chain depth is 5 arcs → out at L5.",
      check: (_c, api) => api.getLevels().out === GOLDENS.maxLevel,
    },
    {
      id: "all-levels",
      title: "Match golden levels",
      level: "Practice",
      prompt: "Assign levels matching the Kahn levelization of the chain.",
      hint: "in:0 … out:5, or Run levelize.",
      check: (_c, api) => levelsMatchGolden(api.getLevels()),
    },
    {
      id: "sources-sinks",
      title: "Source in / sink out",
      level: "Practice",
      prompt: "Confirm graph sources are [in] and sinks are [out] (always true on this netlist).",
      hint: "Metrics show pin/arc counts; Check verifies topology goldens.",
      check: (_c, api) => {
        const t = api.getTiming();
        return (
          sources(t).join(",") === GOLDENS.sources.join(",") &&
          sinks(t).join(",") === GOLDENS.sinks.join(",")
        );
      },
    },
    {
      id: "cell-net-split",
      title: "2 cell / 3 net arcs",
      level: "Practice",
      prompt: "Workspace has 2 cell arcs and 3 net arcs.",
      hint: "Solid = cell, dashed = net.",
      check: (_c, api) => {
        const k = arcKindCounts(api.getTiming());
        return k.cell === GOLDENS.cellArcs && k.net === GOLDENS.netArcs;
      },
    },
    {
      id: "path-delay",
      title: "Path delay 3.2",
      level: "Practice",
      prompt: "Sum of arc delays equals 3.2.",
      hint: "Read delay labels on arcs.",
      check: (_c, api) => near(pathDelaySum(api.getTiming()), GOLDENS.pathDelay),
    },
    {
      id: "cell-delay-sum",
      title: "Cell delay sum 2.7",
      level: "Practice",
      prompt: "Sum of cell-arc delays equals 2.7.",
      hint: "Only u1 and u2 cell arcs.",
      check: (_c, api) => near(cellDelaySum(api.getTiming()), GOLDENS.cellDelaySum),
    },
    {
      id: "levelize-ok",
      title: "Levelize succeeds",
      level: "Challenge",
      prompt: "On the acyclic chain, Run levelize (or assign by hand) so all levels are set.",
      hint: "Remove cycle edge if you added one.",
      check: (_c, api) => {
        const lv = api.getLevels();
        return levelsMatchGolden(lv) && levelize(api.getTiming()) != null;
      },
    },
    {
      id: "cycle-fails",
      title: "Cycle fails levelize",
      level: "Challenge",
      prompt: "Add the cycle edge; Run levelize — levels stay incomplete (levelize returns null).",
      hint: "Add cycle edge, then Run levelize.",
      check: (_c, api) => {
        const t = api.getTiming();
        return t.arcs.length > TINY_TIMING.arcs.length && levelize(t) == null;
      },
    },
    {
      id: "u1y-level-2",
      title: "u1/Y at level 2",
      level: "Challenge",
      prompt: "Pin u1/Y is at level 2.",
      hint: "in→u1/A→u1/Y.",
      check: (_c, api) => api.getLevels()["u1/Y"] === 2,
    },
  ],
  onChallengeSetup: (_ctx, api, ch) => {
    if (ch.id === "cycle-fails") {
      /* learner adds cycle */
      api.setLevels(emptyLevels(api.getTiming()));
    }
  },
});
