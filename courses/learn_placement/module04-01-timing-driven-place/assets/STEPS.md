# Timing-driven placement — step-by-step (for slides / transcript)

**Module:** `module04-01-timing-driven-place`  
**Lab / algo:** `timing-driven-place`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=timing-driven-place&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Plain HPWL hides critical nets

![Step 1](steps/01-plain-vs-weighted.png)

**Caption (transcript):** On the starter, plain HPWL is fifty-two, but timing-weighted HPWL is one hundred sixteen because the four-pin net carries weight five.

**Slide bullets:**

- weights = [1,1,1,1,5,1]
- Net ABCD is critical
- Report both totals

**On-screen metrics:**

```
Plain HPWL: 52
Timing HPWL: 116
Net4 weight: 5
```

## Step 2 — Weighted sum of net HPWLs

![Step 2](steps/02-weight-math.png)

**Caption (transcript):** Multiply each net’s bbox HPWL by its criticality and sum. The critical ABCD net alone contributes five times sixteen equals eighty on the starter.

**Slide bullets:**

- Σ wᵢ · HPWL(netᵢ)
- Heavy nets pull harder
- Same coordinates, new objective

**On-screen metrics:**

```
ABCD plain: 16
ABCD weighted: 80
Total timing: 116
```

## Step 3 — Golden timing cost drops to thirty

![Step 3](steps/03-golden-timing.png)

**Caption (transcript):** The compact golden cuts the critical bbox sharply. Timing-weighted HPWL falls from one hundred sixteen to thirty while plain HPWL hits fourteen.

**Slide bullets:**

- Starter timing 116 → golden 30
- Plain golden still 14
- Critical net drove the win

**On-screen metrics:**

```
goldenTimingHpwl: 30
goldenHpwl: 14
Measured timing: 30
```

## Step 4 — Always quote plain and weighted

![Step 4](steps/04-both-reports.png)

**Caption (transcript):** A placement can look fine on plain HPWL while the critical net stays long. Timing labs demand both numbers so the objective is visible.

**Slide bullets:**

- Plain: wirelength yardstick
- Weighted: timing objective
- Critical net highlighted

**On-screen metrics:**

```
starter: 52 / 116
golden: 14 / 30
```

## Step 5 — Weights change what you optimize

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Timing-driven place is still wirelength—just weighted. Remember one hundred sixteen to thirty on this instance, and never drop the plain HPWL report.

**Slide bullets:**

- Critical net weight 5
- 116 → 30 timing HPWL
- Course wrap: compare all engines

**On-screen metrics:**

```
starterTimingHpwl: 116
goldenTimingHpwl: 30
```

