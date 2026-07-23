#!/usr/bin/env python3
"""Backfill ## Pseudocode into EXAMPLES + transcript code slides for ready PD/STA courses.

Ensures ≤12 lines per ```text fence (CODE_SLIDE_MAX_LINES). Run from repo root:
  python3 scripts/inject_algo_pseudocode.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# mid, title, algo, pseudo, concept_spoken, sketch_spoken
Lab = tuple[str, str, str, str, str, str]

STA: list[Lab] = [
    (
        "module01-01-timing-graph",
        "Timing graph",
        "build pin/arc graph + Kahn levelize",
        """\
INPUT: pins, arcs (delay, kind cell|net)
OUTPUT: levels[] or FAIL(cycle)
indeg[v]←|preds|; Q←{v|indeg=0}; level[Q]=0
while Q:
  u←pop; for v in succ(u):
    indeg[v]−=1; level[v]←max(level[v],level[u]+1)
    if indeg[v]=0: push v
FAIL if not all visited else return levels
GOLDEN: 6 pins, 5 arcs; in:0 … out:5""",
        "Pseudocode for this lab is Kahn levelize on a pin and arc timing graph. Inputs are pins and delayed arcs. The loop peels indegree-zero pins and writes levels. Stop with failure if a cycle leaves pins unvisited.",
        "On the tiny chain the sketch returns levels zero through five with out at five. Six pins and five arcs are the shared instance. Adding out to in makes levelize fail—that is the cycle golden.",
    ),
    (
        "module01-03-arrival-required",
        "Arrival and required",
        "forward arrival + backward setup required",
        """\
INPUT: DAG G, period, arrival seeds
OUTPUT: A[], R_setup[]
for p in topo(G):
  A[p]← max over u→p of A[u]+delay   (sources: seed/0)
for sinks: R[p]←period×cycles
for p in reverse_topo:
  R[p]← min over p→v of R[v]−delay
GOLDEN: A[out]=3.2; R[out]=10; R[in]=6.8""",
        "Arrival and required need two written passes. Forward topo takes a max over predecessors for arrival. Reverse topo takes a min over successors for setup required from the period at sinks.",
        "Goldens on the chain: arrival at out is three point two, required at out is ten, and required at in is six point eight. Arrival is latest; required is earliest.",
    ),
    (
        "module02-01-slack-setup-hold",
        "Slack setup and hold",
        "setup slack R−A; hold lite A−Rhold",
        """\
INPUT: A[], R_setup[], R_hold[] (lite)
OUTPUT: setup_slack, hold_slack, meet?
setup_slack(p) ← R_setup[p] − A[p]
hold_slack(p)  ← A[p] − R_hold[p]
R_hold[sink] ← 0 in this lite model
meet_setup if setup_slack(sink)≥0
meet_hold  if hold_slack(sink)≥0
GOLDEN: setup(out)=6.8; hold(out)=3.2""",
        "Slack pseudocode is arithmetic on tags you already have. Setup slack is required minus arrival. Hold lite uses required hold zero at the sink and arrival minus that required.",
        "On the tiny chain with period ten, setup slack at out is six point eight and hold slack is three point two. Shrink the period to three and setup fails first.",
    ),
    (
        "module02-03-critical-path",
        "Critical path",
        "backtrace worst path using arrivals",
        """\
INPUT: G, A[], sink
OUTPUT: pin path (source→…→sink)
path←[sink]; cur←sink
while cur has preds:
  pick u→cur with A[u]+delay == A[cur]
  (tie-break: largest A[u])
  prepend u; cur←u
return path
GOLDEN: in→u1/A→u1/Y→u2/A→u2/Y→out""",
        "Critical path pseudocode walks backward from the sink. At each pin pick a predecessor arc whose arrival plus delay exactly rebuilds the pin’s arrival, breaking ties toward larger arrival.",
        "The golden path is six pins from in through both cells to out. Path delay must equal arrival at out—three point two on this instance.",
    ),
    (
        "module03-01-incremental-update",
        "Incremental update",
        "invalidate fanout cone; recompute A",
        """\
