/**
 * Floorplanning algorithm walkthrough steps (5 each).
 * Consumed by algorithm-walkthrough/walkthrough.js.
 */
import {
  BAD_PACK,
  GOLDEN_BSTAR,
  GOLDEN_PACK,
  GOLDEN_PINS,
  GOLDEN_POLISH,
  GOLDEN_SP,
  MACRO_PACK,
  OVERLAP_PACK,
  SOFT_A_PACK,
  clonePack,
  cost,
  deadspace,
  density,
  evalPolish,
  hpwl,
  isLegalPacking,
  legalityReport,
  packBstar,
  packHierarchical,
  packSequencePair,
} from "../../assets/floorplanning-core.js";

const polish = evalPolish(GOLDEN_POLISH);
const bstar = packBstar(GOLDEN_BSTAR);
const sp = packSequencePair(GOLDEN_SP.pos, GOLDEN_SP.neg);
const hier = packHierarchical();

/** @typedef {{ id: string, title: string, caption: string, bullets: string[], metrics?: string[], pack?: object|null, pins?: object[], empty?: boolean }} FpStep */

/** @type {Record<string, { title: string, module: string, kind: 'floorplan', steps: FpStep[] }>} */
export const FLOORPLAN_ALGOS = {
  "fixed-outline": {
    title: "Fixed outline",
    module: "module01-01-fixed-outline",
    kind: "floorplan",
    steps: [
      {
        id: "outline",
        title: "Fixed outline is 10×8",
        caption:
          "Modern floorplanning starts with a fixed outline. Ours is ten by eight—area eighty. Modules A through E must pack inside; growing the chip is not allowed.",
        bullets: [
          "Outline W×H = 10×8",
          "Lower-left coordinates",
          "Legality before wirelength",
        ],
        metrics: ["outline: 10×8", "outlineArea: 80", "modules: A–E"],
        pack: {},
        empty: true,
      },
      {
        id: "bad-overflow",
        title: "Bad pack: E overflows",
        caption:
          "The bad seed places E at x equals nine with width two, so it sticks past the right edge. Legality fails immediately—E is outside the outline.",
        bullets: [
          "E: x=9, w=2 → right edge 11",
          "Outline width is only 10",
          "Illegal before density matters",
        ],
        metrics: [
          "legal: false",
          "reason: E outside outline",
          `deadspace (areas): ${deadspace()}`,
        ],
        pack: clonePack(BAD_PACK),
      },
      {
        id: "overlap",
        title: "Overlap is also illegal",
        caption:
          "A second failure mode: E sits on top of C. Edge-touching is fine; positive-area interior overlap is not. The checker reports C overlaps E.",
        bullets: [
          "Interior overlap rejected",
          "Edge touching allowed",
          "Same outline, wrong packing",
        ],
        metrics: ["legal: false", "reason: C overlaps E"],
        pack: clonePack(OVERLAP_PACK),
      },
      {
        id: "golden",
        title: "Golden pack is legal",
        caption:
          "The golden packing keeps every block inside ten by eight with no overlaps. A sits at the origin; B, C, and E march right; D stacks above A.",
        bullets: [
          "A at (0,0), D above A",
          "B–C–E along the bottom",
          "legal: true, reason: ok",
        ],
        metrics: [
          "legal: true",
          "reason: ok",
          `report: ${legalityReport(GOLDEN_PACK).reason}`,
        ],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "takeaway",
        title: "Legality is the gate",
        caption:
          "Never optimize density or wirelength on an illegal packing. Fix containment and overlap first—then the metrics in the next lab mean something.",
        bullets: [
          "Containment + non-overlap",
          "Golden: legal inside 10×8",
          "Next: deadspace 57 on this instance",
        ],
        metrics: ["golden legal: true", "bad legal: false"],
        pack: clonePack(GOLDEN_PACK),
      },
    ],
  },

  "area-deadspace": {
    title: "Area & deadspace",
    module: "module01-03-area-deadspace",
    kind: "floorplan",
    steps: [
      {
        id: "areas",
        title: "Module areas sum to 23",
        caption:
          "Add the five module areas: A is six, B is six, C is four, D is three, E is four. That is twenty-three units of silicon that must fit in the outline.",
        bullets: ["A 3×2=6", "B 2×3=6", "C 2×2=4", "D 3×1=3", "E 2×2=4"],
        metrics: ["moduleAreaSum: 23"],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "outline-area",
        title: "Outline area is 80",
        caption:
          "Ten times eight is eighty. That is the budget. Module area twenty-three leaves whitespace—deadspace—equal to fifty-seven.",
        bullets: ["outlineArea = W×H = 80", "deadspace = 80 − 23 = 57"],
        metrics: ["outlineArea: 80", "deadspace: 57"],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "density",
        title: "Density is 0.2875",
        caption:
          "Density is module area over outline area: twenty-three over eighty equals zero point two eight seven five. Whitespace fraction is zero point seven one two five.",
        bullets: [
          "density = 23/80 = 0.2875",
          "whitespace = 57/80 = 0.7125",
          "Placement-independent for fixed sizes",
        ],
        metrics: [`density: ${density()}`, "whitespace: 0.7125"],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "legal-metrics",
        title: "Metrics need a legal pack",
        caption:
          "On the golden legal packing these numbers are honest. On an overflow packing the area math still computes, but the floorplan is invalid—do not celebrate density on illegal layouts.",
        bullets: [
          "Golden packing is legal",
          "Deadspace 57 is the teaching golden",
          "Illegal packs still report area math",
        ],
        metrics: [
          `legal: ${isLegalPacking(GOLDEN_PACK)}`,
          "deadspace: 57",
          "density: 0.2875",
        ],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "takeaway",
        title: "Report area trio every time",
        caption:
          "Habit: print module area, outline area, deadspace, and density with every packing. Representations later change geometry; this trio stays the scoreboard.",
        bullets: [
          "Always report 23 / 80 / 57 / 0.2875",
          "Density < 1 means whitespace remains",
          "Next: slicing polish that fits BB 9×3",
        ],
        metrics: ["golden: 23, 80, 57, 0.2875"],
        pack: clonePack(GOLDEN_PACK),
      },
    ],
  },

  "slicing-floorplan": {
    title: "Slicing floorplan",
    module: "module02-01-slicing-floorplan",
    kind: "floorplan",
    steps: [
      {
        id: "polish",
        title: "Polish expression encodes cuts",
        caption:
          "A slicing floorplan is a tree of through-cuts. Postfix polish A D H B V C V E V stacks A under D, then places B, C, and E to the right with vertical cuts.",
        bullets: [
          "Operands = modules",
          "H = horizontal cut (stack)",
          "V = vertical cut (side by side)",
        ],
        metrics: ["polish: A D H B V C V E V", "tokens: 9"],
        pack: {},
        empty: true,
      },
      {
        id: "stack-ad",
        title: "A D H stacks height 3",
        caption:
          "A is three by two; D is three by one. An H cut stacks D above A into a three by three block at the lower left.",
        bullets: ["A at (0,0)", "D at (0,2)", "composite 3×3"],
        metrics: ["after A D H: w=3 h=3"],
        pack: {
          A: { x: 0, y: 0, w: 3, h: 2 },
          D: { x: 0, y: 2, w: 3, h: 1 },
        },
      },
      {
        id: "attach-b",
        title: "V attaches B on the right",
        caption:
          "Next V places B beside the A–D stack. Bounding width becomes five; height stays three.",
        bullets: ["B at x=3", "BB width 5", "height still 3"],
        metrics: ["after … B V: w=5 h=3"],
        pack: {
          A: { x: 0, y: 0, w: 3, h: 2 },
          D: { x: 0, y: 2, w: 3, h: 1 },
          B: { x: 3, y: 0, w: 2, h: 3 },
        },
      },
      {
        id: "full",
        title: "Full polish packs BB 9×3",
        caption:
          "Adding C and E with more V cuts finishes the golden polish. Bounding box is nine by three—legal inside the ten-by-eight outline.",
        bullets: [
          "Final BB: 9×3",
          "Fits outline 10×8",
          "Five modules placed",
        ],
        metrics: [
          `bb: ${polish.w}×${polish.h}`,
          `legal: ${isLegalPacking(polish.pack)}`,
        ],
        pack: clonePack(polish.pack),
      },
      {
        id: "takeaway",
        title: "Slicing cannot make wheels",
        caption:
          "Not every packing is slicing. Wheel topologies need non-slicing codes like B-star or sequence pair—next labs. For slicing, polish plus H/V evaluation is enough.",
        bullets: [
          "Golden polish → BB 9×3",
          "legal: true",
          "Non-slicing needs other reps",
        ],
        metrics: ["starter golden: BB 9×3"],
        pack: clonePack(polish.pack),
      },
    ],
  },

  "bstar-tree": {
    title: "B*-tree",
    module: "module02-03-bstar-tree",
    kind: "floorplan",
    steps: [
      {
        id: "root",
        title: "Root A at the origin",
        caption:
          "B-star packing places the root at the lower left. A lands at zero comma zero with size three by two. Left children go right-of; right children go above via the contour.",
        bullets: [
          "Root = lower-left",
          "Left child = right-of parent",
          "Right child = above on contour",
        ],
        metrics: ["A at (0,0)", "tree root: A"],
        pack: { A: { x: 0, y: 0, w: 3, h: 2 } },
      },
      {
        id: "left-chain",
        title: "Left chain B→C→E",
        caption:
          "The left spine walks rightward: B at x equals three, then C, then E. Contour heights track the skyline so later modules sit tightly.",
        bullets: ["B.x = A.x + A.w = 3", "C and E continue right", "Contour updates each place"],
        metrics: ["B at (3,0)", "C at (5,0)", "E at (7,0)"],
        pack: {
          A: bstar.A,
          B: bstar.B,
          C: bstar.C,
          E: bstar.E,
        },
      },
      {
        id: "right-d",
        title: "Right child D above A",
        caption:
          "D is the right child of A, so it packs above A on the contour. Its y is at least two—A's height—keeping the tree geometry honest.",
        bullets: ["D.y >= A.h", "Same x as A branch", "Still non-overlapping"],
        metrics: [`D at (${bstar.D.x},${bstar.D.y})`, `A.h=${bstar.A.h}`],
        pack: clonePack(bstar),
      },
      {
        id: "legal",
        title: "Full B* pack is legal",
        caption:
          "All five modules are placed. The packing is legal inside ten by eight. Perturbing the tree—swap, rotate, move—will feed simulated annealing later.",
        bullets: [
          "Five modules placed",
          "legal: true",
          "Tree is a packing code, not netlist",
        ],
        metrics: [`legal: ${isLegalPacking(bstar)}`, "modules: A–E"],
        pack: clonePack(bstar),
      },
      {
        id: "takeaway",
        title: "B* is compact and mutable",
        caption:
          "B-star stores adjacency for packing, not connectivity. Get left and right semantics right, keep the contour correct, and you have a fast neighbor generator for search.",
        bullets: [
          "Left/right geometry is the bug magnet",
          "Contour must update on place",
          "Next: sequence-pair alternative",
        ],
        metrics: ["starter golden: legal B* pack"],
        pack: clonePack(bstar),
      },
    ],
  },

  "sequence-pair": {
    title: "Sequence pair",
    module: "module02-05-sequence-pair",
    kind: "floorplan",
    steps: [
      {
        id: "seqs",
        title: "Two permutations encode geometry",
        caption:
          "Sequence pair uses a positive and a negative permutation of the same modules. Ours are pos A B C E D and neg D A B C E—five ids each, same set.",
        bullets: [
          "pos + neg are permutations",
          "Same five module ids",
          "Constraints → longest-path pack",
        ],
        metrics: ["pos: A B C E D", "neg: D A B C E"],
        pack: {},
        empty: true,
      },
      {
        id: "h-rules",
        title: "Horizontal constraints set x",
        caption:
          "Module i is left of j when i appears before j in both sequences. Longest-path packing pushes each block as far left as those constraints allow.",
        bullets: [
          "i left of j if pos(i)<pos(j) and neg(i)<neg(j)",
          "x = longest path over left-of edges",
        ],
        metrics: ["A tends left", "E tends right"],
        pack: clonePack(sp),
      },
      {
        id: "v-rules",
        title: "Vertical constraints set y",
        caption:
          "Module i is below j when i precedes j in pos but follows in neg. That fills y coordinates without overlaps for a feasible pair.",
        bullets: [
          "i below j if pos(i)<pos(j) and neg(i)>neg(j)",
          "y = longest path over below edges",
        ],
        metrics: [`D.y=${sp.D.y}`, "D can sit above the bottom row"],
        pack: clonePack(sp),
      },
      {
        id: "legal",
        title: "Golden SP packs legally",
        caption:
          "Evaluating the golden sequences places all five modules with non-negative coordinates and a legal packing inside the outline.",
        bullets: [
          "Five modules placed",
          "legal: true",
          "Coords ≥ 0",
        ],
        metrics: [`legal: ${isLegalPacking(sp)}`, "ids: A–E"],
        pack: clonePack(sp),
      },
      {
        id: "takeaway",
        title: "SP neighbors are permutation moves",
        caption:
          "Annealing on sequence pair swaps or rotates entries in pos and neg. Feasibility stays geometric; cost can be deadspace plus wirelength.",
        bullets: [
          "Neighbor = edit permutations",
          "Pack via longest paths",
          "Next: SA search on packings",
        ],
        metrics: ["starter golden: legal SP"],
        pack: clonePack(sp),
      },
    ],
  },

  "simulated-annealing-fp": {
    title: "Simulated annealing FP",
    module: "module03-01-simulated-annealing-fp",
    kind: "floorplan",
    steps: [
      {
        id: "bad-cost",
        title: "Illegal packs pay 1000",
        caption:
          "Our toy cost adds one thousand when the packing is illegal. The bad overflow seed therefore sits at cost about one thousand forty-four—dominated by the penalty.",
        bullets: [
          "illegal → +1000",
          "Plus deadspace and HPWL terms",
          "Never accept illegal as “good”",
        ],
        metrics: [
          `cost(bad)≈${cost(BAD_PACK).toFixed(1)}`,
          `legal: ${isLegalPacking(BAD_PACK)}`,
        ],
        pack: clonePack(BAD_PACK),
      },
      {
        id: "golden-cost",
        title: "Golden cost stays under 1000",
        caption:
          "The golden legal packing drops below the penalty floor. Cost is about thirty-six—deadspace and a small HPWL proxy, no illegality tax.",
        bullets: [
          `cost(golden)≈${cost(GOLDEN_PACK).toFixed(1)}`,
          "legal: true",
          "Beats bad by ~1000",
        ],
        metrics: [
          `cost(golden)≈${cost(GOLDEN_PACK).toFixed(1)}`,
          `hpwl≈${hpwl(GOLDEN_PACK).toFixed(1)}`,
        ],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "neighbor",
        title: "Neighbors swap module positions",
        caption:
          "A simple SA move swaps the lower-left corners of two modules while keeping sizes. Accept improving moves; accept worsening ones with temperature probability.",
        bullets: [
          "saSwap(A,E) exchanges coordinates",
          "Sizes unchanged",
          "Re-check legality after the move",
        ],
        metrics: ["move: coordinate swap", "then rescore cost"],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "improve",
        title: "Improve: bad → golden",
        caption:
          "One teaching “improve” step replaces the illegal seed with the golden packing. Cost falls below one thousand and legality flips to true—exactly what a cooling schedule should prefer.",
        bullets: [
          "cost drops below 1000",
          "legal becomes true",
          "HPWL becomes finite and meaningful",
        ],
        metrics: [
          `before≈${cost(BAD_PACK).toFixed(1)}`,
          `after≈${cost(GOLDEN_PACK).toFixed(1)}`,
        ],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "takeaway",
        title: "SA needs a representation",
        caption:
          "Annealing is only as good as the move set. Pair it with polish, B-star, or sequence-pair edits—plus soft sizing and macros—in the labs that follow.",
        bullets: [
          "Penalty for illegal solutions",
          "Golden cost ≪ bad cost",
          "Representation defines neighbors",
        ],
        metrics: ["starter: improve to golden"],
        pack: clonePack(GOLDEN_PACK),
      },
    ],
  },

  "soft-module-sizing": {
    title: "Soft module sizing",
    module: "module03-03-soft-module-sizing",
    kind: "floorplan",
    steps: [
      {
        id: "soft-a",
        title: "A is soft with area 6",
        caption:
          "Module A is soft: area stays six, but aspect can move between one half and two. Hard modules B through E keep fixed shapes.",
        bullets: [
          "A soft: aspect_min 0.5, max 2",
          "Area A = 3×2 = 6",
          "B–E are hard",
        ],
        metrics: ["A: 3×2 area 6", "soft: true"],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "reshape",
        title: "Reshape A to 2×3",
        caption:
          "Reshape soft A to two by three—still area six. The soft packing moves neighbors so the outline stay legal.",
        bullets: ["2×3 = 6", "Aspect within [0.5, 2]", "Repack around A"],
        metrics: ["A: 2×3", "area: 6"],
        pack: clonePack(SOFT_A_PACK),
      },
      {
        id: "legal",
        title: "Soft packing stays legal",
        caption:
          "After reshape, the soft packing remains legal inside ten by eight. Softness is not a license to overflow—legality still gates acceptance.",
        bullets: [
          "legal: true",
          "Area preserved",
          "Hard blocks unchanged in size",
        ],
        metrics: [`legal: ${isLegalPacking(SOFT_A_PACK)}`],
        pack: clonePack(SOFT_A_PACK),
      },
      {
        id: "compare",
        title: "Hard vs soft views",
        caption:
          "Compare the hard three-by-two golden with the soft two-by-three packing. Same area budget for A; different whitespace shape.",
        bullets: [
          "Hard A: 3×2",
          "Soft A: 2×3",
          "Both legal teaching goldens",
        ],
        metrics: ["hard golden vs soft pack"],
        pack: clonePack(SOFT_A_PACK),
      },
      {
        id: "takeaway",
        title: "Softness is constrained freedom",
        caption:
          "Soft modules trade aspect for packing quality under area and aspect bounds. Always re-check legality after a resize.",
        bullets: [
          "Keep area ≈ constant",
          "Respect aspect_min/max",
          "Next: fixed macros",
        ],
        metrics: ["starter: A 3×2 → 2×3"],
        pack: clonePack(SOFT_A_PACK),
      },
    ],
  },

  "macro-placement": {
    title: "Macro placement",
    module: "module03-05-macro-placement",
    kind: "floorplan",
    steps: [
      {
        id: "free",
        title: "Free golden has movable D",
        caption:
          "In the free golden packing, D sits at zero comma two above A. Nothing is flagged as a hard macro yet.",
        bullets: ["D at (0,2)", "All blocks movable", "legal: true"],
        metrics: ["mode: free", "D@(0,2)"],
        pack: clonePack(GOLDEN_PACK),
      },
      {
        id: "fix-d",
        title: "Fix macro D at (0,0)",
        caption:
          "Macro mode pins hard block D at the origin and marks it macro true. Soft and standard cells must pack around that fixed rectangle.",
        bullets: [
          "D fixed at (0,0)",
          "D.macro = true",
          "Size stays 3×1",
        ],
        metrics: ["D@(0,0)", "macro: true"],
        pack: { D: MACRO_PACK.D },
      },
      {
        id: "pack-rest",
        title: "Pack A–E around the macro",
        caption:
          "A stacks above D; B, C, and E fill to the right. The macro packing differs from the free golden—D no longer sits at zero comma two.",
        bullets: [
          "A.y >= D.h",
          "Differs from free D position",
          "Five modules still present",
        ],
        metrics: [`A@(${MACRO_PACK.A.x},${MACRO_PACK.A.y})`, "legal check next"],
        pack: clonePack(MACRO_PACK),
      },
      {
        id: "legal",
        title: "Macro packing is legal",
        caption:
          "Despite the fixed block, the packing stays legal: no overflow, no overlaps. Fixed macros constrain search but do not excuse illegality.",
        bullets: ["legal: true", "D remains 3×1", "Macro flag preserved"],
        metrics: [`legal: ${isLegalPacking(MACRO_PACK)}`],
        pack: clonePack(MACRO_PACK),
      },
      {
        id: "takeaway",
        title: "Macros first, then cells",
        caption:
          "Industrial flows often place large macros before standard cells. Treat fixed rectangles as hard constraints, then optimize the rest.",
        bullets: [
          "Fix macros early",
          "Pack around them",
          "Next: hierarchical clusters",
        ],
        metrics: ["starter: D macro @ (0,0)"],
        pack: clonePack(MACRO_PACK),
      },
    ],
  },

  "hierarchical-floorplan": {
    title: "Hierarchical floorplan",
    module: "module04-01-hierarchical-floorplan",
    kind: "floorplan",
    steps: [
      {
        id: "clusters",
        title: "Two clusters: AB and CDE",
        caption:
          "Hierarchy packs locally first. Left cluster holds A and B; right cluster holds C, D, and E. Each cluster is a mini-floorplan.",
        bullets: ["Left: AB", "Right: CDE", "Pack then place clusters"],
        metrics: ["clusters: 2"],
        pack: {
          A: { x: 0, y: 0, w: 3, h: 2 },
          B: { x: 3, y: 0, w: 2, h: 3 },
        },
      },
      {
        id: "left",
        title: "Left cluster packs at x<5",
        caption:
          "AB occupies the left side with A at the origin and B at x equals three. Everything in this cluster stays left of x equals five.",
        bullets: ["A.x < 5", "B.x < 5", "Local packing done"],
        metrics: ["left max x+w ≤ 5"],
        pack: {
          A: hier.A,
          B: hier.B,
        },
      },
      {
        id: "right",
        title: "Right cluster offsets by 5",
        caption:
          "CDE packs in local coordinates, then shifts by five in x. C, D, and E all land at x greater than or equal to five—no cluster overlap.",
        bullets: ["offset x=5", "C.x ≥ 5", "E.x ≥ 5"],
        metrics: ["rightMin x ≥ 5"],
        pack: clonePack(hier),
      },
      {
        id: "legal",
        title: "Hierarchy is legal overall",
        caption:
          "Placing the two cluster bounding boxes yields a legal chip packing. Hierarchy scales: recurse inside clusters, then assemble.",
        bullets: [
          "Five modules placed",
          "legal: true",
          "Clusters separated in x",
        ],
        metrics: [`legal: ${isLegalPacking(hier)}`],
        pack: clonePack(hier),
      },
      {
        id: "takeaway",
        title: "Hierarchy reuses the same engines",
        caption:
          "Each level can use slicing, B-star, or SA. The teaching golden is simply AB left and CDE right at offset five.",
        bullets: [
          "Pack locally, place globally",
          "Same legality rules",
          "Next: pin assignment",
        ],
        metrics: ["starter: AB | CDE @x=5"],
        pack: clonePack(hier),
      },
    ],
  },

  "pin-assignment": {
    title: "Pin assignment",
    module: "module04-03-pin-assignment",
    kind: "floorplan",
    steps: [
      {
        id: "no-pins",
        title: "Packing without pins",
        caption:
          "Start from the golden packing with an empty pin list. Pins will sit on outline edges—not inside modules—for I/O literacy.",
        bullets: ["Golden pack shown", "pins: none", "Four sides available"],
        metrics: ["pins: 0", "valid: false (needs 4 sides)"],
        pack: clonePack(GOLDEN_PACK),
        pins: [],
      },
      {
        id: "assign",
        title: "Assign one pin per side",
        caption:
          "Golden pins place P0 on the left, P1 on the bottom, P2 on the right, and P3 on the top. Offsets stay inside each edge length.",
        bullets: [
          "P0 left @2",
          "P1 bottom @4",
          "P2 right @3",
          "P3 top @5",
        ],
        metrics: ["pins: 4", "sides: 4"],
        pack: clonePack(GOLDEN_PACK),
        pins: GOLDEN_PINS.map((p) => ({ ...p })),
      },
      {
        id: "valid",
        title: "Coverage makes pinsValid true",
        caption:
          "pinsValid requires every side to appear and offsets to lie on the edge. The golden set covers all four sides—valid returns true.",
        bullets: [
          "Four distinct sides",
          "Offsets in range",
          "valid: true",
        ],
        metrics: ["valid: true", "ids: P0–P3"],
        pack: clonePack(GOLDEN_PACK),
        pins: GOLDEN_PINS.map((p) => ({ ...p })),
      },
      {
        id: "empty-bad",
        title: "Empty set is invalid",
        caption:
          "Clear the pins and validity fails: you no longer cover four sides. Assignment is a first-class constraint, not decoration.",
        bullets: ["Empty → invalid", "Need four sides", "Order/offsets matter later"],
        metrics: ["pins: 0", "valid: false"],
        pack: clonePack(GOLDEN_PACK),
        pins: [],
      },
      {
        id: "takeaway",
        title: "Pins feed place and route",
        caption:
          "Boundary pins shape terminal propagation and routing demand. After floorplan shapes settle, pin assignment is the bridge to placement.",
        bullets: [
          "One pin per side in the toy",
          "valid covers left/right/top/bottom",
          "Next course: learn_placement",
        ],
        metrics: ["starter: P0–P3 on four sides"],
        pack: clonePack(GOLDEN_PACK),
        pins: GOLDEN_PINS.map((p) => ({ ...p })),
      },
    ],
  },
};
