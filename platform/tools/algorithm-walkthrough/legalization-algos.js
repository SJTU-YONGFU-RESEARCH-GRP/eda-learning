/**
 * Legalization algorithm walkthrough steps (5 each).
 * Consumed by algorithm-walkthrough/walkthrough.js.
 */
import {
  CHIP_W,
  FIXED_MACROS,
  FLOAT_PLACEMENT,
  GOLDEN_PLACEMENT,
  GOLDENS,
  N_ROWS,
  OVERLAP_PLACEMENT,
  ROW_YS,
  WIDTHS,
  abacusLegalize,
  clonePositions,
  detailedLegalize,
  globalLegalize,
  greedySnap,
  isLegal,
  legalizeCost,
  legalityReport,
  overlapRemoval,
  tetrisLegalize,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";

const overlap = clonePositions(OVERLAP_PLACEMENT);
const float = clonePositions(FLOAT_PLACEMENT);
const golden = clonePositions(GOLDEN_PLACEMENT);

const floatSnapped = greedySnap(float);
const overlapSnapped = greedySnap(overlap);
const overlapRemoved = overlapRemoval(overlap);
const abacus = abacusLegalize(overlap);
const abacusFixed = abacusLegalize(overlap, { fixed: FIXED_MACROS });
const tetris = tetrisLegalize(overlap);
const globalResult = globalLegalize(overlap);
const detailedResult = detailedLegalize(overlap);

const overlapReport = legalityReport(overlap);
const goldenReport = legalityReport(golden);
const floatSnapReport = legalityReport(floatSnapped);

/** @typedef {{ id: string, title: string, caption: string, bullets: string[], metrics?: string[], positions?: object|null, highlight?: string[] }} LegStep */

/** @type {Record<string, { title: string, module: string, kind: 'legalization', steps: LegStep[] }>} */
export const LEGALIZATION_ALGOS = {
  "site-row-model": {
    title: "Site & row model",
    module: "module01-01-site-row-model",
    kind: "legalization",
    steps: [
      {
        id: "empty-chip",
        title: "Twelve-by-six chip, three rows",
        caption:
          "Legalization lives on a discrete canvas: chip width twelve sites, height six (three rows of height two). Row bottoms sit at y equals zero, two, and four. Every movable cell must land on a row and align to site pitch one.",
        bullets: [
          "CHIP_W = 12 · CHIP_H = 6",
          "Row bottoms: y = 0, 2, 4",
          "Lower-left origin for cell coordinates",
        ],
        metrics: [
          `chip: ${GOLDENS.chipW}×${GOLDENS.chipH}`,
          `rows: ${GOLDENS.nRows}`,
          `rowH: ${GOLDENS.rowH}`,
        ],
        positions: {},
      },
      {
        id: "cell-widths",
        title: "Cell widths A–D = 2, E–F = 1",
        caption:
          "Six cells A through F occupy ten sites total—two sites each for A–D and one each for E and F. Width drives how many consecutive sites a rectangle spans when you pack a row.",
        bullets: [
          "Widths are integers in site units",
          "Total width 10 ≤ chip 12",
          "Same six-cell toy across all labs",
        ],
        metrics: [
          "A–D width: 2",
          "E–F width: 1",
          `total width: ${GOLDENS.totalCellWidth}`,
        ],
        positions: golden,
        highlight: ["A", "B", "C", "D", "E", "F"],
      },
      {
        id: "site-pitch",
        title: "Site pitch equals one",
        caption:
          "Each vertical tick is one site. Legal x coordinates are integers; a width-two cell at x equals four covers sites four and five on its row. The golden packing shows legal site alignment.",
        bullets: [
          "SITE_W = 1",
          "x must be integer-aligned",
          "Row lines dashed at y = 0, 2, 4",
        ],
        metrics: [`site pitch: ${GOLDENS.siteW}`, `rows: ${ROW_YS.join(", ")}`],
        positions: golden,
      },
      {
        id: "golden-pack",
        title: "Golden legal packing",
        caption:
          "The reference legal layout spreads A and B on row zero, C on row one, and E plus D on row top. No overlap, every cell on-row and site-aligned—this is the teaching golden.",
        bullets: [
          "Row 0: A@0, B@2, F@10",
          "Row 2: C@0",
          "Row 4: E@0, D@8",
        ],
        metrics: [
          "legal: true",
          `HPWL: ${totalHpwl(golden)}`,
          "reason: ok",
        ],
        positions: golden,
      },
      {
        id: "overlap-contrast",
        title: "Contrast: illegal overlap stack",
        caption:
          "The overlap seed stacks A, B, and C at (4, 2) on the middle row—same width-two cells fighting for the same sites. Legality fails before you even discuss wirelength.",
        bullets: [
          "A,B,C @ (4,2) stacked",
          "First failure: overlap A/B",
          "Legalization must repair this",
        ],
        metrics: [
          "legal: false",
          `reason: ${overlapReport.reason}`,
          "Next: legality metrics",
        ],
        positions: overlap,
        highlight: ["A", "B", "C"],
      },
    ],
  },

  "legality-metrics": {
    title: "Legality metrics",
    module: "module01-03-legality-metrics",
    kind: "legalization",
    steps: [
      {
        id: "overlap-illegal",
        title: "Overlap seed is illegal",
        caption:
          "Starting from the overlap placement, the checker reports overlap A/B first—three cells share the middle row at x equals four. That single reason is enough to fail legality.",
        bullets: [
          "Pairwise overlap on same row",
          "First reason wins the report",
          "Golden overlapIllegal: true",
        ],
        metrics: [
          "legal: false",
          `reason: ${overlapReport.reason}`,
          `all reasons: ${overlapReport.reasons.length}`,
        ],
        positions: overlap,
        highlight: ["A", "B"],
      },
      {
        id: "checks",
        title: "Four legality checks",
        caption:
          "A legal placement must be on-row, site-aligned, inside the chip, and overlap-free. Fixed macros add a fifth check later—did the macro move off its lock?",
        bullets: [
          "On-row: y ∈ {0, 2, 4}",
          "Site-aligned: integer x",
          "In-chip: x + width ≤ 12",
          "No area overlap on a row",
        ],
        metrics: [
          `rows: ${N_ROWS}`,
          `chip width: ${CHIP_W}`,
          "edge-touch OK, area overlap not",
        ],
        positions: overlap,
      },
      {
        id: "golden-ok",
        title: "Golden placement passes",
        caption:
          "The golden reference satisfies every check: reason ok, legal true. Use it as the positive control when you unit-test your legality reporter.",
        bullets: [
          "All cells on valid rows",
          "Integer site coordinates",
          "No pairwise overlap",
        ],
        metrics: [
          "legal: true",
          `reason: ${goldenReport.reason}`,
          `goldenLegal: ${GOLDENS.goldenLegal}`,
        ],
        positions: golden,
      },
      {
        id: "displacement",
        title: "Displacement: L1 from origin",
        caption:
          "Displacement sums Manhattan distance per cell from a reference layout—here the overlap seed. Abacus later moves cells only four total units; overlap removal moves six.",
        bullets: [
          "L1: |Δx| + |Δy| per cell",
          "Sum over all movables",
          "Lower is closer to global place",
        ],
        metrics: [
          `overlap-removal disp: ${GOLDENS.overlapRemovalDisp}`,
          `abacus disp: ${GOLDENS.abacusDisp}`,
          "Report after legalize",
        ],
        positions: abacus,
      },
      {
        id: "hpwl-after",
        title: "HPWL after legalize",
        caption:
          "Wirelength still matters: Abacus lands at HPWL thirty-eight with displacement four; Tetris-style packing hits HPWL thirty-two with displacement six. Always pair legality with both metrics.",
        bullets: [
          "Same nets as placement course",
          "Cell centers for HPWL bbox",
          "Legal ≠ optimal HPWL",
        ],
        metrics: [
          `abacus HPWL: ${GOLDENS.abacusHpwl}`,
          `tetris HPWL: ${GOLDENS.tetrisHpwl}`,
          `abacus disp: ${GOLDENS.abacusDisp}`,
        ],
        positions: abacus,
      },
    ],
  },

  "greedy-snap": {
    title: "Greedy snap",
    module: "module02-01-greedy-snap",
    kind: "legalization",
    steps: [
      {
        id: "float-seed",
        title: "Float placement from global place",
        caption:
          "After global placement, cells sit at fractional coordinates—A near (3.7, 1.2), B near (4.1, 1.4). Nothing is site-aligned yet; that is the float seed for greedy snap.",
        bullets: [
          "Fractional x and y",
          "Middle row target for A–C",
          "D, E, F also float",
        ],
        metrics: ["starter: FLOAT_PLACEMENT", "legal before snap: false"],
        positions: float,
      },
      {
        id: "snap-all",
        title: "Snap every cell to nearest site",
        caption:
          "Greedy snap rounds x to the nearest site and y to the nearest row. A lands at (4, 2)—same as B. C snaps to (5, 2). D, E, and F snap to their row neighbors.",
        bullets: [
          "snapX with cell width clamp",
          "snapY to nearest ROW_YS",
          "No overlap repair yet",
        ],
        metrics: [
          "A → (4, 2)",
          "B → (4, 2)",
          "C → (5, 2)",
        ],
        positions: floatSnapped,
        highlight: ["A", "B", "C"],
      },
      {
        id: "still-overlap",
        title: "Still illegal: A/B overlap",
        caption:
          "After snap, A and B still share (4, 2). The legality report again says overlap A/B. Snap alone does not legalize—it only quantizes coordinates.",
        bullets: [
          "floatSnapLegal: false",
          "Same failure as overlap seed",
          "C nearby but not stacked",
        ],
        metrics: [
          "legal: false",
          `reason: ${floatSnapReport.reason}`,
          "A,B @ (4,2)",
        ],
        positions: floatSnapped,
        highlight: ["A", "B"],
      },
      {
        id: "snap-not-legal",
        title: "Teaching point: snap ≠ legal",
        caption:
          "Students often assume rounding fixes everything. On this instance greedy snap creates the same middle-row pile as the integer overlap seed. Legalization needs a second phase.",
        bullets: [
          "Snap is necessary, not sufficient",
          "Check legality after snap",
          "Next: overlap removal or Abacus",
        ],
        metrics: ["greedy snap only", "overlap remains"],
        positions: floatSnapped,
        highlight: ["A", "B", "C"],
      },
      {
        id: "next-phase",
        title: "Next: overlap removal / Abacus",
        caption:
          "Follow snap with per-row packing or Abacus row assignment. Overlap removal spreads A, B, C along row two; Abacus spreads them across rows with lower displacement.",
        bullets: [
          "overlap-removal: disp 6",
          "abacus: disp 4",
          "Both start from overlap or float snap",
        ],
        metrics: [
          `overlapRemovalDisp: ${GOLDENS.overlapRemovalDisp}`,
          `abacusDisp: ${GOLDENS.abacusDisp}`,
        ],
        positions: overlapRemoved,
      },
    ],
  },

  "overlap-removal": {
    title: "Overlap removal",
    module: "module02-03-overlap-removal",
    kind: "legalization",
    steps: [
      {
        id: "overlap-seed",
        title: "A, B, C stacked at (4, 2)",
        caption:
          "The overlap seed piles three width-two cells on the middle row at x equals four. Greedy snap would leave the same conflict—overlap removal snaps first, then packs each row left-to-right.",
        bullets: [
          "A,B,C @ (4,2)",
          "illegal: overlap A/B",
          "D@8,4 · E@0,4 · F@10,0",
        ],
        metrics: ["legal: false", `reason: ${overlapReport.reason}`],
        positions: overlap,
        highlight: ["A", "B", "C"],
      },
      {
        id: "after-snap",
        title: "After snap: still stacked",
        caption:
          "Snapping the overlap seed does not separate A, B, and C—they remain on (4, 2). Overlap removal keeps their row assignment and resolves x conflicts by packing.",
        bullets: [
          "Snap preserves row intent",
          "Overlap is an x problem on-row",
          "Pack by increasing x order",
        ],
        metrics: ["snap legal: false", "middle row crowded"],
        positions: overlapSnapped,
        highlight: ["A", "B", "C"],
      },
      {
        id: "row-pack",
        title: "Per-row pack: A@4, B@6, C@8",
        caption:
          "On row y equals two, sort by x and place left without overlap: A at four, B at six, C at eight. Each width-two cell occupies two consecutive sites—now legal on that row.",
        bullets: [
          "Preserve sort order from snap",
          "Left pack within row",
          "No cross-row moves",
        ],
        metrics: [
          "A @ (4,2)",
          "B @ (6,2)",
          "C @ (8,2)",
        ],
        positions: overlapRemoved,
        highlight: ["A", "B", "C"],
      },
      {
        id: "legal-metrics",
        title: "Legal: disp 6, HPWL 32",
        caption:
          "Full overlap removal on the seed is legal with total displacement six and HPWL thirty-two. D, E, and F never moved from their overlap-seed roles.",
        bullets: [
          "legal: true",
          "L1 disp from overlap origin",
          "Report HPWL with same nets",
        ],
        metrics: [
          `disp: ${GOLDENS.overlapRemovalDisp}`,
          `HPWL: ${GOLDENS.overlapRemovalHpwl}`,
          `measured disp: ${totalDisplacement(overlap, overlapRemoved)}`,
        ],
        positions: overlapRemoved,
      },
      {
        id: "unchanged",
        title: "D, E, F unchanged",
        caption:
          "Macro-sized D stays at (8, 4), E at (0, 4), F at (10, 0). Overlap removal only repacked the crowded middle row—fixed-looking cells on other rows are untouched.",
        bullets: [
          "D top row @ 8",
          "E top row @ 0",
          "F bottom row @ 10",
        ],
        metrics: ["movables repacked: A,B,C", "others held row"],
        positions: overlapRemoved,
        highlight: ["D", "E", "F"],
      },
    ],
  },

  "abacus-row-pack": {
    title: "Abacus row pack",
    module: "module02-05-abacus-row-pack",
    kind: "legalization",
    steps: [
      {
        id: "overlap-seed",
        title: "Start from overlap seed",
        caption:
          "Abacus-lite processes movables by increasing original x. From the same overlap seed as overlap removal, it tries each row and picks the placement with minimum L1 displacement.",
        bullets: [
          "Order: A, B, C, … by x",
          "Try every row for each cell",
          "Leftmost legal site on row",
        ],
        metrics: ["seed: OVERLAP_PLACEMENT", "legal: false"],
        positions: overlap,
        highlight: ["A", "B", "C"],
      },
      {
        id: "try-rows",
        title: "Process by x: try each row",
        caption:
          "Cell A tries rows zero, two, four—picks row two at x four (zero displacement). B chooses row zero at x four. C chooses row four at x four. Cross-row spread beats single-row pack.",
        bullets: [
          "Per-cell row trial",
          "Min L1 from origin",
          "Tie-break: smaller x",
        ],
        metrics: ["A → row 2", "B → row 0", "C → row 4"],
        positions: abacus,
        highlight: ["A", "B", "C"],
      },
      {
        id: "abacus-result",
        title: "Result: A@4,2 B@4,0 C@4,4",
        caption:
          "Final Abacus layout: A on middle row, B on bottom, C on top—all at x equals four but on different rows. D, E, F stay at their seed coordinates.",
        bullets: [
          "A @ (4,2)",
          "B @ (4,0)",
          "C @ (4,4)",
        ],
        metrics: [
          `disp: ${GOLDENS.abacusDisp}`,
          `HPWL: ${GOLDENS.abacusHpwl}`,
          "legal: true",
        ],
        positions: abacus,
        highlight: ["A", "B", "C"],
      },
      {
        id: "vs-overlap-removal",
        title: "Lower displacement than Tetris",
        caption:
          "Abacus displacement is four versus six for overlap removal / Tetris on this seed. You pay three HPWL points—thirty-eight versus thirty-two—for staying closer to global targets.",
        bullets: [
          "abacus disp: 4",
          "tetris disp: 6",
          "HPWL tradeoff: 38 vs 32",
        ],
        metrics: [
          `abacusDisp: ${GOLDENS.abacusDisp}`,
          `tetrisDisp: ${GOLDENS.tetrisDisp}`,
          `abacusHpwl: ${GOLDENS.abacusHpwl}`,
        ],
        positions: abacus,
      },
      {
        id: "takeaway",
        title: "Abacus minimizes movement",
        caption:
          "Abacus is the detailed legalizer in this course: try rows, pick min displacement. Use it when staying near global coordinates matters more than the last HPWL point.",
        bullets: [
          "Cross-row assignment",
          "disp 4 golden",
          "Next: Tetris contrast",
        ],
        metrics: [`abacusLegal: ${GOLDENS.abacusLegal}`],
        positions: abacus,
      },
    ],
  },

  "tetris-row-pack": {
    title: "Tetris row pack",
    module: "module02-07-tetris-row-pack",
    kind: "legalization",
    steps: [
      {
        id: "overlap-seed",
        title: "Same overlap seed",
        caption:
          "Tetris-lite assigns each cell to its nearest row, then left-packs within the row—same engine as overlap removal. Start from the triple stack at (4, 2).",
        bullets: [
          "Nearest row from float y",
          "Per-row left pack",
          "No cross-row trial",
        ],
        metrics: ["seed: OVERLAP", "legal: false"],
        positions: overlap,
        highlight: ["A", "B", "C"],
      },
      {
        id: "nearest-row",
        title: "Nearest row, then left pack",
        caption:
          "A, B, and C stay on middle row two after snap. Sort by x and pack: A at four, B at six, C at eight—identical to overlap removal on this instance.",
        bullets: [
          "Row locked after snap",
          "Shelf pack left-to-right",
          "Simpler control flow",
        ],
        metrics: ["all on y=2", "pack order A,B,C"],
        positions: tetris,
        highlight: ["A", "B", "C"],
      },
      {
        id: "tetris-result",
        title: "Result: disp 6, HPWL 32",
        caption:
          "Tetris legalizes with displacement six and HPWL thirty-two—the overlap-removal golden. Same coordinates, same metrics: this is the global legalize path in later labs.",
        bullets: [
          "legal: true",
          "disp: 6",
          "HPWL: 32",
        ],
        metrics: [
          `disp: ${GOLDENS.tetrisDisp}`,
          `HPWL: ${GOLDENS.tetrisHpwl}`,
          `measured: ${totalDisplacement(overlap, tetris)}`,
        ],
        positions: tetris,
      },
      {
        id: "contrast-abacus",
        title: "Contrast Abacus disp 4",
        caption:
          "Abacus spreads A, B, C across three rows for displacement four. Tetris keeps them on one row and moves farther in x—six total L1 units.",
        bullets: [
          "Abacus: cross-row, disp 4",
          "Tetris: single row, disp 6",
          "HPWL favors Tetris here",
        ],
        metrics: [
          `abacusDisp: ${GOLDENS.abacusDisp}`,
          `tetrisDisp: ${GOLDENS.tetrisDisp}`,
          "Δ disp: 2",
        ],
        positions: tetris,
        highlight: ["A", "B", "C"],
      },
      {
        id: "tradeoff",
        title: "Tradeoff: simpler vs better displacement",
        caption:
          "Tetris is easier to implement and slightly better on HPWL for this toy. Abacus is the choice when displacement budget is tight—preview the detailed-vs-global lab.",
        bullets: [
          "Tetris = global legalize lite",
          "Abacus = detailed legalize lite",
          "Pick by disp vs HPWL budget",
        ],
        metrics: [
          `tetrisHpwl: ${GOLDENS.tetrisHpwl}`,
          `abacusHpwl: ${GOLDENS.abacusHpwl}`,
        ],
        positions: tetris,
      },
    ],
  },

  "fixed-macros": {
    title: "Fixed macros",
    module: "module03-01-fixed-macros",
    kind: "legalization",
    steps: [
      {
        id: "d-locked",
        title: "Macro D locked at (8, 4)",
        caption:
          "Cell D is a fixed macro at (8, 4) on the top row—width two covers sites eight and nine. Every legalizer must leave D untouched while packing movables around it.",
        bullets: [
          "FIXED_MACROS.D = (8,4)",
          "Width 2 blocks sites 8–9",
          "Movables: A,B,C,E,F",
        ],
        metrics: ["D fixed", "top row y=4"],
        positions: overlap,
        highlight: ["D"],
      },
      {
        id: "abacus-fixed",
        title: "Abacus with fixed macros",
        caption:
          "Run Abacus with the fixed map: D is placed first, occupied sites on row four block C from sliding into the macro. Movable cells trial rows respecting blocked intervals.",
        bullets: [
          "opts.fixed = FIXED_MACROS",
          "Blocked intervals per row",
          "Pack around macro footprint",
        ],
        metrics: ["engine: abacusLegalize", "fixed: D"],
        positions: abacusFixed,
        highlight: ["D"],
      },
      {
        id: "d-never-moves",
        title: "D never moves",
        caption:
          "After Abacus with fixed macros, D remains at (8, 4). Legality report includes a macro check—any drift off the lock fails the run.",
        bullets: [
          "D @ (8,4) before and after",
          "Macro legality enforced",
          "disp still 4 on overlap seed",
        ],
        metrics: [
          "D.x=8 D.y=4",
          `disp: ${GOLDENS.abacusDisp}`,
          "legal: true",
        ],
        positions: abacusFixed,
        highlight: ["D"],
      },
      {
        id: "still-legal",
        title: "Still legal, displacement 4",
        caption:
          "With D fixed, Abacus still legalizes A, B, C, E, and F with total displacement four—the same as the unconstrained Abacus run on this instance because D never moved in either.",
        bullets: [
          "Full legality: true",
          "No overlap with macro",
          "Movables avoid sites 8–9 on row 4",
        ],
        metrics: [
          `abacusDisp: ${GOLDENS.abacusDisp}`,
          `HPWL: ${GOLDENS.abacusHpwl}`,
          `legal: ${isLegal(abacusFixed, { fixed: FIXED_MACROS })}`,
        ],
        positions: abacusFixed,
      },
      {
        id: "avoid-macro",
        title: "Movables avoid macro sites",
        caption:
          "C lands on row four at x four—left of E at zero, right of the macro gap. Packing algorithms must treat fixed macros as obstacles, not soft preferences.",
        bullets: [
          "C @ (4,4) clears D",
          "E @ (0,4) on same row",
          "Never slide through macro",
        ],
        metrics: ["macro sites reserved", "row-4 pack around D"],
        positions: abacusFixed,
        highlight: ["A", "B", "C", "E", "F"],
      },
    ],
  },

  "displacement-hpwl": {
    title: "Displacement vs HPWL",
    module: "module03-03-displacement-hpwl",
    kind: "legalization",
    steps: [
      {
        id: "cost-formula",
        title: "Cost = HPWL + λ · displacement",
        caption:
          "Legalization objectives often combine wirelength with a displacement penalty from the pre-legalize layout. Lambda controls how hard you resist moving cells away from global placement.",
        bullets: [
          "cost = HPWL + λ·disp",
          "disp = L1 from origin",
          "Same nets as placement labs",
        ],
        metrics: ["λ tunable", "report both terms"],
        positions: overlap,
      },
      {
        id: "abacus-metrics",
        title: "Abacus vs overlap origin",
        caption:
          "Abacus on the overlap seed yields HPWL thirty-eight and displacement four versus the illegal starter. That is the Pareto point with lower movement.",
        bullets: [
          "origin: OVERLAP",
          "abacus legal",
          "HPWL 38 · disp 4",
        ],
        metrics: [
          `HPWL: ${GOLDENS.abacusHpwl}`,
          `disp: ${GOLDENS.abacusDisp}`,
          `HPWL overlap illegal: n/a`,
        ],
        positions: abacus,
      },
      {
        id: "lambda-1",
        title: "λ = 1 → cost 42",
        caption:
          "With lambda one, cost equals thirty-eight plus four equals forty-two. Displacement is cheap—one HPWL point buys one unit of movement in the objective.",
        bullets: [
          "38 + 1×4 = 42",
          "abacusCostLambda1 golden",
          "Compare to Tetris cost",
        ],
        metrics: [
          `λ=1 cost: ${GOLDENS.abacusCostLambda1}`,
          `measured: ${legalizeCost(abacus, overlap, 1)}`,
        ],
        positions: abacus,
      },
      {
        id: "lambda-5",
        title: "λ = 5 → cost 58",
        caption:
          "Raise lambda to five: cost becomes thirty-eight plus five times four equals fifty-eight. The same legal layout looks expensive when you punish displacement heavily.",
        bullets: [
          "38 + 5×4 = 58",
          "abacusCostLambda5 golden",
          "Higher λ favors staying put",
        ],
        metrics: [
          `λ=5 cost: ${GOLDENS.abacusCostLambda5}`,
          `measured: ${legalizeCost(abacus, overlap, 5)}`,
        ],
        positions: abacus,
      },
      {
        id: "lambda-tradeoff",
        title: "Higher λ favors staying put",
        caption:
          "When lambda is large, algorithms that minimize displacement—Abacus over Tetris—win the combined cost even if HPWL is slightly worse. Quote λ whenever you compare legalizers.",
        bullets: [
          "Low λ: wirelength dominates",
          "High λ: displacement dominates",
          "Tetris: lower HPWL, higher disp",
        ],
        metrics: [
          "abacus: HPWL 38 disp 4",
          "tetris: HPWL 32 disp 6",
          "λ=5 gap widens",
        ],
        positions: abacus,
      },
    ],
  },

  "detailed-vs-global": {
    title: "Detailed vs global legalize",
    module: "module04-01-detailed-vs-global",
    kind: "legalization",
    steps: [
      {
        id: "global-tetris",
        title: "Global = Tetris, disp 6",
        caption:
          "Global legalize lite maps to Tetris-style nearest-row shelf pack. On the overlap seed it legalizes with displacement six and HPWL thirty-two.",
        bullets: [
          "globalLegalize → tetris",
          "single-row shelf for A,B,C",
          "fast, simple pipeline stage",
        ],
        metrics: [
          `globalDisp: ${GOLDENS.globalDisp}`,
          `HPWL: ${GOLDENS.tetrisHpwl}`,
          "legal: true",
        ],
        positions: globalResult,
      },
      {
        id: "detailed-abacus",
        title: "Detailed = Abacus, disp 4",
        caption:
          "Detailed legalize lite maps to Abacus row trial. Same seed, both legal—but displacement drops to four by spreading A, B, C across rows.",
        bullets: [
          "detailedLegalize → abacus",
          "cross-row assignment",
          "lower L1 movement",
        ],
        metrics: [
          `detailedDisp: ${GOLDENS.detailedDisp}`,
          `HPWL: ${GOLDENS.abacusHpwl}`,
          "legal: true",
        ],
        positions: detailedResult,
      },
      {
        id: "both-legal",
        title: "Both pipelines legal",
        caption:
          "Global and detailed both pass legality on the overlap seed. The difference is how far cells move and how HPWL shifts—thirty-two versus thirty-eight here.",
        bullets: [
          "Same starter coordinates",
          "Both isLegal true",
          "Metrics tell the story",
        ],
        metrics: [
          "global legal: true",
          "detailed legal: true",
          "HPWL delta: 6",
        ],
        positions: detailedResult,
      },
      {
        id: "side-by-side",
        title: "Side-by-side metrics",
        caption:
          "Global Tetris: disp six, HPWL thirty-two. Detailed Abacus: disp four, HPWL thirty-eight. Neither dominates on both axes—pick by your displacement budget.",
        bullets: [
          "global: disp 6 HPWL 32",
          "detailed: disp 4 HPWL 38",
          "Report both in regressions",
        ],
        metrics: [
          `globalDisp: ${GOLDENS.globalDisp}`,
          `detailedDisp: ${GOLDENS.detailedDisp}`,
          `tetrisHpwl: ${GOLDENS.tetrisHpwl}`,
          `abacusHpwl: ${GOLDENS.abacusHpwl}`,
        ],
        positions: detailedResult,
      },
      {
        id: "pick-detailed",
        title: "Pick detailed when displacement is tight",
        caption:
          "Production flows often run a fast global legalize, then a detailed pass when timing or continuity needs cells near global targets. On this toy, that is Abacus over Tetris.",
        bullets: [
          "Tight disp budget → detailed",
          "HPWL-first → global Tetris",
          "Course wrap: offline compare next",
        ],
        metrics: [
          "detailedDisp: 4",
          "globalDisp: 6",
          "both legal on overlap seed",
        ],
        positions: detailedResult,
      },
    ],
  },
};

/** Algo ids that use drawLegalization. */
export const LEGALIZATION_ALGO_IDS = Object.keys(LEGALIZATION_ALGOS);
