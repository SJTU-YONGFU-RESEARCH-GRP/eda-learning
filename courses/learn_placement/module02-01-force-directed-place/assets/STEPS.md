# Force-directed placement — step-by-step (for slides / transcript)

**Module:** `module02-01-force-directed-place`  
**Lab / algo:** `force-directed-place`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=force-directed-place&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start from HPWL fifty-two

![Step 1](steps/01-starter.png)

**Caption (transcript):** Force-directed place pulls free cells toward the average of their net neighbors, plus a weak center pull. Begin on the spread starter at HPWL fifty-two.

**Slide bullets:**

- Spring pull along net edges
- Weak center attraction
- Small alpha avoids collapse

**On-screen metrics:**

```
HPWL: 52
iters: 5 (default)
alpha ≈ 0.12
```

## Step 2 — Neighbors pull cells inward

![Step 2](steps/02-mid-iters.png)

**Caption (transcript):** After a couple of lite iterations, A–D drift toward the center while E and F follow their neighbors. Wirelength is already dropping.

**Slide bullets:**

- Each free cell → neighbor average
- Blend with small alpha
- Pads stay free in this lab

**On-screen metrics:**

```
Mid HPWL: 34.5
Still above golden 14
```

## Step 3 — After force: about eighteen point seven

![Step 3](steps/03-after-force.png)

**Caption (transcript):** Default five iterations land near eighteen point seven—clearly better than fifty-two, still above the compact golden fourteen.

**Slide bullets:**

- Report before/after HPWL
- Force ≈ 18.7 on this seed
- Not a full legalizer

**On-screen metrics:**

```
Before: 52
After: 18.7
Measured: 18.7
```

## Step 4 — Force vs golden compact

![Step 4](steps/04-vs-golden.png)

**Caption (transcript):** Golden fourteen is tighter still. Force is a cheap continuous move—good teaching progress without claiming the absolute minimum.

**Slide bullets:**

- Force ≈ 18.7
- Golden = 14
- Same nets, different tightness

**On-screen metrics:**

```
forceHpwlAfter: 18.7
goldenHpwl: 14
```

## Step 5 — Alpha trades speed vs collapse

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Too much alpha stacks cells; too little barely moves. Lock the iteration count and alpha so your eighteen point seven golden stays stable.

**Slide bullets:**

- Neighbor average + center pull
- Starter 52 → ≈18.7
- Next: quadratic with fixed pads

**On-screen metrics:**

```
forceHpwlAfter: 18.7
```

