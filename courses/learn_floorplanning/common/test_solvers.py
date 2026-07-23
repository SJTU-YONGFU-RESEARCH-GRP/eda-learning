#!/usr/bin/env python3
"""Golden checks for learn_floorplanning common/."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from goldens import (  # noqa: E402
    BAD_PACK,
    GOLDEN_PACK,
    GOLDEN_PINS,
    MACRO_PACK,
    MODULES,
    OUTLINE,
    OVERLAP_PACK,
    SOFT_A_PACK,
)
from metrics import deadspace, density, is_legal_packing, legality_report  # noqa: E402
from pack import (  # noqa: E402
    eval_polish,
    pack_bstar,
    pack_hierarchical,
    pack_sequence_pair,
)
from goldens import GOLDEN_BSTAR, GOLDEN_POLISH, GOLDEN_SP  # noqa: E402
from solvers import cost  # noqa: E402


def main() -> int:
    assert deadspace(OUTLINE, MODULES) == 57
    assert abs(density(OUTLINE, MODULES) - 0.2875) < 1e-12
    assert is_legal_packing(GOLDEN_PACK, OUTLINE)
    assert not is_legal_packing(BAD_PACK, OUTLINE)
    assert "E" in legality_report(BAD_PACK, OUTLINE)["reason"]
    assert not is_legal_packing(OVERLAP_PACK, OUTLINE)
    polish = eval_polish(GOLDEN_POLISH, MODULES)
    assert polish["w"] == 9 and polish["h"] == 3
    assert is_legal_packing(polish["pack"], OUTLINE)
    assert is_legal_packing(pack_bstar(GOLDEN_BSTAR, MODULES), OUTLINE)
    assert is_legal_packing(
        pack_sequence_pair(GOLDEN_SP["pos"], GOLDEN_SP["neg"], MODULES), OUTLINE
    )
    assert is_legal_packing(SOFT_A_PACK, OUTLINE)
    assert is_legal_packing(MACRO_PACK, OUTLINE)
    assert MACRO_PACK["D"]["x"] == 0 and MACRO_PACK["D"]["y"] == 0
    assert is_legal_packing(pack_hierarchical(), OUTLINE)
    assert cost(GOLDEN_PACK) < 1000 <= cost(BAD_PACK) or cost(BAD_PACK) >= 1000
    assert {p["side"] for p in GOLDEN_PINS} == {"left", "right", "top", "bottom"}
    print("OK — learn_floorplanning common goldens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
