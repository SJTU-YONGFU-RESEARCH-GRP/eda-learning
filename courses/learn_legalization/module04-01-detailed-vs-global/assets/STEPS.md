# Detailed versus global legalize — step-by-step (for slides / transcript)

**Module:** `module04-01-detailed-vs-global`  
**Lab / algo:** `detailed-vs-global`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=detailed-vs-global&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Global = Tetris, disp 6

![Step 1](steps/01-global-tetris.png)

**Caption (transcript):** Global legalize lite maps to Tetris-style nearest-row shelf pack. On the overlap seed it legalizes with displacement six and HPWL thirty-two.

**Slide bullets:**

- globalLegalize → tetris
- single-row shelf for A,B,C
- fast, simple pipeline stage

**On-screen metrics:**

```
globalDisp: 6
HPWL: 32
legal: true
```

## Step 2 — Detailed = Abacus, disp 4

![Step 2](steps/02-detailed-abacus.png)

**Caption (transcript):** Detailed legalize lite maps to Abacus row trial. Same seed, both legal—but displacement drops to four by spreading A, B, C across rows.

**Slide bullets:**

- detailedLegalize → abacus
- cross-row assignment
- lower L1 movement

**On-screen metrics:**

```
detailedDisp: 4
HPWL: 38
legal: true
```

## Step 3 — Both pipelines legal

![Step 3](steps/03-both-legal.png)

**Caption (transcript):** Global and detailed both pass legality on the overlap seed. The difference is how far cells move and how HPWL shifts—thirty-two versus thirty-eight here.

**Slide bullets:**

- Same starter coordinates
- Both isLegal true
- Metrics tell the story

**On-screen metrics:**

```
global legal: true
detailed legal: true
HPWL delta: 6
```

## Step 4 — Side-by-side metrics

![Step 4](steps/04-side-by-side.png)

**Caption (transcript):** Global Tetris: disp six, HPWL thirty-two. Detailed Abacus: disp four, HPWL thirty-eight. Neither dominates on both axes—pick by your displacement budget.

**Slide bullets:**

- global: disp 6 HPWL 32
- detailed: disp 4 HPWL 38
- Report both in regressions

**On-screen metrics:**

```
globalDisp: 6
detailedDisp: 4
tetrisHpwl: 32
abacusHpwl: 38
```

## Step 5 — Pick detailed when displacement is tight

![Step 5](steps/05-pick-detailed.png)

**Caption (transcript):** Production flows often run a fast global legalize, then a detailed pass when timing or continuity needs cells near global targets. On this toy, that is Abacus over Tetris.

**Slide bullets:**

- Tight disp budget → detailed
- HPWL-first → global Tetris
- Course wrap: offline compare next

**On-screen metrics:**

```
detailedDisp: 4
globalDisp: 6
both legal on overlap seed
```

