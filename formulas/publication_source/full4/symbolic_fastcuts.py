"""Algebraically identical interval cuts, short-circuiting identically zero factors."""
from cochains import C,interval_terms

def cup(a,b,i=0,s=None,twists=(0,0)):
 degree=a.deg+b.deg-i
 if i<0 or a.known_zero or b.known_zero:return C(degree,mod=a.mod)
 terms=interval_terms(tuple(1+j%2 for j in range(i+2)),(a.deg,b.deg));sign=(-1)**((i*(a.deg+b.deg)+i*(i-1)//2)%2)
 def ev(f):
  out=0
  for fs,cs in terms:
   ff=tuple(f[i] for i in fs[0]);gg=tuple(f[i] for i in fs[1])
   av=a(ff)
   if not av:continue
   bv=b(gg)
   if not bv:continue
   term=av*bv
   if s is not None and a.mod!=2:
    tr=0
    if twists[0] and ff[0]!=f[0]:tr+=s((f[0],ff[0]))
    if twists[1] and gg[0]!=f[0]:tr+=s((f[0],gg[0]))
    term=term*((-1)**(tr%2))
   out+=term*(cs*sign)
  return out
 out=C(degree,fun=ev,mod=a.mod)
 out.closed=(a.closed and b.closed and(i==0 or(a is b and a.mod==2)))and s is None
 return out

def op(word,*args):
 w=tuple(map(int,word));deg=tuple(x.deg for x in args);d=sum(deg)-len(w)+len(args)
 if any(a.known_zero for a in args):return C(d)
 terms=interval_terms(w,deg)
 def ev(f):
  ans=0
  for fs,_ in terms:
   term=1
   for x,g in zip(args,fs):
    term*=x(tuple(f[i] for i in g))
    if not term:break
   ans+=term
  return ans
 return C(d,fun=ev)

def install():
 import cochains,compact,explicit_pip,fractional,cubic_repair
 for m in (cochains,compact,explicit_pip,fractional,cubic_repair):
  if hasattr(m,'cup'):m.cup=cup
  if hasattr(m,'op'):m.op=op