INPUT: G, edit u→v delay:=d', A_old
OUTPUT: A_new, invalidated cone
set delay(u,v)←d'
inv ← BFS successors from v (incl. v)
delete A[p] for p in inv
recompute A in topo order for missing pins
GOLDEN edit 1.2→2.0 on u1 cell:
  inv={u1/Y,u2/A,u2/Y,out}; A[out]=4.0""",
        "Incremental STA is cone invalidation plus selective recompute. After an arc delay edit, BFS the fanout from the arc’s sink, clear those arrivals, then refill in topo order.",
        "Bump the u1 cell delay from one point two to two. The golden cone is u1/Y, u2/A, u2/Y, and out. Arrival at out becomes four and setup slack six.",
    ),
    (
        "module03-03-false-multicycle-lite",
        "False and multicycle lite",
        "disable arcs + setup_cycles×period",
        """\
INPUT: G, disable set S, setup_cycles
OUTPUT: setup slack at sink
A ← prop_arrival using arcs ∉ S
R ← prop_required; R[sink]←period×cycles
slack ← R[sink] − A[sink]
GOLDEN default: slack(out)=6.8
cycles=2 → R[out]=20, slack=16.8
disable u1/Y→u2/A breaks that path""",
        "Exceptions enter the same propagate sketch. False paths omit disabled arcs. Multicycle setup multiplies the sink required by setup cycles times the period.",
        "Default slack at out is six point eight. Two cycles raises required to twenty and slack to sixteen point eight. Disabling u1/Y to u2/A removes that timing path.",
    ),
]

PART: list[Lab] = [
    (
        "module01-01-cutsize-balance",
        "Cutsize and balance",
        "cutsize + balance metrics",
        """\
INPUT: assignment side[v], weighted edges
OUTPUT: cutsize, sizes, imbalance
cut ← Σ w(u,v) where side[u]≠side[v]
size[p] ← Σ node_size on side p
imbalance ← |s0−s1| / (s0+s1)
GOLDEN bad AE|BCD: cut=12, sizes 2|3
GOLDEN ABC|DE: cut=3, sizes 3|2""",
        "Before any refinement, write the metrics. Pseudocode sums cut edges for cutsize and part sizes for balance. Imbalance is the absolute size gap over total size.",
        "Bad seed AE versus BCD cuts both heavy edges for cutsize twelve. Golden ABC versus DE drops the cut to three with sizes three and two.",
    ),
    (
        "module01-03-initial-bipartition",
        "Initial bipartition",
        "random / greedy / grow seed bipartition",
        """\
INPUT: graph G, method ∈ {random,greedy,grow}
OUTPUT: legal side[v] ∈ {0,1}
random(seed): shuffle; split by half
greedy: keep heaviest edges internal when able
grow(seed): expand frontier until size budget
report cutsize + balance for every seed
GOLDEN: grow(D)→DE|ABC cut=3
random(7)→AE|BCD cut=12""",
        "Initial bipartition is three named constructors in pseudocode: random split, greedy heavy-edge keep, and grow from a seed until the size budget.",
        "Grow from D yields DE versus ABC at cut three. Random seed seven recovers the bad AE versus BCD cut of twelve. Always print cutsize and balance before KL or FM.",
    ),
    (
        "module02-01-kl-partition",
        "Kernighan–Lin",
        "KL pair-swap with prefix rollback",
        """\
INPUT: bipartition side[], max_passes
OUTPUT: refined side[]
each pass: unlock all; compute D-values
repeat |V|/2: pick unlocked pair max swap gain
  lock pair; update working sides + D
keep prefix with best cumulative gain (>0)
apply prefix; stop if no improving pass
GOLDEN BAD_SEED cut 12 → ABC|DE cut 3""",
        "KL pseudocode builds a locked swap sequence each pass, then rolls back to the best positive prefix. Pair gain uses D-values minus twice the edge between the pair.",
        "From the cutsize-twelve bad seed the winning prefix is one swap, A with D. The sketch lands on ABC versus DE at cut three, then the next pass stops.",
    ),
    (
        "module02-03-fm-partition",
        "Fiduccia–Mattheyses",
        "FM single-vertex moves + balance",
        """\
INPUT: side[], balance_tol, max_passes
OUTPUT: refined side[]
each pass: while unlocked legal moves exist:
  pick v with max gain among balance-ok flips
  lock v; flip on working copy
keep best positive-gain prefix; apply
stop when a pass cannot improve
GOLDEN BAD_SEED → flip D then A → cut 3""",
        "FM moves one vertex at a time. Pseudocode ranks unlocked legal flips by gain, locks them into a sequence, then keeps the best positive prefix under a balance filter.",
        "Same bad seed as KL: FM flips D then A, keeps a prefix of two, and reaches ABC versus DE at cut three.",
    ),
    (
        "module02-05-spectral-partition",
        "Spectral bipartition",
        "Fiedler order + balanced cut sweep",
        """\
