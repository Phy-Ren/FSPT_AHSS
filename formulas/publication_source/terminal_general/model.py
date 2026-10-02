"""Zero-background p+ip terminal cochains in the accepted B coordinate.
The source and the residual are transcriptions, not inferred products.
"""
from pathlib import Path
import sys,json
from functools import lru_cache
from itertools import combinations
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,sq,op,primitive
from compact import beta_open

TD=json.loads((ROOT/'stages/data/T6_zero_anf.json').read_text())
TF=[tuple(f) for f in TD['faces']]
TM=tuple(sorted(int(m) for m in TD['ANF_masks']))

def compile_anf(masks):
    nodes=[('z',),('o',)]; ids={():0,(0,):1}
    def rec(ms):
        if ms in ids:return ids[ms]
        # Highest variable gives predictable compact DAG and cheap partition.
        b=1<<(max(ms).bit_length()-1)
        pp=tuple(m^b for m in ms if m&b);qq=tuple(m for m in ms if not m&b)
        ip,iq=rec(pp),rec(qq)
        ids[ms]=len(nodes);nodes.append(('x',b.bit_length()-1,ip,iq))
        return ids[ms]
    root=rec(tuple(sorted(masks)))
    return nodes,root

DAGFILE=Path(__file__).with_name('T6_dag.json')
if DAGFILE.exists():T_DAG,T_ROOT=json.loads(DAGFILE.read_text())
else:
    T_DAG,T_ROOT=compile_anf(TM);DAGFILE.write_text(json.dumps((T_DAG,T_ROOT)))

def eval_anf_dag(nodes,root,xs):
    vals=[0,1]
    for node in nodes[2:]:
        v=xs[node[1]]*vals[node[2]]+vals[node[3]]
        vals.append(v%2)
    return vals[root]

def T6(u):
    def ev(f):
        xs=[u(tuple(f[i] for i in g)) for g in TF]
        return eval_anf_dag(T_DAG,T_ROOT,xs)
    return C(6,fun=ev)

def digit(z,j):
    if isinstance(z,int):return (z>>j)&1
    for _ in range(j):z=(z-(z%2).lift(z.m))//2
    return z%2

ydata=json.loads((ROOT/'reference/d4_input/code/Y6_word_total.json').read_text())
YTERMS=next(b['terms'] for b in ydata['blocks'] if (b['i'],b['j'],b['k'])==(0,6,0))
YMASKS=[]
for nc,wc in YTERMS:
    nc=int(nc);mask=0
    for j in range(15):
        e=(nc>>(4*j))&15
        for q in range(3):
            if e>>q&1:mask|=1<<(3*j+q)
    YMASKS.append(mask)
Y_DAG,Y_ROOT=compile_anf(tuple(YMASKS))

def Y6(n):
    def ev(f):
        coords=[n((f[u-1],f[u],f[v]))-n((f[u-1],f[u],f[v-1])) for u,v in combinations(range(1,7),2)]
        xs=[digit(z,q) for z in coords for q in range(3)]
        return eval_anf_dag(Y_DAG,Y_ROOT,xs)
    return C(6,fun=ev)

def half_floor(n):return (n-n.reduce(2).lift()).div(2)
def zeta(a,b):return op('1231343',a,a,b,b)
def xi(n):
    a=n.reduce(2);h=half_floor(n).reduce(2)
    return zeta(a,a)+cup(h,h.d())
def F(n,u):return sq(u,2)+xi(n)
def B(n,u):return (u.lift().d()-cup(n,n)).div(2)

def H(n,u):
    a=n.reduce(2);h=half_floor(n).reduce(2)
    return T6(u)+cup(sq(u,2),xi(n),4)+Y6(n)+cup(sq(u,1),cup(a,h)+cup(h,a),2)

def intrinsic(a,b):
    return (op('12413423',a,a,a,b)+op('12314132',a,a,b,b)+op('12314324',a,a,b,b)
         +op('12341321',a,a,b,b)+op('12132413',a,b,b,b)+op('12324214',a,b,b,b))

