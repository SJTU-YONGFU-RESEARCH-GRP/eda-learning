# Fiduccia–Mattheyses bipartition — step-by-step (for slides / transcript)

**Module:** `module02-03-fm-partition`  
**Lab / algo:** `fm-partition`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=fm-partition&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Same bad seed, different move set

![Step 1](steps/01-bad-seed.png)

**Caption (transcript):** FM starts from the same cutsize-12 seed, but moves one vertex at a time instead of swapping a pair. That suits hypergraph / cell-move implementations.

**Slide bullets:**

- Single-vertex moves across the cut
- Bucketed gains for speed (classic FM)
- Balance tolerance limits lopsided moves

**On-screen metrics:**

```
seed cutsize: 12
parts: AE|BCD
```

## Step 2 — Move 1: flip D (gain 3)

![Step 2](steps/02-move-d.png)

**Caption (transcript):** Highest legal move sends D to the other side with gain 3. Partial progress: D joins E's side early.

**Slide bullets:**

- Pick unlocked vertex with best gain
- Apply move, lock vertex
- Update neighbor gains

**On-screen metrics:**

```
move: D(g=3)
running toward best prefix
```

## Step 3 — Move 2: flip A (gain 6)

![Step 3](steps/03-move-a.png)

**Caption (transcript):** Next, A flips with gain 6. Cumulative gain is 3+6=9 — the same total improvement KL found with one swap.

**Slide bullets:**

- Two moves ≈ one KL swap's worth of gain
- best_k=2 keeps both moves
- bestCum=9

**On-screen metrics:**

```
moves: D(3), A(6)
bestCum=9
cut 12→3
```

## Step 4 — Final ABC|DE, cutsize 3

![Step 4](steps/04-final.png)

**Caption (transcript):** FM lands on the same refined bipartition as KL. Teaching point: move style differs, destination quality matches on this instance.

**Slide bullets:**

- parts: ABC|DE
- cutsize: 3
- Compare with KL transcript side-by-side

**On-screen metrics:**

```
cutsize: 3
pass 0 improved=true
```

## Step 5 — Pass 1 confirms local optimum

![Step 5](steps/05-pass1-stop.png)

**Caption (transcript):** A second FM pass finds no improving move prefix. Stop. In real tools, FM often runs inside multilevel V-cycles with tighter balance and hyperedges.

**Slide bullets:**

- improved=false on pass 1
- Cell moves scale to large netlists
- Next: multilevel + hypergraph partition

**On-screen metrics:**

```
pass 1: best_k=0
stop
```

