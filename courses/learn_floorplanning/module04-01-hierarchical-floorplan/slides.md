---
marp: true
title: Hierarchical floorplans
paginate: true
---

# Hierarchical floorplans

Large designs floorplan recursively

---

## The idea
- Pick a parent region inside the outline
- Floorplan a subset of modules inside that region as if it were its own fixed outline
- Place sibling regions, then recurse
- Top-level deadspace still uses the chip outline area
- Keep region outlines legal with respect to their parent

---

## Browser lab track
- Open **hierarchical-floorplan**
- Load a two-level starter: a parent outline and two child groups
- Pack inside each child, then place children in the parent
- Inspect metrics at both levels
- Then implement nested packing in Track A

---

## Implement track
- Partition A–E into two groups
- Floorplan each group into a sub-rectangle
- Verify no group overflows its region and regions don’t overlap
- Report global deadspace

---

## Pitfalls
- Optimizing children while ignoring parent legality leaves you with beautiful
- Don’t double-count module area across levels
- Align coordinates to a single global origin when composing

---

## Your turn
- Ship one hierarchical packing for the tiny instance
- Next: assign I/O pins to the chip boundary

