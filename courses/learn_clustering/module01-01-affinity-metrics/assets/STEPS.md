# Affinity metrics — step-by-step (for slides / transcript)

**Module:** `module01-01-affinity-metrics`  
**Lab / algo:** `affinity-metrics`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=affinity-metrics&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start with a tiny weighted graph

![Step 1](steps/01-raw-graph.png)

**Caption (transcript):** Five cells A–E with edge weights. Heavy edges A–B and D–E both weigh 5; the bridge through C is weaker. Affinity will decide which pairs want to cluster first.

**Slide bullets:**

- Nodes = cells / clusters to group
- Edge weight = how strongly a pair should stay together
- Reference instance used across all clustering labs

**On-screen metrics:**

```
Graph: 5 nodes, 6 edges
Heaviest edges: A–B=5, D–E=5
```

## Step 2 — Edge-weight affinity ranks pairs

![Step 2](steps/02-edge-rank.png)

**Caption (transcript):** Pure edge-weight affinity just sorts existing edges. A–B and D–E tie at 5; tie-break puts A–B first. This ranking is the simplest merge priority.

**Slide bullets:**

- score(u,v) = w(u,v)
- Sort descending by score
- Top pair becomes the first merge candidate

**On-screen metrics:**

```
1. A–B @ 5
2. D–E @ 5
3. B–C @ 4
4. C–D @ 2
5. A–C @ 1
6. C–E @ 1
```

## Step 3 — Shared neighbors boost A–B

![Step 3](steps/03-shared-idea.png)

**Caption (transcript):** A and B already share edge weight 5. They also share neighbor C. Shared-neighbor affinity adds min(w(A,C), w(B,C)) = min(1,4) = 1, so A–B rises to 6.

**Slide bullets:**

- Direct edge still counts
- Plus support through common neighbors
- Encourages dense triangles to cluster

**On-screen metrics:**

```
w(A,B)=5
shared via C: min(1,4)=1
score(A,B)=6
```

## Step 4 — Shared ranking reshuffles the list

![Step 4](steps/04-shared-rank.png)

**Caption (transcript):** Under shared-neighbor scoring, A–B and D–E lead at 6. Weak edge A–C jumps to 5 because of B. Non-edges like B–D can appear from shared support alone.

**Slide bullets:**

- A–C: was 1 → now 5
- Invented pairs (e.g. B–D @ 2) show transitive pull
- Same idea feeds greedy merge priorities

**On-screen metrics:**

```
1. A–B @ 6
2. D–E @ 6
3. A–C @ 5
4. B–C @ 5
5. C–D @ 3
6. C–E @ 3
```

## Step 5 — Why affinity matters in EDA

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Affinity is the objective’s local preference: which cells belong together before global constraints. Bad affinity → bad merges → harder refinement later.

**Slide bullets:**

- Edge weight = connectivity / nets shared
- Shared neighbors ≈ denser local groups
- Next labs consume this ranking to merge

**On-screen metrics:**

```
Edge top: A–B @ 5
Shared top: A–B @ 6
Teaching graph stays fixed for goldens
```

