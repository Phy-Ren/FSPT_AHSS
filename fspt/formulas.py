"""Exact cochain formulas, independent of a resolution or classification table.

The expression graph is evaluated on ordered faces in Python and exported to
the GAP native-resolution adapter. Phases use integer numerators modulo eight.
The two leading degrees refer to Majorana chains, not the integer p+ip layer.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
from typing import Callable, Mapping


@lru_cache(None)
def cuts(word: tuple[int, ...], degrees: tuple[int, ...]):
    """Literal interval definition; no table of phase values is consulted."""
    degree = sum(degrees) - len(word) + len(degrees)
    if degree < 0:
        return ()
    result = []
    for middle in combinations_with_replacement(range(degree + 1), len(word) - 1):
        endpoints = (0,) + middle + (degree,)
        faces = []
        for label, d in enumerate(degrees, 1):
            vertices = tuple(v for j, x in enumerate(word) if x == label
                             for v in range(endpoints[j], endpoints[j + 1] + 1))
            if len(vertices) != d + 1 or len(set(vertices)) != len(vertices):
                break
            faces.append(vertices)
        else:
            lengths = tuple(endpoints[j + 1] - endpoints[j] + 1 for j in range(len(word)))
            exponent = sum(lengths[i] * lengths[j]
                           for i in range(len(word)) for j in range(i + 1, len(word))
                           if word[i] > word[j])
            result.append((tuple(faces), (-1) ** exponent))
    return tuple(result)


@dataclass(frozen=True, eq=False)
class Cochain:
    degree: int
    modulus: int | None
    operation: str
    arguments: tuple = ()

    def __add__(self, other):
        if self.degree != other.degree:
            raise ValueError(("degree mismatch", self.degree, other.degree))
        modulus = self.modulus if self.modulus == other.modulus else None
        return node(self.degree, modulus, "add", self, other)

    def __sub__(self, other):
        return self + other.scale(-1)

    def __mul__(self, other):
        return cup(self, other)

    def scale(self, factor):
        return node(self.degree, self.modulus, "scale", self, factor)

    def reduce(self, modulus=2):
        return node(self.degree, modulus, "reduce", self)

    def lift(self):
        return self.reduce(None)

    def divide(self, divisor):
        if self.modulus is not None:
            raise ValueError("Exact division requires integer coefficients")
        return node(self.degree, None, "divide", self, divisor)

    def differential(self):
        return node(self.degree + 1, self.modulus, "d", self)

    def beta(self):
        return self.lift().differential().divide(2)

    def twisted_differential(self, s):
        return (self.lift().differential() - cup(s, self, integer=True).scale(2)).reduce(self.modulus)


@lru_cache(None)
def node(degree, modulus, operation, *arguments):
    return Cochain(degree, modulus, operation, tuple(arguments))


def field(name, degree, modulus=2):
    return node(degree, modulus, "field", name)


def zero(degree, modulus=2):
    return node(degree, modulus, "zero")


def word(labels, *inputs, integer=False):
    labels = tuple(map(int, labels)) if isinstance(labels, str) else tuple(labels)
    degree = sum(x.degree for x in inputs) - len(labels) + len(inputs)
    return node(degree, None if integer else 2, "word", labels, tuple(inputs))


def cup(a, b, i=0, integer=False):
    if i < 0:
        return zero(a.degree + b.degree - i, None if integer else 2)
    return word(tuple(1 + j % 2 for j in range(i + 2)), a, b, integer=integer)


def square(a, k):
    return cup(a, a, a.degree - k) + cup(a, a.differential(), a.degree - k + 1)


def phase(*terms):
    coefficient, cochain = terms[0]
    result = cochain.lift().scale(coefficient)
    for coefficient, cochain in terms[1:]:
        result = result + cochain.lift().scale(coefficient)
    return result.reduce(8)


def evaluate(expression: Cochain, fields: Mapping[str, Callable | Mapping], face=None):
    """Evaluate on simplex faces; missing dictionary entries are an error."""
    if face is None:
        face = tuple(range(expression.degree + 1))

    @lru_cache(None)
    def visit(x, f):
        if len(f) != x.degree + 1:
            raise ValueError((x.degree, f))
        if len(set(f)) != len(f):
            return 0
        op, args = x.operation, x.arguments
        if op == "zero":
            value = 0
        elif op == "field":
            fn = fields[args[0]]
            value = fn(f) if callable(fn) else fn[f]
        elif op == "add":
            value = visit(args[0], f) + visit(args[1], f)
        elif op == "scale":
            value = args[1] * visit(args[0], f)
        elif op == "reduce":
            value = visit(args[0], f)
        elif op == "divide":
            value, remainder = divmod(visit(args[0], f), args[1])
            if remainder:
                raise ArithmeticError(("nonintegral quotient", args[1], f))
        elif op == "d":
            value = sum((-1) ** i * visit(args[0], f[:i] + f[i+1:]) for i in range(len(f)))
        elif op == "word":
            labels, inputs = args
            value = 0
            for local_faces, sign in cuts(labels, tuple(a.degree for a in inputs)):
                term = sign if x.modulus is None else 1
                for a, local in zip(inputs, local_faces):
                    term *= visit(a, tuple(f[j] for j in local))
                value += term
        else:
            raise ValueError(op)
        return value % x.modulus if x.modulus is not None else value

    return visit(expression, tuple(face))


def majorana_source(a, w, s):
    return square(a, 2) + w*a + s*a.beta().reduce()


def majorana_product(a, b, s):
    return cup(a, b, a.degree - 1) + s*cup(a, b, a.degree)


def gamma(a, w, s):
    p, P = a.degree, a.beta()
    r = P.reduce()
    if p == 1:
        h = word('123134', w,w,a,a) + cup(w*a,s*r,2) + cup(w,s,1)*r + s*(s+a)*r
        return phase((4,h),(2,cup(w,P,integer=True)),(2,cup(s,cup(a,P,integer=True),integer=True)))
    if p != 2:
        raise ValueError("Majorana phase supplied only in degrees one and two")
    x = zero(5)
    for label in ('1213243','1213431','1232141','1234321'):
        x = x + word(label,a,a,a,a)
    q, W, R = a*a, w*a, s*r
    h = word('1231343',w,w,a,a) + x + cup(q,W,3) + cup(q,R,3) + cup(W,R,3)
    h = h + word('1231434',s,s,r,r) + cup(w,s,1)*r + s*q
    carry = (P+r.lift()).divide(2).reduce()
    h = h+s*s*carry
    return phase((4,h),(2,cup(w,P,integer=True)),(2,cup(P,P,1,integer=True)))


def obstruction(a, c, w, s):
    """CA-coordinate O4 or O5, integer numerator modulo eight."""
    return (phase((4,square(c,2)+w*c)) + gamma(a,w,s)).reduce(8)


def _gw(a,c,b,cp,w,s):
    return phase((4,cup(c,cp,a.degree)+cup(c.differential(),cp,a.degree+1)
                      +cup(c+cp,majorana_product(a,b,s),a.degree)))


def _h4(a):
    return phase((2,cup(a,a.beta(),1,integer=True)),(1,cup(a,a,integer=True)))


def _j4(a,s):
    P=a.beta()
    return phase((4,s*(P+P.reduce().lift()).divide(2).reduce()))


def stacking(a,c,b,cp,w,s):
    """Manuscript U3/U4, same CA coordinate as obstruction()."""
    p=a.degree
    N=a+b; P=a.beta(); Q=b.beta()
    u=cup(a,b,p); S=cup(a,b,p,integer=True); T=S.differential()
    if p == 1:
        beta=phase((2,cup(P,Q,1,integer=True)),(-2,cup(P+Q,S,integer=True)),
                   (-2,cup(S,P+Q,integer=True)),(2,cup(S,T,integer=True)))
        y=phase((4,cup(a,a*b,1)*b))-phase((1,N*N*N))+phase((1,a*a*a))+phase((1,b*b*b))
        lw=phase((4,cup(w*N,a*b,2)),(-2,cup(w,S,integer=True)))
        ea,eb,eu=cup(s,a,1),cup(s,b,1),cup(s,u,1)
        ls=s*(ea+eb+eu)*u+ea*u*N+(ea*a+a*eb+s*a+a*s)*u+s*(u*a+a*b+b*u)
        pure_s=phase((4,ls),(2,s*a*b))
        mixed=phase((4,cup(w,s,1)*u+cup(w*N,s*u,2)+cup(w*b,s*a*a,3)))
    elif p == 2:
        r,rp=P.reduce(),Q.reduce(); t,tb=cup(a,b,1),cup(b,a,1);v=s*u
        beta=phase((-2,cup(P,Q,2,integer=True)),(2,cup(P+Q,S,1,integer=True)),
                   (-2,cup(S,P+Q,1,integer=True)),(2,cup(S,T,1,integer=True)),(2,cup(S,S,integer=True)))
        z=zero(4); inputs={'a':a,'b':b}
        for label,names in [('12413423','aaab'),('12314132','aabb'),('12314324','aabb'),
                            ('12341321','aabb'),('12132413','abbb'),('12324214','abbb')]:
            z=z+word(label,*(inputs[x] for x in names))
        y=phase((4,z),(2,a*b))+_h4(N)-_h4(a)-_h4(b)
        lw=phase((4,cup(w*N,t,3)+cup(b*b,w*a,4)+cup(a*b+b*a,w*N,4)),(-2,cup(w,S,integer=True)))
        mixed=phase((4,cup(s,w*u,1)+w*cup(s,u,1)+cup(w*a,v,3)+cup(w*b,s*r,4)+cup(w*b,v,3)))
        ls=(s*cup(rp,v,3)+s*cup(a,cup(b,v,2),2)+s*cup(r,v,3)+cup(t,s*rp,3)
            +cup(b*b,v,3)+s*cup(r,rp,3)+cup(b*a,s*t,4)+cup(t,v,2)+cup(b*a,s*tb,4)
            +cup(b*b,s*r,4)+s*cup(a,cup(b,t,2),2)+cup(v,b*a,3)+cup(a*b,v,3)
            +cup(a*a,v,3)+cup(t,s*r,3)+s*cup(b,v,2)+s*cup(a,v,2)+s*cup(b,t,2)
            +s*cup(a,t,2)+s*s*u)
        BT=phase((2,cup(s,cup(a,b,1,integer=True),integer=True)),(4,s*(cup(a+b,u,1)+cup(b,r,2))))
        pure_s=phase((4,s*t+ls))+BT+_j4(N,s)-_j4(a,s)-_j4(b,s)
    else:
        raise ValueError("Stacking formulas supplied only for p=1,2")
    return (_gw(a,c,b,cp,w,s)+beta+y+lw+pure_s+mixed).reduce(8)


def pip_majorana(n,w,s):
    a=n.reduce()
    return square(a,2)+w*a+s*square(a,1)


def pip_parity(n,b,w,s):
    """Native p+ip d3 source; n is an INTEGER cocycle, b need not be closed."""
    p=n.degree; a=n.reduce();h=(n-a.lift()).divide(2).reduce()
    t=cup(a,a,p-1);W=w+s*s;bp=b+s*h;q=cup(a,a,p-2);v=cup(W,W,1)
    zeta=lambda x,y:word('12313'+''.join(str(4 if j%2==0 else 3) for j in range(y.degree)),x,x,y,y)
    out=square(bp,2)+w*bp+s*square(bp,1)+zeta(W,a)+(v+s*W)*h+(cup(v,s,1)+s*cup(s,W,1))*a
    if p==1:
        return out
    if p==2:
        return (out+zeta(a,a)+cup(q,W*a,3)+h*h.differential()+cup(t,s*a,1)
                +s*(cup(q,W*a,4)+cup(a,s,1)*a+cup(a,t,1)+q))
    raise ValueError("Native p+ip sources supplied only for p=1,2")


@lru_cache(None)
def formula(name, p):
    w,s=field('w',2),field('s',1)
    a,b,c,cp=field('a',p),field('b',p),field('c',p+1),field('cp',p+1)
    if name=='majorana_source':return majorana_source(a,w,s)
    if name=='majorana_product':return majorana_product(a,b,s)
    if name=='obstruction':return obstruction(a,c,w,s)
    if name=='stacking':return stacking(a,c,b,cp,w,s)
    if name=='pip_majorana':return pip_majorana(field('n',p,None),w,s)
    if name=='pip_parity':return pip_parity(field('n',p,None),field('b',p+1),w,s)
    raise ValueError(name)


def evaluate_bar(name,p,arguments,*,identity,multiply,fields):
    """Convert normalized inhomogeneous cochains to ordered simplex faces."""
    products={}
    for i in range(len(arguments)+1):
        value=identity
        for j in range(i+1,len(arguments)+1):
            value=multiply(value,arguments[j-1]);products[i,j]=value
    def adapt(fn):
        def value(face):
            increments=tuple(products[i,j] for i,j in zip(face,face[1:]))
            return 0 if any(g==identity for g in increments) else fn(*increments)
        return value
    e=formula(name,p)
    numerator=evaluate(e,{key:adapt(value) for key,value in fields.items()})
    return Fraction(numerator,8) if name in ('obstruction','stacking') else numerator


# Exact unary CF-coordinate comparison on the torsion sector n=k*s, omega=0.
# See tests/derive_pip_coordinate.py for exhaustive derivation and normalization.
PIP_CF_COORDINATE_ANF=((),(16,24,40,48),(5,7,9,10,14,15,17,23,33,39),
                       (5,7,9,10,14,15,16,17,23,24,33,39,40,48))


def pip_cf_coordinate(multiple,b,s,face=(0,1,2,3)):
    """Lambda: d Lambda = native d3 + collaborator d3 for n=multiple*s.

    Binary B obeys dB=(multiple mod2)*s^3. Both field arguments take faces.
    This is a verified CF-coordinate dictionary, not a choice of upper product.
    """
    get=lambda fn,f:fn(f) if callable(fn) else fn[f]
    x=[get(s,(face[0],face[i])) for i in (1,2,3)]
    x += [get(b,(face[0],face[i],face[j])) for i,j in ((1,2),(1,3),(2,3))]
    active=sum((v%2)<<i for i,v in enumerate(x))
    return sum((active&mask)==mask for mask in PIP_CF_COORDINATE_ANF[multiple%4])%2
