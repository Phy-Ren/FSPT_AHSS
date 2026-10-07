"""Exact full open-cochain coefficient proof of the diagonal lift-carry rewrite.

The source and product representative are unchanged. The public verifier is
used only for its standard cochain arithmetic; both displayed phase formulas
are transcribed independently below. No solver or sampled assignments occur.
"""
from pathlib import Path
from itertools import combinations
import importlib.util,json,hashlib,time
HERE=Path(__file__).resolve().parent
source=HERE/'verify_three_dimensional_canonical_self_stacking.py'
spec=importlib.util.spec_from_file_location('public_cochain_arithmetic',source)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
C,P,cup=p.Cochain,p.Polynomial,p.cup;top=tuple(range(5))

def phase(value,den):
    if isinstance(value,C):value=value(top)
    return P({m:(16//den)*a for m,a in value.terms.items()},16)

def old_gamma(u,w,s):
    A=u.differential();t=cup(u,u,1);B=p.beta_open(u);b=B.binary()
    V=C(4,{top:u((0,1,2))*u((1,2,3))*u((2,3,4))*A((0,1,3,4))})
    half=(V+p.operation('123131',u,u,t)+cup(cup(u,A,2),u,1)+cup(u,t,1)
          +cup(u,cup(u,t,1),2)+cup(cup(u,u),cup(w,u),4)
          +cup(cup(u,u)+cup(w,u),cup(s,b),4)+cup(cup(w,s,1),u)
          +cup(t,cup(s,u),2)+cup(cup(s,s),u)+cup(s,b)+cup(s,cup(cup(s,u),u,2)))
    quarter=cup(B,B,2)+cup(u.lift(16),u.lift(16))-cup(w.lift(16),u.lift(16))
    return phase(half,2)+phase(quarter,4)

def new_gamma(u,w,s):
    A=u.differential();B=p.beta_open(u)
    # The known intrinsic Majorana source; its differential completion is
    # deliberately not included in this physical contribution.
    O_gamma=cup(u,u)+cup(s,cup(u,u,1))+cup(w,u)
    half=(C(4,{top:u((0,1,2))*u((1,2,3))*u((2,3,4))*A((0,1,3,4))})
          +p.operation('123131',u,u,cup(u,u,1))
          +cup(cup(u,A,2),u,1)+cup(u,cup(u,u,1),1)
          +cup(u,cup(u,cup(u,u,1),1),2)+cup(u,u)+cup(cup(w,s,1),u)
          +cup(cup(u,u,1),cup(s,u),2)+cup(cup(s,s),u)
          +cup(s,cup(cup(s,u),u,2)))
    quarter=(cup(B,B,2)-cup(s,B.binary()).lift(16)
             -(O_gamma+cup(s,cup(u,A,2))).lift(16))
    return phase(half,2)+phase(quarter,4)

def build_fields(tower=False):
    labels=[]
    def closed(name,degree):
        vals={}
        for f in p.faces(degree):
            if f[0]==0:vals[f]=P({1<<len(labels):1},2);labels.append({'field':name,'face':list(f)})
        for f in p.faces(degree):
            if f[0]:vals[f]=sum(vals[(0,)+f[:j]+f[j+1:]]for j in range(len(f)))
        return C(degree,vals)
    s,w=closed('s',1),closed('w',2)
    if tower:
        ur=closed('u_root',2);A=cup(w+cup(s,s),s)
        u=C(2,{f:ur(f)+(A((0,)+f)if f[0]else 0)for f in p.faces(2)})
    else:
        vals={}
        for f in p.faces(2):vals[f]=P({1<<len(labels):1},2);labels.append({'field':'open_u','face':list(f)})
        u=C(2,vals)
    return u,w,s,labels

start=time.monotonic();u,w,s,labels=build_fields()
bridge=p.beta_open(u).binary()+p.square(u,1)
bridge_res={''.join(map(str,f)):len(bridge(f).terms)for f in p.faces(3)}
assert not any(bridge_res.values())
source_bridge=(cup(u,u)+cup(s,cup(u,u,1))+cup(w,u)+cup(s,cup(u,u.differential(),2))
               +cup(u,u)+cup(w,u)+cup(s,p.beta_open(u).binary()))
assert not source_bridge(top)
old,new=old_gamma(u,w,s),new_gamma(u,w,s)
assert not old-new
# An independent three-bit integer carry identity proves the only changed
# arithmetic step without reusing either cochain assembly above.
X,Y,Z=[P({1<<i:1},2)for i in range(3)]
left=phase(X*Y+(X+Y)*Z,2)+phase(X.lift(16)-Y.lift(16),4)
right=phase(X,2)+phase(Z.lift(16)-(X+Y+Z).lift(16),4)
assert not left-right
ut,wt,st,tower_labels=build_fields(True)
data=json.loads((HERE/'three_dimensional_canonical_self_stacking.json').read_text())
assert data['variables'][:len(tower_labels)]==tower_labels
frozen=P(dict(data['reference_sector_phases_mod16']['GAMMA']),16)
assert not new_gamma(ut,wt,st)-frozen
report={'status':'PASS','scope':'The complete previously designated 3D Majorana diagonal contribution for arbitrary open binary u2 and closed binary s1,omega2.',
 'independent_open_input_bits':len(labels),'open_input_labels':labels,
 'open_Bockstein_Sq1_face_residuals':bridge_res,'lower_source_bridge_residual':len(source_bridge(top).terms),
 'independent_three_bit_carry_residual':len((left-right).terms),
 'complete_open_phase_residual_mod16':len((old-new).terms),
 'frozen_canonical_torsion_sector_residual_mod16':len((new_gamma(ut,wt,st)-frozen).terms),
 'old_outer_terms':16,'new_half_terms':10,'new_quarter_terms':3,'new_outer_terms':13,
 'whole_binary_lift_interior_terms':2,'new_terms_with_lift_interior_counted':14,
 'standard_lower_source_retained':'O4_gamma[u]',
 'cochain_equality':'exact modulo one','source_changed':False,'new_gauge':False,'physical_sector_reassignment':False,
 'public_arithmetic_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'seconds':time.monotonic()-start}
(HERE/'OPEN_GAMMA_LIFT_REDUCTION_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k!='open_input_labels'},indent=2))