INPUT: weighted undirected G
OUTPUT: side[] bipartition
L ← Laplacian; take Fiedler eigenvector
order ← nodes sorted by Fiedler value
sweep balanced prefixes; pick min cutsize
GOLDEN: DE|ABC (or ABC|DE) cut=3""",
        "Spectral bipartition reads the Fiedler vector of the Laplacian, sorts nodes, then sweeps balanced prefixes for the cheapest cut.",
        "On the starter graph the winning split is D E versus A B C with cutsize three—the same golden communities KL and FM refine toward.",
    ),
    (
        "module02-07-recursive-bisection",
        "Recursive bisection",
        "repeat bipartition until k parts",
        """\
INPUT: G, target k parts
OUTPUT: side[v] ∈ {0..k−1}
parts ← {all nodes}
while |parts| < k:
  pick largest part P
  bipartition P (spectral/KL/FM)
  replace P with the two halves
GOLDEN k=2: ABC|DE cut=3
k=3 continues on ABC → AB|C|DE""",
        "Recursive bisection is a loop over parts: while you have fewer than k parts, split the largest with a bipartitioner and replace it by the two halves.",
        "First split yields ABC versus DE at cut three. For k equals three the sketch bisects ABC next into A B versus C with D E untouched.",
    ),
    (
        "module03-01-multiway-partition",
        "Multiway partitioning",
        "recursive bisection vs round-robin k-way",
        """\
INPUT: G, k
OUTPUT: k-way assignment + cutsize
method A: recursive_bisection(G,k)
method B: round-robin / block assign labels
cut ← Σ w where side[u]≠side[v]
GOLDEN k=3 recursive: AB|C|DE cut=8
round-robin alphabetic: cut≈18 (worse)""",
        "Multiway compares two constructors in pseudocode: recursive bisection to k, versus a naive round-robin labeling. Both must report the same cutsize metric.",
        "Recursive k equals three lands A B, C, and D E with cut eight. Alphabetical round-robin shreds heavy edges and scores about eighteen.",
    ),
    (
        "module03-03-terminal-propagation",
        "Terminal propagation",
        "fix terminals; partition free cells",
        """\
INPUT: G, fixed terminals T with side
OUTPUT: side for free cells
lock every t∈T at its side
partition free nodes (KL/FM/spectral)
treat T as immovable during moves
report cutsize with terminals included
GOLDEN: fixed terminals steer free cells""",
        "Terminal propagation adds locked nodes to the bipartition sketch. Fixed terminals keep their sides and act as immovable anchors while free cells move.",
        "After locks are placed, run the same refiner on free cells only. Cutsize still counts every edge, including those that touch terminals.",
    ),
    (
        "module03-05-hypergraph-partition",
        "Hypergraph partitioning",
        "hyperedge cut (span >1 part)",
        """\
INPUT: hyperedges e={pins…}, side[]
OUTPUT: hyperedge_cut
cut ← count edges with |{side[p]:p∈e}| > 1
(optional) expand to pairwise clique for KL/FM
GOLDEN ABC|DE: one cut net on starter H
pairwise clique expansion can differ""",
        "Hypergraph cut counts a net once if it spans more than one part. Pseudocode is a span check per hyperedge—not a sum of clique pairs unless you expand deliberately.",
        "On the starter hypergraph, golden ABC versus DE leaves a single cut net. Expanding to a clique can tell a different numeric story—report which model you used.",
    ),
    (
        "module04-01-multilevel-partition",
        "Multilevel partitioning",
        "coarsen → partition → project → refine",
        """\
INPUT: G, coarsen until tiny
OUTPUT: fine side[]
coarsen: match/cluster heavy edges
partition coarse (spectral/KL/FM)
project labels to finer level
refine with FM/KL at each uncoarsen
GOLDEN project ABC|DE cut=3; refine keeps 3""",
        "Multilevel is a V-cycle in pseudocode: coarsen, partition the tiny graph, project labels upward, and refine at each level.",
        "On TINY_GRAPH the projected seed is already ABC versus DE at cut three. Refine keeps that cut—multilevel beats polishing the cut-twelve bad seed alone.",
    ),
]

FP: list[Lab] = [
    (
        "module01-01-fixed-outline",
        "Fixed outline",
        "containment + non-overlap legality",
        """\
