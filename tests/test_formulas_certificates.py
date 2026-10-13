"""Universal F2 coefficient identities for both frozen polarization tables.

Adapted from verify_certificates.py, symbolic.py and symbolic_r_block.py in
U1f_AHSS_Consolidated_v0_7. No fitting, linear solve, or random sampling.
"""
from itertools import combinations
from pathlib import Path
import json
import unittest
from insulator._engine.simplex import C, primitive, word, cartan32
from insulator._engine.product4d import P32, CP

class P:
    def __init__(self,m=()):self.m=frozenset(m)
    def __add__(self,o):
        if not isinstance(o,P):o=P([0]) if o%2 else P()
        return P(self.m^o.m)
    __radd__=__add__
    def __neg__(self):return self
    def __sub__(self,o):return self+o
    def __mul__(self,o):
        if not isinstance(o,P):return self if o%2 else P()
        out=set()
        for a in self.m:
            for b in o.m:
                c=a|b
                if c in out:out.remove(c)
                else:out.add(c)
        return P(out)
    __rmul__=__mul__
    def __mod__(self,m):
        assert m==2
        return self
    def __repr__(self):return f'P[{len(self.m)}]'
    def __eq__(self,o):return isinstance(o,P) and self.m==o.m
    def __bool__(self):return bool(self.m)

def var(i):return P([1<<i])

def cocycle(N,p,start=0):
    base=list(combinations(range(1,N+1),p));ind={f:var(start+i) for i,f in enumerate(base)};v={}
    for f in combinations(range(N+1),p+1):
        v[f]=ind[f[1:]] if f[0]==0 else sum(ind[f[:j]+f[j+1:]] for j in range(len(f)))
    return C(N,p,v),start+len(base)


def sym_inputs(N):
 r,off=cocycle(N,1);s,off=cocycle(N,1,off);x,off=cocycle(N,2,off);y,off=cocycle(N,2,off)
 hxf,off=cocycle(N,2,off);hyf,off=cocycle(N,2,off)
 hx=primitive(x.sq(1)+s.cup(x,0,True))+hxf
 hy=primitive(y.sq(1)+s.cup(y,0,True))+hyf
 return r,s,x,y,hx,hy,off

def sym_J(x,hx,r,s):
 L=x.cup(x,0,True)
 hL=C(x.N,4,{f:hx(f[:3])*x(f[2:])+x(f[:3])*hx(f[2:])+s((f[0],f[2]))*x(f[:3])*x(f[2:]) for f in combinations(range(x.N+1),5)})
 K=word((1,2,3,1,3,4,3),x,x,x,x)+hx.cup(x.sq(1),0,True)+s.cup(x,0,True).cup(hx,0,True)+s.cup(x.cup(s,1,True),0,True).cup(x,0,True)
 reorder=(r.cup(s,1,True).cup(r,0,True)+s.sq(1).cup(r,1,True)).cup(L,0,True)
 return word((1,2,3,1,4,3,4,3),r,r,L,L)+r.sq(1).cup(hL,0,True)+r.cup(K,0,True)+reorder

def residual(N):
 r,s,x,y,hx,hy,off=sym_inputs(N);eta=(r+s).cup(s,0,True)
 h=x.cup(y,1,True);e=x.cup(y,0,True)+r.cup(h,0,True)
 V=r.cup(x.cup(x,0,True),0,True);Vp=r.cup(y.cup(y,0,True),0,True)
 Jdiff=sym_J(x+y,hx+hy+x.cup(y,2,True),r,s)+sym_J(x,hx,r,s)+sym_J(y,hy,r,s)
 R=e.sq(2)+eta.cup(e,0,True)+V.cup(Vp,4,True)+(V+Vp).cup(e.d(),4,True)+Jdiff
 R=R+r.sq(1).cup(x.cup(y,0,True),0,True)+s.cup(r.sq(1),0,True).cup(h,0,True)+x.cup(x,0,True).cup(y,0,True)+x.cup(y,0,True).cup(y,0,True)
 # Remove the known r=0 carry-assisted Cartan primitive.
 H22=word((1,2,3,1,3,4,3),x,x,y,y)+hx.cup(y.sq(1),0,True)+s.cup(x,0,True).cup(hy,0,True)+s.cup(x.cup(s,1,True),0,True).cup(y,0,True)
 return (R+H22.d()).mod(2),(r,s,x,y,hx,hy,off)


