"""Final explicit manuscript-aligned U3 and U4; phases in units of 1/8.

The functions ``blocks3`` and ``blocks4`` correspond one-to-one to the six
summands in the two boxed formulas of the English note. They do not read any
numerical phase table. ``Uop`` preserves the manuscript's separate c/cgamma
operator factors; ``Uca`` uses its total Gu--Wen coordinate.
"""
from cochains import C, faces, cup, word, phase
from manuscript import GW, mk, operator_gauge

Z4_WORDS = [
    ('12413423', 'aaab'), ('12314132', 'aabb'),
    ('12314324', 'aabb'), ('12341321', 'aabb'),
    ('12132413', 'abbb'), ('12324214', 'abbb'),
]

def carry(a):
    P = a.beta()
    return C(a.N, a.d+1, {f:(v+v%2)//2 for f,v in P.v.items()}, None)

def h4(a):
    return phase((2, cup(a, a.beta(), 1, integer=True)),
                 (1, cup(a, a, integer=True)))

def j4(a,s):
    return phase((4, s*carry(a).red()))

def R4(a,s):
    """rho4=h4+j4; used only for the explicit reference dictionary."""
    return (h4(a)+j4(a,s)).red(8)

def H3(a):
    return phase((1, a*a*a))

def blocks3(a,c,b,cp,w,s):
    if a.d != 1 or b.d != 1 or c.d != 2 or cp.d != 2:
        raise ValueError('blocks3 requires degrees (a,c,b,cprime)=(1,2,1,2)')
    N=a+b; u=cup(a,b,1); S=cup(a,b,1,integer=True); T=S.di(None)
    P=a.beta(); Q=b.beta()
    beta=phase((2,cup(P,Q,1,integer=True)),
               (-2,cup(P+Q,S,integer=True)),
               (-2,cup(S,P+Q,integer=True)),
               (2,cup(S,T,integer=True)))
    y=(phase((4,cup(a,a*b,1)*b))-H3(N)+H3(a)+H3(b)).red(8)
    lw=phase((4,cup(w*N,a*b,2)),(-2,cup(w,S,integer=True)))
    ea=cup(s,a,1); eb=cup(s,b,1); eu=cup(s,u,1)
    ls=s*(ea+eb+eu)*u+ea*u*N+(ea*a+a*eb+s*a+a*s)*u+s*(u*a+a*b+b*u)
    pure_s=phase((4,ls),(2,s*a*b))
    mixed=phase((4,cup(w,s,1)*u+cup(w*N,s*u,2)+cup(w*b,s*a*a,3)))
    return {'GW':GW(a,c,b,cp,w,s),'Bockstein':beta,'Adem':y,
            'omega':lw,'s':pure_s,'omega_s':mixed}

def blocks4(a,c,b,cp,w,s):
    if a.d != 2 or b.d != 2 or c.d != 3 or cp.d != 3:
        raise ValueError('blocks4 requires degrees (a,c,b,cprime)=(2,3,2,3)')
    N=a+b; P=a.beta(); Q=b.beta(); r=P.red(); rp=Q.red()
    u=cup(a,b,2); t=cup(a,b,1); tb=cup(b,a,1); v=s*u
    S=cup(a,b,2,integer=True); T=S.di(None)
    beta=phase((-2,cup(P,Q,2,integer=True)),
               (2,cup(P+Q,S,1,integer=True)),
               (-2,cup(S,P+Q,1,integer=True)),
               (2,cup(S,T,1,integer=True)),
               (2,cup(S,S,integer=True)))
    z=C(a.N,4,{}); fields={'a':a,'b':b}
    for wd,inputs in Z4_WORDS:
        z=z+word(wd,*[fields[x] for x in inputs])
    y=(phase((4,z),(2,a*b))+h4(N)-h4(a)-h4(b)).red(8)
    lw=phase((4,cup(w*N,t,3)+cup(b*b,w*a,4)+cup(a*b+b*a,w*N,4)),
             (-2,cup(w,S,integer=True)))
    mixed=phase((4,cup(s,w*u,1)+w*cup(s,u,1)+cup(w*a,v,3)
                    +cup(w*b,s*r,4)+cup(w*b,v,3)))
    # Twenty displayed mod-two summands; no hidden homotopy or lookup table.
    ls=(s*cup(rp,v,3)
        +s*cup(a,cup(b,v,2),2)
        +s*cup(r,v,3)
        +cup(t,s*rp,3)
        +cup(b*b,v,3)
        +s*cup(r,rp,3)
        +cup(b*a,s*t,4)
        +cup(t,v,2)
        +cup(b*a,s*tb,4)
        +cup(b*b,s*r,4)
        +s*cup(a,cup(b,t,2),2)
        +cup(v,b*a,3)
        +cup(a*b,v,3)
        +cup(a*a,v,3)
        +cup(t,s*r,3)
        +s*cup(b,v,2)
        +s*cup(a,v,2)
        +s*cup(b,t,2)
        +s*cup(a,t,2)
        +s*s*u)
    BT=phase((2,cup(s,cup(a,b,1,integer=True),integer=True)),
             (4,s*(cup(a+b,u,1)+cup(b,r,2))))
    pure_s=(phase((4,s*t+ls))+BT+j4(N,s)-j4(a,s)-j4(b,s)).red(8)
    return {'GW':GW(a,c,b,cp,w,s),'Bockstein':beta,'Adem':y,
            'omega':lw,'s':pure_s,'omega_s':mixed}

def Uca(a,c,b,cp,w,s):
    if a.d == 1: blocks=blocks3(a,c,b,cp,w,s)
    elif a.d == 2: blocks=blocks4(a,c,b,cp,w,s)
    else: raise ValueError('Only p=1,2 are claimed in this note')
    out=blocks['GW']
    for name in ('Bockstein','Adem','omega','s','omega_s'):
        out=out+blocks[name]
    return out.red(8)

def Uop(a,c,b,cp,w,s):
    total=c+cp+mk(a,b,s)
    return (Uca(a,c,b,cp,w,s)+operator_gauge(total)
            -operator_gauge(c)-operator_gauge(cp)).red(8)
