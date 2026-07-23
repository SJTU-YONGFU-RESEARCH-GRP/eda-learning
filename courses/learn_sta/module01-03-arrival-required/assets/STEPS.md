# Arrival and required times — step-by-step (for slides / transcript)

**Module:** `module01-03-arrival-required`  
**Lab / algo:** `arrival-required`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=arrival-required&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Seed arrival at the source

![Step 1](steps/01-seed-arrival.png)

**Caption (transcript):** Set arrival at in to zero for the launch edge. Every other pin waits for its predecessors.

**Slide bullets:**

- Arrival at sources starts the wavefront
- Here A(in) = 0
- No delay yet on the first net

**On-screen metrics:**

```
A(in) = 0
```

## Step 2 — Propagate arrival forward

![Step 2](steps/02-forward-wave.png)

**Caption (transcript):** For each pin in topo order, arrival is the max over predecessors of A(pred) + delay. At out the wavefront reaches 3.2.

**Slide bullets:**

- A(v) = max(A(u) + d(u→v))
- Cell delays dominate this toy path
- Golden A(out) = 3.2

**On-screen metrics:**

```
A(u1/Y)=1.2
A(u2/A)=1.5
A(u2/Y)=3.0
A(out)=3.2
```

## Step 3 — Seed required at the sink

![Step 3](steps/03-seed-required.png)

**Caption (transcript):** For a single-cycle setup check, required at out equals the clock period—here 10.

**Slide bullets:**

- Setup capture edge sets R(out)
- R(out) = period × cycles
- Default cycles = 1 → 10

**On-screen metrics:**

```
period = 10
R(out) = 10
```

## Step 4 — Propagate required backward

![Step 4](steps/04-backward-wave.png)

**Caption (transcript):** Walk reverse topo order. Required at a pin is the min over successors of R(succ) − delay. At in, required becomes 6.8.

**Slide bullets:**

- R(u) = min(R(v) − d(u→v))
- Tightest successor wins
- Golden R(in) = 6.8

**On-screen metrics:**

```
R(u2/Y)=9.8
R(u1/Y)=8.0
R(u1/A)=6.8
R(in)=6.8
```

## Step 5 — Keep both tags on every pin

![Step 5](steps/05-both-tags.png)

**Caption (transcript):** Arrival and required live together. Slack at a pin is R − A for setup. Next labs turn those tags into slack and a critical path.

**Slide bullets:**

- Forward then backward
- Same graph, two tag maps
- A(out)=3.2 and R(out)=10

**On-screen metrics:**

```
A(out)=3.2
R(out)=10
next: slack = 6.8
```

