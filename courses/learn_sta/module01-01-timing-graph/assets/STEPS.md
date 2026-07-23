# Timing graph — step-by-step (for slides / transcript)

**Module:** `module01-01-timing-graph`  
**Lab / algo:** `timing-graph`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=timing-graph&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start with a tiny timing chain

![Step 1](steps/01-tiny-chain.png)

**Caption (transcript):** Six pins form one path from primary input in through two cells to out. Net arcs are dashed; cell arcs are solid. This is the shared starter for every STA lab.

**Slide bullets:**

- Pins = ports and cell pins
- Directed arcs carry delay
- One path keeps goldens easy to check by hand

**On-screen metrics:**

```
Pins: 6
Arcs: 5 (2 cell / 3 net)
Clock period: 10 (for later labs)
```

## Step 2 — Name sources and sinks

![Step 2](steps/02-sources-sinks.png)

**Caption (transcript):** A source has no incoming arc; a sink has no outgoing arc. On this chain, in is the only source and out is the only sink.

**Slide bullets:**

- Source = no predecessor arc
- Sink = no successor arc
- Arrival starts at sources; required at sinks

**On-screen metrics:**

```
sources: in
sinks: out
```

## Step 3 — Levelize with Kahn's algorithm

![Step 3](steps/03-levelize.png)

**Caption (transcript):** Process pins with indegree zero, then peel successors. out lands at level 5 on this chain.

**Slide bullets:**

- Queue pins with indegree 0
- level(v) = 1 + max(level of preds)
- If some pins never finish, there is a cycle

**On-screen metrics:**

```
in: L0
u1/A: L1 · u1/Y: L2
u2/A: L3 · u2/Y: L4
out: L5
```

## Step 4 — Topo order and delay sums

![Step 4](steps/04-topo-delays.png)

**Caption (transcript):** Sorting pins by level gives the topo order. Path delay sums to 3.2; cell arcs alone sum to 2.7.

**Slide bullets:**

- Topo order follows increasing level
- Path delay Σ = sum of every arc
- Cell delay Σ ignores net arcs

**On-screen metrics:**

```
topo: in → u1/A → u1/Y → u2/A → u2/Y → out
path delay Σ: 3.2
cell delay Σ: 2.7
```

## Step 5 — A cycle fails levelize

![Step 5](steps/05-cycle-reject.png)

**Caption (transcript):** Add a back-edge from out to in and Kahn's algorithm stalls. Timing graphs for STA must be acyclic.

**Slide bullets:**

- Back-edge out→in creates a cycle
- levelize returns null
- Fix the graph before propagating arrival

**On-screen metrics:**

```
acyclic: false
levels: null
```

