"""Exact signed CF-only parity bridge; no superconducting production imports."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import sys, random, json, hashlib
sys.dont_write_bytecode=True
ROOT=Path('/home/xingyu/AllFSPT_reviews/e8_v09_da3ad936/E8_AHSS_v0_9')
sys.path.insert(0,str(ROOT/'reference'))
import u1f
from simplex import C,rand,char,bin0,Fopen
rng=random.Random(2026101501)
counts={}
def ck(name,c):
    assert c.mod(1).maxabs()==0,(name,next((f,v) for f,v in c.mod(1).v.items() if v))
    counts[name]=counts.get(name,0)+1
for d in (2,3,4):
  for case in range(8):
    N=d+2
    st=[rng.randrange(2) for _ in range(N+1)]
    rt=[rng.randrange(2) for _ in range(N+1)]
    ct=[a^b for a,b in zip(st,rt)]
    s=char(N,st).ret(st);r=char(N,rt).ret(rt)
    X=rand(N,1,ct,rng).sc(F(1,7))
    W=rand(N,1,None,rng).d().mod(2)
    M=W.ret(ct)+rand(N,2,ct,rng).sc(2)
    omega=(M-X.d()).sc(F(1,2))
    bg=u1f.Symmetry(omega,s,r)
    z=rand(N,d-1,rt,rng).d();zp=rand(N,d-1,rt,rng).d()
    u=rand(N,d-1,rt,rng)
    def SC_source(x): return (W.cup(bin0(x))+bin0(x).sq(2)).sc(F(1,2)).ret(st)
    def R(z): return X.cup(z).sc(F(1,2))
    def GCI(z,u): return (omega.cup(u)+bin0(u).sq(2).sc(F(1,2))+Fopen(z,u.d())).ret(st)
    def GSC(z,u): return ((W.cup(bin0(u))+bin0(u).sq(2)).sc(F(1,2))+Fopen(bin0(z),bin0(u).d())).ret(st)
    ck('closed_charge_source_d'+str(d),SC_source(z)-u1f.charge_source(bg,z)-R(z).d())
    ck('closed_charge_product_d'+str(d),Fopen(z,zp)-Fopen(bin0(z),bin0(zp))+R(z+zp)-R(z)-R(zp))
    K=X.cup(u).sc(F(-1,2))
    ck('closed_charge_gauge_d'+str(d),GCI(z,u)+R(z+u.d())-R(z)-GSC(z,u)-K.d())
    opened=rand(N,d,rt,rng)
    ck('open_charge_residual_d'+str(d),SC_source(opened)-u1f.charge_source(bg,opened)-R(opened).d()-X.cup(opened.d()).sc(F(1,2)))
result={'status':'PASS','seed':2026101501,'checks':sum(counts.values()),'counts':counts,'scope':'CF-only bridge in the stated short-gauge coordinates, d=2,3,4; independent s/rho, full circle carry. Open-charge residual retained. Not the nonzero-CI universal bridge.','notation':'(e_p,n_p,n_{p+2},nu_{p+3}); e_p=n_p=0, z=n_{p+2}','reference_sha256':hashlib.sha256((ROOT/'reference/u1f.py').read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
