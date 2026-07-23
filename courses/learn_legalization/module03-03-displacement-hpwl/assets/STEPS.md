# Displacement versus HPWL — step-by-step (for slides / transcript)

**Module:** `module03-03-displacement-hpwl`  
**Lab / algo:** `displacement-hpwl`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=displacement-hpwl&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Cost = HPWL + λ · displacement

![Step 1](steps/01-cost-formula.png)

**Caption (transcript):** Legalization objectives often combine wirelength with a displacement penalty from the pre-legalize layout. Lambda controls how hard you resist moving cells away from global placement.

**Slide bullets:**

- cost = HPWL + λ·disp
- disp = L1 from origin
- Same nets as placement labs

**On-screen metrics:**

```
λ tunable
report both terms
```

## Step 2 — Abacus vs overlap origin

![Step 2](steps/02-abacus-metrics.png)

**Caption (transcript):** Abacus on the overlap seed yields HPWL thirty-eight and displacement four versus the illegal starter. That is the Pareto point with lower movement.

**Slide bullets:**

- origin: OVERLAP
- abacus legal
- HPWL 38 · disp 4

**On-screen metrics:**

```
HPWL: 38
disp: 4
HPWL overlap illegal: n/a
```

## Step 3 — λ = 1 → cost 42

![Step 3](steps/03-lambda-1.png)

**Caption (transcript):** With lambda one, cost equals thirty-eight plus four equals forty-two. Displacement is cheap—one HPWL point buys one unit of movement in the objective.

**Slide bullets:**

- 38 + 1×4 = 42
- abacusCostLambda1 golden
- Compare to Tetris cost

**On-screen metrics:**

```
λ=1 cost: 42
measured: 42
```

## Step 4 — λ = 5 → cost 58

![Step 4](steps/04-lambda-5.png)

**Caption (transcript):** Raise lambda to five: cost becomes thirty-eight plus five times four equals fifty-eight. The same legal layout looks expensive when you punish displacement heavily.

**Slide bullets:**

- 38 + 5×4 = 58
- abacusCostLambda5 golden
- Higher λ favors staying put

**On-screen metrics:**

```
λ=5 cost: 58
measured: 58
```

## Step 5 — Higher λ favors staying put

![Step 5](steps/05-lambda-tradeoff.png)

**Caption (transcript):** When lambda is large, algorithms that minimize displacement—Abacus over Tetris—win the combined cost even if HPWL is slightly worse. Quote λ whenever you compare legalizers.

**Slide bullets:**

- Low λ: wirelength dominates
- High λ: displacement dominates
- Tetris: lower HPWL, higher disp

**On-screen metrics:**

```
abacus: HPWL 38 disp 4
tetris: HPWL 32 disp 6
λ=5 gap widens
```

