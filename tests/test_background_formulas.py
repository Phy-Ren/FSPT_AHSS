"""Independent, exact local controls for arbitrary closed omega/sign backgrounds.

The supplied p+ip evaluator is imported without modification. This is a finite
local cochain audit, not a classification result or proof of all group identities.
Run directly to save evidence and a separate compute-node GAP fixture driver.
"""
import argparse
import hashlib
import importlib
from itertools import combinations
from fractions import Fraction
import json
from pathlib import Path
import random
import re
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas import evaluate, formula
from fspt.formulas_fast_compile import compile_expression
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas_export import gap_literal

VENDOR = ROOT/'vendor/p_ip_d4_normalized_package/code'
SOURCE_FILES = [
    'fspt/formulas.py', 'fspt/formulas_fast_compile.py', 'fspt/formulas_pip_compile.py',
    'gap/formula_data.g', 'gap/formula_fast.g', 'gap/formulas.g',
    'gap/stacking.g', 'gap/stacking_closed_cf.g', 'gap/backend.g',
    'gap/pip_o5_background.json', 'gap/pip_o5_background.g',
    'gap/pip_o5_program.json', 'gap/pip_o5_program.g',
    'results/space_groups/source/gap/pip_o5_program.g',
    'gap/pip_o5_general.g', 'gap/pip_o5_sign.g',
    'vendor/p_ip_d4_normalized_package/code/pip_d4.py',
    'vendor/p_ip_d4_normalized_package/code/cochains.py',
    'vendor/p_ip_d4_normalized_package/code/explicit_pip.py',
    'vendor/p_ip_d4_normalized_package/code/polynomial_tables.py',
    'vendor/p_ip_d4_normalized_package/code/Y5_word_total.json',
]


def hashes():
    return {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_FILES}


def faces(degree, dimension):
    return combinations(range(dimension+1), degree+1)


def differential(values, degree, dimension):
    return {f: sum((-1)**i*values[f[:i]+f[i+1:]] for i in range(len(f))) % 2
            for f in faces(degree+1, dimension)}


def random_binary(rng, degree, dimension):
    return {f: rng.randrange(2) for f in faces(degree, dimension)}


def import_oracle():
    # The other supplied bundle also calls its module cochains. Verify its origin
    # rather than silently accepting whichever test imported that name first.
    current = sys.modules.get('cochains')
    if current is not None and Path(current.__file__).resolve() != (VENDOR/'cochains.py').resolve():
        raise RuntimeError('Run this audit in its own Python process: incompatible oracle cochains module')
    sys.path.insert(0, str(VENDOR))
    q = importlib.import_module('cochains')
    evaluator = importlib.import_module('pip_d4').evaluate_simplex
    return q, evaluator


def legal_pip(q, seed, sign_mask, omega_zero=False, multiple=1):
    dimension = 5
    rng = random.Random(seed)
    vertices = [0]+[(sign_mask>>i)&1 for i in range(5)]
    sd = {f: vertices[f[0]] ^ vertices[f[1]] for f in faces(1, dimension)}
    wd = differential(random_binary(rng, 1, dimension), 1, dimension)
    if omega_zero:
        wd = {f: 0 for f in wd}
    # Include signed arbitrary-precision carries, beyond machine-int range.
    potentials = [((-1)**i)*(2**(65+i*3)+rng.randrange(-8192, 8193)) for i in range(6)]
    nd = {f: multiple*((1-2*sd[f])*potentials[f[1]]-potentials[f[0]])
          for f in faces(1, dimension)}
    n, s, w = q.C(1, nd, mod=None), q.C(1, sd), q.C(2, wd)
    a = n.reduce(2)
    primary = q.sq(a, 2)+q.cup(w, a)+q.cup(s, q.sq(a, 1))
    if multiple == 16:
        b, c = q.C(2), q.C(3)
    else:
        dbound = differential(random_binary(rng, 1, dimension), 1, dimension)
        bd = {f: ((0 if 0 in f else primary((0,)+f))+dbound[f]) % 2
              for f in faces(2, dimension)}
        b = q.C(2, bd)
        parity = q.parity(n, b, w, s)
        cbound = differential(random_binary(rng, 2, dimension), 2, dimension)
        cd = {f: ((0 if 0 in f else parity((0,)+f))+cbound[f]) % 2
              for f in faces(3, dimension)}
        c = q.C(3, cd)
    data = {'n': n, 'b': b, 'c': c, 's': s, 'w': w}
    # Independent elementary coboundary checks plus both independently evaluated
    # source adapters; the oracle performs its own complete tower validation too.
    assert all(v == 0 for v in differential(sd, 1, dimension).values())
    assert all(v == 0 for v in differential(wd, 2, dimension).values())
    for i, j, k in faces(2, dimension):
        assert (1-2*sd[(i, j)])*nd[(j, k)]-nd[(i, k)]+nd[(i, j)] == 0
    for f in faces(3, dimension):
        assert b.d()(f) == primary(f) == evaluate(formula('pip_majorana', 1), data, f)
    parity = q.parity(n, b, w, s)
    for f in faces(4, dimension):
        assert c.d()(f) == parity(f) == evaluate(formula('pip_parity', 1), data, f)
    return data


