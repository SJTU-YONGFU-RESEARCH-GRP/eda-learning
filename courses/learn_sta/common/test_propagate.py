#!/usr/bin/env python3
"""Golden checks for learn_sta propagation helpers."""
from __future__ import annotations

from pathlib import Path

from propagate import (
    PROP_GOLDENS,
    critical_path_to,
    hold_slack,
    incremental_arrival,
    propagate_arrival,
    propagate_required,
    setup_slack,
)
from timing_io import load_timing

ROOT = Path(__file__).resolve().parent
t = load_timing(ROOT / "tiny_timing.json")


def _eq_map(a, b):
    assert set(a) == set(b)
    for k in a:
        assert abs(a[k] - b[k]) < 1e-9, (k, a[k], b[k])


def main() -> None:
    arr = propagate_arrival(t)
    assert arr is not None
    _eq_map(arr, PROP_GOLDENS["arrival"])

    req = propagate_required(t, mode="setup")
    assert req is not None
    _eq_map(req, PROP_GOLDENS["required_setup"])

    assert abs(setup_slack(arr, req, "out") - PROP_GOLDENS["setup_slack_out"]) < 1e-9

    req_h = propagate_required(t, mode="hold")
    assert abs(hold_slack(arr, req_h, "out") - PROP_GOLDENS["hold_slack_out"]) < 1e-9

    path = critical_path_to(t, arr, "out")
    assert path == PROP_GOLDENS["critical_path"]

    inc = PROP_GOLDENS["incremental"]
    _tt, arr2, inv = incremental_arrival(
        t, inc["edit_from"], inc["edit_to"], inc["new_delay"], arr
    )
    assert abs(arr2["out"] - inc["arrival_out"]) < 1e-9
    assert set(inv) == set(inc["invalidated"])
    req2 = propagate_required(_tt, mode="setup")
    assert abs(setup_slack(arr2, req2, "out") - inc["setup_slack_out"]) < 1e-9

    mc = PROP_GOLDENS["multicycle"]
    req_mc = propagate_required(t, mode="setup", setup_cycles=mc["setup_cycles"])
    assert abs(req_mc["out"] - mc["required_out"]) < 1e-9
    assert abs(setup_slack(arr, req_mc, "out") - mc["setup_slack_out"]) < 1e-9

    # False path: disable bridge net → out has no arrival via chain (treat as missing)
    disabled = {("u1/Y", "u2/A")}
    arr_fp = propagate_arrival(t, disable_arcs=disabled)
    # u2/A and below still get values from... actually no preds if disabled - u2/A has only that pred
    assert arr_fp["u1/Y"] == 1.2
    # With disabled arc, u2/A has no enabled preds → 0 in our impl
    assert arr_fp["u2/A"] == 0.0

    print("ok propagate goldens: arrival/required/slack/path/incremental/multicycle")


if __name__ == "__main__":
    main()
