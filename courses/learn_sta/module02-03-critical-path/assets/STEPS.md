# Critical path — step-by-step (for slides / transcript)

**Module:** `module02-03-critical-path`  
**Lab / algo:** `critical-path`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=critical-path&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Start from the worst endpoint

![Step 1](steps/01-worst-sink.png)

**Caption (transcript):** Critical-path traceback begins at the endpoint with the worst setup slack. Here that is out with slack 6.8—still the only sink.

**Slide bullets:**

- Pick the worst slack sink
- Trace into arrival tags
- Do not guess from the source

**On-screen metrics:**

```
sink: out
setup slack: 6.8
```

## Step 2 — Step to the matching predecessor

![Step 2](steps/02-match-pred.png)

**Caption (transcript):** At each pin, choose a predecessor u where A(u) + delay equals A(v). That arc is on the critical path.

**Slide bullets:**

- Match A(u)+d to A(v)
- Ties: prefer larger A(u)
- Walk until a source

**On-screen metrics:**

```
out ← u2/Y (+0.2)
u2/Y ← u2/A (+1.5)
```

## Step 3 — The full golden path

![Step 3](steps/03-full-path.png)

**Caption (transcript):** The complete critical path is in → u1/A → u1/Y → u2/A → u2/Y → out. Arrival at out equals the sum of arc delays along this path: 3.2.

**Slide bullets:**

- Six pins on one path
- Path delay = A(out)
- Golden list matches PROP_GOLDENS

**On-screen metrics:**

```
in → u1/A → u1/Y → u2/A → u2/Y → out
path delay = 3.2
```

## Step 4 — Fix the path, not a random gate

![Step 4](steps/04-why-it-matters.png)

**Caption (transcript):** Optimization and ECO work chase critical paths. Tag matching keeps you honest when reconvergence exists—on this chain there is only one route.

**Slide bullets:**

- Trace before you resize
- Reconvergence needs care
- Toy chain has one route

**On-screen metrics:**

```
reconvergence: none
cells on path: u1, u2
```

## Step 5 — Slack and path travel together

![Step 5](steps/05-slack-path.png)

**Caption (transcript):** Reports pair worst slack with its path. Next labs edit delays and exceptions—always re-trace after the tags change.

**Slide bullets:**

- Slack names the problem
- Path names where to look
- Re-trace after edits

**On-screen metrics:**

```
slack 6.8 @ out
path length 6
```

