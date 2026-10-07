#!/usr/bin/env python3
"""Exact general3D CF exchange reduction, standard library only.

Binary variables satisfy x_i^2=x_i. Integer coefficient polynomials preserve
canonical whole lifts and signed cups. All50 independent open-cochain/background
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


WORDS = [('1212312', ('du', 'c', 'v')), ('1213121', ('du', 'c', 'v')), ('121314134', ('dv', 's', 'c', 'u')), ('121314134', ('dv', 's', 'cp', 'u')), ('1213231', ('du', 'c', 'v')), ('1213231', ('u', 'c', 'dv')), ('121341314', ('du', 's', 'v', 'c')), ('121341314', ('du', 's', 'v', 'cp')), ('121341314', ('c', 's', 'du', 'v')), ('121341314', ('cp', 's', 'du', 'v')), ('121342434', ('s', 'c', 'du', 'v')), ('121342434', ('s', 'c', 'u', 'dv')), ('121342434', ('s', 'cp', 'du', 'v')), ('121342434', ('s', 'cp', 'u', 'dv')), ('121343134', ('dv', 's', 'c', 'u')), ('121343134', ('dv', 's', 'cp', 'u')), ('121343134', ('c', 's', 'du', 'v')), ('121343134', ('cp', 's', 'du', 'v')), ('121343413', ('du', 's', 'c', 'v')), ('121343413', ('du', 's', 'cp', 'u')), ('121343413', ('du', 's', 'cp', 'v')), ('121343413', ('dv', 's', 'c', 'u')), ('121343413', ('dv', 's', 'c', 'v')), ('121343413', ('dv', 's', 'cp', 'u')), ('121343424', ('s', 'c', 'u', 'dv')), ('121343424', ('s', 'cp', 'u', 'dv')), ('1231212', ('du', 'c', 'v')), ('1231212', ('du', 'cp', 'v')), ('123121412', ('du', 'c', 's', 'v')), ('123121412', ('du', 'cp', 's', 'v')), ('123121412', ('dv', 'c', 's', 'u')), ('123121412', ('dv', 'cp', 's', 'u')), ('123124121', ('du', 'cp', 's', 'u')), ('123124121', ('dv', 'c', 's', 'v')), ('123124134', ('c', 's', 'v', 'du')), ('123124134', ('cp', 's', 'v', 'du')), ('123124142', ('du', 'c', 's', 'v')), ('123124142', ('du', 'cp', 's', 'v')), ('123124142', ('dv', 'c', 's', 'u')), ('123124142', ('dv', 'cp', 's', 'u')), ('123124143', ('du', 's', 'v', 'c')), ('123124143', ('du', 's', 'v', 'cp')), ('123124143', ('c', 's', 'v', 'du')), ('123124143', ('cp', 's', 'v', 'du')), ('123124214', ('dv', 'c', 's', 'u')), ('123124214', ('dv', 'cp', 's', 'u')), ('123124241', ('dv', 'c', 's', 'u')), ('123124241', ('dv', 'cp', 's', 'u')), ('1231321', ('c', 'du', 'v')), ('1231321', ('c', 'u', 'dv')), ('123141214', ('du', 'c', 's', 'v')), ('123141214', ('du', 'cp', 's', 'v')), ('123141214', ('c', 'v', 's', 'du')), ('123141214', ('cp', 'v', 's', 'du')), ('123141314', ('du', 's', 'c', 'v')), ('123141314', ('du', 's', 'cp', 'v')), ('123141314', ('c', 's', 'du', 'v')), ('123141314', ('c', 's', 'dv', 'u')), ('123141314', ('cp', 's', 'du', 'v')), ('123141314', ('cp', 's', 'dv', 'u')), ('123142124', ('du', 'c', 's', 'v')), ('123142124', ('du', 'cp', 's', 'v')), ('123142141', ('du', 'c', 's', 'v')), ('123142141', ('du', 'cp', 's', 'v')), ('123142141', ('du', 'v', 's', 'c')), ('123142141', ('du', 'v', 's', 'cp')), ('123142142', ('c', 'v', 's', 'du')), ('123142142', ('cp', 'v', 's', 'du')), ('123142414', ('du', 'v', 's', 'c')), ('123142414', ('du', 'v', 's', 'cp')), ('1232131', ('du', 'v', 'c')), ('1232131', ('du', 'v', 'cp')), ('1232131', ('u', 'dv', 'c')), ('1232131', ('u', 'dv', 'cp')), ('123214142', ('du', 'c', 's', 'v')), ('123214142', ('du', 'cp', 's', 'u')), ('123214142', ('du', 'cp', 's', 'v')), ('123214142', ('dv', 'c', 's', 'u')), ('123214142', ('dv', 'c', 's', 'v')), ('123214142', ('dv', 'cp', 's', 'u')), ('1232312', ('du', 'cp', 'v')), ('1232312', ('u', 'cp', 'dv')), ('1232321', ('u', 'dv', 'c')), ('1232321', ('u', 'dv', 'cp')), ('123241214', ('dv', 'c', 's', 'u')), ('123241214', ('dv', 'cp', 's', 'u')), ('123241241', ('dv', 'c', 's', 'u')), ('123241241', ('dv', 'cp', 's', 'u')), ('123241413', ('du', 's', 'v', 'c')), ('123241413', ('du', 's', 'v', 'cp')), ('123241421', ('du', 'cp', 's', 'u')), ('123241421', ('dv', 'c', 's', 'v')), ('123242324', ('s', 'du', 'c', 'v')), ('123242324', ('s', 'du', 'cp', 'v')), ('123243141', ('du', 's', 'v', 'c')), ('123243141', ('du', 's', 'v', 'cp')), ('123413134', ('du', 's', 'c', 'v')), ('123413134', ('du', 's', 'cp', 'v')), ('123413134', ('dv', 's', 'c', 'u')), ('123413134', ('dv', 's', 'cp', 'u')), ('123413143', ('du', 's', 'c', 'v')), ('123413143', ('du', 's', 'cp', 'v')), ('123413413', ('du', 's', 'cp', 'u')), ('123413413', ('du', 's', 'v', 'c')), ('123413413', ('du', 's', 'v', 'cp')), ('123413413', ('dv', 's', 'c', 'u')), ('123413413', ('dv', 's', 'c', 'v')), ('123413413', ('dv', 's', 'cp', 'u')), ('123413413', ('c', 's', 'dv', 'u')), ('123413413', ('c', 's', 'dv', 'v')), ('123413413', ('cp', 's', 'du', 'u')), ('123413413', ('cp', 's', 'dv', 'u')), ('123413413', ('v', 's', 'du', 'c')), ('123413413', ('v', 's', 'du', 'cp')), ('123413431', ('du', 's', 'c', 'v')), ('123413431', ('du', 's', 'cp', 'u')), ('123413431', ('du', 's', 'cp', 'v')), ('123413431', ('dv', 's', 'c', 'v')), ('123413431', ('c', 's', 'du', 'v')), ('123413431', ('c', 's', 'dv', 'v')), ('123413431', ('cp', 's', 'du', 'u')), ('123413431', ('cp', 's', 'du', 'v')), ('123421241', ('du', 'c', 's', 'v')), ('123421241', ('du', 'cp', 's', 'v')), ('123431431', ('du', 's', 'c', 'v')), ('123431431', ('du', 's', 'cp', 'v')), ('123432343', ('s', 'u', 'dv', 'c')), ('123432343', ('s', 'u', 'dv', 'cp')), ('123432423', ('s', 'du', 'v', 'c')), ('123432423', ('s', 'du', 'v', 'cp')), ('123432423', ('s', 'u', 'dv', 'c')), ('123432423', ('s', 'u', 'dv', 'cp'))]


def run():
    labels=[]
    def field(name,degree,closed=False):
        vals={}
        for f in faces(degree):
            if not closed or not f[0]:
                vals[f]=Polynomial({1<<len(labels):1},2);labels.append((name,f))
        if closed:
            for f in faces(degree):
                if f[0]:vals[f]=sum(vals[(0,)+f[:j]+f[j+1:]]for j in range(len(f)))
        return Cochain(degree,vals)
    u,v,c,cp,s=field('check_n2',2),field('check_n2_prime',2),field('n3',3),field('n3_prime',3),field('s1',1,True)
    w,t=field('omega2',2,True),field('lower_stacking_carry',2)
    A,B=u.differential(),v.differential();values=dict(u=u,v=v,c=c,cp=cp,s=s,du=A,dv=B)
    old=sum((operation(word,*(values[x]for x in names))for word,names in WORDS),Cochain(4))
    f=(0,1,2,3,4);i,j,k,l,m=f
    left=(v((i,j,k))*A((i,k,l,m))+u((i,l,m))*B((i,j,k,l))
      +v((j,k,l))*A((i,j,l,m))+u((i,j,m))*B((j,k,l,m))+v((k,l,m))*A((i,j,k,m))
      +s((i,j))*(v((j,k,m))*A((j,k,l,m))+(u((j,k,l))+v((j,k,l)))*B((j,k,l,m))))
    right=(v((i,j,k))*A((i,k,l,m))+u((i,l,m))*B((i,j,k,l))
      +s((i,j))*((u((j,k,l))+v((j,k,m)))*A((j,k,l,m))+u((j,k,l))*B((j,k,l,m))))
    new=c.differential()(f)*left+cp.differential()(f)*right
    residual=old(f)-new
    assert not residual
    def P4(x,z):
        terms=[('121231',(z,w,x)),('121323',(w,z,x)),('12134243',(s,z,x,x)),('12134323',(s,z,x,x)),('123131',(z,w,x)),('12313431',(z,s,x,x)),('12341431',(z,s,x,x)),('12342432',(s,z,x,x))]
        return sum((operation(word,*args)for word,args in terms),Cochain(4))
    def parity(x):return cup(x,x)+cup(w,x)+cup(s,cup(x,x,1))
    p4_old=P4(u,c)
    p4_new=cup(c.differential(),parity(u)+cup(u,u),4)
    p4_res=p4_old(f)-p4_new(f)
    z=c+cp;N=u+v+t;plain=u+v
    pair_old=P4(N,z)+P4(plain,z)
    pair_new=cup(z.differential(),parity(N)+parity(plain)+cup(N,N)+cup(plain,plain),4)
    pair_res=pair_old(f)-pair_new(f)
    full_res=old(f)+pair_old(f)-new-pair_new(f)
    assert not p4_res and not pair_res and not full_res
    return {'status':'PASS','input_MS_terms':len(WORDS),'output_explicit_face_terms':13,
            'independent_binary_variables':len(labels),'collected_scalar_coefficients':len(new.terms),
            'residual_coefficients':len(residual.terms),'P4_single_residual':len(p4_res.terms),'P4_actual_output_pair_residual':len(pair_res.terms),'combined_general_cpsi_residual':len(full_res.terms),'new_complete_cpsi_term_count':29,'scope':'Arbitrary binary degree2 inputs and degree3 completions; closed sign background. The current lower equations identify the original W*bar(n1) arguments with dcheck(n2).',
            'source_change':False,'output_gauge':False,'phase_coefficient':'1/2','method':'Exact normalized-MS and physical-face coefficient polynomials; no sampled cases or fit'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
