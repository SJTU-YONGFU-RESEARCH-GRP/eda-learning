# Examples — Macro placement

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**fix hard macro then pack free**

## Pseudocode

```text
INPUT: macros F locked (x,y), free modules
OUTPUT: legal pack; macros never move
place each f∈F at locked pose (macro flag)
pack free modules around F obstacles
fail if any macro drifts
GOLDEN free: D@(0,2); macro: D@(0,0)
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
