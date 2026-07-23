# Half-perimeter wirelength — step-by-step (for slides / transcript)

**Module:** `module01-01-hpwl-metrics`  
**Lab / algo:** `hpwl-metrics`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=hpwl-metrics&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Starter placement is spread out

![Step 1](steps/01-starter-spread.png)

**Caption (transcript):** Six cells A–F sit on a rough eight-by-eight canvas. The spread-out seed pulls nets long: total half-perimeter wirelength is fifty-two. This is the shared starter for every placement lab.

**Slide bullets:**

- Nodes = movable cells
- Dashed boxes = per-net bounding boxes
- HPWL = sum of (width + height) over nets

**On-screen metrics:**

```
Total HPWL: 52
Nets: 6 (one 4-pin)
Cells: A–F
```

## Step 2 — One net: bbox width plus height

![Step 2](steps/02-one-net.png)

**Caption (transcript):** Net A–B alone has pins at (0,0) and (8,0). Width is eight, height is zero, so HPWL is eight. Every net uses the same bbox rule before you sum.

**Slide bullets:**

- min/max x and y among pins
- HPWL(net) = (maxX−minX) + (maxY−minY)
- Two-pin nets reduce to Manhattan span

**On-screen metrics:**

```
Net A–B HPWL: 8
Net C–D HPWL: 8
4-pin ABCD HPWL: 16
```

## Step 3 — Sum six nets to fifty-two

![Step 3](steps/03-sum-nets.png)

**Caption (transcript):** Four two-pin nets at eight each, the four-pin ABCD net at sixteen, and E–F at four: eight times four plus sixteen plus four equals fifty-two. That is the starter golden.

**Slide bullets:**

- A–B, C–D, A–C, B–D: 8 each
- ABCD: 16 · E–F: 4
- Never celebrate collapse to one point

**On-screen metrics:**

```
2-pin×4 = 32
4-pin = 16
E–F = 4
Total = 52
```

## Step 4 — Golden placement drops to fourteen

![Step 4](steps/04-golden-compact.png)

**Caption (transcript):** The compact reference tucks A–D into a two-by-two block near the center. Same nets, shorter boxes: total HPWL falls from fifty-two to fourteen.

**Slide bullets:**

- Same netlist, tighter coordinates
- ABCD bbox shrinks from 16 → 4
- Reference for later algorithms

**On-screen metrics:**

```
Starter HPWL: 52
Golden HPWL: 14
Delta: −38
```

## Step 5 — HPWL is the teaching yardstick

![Step 5](steps/05-takeaway.png)

**Caption (transcript):** Report total HPWL before and after every move. Fifty-two versus fourteen is the starter story—but a tiny total with stacked cells is not a usable placement.

**Slide bullets:**

- Compute bbox HPWL per net, then sum
- Starter 52 · golden 14
- Next: clique and star models

**On-screen metrics:**

```
starterHpwl: 52
goldenHpwl: 14
```

