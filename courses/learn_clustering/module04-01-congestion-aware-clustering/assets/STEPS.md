# Congestion-aware clustering — step-by-step (for slides / transcript)

**Module:** `module04-01-congestion-aware-clustering`  
**Lab / algo:** `congestion-aware-clustering`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=congestion-aware-clustering&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start from BAD_SEED

![Step 1](steps/01-bad-seed.png)

**Caption (transcript):** Same cutsize-12 seed AE|BCD. Congestion map marks C–D=5 and C–E=4 — cheap wire cuts may be expensive for routing.

**Slide bullets:**

- plain cut ignores congestion
- penalty sums cong on cut edges
- λ trades plain vs penalty

**On-screen metrics:**

```
seed cut: 12
cong: C|D=5, C|E=4
```

## Step 2 — λ=0 → ordinary FM

![Step 2](steps/02-lam0.png)

**Caption (transcript):** With λ=0, boosted weights equal original weights. FM recovers ABC|DE: plain=3 but penalty=9 because both congested bridges are cut.

**Slide bullets:**

- plain=3, pen=9
- parts: ABC|DE
- Objective ignores routing pain

**On-screen metrics:**

```
λ=0
plain=3
pen=9
```

## Step 3 — Boost weights by λ·cong

![Step 3](steps/03-boost.png)

**Caption (transcript):** For λ=5, C–D and C–E become very expensive to cut. FM optimizes the boosted graph, then we report plain cut and congestion penalty separately.

**Slide bullets:**

- w' = w + λ·cong
- Run FM on w'
- Score plain + λ·pen on original

**On-screen metrics:**

```
λ=5
C–D and C–E heavily boosted
```

## Step 4 — λ=5 → pen 0, plain 5

![Step 4](steps/04-lam5.png)

**Caption (transcript):** Result AB|CDE: plain cut rises to 5, but congestion penalty drops to 0 — congested bridges stay internal.

**Slide bullets:**

- parts: AB|CDE
- plain=5, pen=0
- objective=5

**On-screen metrics:**

```
λ=5
plain=5
pen=0
```

## Step 5 — Objective tradeoffs

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** EDA flows rarely optimize cut alone. λ makes the congestion tax explicit so students see the Pareto move between wire and routing.

**Slide bullets:**

- λ=0 favors classic communities
- λ>0 protects congested edges
- Same FM engine, different weights

**On-screen metrics:**

```
Goldens: (3,9) vs (5,0)
```

