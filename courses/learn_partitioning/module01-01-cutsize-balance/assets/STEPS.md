# Cutsize and balance — step-by-step (for slides / transcript)

**Module:** `module01-01-cutsize-balance`  
**Lab / algo:** `cutsize-balance`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=cutsize-balance&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Same graph, two bipartitions

![Step 1](steps/01-graph.png)

**Caption (transcript):** TINY_GRAPH has five cells. Partition quality is measured by cutsize (sum of cut edge weights) and balance (how even the two sides are).

**Slide bullets:**

- Cutsize = wire crossing the partition
- Balance ratio = min side / max side
- Both metrics matter in floorplanning

**On-screen metrics:**

```
5 nodes, 6 edges
Target: legal 2-way split
```

## Step 2 — Bad seed: cutsize 12

![Step 2](steps/02-bad-seed.png)

**Caption (transcript):** Seed AE|BCD cuts both heavy edges A–B(5) and D–E(5). Cutsize is 12 — a terrible wire cost even though the split is legal.

**Slide bullets:**

- Parts: A,E vs B,C,D
- Heavy internal edges become cut edges
- Same graph used across partitioning labs

**On-screen metrics:**

```
seed: {"A":"0","E":"0","B":"1","C":"1","D":"1"}
cutsize: 12
parts: AE|BCD
```

## Step 3 — Bad seed balance: ratio 2/3

![Step 3](steps/03-bad-balance.png)

**Caption (transcript):** Side sizes are 2 vs 3, so balance ratio = 2/3 and imbalance |2−3|/5 = 0.2. The split is moderately balanced — cutsize, not balance, is the problem.

**Slide bullets:**

- ratio = min/max of side sizes
- imbalance = |s0−s1| / n
- Balance alone does not rank partitions

**On-screen metrics:**

```
sizes: 2 vs 3
ratio: 0.6667
imbalance: 0.2
```

## Step 4 — Golden ABC|DE: cutsize 3

![Step 4](steps/04-golden.png)

**Caption (transcript):** Golden bipartition ABC|DE keeps A–B and D–E internal. Only weak bridges C–D(2) and C–E(1) are cut — cutsize drops to 3 with the same 2/3 ratio.

**Slide bullets:**

- Heavy edges stay inside communities
- Same balance ratio as bad seed
- Cutsize distinguishes quality

**On-screen metrics:**

```
parts: ABC|DE
cutsize: 3
ratio: 2/3 (unchanged)
```

## Step 5 — Cutsize + balance literacy

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Two partitions can share the same balance but differ wildly in cut. EDA flows optimize cut under balance constraints — never balance alone.

**Slide bullets:**

- Bad: AE|BCD cut 12, ratio 2/3
- Golden: ABC|DE cut 3, ratio 2/3
- Refinement labs repair bad seeds later

**On-screen metrics:**

```
12 → 3 cut improvement
ratio stays 2/3
```

