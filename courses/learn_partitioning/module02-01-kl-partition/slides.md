---
marp: true
title: Kernighan–Lin bipartition
paginate: true
---

# Kernighan–Lin bipartition

Kernighan–Lin improves an existing bipartition by swapping pairs across the cut

---

## The idea
- Score each unlocked pair by swap gain
- Here the winning prefix is one swap: A with D, gain nine
- Pass one then finds nothing and KL stops at a local optimum for swap moves

---

## Pseudocode
- KL pseudocode builds a locked swap sequence each pass
- Pair gain uses D-values minus twice the edge between the pair
- Open this module's examples file and find the Pseudocode section
- That written sketch is what you implement on the implement track and what the browser

---

## Algorithm sketch
- From the cutsize-twelve bad seed the winning prefix is one swap, A with D
- The sketch lands on ABC versus DE at cut three, then the next pass stops

---

## Algorithm sketch — try these

```
INPUT: bipartition side[], max_passes
OUTPUT: refined side[]
each pass: unlock all; compute D-values
repeat |V|/2: pick unlocked pair max swap gain
  lock pair; update working sides + D
keep prefix with best cumulative gain (>0)
apply prefix; stop if no improving pass
GOLDEN BAD_SEED cut 12 → ABC|DE cut 3
```

---

## Bad seed: cutsize 12
![Bad seed: cutsize 12](assets/steps/01-bad-seed.png)

---

## Score pairwise swaps by gain
![Score pairwise swaps by gain](assets/steps/02-gain-idea.png)

---

## Accept prefix: only A↔D
![Accept prefix: only A↔D](assets/steps/03-accept-swap.png)

---

## Refined partition ABC|DE
![Refined partition ABC|DE](assets/steps/04-final.png)

---

## Next pass finds nothing
![Next pass finds nothing](assets/steps/05-pass1-stop.png)

---

## Browser lab track
- In the browser lab track, open the **kl-partition** lab from the tools shelf
- Load the starter graph, run the algorithm once
- Work the challenges that lock the goldens

---

## Implement track
- In the implement track
- Parse the tiny graph, run the algorithm with a deterministic seed
- Match the browser goldens before you claim the checklist

---

## Pitfalls
- Common traps
- For multilevel flows, verify coarsening before you blame the refiner

---

## Your turn
- Complete the checklist for at least one track, preferably both
- Implement until your metrics match the starter goldens
- When you’re ready, take the short quiz, then continue to the next module

