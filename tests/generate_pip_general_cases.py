"""Existing twelve legal O5 fixtures plus negative signed-integer towers."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas_export import gap_literal
sys.path.insert(0, str(ROOT / 'vendor/p_ip_d4_normalized_package/code'))
import cochains as ref
from pip_d4 import evaluate_simplex

program = json.loads((ROOT / 'gap/pip_o5_program.json').read_text())
fixtures = []
negative_values = 0
mismatches = []
for case in range(84):
    random.seed(7513 + case if case < 12 else 839210 + case)
    N = 5
    s = ref.random_cochain(0, N).d()
    w = ref.C(2)
    if case < 12:
        n = s.lift() if case % 2 else ref.ds(ref.random_cochain(0, N, 16).lift(), s)
    else:
        bound = 64 if case < 76 else 2**45
        z = ref.C(0, values={(i,): random.randrange(-bound, bound + 1) for i in range(N + 1)}, mod=None)
        n = ref.ds(z, s)
    P = ref.sq(n.reduce(2), 2) + ref.cup(w, n.reduce(2)) + ref.cup(s, ref.sq(n.reduce(2), 1))
    b = ref.primitive(P) + ref.random_cochain(1, N).d()
    Q = ref.parity(n, b, w, s)
    c = ref.primitive(Q) + ref.random_cochain(2, N).d()
    fields = {'n': n, 'b': b, 'c': c, 's': s, 'w': w}
    expected = evaluate_simplex(1, n_integer=n, n_majorana=b, n_fermion=c, omega2=w, s1=s)['numerator_mod16']
    graph_value = evaluate_program(program, fields)
    if graph_value != expected:
        mismatches.append(dict(case=case, seed=7513+case if case<12 else 839210+case,
            graph=graph_value, oracle=expected,
            fields={name: [[list(face), fields[name](face)] for face in combinations(range(6), fields[name].deg+1)] for name in fields},
            dsn=[ref.ds(n,s)(face) for face in combinations(range(6),3)],
            db_minus_P=[(b.d()(face)-P(face))%2 for face in combinations(range(6),4)],
            dc_minus_Q=[(c.d()(face)-Q(face))%2 for face in combinations(range(6),5)]))
        print('EXISTING_GRAPH_ORACLE_MISMATCH',case,graph_value,expected,flush=True)
    encoded = []
    for name in ['n', 'b', 'c', 's']:
        field = fields[name]
        rows = []
        for face in combinations(range(6), field.deg + 1):
            value = field(face)
            if name == 'n' and value < 0:
                negative_values += 1
            rows.append([[sum(2**i for i in range(a, z)) for a, z in zip(face, face[1:])], value])
        encoded.append([name, rows])
    fixtures.append([graph_value, encoded])
assert negative_values > 0
digest = hashlib.sha256((ROOT / 'gap/pip_o5_program.json').read_bytes()).hexdigest()
(ROOT / 'tests/pip_general_cases.g').write_text('AFSPipGeneralCasesSourceSha256 := '+gap_literal(digest)+';;\nAFSPipGeneralCases := ' + gap_literal(fixtures) + ';;\n')
audit = ROOT / 'runs/formula_audit'
audit.mkdir(parents=True, exist_ok=True)
(audit / 'generic_oracle_discrepancies.json').write_text(json.dumps(mismatches,indent=2)+'\n')
print('GENERATED {} graph fixtures; {} negative integer edge values; {} graph/oracle discrepancies'.format(len(fixtures),negative_values,len(mismatches)))

if mismatches and '--allow-oracle-mismatch' not in sys.argv:
    raise AssertionError('Existing scalar graph disagrees with original oracle; see runs/formula_audit/generic_oracle_discrepancies.json')