INPUT: outline W×H, modules (x,y,w,h)
OUTPUT: legal? / failure reason
for each m: fail if outside [0,W]×[0,H]
for each pair: fail if interior overlap
edge-touch OK; positive-area overlap not
GOLDEN pack legal; E@x=9 overflow illegal
outline 10×8 (area 80); modules A–E""",
        "Fixed-outline legality is two loops in pseudocode: each module must sit inside the outline, and every pair must not have positive-area overlap.",
        "Outline is ten by eight. Golden packing of A through E is legal. Bad seed with E at x nine overflows. Overlap of C and E is the other failure mode.",
    ),
    (
        "module01-03-area-deadspace",
        "Area and deadspace",
        "module area, density, deadspace",
        """\
INPUT: outline W×H, modules areas
OUTPUT: area_sum, deadspace, density
area_sum ← Σ w[m]·h[m]
deadspace ← W·H − area_sum
density ← area_sum / (W·H)
only report density on legal packs
GOLDEN: area=23; outline=80; dead=57
density=0.2875""",
        "Deadspace pseudocode is arithmetic after legality. Sum module areas, subtract from outline area, and divide for density.",
        "On the golden packing area is twenty-three, outline eighty, deadspace fifty-seven, density about zero point two eight seven five. Do not celebrate density on illegal packs.",
    ),
    (
        "module02-01-slicing-floorplan",
        "Slicing / polish",
        "postfix H/V polish evaluation",
        """\
INPUT: polish tokens (modules + H/V)
OUTPUT: packing (x,y,w,h) per module
stack-eval postfix:
  module → push rect
  H: pop a,b; stack vertically
  V: pop a,b; place side by side
GOLDEN: A D H B V C V E V
bbox 9×3; legal in 10×8""",
        "Slicing polish is a postfix stack. Modules push rectangles; H stacks vertically; V places side by side. The sketch names the operators so evaluation stays deterministic.",
        "Golden tokens A D H B V C V E V pack to a nine by three bbox inside the ten by eight outline.",
    ),
    (
        "module02-03-bstar-tree",
        "B*-tree",
        "contour pack from B*-tree",
        """\
INPUT: binary tree (left=right-of, right=above)
OUTPUT: packed (x,y) via contour
root at (0,0)
left child: x ← parent.x + parent.w
right child: y ← above parent (contour)
update horizontal contour after each place
GOLDEN: A@0,0; B.x=A.x+A.w; D.y≥A.h; legal""",
        "B-star packing walks the tree with a contour. Left child sits to the right of the parent; right child sits above using the contour height.",
        "Golden tree roots A at the origin. B’s x equals A’s right edge; D’s y is at least A’s height. The packing must stay legal in the outline.",
    ),
    (
        "module02-05-sequence-pair",
        "Sequence pair",
        "longest-path pack from pos/neg",
        """\
INPUT: pos[], neg[] permutations of modules
OUTPUT: (x,y) via constraint longest paths
pos/neg order ⇒ horizontal & vertical constraints
x ← longest path in H-graph; y ← V-graph
GOLDEN pos=A B C E D; neg=D A B C E
packs legally with non-negative coords""",
        "Sequence-pair pseudocode turns two permutations into horizontal and vertical constraints, then longest-path packs x and y.",
        "Golden pos is A B C E D and neg is D A B C E. Evaluation must place all five modules legally with non-negative coordinates.",
    ),
    (
        "module03-01-simulated-annealing-fp",
        "SA floorplan",
        "anneal with illegality penalty cost",
        """\
INPUT: pack / representation, T schedule
OUTPUT: best legal low-cost pack
cost ← 1000·¬legal + deadspace + α·HPWL
propose neighbor (swap/move/perturb)
accept if Δ<0 or rand < e^(−Δ/T)
keep best; cool T
GOLDEN legal cost≈36; bad≈1044""",
        "Floorplan annealing uses a cost that heavily penalizes illegality. Pseudocode proposes neighbors, accepts by Metropolis, and keeps the best legal iterate.",
        "Bad overflow seed costs about one thousand forty-four. Golden legal packing is about thirty-six. One teaching improve step replaces bad with golden.",
    ),
    (
        "module03-03-soft-module-sizing",
        "Soft module sizing",
        "reshape soft A under area+aspect",
        """\
