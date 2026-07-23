# Quadratic placement — step-by-step (for slides / transcript)

**Module:** `module02-03-quadratic-place`  
**Lab / algo:** `quadratic-place`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=quadratic-place&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Pads A and D stay fixed

![Step 1](steps/01-pads-fixed.png)

**Caption (transcript):** Quadratic-lite averages neighbors under fixed pads. Here A stays at (0,0) and D at (8,8)—anchors that free cells must respect.

**Slide bullets:**

- Fixed pads: A, D
- Gauss–Seidel neighbor average
- Blend retains some prior coord

**On-screen metrics:**

```
HPWL: 52
A @ (0,0) · D @ (8,8)
```

## Step 2 — Free cells slide toward neighbors

![Step 2](steps/02-free-cells.png)

**Caption (transcript):** B, C, E, and F update toward the average of their neighbors while A and D hold. The system cannot collapse onto the pads.

**Slide bullets:**

- Update only non-pad cells
- blend ≈ 0.55 toward average
- Pads raise HPWL vs free force

**On-screen metrics:**

```
Free: B, C, E, F
Fixed: A, D
```

## Step 3 — After quadratic: HPWL forty-eight

![Step 3](steps/03-after-quad.png)

**Caption (transcript):** Default iterations reach total HPWL forty-eight. Pads constrain the free cells, so you will not match free force’s eighteen point seven.

**Slide bullets:**

- Starter 52 → 48
- Pads keep the spread
- Teaching point: constraints cost WL

**On-screen metrics:**

```
Before: 52
After: 48
Measured: 48
```

## Step 4 — Quadratic vs unconstrained force

![Step 4](steps/04-vs-force.png)

**Caption (transcript):** Force without pads reaches about eighteen point seven; quadratic with pads stays at forty-eight. Same seed, different constraint story.

**Slide bullets:**

- Force (free): ≈18.7
- Quadratic (pads): 48
- Both beat starter 52

**On-screen metrics:**

```
forceHpwlAfter: 18.7
quadraticHpwlAfter: 48
```

## Step 5 — Pads anchor the solve

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Always declare fixed cells. On this instance the quadratic golden is forty-eight—modest wirelength win, honest about pad constraints.

**Slide bullets:**

- Fixed A, D
- Starter 52 → 48
- Next: analytical density stage

**On-screen metrics:**

```
quadraticHpwlAfter: 48
```

