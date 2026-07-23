# Timing-aware clustering — step-by-step (for slides / transcript)

**Module:** `module04-03-timing-aware-clustering`  
**Lab / algo:** `timing-aware-clustering`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=timing-aware-clustering&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Mark critical edges

![Step 1](steps/01-criticality.png)

**Caption (transcript):** Criticality map emphasizes path A–B–C–D: A–B=5, B–C=4, C–D=3. Cutting critical edges hurts timing more than raw wire weight suggests.

**Slide bullets:**

- weighted edge = w × criticality
- Start from BAD_SEED
- FM on the weighted graph

**On-screen metrics:**

```
A|B=5
B|C=4
C|D=3
```

## Step 2 — Reweight then refine

![Step 2](steps/02-weight.png)

**Caption (transcript):** Multiply each edge by its criticality (default 1 if missing). FM now strongly prefers keeping A–B and B–C internal.

**Slide bullets:**

- Protect the critical path
- Still a bipartition FM
- Report plain and weighted cuts

**On-screen metrics:**

```
engine: FM on weighted edges
```

## Step 3 — Land on ABC|DE

![Step 3](steps/03-result.png)

**Caption (transcript):** Timing-aware FM reaches ABC|DE. Plain cutsize is 3; weighted cut (criticality-scaled) is 7.

**Slide bullets:**

- plain=3
- weightedCut=7
- parts: ABC|DE

**On-screen metrics:**

```
plain: 3
weighted: 7
```

## Step 4 — Critical edges uncut

![Step 4](steps/04-protect.png)

**Caption (transcript):** A–B and B–C stay inside ABC. The cut uses less critical bridges C–D and C–E — acceptable plain cut, better timing story.

**Slide bullets:**

- A–B (crit 5) internal
- B–C (crit 4) internal
- Bridge cut carries lower timing risk

**On-screen metrics:**

```
critical path protected
```

## Step 5 — Timing as an objective

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Reweighting turns the same FM kernel into a timing-aware partitioner. Students compare plain vs weighted metrics on one seed.

**Slide bullets:**

- Criticality ≠ congestion
- Same BAD_SEED, different map
- Goldens: plain 3 / weighted 7

**On-screen metrics:**

```
Starter golden: ABC|DE
```

