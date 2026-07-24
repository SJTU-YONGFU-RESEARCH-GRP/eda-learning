# DRC spacing lite — step-by-step (for slides / transcript)

**Module:** `module03-01-drc-spacing`  
**Lab / algo:** `drc-spacing`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=drc-spacing&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Lite checker

![Step 1](steps/01-lite.png)

**Caption (transcript):** Same-layer parallel segments one grid apart fail.

**Slide bullets:**

- Toy rule
- Not full deck

**On-screen metrics:**

```
minDist=1
```

## Step 2 — Spread pass

![Step 2](steps/02-pass.png)

**Caption (transcript):** Spread layered routes pass on the toy.

**Slide bullets:**

- pass=true

**On-screen metrics:**

```
Spread starter
```

## Step 3 — Violation demo

![Step 3](steps/03-fail.png)

**Caption (transcript):** Adjacent M1 rows at y=2 and y=3 fail minDist=1.

**Slide bullets:**

- Fail case

**On-screen metrics:**

```
Teaching
```

## Step 4 — After route

![Step 4](steps/04-route.png)

**Caption (transcript):** Run checker on learner sequential routes.

**Slide bullets:**

- Check button

**On-screen metrics:**

```
Learner routes
```

## Step 5 — Real DRC

![Step 5](steps/05-real.png)

**Caption (transcript):** Production routers use full width/spacing/via rules.

**Slide bullets:**

- learn_drc next

**On-screen metrics:**

```
Signoff
```

