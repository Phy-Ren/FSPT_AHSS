"""Adapted from the frozen U1f consolidated v0.7 formula archive."""
from pathlib import Path
import json
from .simplex import C, F, combinations, word, halves, bin0, background, Fopen, E4d_integer
ROOT=Path(__file__).resolve().parent

CP=json.loads((ROOT/'cartan32_polarizer.json').read_text())
RP=json.loads((ROOT/'r_polarizer.json').read_text())
R_TERMS=tuple(int(m,16) for m in RP['terms_hex'])

def P32(z,x,y):
    vals={}
    for f in combinations(range(z.N+1),6):
        zs=[z((f[0],)+tuple(f[i] for i in ff)) for ff in CP['z_faces']]
        xs=[x((f[0],)+tuple(f[i] for i in ff)) for ff in CP['x_faces']]
        ys=[y((f[0],)+tuple(f[i] for i in ff)) for ff in CP['x_faces']]
        total=0
        for iz,ix,iy in CP['terms']:
            term=xs[ix]*ys[iy]
            for j in iz:term*=zs[j]
            total+=term
        vals[f]=total%2
    return C(z.N,5,vals)

def H22(k,l,s):
    x,y=bin0(k),bin0(l); ss=bin0(s)
    return (word((1,2,3,1,3,4,3),x,x,y,y)+halves(k).cup(y.sq(1),0,True)+ss.cup(x,0,True).cup(halves(l),0,True)+ss.cup(x.cup(ss,1,True),0,True).cup(y,0,True)).mod(2)

def cubic_polarizer(k,l):
    h=k.cup(l,1)
    return k.cup(h).sc(2)+h.cup(k)+h.cup(l).sc(2)+l.cup(h)

def E5_partial(a,k,n,l,m,s,r,lam=F(1,6)):
    A,B=background(a,s);h=k.cup(l,1);e=E4d_integer(k,l,r)
    x,y,z,rr=bin0(k),bin0(l),bin0(B),bin0(r)
    V=rr.cup(x.cup(x,0,True),0,True);Tp=z.cup(y,0,True)
    binary=P32(z,x,y)+halves(B).cup(x.cup(y,2,True),0,True)+V.cup(Tp,5,True)+H22(k,l,s)
    rational=A.cup(h.ret(r.tw)).sc(F(-1,2)) + rr.cup(rr).cup(h).ret(s.tw).sc(F(1,4))+cubic_polarizer(k,l).sc(lam)
    R=s.ret(a.tw).cup(e).sc(F(1,4)).ret(s.tw)
    return (Fopen(n,m)+Fopen(n+m,e)+binary.sc(F(1,2))+rational-R).ret(s.tw)

def R5_table(k,l,s,r):
    spec=RP
    fields=(bin0(r),bin0(s),bin0(k),bin0(l),halves(k),halves(l))
    terms=R_TERMS;vals={}
    for f in combinations(range(k.N+1),6):
        vv=[fields[sp](tuple(f[i] for i in ff)) for sp,ff in spec['variables']]
        value=0
        for mon in terms:
            term=1
            while mon and term:
                bit=mon&-mon;term*=vv[bit.bit_length()-1];mon-=bit
            value+=term
        vals[f]=value%2
    out=C(k.N,5,vals).sc(F(1,2))
    if spec.get('quarter_rxy'):
        out=out+bin0(r).cup(bin0(k),0,True).cup(bin0(l),0,True).sc(F(1,4))
    return out.ret(s.tw)

def E5(a,k,n,l,m,s,r,lam=F(1,6)):
    return E5_partial(a,k,n,l,m,s,r,lam)+R5_table(k,l,s,r)

def lower_gauge(a,k,n,u,v,s,r):
    A,B=background(a,s);du=u.d()
    out=k+du
    q=k.cup(u)+u.cup(k)+u.cup(du)
    return out,n+B.cup(u)+r.cup(q)+v.d()

def lower_commutator(k,l,r):
    return k.cup(l,1).ret(r.tw).sc(-1)+r.cup(k.cup(l,2))

def charge_gauge(a,k,n,v,s,r):
    phi=a.cup(v)+bin0(v).sq(2).sc(F(1,2))
    return (phi+Fopen(n,v.d())).ret(s.tw)

