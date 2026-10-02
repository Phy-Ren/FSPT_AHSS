"""Explicit comparison with the manuscript's native suspension."""
from lower import *

def kappa3(n,u,w,s):
 a=n.reduce(2);W=w+cup(s,s)
 return cup(a+s,u)+cup(W,carry(n))+cup(cup(W,a+s,1),a)

def f2(n,u,s):
 a=n.reduce(2);h=carry(n)
 def val(f):
  i,j,k=f;x=a((i,j));y=a((j,k));q=h((j,k));z=u(f)
  return x*z+s((i,j))*((q+z)*(1+x*y)+z*(y+q))
 return C(2,fun=val)

def majorana_gauge(u,r,w,s):
 dr=r.d()
 return (sq(r,2)+cup(s,sq(r,1))+cup(w,r)+cup(u,dr,2)+cup(u.d(),dr,3)
       +cup(s,cup(u,dr,3)+cup(u.d(),dr,4)))

def old_G_symbolic(n,uraw,w,s,*,one=1,zero=0):
 from suspension import G3_MASKS
 a=n.reduce(2);h=carry(n)
 def val(f):
  onefaces=[f[:2],(f[0],f[2]),(f[0],f[3])]
  two=[f[:3],(f[0],f[1],f[3]),(f[0],f[2],f[3])]
  xx=[s(g) for g in onefaces]+[a(g) for g in onefaces]+[h(g) for g in onefaces]+[w(g) for g in two]+[uraw(g) for g in two]
  total=zero
  for mask in G3_MASKS:
   term=one
   for j,x in enumerate(xx):
    if mask>>j&1:term*=x
   total+=term
  return total
 return C(3,fun=val)
