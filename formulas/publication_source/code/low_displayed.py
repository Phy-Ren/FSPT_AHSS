"""Literal compact forms of current manuscript Eqs. (28),(56),(154),(174).

These are an independent regrouping of low_formulas.py, not new endpoints.
All phase outputs are integer numerators over eight.
"""
from cochains import *
from low_formulas import carry,Z4_WORDS

def majorana3(a,b,w,s):
 N=a+b;u=cup(a,b,1);m=a*b+s*u;P=a.beta();Q=b.beta();R=N.beta();S=u.lift()
 z=(cup(a,a*b,1)*b+cup(w*N,m,2)+(cup(w,s,1)+cup(w,s*a,2))*u
    +cup(m,s*u,1)+cup(a,s*u,1)*a+cup(s,a,1)*a*u
    +s*(b*u+cup(u,m,1)+cup(N,s*u,1)))
 qr=(cup(P,Q,1,integer=True)-cup(P+Q+w.lift(),S,integer=True)
    -cup(S,R,integer=True)+cup(s,cup(a,b,integer=True),integer=True))
 cube=lambda x:cup(x,cup(x,x,integer=True),integer=True)
 return phase((4,z),(2,qr),(1,cube(a)+cube(b)-cube(N)))

def majorana4(a,b,w,s):
 N=a+b;u=cup(a,b,2);t=cup(a,b,1);m=t+s*u;P=a.beta();Q=b.beta();R=N.beta();r=P.red();rp=Q.red();S=u.lift()
 z=C(a.N,4,{});fields={'a':a,'b':b}
 for wd,inputs in Z4_WORDS:z=z+word(wd,*[fields[v] for v in inputs])
 z=(z+cup(w*N,m,3)+cup(a*b+b*a,w*N,4)+cup(b*b,w*a,4)
    +cup((b+w)*b,s*r,4)+cup(w,s,1)*u+cup(t,s*(r+rp),3)
    +cup(N*N,s*u,3)+cup(t,s*u,2)
    +s*(m+cup(r+rp,s*u,3)+cup(a,cup(b,m,2),2)+cup(r,rp,3)
      +cup(N,m,2)+cup(N,u,1)+cup(b,r,2)+(carry(N)-carry(a)-carry(b)).red()))
 qr=(cup(P,Q,2,integer=True).scale(-1)+cup(P+Q,S,1,integer=True)-cup(S,R,1,integer=True)
      +cup(S,S,integer=True)+cup(a,b,integer=True)-cup(w,S,integer=True)
      +cup(s,cup(a,b,1,integer=True),integer=True)
      +cup(N,R,1,integer=True)-cup(a,P,1,integer=True)-cup(b,Q,1,integer=True))
 eig=cup(N,N,integer=True)-cup(a,a,integer=True)-cup(b,b,integer=True)
 return phase((4,z),(2,qr),(1,eig))
