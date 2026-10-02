"""Compile the complete supplied local operations to shared scalar programs.

Compilation is group independent. No known classification, fitted phase table,
or cohomology solver contributes to a generated operation. Publication modules
supply expression syntax and fixed coefficients; runtime imports none of them.
Run one build target per fresh process to isolate their historical namespaces.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib
import itertools
import json
import os
from pathlib import Path
import sys
import tempfile
import time

from fspt.formulas_pip_compile import Builder, Scalar


def atomic_write_bytes(path, raw):
    """Publish a complete kernel without exposing partial bytes to snapshots."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='wb', prefix='.'+path.name+'.',
                suffix='.tmp', dir=str(path.parent), delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temporary), str(path))
        temporary = None
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def compact_program(builder, outputs, metadata):
    pending = [x.index for x in outputs]
    active = set()
    while pending:
        i = pending.pop()
        if i in active:
            continue
        active.add(i)
        op, *args = builder.nodes[i]
        if op in ('add', 'mul'):
            pending.extend(args[:2])
        elif op in ('mod', 'div', 'floor', 'bit'):
            pending.append(args[0])
    ordered = sorted(active)
    remap = {i: j for j, i in enumerate(ordered)}
    nodes = []
    for i in ordered:
        op, *args = builder.nodes[i]
        if op in ('add', 'mul'):
            args[:2] = [remap[a] for a in args[:2]]
        elif op in ('mod', 'div', 'floor', 'bit'):
            args[0] = remap[args[0]]
        nodes.append([op] + args)
    return dict(metadata, program=nodes, outputs=[remap[x.index] for x in outputs])


