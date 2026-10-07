"""Read saved 4D presentations; replay exact algebra without cochain jobs."""
from collections import Counter
from hashlib import sha256
import json
from math import gcd, prod
from pathlib import Path

PUBLIC = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
INDEX = PUBLIC / "results/computed_examples/index.json"


def hash_json(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def two_valuation(value):
    assert value > 0
    return (value & -value).bit_length()-1


def odd_part(value):
    return value >> two_valuation(value)


def unit(n, i, coefficient=1):
    row = [0]*n
    row[i] = coefficient
    return row


def target(rows, row_index, generator_index, order):
    return [order*int(j == generator_index)-v for j, v in enumerate(rows[row_index])]


def prepare(record):
    gs = record["generators"]
    rows = [list(row) for row in record["presentation"]]
    finite = [i for i, g in enumerate(gs) if g["quotientOrder"]]
    pr = dict(zip(finite, range(len(finite))))
    assert all(len(row) == len(gs) for row in rows)
    for i in finite:
        assert rows[pr[i]][i] == gs[i]["quotientOrder"]
        assert all(rows[pr[i]][j] == 0 for j in range(len(gs))
                   if j != i and gs[j]["layer"] >= gs[i]["layer"])
    sign = any(record["inputModel"]["s1"])
    incoming = len(finite) if sign else None
    if incoming is not None:
        assert incoming < len(rows)
    if "witnesses" in record:
        witness_index = 0
        for w in record["witnesses"]:
            if w["kind"] == "free-permanent-generator":
                continue
            if w["kind"] == "incoming-gauge-relation" and w["gaugeLayer"] == 3:
                assert sign and witness_index == incoming
                assert w["gaugeOrder"] == 2 and w["gaugeDegree"] == 1
            witness_index += 1
        assert witness_index == len(rows)
    return gs, rows, pr, incoming


def replay_two_primary(record):
    gs, rows, pr, incoming = prepare(record)
    original = [list(row) for row in rows]
    n = len(gs)
    majorana = [i for i, g in enumerate(gs) if g["layer"] == 2]
    pip = [i for i, g in enumerate(gs) if g["layer"] == 3]
    assert all(gs[i]["quotientOrder"] > 0 and not gs[i]["quotientOrder"] & (gs[i]["quotientOrder"]-1) for i in pip)
    assert all(gs[i]["quotientOrder"] == 2 for i in majorana)
    operations = []

    def row_add(destination, source, coefficient):
        assert destination != source
        rows[destination] = [x+coefficient*y for x, y in zip(rows[destination], rows[source])]
        operations.append(["row_add", destination, source, coefficient])

    def column_add(destination, source, coefficient):
        assert destination != source
        for row in rows:
            row[destination] += coefficient*row[source]
        operations.append(["column_add", destination, source, coefficient])

    def change_basis(pivot, replacement):
        assert replacement[pivot] == 1
        for row in rows:
            coefficient = row[pivot]
            for j in range(n):
                if j != pivot:
                    row[j] -= coefficient*replacement[j]
        operations.append(["basis_row", pivot, list(replacement)])

    def normalize_power(i):
        q = gs[i]["quotientOrder"]
        y = target(rows, pr[i], i, q)
        for j in majorana:
            coefficient = y[j]//2
            if coefficient:
                row_add(pr[i], pr[j], coefficient)
                y = target(rows, pr[i], i, q)
        return y

    if incoming is not None:
        for j in majorana:
            coefficient = rows[incoming][j]//2
            if coefficient:
                row_add(incoming, pr[j], -coefficient)
        incoming_target = list(rows[incoming])
    else:
        incoming_target = [0]*n
    incoming_pivot = next((j for j in majorana if incoming_target[j]), None)
    assert all(incoming_target[j] in (0, 1) for j in majorana)
    for ri in range(len(pr), len(rows)):
        if ri != incoming:
            assert all(rows[ri][j] == 0 for j in majorana)

    def image(i):
        y = target(rows, pr[i], i, gs[i]["quotientOrder"])
        value = [y[j] % 2 for j in majorana]
        if incoming_pivot is not None:
            c = y[incoming_pivot] % 2
            value = [a ^ (c*incoming_target[j]) for a, j in zip(value, majorana)]
        return value

    initial_images = {i: image(i) for i in pip}
    pivot_roots = []
    eliminations = []
    for i in sorted(pip, key=lambda j: (-gs[j]["quotientOrder"], j)):
        for j, vector, pivot in pivot_roots:
            value = image(i)
            if value[pivot]:
                qi, qj = gs[i]["quotientOrder"], gs[j]["quotientOrder"]
                assert qj % qi == 0
                # New x_i=x_i+(qj/qi)x_j; its power row adds the entire
                # already transformed power row of x_j, including lower carries.
                column_add(j, i, -(qj//qi))
                row_add(pr[i], pr[j], 1)
                assert image(i) == [a ^ b for a, b in zip(value, vector)]
                eliminations.append({"root": i, "higher_exponent_root": j,
                                     "integer_coefficient": qj//qi})
        value = image(i)
        if any(value):
            pivot_roots.append((i, value, value.index(1)))
    final_images = {i: image(i) for i in pip}
    for i in pip:
        y = target(rows, pr[i], i, gs[i]["quotientOrder"])
        if incoming_pivot is not None and y[incoming_pivot] % 2:
            row_add(pr[i], incoming, 1)
        y = normalize_power(i)
        assert [y[j] for j in majorana] == final_images[i]

    chosen = []

    def choose_majorana_root(row_index, y, pivot, pip_index=None):
        change_basis(pivot, y)
        for j in majorana:
            if j != pivot and y[j]:
                row_add(pr[pivot], pr[j], y[j])
        assert rows[pr[pivot]][pivot] == 2
        assert all(rows[pr[pivot]][j] == 0 for j in majorana+pip if j != pivot)
        expected = unit(n, pivot)
        if pip_index is not None:
            expected = [gs[pip_index]["quotientOrder"]*int(j == pip_index)-int(j == pivot) for j in range(n)]
        assert rows[row_index] == expected
        chosen.append({"pivot": pivot, "full_target": y, "source_pip_root": pip_index,
                       "square_relation": list(rows[pr[pivot]])})

    if incoming_pivot is not None:
        choose_majorana_root(incoming, list(rows[incoming]), incoming_pivot)
    for i, vector, pivot in pivot_roots:
        y = target(rows, pr[i], i, gs[i]["quotientOrder"])
        choose_majorana_root(pr[i], y, majorana[pivot], i)
    kernel_targets = []
    for i in pip:
        if not any(final_images[i]):
            y = target(rows, pr[i], i, gs[i]["quotientOrder"])
            assert all(y[j] == 0 for j in majorana+pip)
            kernel_targets.append({"root": i, "had_nonzero_initial_image": any(initial_images[i]),
                                   "full_cf_bosonic_offset": y, "offset_vector_nonzero": any(y)})
    reverse = [list(row) for row in rows]
    for operation in reversed(operations):
        if operation[0] == "row_add":
            _, d, s, c = operation
            reverse[d] = [x-c*y for x, y in zip(reverse[d], reverse[s])]
        elif operation[0] == "column_add":
            _, d, s, c = operation
            for row in reverse:
                row[d] -= c*row[s]
        else:
            _, pivot, y = operation
            for row in reverse:
                coefficient = row[pivot]
                for j in range(n):
                    if j != pivot:
                        row[j] += coefficient*y[j]
    assert reverse == original
    return {"status": "PASS", "orders": [gs[i]["quotientOrder"] for i in pip],
            "incoming_majorana_image_nonzero": incoming_pivot is not None,
            "initial_power_images": initial_images, "independent_final_power_images": final_images,
            "socle_eliminations": eliminations, "chosen_majorana_roots": chosen,
            "kernel_power_targets": kernel_targets, "operations": operations,
            "old_presentation_sha256": hash_json(original), "new_presentation_sha256": hash_json(rows),
            "exact_inverse_reconstruction": "PASS"}


def audit_odd(record):
    gs, rows, pr, incoming = prepare(record)
    bosons = [i for i, g in enumerate(gs) if g["layer"] == 0]
    moduli = [odd_part(gs[i]["quotientOrder"]) for i in bosons]
    projections = {}
    for j, i in enumerate(bosons):
        projections[i] = [int(j == k) % modulus for k, modulus in enumerate(moduli)]

    def project(vector):
        assert all(not value or j in projections for j, value in enumerate(vector))
        return [sum(value*projections[j][k] for j, value in enumerate(vector) if value) % modulus
                for k, modulus in enumerate(moduli)]

    for i, g in enumerate(gs):
        if g["layer"] in (1, 2):
            lower = target(rows, pr[i], i, 2)
            projections[i] = [value*pow(2, -1, modulus) % modulus if modulus > 1 else 0
                              for value, modulus in zip(project(lower), moduli)]
    incoming_odd = [project(row) for row in rows[len(pr):]]
    assert all(not any(row) for row in incoming_odd)
    result = []
    for i, g in enumerate(gs):
        q = g["quotientOrder"]
        if g["layer"] != 3 or odd_part(q) == 1:
            continue
        r = odd_part(q)
        k = next(k for k in range(1, 1000) if (2**k-1) % r == 0 and gcd((2**k-1)//r, r) == 1)
        t = (2**k-1)//r
        a = project(target(rows, pr[i], i, q))
        b = [(4*t*value) % modulus for value, modulus in zip(a, moduli)]
        quotient_moduli = [gcd(r, modulus) for modulus in moduli]
        recovered = [value*pow(4*t, -1, modulus) % modulus if modulus > 1 else 0
                     for value, modulus in zip(b, quotient_moduli)]
        expected = [value % modulus for value, modulus in zip(a, quotient_moduli)]
        assert recovered == expected
        result.append({"root": g["name"], "quotient_order": q, "two_adic_exponent": two_valuation(q),
                       "odd_quotient_order": r, "doubling_cycle_length": k, "cycle_multiplier": t,
                       "binary_layer_erasure_multiplier": 4, "bosonic_odd_moduli": moduli,
                       "old_odd_power_image": a, "phase_difference_image": b,
                       "extension_quotient_moduli": quotient_moduli,
                       "recovered_extension_class": recovered, "status": "PASS"})
    return {"incoming_odd_images_vanish": True, "roots": result}


def main(public=PUBLIC, output=OUT):
    global PUBLIC, INDEX, OUT
    PUBLIC, OUT = Path(public), Path(output)
    INDEX = PUBLIC / "results/computed_examples/index.json"
    index = json.loads(INDEX.read_text())
    cases = [c for c in index["cases"] if c["dimension"] == 4]
    orders = []
    rows_two, rows_odd, missing, failures = [], [], [], []
    final_pip_hist = Counter()
    for case in cases:
        assert case["symmetry_kind"] == "finite_internal"
        orders.append((case["id"], prod(case["invariant_factors"])))
        for layer in case["final_filtration"]:
            if layer["layer"] == "pip":
                final_pip_hist.update(layer["quotient_invariants"])
        path = PUBLIC / case["result"]
        record = json.loads(path.read_text())
        if "generators" not in record or "presentation" not in record:
            missing.append(case["id"])
            continue
        try:
            common = {"id": case["id"], "record": case["result"],
                      "record_sha256": sha256(path.read_bytes()).hexdigest(),
                      "with_detailed_witnesses": "witnesses" in record}
            qs = [g["quotientOrder"] for g in record["generators"] if g["layer"] == 3]
            if all(not q & (q-1) for q in qs):
                rows_two.append(dict(common, **replay_two_primary(record)))
            if any(q & (q-1) for q in qs):
                rows_odd.append(dict(common, **audit_odd(record)))
        except Exception as error:
            failures.append({"id": case["id"], "error": repr(error)})
    report = {
        "status": "PASS" if not failures else "FAIL",
        "scope": "Saved 4D integer presentations only; no new cochain calculation or Smith normal form.",
        "catalogue_cases": len(cases), "all_groups_finite_internal": True,
        "marked_presentations_available": len(cases)-len(missing), "summary_only_cases": len(missing),
        "two_primary_pip_presentation_replays": len(rows_two), "odd_pip_presentation_checks": len(rows_odd),
        "final_pip_order_histogram": dict(sorted(final_pip_hist.items())),
        "group_order_threshold_counts": {str(bound): sum(order <= bound for _, order in orders)
                                         for bound in [1, 16, 256, 4096, 65536, 1048576, 16777216]},
        "maximum_group_order": max(order for _, order in orders),
        "largest_groups": sorted(orders, key=lambda entry: (-entry[1], entry[0]))[:10],
        "cases_with_socle_elimination": sum(bool(row["socle_eliminations"]) for row in rows_two),
        "socle_elimination_count": sum(len(row["socle_eliminations"]) for row in rows_two),
        "cases_with_dependent_power_image_removed": sum(any(t["had_nonzero_initial_image"] for t in row["kernel_power_targets"]) for row in rows_two),
        "kernel_targets_with_retained_nonzero_lower_offsets": sum(t["offset_vector_nonzero"] for row in rows_two for t in row["kernel_power_targets"]),
        "two_primary_cases": rows_two, "odd_cases": rows_odd, "summary_only_ids": missing, "failures": failures,
    }
    (OUT / "FOUR_DIMENSIONAL_PRESENTATION_AUDIT.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ["two_primary_cases", "odd_cases", "summary_only_ids"]}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=PUBLIC,
                        help="Published repository containing results/computed_examples/index.json")
    parser.add_argument("--output-directory", type=Path, default=OUT)
    args = parser.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    main(args.repository_root, args.output_directory)
