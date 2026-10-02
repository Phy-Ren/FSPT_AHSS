"""Fixed representatives of the supplied September 24 manuscript. Units 1/8."""
from cochains import *

def source(a,w,s):
 return cup(a,a,a.d-2)+w*a+s*a.beta().red()
def mk(a,b,s):return cup(a,b,a.d-1)+s*cup(a,b,a.d)
def makeupper(a,w,s,bits=0):
 f=source(a,w,s);p=cone(a.N,a.d+1,bits)
 for t in faces(a.N,a.d+1):
  if t[0]:p.v[t]=(p[t]+f[(0,)+t])%2
 return p

def gamma(a,w,s):
 r=a.beta().red();P=a.beta();k=a.d
 if k==1:
  h=word('123134',w,w,a,a)+cup(w*a,s*r,2)+cup(w,s,1)*r+s*(s+a)*r
  return phase((4,h),(2,cup(w,P,integer=True)),(2,cup(s,cup(a,P,integer=True),integer=True)))
 if k==2:
  x=word('1213243',a,a,a,a)+word('1213431',a,a,a,a)+word('1232141',a,a,a,a)+word('1234321',a,a,a,a)
  z='1231343'; zs='1231434'
 elif k==3:
  x=word('1213243142',a,a,a,a)+word('1213431412',a,a,a,a)+word('1232431421',a,a,a,a)+word('1234314212',a,a,a,a)+cup(r,r,2)
  z='12313434';zs='12314343'
 else: raise ValueError(k)
 Q=cup(a,a,k-2);W=w*a;R=s*r
 h=word(z,w,w,a,a)+x+cup(Q,W,k+1)+cup(Q,R,k+1)+cup(W,R,k+1)+word(zs,s,s,r,r)+cup(w,s,1)*r+s*Q
 carry=C(a.N,k+1,{f:(v+v%2)//2 for f,v in P.v.items()},None)
 h=h+s*s*carry.red()
 return phase((4,h),(2,cup(w,P,integer=True)),(2,cup(P,P,k-1,integer=True)))

def upper_gw(p,w):return phase((4,cup(p,p,p.d-2)+cup(p,p.di(),p.d-1)+w*p))
def operator_gauge(p):return phase((4,cup(p,p.di(),p.d)))
def Oca(a,p,w,s):return (upper_gw(p,w)+gamma(a,w,s)).red(8)
def Oop(a,p,w,s):return (Oca(a,p,w,s)+operator_gauge(p).D(s)).red(8)
def GW(a,p,b,q,w,s):return phase((4,cup(p,q,a.d)+cup(p.di(),q,a.d+1)+cup(p+q,mk(a,b,s),a.d)))
