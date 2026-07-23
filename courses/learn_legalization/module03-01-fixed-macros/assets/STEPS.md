# Fixed macros — step-by-step (for slides / transcript)

**Module:** `module03-01-fixed-macros`  
**Lab / algo:** `fixed-macros`  
**Viewer:** `/tools/algorithm-walkthrough/?algo=fixed-macros&step=1`

Use each **Caption** as spoken prose (or a shortened slide note).
Use **Bullets** on the PPT; pair with the PNG in `assets/steps/`.

## Step 1 — Macro D locked at (8, 4)

![Step 1](steps/01-d-locked.png)

**Caption (transcript):** Cell D is a fixed macro at (8, 4) on the top row—width two covers sites eight and nine. Every legalizer must leave D untouched while packing movables around it.

**Slide bullets:**

- FIXED_MACROS.D = (8,4)
- Width 2 blocks sites 8–9
- Movables: A,B,C,E,F

**On-screen metrics:**

```
D fixed
top row y=4
```

## Step 2 — Abacus with fixed macros

![Step 2](steps/02-abacus-fixed.png)

**Caption (transcript):** Run Abacus with the fixed map: D is placed first, occupied sites on row four block C from sliding into the macro. Movable cells trial rows respecting blocked intervals.

**Slide bullets:**

- opts.fixed = FIXED_MACROS
- Blocked intervals per row
- Pack around macro footprint

**On-screen metrics:**

```
engine: abacusLegalize
fixed: D
```

## Step 3 — D never moves

![Step 3](steps/03-d-never-moves.png)

**Caption (transcript):** After Abacus with fixed macros, D remains at (8, 4). Legality report includes a macro check—any drift off the lock fails the run.

**Slide bullets:**

- D @ (8,4) before and after
- Macro legality enforced
- disp still 4 on overlap seed

**On-screen metrics:**

```
D.x=8 D.y=4
disp: 4
legal: true
```

## Step 4 — Still legal, displacement 4

![Step 4](steps/04-still-legal.png)

**Caption (transcript):** With D fixed, Abacus still legalizes A, B, C, E, and F with total displacement four—the same as the unconstrained Abacus run on this instance because D never moved in either.

**Slide bullets:**

- Full legality: true
- No overlap with macro
- Movables avoid sites 8–9 on row 4

**On-screen metrics:**

```
abacusDisp: 4
HPWL: 38
legal: true
```

## Step 5 — Movables avoid macro sites

![Step 5](steps/05-avoid-macro.png)

**Caption (transcript):** C lands on row four at x four—left of E at zero, right of the macro gap. Packing algorithms must treat fixed macros as obstacles, not soft preferences.

**Slide bullets:**

- C @ (4,4) clears D
- E @ (0,4) on same row
- Never slide through macro

**On-screen metrics:**

```
macro sites reserved
row-4 pack around D
```