INPUT: soft A area=6, aspect∈[0.5,2]
OUTPUT: (w,h) with w·h=area; pack rest
choose aspect; set w,h; re-pack / legalize
hard modules keep fixed w×h
GOLDEN hard A 3×2 vs soft A 2×3 pack
both area 6; whitespace shape differs""",
        "Soft sizing picks width and height for A under a fixed area and aspect bounds, then re-packs the hard modules around it.",
        "Hard golden keeps A at three by two. Soft teaching pack uses two by three. Area stays six; deadspace shape changes.",
    ),
    (
        "module03-05-macro-placement",
        "Macro placement",
        "fix hard macro then pack free",
        """\
INPUT: macros F locked (x,y), free modules
OUTPUT: legal pack; macros never move
place each f∈F at locked pose (macro flag)
pack free modules around F obstacles
fail if any macro drifts
GOLDEN free: D@(0,2); macro: D@(0,0)""",
        "Macro placement locks hard blocks first. Free modules pack around those obstacles; legality fails if a macro drifts.",
        "Free golden has movable D at zero comma two. Macro teaching pack pins D at zero comma zero with macro true and the rest legal.",
    ),
    (
        "module04-01-hierarchical-floorplan",
        "Hierarchical floorplan",
        "cluster then pack clusters",
        """\
INPUT: clusters of modules
OUTPUT: top-level pack of cluster bboxes
pack each cluster internally (slice/B*/SA)
pack cluster bboxes in outline
GOLDEN teaching: AB left; CDE right @x=5""",
        "Hierarchical floorplan packs inside clusters first, then packs the cluster bounding boxes in the outline.",
        "Teaching golden places cluster A B on the left and C D E on the right starting at x equals five.",
    ),
    (
        "module04-03-pin-assignment",
        "Pin assignment",
        "boundary pins on outline sides",
        """\
INPUT: outline, pin list {side, offset}
OUTPUT: pinsValid?
each pin on left|right|top|bottom edge
offset in range for that side
require all four sides represented
GOLDEN 4 pins (one/side) → valid true
empty list → valid false""",
        "Pin assignment validates boundary I/O. Pseudocode checks side and offset ranges and requires all four outline sides to appear.",
        "Golden pins cover left, bottom, right, and top and return valid true. An empty list fails validity.",
    ),
]

PLACE: list[Lab] = [
    (
        "module01-01-hpwl-metrics",
        "HPWL metrics",
        "half-perimeter wirelength sum",
        """\
INPUT: positions, nets
OUTPUT: total HPWL
for each net: bbox → (maxx−minx)+(maxy−miny)
total ← Σ net HPWL
GOLDEN starter=52; compact=14
NOTE: collapsed point ≠ usable place""",
        "HPWL is one loop over nets: bounding-box width plus height, then sum. That sum is the teaching yardstick for every later placer.",
        "Starter placement scores fifty-two. Compact golden scores fourteen. Never celebrate a tiny total that piles every cell on one point.",
    ),
    (
        "module01-03-net-models",
        "Net models",
        "bbox vs clique vs star HPWL",
        """\
INPUT: net pins, positions, model
bbox: one HPWL on all pins
clique: Σ pairwise HPWL over pin pairs
star: Σ HPWL(hub, other pins)
GOLDEN 4-pin ABCD on golden place:
  clique=16; star from A=8""",
        "Net models change which edges enter the sum. Pseudocode names bbox, clique, and star so reports stay comparable.",
        "On golden ABCD, clique HPWL is sixteen and star from A is eight. Mixing models in one table is a metric bug.",
    ),
    (
        "module02-01-force-directed-place",
        "Force-directed place",
        "neighbor average pull + weak center",
        """\
INPUT: positions, nets, α, iters, fixed pads
OUTPUT: updated positions + HPWL
each iter, for free cell c:
  tgt ← avg neighbor coords (+ weak center)
  pos[c] ← (1−α)·pos[c] + α·tgt
pads stay fixed
GOLDEN starter 52 → ≈18.7 after defaults""",
        "Force-directed place blends each free cell toward its neighbor average with step alpha. Fixed pads do not move.",
        "From starter fifty-two, default lite iterations land near eighteen point seven—better wirelength, still above compact fourteen.",
    ),
    (
        "module02-03-quadratic-place",
        "Quadratic place",
        "Gauss–Seidel neighbor solve w/ pads",
        """\