class UniversalCertificates(unittest.TestCase):
    def test_closed_charge_cylinder_gauge_has_explicit_exact_difference(self):
        from insulator._engine.prism import pull_on_path, evalface, interval_paths

        # Work over the universal Boolean polynomial ring. The charge cocycle
        # and arbitrary gauge parameter have 14 (p=3) or 20 (p=4) free bits.
        # Half-valued phases forget all coefficient signs modulo one.
        for p in (3, 4):
            N = p + 1
            charge, offset = cocycle(N, p)
            faces = list(combinations(range(N + 1), p))
            parameter = C(N, p - 1, {face: var(offset + i) for i, face in enumerate(faces)})
            cylinder = P()
            for path, sign in interval_paths(N):
                pulled_charge = pull_on_path(charge, path)
                height_parameter = C(N + 1, p - 1, {
                    face: path[face[0]][0] * evalface(parameter, tuple(path[j][1] for j in face))
                    for face in combinations(range(N + 2), p)})
                cylinder_charge = pulled_charge + height_parameter.d()
                cylinder += cylinder_charge.sq(2)(tuple(range(N + 2)))
            short = (parameter.sq(2) + charge.cup(parameter.d(), p - 1, True)
                     + charge.d().cup(parameter.d(), p, True))
            witness = charge.cup(parameter, p - 1, True)
            top = tuple(range(N + 1))
            self.assertFalse(cylinder + short(top) + witness.d()(top))

    def test_cartan32_all_coefficients_and_degeneracies(self):
        z, off = cocycle(6, 3)
        x, off = cocycle(6, 2, off)
        y, off = cocycle(6, 2, off)
        target = (cartan32(z, x+y) + cartan32(z, x) + cartan32(z, y)
                  + z.cup(x,0,True).cup(z.cup(y,0,True),4,True)
                  + z.sq(1).cup(x.cup(y,2,True),0,True)
                  + z.cup(x.cup(y,1,True),0,True)).mod(2)
        self.assertFalse((P32(z,x,y).d() + target)(tuple(range(7))))
        self.assertEqual(len(CP['terms']), 814)
        zz, off = cocycle(4,3)
        xx, off = cocycle(4,2,off)
        yy, off = cocycle(4,2,off)
        for j in range(5):
            f = tuple(list(range(j+1)) + [j] + list(range(j+1,5)))
            def ev(c, ff):
                return P() if len(set(ff)) < len(ff) else c(ff)
            zs = [ev(zz,(f[0],)+tuple(f[i] for i in ff)) for ff in CP['z_faces']]
            xs = [ev(xx,(f[0],)+tuple(f[i] for i in ff)) for ff in CP['x_faces']]
            ys = [ev(yy,(f[0],)+tuple(f[i] for i in ff)) for ff in CP['x_faces']]
            total = P()
            for iz, ix, iy in CP['terms']:
                value = xs[ix] * ys[iy]
                for q in iz:
                    value = value * zs[q]
                total = total + value
            self.assertFalse(total)

    def test_charge_conjugation_all_coefficients_and_degeneracies(self):
        path = Path(__file__).resolve().parents[1] / 'insulator/_engine/r_polarizer.json'
        spec = json.loads(path.read_text())
        terms = [int(m,16) for m in spec['terms_hex']]
        self.assertEqual(len(terms), 3117)
        def table(fields, f):
            vv = [fields[sp](tuple(f[i] for i in ff))
                  if len(set(f[i] for i in ff)) == len(ff) else P()
                  for sp, ff in spec['variables']]
            total = P()
            for monomial in terms:
                out = P([0])
                while monomial and out:
                    bit = monomial & -monomial
                    out = out * vv[bit.bit_length()-1]
                    monomial -= bit
                total = total + out
            return total
        target, data = residual(6)
        value = sum(table(data[:-1], f) for f in combinations(range(7),6))
        self.assertFalse(value + target(tuple(range(7))))
        fields = sym_inputs(4)[:-1]
        for j in range(5):
            face = tuple(list(range(j+1)) + [j] + list(range(j+1,5)))
            self.assertFalse(table(fields, face))

if __name__ == '__main__':
    unittest.main()
