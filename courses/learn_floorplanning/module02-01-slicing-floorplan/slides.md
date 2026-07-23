---
marp: true
title: Slicing floorplans
paginate: true
---

# Slicing floorplans

A slicing floorplan is built by recursively cutting a rectangle with through-cuts

---

## The idea
- An H operator stacks left and right children as bottom and top (or as specified by your
- A V operator places them side by side
- Evaluating the tree bottom-up yields the size of each composite rectangle
- Polish expressions are postfix: operands then H or V
- Not every packing is slicing

---

## Browser lab track
- Open **slicing-floorplan**
- Load a starter polish expression or tree
- Step through cuts and watch rectangles subdivide
- Read deadspace on the fixed outline
- Change one operator from H to V and see the packing reshape
- Then implement tree evaluation yourself

---

## Implement track
- Define a small tree or polish string over modules A–E
- Evaluate composite widths and heights, then assign (x, y) under the ten-by-eight outline
- Reject trees whose root size exceeds the outline
- Report legality and deadspace
- Keep operator conventions documented in comments

---

## Pitfalls
- Swapping H and V conventions silently flips the packing
- Forgetting that composite size is max-along-cut versus sum-along-cut is the classic bug
- Also: a polish string that is not a valid slicing expression will crash a naive evaluator

---

## Your turn
- Pack a legal slicing floorplan for the starter modules
- Quiz when ready

