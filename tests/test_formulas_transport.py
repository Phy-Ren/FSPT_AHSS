"""Independent nonabelian finite-group test of GAP-to-simplex face transport.

The GAP bar callbacks and Python local fields are constructed independently.
Both sign characters are nontrivial and independent on the order-eight D4.
"""
import json, subprocess, random, tempfile, shutil, unittest
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import insulator as U

ROOT=str(Path(__file__).resolve().parents[1])
rng=random.Random(19281)
pairs=[(a,b) for a in range(4) for b in range(2)]
def mul(x,y):return ((x[0]+(-1)**x[1]*y[0])%4,(x[1]+y[1])%2)
def inv(x):return ((-(-1)**x[1]*x[0])%4,x[1])
def sb(g):return g[0]%2
def rb(g):return g[1]
def alpha(g):return F(0) if g==(0,0) else F(2*g[0]+3*g[1]-3,7)
def omega(g,h):return (-1)**(sb(g)+rb(g))*alpha(h)-alpha(mul(g,h))+alpha(g)
def seed(args,offset=0):
    if (0,0) in args:return 0
    return sum((j+1)*(pairs.index(g)+1) for j,g in enumerate(args))%9-4+offset

def local(N,p,callback,vertices,tw):
    return U.Cochain(N,p,{f:callback(*[mul(inv(vertices[f[j]]),vertices[f[j+1]]) for j in range(p)])
                        for f in combinations(range(N+1),p+1)},tw)
