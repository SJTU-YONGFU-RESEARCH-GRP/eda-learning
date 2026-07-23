# Kernighan–Lin refinement — step-by-step (for slides / transcript)

**Module:** `module02-05-kernighan-lin`  
**Lab / algo:** `kernighan-lin`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=kernighan-lin&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Bad seed: cutsize 12

![Step 1](steps/01-bad-seed.png)

**Caption (transcript):** Start from a terrible bipartition AE|BCD. Both heavy edges A–B and D–E are cut, so cutsize is 12. KL will search improving swaps.

**Slide bullets:**

- Seed parts: A,E vs B,C,D
- Cut includes A–B(5) and D–E(5)
- Goal: reduce cut without enumerating all partitions

**On-screen metrics:**

```
seed: {"A":"0","E":"0","B":"1","C":"1","D":"1"}
cutsize: 12
```

## Step 2 — Score pairwise swaps by gain

![Step 2](steps/02-gain-idea.png)

**Caption (transcript):** KL considers swapping one vertex from each side. Gain estimates how much the cut shrinks. The best unlocked pair here is A↔D with gain 9.

**Slide bullets:**

- D(v)=external−internal for each vertex
- Swap gain uses D values and the edge between the pair
- Lock pairs after considering them in a pass

**On-screen metrics:**

```
Best candidate swap: A ↔ D
gain g = 9
```

## Step 3 — Accept prefix: only A↔D

![Step 3](steps/03-accept-swap.png)

**Caption (transcript):** Pass 0 builds a sequence of candidate swaps, then keeps the prefix with best cumulative gain. Here best_k=1: perform A↔D once.

**Slide bullets:**

- best_k = 1
- bestCum = 9
- cut 12 → 3 in one swap

**On-screen metrics:**

```
pass 0: A/D(9)
cutBefore=12 cutAfter=3
improved=true
```

## Step 4 — Refined partition ABC|DE

![Step 4](steps/04-final.png)

**Caption (transcript):** After the swap, A joins B,C and D joins E. Heavy edges are internal; only the weak C–D/C–E bridge remains cut.

**Slide bullets:**

- Final parts: ABC|DE
- Matches the greedy/LP communities
- Cutsize golden: 3

**On-screen metrics:**

```
cutsize: 3
parts: ABC|DE
```

## Step 5 — Next pass finds nothing

![Step 5](steps/05-pass1-stop.png)

**Caption (transcript):** Pass 1 reports improved=false. KL stops when a full pass cannot improve—local optimum for swap moves from this seed.

**Slide bullets:**

- Local, not global, optimum
- Quality depends on the seed
- Still the classic bipartition refiner

**On-screen metrics:**

```
pass 1: best_k=0 improved=false
stop
```

