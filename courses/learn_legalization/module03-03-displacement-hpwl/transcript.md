# Displacement versus HPWL

**Module id:** module03-03-displacement-hpwl
**Lab:** displacement-hpwl
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Displacement versus HPWL

Legalization cost combines HPWL and displacement: cost equals HPWL plus lambda times displacement from the pre-legalize layout. Abacus on the overlap seed reports HPWL thirty-eight and displacement four.

## Slide 2 — The idea

Lambda one gives cost forty-two; lambda five gives cost fifty-eight on the same legal Abacus result. Higher lambda favors staying near global placement even when wirelength could be slightly better under a different packer.

<!-- algorithm-walkthrough -->

## Slide 3 — Cost = HPWL + λ · displacement

![Cost = HPWL + λ · displacement](assets/steps/01-cost-formula.png)

Legalization objectives often combine wirelength with a displacement penalty from the pre-legalize layout. Lambda controls how hard you resist moving cells away from global placement.

## Slide 4 — Abacus vs overlap origin

![Abacus vs overlap origin](assets/steps/02-abacus-metrics.png)

Abacus on the overlap seed yields HPWL thirty-eight and displacement four versus the illegal starter. That is the Pareto point with lower movement.

## Slide 5 — λ = 1 → cost 42

![λ = 1 → cost 42](assets/steps/03-lambda-1.png)

With lambda one, cost equals thirty-eight plus four equals forty-two. Displacement is cheap—one HPWL point buys one unit of movement in the objective.

## Slide 6 — λ = 5 → cost 58

![λ = 5 → cost 58](assets/steps/04-lambda-5.png)

Raise lambda to five: cost becomes thirty-eight plus five times four equals fifty-eight. The same legal layout looks expensive when you punish displacement heavily.

## Slide 7 — Higher λ favors staying put

![Higher λ favors staying put](assets/steps/05-lambda-tradeoff.png)

When lambda is large, algorithms that minimize displacement—Abacus over Tetris—win the combined cost even if HPWL is slightly worse. Quote λ whenever you compare legalizers.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **displacement-hpwl** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
