import {
  CONGESTED_SEED,
  PLACEMENT,
  rudyDemand,
  congestionMap,
  overflowMetrics,
  CAPACITY,
  placementFeedbackLite,
} from "../../assets/congestion-core.js";

const spread = PLACEMENT;
const seed = CONGESTED_SEED;

function step(id, title, caption, bullets, metrics, positions, extra = {}) {
  return { id, title, caption, bullets, metrics, positions, ...extra };
}

export const CONGESTION_ALGOS = {
  "gcell-grid": {
    title: "GCell grid",
    module: "module01-01-gcell-grid",
    kind: "congestion",
    steps: [
      step("chip", "Chip and GCells", "Twelve by eight chip with a four-by-two GCell overlay. Each tile is three by four.", ["Lower-left origin", "i = floor(x/3)", "j = floor(y/4)"], ["Grid: 4×2", "cellW=3 cellH=4"], spread),
      step("a00", "A lands in (0,0)", "Cell A at (1,1) indexes to GCell column 0, row 0.", ["Clamp to last tile on edges"], ["A → (0,0)"], spread, { highlight: ["A"] }),
      step("d21", "D lands in (2,1)", "D at (8,5) → i=2, j=1 (top row).", ["Top row is j=1"], ["D → (2,1)"], spread, { highlight: ["D"] }),
      step("paint", "Paint all centers", "Every cell maps to exactly one GCell; the grid is the router’s coarse map.", ["Used by every estimator"], ["8 tiles total"], spread),
      step("seed", "Clustered seed", "Congested seed piles cells into center tiles—later labs heat those GCells.", ["Same grid, hotter map"], ["Center columns"], seed),
    ],
  },
  "capacity-demand": {
    title: "Capacity vs demand",
    module: "module01-03-capacity-demand",
    kind: "congestion",
    steps: [
      step("cap", "Capacity budget", "Each GCell has capacity 2.0 on the toy instance.", ["Scalar Cap for goldens"], ["Cap=2"], seed),
      step("demand", "Demand arrives", "Estimators deposit demand into tiles; surplus = demand − Cap.", ["Positive surplus = overflow"], ["Compare per tile"], seed, { heatFrom: "rudy" }),
      step("flag", "Oversubscribed tiles", "Flag every tile with demand > Cap before trusting a heat map.", ["List hot tiles"], ["count ≥ 1 on seed"], seed),
      step("toggle", "Lower Cap", "At Cap=1 more tiles fail—capacity is part of the contract.", ["Document units"], ["Cap is a knob"], seed),
      step("spread", "Spread helps", "Moving cells outward reduces how many tiles exceed Cap.", ["Placement feeds congestion"], ["Toward quieter tiles"], spread),
    ],
  },
  "rudy-estimate": {
    title: "RUDY estimate",
    module: "module02-01-rudy-estimate",
    kind: "congestion",
    steps: [
      step("bbox", "Net bounding box", "RUDY starts from each net’s axis-aligned pin bbox and HPWL.", ["HPWL = width+height"], ["6 nets"], seed),
      step("share", "Uniform share", "Density = HPWL / #overlapping GCells; add to each overlapping tile.", ["At least one tile"], ["Deterministic"], seed),
      step("sum", "Sum over nets", "Demand is the sum across nets—center tiles collect many contributions on a cluster.", ["Matrix 4×2"], ["Seed max ov ≈ 5"], seed),
      step("overflow", "Overflow appears", "ov = max(0, demand−Cap). Seed shows a clear hotspot.", ["total/max/count"], ["Cap=2"], seed),
      step("spread", "Spread cools total pattern", "Long nets paint many tiles; cluster spikes max. Both are useful views.", ["Compare seeds"], ["Use max for hotspots"], spread),
    ],
  },
  "probabilistic-demand": {
    title: "Probabilistic demand",
    module: "module02-03-probabilistic-demand",
    kind: "congestion",
    steps: [
      step("lshape", "L-shape idea", "Two-pin nets route on L-shapes with half probability each bend.", ["H-then-V and V-then-H"], ["Corridors not filled boxes"], seed),
      step("deposit", "Deposit along legs", "Walk GCells on each leg and share demand along the path.", ["Corner may be shared"], ["Document scaling"], seed),
      step("multi", "Multi-pin star", "Star from bbox center to each pin; deposit like two-pin edges.", ["Toy multi-pin"], ["Same Cap"], seed),
      step("compare", "Versus RUDY", "Probabilistic concentrates on corridors; RUDY paints the bbox.", ["Totals may differ"], ["Both teach overflow"], seed),
      step("cool", "Spread again", "Spreading still reduces probabilistic overflow—feedback is placement.", ["Same push ideas"], ["Next: heat map"], spread),
    ],
  },
  "congestion-map": {
    title: "Congestion map",
    module: "module02-05-congestion-map",
    kind: "congestion",
    steps: [
      step("ratio", "Demand / Cap", "Congestion is a ratio per GCell—values above one are oversubscribed.", ["Heat = ratio"], ["Cap=2"], seed),
      step("hot", "Hottest tile", "Argmax over the matrix with fixed scan order for stable goldens.", ["Name (i,j)"], ["Center on seed"], seed),
      step("legend", "Read the colors", "Hotter colors mean higher congestion; use metrics for exact floats.", ["Don’t eyeball only"], ["Regression uses numbers"], seed),
      step("move", "Move the hotspot", "Dragging cells can move which tile is hottest.", ["Learner state"], ["Challenges score positions"], seed),
      step("spread", "Cooler map", "Spread placement lowers peak ratios.", ["Toward routing"], ["Overflow lab next"], spread),
    ],
  },
  "overflow-metrics": {
    title: "Overflow metrics",
    module: "module02-07-overflow-metrics",
    kind: "congestion",
    steps: [
      step("def", "Define overflow", "ov = max(0, demand−Cap) per tile.", ["Never negative"], ["Cap=2"], seed),
      step("total", "Total overflow", "Sum of per-tile overflow—primary regression number.", ["Seed total = 5"], ["Spread total higher but flatter"], seed),
      step("max", "Max overflow", "Worst tile—catches hotspots even when total is moderate.", ["Seed max = 5"], ["Hotspot detector"], seed),
      step("count", "Congested count", "How many tiles overflow—useful for “how widespread”.", ["count on seed = 1"], ["Triple report"], seed),
      step("target", "Hit a target", "Move cells until total/max/count clear challenge thresholds.", ["Check scores positions"], ["No reveal required"], spread),
    ],
  },
  "cell-inflator": {
    title: "Cell inflator",
    module: "module03-01-cell-inflator",
    kind: "congestion",
    steps: [
      step("idea", "Why inflate", "Make cells in hot GCells act larger so the next place pass spreads.", ["Width scale"], ["Coords unchanged here"], seed),
      step("rule", "Scale rule", "If cong>1: w' = w·(1+α(c−1)), α=0.5.", ["Else keep w"], ["Center cells grow"], seed),
      step("run", "Apply once", "Compute congestion from RUDY, then inflate widths once.", ["Don’t double-apply"], ["Reset to base widths"], seed),
      step("quiet", "Quiet tiles", "Cells in tiles with cong≤1 stay at base width.", ["Selective"], ["E may stay 1"], seed),
      step("link", "Link to place", "Widths feed the next placer—estimation alone is not enough.", ["Feedback course arc"], ["Net weights next"], spread),
    ],
  },
  "net-weighting": {
    title: "Net weighting",
    module: "module03-03-net-weighting",
    kind: "congestion",
    steps: [
      step("idea", "Weight hot nets", "Nets through congested GCells get larger weights for weighted place.", ["w=1+β·mean cong"], ["β=1 demo"], seed),
      step("bbox", "Mean under bbox", "Average congestion over GCells under the net bbox—not the whole chip.", ["Local mean"], ["6 nets"], seed),
      step("rank", "4-pin ranks high", "On a cluster, the 4-pin net outranks short E–F.", ["w4 ≥ w5"], ["Timing cousin"], seed),
      step("cool", "Spread lowers weights", "As congestion falls, weights ease back toward 1.", ["Coupled to map"], ["Still report overflow"], spread),
      step("use", "Use in placer", "Weighted HPWL pulls soft from hotspots—pair with inflators.", ["Two knobs"], ["Feedback lab next"], seed),
    ],
  },
  "placement-feedback": {
    title: "Placement feedback",
    module: "module04-01-placement-feedback",
    kind: "congestion",
    steps: [
      step("seed", "Hot starter", "Congested seed starts with total overflow 5 at Cap=2.", ["RUDY demand"], ["Need a loop"], seed),
      step("estimate", "Estimate", "Run RUDY → congestion → overflow per tile.", ["Same estimators"], ["Matrix in hand"], seed),
      step("push", "Push outward", "Cells in overflowing tiles step toward the quietest neighbor GCell.", ["Clamp to chip"], ["Toy one-pass"], seed),
      step("after", "Overflow drops", "After one feedback pass, total overflow falls (often to ~0 on this toy).", ["Remeasure demand"], ["Assert after < before"], placementFeedbackLite(seed)),
      step("next", "Toward routing", "Real flows iterate with global routing; next course deepens GCell edges.", ["learn_global_routing"], ["CTS also next"], spread),
    ],
  },
};
