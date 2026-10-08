#!/usr/bin/env python3
"""Export 3+1D backgrounds with verified short cocycles and section witnesses.

This translates saved finite multiplication/cocycle tables. It does not solve
classification, stacking, cohomology or any numerical physics problem.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREFIX='results/computed_examples/'
META={'D8':(4,0,-1),'D16':(8,0,-1),'Q8':(4,2,-1),'Q16':(8,4,-1),
      'M16':(8,0,5),'SD16':(8,0,3)}

def sha(data):return hashlib.sha256(data).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def saved_path(name):
    assert name.startswith(PREFIX)
    return HERE/name[len(PREFIX):]

def group_tex(values):
    if not values:return '0'
    return r'\times'.join((r'\mathbb Z' if n==0 else r'\mathbb Z_{'+str(n)+'}')+
        ('^{'+str(c)+'}' if c>1 else '') for n,c in Counter(values).items())

class Extension:
    def __init__(self,m):
        self.m=m;self.n=m['order'];self.p=[[a-1 for a in row] for row in m['productTable']];self.w=m['omega2']
        self.gens=[i-1 for i in m['generatorIndices']]
        reached={0};queue=[0]
        for g in queue:
            for h in self.gens:
                gh=self.p[g][h]
                if gh not in reached:reached.add(gh);queue.append(gh)
        assert len(reached)==self.n, m['id']
        assert all(m['s1'][self.p[g][h]]==(m['s1'][g]^m['s1'][h]) for g,h in itertools.product(range(self.n),repeat=2))
    def mul(self,a,b):return self.p[a[0]][b[0]],a[1]^b[1]^self.w[a[0]][b[0]]
    def power(self,a,n):
        if n<0:return self.power(self.inverse(a),-n)
        out=(0,0)
        for _ in range(n):out=self.mul(out,a)
        return out
    def inverse(self,a):
        b=next(b for b in range(self.n) if self.p[a[0]][b]==0)
        return b,a[1]^self.w[a[0]][b]
    def order(self,g):
        for k in range(1,self.n+1):
            if self.power((g,0),k)[0]==0:return k
        raise ValueError('No order')
    def section_check(self,coords,sections,formula):
        assert len(coords)==self.n and len(sections)==self.n
        for g,h in itertools.product(range(self.n),repeat=2):
            transported=self.w[g][h]^sections[g]^sections[h]^sections[self.p[g][h]]
            assert transported==formula(coords[g],coords[h])%2,(self.m['id'],g,h,transported)
        return dict(coordinates_by_element=[coords[i] for i in range(self.n)],
                    section_one_cochain=[sections[i] for i in range(self.n)],
                    identity='omega_display = omega_saved + delta(section_one_cochain)',
                    all_ordered_pairs_verified=self.n*self.n)

def character(bits,names):return '+'.join(x for x,b in zip(names,bits) if b) or '0'
def binary_square(name):return name+'^2' if '_' not in name else name+'^{2}'
def abelian(e):
    orders=[e.order(g) for g in e.gens]
    assert __import__('math').prod(orders)==e.n
    assert all(e.p[g][h]==e.p[h][g] for g,h in itertools.product(e.gens,repeat=2))
    d=len(orders);lifts=[(g,0) for g in e.gens]
    eps=[e.power(g,n)[1] for g,n in zip(lifts,orders)]
    cross=[[e.mul(lifts[j],lifts[i])[1]^e.mul(lifts[i],lifts[j])[1] for j in range(d)] for i in range(d)]
    coords={};sections={}
    for indices in itertools.product(*(range(n) for n in orders)):
        state=(0,0)
        for lift,k in zip(lifts,indices):state=e.mul(state,e.power(lift,k))
        assert state[0] not in coords
        coords[state[0]]=list(indices);sections[state[0]]=state[1]
    def formula(u,v):
        return sum(b*((i+j)//n) for b,i,j,n in zip(eps,u,v,orders))+sum(cross[i][j]*u[j]*v[i] for i in range(d) for j in range(i+1,d))
    witness=e.section_check(coords,sections,formula)
    names=['x' if d==1 else ('x' if i==0 else 'y') if d==2 else 'x_{'+str(i+1)+'}' for i in range(d)]
    terms=[binary_square(names[i]) if orders[i]==2 else r'\eta_{'+str(i+1)+'}' for i,b in enumerate(eps) if b]
    terms += [names[j]+r'\cup '+names[i] for i in range(d) for j in range(i+1,d) if cross[i][j]]
    signs=[e.m['s1'][g] for g in e.gens]
    assert all(e.m['s1'][g]==sum(b*c for b,c in zip(signs,coords[g]))%2 for g in range(e.n))
    return dict(kind='abelian',orders=orders,power_bits=eps,commutator_bits=cross,
        generator_names=['r_'+str(i+1) for i in range(d)],character_names=names,
        grading_tex=character(signs,names),omega_tex='+'.join(terms) or '0',
        cocycle_formula='sum_i epsilon_i floor((u_i+v_i)/m_i) + sum_(i<j) kappa_ij u_j v_i (mod 2)',
        witness=witness)

def metacyclic(e):
    m,k,a=META[e.m['group']];r,t=[(g,0) for g in e.gens]
    assert e.order(r[0])==m
    alpha=e.power(r,m);lhs=e.power(t,2);rhs=e.power(r,k)
    conj=e.mul(e.mul(t,r),e.inverse(t));power=e.power(r,a)
    assert alpha[0]==0 and lhs[0]==rhs[0] and conj[0]==power[0]
    bits=[alpha[1],lhs[1]^rhs[1],conj[1]^power[1]]
    coords={};sections={}
    for i,j in itertools.product(range(m),range(2)):
        state=e.mul(e.power(r,i),e.power(t,j))
        assert state[0] not in coords
        coords[state[0]]=[i,j];sections[state[0]]=state[1]
    def formula(u,v):
        i,j=u;h,l=v
        return bits[0]*((i+a**j*h+k*j*l)//m)+bits[1]*j*l+bits[2]*j*h
    witness=e.section_check(coords,sections,formula)
    signs=[e.m['s1'][g] for g in e.gens]
    assert all(e.m['s1'][g]==sum(b*c for b,c in zip(signs,coords[g]))%2 for g in range(e.n))
    return dict(kind='metacyclic',rotation_order=m,square_power=k,conjugation_power=a,
        lift_bits=bits,generator_names=['r','t'],character_names=['x','y'],
        grading_tex=character(signs,['x','y']),omega_tex=(r'\omega_{'+''.join(map(str,bits))+'}' if any(bits) else '0'),
        base_relations=f'r^{m}=1, t^2=r^{k}, trt^-1=r^{a}',
        extension_relations=f'R^{m}=f^alpha, T^2=R^{k} f^beta, TRT^-1=R^{a} f^gamma, f^2=1, f central',
        cocycle_formula='alpha floor((i+a^j i_prime+k*j*j_prime)/m) + beta*j*j_prime + gamma*j*i_prime (mod 2)',
        witness=witness)

def special(e):
    group=e.m['group'];nonzero=any(any(r) for r in e.w)
    if group=='A4':
        r,t=[(g,0) for g in e.gens]
        assert e.power(r,3)==e.power(t,3)==(0,0)
        assert e.power(e.mul(r,t),2)==(0,int(nonzero))
        return dict(kind='tetrahedral',grading_tex='0',omega_tex=r'\omega_{\rm tet}' if nonzero else '0',
            verified_lift_relations='R^3=T^3=1, (RT)^2=f' if nonzero else 'R^3=T^3=(RT)^2=1',
            definition='omega_tet is the central extension 1 -> C2^f -> SL(2,F3) -> A4 -> 1.',
            exact_saved_representative='inputModel.omega2')
    assert not nonzero
    if group=='SL(2,F3)':
        return dict(kind='binary_tetrahedral',grading_tex='0',omega_tex='0')
    if group=='Meta32_action3_t4r4':
        r,t=[(g,0) for g in e.gens]
        assert e.power(r,8)==(0,0) and e.power(t,4)==e.power(r,4)
        assert e.mul(e.mul(t,r),e.inverse(t))==e.power(r,3)
        return dict(kind='metacyclic32',grading_tex=character([e.m['s1'][g] for g in e.gens],['x','y']),omega_tex='0',
            base_relations='r^8=1, t^4=r^4, trt^-1=r^3',generator_names=['r','t'],character_names=['x','y'])
    if group=='CentralC8Q8':
        r,x,y=[(g,0) for g in e.gens]
        assert e.power(r,8)==(0,0) and e.power(x,2)==e.power(y,2)==e.power(r,4)
        assert e.mul(y,x)==e.mul(e.power(r,4),e.mul(x,y))
        assert e.mul(r,x)==e.mul(x,r) and e.mul(r,y)==e.mul(y,r)
        return dict(kind='central_product',grading_tex='x',omega_tex='0',
            base_relations='r central, r^8=1, u^2=v^2=r^4, vu=r^4 uv',
            generator_names=['r','u','v'],grading_on_named_generators=[1,0,0])
    raise ValueError(group)

def gb_tex(group):
    if group.startswith('C2^'):return r'\mathbb Z_2^{'+group.split('^')[1]+'}'
    if group=='V4':return r'\mathbb Z_2^2'
    if group.startswith('C') and group[1:].isdigit():return r'\mathbb Z_{'+group[1:]+'}'
    if group in ('C4xC2','C8xC2'):return r'\mathbb Z_{'+group[1]+'}'+r'\times\mathbb Z_2'
    return {'A4':'A_4','D8':'D_8','D16':'D_{16}','Q8':'Q_8','Q16':'Q_{16}','M16':'M_{16}',
        'SD16':r'\mathrm{SD}_{16}','Meta32_action3_t4r4':r'G_{32}',
        'CentralC8Q8':r'\mathbb Z_8\circ Q_8','SL(2,F3)':r'\mathrm{SL}(2,\mathbb F_3)'}[group]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    raw=(HERE/'index.json').read_bytes();index=json.loads(raw)
    groups=defaultdict(list)
    for r in index['cases']:
        if r['dimension']==3 and r['symmetry_kind']=='finite_internal':groups[r['deduplication_key']].append(r)
    rows=[]
    for records in groups.values():
        records.sort(key=lambda r: (r['id'].startswith('d3_E'),r['id']))
        r=records[0];path=saved_path(r['input_catalog']);payload=json.loads(path.read_text());m=payload['models'][0];e=Extension(m)
        if m['group'] in META:display=metacyclic(e)
        elif m['group'].startswith('C') and m['group']!='CentralC8Q8' or m['group']=='V4':display=abelian(e)
        else:display=special(e)
        bott=next((x['id'][4:] for x in records if x['id'].startswith('d3_E')),None)
        if bott is not None:
            p,q=map(int,bott)
            assert display['orders']==[2]*(p+q)
            assert display['power_bits']==[0]*p+[1]*q
            assert all(display['commutator_bits'][i][j]==1 for i in range(p+q) for j in range(i+1,p+q))
            assert r['grading_on_generators']==[1]*(p+q)
            display['bott_family']={'p':p,'q':q,'n':p+q,
                'grading':'sum_i x_i',
                'omega':'sum_(i=p+1)^(p+q) x_i^2 + sum_(i<j) x_j cup x_i'}
        layers={x['layer']:x['quotient_invariants'] for x in r['final_filtration']}
        row=dict(case=r['id'],alias_records=[x['id'] for x in records],group=m['group'],group_tex=gb_tex(m['group']),
            order=m['order'],input_model=m,input_catalog=r['input_catalog'],input_file_sha256=sha(path.read_bytes()),
            exact_input_sha256=r['exact_input_sha256'],deduplication_key=r['deduplication_key'],
            grading_on_generators=r['grading_on_generators'],background_display=display,
            final_layers={k:layers[k] for k in ('pip','majorana','complex_fermion','bosonic')},
            final_layers_tex={k:group_tex(layers[k]) for k in ('pip','majorana','complex_fermion','bosonic')},
            stacking_group=r['invariant_factors'],stacking_group_tex=group_tex(r['invariant_factors']),
            provenance=[dict(id=x['id'],origin=x['origin'],result=x['result'],result_sha256=x['sha256'],
                source_id=x['source_id']) for x in records],
            hand_calculation=r['id']=='d3_C2_w1_s1')
        rows.append(row)
    rows.sort(key=lambda r:(r['order'],r['group'],r['case']))
    assert len(rows)==77 and sum(len(r['alias_records']) for r in rows)==78
    result=dict(schema='fspt-symbolic-3d-backgrounds-v1',records=rows,record_count=77,named_record_count=78,
        additional_beyond_hand_calculation=76,catalog_sha256=sha(raw),
        convention='Group subscripts specify their order. Binary characters evaluate on the listed generators. Displayed cocycles and saved literal cocycles are related by the provided exact section one-cochain; final filtered groups are unchanged.',
        abelian_carry_definition='eta_i(u,v)=floor((u_i+v_i)/m_i) mod 2, x_i(u)=u_i mod 2.',
        metacyclic_cocycle_definition='For g=r^i t^j and h=r^i_prime t^j_prime, omega_(alpha,beta,gamma)(g,h)=alpha floor((i+a^j i_prime+k*j*j_prime)/m)+beta*j*j_prime+gamma*j*i_prime mod 2; 0<=i,i_prime<m and j,j_prime in {0,1}.',
        scope='A publication translation of all accepted finite internal 3+1D rows, with exact pairwise section checks; no recomputation of classification or stacking.')
    stream=io.StringIO(newline='');fields=['case','aliases','Gb','order','s1','omega2','lift_bits','pip','majorana','complex_fermion','bosonic','stacking_group','hand_calculation','input_catalog']
    w=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');w.writeheader()
    for r in rows:
        d=r['background_display'];w.writerow(dict(case=r['case'],aliases=';'.join(r['alias_records']),Gb=r['group_tex'],order=r['order'],
            s1=d['grading_tex'],omega2=d['omega_tex'],lift_bits=json.dumps(d.get('lift_bits',[])),
            **r['final_layers_tex'],stacking_group=r['stacking_group_tex'],hand_calculation=r['hand_calculation'],input_catalog=r['input_catalog']))
    outputs={'tables/internal_3d_symbolic.json':json.dumps(result,indent=2,sort_keys=True)+'\n','tables/internal_3d_symbolic.csv':stream.getvalue()}
    for name,data in outputs.items():
        target=HERE/name
        if args.check:assert target.read_text()==data,name
        else:target.write_text(data)
    print(json.dumps(dict(status='passed',distinct_3d_backgrounds=77,named_records=78,additional_beyond_hand=76,
        literal_pair_section_checks=sum(r['background_display'].get('witness',{}).get('all_ordered_pairs_verified',0) for r in rows))))

if __name__=='__main__':main()
