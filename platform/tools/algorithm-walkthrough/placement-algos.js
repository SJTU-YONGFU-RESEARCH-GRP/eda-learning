/**
 * Placement algorithm walkthrough steps (5 each).
 * Consumed by algorithm-walkthrough/walkthrough.js.
 */
import {
  FIXED_PADS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  NET_WEIGHTS,
  OVERLAP_PLACEMENT,
  STARTER_PLACEMENT,
  analyticalPlace,
  cliqueHpwl,
  clonePositions,
  densityBins,
  forceDirectedPlace,
  hpwl,
  minPairDistance,
  quadraticPlace,
  round1,
  saPlace,
  spreadCells,
  timingWeightedHpwl,
  totalHpwl,
} from "../../assets/placement-core.js";

const starter = clonePositions(STARTER_PLACEMENT);
const golden = clonePositions(GOLDEN_PLACEMENT);
const overlap = clonePositions(OVERLAP_PLACEMENT);

const forceAfter = forceDirectedPlace(starter);
const forceMid = forceDirectedPlace(starter, { iters: 2 });
const quadAfter = quadraticPlace(starter);
const analAfter = analyticalPlace(starter);
const saResult = saPlace(starter);
const spreadAfter = spreadCells(overlap);

const densStarter = densityBins(starter, { capacity: 1 });
const densGolden1 = densityBins(golden, { capacity: 1 });
const densGolden2 = densityBins(golden, { capacity: 2 });

/** @typedef {{ id: string, title: string, caption: string, bullets: string[], metrics?: string[], positions?: object|null, highlightNets?: (string|number)[], highlightCells?: string[], grid?: number, showNets?: boolean, showBBox?: boolean }} PlaceStep */

