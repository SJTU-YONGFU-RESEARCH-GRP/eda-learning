# Multi-pin tree (Steiner-lite) — step-by-step (for slides / transcript)

**Module:** `module02-07-multipin-tree`  
**Lab / algo:** `multipin-tree`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=multipin-tree&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Four-pin net

![Step 1](steps/01-net4.png)

**Caption (transcript):** Net [A,B,C,D] needs a tree, not a single two-pin path.

**Slide bullets:**

- Star demo
- 4 legs

**On-screen metrics:**

```
Net index 4
```

## Step 2 — Bbox center

![Step 2](steps/02-center.png)

**Caption (transcript):** Star hub at mean GCell of pins (clamped).

**Slide bullets:**

- Steiner lite
- Toy only

**On-screen metrics:**

```
Hub GCell
```

## Step 3 — Four L legs

![Step 3](steps/03-legs.png)

**Caption (transcript):** Each pin gets an L-route from the hub in the full sequential pass.

**Slide bullets:**

- 4 paths
- Edge sharing

**On-screen metrics:**

```
Highlight net 4
```

## Step 4 — Shared edges

![Step 4](steps/04-usage.png)

**Caption (transcript):** Multi-pin trees reuse edges—overflow adds up.

**Slide bullets:**

- Sum usage
- Cap=2

**On-screen metrics:**

```
Watch corridors
```

## Step 5 — Two-pin nets

![Step 5](steps/05-two.png)

**Caption (transcript):** Short nets E–F stay single L paths.

**Slide bullets:**

- Mix topologies
- Six nets total

**On-screen metrics:**

```
E–F short
```

