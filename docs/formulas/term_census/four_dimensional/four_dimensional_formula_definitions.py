"""Literal source/product expressions for the weighted count semiring.
Internal Python names are declared immediately and are not reader notation.
This file is evaluated by derive_four_dimensional_weights.py.
"""
a,b,h,k,n,m,u,v,c,cp,w,W,s=map(atom,['bar n2','bar n2 prime','second n2','second n2 prime','n2','n2 prime','check n3','check n3 prime','n4','n4 prime','omega2','check omega2','s1'])
A=cup(a,a)+cup(W,a);Ap=cup(b,b)+cup(W,b)
t=cup(a,b,1);r=cup(a,b,2)
# The declared derivatives remain standard differential inputs in baseline.
kappa=cup(u,u,1)+cup(s,cup(u,u,2))+cup(w,u)+cup(u,d(u),2)+cup(s,cup(u,d(u),3))
def psi(a,h):
 return (ms('1231343',a,a,a,a)+ms('1231343',W,W,a,a)+cup(cup(a,a),cup(W,a),3)+cup(h,d(h))
 +cup(cup(a,a,1),cup(s,a),1)+cup(s,cup(cup(a,a),cup(W,a),4)+cup(cup(a,s,1),a)+cup(a,cup(a,a,1),1)+cup(a,a))
 +cup(cup(W,W,1)+cup(s,W),h)+cup(cup(cup(W,W,1),s,1)+cup(s,cup(s,W,1)),a))
Xi=psi(a,h)
Eg=cup(u,v,2)+cup(s,cup(u,v,3))
Em=cup(d(u),v,3)+cup(u+v,t,2)+cup(s,cup(d(u),v,4)+cup(u+v,t,3))
ell=op('face-monomial',a,b)+op('face-monomial',a,b,a,b)
z=(ms('12413423',a,a,a,b)+ms('12314132',a,a,b,b)+ms('12314324',a,a,b,b)+ms('12341321',a,a,b,b)+ms('12132413',a,b,b,b)+ms('12324214',a,b,b,b))
Ep=(z+cup(cup(W,a+b),t,3)+cup(cup(b,b),cup(W,a),4)+cup(d(t),cup(W,a+b),4)+cup(h,k+b)+cup(a,k)+cup(d(h),k,1)+cup(h+k,r)
 +cup(cup(s,a),cup(b,b,1),2)+cup(a,cup(s,b),1)+cup(r,cup(s,a+b),1)+cup(s,cup(s,r)+cup(a,d(k),2)+cup(r,a+b,1)+ell))
E=Eg+Em+Ep
Bg=atom('beta-open check n3');Bgp=atom('beta-open check n3 prime')
Bp=(lift(A)-cup(n,n)-cup(W,n)).scale(F(1,2))
Bpp=(lift(Ap)-cup(m,m)-cup(W,m)).scale(F(1,2))
bg,bgp,bp,bpp=bar(Bg),bar(Bgp),bar(Bp),bar(Bpp)
# Reduce parity of integral carries before using binary V.
lg=cup(u,v,3);lm=cup(u+v,t,3);lp=bar((t+cup(n,m,1)).scale(F(1,2)))
def Sq2(x):return cup(x,x,1)+cup(x,d(x),2)
Vg=(cup(bg,bgp,3)+cup(d(bg),bgp,4)+cup(bg+bgp,d(lg),3)+cup(d(bg)+d(bgp),d(lg),4)+Sq2(lg)+cup(w,lg))
Vm=(cup(bg,bpp,3)+cup(d(bg),bpp,4)+cup(bp,bgp,3)+cup(d(bp),bgp,4)
 +cup(bg+bgp,d(lm+lp)+cup(b,a),3)+cup(d(bg)+d(bgp),d(lm+lp)+cup(b,a),4)
 +cup(bp+bpp,d(lg+lm),3)+cup(d(bp)+d(bpp),d(lg+lm),4)+Sq2(lm)+cup(cup(b,a),d(lg+lm),3)+cup(w,lm)+cup(v,a)+cup(b,u))
for x,y in [(lg,lm),(lg,lp),(lm,lp)]:Vm=Vm+cup(x,y,1)+cup(y,x,1)+cup(x,d(y),2)+cup(y,d(x),2)
bs=atom('bar beta_s check omega2');bs2=atom('second beta_s check omega2')
Vp=(cup(bp,bpp,3)+cup(d(bp),bpp,4)+cup(bp+bpp,d(lp)+cup(b,a),3)+cup(d(bp)+d(bpp),d(lp)+cup(b,a),4)
 +Sq2(lp)+cup(cup(b,a),d(lp),3)+cup(w,lp)+cup(bs2+bs,r)+ms('1231343',b,b,a,a)+cup(cup(W,b,1),a)+cup(k,cup(a,a,1))+cup(cup(s,b),h)+cup(cup(s,cup(b,s,1)),a))
Cartan=(ms('12132434',bs,bs,a,a)+cup(bs2,cup(a,a,1))+cup(cup(s,bs),h)+cup(cup(s,cup(bs,s,1)),a))
Ptw=cup(W,W)+cup(W,op('d_s',W),1)
N=atom('N2');Na=atom('bar N2');U=atom('check N3');Cout=atom('N4')
ku=(cup(U,U,1)+cup(s,cup(U,U,2))+cup(w,U)+cup(U,d(U),2)+cup(s,cup(U,d(U),3)))
kp=(cup(v,v,1)+cup(s,cup(v,v,2))+cup(w,v)+cup(v,d(v),2)+cup(s,cup(v,d(v),3)))
Xip=psi(b,k);XiN=psi(Na,atom('second N2'))
# Named sums are represented by their literal rows, never by one AST node.
rows=WEIGHTS['baseline_majorana_rows']
Tg=P();Tm=P();al={'u':u,'A':d(u),'w':w,'s':s}
for row in rows:
 term=ms(row['word'],*(al[x]for x in row['inputs']))
 if 'A'in row['inputs']:Tm=Tm+term
 else:Tg=Tg+term
