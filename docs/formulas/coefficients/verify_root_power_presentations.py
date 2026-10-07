"""Replay exact marked-basis/row changes in all saved 3D presentations.

This reads completed records. It neither computes a cochain product nor
launches classification, nor computes a new Smith normal form.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[3])
parser.add_argument("--output-directory", type=Path, default=Path(__file__).resolve().parent)
arguments = parser.parse_args()
ROOT = arguments.repository_root.resolve()
PUBLIC = ROOT
OUT = arguments.output_directory.resolve()
OUT.mkdir(parents=True, exist_ok=True)
INDEX = ROOT / "results/computed_examples/index.json"


def add_scaled(left, right, factor):
    return [a + factor*b for a, b in zip(left, right)]


def unit(n, j, value=1):
    row = [0]*n
    row[j] = value
    return row


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def replay(case):
    path = PUBLIC / case["result"]
    record = json.loads(path.read_text())
    generators, rows = record["generators"], record["presentation"]
    n = len(generators)
    assert all(len(row) == n for row in rows)
    finite = [i for i, g in enumerate(generators) if g["quotientOrder"]]
    majorana = [i for i, g in enumerate(generators) if g["layer"] == 2]
    pip = [i for i, g in enumerate(generators) if g["layer"] == 3]
    torsion_pip = [i for i in pip if generators[i]["quotientOrder"]]
    assert len(torsion_pip) <= 1
    assert all(generators[i]["quotientOrder"] == 2 for i in majorana + torsion_pip)
    power_row = {i: j for j, i in enumerate(finite)}
    for i, j in power_row.items():
        assert rows[j][i] == generators[i]["quotientOrder"]
        assert all(rows[j][k] == 0 for k in range(n)
                   if k != i and generators[k]["layer"] >= generators[i]["layer"])
    witnesses = record.get("witnesses")
    witness_row = {}
    if witnesses is not None:
        j = 0
        names = {g["name"]: i for i, g in enumerate(generators)}
        for w in witnesses:
            kind = w["kind"]
            if kind == "free-permanent-generator":
                continue
            if kind == "bosonic-cohomology-order":
                expected = unit(n, names[w["generator"]], w["order"])
            elif kind == "full-power-relation":
                expected = add_scaled(unit(n, names[w["generator"]], w["order"]),
                                      w["reduction"]["coordinates"], -1)
            elif kind == "incoming-gauge-relation":
                expected = w["reduction"]["coordinates"]
            else:
                raise AssertionError("unrecognized witness kind " + kind)
            assert rows[j] == expected
            witness_row[j] = w
            j += 1
        assert j == len(rows)
    input_sign = record.get("inputModel", {}).get("s1")
    if input_sign is None:
        input_sign = case.get("grading_on_generators")
    if input_sign is not None:
        sign_nontrivial = any(input_sign)
        sign_evidence = "explicit input character"
    else:
        assert witnesses is not None
        sign_nontrivial = not any(w.get("gaugeLayer") == 3 for w in witnesses)
        sign_evidence = "complete saved H0(Z_s) gauge-parameter witness list"
    if not sign_nontrivial:
        assert not torsion_pip
        distinguished = len(finite)
        kind = "incoming_integer_generator"
        assert distinguished < len(rows)
        if witnesses is not None:
            w = witness_row[distinguished]
            assert w["kind"] == "incoming-gauge-relation"
            assert w["gaugeLayer"] == 3 and w["gaugeDegree"] == 0 and w["gaugeOrder"] == 0
            assert sum(v.get("gaugeLayer") == 3 for v in witnesses) == 1
        target = list(rows[distinguished])
        # New target = old target - normalization rows; incoming relation has
        # the same sign, while a power relation has the opposite target sign.
        preparation_sign = -1
    elif torsion_pip:
        p = torsion_pip[0]
        distinguished = power_row[p]
        kind = "torsion_pip_square"
        target = add_scaled(unit(n, p, 2), rows[distinguished], -1)
        preparation_sign = 1
    else:
        distinguished = None
        kind = "no_distinguished_target"
        target = [0]*n
        preparation_sign = 0
    assert all(target[i] == 0 for i in pip)
    if witnesses is not None and sign_nontrivial:
        assert not any(w.get("gaugeLayer") == 3 for w in witnesses)
    # Every incoming relation other than the one distinguished integer
    # endpoint has zero Majorana coordinates in the current presentation.
    for j in range(len(finite), len(rows)):
        if j != distinguished:
            assert all(rows[j][i] == 0 for i in majorana)
    original_target = list(target)
    normalizations = []
    prepared = [list(row) for row in rows]
    for i in majorana:
        quotient = target[i] // 2
        if quotient:
            j = power_row[i]
            target = add_scaled(target, rows[j], -quotient)
            prepared[distinguished] = add_scaled(prepared[distinguished], rows[j],
                                                 preparation_sign*quotient)
            normalizations.append({"generator_index_zero_based": i, "row_index_zero_based": j,
                                   "coefficient": quotient})
    assert all(target[i] in (0, 1) for i in majorana)
    pivot = next((i for i in majorana if target[i]), None)
    report = {
        "id": case["id"], "record": case["result"],
        "record_sha256": sha256(path.read_bytes()).hexdigest(),
        "sign_nontrivial": sign_nontrivial, "sign_evidence": sign_evidence,
        "witnesses_replayed": witnesses is not None,
        "generators": [g["name"] for g in generators],
        "kind": kind, "distinguished_row_index_zero_based": distinguished,
        "target_original": original_target, "target_normalized": target,
        "target_normalization_rows": normalizations,
        "requires_majorana_root_choice": pivot is not None,
        "basis_matrix_nonidentity": pivot is not None and target != unit(n, pivot),
        "old_presentation_sha256": digest(rows),
        "free_pip_roots": sum(generators[i]["quotientOrder"] == 0 for i in pip),
    }
    if pivot is None:
        assert all(target[i] == 0 for i in majorana)
        transformed = prepared
        reconstructed = [list(row) for row in prepared]
    else:
        # T has identity rows except row pivot = target. Since target[pivot]=1,
        # det(T)=1 and the following rank-one formula is exactly T^{-1}.
        inverse_row = [-value for value in target]
        inverse_row[pivot] = 1

        def into_new(row):
            return [row[j] if j == pivot else row[j]-row[pivot]*target[j] for j in range(n)]

        def into_old(row):
            return [row[j] if j == pivot else row[j]+row[pivot]*target[j] for j in range(n)]

        for j in range(n):
            assert into_old(into_new(unit(n, j))) == unit(n, j)
            assert into_new(into_old(unit(n, j))) == unit(n, j)
        assert into_new(target) == unit(n, pivot)
        transformed = [into_new(row) for row in prepared]
        expected_distinguished = unit(n, pivot)
        if kind == "torsion_pip_square":
            expected_distinguished = add_scaled(unit(n, torsion_pip[0], 2), unit(n, pivot), -1)
        assert transformed[distinguished] == expected_distinguished
        # Replace the old pivot's square row by the square of the whole new
        # target Y. This is an invertible addition of the other square rows.
        pivot_row = power_row[pivot]
        square_combination = []
        for j in majorana:
            if j != pivot and target[j]:
                transformed[pivot_row] = add_scaled(transformed[pivot_row], transformed[power_row[j]], target[j])
                square_combination.append({"row_index_zero_based": power_row[j], "coefficient": target[j]})
        new_square = transformed[pivot_row]
        assert new_square[pivot] == 2
        assert all(new_square[j] == 0 for j in majorana + pip if j != pivot)
        report.update({
            "pivot_index_zero_based": pivot, "replaced_generator": generators[pivot]["name"],
            "new_generator_is_entire_distinguished_target": True,
            "basis_matrix": {"other_rows": "identity", "replacement_row": target},
            "inverse_basis_matrix": {"other_rows": "identity", "replacement_row": inverse_row},
            "determinant": 1, "transformed_distinguished_relation": transformed[distinguished],
            "new_root_square_relation": new_square,
            "new_root_square_added_rows": square_combination,
        })
        # Reverse every row addition and the basis change, exactly.
        reverse = [list(row) for row in transformed]
        for item in square_combination:
            reverse[pivot_row] = add_scaled(reverse[pivot_row], reverse[item["row_index_zero_based"]], -item["coefficient"])
        reconstructed = [into_old(row) for row in reverse]
        assert reconstructed == prepared
    for item in normalizations:
        reconstructed[distinguished] = add_scaled(reconstructed[distinguished], rows[item["row_index_zero_based"]],
                                                  -preparation_sign*item["coefficient"])
    assert reconstructed == rows
    report.update({"new_presentation_sha256": digest(transformed),
                   "exact_inverse_reconstruction": "PASS", "status": "PASS"})
    return report


index = json.loads(INDEX.read_text())
results, failures = [], []
for case in index["cases"]:
    if case["dimension"] != 3:
        continue
    try:
        results.append(replay(case))
    except Exception as error:
        failures.append({"id": case["id"], "error": repr(error)})
counts = Counter(result["kind"] for result in results)
summary = {
    "status": "PASS" if not failures else "FAIL",
    "scope": "Exact integer basis/row replay of saved presentations; no new cochain or group computation; no SNF recomputation.",
    "cases_attempted": len(results)+len(failures), "cases_passed": len(results),
    "nonzero_majorana_targets": sum(r["requires_majorana_root_choice"] for r in results),
    "nonzero_majorana_targets_by_kind": dict(Counter(r["kind"] for r in results if r["requires_majorana_root_choice"])),
    "nonidentity_integer_basis_changes": sum(r["basis_matrix_nonidentity"] for r in results),
    "nonidentity_integer_basis_changes_by_kind": dict(Counter(r["kind"] for r in results if r["basis_matrix_nonidentity"])),
    "case_kinds": dict(counts), "with_full_witness_replay": sum(r["witnesses_replayed"] for r in results),
    "summary_records_using_declared_production_row_order": sum(not r["witnesses_replayed"] for r in results),
    "cases_with_free_pip_roots": sum(r["free_pip_roots"] > 0 for r in results),
    "target_normalizations_needed": sum(bool(r["target_normalization_rows"]) for r in results),
    "failures": failures, "cases": results,
}
(OUT / "ADAPTIVE_THREE_DIMENSIONAL_REPLAY.json").write_text(json.dumps(summary, indent=2)+"\n")
print(json.dumps({k: v for k, v in summary.items() if k != "cases"}, indent=2))
if failures:
    raise SystemExit(1)
