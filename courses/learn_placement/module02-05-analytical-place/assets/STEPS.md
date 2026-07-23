# Analytical / density-aware place — step-by-step (for slides / transcript)

**Module:** `module02-05-analytical-place`  
**Lab / algo:** `analytical-place`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=analytical-place&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Wirelength stage clusters first

![Step 1](steps/01-wl-stage.png)

**Caption (transcript):** Analytical lite starts like force/quadratic: pull for wirelength with pads A and D fixed. Clustering cuts HPWL but can overload bins.

**Slide bullets:**

- Force + quadratic wirelength stage
- Pads A, D fixed
- Clusters before spreading

**On-screen metrics:**

```
Start HPWL: 52
Goal: cut WL without total collapse
```

## Step 2 — Density stage pushes overloaded bins

![Step 2](steps/02-density-stage.png)

**Caption (transcript):** A density-repulsion stage pushes cells out of crowded two-by-two bins, then a light reconnect keeps HPWL from exploding.

**Slide bullets:**

- Count cells per bin
- Repel from crowded bin centers
- Light force reconnect afterward

**On-screen metrics:**

```
2×2 density grid
Watch HPWL and overflow together
```

## Step 3 — After analytical: about forty-eight point one

![Step 3](steps/03-after-anal.png)

**Caption (transcript):** The combined solve lands near forty-eight point one—close to quadratic, deliberately above free force, because spreading fights pure collapse.

**Slide bullets:**

- Starter 52 → ≈48.1
- Near quadratic, above force
- Density-aware, not full legalizer

**On-screen metrics:**

```
analyticalHpwlAfter: 48.1
Measured: 48.1
```

## Step 4 — Report HPWL and overflow

![Step 4](steps/04-both-metrics.png)

**Caption (transcript):** Winning wirelength while overflowing every bin is not analytical success. Quote both metrics after the density stage.

**Slide bullets:**

- HPWL ≈ 48.1
- Bin overflow still matters
- Pads remain fixed

**On-screen metrics:**

```
HPWL: 48.1
quadratic compare: 48
```

## Step 5 — Wirelength then density

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Analytical lite is a two-act play: cluster for wirelength, spread for density. Lock pads and iteration knobs so forty-eight point one stays reproducible.

**Slide bullets:**

- WL stage → density stage
- ≈48.1 on this seed
- Next: simulated annealing

**On-screen metrics:**

```
analyticalHpwlAfter: 48.1
```

