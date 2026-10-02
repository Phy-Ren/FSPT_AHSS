"""Complete zero-background 3+1D terminal product in the fixed Majorana
Cartan--Adem/Gu--Wen coordinate. All phase outputs are integer numerators /16.
This module does not claim a nonzero-background or 4+1D terminal product.
The only new binary polynomial has two displayed brackets (six expanded cups).
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,sq,op,adem

Z4=(('12413423','xxxy'),('12314132','xxyy'),('12314324','xxyy'),
    ('12341321','xxyy'),('12132413','xyyy'),('12324214','xyyy'))

def beta(x):return x.lift().d().div(2)
def mc_coordinate16(x):
    return cup(x.lift(),beta(x),1).scaled(4)+cup(x.lift(),x.lift()).scaled(2)
def source16(u,c):
    return (sq(c,2)+adem(u)).lift().scaled(8)+cup(beta(u),beta(u),1).scaled(4)

def mc_product16(x,c,y,cp):
    """Literal six-word closed-Majorana product, not a primitive oracle."""
    z=C(4);atoms={'x':x,'y':y}
    for word,labels in Z4:z=z+op(word,*(atoms[j] for j in labels))
    P=beta(x);Q=beta(y);N=x+y;S=cup(x,y,2).lift();t=cup(x,y,1)
    half=cup(c,cp,2)+cup(c.d(),cp,3)+cup(c+cp,t,2)+z
    quarter=(cup(P,Q,2).scaled(-1)+cup(P+Q,S,1)-cup(S,beta(N),1)
             +cup(S,S)+cup(x.lift(),y.lift()))
    return (half.lift().scaled(8)+quarter.scaled(4)
            +mc_coordinate16(N)-mc_coordinate16(x)-mc_coordinate16(y))

def root_data(n,np):
    if n.deg!=1 or np.deg!=1 or n.mod is not None or np.mod is not None:
        raise ValueError('Two ordinary integer degree-one cocycles are required')
    a=n.reduce(2);b=np.reduce(2)
    h=(n-a.lift()).div(2).reduce(2);k=(np-b.lift()).div(2).reduce(2)
    v=cup(a,b,1);t=cup(a,b)
    eta0=cup(cup(a,v),b)+cup(h,cup(b,b))
    g=cup(a+h,k);eta=eta0+g.d()
    L=(cup(cup(cup(a,cup(a,k,1))+cup(h,k),a+b),b)
       +cup(cup(h,cup(b,v)+cup(v,a)),b))
    kap=(t.lift()-cup(n,np)).div(2)
    return {'a':a,'b':b,'h':h,'k':k,'v':v,'t':t,'eta0':eta0,
            'eta':eta,'g':g,'L':L,'kap':kap,'beta':beta(t)}

def fermion_gauge16(c,g):
    """O(u,c+dg)-O(u,c)=d(gauge), with u fixed."""
    dg=g.d()
    return (sq(g,2)+cup(c,dg,2)+cup(c.d(),dg,3)).lift().scaled(8)

def root_phase16(n,np):
    D=root_data(n,np);t=D['t'];kap=D['kap'];bt=D['beta']
    fractional=(cup(kap,bt,1)+cup(kap,kap)).scaled(4)+mc_coordinate16(t)
    return fractional+D['L'].lift().scaled(8)+fermion_gauge16(D['eta0'],D['g'])

def lower(n,u,c,np,v,cp):
    D=root_data(n,np);t=D['t'];w=u+v;f=c+cp+cup(u,v,1)
    return n+np,w+t,f+D['eta']+cup(w,t,1)

def product16(n,u,c,np,v,cp):
    D=root_data(n,np);t=D['t'];w=u+v;f=c+cp+cup(u,v,1)
    return (mc_product16(u,c,v,cp)+mc_product16(w,f,t,D['eta'])
            +root_phase16(n,np))

def raw_coordinate16(u):return cup(u,beta(u).reduce(2),1).lift().scaled(8)

def raw_product16(n,u,c,np,v,cp):
    _,U,_=lower(n,u,c,np,v,cp)
    return product16(n,u,c,np,v,cp)+raw_coordinate16(U)-raw_coordinate16(u)-raw_coordinate16(v)

def operator_coordinate16(c):return cup(c,c.d(),3).lift().scaled(8)
def operator_source16(u,c):return source16(u,c)+operator_coordinate16(c).d()
def operator_product16(n,u,c,np,v,cp):
    _,U,Cf=lower(n,u,c,np,v,cp)
    return product16(n,u,c,np,v,cp)+operator_coordinate16(Cf)-operator_coordinate16(c)-operator_coordinate16(cp)
