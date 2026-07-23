# Simulated annealing floorplan search — step-by-step (for slides / transcript)

**Module:** `module03-01-simulated-annealing-fp`  
**Lab / algo:** `simulated-annealing-fp`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=simulated-annealing-fp&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Illegal packs pay 1000

![Step 1](steps/01-bad-cost.png)

**Caption (transcript):** Our toy cost adds one thousand when the packing is illegal. The bad overflow seed therefore sits at cost about one thousand forty-four—dominated by the penalty.

**Slide bullets:**

- illegal → +1000
- Plus deadspace and HPWL terms
- Never accept illegal as “good”

**On-screen metrics:**

```
cost(bad)≈1044.4
legal: false
```

## Step 2 — Golden cost stays under 1000

![Step 2](steps/02-golden-cost.png)

**Caption (transcript):** The golden legal packing drops below the penalty floor. Cost is about thirty-six—deadspace and a small HPWL proxy, no illegality tax.

**Slide bullets:**

- cost(golden)≈35.7
- legal: true
- Beats bad by ~1000

**On-screen metrics:**

```
cost(golden)≈35.7
hpwl≈12.5
```

## Step 3 — Neighbors swap module positions

![Step 3](steps/03-neighbor.png)

**Caption (transcript):** A simple SA move swaps the lower-left corners of two modules while keeping sizes. Accept improving moves; accept worsening ones with temperature probability.

**Slide bullets:**

- saSwap(A,E) exchanges coordinates
- Sizes unchanged
- Re-check legality after the move

**On-screen metrics:**

```
move: coordinate swap
then rescore cost
```

## Step 4 — Improve: bad → golden

![Step 4](steps/04-improve.png)

**Caption (transcript):** One teaching “improve” step replaces the illegal seed with the golden packing. Cost falls below one thousand and legality flips to true—exactly what a cooling schedule should prefer.

**Slide bullets:**

- cost drops below 1000
- legal becomes true
- HPWL becomes finite and meaningful

**On-screen metrics:**

```
before≈1044.4
after≈35.7
```

## Step 5 — SA needs a representation

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Annealing is only as good as the move set. Pair it with polish, B-star, or sequence-pair edits—plus soft sizing and macros—in the labs that follow.

**Slide bullets:**

- Penalty for illegal solutions
- Golden cost ≪ bad cost
- Representation defines neighbors

**On-screen metrics:**

```
starter: improve to golden
```

