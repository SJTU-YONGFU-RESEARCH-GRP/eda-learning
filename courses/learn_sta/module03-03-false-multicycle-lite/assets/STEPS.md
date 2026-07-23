# False and multicycle paths (engine view) — step-by-step (for slides / transcript)

**Module:** `module03-03-false-multicycle-lite`  
**Lab / algo:** `false-multicycle-lite`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=false-multicycle-lite&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Normal single-cycle setup

![Step 1](steps/01-normal-check.png)

**Caption (transcript):** Without exceptions, required at out is one period (10) and setup slack is 6.8. That is the baseline the exceptions will change.

**Slide bullets:**

- cycles = 1
- R(out)=10
- slack=6.8

**On-screen metrics:**

```
setup slack=6.8
```

## Step 2 — Multicycle widens the required window

![Step 2](steps/02-multicycle.png)

**Caption (transcript):** A setup multicycle of 2 means required = 2 × period = 20. Slack becomes 16.8. The graph did not change—only the endpoint budget did.

**Slide bullets:**

- R = period × cycles
- cycles=2 → R=20
- slack=16.8

**On-screen metrics:**

```
required out=20
setup slack=16.8
```

## Step 3 — False path disables an arc

![Step 3](steps/03-false-path.png)

**Caption (transcript):** Marking the bridge net u1/Y→u2/A as false removes it from propagation. Downstream pins no longer see the real wavefront—u2/A falls back to 0 in this lite engine.

**Slide bullets:**

- Disable arc u1/Y|u2/A
- Propagation skips it
- Lite model: orphan pin → 0

**On-screen metrics:**

```
disabled: u1/Y|u2/A
A(u1/Y)=1.2
A(u2/A)=0
```

## Step 4 — Exceptions are engine data

![Step 4](steps/04-engine-data.png)

**Caption (transcript):** SDC authoring lives in learn_sdc. Here you only consume false-path and multicycle as flags the timer reads—same idea as production engines.

**Slide bullets:**

- Constraints → engine inputs
- Not GUI click-paths
- Wrong exception → wrong slack

**On-screen metrics:**

```
false-path: remove arc
multicycle: scale required
```

## Step 5 — Always recheck after exceptions

![Step 5](steps/05-recheck.png)

**Caption (transcript):** Apply exceptions, then recompute tags and slack. Never keep a stale 6.8 after a multicycle or false-path change.

**Slide bullets:**

- Apply → recompute → report
- Stale tags lie
- Next: offline compare habit

**On-screen metrics:**

```
normal 6.8
multicycle 16.8
false-path breaks the bridge
```

