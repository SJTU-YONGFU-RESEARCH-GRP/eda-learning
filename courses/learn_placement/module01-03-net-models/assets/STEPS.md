# Net models for wirelength — step-by-step (for slides / transcript)

**Module:** `module01-03-net-models`  
**Lab / algo:** `net-models`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=net-models&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Bbox HPWL is the default report

![Step 1](steps/01-bbox-default.png)

**Caption (transcript):** On the golden four-pin net A–B–C–D, the bounding box is two by two, so bbox HPWL is four. That is the cheap, standard teaching metric.

**Slide bullets:**

- Bbox = half-perimeter of pin hull
- Cheap to compute
- Standard report across labs

**On-screen metrics:**

```
ABCD bbox HPWL: 4
Total golden HPWL: 14
```

## Step 2 — Clique sums every pair

![Step 2](steps/02-clique-model.png)

**Caption (transcript):** Clique wirelength adds HPWL of every pairwise edge among the four pins. On golden ABCD that sum is sixteen—four times the bbox number.

**Slide bullets:**

- C(n,2) pairwise spans
- Overestimates multi-pin affinity
- Same pins, larger objective

**On-screen metrics:**

```
clique(ABCD): 16
bbox(ABCD): 4
Ratio: 4× on this instance
```

## Step 3 — Star depends on the hub

![Step 3](steps/03-star-model.png)

**Caption (transcript):** Star sums spokes from a hub to every other pin. With hub A on golden ABCD, star HPWL is eight—between bbox four and clique sixteen.

**Slide bullets:**

- Pick a hub (here A)
- Sum HPWL(hub, other) for each pin
- Hub choice changes the number

**On-screen metrics:**

```
star-from-A: 8
clique: 16
bbox: 4
```

## Step 4 — Same pins, three numbers

![Step 4](steps/04-compare-models.png)

**Caption (transcript):** Bbox four, star-from-A eight, clique sixteen. Pick one model for the reported objective and say which—mixing models is how goldens quietly disagree.

**Slide bullets:**

- Bbox: cheap standard
- Star: hub-sensitive
- Clique: densest affinity

**On-screen metrics:**

```
bbox = 4
star-from-A = 8
clique = 16
```

## Step 5 — Name the model you optimize

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Use one wirelength model in the objective and in the report. The rest of the course quotes bbox HPWL unless a lab explicitly asks for clique or star.

**Slide bullets:**

- Default report = bbox HPWL
- Golden ABCD: 4 / 8 / 16
- Next: force-directed place

**On-screen metrics:**

```
cliqueHpwlGolden4pin: 16
starHpwlGolden4pinFromA: 8
```

