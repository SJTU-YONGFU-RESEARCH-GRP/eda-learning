# Examples — B*-tree

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**contour pack from B*-tree**

## Pseudocode

```text
INPUT: binary tree (left=right-of, right=above)
OUTPUT: packed (x,y) via contour
root at (0,0)
left child: x ← parent.x + parent.w
right child: y ← above parent (contour)
update horizontal contour after each place
GOLDEN: A@0,0; B.x=A.x+A.w; D.y≥A.h; legal
```

## Starter prompts

1. Implement the pseudocode above (or call the matching `common/` helper).
2. Print the metrics named in the GOLDEN line; match browser / Track A tests.
3. Change one knob and report what moved.

## Expected artifacts

- Outputs listed in the pseudocode OUTPUT line
- Note tying the run to the pseudocode phases

## Stretch

Scale the instance slightly; keep the same metrics API.
