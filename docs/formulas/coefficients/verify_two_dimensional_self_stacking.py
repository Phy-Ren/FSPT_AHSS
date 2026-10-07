"""Exact complete 2+1D self-stacking verification in the current reader phase."""
import importlib.util,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cochains',ROOT/'verify_three_dimensional_majorana_self_stacking.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.faces=lambda degree: tuple(itertools.combinations(range(4),degree+1))
P,C,cu=m.Polynomial,m.Cochain,m.cup
labels=[]
def closed(name,degree):
 v={}
 for f in m.faces(degree):
  if f[0]==0:v[f]=P({1<<len(labels):1},2);labels.append((name,f))
 for f in m.faces(degree):
  if f[0]:v[f]=sum(v[(0,)+f[:j]+f[j+1:]]for j in range(len(f)))
 return C(degree,v)
n,s,w=closed('n1',1),closed('s1',1),closed('omega2',2)
a=n.values;b=s.values;top=(0,1,2,3)
L=b[0,1]*a[1,2]*a[1,3]*a[2,3]+b[0,1]*a[0,2]*a[1,2]*(a[1,3]*a[2,3]+a[1,2]*a[2,3])+a[2,3]*a[2,3]*(b[1,2]*a[1,3]*(b[0,1]*a[1,2]+a[0,1])+b[0,1]*b[0,2]*a[1,2])
# Complete equal-input phase in units of one eighth.
B=m.beta(n);N=cu(n,n)+cu(s,n);q=cu(w,n)+cu(s,B.binary())
c0=closed('n2_root',2)
c=C(2,{f:c0(f)+(q((0,)+f)if f[0]else 0)for f in m.faces(2)})
assert not(c.differential()-q)(top)
nI=n.lift(8);sI=s.lift(8);wI=w.lift(8);BI=n.lift(16).differential().divide(2)
lam=cu(nI,nI,1)
first=cu(cu(n,cu(n,n),1),n)
Lco=C(3,{top:L})
half=Lco+cu(cu(w,s,1),n)+cu(cu(w,n),cu(s,cu(n,n)),3)+first
quarter=(cu(BI,BI,1)-cu(BI+BI,lam)-cu(lam,BI+BI)+cu(lam,lam.differential())-cu(wI,lam)+cu(s,cu(n,n)).lift(8))
upper=cu(c,c,1)+cu(q,c,2)
literal=4*(half+upper)(top).lift(8)+2*quarter(top)+2*cu(cu(n,n),n)(top).lift(8)
Lnew=cu(cu(n,n),cu(s,n),1)+cu(cu(s,cu(s,n),1),n)
short_half=upper+Lnew+cu(cu(w,s,1),n)+cu(s,B.binary())
short_quarter=-cu(cu(n,n),n).lift(8)-q.lift(8)
short=4*short_half(top).lift(8)+2*short_quarter(top)
checks={'first_intrinsic_term':first(top),'Bockstein_cup1_diagonal':cu(BI,BI,1)(top),'antiunitary_two_terms':L-Lnew(top),'complete_phase':literal-short}
assert all(not x for x in checks.values())
receipt={'status':'PASS','independent_binary_variables':len(labels),'scope':'Complete 2+1D zero-integer-decoration input; closed n1, omega2, s1; every n2 completion; current reader phase','proof':'Exact Boolean and integral coefficient comparison','residuals':{k:len(v.terms)for k,v in checks.items()},'half_terms':6,'quarter_terms':2,'total_terms':8,'labels':labels}
(Path(__file__).parent/'two_dimensional_self_stacking_check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
