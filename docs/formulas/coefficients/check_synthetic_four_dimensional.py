"""Check reversible socle reduction, including dependent nonzero lower carries."""
from itertools import product
import json
from pathlib import Path
from verify_four_dimensional_root_powers import replay_two_primary

out = Path(__file__).resolve().parent
cases = []
for (q0, q1), signed, offset in product([(2, 2), (4, 2), (8, 4)], [0, 1], range(4)):
    record = {
        "inputModel": {"s1": [signed]},
        "generators": [
            {"name": "D", "layer": 0, "quotientOrder": 4},
            {"name": "C", "layer": 1, "quotientOrder": 2},
            {"name": "M0", "layer": 2, "quotientOrder": 2},
            {"name": "M1", "layer": 2, "quotientOrder": 2},
            {"name": "P0", "layer": 3, "quotientOrder": q0},
            {"name": "P1", "layer": 3, "quotientOrder": q1}],
        "presentation": [[4, 0, 0, 0, 0, 0], [-1, 2, 0, 0, 0, 0],
                         [0, -1, 2, 0, 0, 0], [-1, 0, 0, 2, 0, 0],
                         [0, -(offset % 2), -1, 0, q0, 0],
                         [-(offset // 2), 0, -1, 0, 0, q1]]}
    if signed:
        record["presentation"].append([offset, 1, 0, 1, 0, 0])
    result = replay_two_primary(record)
    assert len(result["socle_eliminations"]) == 1
    assert len(result["kernel_power_targets"]) == 1
    assert result["kernel_power_targets"][0]["had_nonzero_initial_image"]
    assert result["kernel_power_targets"][0]["offset_vector_nonzero"]
    cases.append({"name": f"q{q0}_{q1}_sign{signed}_offset{offset}",
                  "record": record, "replay": result})
receipt = {"status": "PASS", "scope": "Synthetic filtered abelian integer presentations; no physical cochain claim.",
           "cases": len(cases), "dependent_images_eliminated": len(cases),
           "nonzero_lower_offsets_preserved": len(cases), "records": cases}
(out / "SYNTHETIC_FOUR_DIMENSIONAL_REPLAY.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({k:v for k,v in receipt.items() if k != "records"}, indent=2))
