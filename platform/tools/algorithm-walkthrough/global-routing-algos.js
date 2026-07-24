import {
  PLACEMENT,
  CLUSTER_SEED,
  GOLDENS,
  lRoute,
  zRoute,
  routeAllL,
  routeAllMaze,
  usageFromRoutes,
  ripupReroute,
  terminalsFromPositions,
  NETS,
  EDGE_CAPACITY,
} from "../../assets/global-routing-core.js";

const spread = PLACEMENT;
const seed = CLUSTER_SEED;

function step(id, title, caption, bullets, metrics, positions, extra = {}) {
  return { id, title, caption, bullets, metrics, positions, ...extra };
}

function spreadRoutes(prefer = "HV") {
  const t = terminalsFromPositions(spread);
  return routeAllL(NETS, t, prefer);
}

export const GLOBAL_ROUTING_ALGOS = {
  "routing-graph": {
    title: "Routing graph",
    module: "module01-01-routing-graph",
    kind: "global-routing",
    steps: [
      step(
        "grid",
        "GCell graph",
        "Four-by-two GCells form a grid graph: nodes are tiles, edges are adjacency.",
        ["10 edges total", "Cap=2 per edge"],
        [`edges: ${GOLDENS.edgeCount}`],
        spread
      ),
      step(
        "h",
        "Horizontal edges",
        "Three horizontal edges per row connect columns i and i+1.",
        ["6 horizontal", "Same j"],
        ["Row bands"],
        spread
      ),
      step(
        "v",
        "Vertical edges",
        "Four vertical edges connect rows j and j+1.",
        ["4 vertical", "Same i"],
        ["Column risers"],
        spread
      ),
      step(
        "neigh",
        "Neighbors",
        "Interior GCell (1,0) has three neighbors; corners have two.",
        ["Degree depends on location", "B sits near mid-bottom"],
        [`mid neighbors=${GOLDENS.neighborCountMid}`],
        spread,
        { highlight: ["B"] }
      ),
      step(
        "cap",
        "Capacity",
        "Each edge tracks usage vs capacity—overflow drives rip-up.",
        ["Cap=2", "Document goldens"],
        ["Router contract"],
        spread
      ),
    ],
  },
  "terminal-gcells": {
    title: "Terminal GCells",
    module: "module01-03-terminal-gcells",
    kind: "global-routing",
    steps: [
      step(
        "map",
        "Pin → GCell",
        "Cell centers map to GCells with floor(x/cellW), floor(y/cellH).",
        ["Same as congestion grid", "i,j clamped"],
        ["Terminals move with cells"],
        spread
      ),
      step(
        "a00",
        "A → (0,0)",
        "Spread A at (1,1) lands in GCell (0,0).",
        ["Lower-left origin", "Clamp edges"],
        [`A → (${GOLDENS.aGcell[0]},${GOLDENS.aGcell[1]})`],
        spread,
        { highlight: ["A"] }
      ),
      step(
        "d21",
        "D → (2,1)",
        "D at (8,5) → (2,1) top row.",
        ["Top row j=1"],
        [`D → (${GOLDENS.dGcell[0]},${GOLDENS.dGcell[1]})`],
        spread,
        { highlight: ["D"] }
      ),
      step(
        "route",
        "Routes on graph",
        "Global routes walk GCell edges between terminal tiles.",
        ["Not bbox paint", "Edge usage"],
        ["L-HV overlay"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "cluster",
        "Cluster seed",
        "Tight cluster maps many pins to one GCell—zero-length routes.",
        ["Hot for study", "Spread for overflow"],
        ["Same grid"],
        seed
      ),
    ],
  },
  "pattern-l-route": {
    title: "L-pattern route",
    module: "module02-01-pattern-l-route",
    kind: "global-routing",
    steps: [
      step(
        "idea",
        "L-shape",
        "Two-pin nets use one bend: HV (horizontal first) or VH.",
        ["Manhattan", "One corner"],
        ["Pattern router"],
        spread
      ),
      step(
        "hv",
        "Route L-HV",
        "Spread placement L-HV yields documented overflow.",
        ["All six nets", "Shared corridors"],
        [`total≈${GOLDENS.spreadLhvTotalOv}`],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "vh",
        "Route L-VH",
        "Swapping bend order changes which edges saturate.",
        ["Same pins", "Different edges"],
        [`VH total≈${GOLDENS.spreadLvhTotalOv}`],
        spread,
        { routes: spreadRoutes("VH") }
      ),
      step(
        "edges",
        "Edge usage",
        "Thicker edges show usage; red dash marks overflow.",
        ["usage vs cap", "max/count"],
        ["Heat on edges"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "move",
        "Move pins",
        "Moving cells changes terminal GCells and L paths.",
        ["Learner state", "Check scores routes"],
        ["Browser lab next"],
        spread
      ),
    ],
  },
  "pattern-z-route": {
    title: "Z-pattern route",
    module: "module02-03-pattern-z-route",
    kind: "global-routing",
    steps: [
      step(
        "z",
        "Two bends",
        "Z-route uses a midpoint column (or row) with two corners.",
        ["vs one-bend L", "More edges possible"],
        ["Toy Z"],
        spread
      ),
      step(
        "ab",
        "A–D Z path",
        "On spread, Z from A to D shows the mid-column bend.",
        ["Compare to L", "Same pins"],
        ["Highlight path"],
        spread,
        {
          highlightPath: (() => {
            const t = terminalsFromPositions(spread);
            return zRoute(t.A, t.D);
          })(),
        }
      ),
      step(
        "l",
        "L reference",
        "L-HV is the fast pattern route baseline.",
        ["Prefer HV/VH", "Pattern router"],
        ["Baseline"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "ov",
        "Overflow tradeoff",
        "Extra bends can spread or concentrate edge usage.",
        ["Not always better", "Measure"],
        ["Cap=2"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "next",
        "Maze escape",
        "When L/Z overflow, maze search detours.",
        ["Penalize saturated edges", "Next lab"],
        ["Maze"],
        spread
      ),
    ],
  },
  "maze-gcell-route": {
    title: "Maze routing",
    module: "module02-05-maze-gcell-route",
    kind: "global-routing",
    steps: [
      step(
        "cost",
        "Edge cost",
        "Maze adds penalty when usage ≥ capacity.",
        ["Search on GCells", "Detour allowed"],
        ["Cost = 1 + penalty"],
        spread
      ),
      step(
        "l-ov",
        "L overflow",
        "L-HV on spread overflows on shared corridors.",
        ["Pattern first", "Then maze"],
        [`total=${GOLDENS.spreadLhvTotalOv}`],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "maze",
        "Route maze",
        "Sequential maze routing considers current usage.",
        ["Six nets", "Finite cost"],
        [`maze≈${GOLDENS.mazeSpreadTotalOv}`],
        spread,
        { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }
      ),
      step(
        "compare",
        "Compare totals",
        "Maze may match or beat L overflow on the toy.",
        ["Not magic", "Still Cap=2"],
        ["Compare L vs maze"],
        spread,
        { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }
      ),
      step(
        "use",
        "When to maze",
        "Use maze when pattern routes saturate edges.",
        ["Global stage", "Rip-up next"],
        ["Next modules"],
        spread
      ),
    ],
  },
  "multipin-tree": {
    title: "Multi-pin tree",
    module: "module02-07-multipin-tree",
    kind: "global-routing",
    steps: [
      step(
        "net4",
        "Four-pin net",
        "Net [A,B,C,D] needs a tree, not a single two-pin path.",
        ["Star demo", "4 legs"],
        ["Net index 4"],
        spread
      ),
      step(
        "center",
        "Bbox center",
        "Star hub at mean GCell of pins (clamped).",
        ["Steiner lite", "Toy only"],
        ["Hub GCell"],
        spread,
        { highlight: ["A", "B", "C", "D"] }
      ),
      step(
        "legs",
        "Four L legs",
        "Each pin gets an L-route from the hub in the full sequential pass.",
        ["4 paths", "Edge sharing"],
        ["Highlight net 4"],
        spread,
        { routes: spreadRoutes("HV"), selectedNet: 4 }
      ),
      step(
        "usage",
        "Shared edges",
        "Multi-pin trees reuse edges—overflow adds up.",
        ["Sum usage", "Cap=2"],
        ["Watch corridors"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "two",
        "Two-pin nets",
        "Short nets E–F stay single L paths.",
        ["Mix topologies", "Six nets total"],
        ["E–F short"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
    ],
  },
  "edge-overflow": {
    title: "Edge overflow",
    module: "module03-01-edge-overflow",
    kind: "global-routing",
    steps: [
      step(
        "def",
        "Overflow",
        "ov(e)=max(0, usage(e)−Cap) per edge.",
        ["Not tile RUDY", "Router metric"],
        ["Edge-local"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "total",
        "Total overflow",
        "Sum over edges—primary regression scalar.",
        ["Sum ov(e)", "Report every pass"],
        [`spread L-HV≈${GOLDENS.spreadLhvTotalOv}`],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "max",
        "Max overflow",
        "Worst edge—catches hotspot corridors.",
        ["Hot corridor", "max metric"],
        [`max≈${GOLDENS.spreadLhvMaxOv}`],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "count",
        "Overflow count",
        "How many edges exceed Cap.",
        ["Triple report", "Same idea as congestion labs"],
        ["count edges"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "target",
        "Hit targets",
        "Move pins or switch HV/VH/maze to clear thresholds.",
        ["Check scores learner", "No golden mode"],
        ["Browser challenges"],
        spread
      ),
    ],
  },
  "ripup-reroute": {
    title: "Rip-up reroute",
    module: "module03-03-ripup-reroute",
    kind: "global-routing",
    steps: [
      step(
        "seq",
        "Sequential L first",
        "Route L-HV; some edges exceed Cap.",
        ["Overflow appears", "Before rip"],
        [`total≈${GOLDENS.spreadLhvTotalOv}`],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "pick",
        "Pick hot edge",
        "Find worst overflowing edge; mark nets using it.",
        ["Shared corridor", "Toy rip order"],
        ["Worst edge first"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "rip",
        "Rip nets",
        "Remove those nets from usage.",
        ["Subtract paths", "Ready to reroute"],
        ["Usage drops"],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "maze-r",
        "Maze reroute",
        "Ripped nets maze-route with updated usage.",
        ["May improve", "GOLDENS.ripupImproves"],
        ["After ripup"],
        spread,
        {
          routes: (() => {
            const t = terminalsFromPositions(spread);
            const r = spreadRoutes("HV");
            const u = usageFromRoutes(r);
            return ripupReroute(r, u, EDGE_CAPACITY, t);
          })(),
        }
      ),
      step(
        "loop",
        "Iterate",
        "Real routers loop estimate→route→rip until clean or budget.",
        ["Detailed route next", "learn_routing"],
        ["Course arc"],
        spread
      ),
    ],
  },
  "sequential-global": {
    title: "Sequential global",
    module: "module04-01-sequential-global",
    kind: "global-routing",
    steps: [
      step(
        "order",
        "Net order",
        "Route nets 0..5 in order; later nets see earlier usage.",
        ["Six nets", "NETS array"],
        ["Order matters"],
        spread
      ),
      step(
        "l-all",
        "Pattern pass",
        "L-HV all nets documents baseline overflow.",
        ["Fast pass", "Baseline"],
        [`total≈${GOLDENS.spreadLhvTotalOv}`],
        spread,
        { routes: spreadRoutes("HV") }
      ),
      step(
        "maze-all",
        "Maze pass",
        "Sequential maze may redistribute usage.",
        ["Penalties", "Compare totals"],
        [`maze≈${GOLDENS.mazeSpreadTotalOv}`],
        spread,
        { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }
      ),
      step(
        "clear",
        "Clear overflow",
        "Goal: total overflow 0 on the toy after moves or maze.",
        ["Challenge lab", "HPWL optional"],
        ["Learner state"],
        spread,
        { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }
      ),
      step(
        "done",
        "Handoff",
        "Global routing feeds detailed routing and DRC-clean paths.",
        ["Edges + caps", "Course wrap"],
        ["Next: learn_routing"],
        spread
      ),
    ],
  },
};

void lRoute;
