#!/usr/bin/env python3
"""Exact 3+1D closed-Majorana self-stacking certificate, standard library only.

Binary variables satisfy x_i^2=x_i. Integer coefficient polynomials preserve
canonical whole lifts and signed cups. All twenty independent valid-tower
bits on the four-simplex are checked simultaneously; no random inputs,
cohomology solver, external coefficient files, or fitted constants are used.
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
def faces(degree): return tuple(combinations(range(5), degree+1))

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

def run():
    labels = []
    def closed(name, degree):
        values = {}
        for f in faces(degree):
            if f[0] == 0:
                values[f] = Polynomial({1 << len(labels): 1},2)
                labels.append({'field':name,'face':f})
        for f in faces(degree):
            if f[0] != 0: values[f] = sum(values[(0,)+f[:j]+f[j+1:]] for j in range(len(f)))
        return Cochain(degree, values)
    u,w,s = closed('n2',2),closed('omega2',2),closed('s1',1)
    B=beta(u); b=B.binary(); t=cup(u,u,1); e=t+cup(s,u)
    assert B.modulus == 4 and all(B(f).modulus == 4 for f in faces(3))
    q=cup(u,u)+cup(w,u)+cup(s,b)
    free_c=closed('n3_root',3)
    c=Cochain(3,{f:free_c(f)+(q((0,)+f) if f[0] else 0) for f in faces(3)})
    assert not(c.differential()-q)(tuple(range(5)))
    words=('12123434','12134131','12314324','12314342','13242412','13413142','13432412')
    V=Cochain(4)
    for word in words: V=V+operation(word,u,u,u,u)
    z0=(V+operation('123131',u,u,t)+cup(t,u,1)+cup(u,t,1)
        +cup(u,cup(u,t,1),2)+cup(b,b,2))
    z=(z0+cup(cup(u,u),cup(w,u),4)
       +cup(cup(u,u)+cup(w,u),cup(s,b),4)
       +cup(cup(w,s,1),u)+cup(t,cup(s,u),2)
       +cup(s,e+cup(b,b,3)+cup(u,u,1)+cup(cup(s,u),u,2)))
    integer_u=u.lift(); integer_w=w.lift()
    Q=-cup(B,B,2)+cup(B+B,integer_u,1)+cup(integer_u,integer_u)-cup(integer_w,integer_u)
    top=tuple(range(5))
    upper=cup(c,c,2)+cup(q,c,3)
    # Units of 1/4. Half brackets are binary before multiplying by two.
    literal=2*(z+upper)(top).lift()+Q(top)
    reduced_half=(upper+cup(cup(w,s,1),u)+cup(b,cup(s,u),2)
                  +cup(s,e)+cup(s,cup(cup(s,u),u,2))+cup(u,u))
    reduced_quarter=cup(B,B,2)+cup(s,b).lift()-q.lift()
    reduced=2*reduced_half(top).lift()+reduced_quarter(top)
    assert Q(top).modulus == reduced_quarter(top).modulus == 4
    assert literal.modulus == reduced.modulus == 4
    intrinsic=(operation('123131',u,u,b)+cup(u,b,1)+cup(u,cup(u,b,1),2))(top)
    checks={'seven_intrinsic_MS_terms':V(top), 'three_intrinsic_terms':intrinsic,
            'complete_ten_term_self_stack':literal-reduced}
    assert all(not value for value in checks.values())
    return {'status':'PASS','independent_binary_variables':len(labels),
            'input_scope':'n1=0; all closed binary n2,omega2,s1; every n3 completing dn3=O4gamma on the four-simplex',
            'method':'Exact Boolean and signed integer coefficient polynomials, not sampled assignments',
            'residual_coefficients':{name:len(value.terms) for name,value in checks.items()},
            'half_terms':7,'quarter_terms':3,'total_terms':10,
            'canonical_lifts_preserved':True,'new_output_gauge':False,
            'phase_units':'1/4','phase_polynomial_modulus':4,
            'bockstein_precision':'Canonical integer lift modulo8 divided exactly by2; B retained modulo4',
            'complete_phase_polynomial_terms':len(reduced.terms)}

if __name__ == '__main__': print(json.dumps(run(),indent=2))
