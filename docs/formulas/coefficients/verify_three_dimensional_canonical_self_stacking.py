#!/usr/bin/env python3
"""Exact canonical p+ip self-stacking certificate, standard library only.

Binary variables satisfy x_i^2=x_i. Integer coefficient polynomials preserve
canonical whole lifts and signed cups. All twenty independent valid-tower
bits on the four-simplex are checked simultaneously; no random inputs,
cohomology solver or fitted constants are used. Explicit physical coefficient
sets and the frozen whole-phase reference are read from the adjacent JSON.
"""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

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


def scaled(a,k):
    return Cochain(a.degree,{f:k*a(f) for f in faces(a.degree)},a.modulus)

def ds(a,s): return a.differential()-scaled(cup(s.lift(16),a),2)

def beta_open(a):
    d=a.lift(16).differential()
    return (d-d.binary().lift(16)).divide(2)

def signed_cup(a,b,index,s,twists):
    degree=a.degree+b.degree-index
    terms=interval_terms(tuple(1+j%2 for j in range(index+2)),(a.degree,b.degree))
    prefactor=(-1)**(index*(a.degree+b.degree)+index*(index-1)//2)
    def value(f):
        out=Polynomial(0,min(a.modulus,b.modulus))
        for (ff,gg),sign in terms:
            z=sign*a(tuple(f[j]for j in ff))*b(tuple(f[j]for j in gg))
            for twist,idx in zip(twists,(ff[0],gg[0])):
                if twist and idx:z=z*(1-2*s((f[0],f[idx])).lift(16))
            out=out+z
        return prefactor*out
    return Cochain(degree,{f:value(f)for f in faces(degree)},min(a.modulus,b.modulus))

def verify_open_exchange_identities():
    labels=[]
    def free(name,degree):
        values={}
        for f in faces(degree):
            values[f]=Polynomial({1<<len(labels):1},2);labels.append((name,f))
        return Cochain(degree,values)
    u,c=free('Majorana',2),free('complex_fermion',3)
    A=u.differential();top=tuple(range(5))
    intrinsic_words=('12123434','12134131','12314324','12314342','13242412','13413142','13432412')
    V=sum((operation(word,u,u,u,u)for word in intrinsic_words),Cochain(4))
    smallV=u((0,1,2))*u((1,2,3))*u((2,3,4))*A((0,1,3,4))
    words=[('1212312',(A,c,u)),('1213121',(A,c,u)),('1213231',(A,c,u)),('1213231',(u,c,A)),
           ('1231321',(c,A,u)),('1231321',(c,u,A)),('1232312',(A,c,u)),('1232312',(u,c,A))]
    M=sum((operation(word,*args)for word,args in words),Cochain(4))
    smallM=c.differential()(top)*(u((1,2,3))*A((0,1,3,4))+u((0,1,4))*A((1,2,3,4))+u((2,3,4))*A((0,1,2,4)))
    residuals={'seven_Majorana_MS_to_one_face':len((V(top)-smallV).terms),'eight_remaining_CF_MS_to_three_faces':len((M(top)-smallM).terms)}
    assert not any(residuals.values())
    return {'independent_free_cochain_bits':len(labels),'residual_coefficients':residuals,'lower_equations_imposed':False}

def run():
    data=json.loads(Path(__file__).with_name('three_dimensional_canonical_self_stacking.json').read_text())
    labels=[]
    def closed(name,degree):
        v={}
        for f in faces(degree):
            if f[0]==0:
                v[f]=Polynomial({1<<len(labels):1},2);labels.append({'field':name,'face':list(f)})
        for f in faces(degree):
            if f[0]:v[f]=sum(v[(0,)+f[:j]+f[j+1:]]for j in range(len(f)))
        return Cochain(degree,v)
    s,w=closed('s',1),closed('w',2);W=w+cup(s,s);A=cup(W,s)
    free_u=closed('u_root',2)
    u=Cochain(2,{f:free_u(f)+(A((0,)+f)if f[0]else 0)for f in faces(2)})
    def kappa(x):return square(x,2)+cup(s,square(x,1))+cup(w,x)
    psi=Cochain(4,{f:W(f[:3])*W((f[0],f[2],f[3]))*s(f[2:4])*s(f[3:5])for f in faces(4)})
    psi=psi+cup(cup(cup(W,W,1),s,1)+cup(s,cup(s,W,1)),s)
    q=kappa(u)+psi
    free_c=closed('c_root',3)
    c=Cochain(3,{f:free_c(f)+(q((0,)+f)if f[0]else 0)for f in faces(3)})
    assert labels==data['variables']
    top=tuple(range(5));du=u.differential();dc=c.differential()
    assert not(du-A)((0,1,2,3)) and not(dc-q)(top)
    t=cup(u,u,1);t2=cup(s,s);N3=square(u,1)+du+cup(s,u)
    outpsi=cup(cup(W,W,1)+cup(s,W),s)
    assert not(N3.differential()+kappa(t2)+outpsi)(top)
    Bgamma=beta_open(u);b=Bgamma.binary()
    integer_u=u.lift(16);integer_w=w.lift(16);integer_W=W.lift(16);n=s.lift(16)
    alpha=ds(integer_W,s).divide(2)
    Bpsi=(A.lift(16)+signed_cup(integer_W,n,0,s,(1,1))).divide(2);B=Bgamma+Bpsi
    alpha_n=signed_cup(alpha,n,0,s,(1,1))
    def phase(a,den):
        value=a(top)if isinstance(a,Cochain)else a
        assert value.modulus>=den or den==2
        return Polynomial({m:v*(16//den)for m,v in value.terms.items()},16)
    def table(key):return Polynomial({m:1 for m in data[key]},2)
    phases={}
    phases['C']=phase(cup(c,c,2),2)
    phases['CGAMMA']=phase(cup(kappa(u),c,3)+cup(N3,kappa(t2),3),2)
    i,j,k,l,m=top
    extra_cf=dc(top)*(u((j,k,l))*du((i,j,l,m))+u((i,j,m))*du((j,k,l,m))+u((k,l,m))*du((i,j,k,m)))
    phases['CPSI']=phase(cup(psi,c,3)+cup(N3,outpsi,3),2)+phase(extra_cf,2)
    V=Cochain(4,{top:u(top[:3])*u(top[1:4])*u(top[2:5])*du((0,1,3,4))})
    gamma_half=(V+operation('123131',u,u,t)+cup(cup(u,du,2),u,1)+cup(u,t,1)+cup(u,cup(u,t,1),2)
                +cup(cup(u,u),cup(w,u),4)+cup(cup(u,u)+cup(w,u),cup(s,b),4)
                +cup(cup(w,s,1),u)+cup(t,cup(s,u),2)+cup(cup(s,s),u)+cup(s,b)+cup(s,cup(cup(s,u),u,2)))
    gamma_quarter=cup(Bgamma,Bgamma,2)+cup(integer_u,integer_u)-cup(integer_w,integer_u)
    phases['GAMMA']=phase(gamma_half,2)+phase(gamma_quarter,4)
    mixed_half=cup(B,integer_u.differential(),2)+ds(cup(Bgamma,integer_u,2),s)-cup(Bgamma,integer_u,1)
    mixed_quarter=(-cup(Bgamma,Bpsi,2)-cup(Bpsi,Bgamma,2)+cup(Bgamma,alpha_n,3)
                   +cup(integer_u-t2.lift(16),integer_u.differential(),1)
                   +cup(integer_u,t2.lift(16))+cup(t2.lift(16),integer_u)
                   +ds(A.lift(16)-t.lift(16),s))
    phases['GAMMAPSI']=phase(table('mixed_half_monomials'),2)+phase(mixed_half,2)+phase(mixed_quarter,4)
    second=(alpha-alpha.binary().lift(16)).divide(2).binary()
    psi_quarter=-cup(Bpsi,Bpsi,2)+cup(Bpsi,alpha_n,3)-cup(integer_w,t2.lift(16))-cup(second,s).lift(16)
    phases['PSI']=phase(table('pure_half_monomials')-cup(t2,t2)(top),2)+phase(psi_quarter,4)+phase(cup(integer_W,t2.lift(16)),8)
    residuals={name:len((value-Polynomial(dict(data['reference_sector_phases_mod16'][name]),16)).terms)for name,value in phases.items()}
    total=sum(phases.values(),Polynomial(0,16))
    total_res=len((total-Polynomial(dict(data['reference_total_phase_mod16']),16)).terms)
    assert not any(residuals.values()) and not total_res,(residuals,total_res)
    return {'status':'PASS','scope':data['scope'],'independent_binary_variables':len(labels),'method':'Exact physical lower-tower Boolean and signed integer polynomials; no sampling or solve','sector_residual_coefficients':residuals,'total_residual_coefficients':total_res,'collected_complete_phase_coefficients':len(total.terms),'declared_structure_counts':data['counts'],'new_gauge':False,'integer_output_gauge_applied':False,'phase_modulus':16,'canonical_lifts_and_twists_preserved':True,'open_exchange_identities':verify_open_exchange_identities()}

if __name__=='__main__':print(json.dumps(run(),indent=2))
