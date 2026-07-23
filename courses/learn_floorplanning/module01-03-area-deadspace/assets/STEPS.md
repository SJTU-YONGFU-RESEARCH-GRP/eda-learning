# Area, packing density, whitespace/deadspace — step-by-step (for slides / transcript)

**Module:** `module01-03-area-deadspace`  
**Lab / algo:** `area-deadspace`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=area-deadspace&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Module areas sum to 23

![Step 1](steps/01-areas.png)

**Caption (transcript):** Add the five module areas: A is six, B is six, C is four, D is three, E is four. That is twenty-three units of silicon that must fit in the outline.

**Slide bullets:**

- A 3×2=6
- B 2×3=6
- C 2×2=4
- D 3×1=3
- E 2×2=4

**On-screen metrics:**

```
moduleAreaSum: 23
```

## Step 2 — Outline area is 80

![Step 2](steps/02-outline-area.png)

**Caption (transcript):** Ten times eight is eighty. That is the budget. Module area twenty-three leaves whitespace—deadspace—equal to fifty-seven.

**Slide bullets:**

- outlineArea = W×H = 80
- deadspace = 80 − 23 = 57

**On-screen metrics:**

```
outlineArea: 80
deadspace: 57
```

## Step 3 — Density is 0.2875

![Step 3](steps/03-density.png)

**Caption (transcript):** Density is module area over outline area: twenty-three over eighty equals zero point two eight seven five. Whitespace fraction is zero point seven one two five.

**Slide bullets:**

- density = 23/80 = 0.2875
- whitespace = 57/80 = 0.7125
- Placement-independent for fixed sizes

**On-screen metrics:**

```
density: 0.2875
whitespace: 0.7125
```

## Step 4 — Metrics need a legal pack

![Step 4](steps/04-legal-metrics.png)

**Caption (transcript):** On the golden legal packing these numbers are honest. On an overflow packing the area math still computes, but the floorplan is invalid—do not celebrate density on illegal layouts.

**Slide bullets:**

- Golden packing is legal
- Deadspace 57 is the teaching golden
- Illegal packs still report area math

**On-screen metrics:**

```
legal: true
deadspace: 57
density: 0.2875
```

## Step 5 — Report area trio every time

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Habit: print module area, outline area, deadspace, and density with every packing. Representations later change geometry; this trio stays the scoreboard.

**Slide bullets:**

- Always report 23 / 80 / 57 / 0.2875
- Density < 1 means whitespace remains
- Next: slicing polish that fits BB 9×3

**On-screen metrics:**

```
golden: 23, 80, 57, 0.2875
```

