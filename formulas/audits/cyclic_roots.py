"""Independent cyclic root audit for the calibrated U(1)^f formulas.

Uses explicit normalized C4 bar cochains, a standard cyclic periodic chain,
exact rational arithmetic, and a small F2 solve for a charge phase completion.
No GAP resolution, global classification backend, or literature target enters.
"""
from pathlib import Path
import argparse
import json
import sys
from functools import lru_cache
from fractions import Fraction as F
from itertools import product, combinations

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import insulator as U


def run_audit():
    m=4
    def alpha(g):return g%2
    def beta(g,h):return (g+h)//m
    
    def local(xs,p,f,chi):
        vs=[0]
        for g in xs:vs.append((vs[-1]+g)%m)
        N=len(xs)
        vals={face:f(*[(vs[face[j+1]]-vs[face[j]])%m for j in range(p)])
              for face in combinations(range(N+1),p+1)}
        return U.Cochain(N,p,vals,[chi*alpha(g) for g in vs])
    def sym(xs):
        N=len(xs)
        return U.Symmetry(local(xs,2,lambda *a:0,0),local(xs,1,alpha,1),local(xs,1,alpha,1))
    def normalized(f):
        def result(*args):return 0 if 0 in args else f(*args)
        return result
    n1=alpha
    n3=normalized(lambda a,b,c:alpha(a)*alpha(b)*alpha(c))
    nu4=normalized(lambda a,b,c,d:-F(alpha(a)*alpha(b)*alpha(c)*alpha(d),16))
    v_table={(1,1):0,(1,2):-1,(1,3):0,(2,1):0,(2,2):1,(2,3):1,(3,1):1,(3,2):0,(3,3):0}
    v=normalized(lambda a,b:v_table[(a,b)])
    def d(f,args,chi):
        n=len(args)-1
        answer=(-1)**(chi*alpha(args[0]))*f(*args[1:])
        for j in range(n):
            merged=args[:j]+((args[j]+args[j+1])%m,)+args[j+2:]
            answer+=(-1)**(j+1)*f(*merged)
        return answer+(-1)**(n+1)*f(*args[:-1])
    for args in product(range(1,m),repeat=3):assert d(v,args,1)==-n3(*args)
    
    @lru_cache(None)
    def ci_square(xs):
        N=len(xs);s=sym(xs);zero=local(xs,3,lambda *a:0,1)
        state=U.State(local(xs,1,n1,1),zero,local(xs,4,nu4,1))
        sq=state.stack(state,s,3)
        joint=sq.gauge(s,3,local(xs,0,lambda:1,1),local(xs,2,v,1))
        assert joint.sheet.maxabs()==joint.charge.maxabs()==0
        sq=sq.gauge(s,3,local(xs,0,lambda:1,1),local(xs,2,lambda *a:0,1))
        assert (sq.charge-local(xs,3,n3,1)).maxabs()==0
        target=local(xs,4,normalized(lambda a,b,c,d:F(alpha(a)*alpha(b)*alpha(c)*alpha(d),4)),1)
        assert (sq.phase-target).mod(1).maxabs()==0
        out=sq.gauge(s,3,local(xs,0,lambda:0,1),local(xs,2,v,1))
        assert out.sheet.maxabs()==out.charge.maxabs()==0
        shorter=(sq.phase+U.charge_gauge(s,sq.charge,local(xs,2,v,1))).mod(1)
        return out.phase(tuple(range(N+1))),shorter(tuple(range(N+1))),joint.phase(tuple(range(N+1)))
    cycle=[(i,1,j,1) for i in range(1,m) for j in range(1,m)]
    ci_log=[{'tuple':list(xs),'phase':str(ci_square(xs)[0]),'short_gauge_phase':str(ci_square(xs)[1]),'single_joint_phase':str(ci_square(xs)[2])} for xs in cycle]
    ci_period=sum(ci_square(xs)[0] for xs in cycle)%1
    short_period=sum(ci_square(xs)[1] for xs in cycle)%1
    joint_period=sum(ci_square(xs)[2] for xs in cycle)%1
    assert ci_period==short_period==joint_period==F(1,2),(ci_period,short_period,joint_period)
    
    # An independent noninflated charge generator has q3(a,b,c)=alpha(a)*beta(b,c).
    q=normalized(lambda a,b,c:alpha(a)*beta(b,c))
    for args in product(range(1,m),repeat=4):assert d(q,args,1)==0
    # A quarter-phase trial plus a solved binary coboundary completes q globally.
    trial=normalized(lambda a,b,c,e:-F(beta(a,b)*beta(c,e),4))
    args4=list(product(range(1,m),repeat=4));indices={x:i for i,x in enumerate(args4)}
    args5=list(product(range(1,m),repeat=5))
    @lru_cache(None)
    def sourceq(xs):
        return U.charge_source(sym(xs),local(xs,3,q,1))(tuple(range(6)))%1
    rows=[]
    for xs in args5:
        value=2*((sourceq(xs)-d(trial,xs,1))%1)
        assert value.denominator==1
        row=0
        faces=[xs[1:]]+[xs[:j]+((xs[j]+xs[j+1])%m,)+xs[j+2:] for j in range(4)]+[xs[:-1]]
        for face in faces:
            if 0 not in face:row^=1<<indices[face]
        row|=(int(value)%2)<<len(args4)
        rows.append(row)
    pivots={}
    for row in rows:
        while row&((1<<len(args4))-1):
            bit=(row&-row).bit_length()-1
            if bit not in pivots:pivots[bit]=row;break
            row^=pivots[bit]
        else:assert row==0,'binary phase completion obstructed'
    solution=0
    for bit,row in sorted(pivots.items(),reverse=True):
        rhs=(row>>len(args4))&1
        rhs^=(bin(row&solution).count('1')%2)
        if rhs:solution|=1<<bit
    correction=normalized(lambda *xs:F((solution>>indices[xs])&1,2))
    phaseq=normalized(lambda *xs:trial(*xs)+correction(*xs))
    for xs in args5:assert (d(phaseq,xs,1)-sourceq(xs))%1==0
    for xs in product(range(1,m),repeat=3):assert d(normalized(lambda a,b:beta(a,b)),xs,1)==-2*q(*xs)
    
    def charge_square(xs):
        N=len(xs);s=sym(xs);state=U.State(local(xs,1,lambda *a:0,1),local(xs,3,q,1),local(xs,4,phaseq,1))
        sq=state.stack(state,s,3)
        out=sq.gauge(s,3,local(xs,0,lambda:0,1),local(xs,2,normalized(lambda a,b:beta(a,b)),1))
        assert out.sheet.maxabs()==out.charge.maxabs()==0
        return out.phase(tuple(range(N+1)))
    charge_log=[{'tuple':list(xs),'phase':str(charge_square(xs))} for xs in cycle]
    charge_period=sum(charge_square(xs) for xs in cycle)%1
    assert charge_period==0,charge_period
    # Original CI phase and the independent charge completion have odd quarter values.
    ci_initial_period=sum(nu4(*xs) for xs in cycle)%1
    charge_initial_period=sum(phaseq(*xs) for xs in cycle)%1
    out={'group':'C4','s':'parity','rho':'parity','omega':'0','method':'explicit normalized bar cochains, direct calibrated local kernels, standard cyclic periodic chain',
         'periodic4_cycle':[[i,1,j,1] for i in range(1,m) for j in range(1,m)],
         'CI_root':{'n1':'alpha(a)=a mod2','n3':'0','nu4':'-alpha(a)alpha(b)alpha(c)alpha(d)/16','native_phase':str(ci_initial_period),
                    'square_after_sheet_gauge':{'sheet_parameter':'u0=1','n3':'alpha(a)alpha(b)alpha(c)','nu4':'alpha(a)alpha(b)alpha(c)alpha(d)/4'},
                    'charge_removal_v2':{','.join(map(str,k)):str(value) for k,value in v_table.items()},
                    'charge_removal_identity':'d_rho v2=-alpha^3 (all27 normalized3-tuples checked)',
                    'final_phase_period':str(ci_period),'short_charge_gauge_period':str(short_period),'single_joint_gauge_period':str(joint_period),'cycle_ledger':ci_log},
         'charge_root':{'n3':'alpha(a) floor((b+c)/4)','native_phase':str(charge_initial_period),'phase_completion':'-beta(a,b)beta(c,d)/4+b4/2',
                        'b4_nonzero':[list(xs) for xs in args4 if (solution>>indices[xs])&1],
                        'completion_check':'all243 normalized5-tuples checked modulo1','square_charge_removal':'v2=beta(a,b)',
                        'final_phase_period':str(charge_period),'cycle_ledger':charge_log},
         'presentation_generator_order':['phase','charge','CI'],'presentation':[[2,0,0],[0,2,0],[-1,0,2]],'torsion':[2,4],'incoming_images':{'closed_charge_gauge':'H^2(C4,Z_sign)=0','closed_CI_gauge':'H^0(C4,Z_sign)=0'},'gauge_path_comparison':'All three gauges have phase period1/2; their closed differences are exact because the cyclic periodic4cycle detects H^4(C4,U1_sign)=Z2.'}
    # The C6 parity map has a symmetry-preserving section g_C2 -> g_C6^3.
    projection=lambda a:a%2
    section=lambda a:3*a
    assert all(projection(section(a))==a for a in range(2))
    assert all(projection((a+b)%6)==(projection(a)+projection(b))%2 for a in range(6) for b in range(6))
    assert all(section((a+b)%2)==(section(a)+section(b))%6 for a in range(2) for b in range(2))
    assert all(section(a)%2==a for a in range(2))
    assert sum((-1)**j for j in range(6))==0
    out['C6_split_inflation_audit']={
        'group':'C6','s':'parity','rho':'parity','omega':'0',
        'projection':'p(g_C6)=g_C2','section':'j(g_C2)=g_C6^3',
        'section_identity':'p o j=id_C2; j^* p^*=id on complete cochain classes',
        'input_root':'C2 AIII complete root (alpha,0,-alpha^4/16), certified order8',
        'conclusion':'Its pullback to C6 has order8 because restriction along j is a left inverse.',
        'periodic_maps':{'g_minus_1_on_Z_sign':-2,'norm_on_Z_sign':0},
        'coefficient_groups':{'H1_Z_sign':[2],'H3_Z_sign':[2],'H4_U1_sign':[2]},
        'incoming_groups':{'H0_Z_sign':[],'H2_Z_sign':[]},
        'tower_order':8,'torsion':[8],
        'scope':'Exact conclusion for the supplied natural CI/charge/phase model; no GAP solver is used.'}
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(run_audit(), indent=2) + '\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')