def lower_fields(p, seed, dimension):
    rng = random.Random(seed)
    data = {'s': differential(random_binary(rng, 0, dimension), 0, dimension),
            'w': differential(random_binary(rng, 1, dimension), 1, dimension)}
    for a, c in [('a', 'c'), ('b', 'cp')]:
        data[a] = differential(random_binary(rng, p-1, dimension), p-1, dimension)
        source_data = dict(data, a=data[a])
        boundary = differential(random_binary(rng, p, dimension), p, dimension)
        data[c] = {f: (boundary[f]+(0 if 0 in f else evaluate(formula('majorana_source', p), source_data, (0,)+f))) % 2
                   for f in faces(p+1, dimension)}
        assert differential(data[c], p+1, dimension) == {
            f: evaluate(formula('majorana_source', p), source_data, f)
            for f in faces(p+2, dimension)}
    return data


def scalar_expression(compiled, data):
    builder, output, active = compiled
    values = {}
    for index in active:
        op, *args = builder.nodes[index]
        if op == 'const':
            value = args[0]
        elif op == 'field':
            f = data[args[0]]
            value = f(tuple(args[1])) if callable(f) else f[tuple(args[1])]
        elif op == 'add':
            value = values[args[0]]+values[args[1]]
        elif op == 'mul':
            value = values[args[0]]*values[args[1]]
        elif op == 'mod':
            value = values[args[0]] % args[1]
        elif op == 'div':
            value, remainder = divmod(values[args[0]], args[1])
            assert remainder == 0
        else:
            raise ValueError(op)
        values[index] = value
    return values[output]


def encode(data, degrees, dimension):
    # Consecutive independent C2 increments encode each ordered face by a tuple
    # of interval bitmasks. No group answer table enters these local fixtures.
    output = []
    for name, degree in degrees.items():
        field = data[name]
        rows = []
        for f in faces(degree, dimension):
            value = field(f) if callable(field) else field[f]
            rows.append([[sum(2**i for i in range(a, z)) for a, z in zip(f, f[1:])], value])
        output.append([name, rows])
    return output


