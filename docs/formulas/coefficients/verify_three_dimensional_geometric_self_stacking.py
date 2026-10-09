#!/usr/bin/env python3
"""Current 3+1D torsion-root diagonal, including the full reference phase.

The existing certificate supplies only arithmetic and the retained exact
coefficient kernels. All physical CF root bits below are in the NEW coordinate.
No source files or frozen coefficients are modified by this verification.
"""
from verify_three_dimensional_canonical_self_stacking import *

def run():
    data=json.loads(Path(__file__).with_name('three_dimensional_canonical_self_stacking.json').read_text())
    labels=[]
    def closed(name,degree):
        v={}
        for f in faces(degree):
            if f[0]==0:
                v[f]=Polynomial({1<<len(labels):1},2);labels.append({'field':name,'face':list(f)})
        for f in faces(degree):
            if f[0]:v[f]=sum(v[(0,)+f[:j]+f[j+1:]]for j in range(len(f)))
        return Cochain(degree,v)
    s,w=closed('s',1),closed('w',2);W=w+cup(s,s);A=cup(W,s)
    free_u=closed('u_root',2)
    u=Cochain(2,{f:free_u(f)+(A((0,)+f)if f[0]else 0)for f in faces(2)})
    def kappa(x):return square(x,2)+cup(s,square(x,1))+cup(w,x)
    psi=Cochain(4,{f:W(f[:3])*W((f[0],f[2],f[3]))*s(f[2:4])*s(f[3:5])for f in faces(4)})
    psi=psi+cup(cup(cup(W,W,1),s,1)+cup(s,cup(s,W,1)),s)
    B3=cup(u,u,1)
    q=kappa(u)+psi+B3.differential()
    free_c=closed('c_root',3)
    c=Cochain(3,{f:free_c(f)+(q((0,)+f)if f[0]else 0)for f in faces(3)})
    assert labels==data['variables']
    top=tuple(range(5));du=u.differential();checked_c=c+B3;dc=checked_c.differential()
    assert not(du-A)((0,1,2,3)) and not(c.differential()-q)(top)
    assert not(dc-kappa(u)-psi)(top)
    t=cup(u,u,1);t2=cup(s,s);N3=square(u,1)+cup(s,u)
    previous_N3=N3+du
    outpsi=cup(cup(W,W,1)+cup(s,W),s)
    assert not(N3.differential()+kappa(t2)+outpsi)(top)
    Bgamma=beta_open(u);b=Bgamma.binary()
    integer_u=u.lift(16);integer_w=w.lift(16);integer_W=W.lift(16);n=s.lift(16)
    alpha=ds(integer_W,s).divide(2)
    Bpsi=(A.lift(16)+signed_cup(integer_W,n,0,s,(1,1))).divide(2);B=Bgamma+Bpsi
    alpha_n=signed_cup(alpha,n,0,s,(1,1))
    def phase(a,den):
        value=a(top)if isinstance(a,Cochain)else a
        assert value.modulus>=den or den==2
        return Polynomial({m:v*(16//den)for m,v in value.terms.items()},16)
    def table(key):return Polynomial({m:1 for m in data[key]},2)
    phases={}
    phases['C']=phase(cup(checked_c,checked_c,2),2)
    phases['CGAMMA']=phase(cup(kappa(u),checked_c,3)+cup(previous_N3,kappa(t2),3),2)
    i,j,k,l,m=top
    extra_cf=dc(top)*(u((j,k,l))*du((i,j,l,m))+u((i,j,m))*du((j,k,l,m))+u((k,l,m))*du((i,j,k,m)))
    phases['CPSI']=phase(cup(psi,checked_c,3)+cup(previous_N3,outpsi,3),2)+phase(extra_cf,2)
    V=Cochain(4,{top:u(top[:3])*u(top[1:4])*u(top[2:5])*du((0,1,3,4))})
    gamma_half=(V+operation('123131',u,u,t)+cup(cup(u,du,2),u,1)+cup(u,t,1)+cup(u,cup(u,t,1),2)
                +cup(cup(u,u),cup(w,u),4)+cup(cup(u,u)+cup(w,u),cup(s,b),4)
                +cup(cup(w,s,1),u)+cup(t,cup(s,u),2)+cup(cup(s,s),u)+cup(s,b)+cup(s,cup(cup(s,u),u,2)))
    gamma_quarter=cup(Bgamma,Bgamma,2)+cup(integer_u,integer_u)-cup(integer_w,integer_u)
    phases['GAMMA']=phase(gamma_half,2)+phase(gamma_quarter,4)
    mixed_half=cup(B,integer_u.differential(),2)+ds(cup(Bgamma,integer_u,2),s)-cup(Bgamma,integer_u,1)
    mixed_quarter=(-cup(Bgamma,Bpsi,2)-cup(Bpsi,Bgamma,2)+cup(Bgamma,alpha_n,3)
                   +cup(integer_u-t2.lift(16),integer_u.differential(),1)
                   +cup(integer_u,t2.lift(16))+cup(t2.lift(16),integer_u)
                   +ds(A.lift(16)-t.lift(16),s))
    phases['GAMMAPSI']=phase(table('mixed_half_monomials'),2)+phase(mixed_half,2)+phase(mixed_quarter,4)
    second=(alpha-alpha.binary().lift(16)).divide(2).binary()
    psi_quarter=-cup(Bpsi,Bpsi,2)+cup(Bpsi,alpha_n,3)-cup(integer_w,t2.lift(16))-cup(second,s).lift(16)
    phases['PSI']=phase(table('pure_half_monomials')-cup(t2,t2)(top),2)+phase(psi_quarter,4)+phase(cup(integer_W,t2.lift(16)),8)
    face_phase=cup(w,u)+cup(u,u)+cup(du,u,1)+cup(previous_N3,du,2)
    K=phase(face_phase,2)
    phases['C']=phases['C']+K
    # Evaluate the frozen exact polynomial on the current checked CF root bits.
    replacements={i:checked_c(tuple(row['face'])) for i,row in enumerate(labels)
                  if row['field']=='c_root'}
    def transported_table(rows):
        out=Polynomial(0,16)
        for mask,coefficient in rows:
            touched=[i for i in replacements if mask&(1<<i)]
            if not touched:
                out=out+Polynomial({mask:coefficient},16);continue
            assert coefficient%8==0
            value=Polynomial({mask & ~sum(1<<i for i in touched):1},2)
            for i in touched:value=value*replacements[i]
            out=out+Polynomial({m:coefficient for m in value.terms},16)
        return out
    expected={name:transported_table(rows) for name,rows in data['reference_sector_phases_mod16'].items()}
    expected['C']=expected['C']+K
    residuals={name:len((value-expected[name]).terms) for name,value in phases.items()}
    total=sum(phases.values(),Polynomial(0,16))
    reference=transported_table(data['reference_total_phase_mod16'])+K
    total_res=len((total-reference).terms)
    assert not any(residuals.values()) and not total_res,(residuals,total_res)
    report={'status':'PASS','scope':'Current geometric coordinate; n1=s1, both backgrounds, arbitrary valid Majorana and CF completions',
        'independent_binary_variables':len(labels),'variables':labels,
        'method':'Exact binary and signed integer coefficient identities, with the previous polynomial transported to current free CF inputs',
        'sector_residual_coefficients':residuals,'total_residual_coefficients':total_res,
        'collected_current_phase_coefficients':len(total.terms),'phase_modulus':16,
        'current_total_phase_mod16':sorted(total.terms.items()),
        'current_sector_phases_mod16':{k:sorted(v.terms.items()) for k,v in phases.items()},
        'face_phase_binary_terms':len(face_phase(top).terms),
        'single_state_map':'checked n3 = n3 + checked n2 cup1 checked n2',
        'current_lower_output':'Sq1(checked n2) + s1 checked n2',
        'previous_phase_output':'N3 + d checked n2','integer_output_gauge_applied':False}
    return report

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=run()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('variables','current_total_phase_mod16','current_sector_phases_mod16')},indent=2))