class Compiler:
    def __init__(self, source):
        self.source = Path(source).resolve()
        self.reference = self.source / 'reference/d4_input/code'
        sys.setrecursionlimit(100000)
        # Full-background modules put their own historic dependencies on sys.path.
        sys.path[:0] = [str(self.source / x) for x in
                       ('full4', 'full3', 'unitary4', 'bosonic',
                        'terminal_general', 'joint', 'omega3')]
        sys.path.insert(0, str(self.reference))
        self.cc = importlib.import_module('cochains')
        self.builder = Builder()
        self.install_symbolic_quotients()
        self.install_total_table()

    def field(self, name, degree, mod=2):
        return self.cc.C(degree, fun=lambda face: self.builder.make(
            'field', name, tuple(face)), mod=mod)

    def install_symbolic_quotients(self):
        C, B = self.cc.C, self.builder
        def div(a, k):
            if a.mod is not None:
                raise ValueError('Integer division requires an integral cochain')
            if a.known_zero:
                return C(a.deg, mod=None)
            result = C(a.deg, fun=lambda f: B.divide(a(f), k), mod=None)
            result.closed = a.closed
            return result
        C.div = div

    def install_total_table(self):
        tables = importlib.import_module('polynomial_tables')
        C, B, reference = self.cc.C, self.builder, self.reference
        def total(n, w, s, filename, degree, **kwargs):
            data = json.loads((reference / filename).read_text())
            def evaluate(face):
                ans = B.scalar(0)
                for block in data['blocks']:
                    i, j, k = block['i'], block['j'], block['k']
                    if i+j+k != degree:
                        raise ValueError('Coefficient table degree mismatch')
                    term0 = B.scalar(1)
                    for t in range(1, i+1):
                        term0 *= s((face[t-1], face[t]))
                    middle, last = face[i:i+j+1], face[i+j:]
                    def transported(f):
                        return n(f) * (1 if face[0] == f[0] else
                                       1-2*s((face[0], f[0])))
                    if n.deg == 1:
                        ns = [transported((middle[t-1], middle[t]))
                              for t in range(1, j+1)]
                    else:
                        ns = [transported((middle[u-1], middle[u], middle[v])) -
                              transported((middle[u-1], middle[u], middle[v-1]))
                              for u, v in itertools.combinations(range(1, j+1), 2)]
                    ws = [w((last[u-1], last[u], last[v])) ^
                          w((last[u-1], last[u], last[v-1]))
                          for u, v in itertools.combinations(range(1, k+1), 2)]
                    for nc, wc in block['terms']:
                        term, nc = term0, int(nc)
                        for e, value in enumerate(ns):
                            mask = (nc >> (4*e)) & 15
                            for bit in range(4):
                                if mask & (1 << bit):
                                    term *= B.bit(value, bit)
                        for e, value in enumerate(ws):
                            if wc & (1 << e):
                                term *= value
                        ans += term
                return ans % 2
            return C(degree, fun=evaluate)
        tables.total_cochain = total

    def fields(self, p, pair=False, native=True):
        C, cup = self.cc.C, self.cc.cup
        n, a, c = self.field('n', p, None), self.field('a', p+1), self.field('c', p+2)
        w, s = self.field('w', 2), self.field('s', 1)
        w.closed = s.closed = True
        carry = lambda x: (x-x.reduce(2).lift()).div(2).reduce(2)
        u = a + cup(s, carry(n)) if native else a
        if not pair:
            return n, u, c, w, s
        m, b, cp = self.field('m', p, None), self.field('b', p+1), self.field('cp', p+2)
        v = b + cup(s, carry(m)) if native else b
        return n, u, c, m, v, cp, w, s

    def high(self, mode):
        """Shared high source, binary part, and pure Y6 completion."""
        cc = self.cc
        src = importlib.import_module('source')
        n, u, c, w, s = self.fields(2, native=False)
        if mode == 'y6':
            explicit = importlib.import_module('explicit_pip')
            value = explicit.binary_completion(n, w, s, accelerate=False)
            return [value(tuple(range(7)))], dict(top_degree=6, denominator=2)
        y = self.field('y', 6)
        H, Q, Pn, Wnn = src.blocks(n, u, c, w, s, y)
        if mode == 'h6':
            # rho uses the c-independent binary source block.
            H, _, _, _ = src.blocks(n, u, cc.C(4), w, s, y)
            values = [H(tuple(range(7)))]
            return values, dict(top_degree=6, denominator=2)
        high = H.lift().scaled(8)+Q.scaled(4)+Pn+Wnn.scaled(2)
        cubic = cc.cup(n, cc.cup(n, n, s=s, twists=(1,1)), s=s, twists=(1,0))
        return [high(tuple(range(7))) % 16, cubic(tuple(range(7)))], dict(
            top_degree=6, denominator=16, output_names=['high16', 'cube'])

    def lower(self, p, mode, stage):
        cc, cup = self.cc, self.cc.cup
        if mode == 'source':
            n, u, c, w, s = self.fields(p)
            a = n.reduce(2)
            native = self.field('a', p+1)
            result = (cc.sq(a, 2)+cup(w, a)+cup(s, cc.sq(a, 1))
                      if stage == 'majorana' else cc.parity(n, native, w, s))
        else:
            n, u, c, m, v, cp, w, s = self.fields(p, pair=True)
            if stage == 'majorana':
                a, b = n.reduce(2), m.reduce(2)
                result = cup(a,b,p-1)+cup(s,cup(a,b,p))
            else:
                third = importlib.import_module('fractional').third_product
                result = third(n,u,m,v,w,s)
                if p == 2:
                    result = result + cup(n.reduce(2),m.reduce(2))
        degree = result.deg
        return [result(tuple(range(degree+1)))], dict(top_degree=degree, denominator=2)

    def nonbinary4(self):
        product = importlib.import_module('product_full')
        args = self.fields(2, pair=True, native=False)
        result = product.collected_blocks(*args)['nonbinary48']
        return [result(tuple(range(6))) % 48], dict(top_degree=5, denominator=48)

    def rho4(self):
        """General residual without value-dependent reference shortcuts.

        The three H values are cached separately by the runtime. All other
        arithmetic is compiled once; neither primitive solves nor Python
        cochain evaluation occurs during a production transfer.
        """
        cc, cup, C = self.cc, self.cc.cup, self.cc.C
        k = importlib.import_module('kernel_full')
        n,u,c,m,v,cp,w,s = self.fields(2, pair=True, native=False)
        D = k.pair_data(n,u,m,v,w,s)
        N,U,B,Bp,BN = (D[x] for x in ('N','U','B','Bp','BN'))
        W,vi,alpha,hv,P = cc.background_data(w,s)
        ef = k.fractional_seed16(n,u,m,v,w,s,native=False)
        V = (ef-cup(W.lift(),D['T'],s=s,twists=(1,0)).scaled(2)).div(4).reduce(2)
        Q = lambda x: cup(x,x,2)+cup(x,x.d(),3)
        I = (Q(BN)-Q(B)-Q(Bp)+cup(w.lift(),D['lambda'].d()-D['R'])
             -k.cartan_word(N,w,s).lift()+k.cartan_word(n,w,s).lift()+k.cartan_word(m,w,s).lift()
             +cup(W.lift(),D['R'],s=s,twists=(1,0))-cup(vi,D['T'],s=s,twists=(1,0))-cc.ds(V.lift(),s))
        F = k.kappa(u,w,s)+cc.pure_parity(n,w,s)
        Fp = k.kappa(v,w,s)+cc.pure_parity(m,w,s)
        e = k.third_product(n,u,m,v,w,s)
        change = (k.binary_correction(N,U,w,s)+k.binary_correction(n,u,w,s)+k.binary_correction(m,v,w,s)
                  +cup(W,D['R'].reduce(2))+cup(alpha,D['t'])+cup(W,cup(n.reduce(2),m.reduce(2))))
        result = (k.upper_residual(F,Fp,e,w)+I.div(2).reduce(2)+change)(tuple(range(7)))
        outputs = [result % 2]
        outputs += [U(face) for face in itertools.combinations(range(7),4)]
        return outputs, dict(top_degree=6, denominator=2,
                             output_names=['rho_without_H']+['U_'+''.join(map(str,f)) for f in itertools.combinations(range(7),4)])

    def tensor4(self):
        # Lstar is a finite displayed tensor cochain; compile its complete
        # polarization and the two fixed signed shuffle corrections.
        trans = importlib.import_module('transfer_model')
        tensor = importlib.import_module('tensor_compact')
        tensor.digit = lambda value, bit: self.builder.bit(value,bit)
        n,u,c,m,v,cp,w,s = self.fields(2, pair=True, native=False)
        top = tuple(range(6))
        value = (tensor.tensor5(n,u,m,v)(top)
                 +trans.sh_diff(2,3,n,u,m,v)+trans.sh_diff(3,2,n,u,m,v)) % 2
        return [value], dict(top_degree=5, denominator=2)

    def majorana4_product(self):
        """Compile the n=m=0 specialization in the SAME publication coordinate.

        At zero integers the chart first-face perturbation is identically zero:
        qroot(W,n)=qroot(W,m)=0. The tensor primitive has bidegrees (2,3) and
        (3,2), so it vanishes when both surviving fiber fields have degree3.
        The complete binary primitive is therefore the fixed finite sum H*rho.
        Expanding that sum once removes all runtime transfer combinatorics.
        """
        cc=self.cc
        frac=importlib.import_module('fractional')
        product=importlib.import_module('product_full')
        ez=importlib.import_module('ez_homotopy')
        a,b=self.field('a',3),self.field('b',3)
        c,cp=self.field('c',4),self.field('cp',4)
        w,s=self.field('w',2),self.field('s',1)
        w.closed=s.closed=True
        zero=cc.C(2,mod=None)
        nonbinary=product.collected_blocks(zero,a,c,zero,b,cp,w,s)['nonbinary48']
        top=tuple(range(6));binary=self.builder.scalar(0);cuts=0
        for simplex in ez.ez_homotopy(5):
            projections=tuple(tuple(v[j] for v in simplex) for j in range(3))
            if min(len(set(projections[j])) for j in (1,2))<4:
                continue
            def pull(x,slot):
                out=cc.C(x.deg,fun=lambda f:x(tuple(projections[slot][i] for i in f)),mod=x.mod)
                out.closed=x.closed
                return out
            aa,bb,ww,ss=pull(a,1),pull(b,2),pull(w,0),pull(s,0)
            residual,_=frac.terminal_residual(zero,aa,zero,bb,ww,ss,
                                              ys=[cc.C(6),cc.C(6),cc.C(6)])
            binary+=residual(tuple(range(7)))
            cuts+=1
        value=(nonbinary(top)+24*(binary%2))%48
        return [value],dict(top_degree=5,denominator=48,integer_zero=True,
                            finite_homotopy_cuts=cuts)

    def dictionary4(self):
        cc=self.cc
        n,u,c,w,s=self.fields(2)
        frac=importlib.import_module('fractional')
        repair=importlib.import_module('cubic_repair')
        change=cc.ds(frac.state_rephasing16(n,u,w,s),s).scaled(3)+repair.cube(n,s).scaled(4)
        return [change(tuple(range(7)))%48],dict(top_degree=6,denominator=48,
                    interpretation='current O6 minus raw normalized O6')

    def lift3(self, kind):
        lower = importlib.import_module('lower')
        prism = importlib.import_module('prism')
        if kind == 'source':
            fields = lower.fields_on_interval(*self.fields(1))
            parameter, base = (0,1), tuple(range(6))
        else:
            fields = lower.fields_on_triangle(*self.fields(1,pair=True))
            parameter, base = (0,1,2), tuple(range(5))
        outputs, calls = [], []
        for path, sign in prism.shuffles(parameter,base):
            start = len(outputs)
            for x in fields:
                outputs.extend(x(tuple(path[i] for i in face))
                               for face in itertools.combinations(range(7),x.deg+1))
            calls.append(dict(offset=start,sign=sign))
        return outputs, dict(top_degree=len(base)-1, denominator=16,
                             kind=kind, high_fields=['n','a','c','w','s'],
                             high_degrees=[2,3,4,2,1], calls=calls)

    def build(self, name):
        if name in ('y6','h6','high6'):
            outputs, metadata = self.high(name)
        elif name == 'nonbinary4':
            outputs, metadata = self.nonbinary4()
        elif name == 'rho4':
            outputs, metadata = self.rho4()
        elif name == 'tensor4':
            outputs, metadata = self.tensor4()
        elif name == 'majorana4_product':
            outputs, metadata = self.majorana4_product()
        elif name == 'dictionary4':
            outputs, metadata = self.dictionary4()
        elif name in ('lift3_source','lift3_product'):
            outputs, metadata = self.lift3(name.split('_')[1])
        else:
            mode, dimension, stage = name.split('_')
            outputs, metadata = self.lower(int(dimension)-2,mode,stage)
        hashes = {}
        for path in self.source.rglob('*.py'):
            hashes[str(path.relative_to(self.source))] = hashlib.sha256(path.read_bytes()).hexdigest()
        for path in self.reference.glob('*.json'):
            hashes[str(path.relative_to(self.source))] = hashlib.sha256(path.read_bytes()).hexdigest()
        metadata.update(name=name, coordinate='publication-20260930-native',
                        compiler_version=1, source_hashes=hashes)
        return compact_program(self.builder, [self.builder.scalar(x) for x in outputs], metadata)


TARGETS = ('y6','h6','high6','nonbinary4','rho4','tensor4','majorana4_product','dictionary4',
           'lift3_source','lift3_product') + tuple(
    '{}_{}_{}'.format(mode,dimension,stage) for mode in ('source','product')
    for dimension in (3,4) for stage in ('majorana','fermion'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--target',choices=TARGETS,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    started = time.monotonic()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    os.environ['FULL4_CACHE_PATH'] = str(args.out.with_suffix('.compile-cache.pickle'))
    result = Compiler(args.source).build(args.target)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    raw = (json.dumps(result,separators=(',',':'))+'\n').encode()
    atomic_write_bytes(args.out, raw)
    print(json.dumps(dict(target=args.target,nodes=len(result['program']),
                          outputs=len(result['outputs']),seconds=time.monotonic()-started,
                          sha256=hashlib.sha256(raw).hexdigest())),flush=True)

if __name__ == '__main__':
    main()
