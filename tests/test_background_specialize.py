"""Exact legal-tower controls for optional full-background scalar specialization."""
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas_background_specialize import KnownIntegerBuilder, specialize
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas_export import gap_literal

spec = importlib.util.spec_from_file_location("background_fixtures", ROOT/"tests/test_background_formulas.py")
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)


def sign_tower(q, seed, mask):
    rng = random.Random(seed)
    vertices = [0]+[(mask >> i) & 1 for i in range(5)]
    s = q.C(1, {f: vertices[f[0]] ^ vertices[f[1]] for f in fixtures.faces(1, 5)})
    w = q.C(2, fixtures.differential(fixtures.random_binary(rng, 1, 5), 1, 5))
    n = s.lift()
    a = n.reduce(2)
    primary = q.sq(a, 2)+q.cup(w, a)+q.cup(s, q.sq(a, 1))
    b = q.primitive(primary)+q.C(2, fixtures.differential(fixtures.random_binary(rng, 1, 5), 1, 5))
    parity = q.parity(n, b, w, s)
    c = q.primitive(parity)+q.C(3, fixtures.differential(fixtures.random_binary(rng, 2, 5), 2, 5))
    return dict(n=n, s=s, w=w, b=b, c=c)


def validation(fixture_path=None):
    raw = (ROOT/"gap/pip_o5_background.json").read_bytes()
    full = json.loads(raw)
    programs = {mode: specialize(full, mode) for mode in ("even", "sign")}
    q, oracle = fixtures.import_oracle()
    data, results, gap_cases = {}, {}, []
    for mode in programs:
        data[mode] = []
        for seed in range(64):
            fields = (fixtures.legal_pip(q, 721303+seed, seed % 32, multiple=2*(1+seed % 4))
                      if mode == "even" else sign_tower(q, 512007+seed, seed % 32))
            expected = oracle(1, n_integer=fields["n"], n_majorana=fields["b"],
                              n_fermion=fields["c"], omega2=fields["w"], s1=fields["s"])["numerator_mod16"]
            baseline = evaluate_program(full, fields)
            actual = evaluate_program(programs[mode], fields)
            if not actual == expected == baseline:
                raise AssertionError((mode, seed, expected, baseline, actual))
            data[mode].append(fields)
            if fixture_path:
                gap_cases.append([mode, expected, fixtures.encode(fields,
                    dict(n=1, s=1, w=2, b=2, c=3), 5)])
        # Warm both implementations, then alternate order over identical fields.
        timings = {"full": 0.0, "specialized": 0.0}
        for iteration in range(3):
            choices = [("full", full), ("specialized", programs[mode])]
            if iteration % 2:
                choices.reverse()
            for name, program in choices:
                start = time.process_time()
                for fields in data[mode]:
                    evaluate_program(program, fields)
                timings[name] += time.process_time()-start
        ints = [fields["n"](f) for fields in data[mode] for f in fixtures.faces(1, 5)]
        results[mode] = dict(cases=len(data[mode]), exact_three_way_matches=True,
            nodes=len(programs[mode]["program"]), original_nodes=len(full["program"]),
            operation_counts=dict(Counter(node[0] for node in programs[mode]["program"])),
            n_negative_count=sum(x < 0 for x in ints), n_largest_bits=max(abs(x).bit_length() for x in ints),
            interpreter_cpu_seconds=timings, interpreter_speedup=timings["full"]/timings["specialized"])
    fixture_sha = None
    if fixture_path:
        content = "AFSBackgroundSpecializationCases := "+gap_literal(gap_cases)+";;\n"
        fixture_path.write_text(content)
        fixture_sha = hashlib.sha256(content.encode()).hexdigest()
    return dict(schema=1, source_program_sha256=hashlib.sha256(raw).hexdigest(),
        gap_fixture_sha256=fixture_sha,
        optional_only=True, production_runtime_changed=False, results=results,
        source_sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in (
            "fspt/formulas_background_specialize.py", "tests/test_background_specialize.py",
            "fspt/formulas_pip_compile.py", "vendor/p_ip_d4_normalized_package/code/pip_d4.py",
            "vendor/p_ip_d4_normalized_package/code/explicit_pip.py",
            "vendor/p_ip_d4_normalized_package/code/polynomial_tables.py")})


class SpecializationTests(unittest.TestCase):
    def test_low_bits_preserve_full_original_even_integer(self):
        b = KnownIntegerBuilder("even")
        n = b.field("n", (0, 1))
        self.assertEqual(b.nodes[n.index][1], "n")
        self.assertEqual(b.constant(b.bit(n, 0)), 0)
        product = n*(1-2*b.field("s", (0, 1)))
        self.assertEqual(b.constant(product % 2), 0)
        self.assertIsNone(b.constant(b.floor(n, 2)))

    def test_signed_bit_semantics_are_floor_not_truncation(self):
        b = KnownIntegerBuilder("sign")
        s = b.field("s", (0, 1))
        for k in (1, 2, 3, 8):
            output = b.bit(-s, k)
            program = dict(program=b.nodes, output=output.index)
            for value in (0, 1):
                self.assertEqual(evaluate_program(program, dict(s=lambda f: value)), value)
        self.assertEqual(b.field("n", (0, 1)).index, s.index)
        self.assertEqual(b.constant(s-s), 0)

    def test_exact_oracle_and_full_graph_controls(self):
        result = validation()
        self.assertEqual([r["cases"] for r in result["results"].values()], [64, 64])


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--evidence":
        out = Path(sys.argv[2])
        if out.exists():
            raise ValueError("preserve previous evidence")
        out.parent.mkdir(parents=True, exist_ok=True)
        result = validation(out.with_name("cases.g"))
        out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        print(json.dumps(result["results"], indent=2))
    else:
        unittest.main()