/** @type {Record<string, { title: string, module: string, kind: 'placement', steps: PlaceStep[] }>} */
export const PLACEMENT_ALGOS = {
  "hpwl-metrics": {
    title: "HPWL metrics",
    module: "module01-01-hpwl-metrics",
    kind: "placement",
    steps: [
      {
        id: "starter-spread",
        title: "Starter placement is spread out",
        caption:
          "Six cells A–F sit on a rough eight-by-eight canvas. The spread-out seed pulls nets long: total half-perimeter wirelength is fifty-two. This is the shared starter for every placement lab.",
        bullets: [
          "Nodes = movable cells",
          "Dashed boxes = per-net bounding boxes",
          "HPWL = sum of (width + height) over nets",
        ],
        metrics: [
          `Total HPWL: ${GOLDENS.starterHpwl}`,
          "Nets: 6 (one 4-pin)",
          "Cells: A–F",
        ],
        positions: starter,
        highlightNets: [],
      },
      {
        id: "one-net",
        title: "One net: bbox width plus height",
        caption:
          "Net A–B alone has pins at (0,0) and (8,0). Width is eight, height is zero, so HPWL is eight. Every net uses the same bbox rule before you sum.",
        bullets: [
          "min/max x and y among pins",
          "HPWL(net) = (maxX−minX) + (maxY−minY)",
          "Two-pin nets reduce to Manhattan span",
        ],
        metrics: [
          `Net A–B HPWL: ${hpwl(NETS[0], starter)}`,
          `Net C–D HPWL: ${hpwl(NETS[1], starter)}`,
          `4-pin ABCD HPWL: ${hpwl(NETS[4], starter)}`,
        ],
        positions: starter,
        highlightNets: [0],
        highlightCells: ["A", "B"],
      },
      {
        id: "sum-nets",
        title: "Sum six nets to fifty-two",
        caption:
          "Four two-pin nets at eight each, the four-pin ABCD net at sixteen, and E–F at four: eight times four plus sixteen plus four equals fifty-two. That is the starter golden.",
        bullets: [
          "A–B, C–D, A–C, B–D: 8 each",
          "ABCD: 16 · E–F: 4",
          "Never celebrate collapse to one point",
        ],
        metrics: [
          "2-pin×4 = 32",
          "4-pin = 16",
          "E–F = 4",
          `Total = ${GOLDENS.starterHpwl}`,
        ],
        positions: starter,
        highlightNets: [0, 1, 2, 3, 4, 5],
      },
      {
        id: "golden-compact",
        title: "Golden placement drops to fourteen",
        caption:
          "The compact reference tucks A–D into a two-by-two block near the center. Same nets, shorter boxes: total HPWL falls from fifty-two to fourteen.",
        bullets: [
          "Same netlist, tighter coordinates",
          "ABCD bbox shrinks from 16 → 4",
          "Reference for later algorithms",
        ],
        metrics: [
          `Starter HPWL: ${GOLDENS.starterHpwl}`,
          `Golden HPWL: ${GOLDENS.goldenHpwl}`,
          `Delta: −${GOLDENS.starterHpwl - GOLDENS.goldenHpwl}`,
        ],
        positions: golden,
        highlightNets: [4],
      },
      {
        id: "takeaway",
        title: "HPWL is the teaching yardstick",
        caption:
          "Report total HPWL before and after every move. Fifty-two versus fourteen is the starter story—but a tiny total with stacked cells is not a usable placement.",
        bullets: [
          "Compute bbox HPWL per net, then sum",
          "Starter 52 · golden 14",
          "Next: clique and star models",
        ],
        metrics: [
          `starterHpwl: ${GOLDENS.starterHpwl}`,
          `goldenHpwl: ${GOLDENS.goldenHpwl}`,
        ],
        positions: golden,
      },
    ],
  },

  "net-models": {
    title: "Net models",
    module: "module01-03-net-models",
    kind: "placement",
    steps: [
      {
        id: "bbox-default",
        title: "Bbox HPWL is the default report",
        caption:
          "On the golden four-pin net A–B–C–D, the bounding box is two by two, so bbox HPWL is four. That is the cheap, standard teaching metric.",
        bullets: [
          "Bbox = half-perimeter of pin hull",
          "Cheap to compute",
          "Standard report across labs",
        ],
        metrics: [
          `ABCD bbox HPWL: ${hpwl(NETS[4], golden)}`,
          `Total golden HPWL: ${GOLDENS.goldenHpwl}`,
        ],
        positions: golden,
        highlightNets: [4],
        highlightCells: ["A", "B", "C", "D"],
      },
      {
        id: "clique-model",
        title: "Clique sums every pair",
        caption:
          "Clique wirelength adds HPWL of every pairwise edge among the four pins. On golden ABCD that sum is sixteen—four times the bbox number.",
        bullets: [
          "C(n,2) pairwise spans",
          "Overestimates multi-pin affinity",
          "Same pins, larger objective",
        ],
        metrics: [
          `clique(ABCD): ${GOLDENS.cliqueHpwlGolden4pin}`,
          `bbox(ABCD): ${hpwl(NETS[4], golden)}`,
          "Ratio: 4× on this instance",
        ],
        positions: golden,
        highlightNets: [4],
        highlightCells: ["A", "B", "C", "D"],
      },
      {
        id: "star-model",
        title: "Star depends on the hub",
        caption:
          "Star sums spokes from a hub to every other pin. With hub A on golden ABCD, star HPWL is eight—between bbox four and clique sixteen.",
        bullets: [
          "Pick a hub (here A)",
          "Sum HPWL(hub, other) for each pin",
          "Hub choice changes the number",
        ],
        metrics: [
          `star-from-A: ${GOLDENS.starHpwlGolden4pinFromA}`,
          `clique: ${cliqueHpwl(NETS[4], golden)}`,
          `bbox: ${hpwl(NETS[4], golden)}`,
        ],
        positions: golden,
        highlightNets: [4],
        highlightCells: ["A"],
      },
      {
        id: "compare-models",
        title: "Same pins, three numbers",
        caption:
          "Bbox four, star-from-A eight, clique sixteen. Pick one model for the reported objective and say which—mixing models is how goldens quietly disagree.",
        bullets: [
          "Bbox: cheap standard",
          "Star: hub-sensitive",
          "Clique: densest affinity",
        ],
        metrics: [
          "bbox = 4",
          "star-from-A = 8",
          "clique = 16",
        ],
        positions: golden,
        highlightNets: [4],
      },
      {
        id: "takeaway",
        title: "Name the model you optimize",
        caption:
          "Use one wirelength model in the objective and in the report. The rest of the course quotes bbox HPWL unless a lab explicitly asks for clique or star.",
        bullets: [
          "Default report = bbox HPWL",
          "Golden ABCD: 4 / 8 / 16",
          "Next: force-directed place",
        ],
        metrics: [
          `cliqueHpwlGolden4pin: ${GOLDENS.cliqueHpwlGolden4pin}`,
          `starHpwlGolden4pinFromA: ${GOLDENS.starHpwlGolden4pinFromA}`,
        ],
        positions: golden,
        highlightNets: [4],
      },
    ],
  },

  "force-directed-place": {
    title: "Force-directed place",
    module: "module02-01-force-directed-place",
    kind: "placement",
    steps: [
      {
        id: "starter",
        title: "Start from HPWL fifty-two",
        caption:
          "Force-directed place pulls free cells toward the average of their net neighbors, plus a weak center pull. Begin on the spread starter at HPWL fifty-two.",
        bullets: [
          "Spring pull along net edges",
          "Weak center attraction",
          "Small alpha avoids collapse",
        ],
        metrics: [`HPWL: ${GOLDENS.starterHpwl}`, "iters: 5 (default)", "alpha ≈ 0.12"],
        positions: starter,
      },
      {
        id: "mid-iters",
        title: "Neighbors pull cells inward",
        caption:
          "After a couple of lite iterations, A–D drift toward the center while E and F follow their neighbors. Wirelength is already dropping.",
        bullets: [
          "Each free cell → neighbor average",
          "Blend with small alpha",
          "Pads stay free in this lab",
        ],
        metrics: [
          `Mid HPWL: ${round1(totalHpwl(NETS, forceMid))}`,
          "Still above golden 14",
        ],
        positions: forceMid,
        highlightCells: ["A", "B", "C", "D"],
      },
      {
        id: "after-force",
        title: "After force: about eighteen point seven",
        caption:
          "Default five iterations land near eighteen point seven—clearly better than fifty-two, still above the compact golden fourteen.",
        bullets: [
          "Report before/after HPWL",
          "Force ≈ 18.7 on this seed",
          "Not a full legalizer",
        ],
        metrics: [
          `Before: ${GOLDENS.starterHpwl}`,
          `After: ${GOLDENS.forceHpwlAfter}`,
          `Measured: ${round1(totalHpwl(NETS, forceAfter))}`,
        ],
        positions: forceAfter,
      },
      {
        id: "vs-golden",
        title: "Force vs golden compact",
        caption:
          "Golden fourteen is tighter still. Force is a cheap continuous move—good teaching progress without claiming the absolute minimum.",
        bullets: [
          "Force ≈ 18.7",
          "Golden = 14",
          "Same nets, different tightness",
        ],
        metrics: [
          `forceHpwlAfter: ${GOLDENS.forceHpwlAfter}`,
          `goldenHpwl: ${GOLDENS.goldenHpwl}`,
        ],
        positions: golden,
        highlightNets: [4],
      },
      {
        id: "takeaway",
        title: "Alpha trades speed vs collapse",
        caption:
          "Too much alpha stacks cells; too little barely moves. Lock the iteration count and alpha so your eighteen point seven golden stays stable.",
        bullets: [
          "Neighbor average + center pull",
          "Starter 52 → ≈18.7",
          "Next: quadratic with fixed pads",
        ],
        metrics: [`forceHpwlAfter: ${GOLDENS.forceHpwlAfter}`],
        positions: forceAfter,
      },
    ],
  },

  "quadratic-place": {
    title: "Quadratic place",
    module: "module02-03-quadratic-place",
    kind: "placement",
    steps: [
      {
        id: "pads-fixed",
        title: "Pads A and D stay fixed",
        caption:
          "Quadratic-lite averages neighbors under fixed pads. Here A stays at (0,0) and D at (8,8)—anchors that free cells must respect.",
        bullets: [
          `Fixed pads: ${FIXED_PADS.join(", ")}`,
          "Gauss–Seidel neighbor average",
          "Blend retains some prior coord",
        ],
        metrics: [
          `HPWL: ${GOLDENS.starterHpwl}`,
          "A @ (0,0) · D @ (8,8)",
        ],
        positions: starter,
        highlightCells: FIXED_PADS,
      },
      {
        id: "free-cells",
        title: "Free cells slide toward neighbors",
        caption:
          "B, C, E, and F update toward the average of their neighbors while A and D hold. The system cannot collapse onto the pads.",
        bullets: [
          "Update only non-pad cells",
          "blend ≈ 0.55 toward average",
          "Pads raise HPWL vs free force",
        ],
        metrics: ["Free: B, C, E, F", "Fixed: A, D"],
        positions: starter,
        highlightCells: ["B", "C", "E", "F"],
      },
      {
        id: "after-quad",
        title: "After quadratic: HPWL forty-eight",
        caption:
          "Default iterations reach total HPWL forty-eight. Pads constrain the free cells, so you will not match free force’s eighteen point seven.",
        bullets: [
          "Starter 52 → 48",
          "Pads keep the spread",
          "Teaching point: constraints cost WL",
        ],
        metrics: [
          `Before: ${GOLDENS.starterHpwl}`,
          `After: ${GOLDENS.quadraticHpwlAfter}`,
          `Measured: ${round1(totalHpwl(NETS, quadAfter))}`,
        ],
        positions: quadAfter,
        highlightCells: FIXED_PADS,
      },
      {
        id: "vs-force",
        title: "Quadratic vs unconstrained force",
        caption:
          "Force without pads reaches about eighteen point seven; quadratic with pads stays at forty-eight. Same seed, different constraint story.",
        bullets: [
          "Force (free): ≈18.7",
          "Quadratic (pads): 48",
          "Both beat starter 52",
        ],
        metrics: [
          `forceHpwlAfter: ${GOLDENS.forceHpwlAfter}`,
          `quadraticHpwlAfter: ${GOLDENS.quadraticHpwlAfter}`,
        ],
        positions: quadAfter,
      },
      {
        id: "takeaway",
        title: "Pads anchor the solve",
        caption:
          "Always declare fixed cells. On this instance the quadratic golden is forty-eight—modest wirelength win, honest about pad constraints.",
        bullets: [
          "Fixed A, D",
          "Starter 52 → 48",
          "Next: analytical density stage",
        ],
        metrics: [`quadraticHpwlAfter: ${GOLDENS.quadraticHpwlAfter}`],
        positions: quadAfter,
        highlightCells: FIXED_PADS,
      },
    ],
  },

  "analytical-place": {
    title: "Analytical place",
    module: "module02-05-analytical-place",
    kind: "placement",
    steps: [
      {
        id: "wl-stage",
        title: "Wirelength stage clusters first",
        caption:
          "Analytical lite starts like force/quadratic: pull for wirelength with pads A and D fixed. Clustering cuts HPWL but can overload bins.",
        bullets: [
          "Force + quadratic wirelength stage",
          "Pads A, D fixed",
          "Clusters before spreading",
        ],
        metrics: [
          `Start HPWL: ${GOLDENS.starterHpwl}`,
          "Goal: cut WL without total collapse",
        ],
        positions: starter,
        highlightCells: FIXED_PADS,
        grid: 2,
      },
      {
        id: "density-stage",
        title: "Density stage pushes overloaded bins",
        caption:
          "A density-repulsion stage pushes cells out of crowded two-by-two bins, then a light reconnect keeps HPWL from exploding.",
        bullets: [
          "Count cells per bin",
          "Repel from crowded bin centers",
          "Light force reconnect afterward",
        ],
        metrics: ["2×2 density grid", "Watch HPWL and overflow together"],
        positions: forceAfter,
        grid: 2,
      },
      {
        id: "after-anal",
        title: "After analytical: about forty-eight point one",
        caption:
          "The combined solve lands near forty-eight point one—close to quadratic, deliberately above free force, because spreading fights pure collapse.",
        bullets: [
          "Starter 52 → ≈48.1",
          "Near quadratic, above force",
          "Density-aware, not full legalizer",
        ],
        metrics: [
          `analyticalHpwlAfter: ${GOLDENS.analyticalHpwlAfter}`,
          `Measured: ${round1(totalHpwl(NETS, analAfter))}`,
        ],
        positions: analAfter,
        highlightCells: FIXED_PADS,
        grid: 2,
      },
      {
        id: "both-metrics",
        title: "Report HPWL and overflow",
        caption:
          "Winning wirelength while overflowing every bin is not analytical success. Quote both metrics after the density stage.",
        bullets: [
          "HPWL ≈ 48.1",
          "Bin overflow still matters",
          "Pads remain fixed",
        ],
        metrics: [
          `HPWL: ${GOLDENS.analyticalHpwlAfter}`,
          `quadratic compare: ${GOLDENS.quadraticHpwlAfter}`,
        ],
        positions: analAfter,
        grid: 2,
      },
      {
        id: "takeaway",
        title: "Wirelength then density",
        caption:
          "Analytical lite is a two-act play: cluster for wirelength, spread for density. Lock pads and iteration knobs so forty-eight point one stays reproducible.",
        bullets: [
          "WL stage → density stage",
          "≈48.1 on this seed",
          "Next: simulated annealing",
        ],
        metrics: [`analyticalHpwlAfter: ${GOLDENS.analyticalHpwlAfter}`],
        positions: analAfter,
        grid: 2,
      },
    ],
  },

  "sa-placement": {
    title: "SA placement",
    module: "module02-07-sa-placement",
    kind: "placement",
    steps: [
      {
        id: "starter-sa",
        title: "Anneal from HPWL fifty-two",
        caption:
          "Simulated annealing jogs one cell at a time under an HPWL cost. Seed forty-two and sixty moves on the starter—deterministic teaching run.",
        bullets: [
          "Random axis jogs",
          "Cost = total HPWL",
          "seed = 42 · moves = 60",
        ],
        metrics: [
          `Start HPWL: ${GOLDENS.starterHpwl}`,
          "T0 ≈ 3 · cool ≈ 0.94",
        ],
        positions: starter,
      },
      {
        id: "accept-reject",
        title: "Accept improvements; maybe worsenings",
        caption:
          "Improvements always accept. Worsenings accept with probability exp(−Δ/T). Temperature cools each move so late stages get pickier.",
        bullets: [
          "Δ ≤ 0 → accept",
          "Else accept with e^(−Δ/T)",
          "Keep the best iterate",
        ],
        metrics: [
          `Accepted: ${GOLDENS.saAccepted}`,
          `Rejected: ${GOLDENS.saRejected}`,
        ],
        positions: starter,
        highlightCells: ["B"],
      },
      {
        id: "best-not-final",
        title: "Best HPWL near forty-nine point six",
        caption:
          "With seed forty-two the best HPWL lands near forty-nine point six—modest gain over fifty-two. Report best, not only the final temperature.",
        bullets: [
          "Best ≠ last iterate",
          "Modest SA gain on this tiny netlist",
          "Force still wins pure WL here",
        ],
        metrics: [
          `saHpwlAfter: ${GOLDENS.saHpwlAfter}`,
          `Measured best: ${round1(saResult.hpwl)}`,
          `accepted/rejected: ${saResult.accepted}/${saResult.rejected}`,
        ],
        positions: saResult.positions,
      },
      {
        id: "seed-lock",
        title: "Fix the seed for goldens",
        caption:
          "Change the seed and accept/reject counts drift. Teaching labs lock seed forty-two so forty-nine point six stays a stable challenge.",
        bullets: [
          "Deterministic PRNG (mulberry32)",
          "seed 42 → ≈49.6 best",
          "44 accept / 16 reject",
        ],
        metrics: [
          `saHpwlAfter: ${GOLDENS.saHpwlAfter}`,
          `saAccepted: ${GOLDENS.saAccepted}`,
          `saRejected: ${GOLDENS.saRejected}`,
        ],
        positions: saResult.positions,
      },
      {
        id: "takeaway",
        title: "SA is a stochastic local search",
        caption:
          "Propose, score, accept or reject, cool, and remember the best. On this instance expect about forty-nine point six—not a force-style collapse.",
        bullets: [
          "Best HPWL ≈ 49.6",
          "Lock seed 42",
          "Next: density bins",
        ],
        metrics: [`saHpwlAfter: ${GOLDENS.saHpwlAfter}`],
        positions: saResult.positions,
      },
    ],
  },

  "density-bins": {
    title: "Density bins",
    module: "module03-01-density-bins",
    kind: "placement",
    steps: [
      {
        id: "grid-idea",
        title: "Partition the die into bins",
        caption:
          "Density bins count cells on a regular grid. Default teaching grid is two-by-two over [0,8]×[0,8]. Capacity one means each bin may hold one cell before overflow.",
        bullets: [
          "Assign cell → bin by (x,y)",
          "overflow = Σ max(0, count − cap)",
          "Report with HPWL",
        ],
        metrics: ["Grid: 2×2", "Capacity: 1", "World: [0,8]²"],
        positions: starter,
        grid: 2,
        showNets: false,
      },
      {
        id: "starter-overflow",
        title: "Starter overflows by two",
        caption:
          "On the spread starter with capacity one, two bins hold two cells each. Overflow sums to two even though HPWL is already fifty-two.",
        bullets: [
          "Bottom-left and bottom-right busy",
          "overflow = 2 at cap 1",
          "Spread ≠ legal density",
        ],
        metrics: [
          `overflow: ${GOLDENS.density2x2Cap1StarterOverflow}`,
          `counts: ${JSON.stringify(densStarter.counts)}`,
          `HPWL: ${GOLDENS.starterHpwl}`,
        ],
        positions: starter,
        grid: 2,
        showNets: false,
      },
      {
        id: "golden-still-overflow",
        title: "Golden also overflows at cap one",
        caption:
          "Compact HPWL fourteen still piles three cells into one bin. Overflow remains two at capacity one—pretty wirelength is not automatic legality.",
        bullets: [
          "Golden HPWL = 14",
          "Same overflow 2 at cap 1",
          "Density is a separate objective",
        ],
        metrics: [
          `overflow: ${GOLDENS.density2x2Cap1GoldenOverflow}`,
          `counts: ${JSON.stringify(densGolden1.counts)}`,
          `HPWL: ${GOLDENS.goldenHpwl}`,
        ],
        positions: golden,
        grid: 2,
        showNets: false,
      },
      {
        id: "raise-capacity",
        title: "Raise capacity to ease overflow",
        caption:
          "With capacity two on the golden placement, overflow drops to one. Capacity is part of the spec—quote it with the overflow number.",
        bullets: [
          "cap 1 → overflow 2",
          "cap 2 → overflow 1",
          "Same coordinates, new budget",
        ],
        metrics: [
          `density2x2Cap2GoldenOverflow: ${GOLDENS.density2x2Cap2GoldenOverflow}`,
          `Measured: ${densGolden2.overflow}`,
        ],
        positions: golden,
        grid: 2,
        showNets: false,
      },
      {
        id: "takeaway",
        title: "HPWL and density travel together",
        caption:
          "Always report wirelength and bin overflow. A placement that wins HPWL while stacking bins fails the density half of the story.",
        bullets: [
          "Starter & golden: overflow 2 @ cap 1",
          "cap 2 golden: overflow 1",
          "Next: spread / legalize lite",
        ],
        metrics: [
          `starter overflow@1: ${GOLDENS.density2x2Cap1StarterOverflow}`,
          `golden overflow@1: ${GOLDENS.density2x2Cap1GoldenOverflow}`,
          `golden overflow@2: ${GOLDENS.density2x2Cap2GoldenOverflow}`,
        ],
        positions: golden,
        grid: 2,
      },
    ],
  },

  "spread-legalize-lite": {
    title: "Spread / legalize lite",
    module: "module03-03-spread-legalize-lite",
    kind: "placement",
    steps: [
      {
        id: "triple-overlap",
        title: "Triple overlap at one point",
        caption:
          "The overlap demo stacks A, B, and C on (4,4). Min pairwise distance is zero—illegal for any site-aware flow, perfect for a spreading lesson.",
        bullets: [
          "A,B,C @ (4,4)",
          "minPairDist = 0",
          "D,E,F already spread",
        ],
        metrics: [
          `minPairDist: ${round1(minPairDistance(overlap))}`,
          "Target minDist: 0.5",
        ],
        positions: overlap,
        highlightCells: ["A", "B", "C"],
        showNets: false,
      },
      {
        id: "push-apart",
        title: "Push near pairs apart",
        caption:
          "While any pair sits closer than minDist, push them along their separation vector. Repeated passes peel the triple stack into distinct points.",
        bullets: [
          "Push along separation vector",
          "strength controls step size",
          "Not full row-site legalization",
        ],
        metrics: ["minDist = 0.5", "iters ≈ 40 + repair"],
        positions: overlap,
        highlightCells: ["A", "B", "C"],
        showNets: false,
      },
      {
        id: "after-spread",
        title: "After spread: min distance holds",
        caption:
          "The lite spreader separates A, B, and C until every pair clears about zero point five. D, E, and F barely move.",
        bullets: [
          "minPairDist ≥ 0.5",
          "Deterministic repair pass",
          "HPWL may rise—that is expected",
        ],
        metrics: [
          `minPairDist: ${round1(minPairDistance(spreadAfter))}`,
          `spreadMinPairDist golden: ${GOLDENS.spreadMinPairDist}`,
        ],
        positions: spreadAfter,
        highlightCells: ["A", "B", "C"],
        showNets: false,
      },
      {
        id: "legality-proxy",
        title: "Spreading is a legality proxy",
        caption:
          "Clearing min distance is not row legalization or site snapping. It is a teaching stand-in so overlap stops hiding behind pretty HPWL.",
        bullets: [
          "Proxy ≠ detailed placement",
          "Still report HPWL after",
          "Use after analytical collapse",
        ],
        metrics: [
          `HPWL after spread: ${round1(totalHpwl(NETS, spreadAfter))}`,
          `minDist: ${GOLDENS.spreadMinPairDist}`,
        ],
        positions: spreadAfter,
        showNets: true,
      },
      {
        id: "takeaway",
        title: "Relieve overlap before celebrating WL",
        caption:
          "Start from the triple-overlap seed, spread to minDist zero point five, and confirm every pair clears the threshold. Then revisit wirelength.",
        bullets: [
          "Overlap seed → spread",
          "minDist 0.5 golden",
          "Next: timing-driven weights",
        ],
        metrics: [`spreadMinPairDist: ${GOLDENS.spreadMinPairDist}`],
        positions: spreadAfter,
        highlightCells: ["A", "B", "C"],
      },
    ],
  },

  "timing-driven-place": {
    title: "Timing-driven place",
    module: "module04-01-timing-driven-place",
    kind: "placement",
    steps: [
      {
        id: "plain-vs-weighted",
        title: "Plain HPWL hides critical nets",
        caption:
          "On the starter, plain HPWL is fifty-two, but timing-weighted HPWL is one hundred sixteen because the four-pin net carries weight five.",
        bullets: [
          "weights = [1,1,1,1,5,1]",
          "Net ABCD is critical",
          "Report both totals",
        ],
        metrics: [
          `Plain HPWL: ${GOLDENS.starterHpwl}`,
          `Timing HPWL: ${GOLDENS.starterTimingHpwl}`,
          `Net4 weight: ${NET_WEIGHTS[4]}`,
        ],
        positions: starter,
        highlightNets: [4],
      },
      {
        id: "weight-math",
        title: "Weighted sum of net HPWLs",
        caption:
          "Multiply each net’s bbox HPWL by its criticality and sum. The critical ABCD net alone contributes five times sixteen equals eighty on the starter.",
        bullets: [
          "Σ wᵢ · HPWL(netᵢ)",
          "Heavy nets pull harder",
          "Same coordinates, new objective",
        ],
        metrics: [
          `ABCD plain: ${hpwl(NETS[4], starter)}`,
          `ABCD weighted: ${NET_WEIGHTS[4] * hpwl(NETS[4], starter)}`,
          `Total timing: ${GOLDENS.starterTimingHpwl}`,
        ],
        positions: starter,
        highlightNets: [4],
        highlightCells: ["A", "B", "C", "D"],
      },
      {
        id: "golden-timing",
        title: "Golden timing cost drops to thirty",
        caption:
          "The compact golden cuts the critical bbox sharply. Timing-weighted HPWL falls from one hundred sixteen to thirty while plain HPWL hits fourteen.",
        bullets: [
          "Starter timing 116 → golden 30",
          "Plain golden still 14",
          "Critical net drove the win",
        ],
        metrics: [
          `goldenTimingHpwl: ${GOLDENS.goldenTimingHpwl}`,
          `goldenHpwl: ${GOLDENS.goldenHpwl}`,
          `Measured timing: ${timingWeightedHpwl(NETS, golden)}`,
        ],
        positions: golden,
        highlightNets: [4],
      },
      {
        id: "both-reports",
        title: "Always quote plain and weighted",
        caption:
          "A placement can look fine on plain HPWL while the critical net stays long. Timing labs demand both numbers so the objective is visible.",
        bullets: [
          "Plain: wirelength yardstick",
          "Weighted: timing objective",
          "Critical net highlighted",
        ],
        metrics: [
          `starter: ${GOLDENS.starterHpwl} / ${GOLDENS.starterTimingHpwl}`,
          `golden: ${GOLDENS.goldenHpwl} / ${GOLDENS.goldenTimingHpwl}`,
        ],
        positions: golden,
        highlightNets: [4],
      },
      {
        id: "takeaway",
        title: "Weights change what you optimize",
        caption:
          "Timing-driven place is still wirelength—just weighted. Remember one hundred sixteen to thirty on this instance, and never drop the plain HPWL report.",
        bullets: [
          "Critical net weight 5",
          "116 → 30 timing HPWL",
          "Course wrap: compare all engines",
        ],
        metrics: [
          `starterTimingHpwl: ${GOLDENS.starterTimingHpwl}`,
          `goldenTimingHpwl: ${GOLDENS.goldenTimingHpwl}`,
        ],
        positions: golden,
        highlightNets: [4],
      },
    ],
  },
};

/** Algo ids that use drawPlacement. */
export const PLACEMENT_ALGO_IDS = new Set(Object.keys(PLACEMENT_ALGOS));
