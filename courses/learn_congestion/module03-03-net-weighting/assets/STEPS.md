# Congestion-aware net weighting — step-by-step (for slides / transcript)

**Module:** `module03-03-net-weighting`  
**Lab / algo:** `net-weighting`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=net-weighting&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Weight hot nets

![Step 1](steps/01-idea.png)

**Caption (transcript):** Nets through congested GCells get larger weights for weighted place.

**Slide bullets:**

- w=1+β·mean cong

**On-screen metrics:**

```
β=1 demo
```

## Step 2 — Mean under bbox

![Step 2](steps/02-bbox.png)

**Caption (transcript):** Average congestion over GCells under the net bbox—not the whole chip.

**Slide bullets:**

- Local mean

**On-screen metrics:**

```
6 nets
```

## Step 3 — 4-pin ranks high

![Step 3](steps/03-rank.png)

**Caption (transcript):** On a cluster, the 4-pin net outranks short E–F.

**Slide bullets:**

- w4 ≥ w5

**On-screen metrics:**

```
Timing cousin
```

## Step 4 — Spread lowers weights

![Step 4](steps/04-cool.png)

**Caption (transcript):** As congestion falls, weights ease back toward 1.

**Slide bullets:**

- Coupled to map

**On-screen metrics:**

```
Still report overflow
```

## Step 5 — Use in placer

![Step 5](steps/05-use.png)

**Caption (transcript):** Weighted HPWL pulls soft from hotspots—pair with inflators.

**Slide bullets:**

- Two knobs

**On-screen metrics:**

```
Feedback lab next
```

