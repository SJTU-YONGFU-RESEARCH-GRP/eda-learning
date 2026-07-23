# Spreading / overlap relief — step-by-step (for slides / transcript)

**Module:** `module03-03-spread-legalize-lite`  
**Lab / algo:** `spread-legalize-lite`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=spread-legalize-lite&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Triple overlap at one point

![Step 1](steps/01-triple-overlap.png)

**Caption (transcript):** The overlap demo stacks A, B, and C on (4,4). Min pairwise distance is zero—illegal for any site-aware flow, perfect for a spreading lesson.

**Slide bullets:**

- A,B,C @ (4,4)
- minPairDist = 0
- D,E,F already spread

**On-screen metrics:**

```
minPairDist: 0
Target minDist: 0.5
```

## Step 2 — Push near pairs apart

![Step 2](steps/02-push-apart.png)

**Caption (transcript):** While any pair sits closer than minDist, push them along their separation vector. Repeated passes peel the triple stack into distinct points.

**Slide bullets:**

- Push along separation vector
- strength controls step size
- Not full row-site legalization

**On-screen metrics:**

```
minDist = 0.5
iters ≈ 40 + repair
```

## Step 3 — After spread: min distance holds

![Step 3](steps/03-after-spread.png)

**Caption (transcript):** The lite spreader separates A, B, and C until every pair clears about zero point five. D, E, and F barely move.

**Slide bullets:**

- minPairDist ≥ 0.5
- Deterministic repair pass
- HPWL may rise—that is expected

**On-screen metrics:**

```
minPairDist: 0.5
spreadMinPairDist golden: 0.5
```

## Step 4 — Spreading is a legality proxy

![Step 4](steps/04-legality-proxy.png)

**Caption (transcript):** Clearing min distance is not row legalization or site snapping. It is a teaching stand-in so overlap stops hiding behind pretty HPWL.

**Slide bullets:**

- Proxy ≠ detailed placement
- Still report HPWL after
- Use after analytical collapse

**On-screen metrics:**

```
HPWL after spread: 26.8
minDist: 0.5
```

## Step 5 — Relieve overlap before celebrating WL

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Start from the triple-overlap seed, spread to minDist zero point five, and confirm every pair clears the threshold. Then revisit wirelength.

**Slide bullets:**

- Overlap seed → spread
- minDist 0.5 golden
- Next: timing-driven weights

**On-screen metrics:**

```
spreadMinPairDist: 0.5
```