def lower(n,u,m,v):
    a=n.reduce(2);b=m.reduce(2);h=half_floor(n).reduce(2);k=half_floor(m).reduce(2)
    t=cup(a,b,1);q=cup(a,b,2)
    e=(cup(u,v,2)+cup(u.d(),v,3)+cup(u+v,t,2)
       +intrinsic(a,b)+cup(h+a,k+b)+cup(h.d(),k,1)+cup(h+k,q))
    return n+m,u+v+t,e

def pair_data(n,u,m,v):
    N,U,e=lower(n,u,m,v)
    la=(U.lift()-u.lift()-v.lift()+cup(n,m,1)).div(2)
    R=cup(m,n);D=la.d()-R
    return dict(N=N,U=U,e=e,B=B(n,u),Bp=B(m,v),lam=la,R=R,D=D)

def residual(n,u,m,v):
    D=pair_data(n,u,m,v);la=D['lam'].reduce(2);r=D['R'].reduce(2);d=D['D'].reduce(2)
    bb=D['B'].reduce(2);bp=D['Bp'].reduce(2)
    a=n.reduce(2);b=m.reduce(2);h=half_floor(n).reduce(2);k=half_floor(m).reduce(2)
    lf=(cup(bb,bp,2)+cup(bb+bp,d,2)+sq(la,3)+cup(la.d(),r,2)
        +cup(cup(b,b),h+a)+cup(k+b,cup(a,a))+op('123143',b,b,a,a))
    f=F(n,u);fp=F(m,v);e=D['e']
    up=sq(e,2)+cup(f,fp,4)+cup(f+fp,e,3)+cup(e,f+fp,3)
    return up+H(D['N'],D['U'])+H(n,u)+H(m,v)+lf

def ZetaZ(m,n):
    return C(5,fun=lambda f:m(f[:3])*m((f[0],f[2],f[3]))*n((f[2],f[3],f[5]))*n(f[3:]),mod=None)

def fraction48(n,u,m,v):
    D=pair_data(n,u,m,v);bb,bp,la,r,dd=(D[k] for k in ('B','Bp','lam','R','D'))
    bn=C(2,fun=lambda f:m(f)*(m(f)-1)//2,mod=None)
    q=cup(n,m,1)
    quart=(cup(bb,bp,3)+cup(bb+bp,dd,3)+cup(la,la,1)+cup(la,la.d(),2)
           +cup(r,la.d(),3)+ZetaZ(m,n)-cup(bn,cup(n,n,1)))
    cubic=cup(n+m.scaled(2),q)+cup(q,n.scaled(2)+m)
    return quart.scaled(12)-cubic.scaled(4)

def source48(n,u,c):return (sq(c,2)+H(n,u)).lift().scaled(24)+cup(B(n,u),B(n,u),2).scaled(12)+cup(cup(n,n),n).scaled(4)
def upper48(c,cp,e):return (cup(c,cp,3)+cup(c.d(),cp,4)+cup(c+cp,e,3)).lift().scaled(24)

def pull(c,projection):
    z=C(c.deg,fun=lambda f:c(tuple(projection[i] for i in f)),mod=c.mod)
    z.closed=c.closed
    return z

def dk_state(d,coords,ufree):
    n=C(2,fun=lambda f:sum(coords[(i,j)] for i in range(f[0]+1,f[1]+1) for j in range(f[1]+1,f[2]+1)),mod=None);n.closed=True
    aa=cup(n.reduce(2),n.reduce(2))
    def uv(f):
        if f[0]==0:return ufree.get(f,0)
        return aa((0,)+f)+sum(ufree.get((0,)+f[:j]+f[j+1:],0) for j in range(4))
    return n,C(3,fun=uv)

def scalar_state(d,rng):
    ns={ij:rng.randrange(-7,8) for ij in combinations(range(1,d+1),2)}
    us={f:rng.randrange(2) for f in combinations(range(d+1),4) if f[0]==0}
    return dk_state(d,ns,us)