def extra_background_identities(q):
    checks = {'closed_cf_obstruction': 0, 'cf_boundary_formula': 0,
              'cf_boundary_flatness': 0, 'ca_stacking_chain_faces': 0,
              'ca_obstruction_closure': 0}
    fixtures = []
    for seed in range(32):
        rng = random.Random(954321+seed)
        s = q.C(1, differential(random_binary(rng, 0, 5), 0, 5))
        w = q.C(2, differential(random_binary(rng, 1, 5), 1, 5))
        beta = q.C(2, random_binary(rng, 2, 5))
        c = beta.d()
        data = dict(a=q.C(2), c=c, beta=beta, w=w, s=s)
        closed_source = q.cup(c, c, 1)+q.cup(w, c)
        terminal = Fraction(evaluate(formula('obstruction', 2), data), 8)
        assert terminal == Fraction(closed_source(tuple(range(6))), 2)
        checks['closed_cf_obstruction'] += 1
        binary_primitive = q.cup(beta, beta)+q.cup(beta, beta.d(), 1)+q.cup(w, beta)
        phase = q.C(4, fun=lambda f: Fraction(binary_primitive(f), 2), mod=None)
        assert q.ds(phase, s)(tuple(range(6))) % 1 == terminal
        checks['cf_boundary_flatness'] += 1
        # A separately formed off-shell square expression retains beta cup1 d beta.
        for f in faces(4, 5):
            assert phase(f) == Fraction((q.sq(beta, 2)+q.cup(w, beta))(f), 2)
            checks['cf_boundary_formula'] += 1
        if seed < 8:
            fixtures.append(['cf_boundary', 2, ['a'], binary_primitive(tuple(range(5))), 2,
                             encode(data, {'a': 2, 'c': 3, 'beta': 2, 'w': 2, 's': 1}, 5)])
    for p in (1, 2):
        for seed in range(16):
            dimension = p+4
            data = lower_fields(p, 741926+100*p+seed, dimension)
            summed = dict(data)
            summed['a'] = {f: (data['a'][f]+data['b'][f]) % 2 for f in data['a']}
            summed['c'] = {f: (data['c'][f]+data['cp'][f]+evaluate(formula('majorana_product', p), data, f)) % 2
                           for f in data['c']}
            right = dict(data, a=data['b'], c=data['cp'])
            for f in faces(p+3, dimension):
                values = [evaluate(formula('stacking', p), data, f[:i]+f[i+1:]) for i in range(len(f))]
                delta = (1-2*data['s'][f[:2]])*values[0]+sum((-1)**i*values[i] for i in range(1, len(f)))
                expected = (evaluate(formula('obstruction', p), summed, f)
                            -evaluate(formula('obstruction', p), data, f)
                            -evaluate(formula('obstruction', p), right, f))
                assert (delta-expected) % 8 == 0, (p, seed, f)
                checks['ca_stacking_chain_faces'] += 1
            f = tuple(range(dimension+1))
            values = [evaluate(formula('obstruction', p), data, f[:i]+f[i+1:]) for i in range(len(f))]
            assert ((1-2*data['s'][f[:2]])*values[0]+sum((-1)**i*values[i] for i in range(1, len(f)))) % 8 == 0
            checks['ca_obstruction_closure'] += 1
            if p == 2 and seed < 8:
                fixtures.append(['ca_chain', 2, [], 0, 1,
                                 encode(data, {'a': 2, 'b': 2, 'c': 3, 'cp': 3, 'w': 2, 's': 1}, 5)])
    return checks, fixtures


def controls(sign_patterns=32):
    started = time.time()
    before = hashes()
    q, oracle = import_oracle()
    general = json.loads((ROOT/'gap/pip_o5_background.json').read_text())
    accepted_text = (ROOT/'results/space_groups/source/gap/pip_o5_program.g').read_text()
    match = re.fullmatch(r'AFSPipO5Program := (.*);;\nAFSPipO5Output := (\d+);;\n', accepted_text)
    assert match, 'Unknown immutable accepted scalar graph format'
    accepted = {'program': json.loads(match.group(1)), 'output': int(match.group(2))-1}
    live = json.loads((ROOT/'gap/pip_o5_program.json').read_text())
    assert live['program'] == accepted['program'] and live['output'] == accepted['output']
    assert (ROOT/'gap/pip_o5_program.g').read_bytes() == (ROOT/'results/space_groups/source/gap/pip_o5_program.g').read_bytes()
    assert general['omega_zero'] is False
    counts = {'full_omega_legal_oracle': 0, 'omega_zero_accepted_regression': 0,
              'sixteen_multiple_zero_tower': 0, 'lower_compiled_interpreter': 0,
              'pip_defining_source_faces': 0}
    fixtures = []
    max_integer = 0
    for mask in range(sign_patterns):
        for kind in ('full', 'zero', 'sixteen'):
            data = legal_pip(q, 381792+mask*7+(kind == 'sixteen'), mask,
                             omega_zero=(kind == 'zero'), multiple=16 if kind == 'sixteen' else 1)
            expected = oracle(1, n_integer=data['n'], n_majorana=data['b'],
                              n_fermion=data['c'], omega2=data['w'], s1=data['s'])['numerator_mod16']
            actual = evaluate_program(general, data)
            assert actual == expected, (kind, mask, actual, expected)
            counts['pip_defining_source_faces'] += 21  # C(6,4)+C(6,5)
            if kind == 'full':
                counts['full_omega_legal_oracle'] += 1
            elif kind == 'zero':
                assert actual == evaluate_program(accepted, data)
                counts['omega_zero_accepted_regression'] += 1
            else:
                assert actual == 0
                counts['sixteen_multiple_zero_tower'] += 1
            max_integer = max(max_integer, *(abs(data['n'](f)) for f in faces(1, 5)))
            if mask < min(sign_patterns, 8):
                fixtures.append(['pip_obstruction', 1, ['w'] if kind == 'zero' else [], expected, 16,
                                 encode(data, {'n': 1, 'b': 2, 'c': 3, 's': 1, 'w': 2}, 5)])
    for p in (1, 2):
        for name in ('obstruction', 'stacking', 'majorana_source', 'majorana_product'):
            expression = formula(name, p)
            zerosets = [(), ('s',), ('w',), ('w', 's')]
            if name == 'obstruction':
                zerosets += [('a',), ('a', 's'), ('w', 'a'), ('w', 'a', 's')]
            programs = {zeros: compile_expression(expression, zeros) for zeros in zerosets}
            for seed in range(8):
                original = lower_fields(p, 659273+100*p+seed, p+4)
                for zeros, program in programs.items():
                    data = {k: dict(v) for k, v in original.items()}
                    for k in zeros:
                        data[k] = {f: 0 for f in data[k]}
                    expected = evaluate(expression, data)
                    assert scalar_expression(program, data) == expected, (name, p, seed, zeros)
                    counts['lower_compiled_interpreter'] += 1
                    if seed < 2:
                        fixtures.append([name, p, list(zeros), expected,
                                         8 if name in ('obstruction', 'stacking') else 1,
                                         encode(data, {'a': p, 'b': p, 'c': p+1, 'cp': p+1, 's': 1, 'w': 2}, expression.degree)])
    extra_checks, extra_fixtures = extra_background_identities(q)
    counts.update(extra_checks)
    fixtures.extend(extra_fixtures)
    after = hashes()
    assert before == after, 'Formula files changed during the audit'
    report = {'schema': 'fspt-arbitrary-background-formula-controls-v1', 'status': 'python-passed-gap-pending',
              'scope': 'Finite local exact arithmetic controls; no new space-group classification or general-background stacking certification.',
              'formula_convention': 'normalized-pip-aw-edge-transport-v2',
              'checks': counts, 'sign_patterns': sign_patterns, 'maximum_absolute_integer': str(max_integer),
              'operations': len(general['program']), 'source_sha256': before,
              'elapsed_seconds': time.time()-started, 'gap_fixtures': len(fixtures),
              'oracle': 'Unmodified vendor/p_ip_d4_normalized_package/code/pip_d4.py::evaluate_simplex(validate=True)',
              'limitations': ['Finite deterministic sample of closed omega and signed integer cocycles; not exhaustive in omega or integer cochains.',
                              'Specialized lower-formula variants also checked off shell after setting selected input fields to zero.',
                              'No physical Pin-minus classification or nonzero-omega p+ip multiplication is inferred.']}
    return report, fixtures