INPUT: positions, nets, fixed pads {A,D}
OUTPUT: free-cell coords + HPWL
repeat: for free c:
  blend toward neighbor average (damped)
pads A,D remain pinned
GOLDEN starter 52 → HPWL 48""",
        "Quadratic-lite solves free cells toward neighbor averages under pinned pads. Damping keeps the system from collapsing.",
        "With A and D fixed, the teaching solve reaches HPWL forty-eight from fifty-two—modest win, honest about pad constraints.",
    ),
    (
        "module02-05-analytical-place",
        "Analytical place",
        "wirelength stage + density spread",
        """\
INPUT: positions, bins, pads
OUTPUT: positions, HPWL, overflow
stage1: wirelength pull (force/quad style)
stage2: push out of overloaded bins
stage3: light reconnect for HPWL
report HPWL and overflow together
GOLDEN lite ≈48.1 HPWL after defaults""",
        "Analytical lite is three stages in pseudocode: wirelength clustering, density repulsion from overloaded bins, then a light reconnect so HPWL does not explode.",
        "Default teaching run lands near forty-eight point one HPWL. Winning wirelength while overflowing every bin is not success—report both metrics.",
    ),
    (
        "module02-07-sa-placement",
        "SA placement",
        "random jogs; Metropolis on HPWL",
        """\
INPUT: positions, seed, moves, T0
OUTPUT: best positions + best HPWL
for i in 1..moves:
  jog one cell on one axis
  accept if ΔHPWL<0 or rand<e^(−Δ/T)
  keep best; cool T
GOLDEN seed=42, 60 moves → best≈49.6
accepted≈44 rejected≈16""",
        "Placement annealing jogs one cell per move under HPWL cost, accepts by Metropolis, and keeps the best iterate—not only the final temperature.",
        "Seed forty-two with sixty moves yields best HPWL near forty-nine point six from fifty-two. Lock the seed so goldens stay stable.",
    ),
    (
        "module03-01-density-bins",
        "Density bins",
        "bin counts + overflow vs capacity",
        """\
INPUT: positions, grid Gx×Gy, capacity C
OUTPUT: overflow, per-bin counts
assign each cell to a bin by (x,y)
overflow ← Σ max(0, count[b]−C)
report HPWL with overflow
GOLDEN 2×2 C=1: starter&golden overflow=2
C=2 on golden → overflow=1""",
        "Density bins count occupants per grid cell and sum overflow above capacity. Pseudocode always pairs that number with HPWL.",
        "On a two-by-two grid with capacity one, both starter and golden still overflow by two. Raise capacity to two on golden and overflow drops to one.",
    ),
    (
        "module03-03-spread-legalize-lite",
        "Spread legalize lite",
        "push pairs to min distance",
        """\
INPUT: positions, min_dist
OUTPUT: spread positions
while exists pair with dist < min_dist:
  push the pair apart along their vector
stop when all pairs clear min_dist
NOTE: not row/site legalization
GOLDEN min_dist=0.5 on overlap seed""",
        "Spread lite pushes close pairs apart until every pairwise distance clears a minimum. It is overlap relief, not site legalization.",
        "Start from the triple-overlap demo, run the spreader with minimum distance zero point five, and confirm pairs clear without exploding HPWL.",
    ),
    (
        "module04-01-timing-driven-place",
        "Timing-driven place",
        "weighted HPWL with net criticality",
        """\
INPUT: positions, nets, weights w[net]
OUTPUT: plain HPWL, timing HPWL
plain ← Σ HPWL(net)
timing ← Σ w[net]·HPWL(net)
optimize timing (or report both)
GOLDEN starter: plain=52 timing=116
compact: plain=14 timing=30""",
        "Timing-driven place multiplies each net’s HPWL by criticality and sums. Pseudocode always reports plain and weighted totals together.",
        "Starter plain fifty-two becomes timing one hundred sixteen because the four-pin net has weight five. Compact golden drops timing cost to thirty.",
    ),
]

COURSES = {
    "learn_sta": (STA, "tiny_timing.json", "common/propagate.py + graph.py"),
    "learn_partitioning": (PART, "tiny_graph.json", "common/solvers.py"),
    "learn_floorplanning": (FP, "tiny_modules.json", "common/solvers.py"),
    "learn_placement": (PLACE, "tiny_place.json", "common/solvers.py"),
}

EXAMPLES_TMPL = """# Examples — {title}