def fields(d,xs,variant):
    vs=[(0,0)]
    for g in xs:vs.append(mul(vs[-1],g))
    N=len(xs);st=[sb(g) for g in vs];rt=[rb(g) for g in vs];tt=[s^r for s,r in zip(st,rt)]
    sym=U.Symmetry(local(N,2,lambda g,h:omega(g,h)+F(variant,2)*sb(g)*sb(h),vs,tt),U.char(N,st).ret(st),U.char(N,rt).ret(rt))
    if d==3:
        u=U.Cochain(N,0,{(j,):-2 for j in range(N+1)},st)
        v=local(N,2,lambda *x:seed(x),vs,rt)
        k=u.d()+sym.s1.sc(variant);n=sym.B3.cup(u)+v.d()
        up=U.Cochain(N,0,{(j,):3 for j in range(N+1)},st)
        vp=local(N,2,lambda *x:seed(x,1),vs,rt)
        kp=up.d()+sym.s1.sc(variant);np=sym.B3.cup(up)+vp.d()
    else:
        u=local(N,1,lambda *x:seed(x),vs,st)
        v=local(N,3,lambda *x:seed(x),vs,rt)
        k=u.d();n=sym.B3.cup(u)+sym.rho1.cup(u.cup(k))+v.d()
        up=local(N,1,lambda *x:seed(x,1),vs,st)
        vp=local(N,3,lambda *x:seed(x,1),vs,rt)
        kp=up.d();np=sym.B3.cup(up)+sym.rho1.cup(up.cup(kp))+vp.d()
    return sym,k,n,kp,np,up,vp


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class FormulaTransport(unittest.TestCase):
    def test_independent_nonabelian_face_transport(self):
        spec=[]
        for d in (3,4):
         for op,N in [('source',d+2),('product',d+1),('gauge',d+1),('integer_obstruction',d+1)]:
          for i in range(2):spec.append((d,op,[rng.randrange(1,8) for _ in range(N)],i))
        with tempfile.TemporaryDirectory() as td:
         out=Path(td)/'result.jsonl';script=Path(td)/'check.g'
         pre='''OnBreak:=function() Where(12);QUIT_GAP(1);end;;
        U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;
        r:=(1,2,3,4);;m:=(2,4);; G:=Group(r,m);;
        pairs:=Cartesian([0..3],[0..1]);;elts:=List(pairs,x->r^x[1]*m^x[2]);;
        idx:=g->Position(elts,g);;s:=g->pairs[idx(g)][1] mod 2;;rho:=g->pairs[idx(g)][2];;
        alph:=function(g) if g=Identity(G) then return 0;fi;return (2*pairs[idx(g)][1]+3*pairs[idx(g)][2]-3)/7;end;;
        c:=rec(G:=G,s:=s,rho:=rho);;c.omega:=function(g,h) return (-1)^(s(g)+rho(g))*alph(h)-alph(g*h)+alph(g);end;;
        seed:=function(xs,offset) local total,j;if Identity(G) in xs then return 0;fi;total:=0;for j in [1..Length(xs)] do total:=total+j*idx(xs[j]);od;return total mod 9-4+offset;end;;
        ss:=function(g,h) return s(g)*s(h)/2;end;;
        checked:=U1Add(c.omega,U1Scale(-1,ss));;B:=U1Coboundary(c,"Zt",checked);;
        out:=OutputTextFile("%s",false);;SetPrintFormattingStatus(out,false);;
        '''%(ROOT,out)
         code=pre
         for d,op,indices,variant in spec:
          code+='variant:=%d;;c.omega:=function(g,h) return (-1)^(s(g)+rho(g))*alph(h)-alph(g*h)+alph(g)+variant*s(g)*s(h)/2;end;;checked:=U1Add(c.omega,U1Scale(-1,ss));;B:=U1Coboundary(c,"Zt",checked);;\n'%variant
          if d==3:
           code+='u:=function() return -2;end;;v:=function(xs...) return seed(xs,0);end;;up:=function() return 3;end;;vp:=function(xs...) return seed(xs,1);end;;\n'
          else:code+='u:=function(xs...) return seed(xs,0);end;;v:=function(xs...) return seed(xs,0);end;;up:=function(xs...) return seed(xs,1);end;;vp:=function(xs...) return seed(xs,1);end;;\n'
          code+='k:=U1Coboundary(c,"Zs",u);;kp:=U1Coboundary(c,"Zs",up);;\n'
          if d==3:code+='k:=U1Add(k,U1Scale(variant,s));;kp:=U1Add(kp,U1Scale(variant,s));;\n'
          code+='n:=U1Add(U1Cup(c,3,B,"Zt",%d,u,"Zs",0,false),U1Coboundary(c,"Zr",v));;\n'%(d-3)
          code+='np:=U1Add(U1Cup(c,3,B,"Zt",%d,up,"Zs",0,false),U1Coboundary(c,"Zr",vp));;\n'%(d-3)
          if d==4:
           code+='n:=U1Add(n,U1Cup(c,1,rho,"Zr",3,U1Cup(c,1,u,"Zs",2,k,"Zs",0,false),"Z",0,false));;\n'
           code+='np:=U1Add(np,U1Cup(c,1,rho,"Zr",3,U1Cup(c,1,up,"Zs",2,kp,"Zs",0,false),"Z",0,false));;\n'
          extras='rec(sheet_prime:=kp,charge_prime:=np)' if op=='product' else ('rec(sheet_parameter:=up,charge_parameter:=vp)' if op=='gauge' else 'rec()')
          comp='"phase"' if op in ('product','gauge') else 'fail'
          code+='f:=U1Formula(c,"%s",%d,rec(sheet:=k,charge:=n),%s,%s,%d);;\n'%(op,d,extras,comp,len(indices))
          code+='WriteLine(out,U1JSON(String(CallFuncList(f,List(%s,i->elts[i+1])))));;\n'%str(indices)
         code+='CloseStream(out);;QUIT_GAP(0);\n'
         script.write_text(code)
         proc=subprocess.run(['gap','-q','-b',str(script)],capture_output=True,text=True,timeout=120)
         if proc.returncode:raise RuntimeError(proc.stdout+proc.stderr)
         results=[F(json.loads(x)) for x in out.read_text().splitlines()]
         assert len(results)==len(spec),(len(results),len(spec),proc.stdout,proc.stderr)
         for (d,op,indices,variant),actual in zip(spec,results):
          sym,k,n,kp,np,u,v=fields(d,[pairs[i] for i in indices],variant);N=len(indices)
          if op=='source':expected=U.source(sym,d,k,n)
          elif op=='integer_obstruction':expected=U.integer_obstruction(sym,d,k)
          elif op=='product':expected=U.product(sym,d,k,n,kp,np)[2]
          else:expected=U.gauge(sym,d,k,n,u,v)[2]
          expected=F(expected(tuple(range(N+1))))
          assert actual==expected,(d,op,indices,actual,expected)


if __name__ == "__main__":
    unittest.main()
