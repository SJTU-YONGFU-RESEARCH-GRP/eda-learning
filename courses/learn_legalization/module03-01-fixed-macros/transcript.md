# Fixed macros

**Module id:** module03-01-fixed-macros
**Lab:** fixed-macros
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Fixed macros

Macro D is locked at (8, 4) on the top row—width two blocks sites eight and nine. Run Abacus with fixed macros: D never moves, movables pack around the obstacle, and the run stays legal with displacement four on this instance.

## Slide 2 — The idea

Fixed cells are placed first; occupied intervals block shelf and Abacus trials on that row. Legality adds a macro check—any drift off the lock fails. Movable cells must route around macro sites, not slide through them.

<!-- algorithm-walkthrough -->

## Slide 3 — Macro D locked at (8, 4)

![Macro D locked at (8, 4)](assets/steps/01-d-locked.png)

Cell D is a fixed macro at (8, 4) on the top row—width two covers sites eight and nine. Every legalizer must leave D untouched while packing movables around it.

## Slide 4 — Abacus with fixed macros

![Abacus with fixed macros](assets/steps/02-abacus-fixed.png)

Run Abacus with the fixed map: D is placed first, occupied sites on row four block C from sliding into the macro. Movable cells trial rows respecting blocked intervals.

## Slide 5 — D never moves

![D never moves](assets/steps/03-d-never-moves.png)

After Abacus with fixed macros, D remains at (8, 4). Legality report includes a macro check—any drift off the lock fails the run.

## Slide 6 — Still legal, displacement 4

![Still legal, displacement 4](assets/steps/04-still-legal.png)

With D fixed, Abacus still legalizes A, B, C, E, and F with total displacement four—the same as the unconstrained Abacus run on this instance because D never moved in either.

## Slide 7 — Movables avoid macro sites

![Movables avoid macro sites](assets/steps/05-avoid-macro.png)

C lands on row four at x four—left of E at zero, right of the macro gap. Packing algorithms must treat fixed macros as obstacles, not soft preferences.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **fixed-macros** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
