---
marp: true
title: Kernighan–Lin refinement
paginate: true
---

# Kernighan–Lin refinement

Kernighan–Lin improves an existing bipartition by swapping pairs across the cut

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
- In the browser lab, show the seed only, then run KL
- Check the challenges for cutsize twelve, the A–D swap, and the final cutsize three

---

## Implement track
- Load the tiny graph and the bad seed
- Print cutsize twelve before you start
- Run the reference KL solver and confirm it accepts A–D

---

## Implement track — try these

```
# pwd — print working directory
pwd

# ls examples — graph + seed partition
ls examples

# run full KL refinement on the bad seed
export PYTHONPATH=../common
python ../common/solvers.py examples/tiny_graph.json --mode kl --seed examples/seed_partition.json

```

---

## Pitfalls to watch
- Forgetting rollback is the classic bug
- Stale D-values after a swap pick the wrong pair next
- And if your seed isn’t labeled zero and one, the gain math won’t match

---

## Your turn
- Reproduce cut twelve to three with the accepted A–D swap
- Finish the checklist and quiz