Track A (implement). Use `examples/{example}` and `../../{common_hint}`.

## Algorithm

**{algo}**

## Pseudocode

```text
{pseudo}
```

## Starter prompts

1. Implement the pseudocode above (or call the matching `common/` helper).
2. Print the metrics named in the GOLDEN line; match browser / Track A tests.
3. Change one knob and report what moved.

## Expected artifacts

- Outputs listed in the pseudocode OUTPUT line
- Note tying the run to the pseudocode phases

## Stretch

Scale the instance slightly; keep the same metrics API.
"""

SLIDE_CONCEPT = """## Slide {n} — Pseudocode

{spoken}

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.
"""

SLIDE_SKETCH = """## Slide {n} — Algorithm sketch

{spoken}

```text
{pseudo}
```
"""


def renumber_slides(text: str) -> str:
    pattern = re.compile(r"^## Slide \d+ — (.+)$", re.M)
    idx = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        idx += 1
        return f"## Slide {idx} — {m.group(1)}"

    return pattern.sub(repl, text)


def strip_pseudo_slides(text: str) -> str:
    text = re.sub(
        r"\n## Slide \d+ — Pseudocode\n.*?(?=\n## Slide |\n<!-- )",
        "\n",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\n## Slide \d+ — Algorithm sketch\n.*?(?=\n## Slide |\n<!-- )",
        "\n",
        text,
        flags=re.S,
    )
    return text


def inject_transcript(course: str, mid: str, pseudo: str, concept: str, sketch: str) -> None:
    path = ROOT / "courses" / course / mid / "transcript.md"
    text = path.read_text(encoding="utf-8")
    text = strip_pseudo_slides(text)
    block = (
        "\n"
        + SLIDE_CONCEPT.format(n=99, spoken=concept).rstrip()
        + "\n\n"
        + SLIDE_SKETCH.format(n=99, spoken=sketch, pseudo=pseudo.rstrip()).rstrip()
        + "\n\n"
    )
    m_walk = re.search(r"<!-- algorithm-walkthrough -->", text)
    m_s2 = re.search(r"^## Slide 2 — ", text, re.M)
    if m_walk and m_s2 and m_walk.start() < m_s2.start():
        m = re.search(
            r"(## Slide 1 — .+?\n\n.*?)(\n(?=<!-- algorithm-walkthrough -->|## Slide ))",
            text,
            re.S,
        )
    else:
        m = re.search(
            r"(## Slide 2 — .+?\n\n.*?)(\n(?=<!-- algorithm-walkthrough -->|## Slide ))",
            text,
            re.S,
        )
    if not m:
        raise SystemExit(f"cannot find insert point in {course}/{mid}")
    text = text[: m.end(1)] + "\n" + block + text[m.start(2) :]
    text = renumber_slides(text)
    # Point implement track at EXAMPLES Pseudocode
    text = text.replace(
        "open this module’s examples and the course `common/` solvers",
        "open this module's EXAMPLES.md Pseudocode section and the course common solvers",
    )
    text = text.replace(
        "open this module's examples and the course `common/` solvers",
        "open this module's EXAMPLES.md Pseudocode section and the course common solvers",
    )
    text = text.replace(
        "open this module’s examples and build the full algorithm",
        "open this module's EXAMPLES.md Pseudocode section and build the full algorithm",
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_examples(course: str, labs: list[Lab], example: str, common_hint: str) -> None:
    for mid, title, algo, pseudo, _c, _s in labs:
        n = len(pseudo.strip().splitlines())
        assert n <= 12, f"{course}/{mid} has {n} lines"
        path = ROOT / "courses" / course / mid / "EXAMPLES.md"
        path.write_text(
            EXAMPLES_TMPL.format(
                title=title,
                example=example,
                common_hint=common_hint,
                algo=algo,
                pseudo=pseudo.rstrip(),
            ),
            encoding="utf-8",
            newline="\n",
        )


def main() -> None:
    total = 0
    for course, (labs, example, common_hint) in COURSES.items():
        write_examples(course, labs, example, common_hint)
        for mid, title, _a, pseudo, concept, sketch in labs:
            inject_transcript(course, mid, pseudo, concept, sketch)
            n = len(pseudo.strip().splitlines())
            print(f"OK  {course}/{mid} fence_lines={n} ({title})")
            total += 1
    print(f"DONE labs={total}")


if __name__ == "__main__":
    main()