GAP_DRIVER = r'''
OnBreak:=function() Where(12);QUIT_GAP(1);end;;
AFS_ROOT:=AFS_BACKGROUND_TEST_SOURCE;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/formula_data.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/formula_fast.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/formulas.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/pip_o5_program.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/pip_o5_general.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/pip_o5_sign.g"));;
Read(Concatenation(AFS_BACKGROUND_TEST_SOURCE,"/gap/pip_o5_background.g"));;
Read(Concatenation(AFS_ROOT,"/gap/stacking.g"));;
Read(Concatenation(AFS_ROOT,"/gap/stacking_closed_cf.g"));;
AFSMakeFixtureField:=function(rows,els)
  local inputs,outputs;
  inputs:=List(rows,row->List(row[1],x->els[x+1]));outputs:=List(rows,row->row[2]);
  return function(arg...) local pos;pos:=Position(inputs,arg);
    if pos=fail then if ForAny(arg,x->IsOne(x)) then return 0;fi;Error("Missing fixture face");fi;
    return outputs[pos];end;
end;;
G:=ElementaryAbelianGroup(64);;gs:=GeneratorsOfGroup(G);;
els:=List([0..63],x->Product([1..6],i->gs[i]^(QuoInt(x,2^(i-1)) mod 2)));;
checks:=0;;
for item in AFSBackgroundFixtures do
  fields:=rec(p:=item[2]);;
  for row in item[6] do fields.(row[1]):=AFSMakeFixtureField(row[2],els);od;
  for z in item[3] do fields.(z):=AFSZero;od;
  ctx:=rec(G:=G,s:=fields.s,omega2:=fields.w);;
  ctx.sign:=g->1-2*ctx.s(g);;
  if item[1]="cf_boundary" then
    state:=AFSStackCFBoundary(ctx,fields.beta);;
    Assert(0,CallFuncList(state.v,gs{[1..4]})=item[4]/item[5]);
    Assert(0,CallFuncList(state.c,gs{[1..3]})=CallFuncList(fields.c,gs{[1..3]}));
    source:=AFSFormula("obstruction",ctx,rec(p:=2,a:=AFSZero,c:=state.c));;
    short:=AFSCoadd(1,[AFSClosedCFObstructionLazy(state.c),AFSComul(1,1/2,AFSCup(0,2,ctx.omega2,3,state.c))]);;
    Assert(0,CallFuncList(source,gs{[1..5]})=CallFuncList(short,gs{[1..5]}));
    Assert(0,CallFuncList(AFSCoboundary(ctx,"U1s",state.v),gs{[1..5]})=CallFuncList(source,gs{[1..5]}));
    Assert(0,CallFuncList(AFSCoboundary(ctx,"F2",state.c),gs{[1..4]})=0);
    checks:=checks+1;continue;
  elif item[1]="ca_chain" then
    left:=rec(a:=fields.a,c:=fields.c,v:=AFSZero);right:=rec(a:=fields.b,c:=fields.cp,v:=AFSZero);;
    product:=AFSStackProduct(ctx,left,right);;
    oleft:=AFSFormula("obstruction",ctx,rec(p:=2,a:=left.a,c:=left.c));;
    oright:=AFSFormula("obstruction",ctx,rec(p:=2,a:=right.a,c:=right.c));;
    oproduct:=AFSFormula("obstruction",ctx,rec(p:=2,a:=product.a,c:=product.c));;
    residual:=AFSCoadd(1,[AFSCoboundary(ctx,"U1s",product.v),oleft,oright,AFSComul(1,-1,oproduct)]);;
    Assert(0,CallFuncList(residual,gs{[1..5]})=0);
    checks:=checks+1;continue;
  fi;
  explicit:=AFSFormula(item[1],ctx,fields);;
  Unbind(fields.w);;
  implicit:=AFSFormula(item[1],ctx,fields);;
  if item[1]="pip_obstruction" then degree:=5;
  else degree:=AFSFormulaData.(Concatenation(item[1],"_",String(item[2])))[2];fi;
  expected:=item[4]/item[5];;
  Assert(0,CallFuncList(explicit,gs{[1..degree]})=expected);
  Assert(0,CallFuncList(implicit,gs{[1..degree]})=expected);
  Assert(0,CallFuncList(implicit,Concatenation([One(G)],gs{[2..degree]}))=0);
  # Explicit omega=0 must override a nonzero background callback on the context.
  if "w" in item[3] then
    ctx.omega2:=function(x,y) return 1;end;;fields.w:=AFSZero;
    override:=AFSFormula(item[1],ctx,fields);
    Assert(0,CallFuncList(override,gs{[1..degree]})=expected);
  fi;
  if item[1]<>"pip_obstruction" then
    AFSUseFastFormulas:=false;;slow:=AFSFormula(item[1],rec(G:=G,s:=fields.s,omega2:=AFSZero),fields);;
    # Restore the intended background when it was omitted for implicit checking.
    if not IsBound(fields.w) then
      slow:=AFSFormula(item[1],rec(G:=G,s:=fields.s,omega2:=ctx.omega2),fields);
    fi;
    Assert(0,CallFuncList(slow,gs{[1..degree]})=expected);
    AFSUseFastFormulas:=true;;
  fi;
  checks:=checks+1;
od;
Print("BACKGROUND_FORMULA_GAP_PASS fixtures=",checks," background_calls=",AFSPipO5BackgroundCalls,"\n");
QUIT_GAP(0);
'''


class BackgroundFormulaTests(unittest.TestCase):
    @unittest.skipUnless((VENDOR/'pip_d4.py').is_file(), 'optional unchanged supplied formula oracle unavailable')
    def test_small_independent_background_control(self):
        report, _ = controls(sign_patterns=2)
        self.assertEqual(report['checks']['full_omega_legal_oracle'], 2)
        self.assertEqual(report['checks']['lower_compiled_interpreter'], 320)


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--sign-patterns', type=int, choices=range(1, 33), default=32)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--gap-output', type=Path)
    parser.add_argument('--gap-source', default='runs/background_formula_controls_source')
    args = parser.parse_args()
    report, fixtures = controls(args.sign_patterns)
    if args.gap_output:
        args.gap_output.parent.mkdir(parents=True, exist_ok=True)
        args.gap_output.write_text('AFS_BACKGROUND_TEST_SOURCE:='+gap_literal(args.gap_source)+';;\n'
                                  +'AFSBackgroundFixtures:='+gap_literal(fixtures)+';;\n'+GAP_DRIVER)
        report['gap_driver_sha256'] = hashlib.sha256(args.gap_output.read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'source_sha256'}, indent=2))


if __name__ == '__main__':
    main()
