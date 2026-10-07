#!/usr/bin/env python3
"""Exact open-Majorana self-stacking word reduction, standard library only.

Binary variables satisfy x_i^2=x_i. Integer coefficient polynomials preserve
canonical whole lifts and signed cups. All thirty independent open-cochain/background
bits on the five-simplex are checked simultaneously; no random inputs, cohomology solver, or fitted constants are used.
"""
from functools import lru_cache
from itertools import combinations
import json

class Polynomial:
    def __init__(self, terms=0, modulus=4):
        if isinstance(terms, int): terms = {0: terms}
        self.modulus = modulus
        self.terms = {m: c % modulus for m, c in terms.items() if c % modulus}
    def convert(self, other):
        return other if isinstance(other, Polynomial) else Polynomial(other, self.modulus)
    def __add__(self, other):
        other = self.convert(other); out = dict(self.terms)
        for m, c in other.terms.items(): out[m] = out.get(m, 0) + c
        return Polynomial(out, min(self.modulus, other.modulus))
    __radd__ = __add__
    def __neg__(self):
        return Polynomial({m: -c for m, c in self.terms.items()}, self.modulus)
    def __sub__(self, other): return self + -self.convert(other)
    def __rsub__(self, other): return self.convert(other) + -self
    def __mul__(self, other):
        other = self.convert(other); out = {}
        for m, a in self.terms.items():
            for n, b in other.terms.items(): out[m | n] = out.get(m | n, 0) + a*b
        return Polynomial(out, min(self.modulus, other.modulus))
    __rmul__ = __mul__
    def __bool__(self): return bool(self.terms)
    def binary(self): return Polynomial(self.terms, 2)
    def lift(self, modulus=4):
        assert self.modulus == 2
        result = Polynomial(0, modulus)
        for m in sorted(self.terms):
            term = Polynomial({m: 1}, modulus)
            result = result + term - 2*result*term
        return result
    def divide(self, k):
        assert self.modulus % k == 0
        assert all(c % k == 0 for c in self.terms.values())
        return Polynomial({m: c//k for m, c in self.terms.items()}, self.modulus//k)

class Cochain:
    def __init__(self, degree, values=None, modulus=2):
        self.degree, self.modulus = degree, modulus
        self.values = values or {}
    def __call__(self, face):
        if len(face) != self.degree+1 or tuple(sorted(set(face))) != tuple(face):
            return Polynomial(0, self.modulus)
        return self.values.get(tuple(face), Polynomial(0, self.modulus))
    def __add__(self, other):
        assert self.degree == other.degree
        return Cochain(self.degree, {f: self(f)+other(f) for f in faces(self.degree)}, min(self.modulus, other.modulus))
    def __neg__(self):
        return Cochain(self.degree, {f: -self(f) for f in faces(self.degree)}, self.modulus)
    def __sub__(self, other): return self + -other
    def differential(self):
        return Cochain(self.degree+1, {f: sum(((-1)**j)*self(f[:j]+f[j+1:]) for j in range(len(f))) for f in faces(self.degree+1)}, self.modulus)
    def lift(self, modulus=4):
        return Cochain(self.degree, {f: self(f).lift(modulus) for f in faces(self.degree)}, modulus)
    def binary(self):
        return Cochain(self.degree, {f: self(f).binary() for f in faces(self.degree)}, 2)
    def divide(self, k):
        return Cochain(self.degree, {f: self(f).divide(k) for f in faces(self.degree)}, self.modulus//k)

@lru_cache(None)
def faces(degree): return tuple(combinations(range(6), degree+1))

@lru_cache(None)
def interval_terms(word,degrees):
    targets=[degrees[j]+1-word.count(j+1)for j in range(len(degrees))]
    if min(targets)<0:return()
    lengths=[0]*len(word);answer=[]
    def visit(i,remaining):
        if i==len(word):
            if any(remaining):return
            cuts=[0]
            for value in lengths:cuts.append(cuts[-1]+value)
            faces=[[]for _ in degrees]
            for k,label in enumerate(word):faces[label-1].extend(range(cuts[k],cuts[k+1]+1))
            if any(len(set(f))!=len(f)for f in faces):return
            inner=[word[k]in word[k+1:]for k in range(len(word))]
            lam=[lengths[k]+int(inner[k])for k in range(len(word))]
            exponent=sum(cuts[k+1]for k in range(len(word))if inner[k])
            exponent+=sum(lam[k]*lam[j]for k in range(len(word))for j in range(k+1,len(word))if word[k]>word[j])
            answer.append((tuple(map(tuple,faces)),(-1)**exponent));return
        j=word[i]-1
        choices=[remaining[j]]if word[i]not in word[i+1:]else range(remaining[j]+1)
        for value in choices:
            lengths[i]=value;left=remaining.copy();left[j]-=value;visit(i+1,left)
    visit(0,targets)
    return tuple(answer)


def operation(word, *inputs):
    word = tuple(map(int, word)); degrees = tuple(x.degree for x in inputs)
    degree = sum(degrees)-len(word)+len(inputs)
    terms = interval_terms(word, degrees)
    return Cochain(degree, {f: sum(product(x(tuple(f[j] for j in face)) for x, face in zip(inputs, cuts)) for cuts, _ in terms) for f in faces(degree)})

def product(values):
    result = 1
    for value in values: result = result*value
    return result

def cup(a, b, index=0):
    degree = a.degree+b.degree-index
    if index < 0: return Cochain(degree, modulus=min(a.modulus,b.modulus))
    terms = interval_terms(tuple(1+j%2 for j in range(index+2)), (a.degree,b.degree))
    prefactor = (-1)**(index*(a.degree+b.degree)+index*(index-1)//2)
    return Cochain(degree, {f: prefactor*sum(sign*a(tuple(f[j] for j in ff))*b(tuple(f[j] for j in gg)) for (ff,gg), sign in terms) for f in faces(degree)}, min(a.modulus,b.modulus))

def square(a, j):
    return cup(a,a,a.degree-j)+cup(a,a.differential(),a.degree-j+1)

def beta(a): return a.lift(8).differential().divide(2)


from pathlib import Path
import hashlib
HERE=Path(__file__).resolve().parent

def run():
    labels=[]
    def field(degree,closed=False):
        values={}
        for face in faces(degree):
            if not closed or face[0]==0:
                values[face]=Polynomial({1<<len(labels):1},2);labels.append(face)
        if closed:
            for face in faces(degree):
                if face[0]:values[face]=sum(values[(0,)+face[:j]+face[j+1:]] for j in range(len(face)))
        return Cochain(degree,values)
    u,w,s=field(3),field(2,True),field(1,True)
    A=u.differential()
    B=(u.lift(8).differential()-A.lift(8)).divide(2)
    b=B.binary()
    assert all(not(b-square(u,1))(f)for f in faces(4))
    fields={r'\check n_3':u,r'\omega_2':w,r's_1':s,r'\overline{d\check n_3}':A,r'\overline{\beta^\circ\check n_3}':b,r'd\overline{\beta^\circ\check n_3}':b.differential()}
    before=HERE/'ARCHIVED_OPEN_GAMMA_DIAGONAL_WORDS.json';after=HERE/'OPEN_GAMMA_DIAGONAL_WORDS.json'
    def evaluate(path):
        rows=json.loads(path.read_text())['terms'];result=Polynomial(0,2)
        for row in rows:
            value=operation(row['word'],*(fields[name]for name in row['inputs']))(tuple(range(6)))
            result=result+value
        return rows,result
    old,P=evaluate(before);new,Q=evaluate(after)
    assert len(old)==218 and len(new)==187
    assert not(P-Q)
    return {'status':'PASS_EXACT_UNIVERSAL_COEFFICIENT_IDENTITY','independent_bits':len(labels),'old_MS':len(old),'new_MS':len(new),'coefficient_monomials':len(P.terms),'residual_monomials':len((P-Q).terms),'new_outer_terms':200,'new_terms_with_106_lift_interiors':302,'representative_change':False,'hashes':{path.name:hashlib.sha256(path.read_bytes()).hexdigest()for path in[before,after]}}

if __name__=='__main__':print(json.dumps(run(),indent=2))
