# Examples — Slicing tree / polish expression packing

Track A (implement). Use the tiny outline first (`examples/tiny_modules.json`, W×H = 10×8).

## Algorithm

**slicing tree / polish expression packing (H and V cuts)**

## Starter prompts

1. Restate the idea in five bullets (inputs → representation or loop → legality → metrics → output).
2. Load modules A–E; confirm outline area = 80 and module areas sum correctly.
3. Produce a packing (or assignment) and check: every module inside the outline, no pairwise overlap.
4. Report deadspace = outlineArea − Σ(module areas) and packing density = Σ areas / outlineArea.
5. Change one knob (aspect of soft A, a tree edge, a sequence swap, a pin side) and report what moved.

## Expected artifacts

- Coordinates (or representation) for each module
- Legality boolean + deadspace / density
- Short note: why this idea belongs on the floorplanning shelf

## Stretch

Add one hard macro at a fixed (x, y) or nest a 2-module sub-floorplan; keep the same metrics API.
