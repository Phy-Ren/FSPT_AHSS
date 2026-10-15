"""Universal congruence certificate for sheet shifts by 16.

Read-only on the immutable parity reference. Each DAG node carries a lower
bound for v2(value) and for v2(shifted_value-value). No sampling is used.
Exact-division instructions are interpreted on their prescribed domain.
"""
from pathlib import Path
import argparse
import hashlib
import json

INF = 10**9


def valuation(x):
    return INF if x == 0 else (abs(x) & -abs(x)).bit_length() - 1


def capped_add(a, b):
    return min(INF, a + b)


def audit(path, shifted_fields=("n", "m")):
    data = json.loads(path.read_text())
    values = []
    exact_divisions = 0
    for index, node in enumerate(data["program"]):
        op = node[0]
        if op == "const":
            out = (valuation(node[1]), INF, node[1])
        elif op == "field":
            out = (0, 4 if node[1] in shifted_fields else INF, None)
        else:
            va, da, ca = values[node[1]]
            if op in ("add", "mul"):
                vb, db, cb = values[node[2]]
                constant = None if ca is None or cb is None else (
                    ca + cb if op == "add" else ca * cb)
                if constant is not None:
                    out = (valuation(constant), INF, constant)
                elif op == "add":
                    out = (min(va, vb), min(da, db), None)
                elif ca == 0 or cb == 0:
                    out = (INF, INF, 0)
                else:
                    # (a+da)(b+db)-ab = a*db+b*da+da*db.
                    out = (capped_add(va, vb), min(capped_add(va, db),
                           capped_add(vb, da), capped_add(da, db)), None)
            else:
                k = node[2]
                if op == "div":
                    exact_divisions += 1
                if ca is not None:
                    if op == "mod":
                        c = ca % k
                    elif op in ("div", "floor"):
                        if op == "div":
                            assert ca % k == 0, (path.name, index, node, ca)
                        c = ca // k
                    elif op == "bit":
                        c = (ca >> k) & 1
                    else:
                        raise ValueError(node)
                    out = (valuation(c), INF, c)
                elif op == "mod":
                    assert k > 0
                    vk = valuation(k)
                    if k & (k - 1) == 0 and da >= vk:
                        difference = INF
                    else:
                        difference = min(da, vk)
                    if k & (k - 1) == 0 and va >= vk:
                        out = (INF, INF, 0)
                    else:
                        out = (min(va, vk), difference, None)
                elif op == "bit":
                    if va > k:
                        out = (INF, INF, 0) if da > k else (INF, 0, None)
                    else:
                        out = (0, INF if da > k else 0, None)
                elif op in ("div", "floor"):
                    assert k > 0 and k & (k - 1) == 0, node
                    vk = valuation(k)
                    out = (max(0, va - vk),
                           INF if da == INF else max(0, da - vk), None)
                else:
                    raise ValueError(node)
        values.append(out)
    def readable(v):
        return "infinity" if v == INF else v
    return {
        "name": path.stem,
        "nodes": len(values),
        "output_difference_v2_lower_bounds": [readable(values[i][1]) for i in data["outputs"]],
        "exact_division_instructions": exact_divisions,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-reference", type=Path,
                        default=Path("/home/xingyu/FSPT_AHSS_public"))
    args = parser.parse_args()
    root = args.public_reference / "fspt/data/full_formula"
    names = ("source_4_majorana", "source_4_fermion", "product_4_majorana",
             "product_4_fermion", "y6", "h6", "high6", "rho4", "tensor4", "nonbinary4")
    programs = [audit(root / (name + ".json")) for name in names]
    for row in programs:
        bounds = row["output_difference_v2_lower_bounds"]
        if row["name"] == "high6":
            assert bounds[0] == "infinity" and bounds[1] >= 4, row
        elif row["name"] == "nonbinary4":
            assert bounds[0] >= 4, row
        else:
            assert all(v == "infinity" for v in bounds), row
    result = {
        "status": "PASS",
        "method": "Conservative relational 2-adic abstract interpretation, not sampling",
        "substitution": "Each n,m face changes by an independent multiple of16; all other integer input faces unchanged",
        "domain": "Both evaluations must lie in every exact-division instruction's prescribed domain",
        "interpretation": "All dyadic/lower packets are unchanged. The cubic and nonbinary numerator may retain an odd-primary change; divisibility16 is not divisibility48.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "programs": programs,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    for row in programs:
        vals = row["output_difference_v2_lower_bounds"]
        print(row["name"], sorted(set(map(str, vals))), len(vals))


if __name__ == "__main__":
    main()
