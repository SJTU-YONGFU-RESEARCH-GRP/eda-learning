# Examples — Hierarchical floorplan

Track A (implement). Use `examples/tiny_modules.json` and `../../common/solvers.py`.

## Algorithm

**cluster then pack clusters**

## Pseudocode

```text
INPUT: clusters of modules
OUTPUT: top-level pack of cluster bboxes
pack each cluster internally (slice/B*/SA)
pack cluster bboxes in outline
GOLDEN teaching: AB left; CDE right @x=5
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
