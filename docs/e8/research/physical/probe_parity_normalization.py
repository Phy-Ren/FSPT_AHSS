"""Symbolically substitute simplicial degeneracies into immutable DAGs.

Conservative exact integer polynomial rewriting. Unresolved div/floor/mod/bit
operations become formal atoms; a zero certificate does not assume anything
about their values. No finite-value sampling is performed.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json


class Symbolic:
    def __init__(self):
        self.atoms = {}
        self.boolean_atoms = set()
        self.peak_terms = 0

    def atom(self, key, boolean=False):
        if key not in self.atoms:
            self.atoms[key] = len(self.atoms)
        a = self.atoms[key]
        if boolean:
            self.boolean_atoms.add(a)
        return { (a,): 1 }

    def clean(self, p):
        p = {m: c for m, c in p.items() if c}
        self.peak_terms = max(self.peak_terms, len(p))
        if len(p) > 100000:
            raise RuntimeError("Conservative symbolic expansion limit")
        return p

    def add(self, p, q):
        out = Counter(p)
        for m, c in q.items():
            out[m] += c
        return self.clean(out)

    def mul(self, p, q):
        out = Counter()
        for m, c in p.items():
            for n, d in q.items():
                # Boolean atoms satisfy x*x=x over the integers as well.
                powers = Counter(m + n)
                monomial = tuple(sorted(a for a, power in powers.items()
                                        for _ in range(1 if a in self.boolean_atoms else power)))
                out[monomial] += c * d
        return self.clean(out)

    def unary(self, op, p, k):
        if not p:
            return {}
        if set(p) <= {()}:
            c = p.get((), 0)
            if op == "mod":
                c %= k
            elif op == "bit":
                c = (c >> k) & 1
            else:
                if op == "div":
                    assert c % k == 0
                c //= k
            return {(): c} if c else {}
        if op == "mod":
            p = self.clean({m: c % k for m, c in p.items()})
            if not p:
                return {}
            if len(p) == 1 and next(iter(p.values())) == 1:
                m = next(iter(p))
                if all(a in self.boolean_atoms for a in m):
                    return p
        if op in ("floor", "div") and all(c % k == 0 for c in p.values()):
            return self.clean({m: c // k for m, c in p.items()})
        return self.atom((op, k, tuple(sorted(p.items()))), op == "bit" or op == "mod" and k == 2)


def audit(data, collapsed_vertex=None, zero_fields=()):
    symbolic = Symbolic()
    values = []
    for node in data["program"]:
        op = node[0]
        if op not in {"const", "field", "add", "mul", "mod", "bit", "floor", "div"}:
            raise ValueError(f"Unsupported opcode: {op}")
        if op == "const":
            value = {(): node[1]} if node[1] else {}
        elif op == "field":
            name, face = node[1:]
            projected = (tuple(face) if collapsed_vertex is None else
                         tuple(v if v <= collapsed_vertex else v - 1 for v in face))
            value = ({} if name in zero_fields or len(set(projected)) != len(projected)
                     else symbolic.atom((name, projected)))
        elif op == "add":
            value = symbolic.add(values[node[1]], values[node[2]])
        elif op == "mul":
            value = symbolic.mul(values[node[1]], values[node[2]])
        else:
            value = symbolic.unary(op, values[node[1]], node[2])
        values.append(value)
    out = {"collapsed_vertex": collapsed_vertex,
            "zero_fields": list(zero_fields),
            "outputs_zero": [not values[i] for i in data["outputs"]],
            "remaining_output_terms": [len(values[i]) for i in data["outputs"]],
            "peak_polynomial_terms": symbolic.peak_terms}
    if data["name"] == "rho4" and collapsed_vertex is not None:
        from itertools import combinations
        seen = {}
        natural = True
        for face, index in zip(combinations(range(7), 4), data["outputs"][1:]):
            projected = tuple(v if v <= collapsed_vertex else v - 1 for v in face)
            if len(set(projected)) != 4:
                natural = natural and not values[index]
            elif projected in seen:
                natural = natural and values[index] == seen[projected]
            else:
                seen[projected] = values[index]
        out["U_is_degenerate_pullback"] = bool(natural)
    if data["name"] == "rho4" and zero_fields:
        from itertools import combinations
        remaining = "b" if "n" in zero_fields else "a"
        expected = [symbolic.unary("mod", symbolic.atom((remaining, face)), 2)
                    for face in combinations(range(7), 4)]
        out["U_equals_other_factor"] = all(values[index] == want for index, want
                                          in zip(data["outputs"][1:], expected))
    return out


def transfer_degeneracies(reference):
    import sys
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(reference))
    from fspt.full_formula.runtime import transfer_cuts
    rows = []
    for i in range(5):
        chain = set()
        for projections in transfer_cuts(5):
            pulled = tuple(tuple(v if v <= i else v - 1 for v in p) for p in projections)
            # Degree-two factor data vanish if its map has fewer than3 vertices.
            if min(len(set(pulled[j])) for j in (1, 2)) < 3:
                continue
            # A simultaneous repeated adjacent vertex is a simplicial degeneracy.
            if any(all(p[j] == p[j + 1] for p in pulled) for j in range(6)):
                continue
            if pulled in chain:
                chain.remove(pulled)
            else:
                chain.add(pulled)
        rows.append({"collapsed_vertex": i, "remaining_projection_chains": len(chain)})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--names", nargs="+", default=["y6", "h6", "high6", "rho4", "tensor4"])
    parser.add_argument("--public-reference", type=Path, default=Path("/home/xingyu/FSPT_AHSS_public"))
    args = parser.parse_args()
    root = args.public_reference / "fspt/data/full_formula"
    result = []
    for name in args.names:
        path = root / (name + ".json")
        data = json.loads(path.read_text())
        rows = []
        for i in range(data["top_degree"]):
            row = audit(data, i)
            assert row["outputs_zero"][0], (name, row)
            if name == "high6":
                assert all(row["outputs_zero"]), row
            if name == "rho4":
                assert row["U_is_degenerate_pullback"], row
            rows.append(row)
            print(name, i, row["remaining_output_terms"][0], flush=True)
        zero_inputs = ({"y6": [("n",)], "h6": [("n", "a", "y")],
                        "rho4": [("n", "a"), ("m", "b")],
                        "tensor4": [("n", "a"), ("m", "b")]}).get(name, [])
        reductions = [audit(data, zero_fields=fields) for fields in zero_inputs]
        for row in reductions:
            assert row["outputs_zero"][0], (name, row)
            if name == "rho4":
                assert row["U_equals_other_factor"], row
            print(name, "zero", row["zero_fields"], row["remaining_output_terms"][0],
                  row.get("U_equals_other_factor"), flush=True)
        result.append({"name": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                       "degeneracies": rows, "zero_factor_reductions": reductions})
    transfer = transfer_degeneracies(args.public_reference)
    assert all(row["remaining_projection_chains"] == 0 for row in transfer)
    print("transfer", transfer)
    files = ["fspt/full_formula/runtime.py", "fspt/full_formula/compiler.py",
             "formulas/publication_source/full4/graded_full.py",
             "formulas/publication_source/full4/product_full.py"]
    Path(__file__).with_suffix(".json").write_text(json.dumps({"status": "PASS",
            "method": "Conservative exact symbolic rewriting and finite projection-chain identities; no sampled field values",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "programs": result, "transfer_degeneracies": transfer,
            "reference_source_sha256": {f: hashlib.sha256((args.public_reference/f).read_bytes()).hexdigest() for f in files}}, indent=2) + "\n")


if __name__ == "__main__":
    main()
