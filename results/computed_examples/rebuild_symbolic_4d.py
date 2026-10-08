#!/usr/bin/env python3
"""Organize every saved 4+1D result and verify explicit background aliases.

This translates finite input tables and checks group/section identities. It does
not rerun a classification, stacking computation, or physical calibration.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import itertools
import json
import math
from pathlib import Path

from rebuild_symbolic_3d import Extension, abelian, character, group_tex

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
META = {
    'D10': (5,2,0,-1),
    'D6': (3,2,0,-1), 'D8': (4,2,0,-1), 'D12': (6,2,0,-1),
    'D16': (8,2,0,-1), 'D24': (12,2,0,-1), 'D32': (16,2,0,-1),
    'Q8': (4,2,2,-1), 'Q16': (8,2,4,-1), 'Q24': (12,2,6,-1),
    'Q32': (16,2,8,-1), 'M16': (8,2,0,5), 'SD16': (8,2,0,3),
    'SD32_action7': (16,2,0,7), 'C4rtC4_inv': (4,4,0,-1),
}
CATEGORIES = [
    ('cyclic', 'Cyclic groups'),
    ('abelian', 'Noncyclic abelian groups'),
    ('dihedral', 'Dihedral groups'),
    ('quaternion', 'Quaternion and dicyclic groups'),
    ('metacyclic', 'Other metacyclic groups'),
    ('products', 'Dihedral and quaternion groups times a cyclic factor'),
    ('polyhedral', 'Tetrahedral and octahedral groups'),
]


def canonical_json(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def group_name(m):
    """Normalize historical names using the actual order, never the name alone."""
    g, n = m['group'], m['order']
    if g == 'SL23':
        return 'SL(2,F3)'
    if g == 'V4' or g.startswith('C2^'):
        return 'x'.join(['C2'] * int(round(math.log2(n))))
    if g == 'S3' or g.startswith('D') and g[1:].isdigit():
        return 'D' + str(n)
    return g


def gb_tex(g):
    if g.startswith('C') and all(x[1:].isdigit() for x in g.split('x')):
        counts = Counter(int(x[1:]) for x in g.split('x'))
        return r'\times'.join(r'\mathbb Z_{'+str(n)+'}' + ('^{'+str(c)+'}' if c>1 else '') for n,c in counts.items())
    if g.startswith('D') and g[1:].isdigit():
        return 'D_{'+str(int(g[1:])//2)+'}'
    if g.startswith('Q') and g[1:].isdigit():
        return 'Q_{'+g[1:]+'}'
    return {
        'A4':'A_4', 'S4':'S_4', 'SL(2,F3)':r'\mathrm{SL}(2,\mathbb F_3)',
        'SD16':r'\mathrm{SD}_{16}', 'SD32_action7':r'\mathrm{SD}_{32}',
        'M16':'M_{16}', 'C4rtC4_inv':r'\mathbb Z_4\rtimes_{-1}\mathbb Z_4',
        'D8xC2':r'D_4\times\mathbb Z_2', 'Q8xC2':r'Q_8\times\mathbb Z_2',
    }[g]


def category(g):
    if g.startswith('C') and g[1:].isdigit(): return 'cyclic'
    if g.startswith('C') and all(x[1:].isdigit() for x in g.split('x')): return 'abelian'
    if g.startswith('D') and g[1:].isdigit(): return 'dihedral'
    if g.startswith('Q') and g[1:].isdigit(): return 'quaternion'
    if g in ('D8xC2','Q8xC2'): return 'products'
    if g in ('A4','S4','SL(2,F3)'): return 'polyhedral'
    assert g in META, g
    return 'metacyclic'


def verify_map(source, target, mapping, section):
    """omega_source = pullback(omega_target) + delta(section)."""
    n = source['order']
    assert target['order'] == n and sorted(mapping) == list(range(n))
    assert section[0] == 0
    for g,h in itertools.product(range(n), repeat=2):
        gh = source['productTable'][g][h]-1
        assert mapping[gh] == target['productTable'][mapping[g]][mapping[h]]-1
        assert source['omega2'][g][h] == (target['omega2'][mapping[g]][mapping[h]] ^ section[g] ^ section[h] ^ section[gh])
    assert all(source['s1'][g] == target['s1'][mapping[g]] for g in range(n))
    return {'source_to_target_elements_one_based':[i+1 for i in mapping],
            'section_one_cochain':section,
            'identity':'omega_source = phi^*omega_target + delta(section); s_source = phi^*s_target',
            'verified_ordered_pairs':n*n}


def metacyclic(e, g):
    m,n,k,a = META[g]
    r,t = [(i,0) for i in e.gens]
    assert e.n == m*n and e.order(r[0]) == m
    rpower=e.power(r,m); tpower=e.power(t,n); rk=e.power(r,k)
    conj=e.mul(e.mul(t,r),e.inverse(t)); ra=e.power(r,a)
    assert rpower[0]==0 and tpower[0]==rk[0] and conj[0]==ra[0]
    bits=[rpower[1], tpower[1]^rk[1], conj[1]^ra[1]]
    coords,sections={},{}
    for i,j in itertools.product(range(m),range(n)):
        v=e.mul(e.power(r,i),e.power(t,j))
        assert v[0] not in coords
        coords[v[0]]=[i,j]; sections[v[0]]=v[1]
    def formula(u,v):
        i,j=u; h,l=v; carry=(j+l)//n
        return (bits[0]*((i+a**j*h+k*carry)//m) + bits[1]*carry
                + bits[2]*h*sum(a**q for q in range(j)))
    witness=e.section_check(coords,sections,formula)
    signs=[e.m['s1'][i] for i in e.gens]
    assert all(e.m['s1'][i] == sum(x*y for x,y in zip(signs,coords[i]))%2 for i in range(e.n))
    return dict(kind='metacyclic', rotation_order=m, quotient_order=n,
        square_power=k, conjugation_power=a, lift_bits=bits,
        generator_names=['r','t'], character_names=['x','y'],
        grading_tex=character(signs,['x','y']), omega_tex=(r'\omega_{'+''.join(map(str,bits))+'}' if any(bits) else '0'),
        base_relations=f'r^{m}=1, t^{n}=r^{k}, trt^-1=r^{a}',
        extension_relations=f'R^{m}=f^{bits[0]}, T^{n}=R^{k} f^{bits[1]}, TRT^-1=R^{a} f^{bits[2]}',
        cocycle_formula='alpha floor((i+a^j h+k floor((j+l)/n))/m) + beta floor((j+l)/n) + gamma h sum_(q=0)^(j-1) a^q (mod 2)',
        witness=witness)


def direct_product(e,g):
    k=0 if g=='D8xC2' else 2
    r,t,z=[(i,0) for i in e.gens]
    assert e.order(r[0])==4
    rpower=e.power(r,4);tpower=e.power(t,2);rk=e.power(r,k)
    conj=e.mul(e.mul(t,r),e.inverse(t));ra=e.power(r,-1)
    zr=e.mul(z,r);rz=e.mul(r,z);zt=e.mul(z,t);tz=e.mul(t,z)
    assert rpower[0]==0 and tpower[0]==rk[0] and conj[0]==ra[0]
    assert zr[0]==rz[0] and zt[0]==tz[0] and e.power(z,2)[0]==0
    bits=[rpower[1],tpower[1]^rk[1],conj[1]^ra[1],e.power(z,2)[1],zr[1]^rz[1],zt[1]^tz[1]]
    coords,sections={},{}
    for i,j,v in itertools.product(range(4),range(2),range(2)):
        state=e.mul(e.mul(e.power(r,i),e.power(t,j)),e.power(z,v))
        assert state[0] not in coords
        coords[state[0]]=[i,j,v];sections[state[0]]=state[1]
    def formula(u,v):
        i,j,q=u;h,l,p=v
        return bits[0]*((i+(-1)**j*h+k*j*l)//4)+bits[1]*j*l+bits[2]*j*h+bits[3]*q*p+bits[4]*q*h+bits[5]*q*l
    witness=e.section_check(coords,sections,formula)
    signs=[e.m['s1'][i] for i in e.gens]
    assert all(e.m['s1'][i]==sum(a*b for a,b in zip(signs,coords[i]))%2 for i in range(e.n))
    return dict(kind='metacyclic_times_c2', rotation_order=4, square_power=k,
        lift_bits=bits,generator_names=['r','t','z'],character_names=['x','y','z'],
        grading_tex=character(signs,['x','y','z']),
        omega_tex=r'\omega_{'+''.join(map(str,bits))+'}' if any(bits) else '0',
        base_relations=f'r^4=1, t^2=r^{k}, trt^-1=r^-1; z^2=1, z central',
        extension_relations=f'R^4=f^{bits[0]}, T^2=R^{k} f^{bits[1]}, TRT^-1=R^-1 f^{bits[2]}, Z^2=f^{bits[3]}, ZR=f^{bits[4]}RZ, ZT=f^{bits[5]}TZ',
        cocycle_formula='alpha floor((i+(-1)^j h+k j l)/4)+beta j l+gamma j h+delta q p+epsilon q h+zeta q l (mod 2)',witness=witness)


def polyhedral(e,g):
    r,t=[(i,0) for i in e.gens]
    if g=='A4':
        # Odd-order generator lifts have unique order-three normalizations.
        r=(r[0],e.power(r,3)[1]);t=(t[0],e.power(t,3)[1])
        bit=e.power(e.mul(r,t),2)[1]
        assert e.power(r,3)==e.power(t,3)==(0,0)
        return dict(kind='tetrahedral',generator_names=['r','t'],grading_tex='0',
            omega_tex=r'\omega_{\rm tet}' if bit else '0',lift_bits=[bit],
            base_relations='r^3=t^3=(rt)^2=1',
            extension_relations=f'R^3=T^3=1, (RT)^2=f^{bit}',
            generator_lift_bits=[r[1],t[1]],
            definition='omega_tet is the binary tetrahedral central extension of A4.',
            exact_saved_representative='input_model.omega2')
    if g=='S4':
        # Fix the odd relation (RT)^3=1; squares/fourth powers are unaffected.
        t=(t[0],e.power(e.mul(r,t),3)[1])
        bits=[e.power(r,2)[1],e.power(t,4)[1]]
        assert e.power(e.mul(r,t),3)==(0,0)
        signs=[e.m['s1'][i] for i in e.gens];assert signs[0]==signs[1]
        return dict(kind='octahedral',generator_names=['r','t'],
            grading_tex='x' if signs[0] else '0',lift_bits=bits,
            omega_tex=r'\omega_{'+''.join(map(str,bits))+'}' if any(bits) else '0',
            base_relations='r^2=t^4=(rt)^3=1',
            extension_relations=f'R^2=f^{bits[0]}, T^4=f^{bits[1]}, (RT)^3=1',
            generator_lift_bits=[r[1],t[1]],
            character_definition='x(r)=x(t)=1 is the sign character.',
            exact_saved_representative='input_model.omega2')
    assert g=='SL(2,F3)' and not any(map(any,e.w)) and not any(e.m['s1'])
    return dict(kind='binary_tetrahedral',generator_names=['r','t'],grading_tex='0',omega_tex='0',
        extension_relations='G_f = C2^f x SL(2,F3)',exact_saved_representative='input_model.omega2')


def display(m):
    e=Extension(m);g=group_name(m)
    if category(g) in ('cyclic','abelian'):
        out=abelian(e)
        out['extension_relations']='; '.join([f'R{i+1}^{n}=f^{b}' for i,(n,b) in enumerate(zip(out['orders'],out['power_bits']))]+[f'R{j+1}R{i+1}=f^{out["commutator_bits"][i][j]}R{i+1}R{j+1}' for i in range(len(e.gens)) for j in range(i+1,len(e.gens))])
    elif g in META: out=metacyclic(e,g)
    elif g in ('D8xC2','Q8xC2'):out=direct_product(e,g)
    else:out=polyhedral(e,g)
    out['grading_on_named_generators']=[m['s1'][i-1] for i in m['generatorIndices']]
    return out


def elementary_alias(source,target):
    """Find an exact graded central-extension isomorphism for Bott aliases."""
    es,et=Extension(source),Extension(target)
    n=source['order'];assert target['order']==n
    d=len(es.gens);assert 2**d==n
    ss=[es.m['s1'][g] for g in es.gens]
    qs=[es.power((g,0),2)[1] for g in es.gens]
    bs=[[es.mul((g,0),(h,0))[1]^es.mul((h,0),(g,0))[1] for h in es.gens] for g in es.gens]
    choices=[[v for v in range(1,n) if et.m['s1'][v]==ss[i] and et.power((v,0),2)[1]==qs[i]] for i in range(d)]
    def find(images,span):
        i=len(images)
        if i==d:return images
        for v in choices[i]:
            if v in span:continue
            if any((et.mul((u,0),(v,0))[1]^et.mul((v,0),(u,0))[1]) != bs[j][i] for j,u in enumerate(images)):continue
            result=find(images+[v],span | {et.p[u][v] for u in span})
            if result is not None:return result
        return None
    images=find([],{0})
    if images is None:return None
    mapping=[None]*n;section=[None]*n
    for bits in itertools.product(range(2),repeat=d):
        a,b=(0,0),(0,0)
        for i,bit in enumerate(bits):
            if bit:a=es.mul(a,(es.gens[i],0));b=et.mul(b,(images[i],0))
        mapping[a[0]]=b[0];section[a[0]]=a[1]^b[1]
    return verify_map(source,target,mapping,section)


def identity_map(a,b):
    assert all(a[k]==b[k] for k in ('order','productTable','s1','omega2'))
    return verify_map(a,b,list(range(a['order'])),[0]*a['order'])


def split_section(m):
    """Solve delta(lambda)=omega over F2, with normalized lambda(1)=0."""
    basis={}
    for g,h in itertools.product(range(m['order']),repeat=2):
        gh=m['productTable'][g][h]-1
        row=(1<<g)^(1<<h)^(1<<gh)
        row &= ~1
        rhs=m['omega2'][g][h]
        while row:
            pivot=row.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(row,rhs);break
            other,value=basis[pivot];row^=other;rhs^=value
        else:
            if rhs:return None
    solution=0
    for pivot,(row,rhs) in sorted(basis.items()):
        if bin(row & solution).count('1')%2 != rhs:solution |= 1<<pivot
    section=[(solution>>g)&1 for g in range(m['order'])]
    assert all((section[g]^section[h]^section[m['productTable'][g][h]-1])==m['omega2'][g][h]
               for g,h in itertools.product(range(m['order']),repeat=2))
    return section


def group_word_tree(e):
    seen={0};queue=[0];tree=[]
    for g in queue:
        for i,h in enumerate(e.gens):
            gh=e.p[g][h]
            if gh not in seen:
                seen.add(gh);queue.append(gh);tree.append((g,i,gh))
    assert len(seen)==e.n
    return tree


def element_map(base,target,images,tree):
    phi=[None]*base.n;phi[0]=0
    for parent,i,g in tree:phi[g]=target.p[phi[parent]][images[i]]
    if len(set(phi))!=base.n:return None
    if not all(phi[base.p[g][h]]==target.p[phi[g]][images[i]]
               for g in range(base.n) for i,h in enumerate(base.gens)):return None
    return phi


def automorphism_images(e,tree):
    orders=[e.order(g) for g in range(e.n)]
    candidates=[[h for h in range(1,e.n) if orders[h]==orders[g]] for g in e.gens]
    pair_orders={(i,j):orders[e.p[g][h]] for i,g in enumerate(e.gens) for j,h in enumerate(e.gens) if i<j}
    for images in itertools.product(*candidates):
        if any(orders[e.p[images[i]][images[j]]]!=value for (i,j),value in pair_orders.items()):continue
        if element_map(e,e,images,tree) is not None:yield images


def extension_signature(e,images,g,kind):
    """Complete defining-relator signs, modulo changes of generator lifts."""
    lifts=[(i,0) for i in images]
    signs=tuple(e.m['s1'][i] for i in images)
    if kind in ('cyclic','abelian'):
        orders=[e.order(i) for i in images]
        power=[e.power(v,n)[1] if n%2==0 else 0 for v,n in zip(lifts,orders)]
        cross=[e.mul(lifts[j],lifts[i])[1]^e.mul(lifts[i],lifts[j])[1]
               for i in range(len(images)) for j in range(i+1,len(images))]
        return signs+tuple(power+cross)
    if g in META or g in ('D8xC2','Q8xC2'):
        m,n,k,a=META[g] if g in META else (4,2,0 if g=='D8xC2' else 2,-1)
        r,t=lifts[:2]
        bits=[e.power(r,m)[1] if m%2==0 else 0,
              e.power(t,n)[1]^e.power(r,k)[1],
              e.mul(e.mul(t,r),e.inverse(t))[1]^e.power(r,a)[1]]
        if len(lifts)==3:
            z=lifts[2]
            bits += [e.power(z,2)[1],e.mul(z,r)[1]^e.mul(r,z)[1],e.mul(z,t)[1]^e.mul(t,z)[1]]
        return signs+tuple(bits)
    r,t=lifts
    if g=='A4':return signs+(e.power(e.mul(r,t),2)[1],)
    if g=='S4':return signs+(e.power(r,2)[1],e.power(t,4)[1])
    assert g=='SL(2,F3)' and not any(map(any,e.w))
    return signs


def verify_unique_backgrounds(rows):
    """Enumerate all automorphisms and compare complete extension signatures."""
    families=defaultdict(list)
    for row in rows:families[row['group']].append(row)
    audit=[]
    for g,group_rows in sorted(families.items()):
        base=Extension(group_rows[0]['input_model']);tree=group_word_tree(base)
        autos=list(automorphism_images(base,tree));assert autos
        signatures={}
        for row in group_rows:
            e=Extension(row['input_model'])
            phi=element_map(base,e,e.gens,tree)
            assert phi is not None,(g,row['background_id'])
            signature=min(extension_signature(e,[phi[i] for i in images],g,row['category']) for images in autos)
            assert signature not in signatures,(g,row['background_id'],signatures.get(signature))
            signatures[signature]=row['background_id']
            row['graded_extension_orbit_signature']=list(signature)
        audit.append(dict(group=g,bosonic_order=base.n,automorphism_count=len(autos),
            checked_backgrounds=len(group_rows),distinct_extension_signatures=len(signatures)))
    return audit


def verify_distinct_quotient_groups(rows):
    """Exclude hidden group-name aliases before comparing background orbits."""
    groups={r['group']:Extension(r['input_model']) for r in rows}
    data={g:(e.n,tuple(sorted(Counter(e.order(i) for i in range(e.n)).items())),
             sum(all(e.p[i][j]==e.p[j][i] for j in range(e.n)) for i in range(e.n)))
          for g,e in groups.items()}
    detailed=[]
    for (ga,a),(gb,b) in itertools.combinations(sorted(groups.items()),2):
        if data[ga]!=data[gb]:continue
        if len(a.gens)>len(b.gens):ga,gb,a,b=gb,ga,b,a
        tree=group_word_tree(a);orders=[b.order(i) for i in range(b.n)]
        choices=[[h for h in range(1,b.n) if orders[h]==a.order(g)] for g in a.gens]
        count=0
        for images in itertools.product(*choices):
            count+=1
            assert element_map(a,b,images,tree) is None,(ga,gb,images)
        detailed.append(dict(groups=[ga,gb],generator_image_tuples_excluded=count))
    return dict(quotient_groups=len(groups),pair_count=len(groups)*(len(groups)-1)//2,
        cheap_invariants='group order, element-order multiset, center order',
        remaining_pairs_verified_by_all_generator_images=detailed)


def load_inputs(records):
    return {r['id']:json.loads((ROOT/r['input_catalog']).read_text())['models'][0] for r in records}


def build():
    index_bytes=(HERE/'index.json').read_bytes();index=json.loads(index_bytes)
    records=[r for r in index['cases'] if r['dimension']==4 and r['symmetry_kind']=='finite_internal']
    by_id={r['id']:r for r in records};inputs=load_inputs(records)
    old=ROOT/'results/complete_formulas'
    canonical={m['id']:m for m in json.loads((old/'catalog/models.json').read_text())['models']}
    old_rows=list(csv.DictReader((old/'finite_4d_canonical_202.csv').open()))
    transformations=json.loads((old/'catalog/historical_transformations.json').read_text())
    names=json.loads((old/'catalog/historical_aliases.json').read_text())
    rows={}
    def add(key,m,r):
        d=display(m);layers={x['layer']:x['quotient_invariants'] for x in r['final_filtration']}
        rows[key]=dict(background_id=key,representative_record=r['id'],group=group_name(m),group_tex=gb_tex(group_name(m)),
            category=category(group_name(m)),bosonic_order=m['order'],fermionic_order=2*m['order'],
            antiunitary=any(m['s1']),input_model=m,background_display=d,
            final_layers={k:layers[k] for k in ('pip','majorana','complex_fermion','bosonic')},
            final_layers_tex={k:group_tex(layers[k]) for k in ('pip','majorana','complex_fermion','bosonic')},
            stacking_group=r['invariant_factors'],stacking_group_tex=group_tex(r['invariant_factors']),
            aliases=[],intro_rows=[])
        section=split_section(m)
        rows[key]['fermion_extension']='split' if section is not None else 'nonsplit'
        rows[key]['splitting_section']=section
    for row in old_rows:
        add(row['canonical_model'],canonical[row['canonical_model']],by_id[row['record_id']])
    for r in records:
        if r['origin']!='prior_complete_release':add(r['model'],inputs[r['id']],r)
    assert len(rows)==568,len(rows)
    maps=[]
    for r in records:
        original=inputs[r['id']]
        if 'bott_controls' in r['collections']:
            matches=[]
            for key,row in rows.items():
                if row['group']==group_name(original):
                    witness=elementary_alias(original,row['input_model'])
                    if witness is not None:matches.append((key,witness))
            assert len(matches)<=1,(r['id'],[k for k,w in matches])
            if matches:
                key,witness=matches[0]
            else:
                key=r['model'];add(key,original,r)
                witness=identity_map(original,original)
        elif r['model'] in transformations:
            trans=transformations[r['model']];key=trans['canonical_id'];target=rows[key]['input_model']
            phi=[i-1 for i in trans['canonical_to_historical_element_indices']]
            lam=trans['omega_coboundary_primitive']
            verify_map(target,original,phi,lam)
            inverse=[phi.index(i) for i in range(len(phi))]
            witness=verify_map(original,target,inverse,[lam[i] for i in inverse])
        else:
            key=names.get(r['model'],r['model'])
            witness=identity_map(original,rows[key]['input_model'])
        row=rows[key]
        assert row['stacking_group']==r['invariant_factors'],r['id']
        assert row['final_layers']=={x['layer']:x['quotient_invariants'] for x in r['final_filtration']},r['id']
        row['aliases'].append(r['id'])
        maps.append(dict(record=r['id'],background_id=key,input_catalog=r['input_catalog'],
            exact_input_sha256=r['exact_input_sha256'],result=r['result'],result_sha256=r['sha256'],
            origin=r['origin'],collections=r['collections'],background_isomorphism=witness))
    historical=json.loads((ROOT/'results/finite_examples/collections/four_dimensional_43.json').read_text())
    by_record={m['record']:m['background_id'] for m in maps}
    intro=[]
    for entry in historical:
        key=by_record['d4_'+entry['model_id']]
        item=dict(table=entry['table'],row=entry['row'],historical_model=entry['model_id'],background_id=key)
        rows[key]['intro_rows'].append(item);intro.append(item)
    assert len(intro)==43 and len({r['background_id'] for r in intro})==43
    source_collections=[]
    source_sets=[('historical_53',ROOT/'results/finite_examples/models.json',
                  ['d4_'+m['id'] for m in json.loads((ROOT/'results/finite_examples/models.json').read_text())['models']]),
                 ('original_43',ROOT/'results/finite_examples/collections/four_dimensional_43.json',
                  ['d4_'+m['model_id'] for m in historical]),
                 ('prior_complete_release',old/'index.json',
                  [r['id'] for r in records if r['origin']=='prior_complete_release']),
                 ('canonical_202',old/'finite_4d_canonical_202.csv',
                  [r['record_id'] for r in old_rows]),
                 ('october_2_supplement',ROOT/'results/complete_formulas_20261002_supplement/index.json',
                  [r['id'] for r in json.loads((ROOT/'results/complete_formulas_20261002_supplement/index.json').read_text())['cases'] if r['dimension']==4]),
                 ('later_campaign',HERE/'index.json',[r['id'] for r in records if r['origin']=='finite_campaign_398']),
                 ('bott_controls',HERE/'index.json',[r['id'] for r in records if 'bott_controls' in r['collections']]),
                 ('separate_controls',HERE/'index.json',[r['id'] for r in records if r['origin']=='additional_calibration_controls'])]
    for label,path,ids in source_sets:
        assert all(i in by_record for i in ids),label
        source_collections.append(dict(collection=label,source=str(path.relative_to(ROOT)),source_sha256=sha(path.read_bytes()),
            named_records=len(ids),distinct_backgrounds=len({by_record[i] for i in ids}),
            record_ids=ids,background_ids=sorted({by_record[i] for i in ids}),uncovered_records=[]))
    result_rows=sorted(rows.values(),key=lambda r:([k for k,v in CATEGORIES].index(r['category']),r['bosonic_order'],r['group'],r['background_id']))
    quotient_audit=verify_distinct_quotient_groups(result_rows)
    orbit_audit=verify_unique_backgrounds(result_rows)
    families=[]
    for key,title in CATEGORIES:
        subset=[r for r in result_rows if r['category']==key]
        families.append(dict(category=key,title=title,backgrounds=len(subset),named_records=sum(len(r['aliases']) for r in subset),
            unitary=sum(not r['antiunitary'] for r in subset),antiunitary=sum(r['antiunitary'] for r in subset),
            split=sum(r['fermion_extension']=='split' for r in subset),nonsplit=sum(r['fermion_extension']=='nonsplit' for r in subset),
            intro=sum(bool(r['intro_rows']) for r in subset),appendix=sum(not r['intro_rows'] for r in subset)))
    return dict(schema='fspt-symbolic-4d-backgrounds-v1',catalog_sha256=sha(index_bytes),named_record_count=len(records),
        literal_input_count=len({r['deduplication_key'] for r in records}),background_count=len(result_rows),
        intro_count=43,additional_backgrounds=len(result_rows)-43,
        group_convention='D_m has order 2m; Q_N has order N. Every group is G_b. G_f is its central extension by C2^f and has twice the stated bosonic order.',
        deduplication='202 canonical baseline backgrounds plus364 later campaign backgrounds and2 separately completed controls, with uncovered Bott backgrounds added explicitly. Historical representative changes are verified using saved isomorphisms and section cochains; Bott comparisons use independently constructed exact graded central-extension isomorphisms.',
        records=result_rows,record_coverage=maps,intro_coverage=intro,categories=families,orbit_uniqueness=orbit_audit,quotient_group_uniqueness=quotient_audit,source_collections=source_collections,
        nonclassification_calibrations=[dict(name=k,path='results/finite_examples/calibrations/'+k+'.json') for k in ('q8_d3_detectors','v4_euler','d8_reflection_square_d4','c2_exact_phase','spinc_t2_cp2')])


def csv_text(rows, symbolic=False):
    fields=['background_id','representative_record','aliases','Gb','bosonic_order','fermionic_order',
            's1','omega2','fermion_extension','extension_parameters','pip','majorana','complex_fermion',
            'bosonic','stacking_group','intro_table_rows']
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');writer.writeheader()
    for row in rows:
        d=row['background_display'];layers=row['final_layers_tex' if symbolic else 'final_layers']
        item=dict(background_id=row['background_id'],representative_record=row['representative_record'],
            aliases=';'.join(row['aliases']),Gb=row['group_tex' if symbolic else 'group'],
            bosonic_order=row['bosonic_order'],fermionic_order=row['fermionic_order'],s1=d['grading_tex'],omega2=d['omega_tex'],
            fermion_extension=row['fermion_extension'],extension_parameters=d.get('lift_bits',d.get('power_bits',[])),
            **layers,stacking_group=row['stacking_group_tex' if symbolic else 'stacking_group'],
            intro_table_rows=';'.join(str(x['table'])+':'+str(x['row']) for x in row['intro_rows']))
        writer.writerow({k:json.dumps(v,separators=(',',':')) if isinstance(v,list) else v for k,v in item.items()})
    return stream.getvalue()


def family_page(key,title,rows):
    lines=['# 4+1D: '+title,'',
        f'{len(rows)} distinct computed symmetry backgrounds. Every background appears in exactly one family table.',
        '', '[All families](../internal_4d.md) · [Background definitions](../../FOUR_DIMENSIONAL_BACKGROUNDS.md) · [CSV]('+key+'.csv)',
        '', 'Each heading specifies the bosonic quotient and its order. The full fermionic symmetry has twice that order; the final column is the stacking group of phases.',
        'The layer columns are final filtration quotients in the order p+ip, Majorana, complex fermion and bosonic.',
        'Historical names and section choices are attached to each background in the [coverage ledger](../../COVERAGE_4D.json).', '']
    grouped=defaultdict(list)
    for row in rows:grouped[row['group']].append(row)
    for group,subset in grouped.items():
        first=subset[0]
        lines += [f'## $G_b={first["group_tex"]}$, order {first["bosonic_order"]}', '',
            '| Background | $s_1$ | $\\omega_2$ | Extension | p+ip | Majorana | CF | Bosonic | Stacking group |',
            '|---|---|---|---|---|---|---|---|---|']
        for row in sorted(subset,key=lambda r:(r['antiunitary'],r['background_id'])):
            d=row['background_display'];vals=[f'[{row["background_id"]}](../../inputs/{row["representative_record"]}.json)',
                '$'+d['grading_tex']+'$','$'+d['omega_tex']+'$',row['fermion_extension']]
            vals += ['$'+row['final_layers_tex'][k]+'$' for k in ('pip','majorana','complex_fermion','bosonic')]
            vals += ['$'+row['stacking_group_tex']+'$']
            lines.append('| '+' | '.join(vals)+' |')
        lines.append('')
    return '\n'.join(lines)


BACKGROUND_DEFINITIONS = r'''# 4+1D finite symmetry backgrounds

An example is specified by $(G_b,s_1,[\omega_2])$. Here $G_b$ is the
bosonic quotient, $s_1$ identifies its antiunitary elements, and
$\omega_2$ defines the central extension by fermion parity $f$.
In every presentation below, $f^2=1$ and $f$ is central and unitary.
The order of $G_f$ is twice the order of $G_b$; neither order is the
stacking group printed in the last column.

The [seven family tables](tables/internal_4d.md) contain each background
once. Distinct names for an isomorphic graded central extension are
provenance aliases. The exact input arrays, group isomorphism, and section
one-cochain for every retained calculation are in the
[coverage ledger](COVERAGE_4D.json) and [symbolic table](tables/internal_4d_symbolic.json).
Changing section means $\omega_2\mapsto\omega_2+d\lambda$; it does not
create another physical example. The split column is determined by solving
this equation, rather than by asking whether the saved cocycle array is zero.

## Cyclic and noncyclic abelian groups

Use ordered generators $r_i$ of orders $m_i$, and write
$g=\prod_i r_i^{u_i}$ with $0\leq u_i<m_i$. Put

$$
\eta_i(g,h)=\left\lfloor\frac{u_i+v_i}{m_i}\right\rfloor\bmod2,
\qquad x_i(g)=u_i\bmod2.
$$

Only even-order factors carry a nonzero binary character. For $m_i=2$,
$\eta_i=x_i^2$. The two-generator tables abbreviate $x_1,x_2$ as $x,y$;
one-generator tables use $x$. The index on $\eta_i$ always refers to the
ordered factors printed in $G_b$.

Every displayed cocycle has the form

$$
\omega_2=\sum_i\epsilon_i\eta_i+
\sum_{i<j}\kappa_{ij}x_j\cup x_i.
$$

It specifies $R_i^{m_i}=f^{\epsilon_i}$ and
$R_jR_i=f^{\kappa_{ij}}R_iR_j$. The generator grading determines
$s_1=\sum_i s_1(r_i)x_i$. The saved section witnesses verify the displayed
cocycle on every ordered pair of elements.

## Dihedral, quaternion and other metacyclic groups

In these tables **$D_m$ has order $2m$**, while $Q_N$ has order $N$.
Use

$$
G_b=\langle r,t\mid r^m=1,\ t^n=r^k,\ trt^{-1}=r^a\rangle.
$$

| Group | $(m,n,k,a)$ |
|---|---|
| $D_m$ | $(m,2,0,-1)$ |
| $Q_N$ | $(N/2,2,N/4,-1)$ |
| $\mathrm{SD}_{16}$ | $(8,2,0,3)$ |
| $\mathrm{SD}_{32}$ | $(16,2,0,7)$ |
| $M_{16}$ | $(8,2,0,5)$ |
| $\mathbb Z_4\rtimes_{-1}\mathbb Z_4$ | $(4,4,0,-1)$ |

The subscript in $\omega_{\alpha\beta\gamma}$ gives the three signs in

$$
R^m=f^\alpha,\qquad T^n=R^k f^\beta,\qquad
TRT^{-1}=R^a f^\gamma.
$$

This also gives an explicit cocycle. For $g=r^it^j$ and
$g'=r^{i'}t^{j'}$ with $0\leq i,i'<m$, $0\leq j,j'<n$, it is

$$
\omega_{\alpha\beta\gamma}(g,g')
=\alpha\left\lfloor\frac{i+a^j i'+k\lfloor(j+j')/n\rfloor}{m}\right\rfloor
+\beta\left\lfloor\frac{j+j'}{n}\right\rfloor
+\gamma i'\sum_{q=0}^{j-1}a^q\pmod2.
$$

The sum is zero for $j=0$. Characters satisfy $x(r)=1,x(t)=0$ and
$y(r)=0,y(t)=1$ whenever allowed by the relations. For odd $m$, only
$y$ is used. The table's $s_1$ is the corresponding combination.

## Products with a cyclic factor

For $D_4\times\mathbb Z_2$ and $Q_8\times\mathbb Z_2$, use $r,t,z$,
with $r^4=z^2=1$, $t^2=r^k$, $trt^{-1}=r^{-1}$ and $z$ central;
$k=0$ for $D_4$ and $k=2$ for $Q_8$.
The six bits in $\omega_{\alpha\beta\gamma\delta\epsilon\zeta}$ mean

$$
\begin{aligned}
R^4&=f^\alpha,&T^2&=R^k f^\beta,&TRT^{-1}&=R^{-1}f^\gamma,\\
Z^2&=f^\delta,&ZR&=f^\epsilon RZ,&ZT&=f^\zeta TZ.
\end{aligned}
$$

For $g=r^it^jz^q$ and $g'=r^{i'}t^{j'}z^{q'}$, the cocycle is

$$
\omega_2(g,g')=
\alpha\left\lfloor\frac{i+(-1)^ji'+kjj'}{4}\right\rfloor
+\beta jj'+\gamma ji'+\delta qq'+\epsilon qi'+\zeta qj'\pmod2.
$$

The characters $x,y,z$ in the grading column evaluate on $r,t,z$,
respectively. The character $z$ and generator $z$ are distinguished by
whether an element or a cochain is required.

## Tetrahedral and octahedral groups

For $A_4$, choose $r^3=t^3=(rt)^2=1$. The nonzero background
$\omega_{\rm tet}$ is specified by $R^3=T^3=1$, $(RT)^2=f$;
its full fermionic extension is the binary tetrahedral group.
The split background on $G_b=\mathrm{SL}(2,\mathbb F_3)$ is a different
example: its fermionic group is $\mathbb Z_2^f\times\mathrm{SL}(2,\mathbb F_3)$.

For $S_4$, choose $r^2=t^4=(rt)^3=1$. The two signs in
$\omega_{\alpha\beta}$ specify

$$
R^2=f^\alpha,\qquad T^4=f^\beta,\qquad (RT)^3=1.
$$

The character $x$ is the permutation sign, with $x(r)=x(t)=1$.
The complete short presentations, including the chosen generator lifts,
are checked directly against the finite multiplication tables.

## Coverage and distinctness

Historical relabelings and section changes are checked on every ordered
pair. The additional Bott-family identifications are constructed from
their graded central extensions and verified by the same pairwise test.
Within each normalized group family, the verifier enumerates every group
automorphism and compares the complete defining-relator signs and grading,
allowing changes of generator lifts. No two retained rows have the same
graded extension orbit. Historical raw result bytes remain unchanged.

The [cochain and geometric controls](CALIBRATIONS_4D.md) have a different
scope and are listed separately from these classification examples.
'''


def build_outputs(result):
    rows=result['records'];outputs={}
    outputs['tables/internal_4d_symbolic.json']=json.dumps(result,indent=2,sort_keys=True)+'\n'
    outputs['tables/internal_4d_symbolic.csv']=csv_text(rows,symbolic=True)
    outputs['tables/internal_4d.csv']=csv_text(rows)
    overview=['# 4+1D finite internal symmetries','',
        f'**{len(rows)} distinct computed symmetry backgrounds**, organized by their bosonic quotient.',
        'Classification and the full stacking group are complete for every row.', '',
        '| Family | Backgrounds | Unitary | Antiunitary | Split extension | Nonsplit extension | Results |',
        '|---|---:|---:|---:|---:|---:|---|']
    for c in result['categories']:
        key=c['category'];subset=[r for r in rows if r['category']==key]
        overview.append(f'| {c["title"]} | {c["backgrounds"]} | {c["unitary"]} | {c["antiunitary"]} | {c["split"]} | {c["nonsplit"]} | [Table](four_dimensional/{key}.md) |')
        outputs['tables/four_dimensional/'+key+'.md']=family_page(key,c['title'],subset)
        outputs['tables/four_dimensional/'+key+'.csv']=csv_text(subset)
    overview += ['', '[Background definitions](../FOUR_DIMENSIONAL_BACKGROUNDS.md) · [Combined CSV](internal_4d.csv) · [Coverage ledger](../COVERAGE_4D.json)',
        '', 'The 609 saved named calculations reduce to these 572 backgrounds after verified group relabelings, automorphisms and cocycle section changes. Repeated computations are retained as provenance for the same row.',
        'All 43 backgrounds in the original two introductory tables are included; the remaining 529 are identified separately in the coverage ledger.',
        '', 'A nonzero cocycle representative can define a split extension. The split/nonsplit columns use its cohomology class. These columns concern the fermionic symmetry, not whether the final stacking group extends its filtration nontrivially.',
        '', '[Cochain and geometric controls](../CALIBRATIONS_4D.md) are listed separately and do not increase the number of classification backgrounds.', '']
    outputs['tables/internal_4d.md']='\n'.join(overview)
    coverage={k:result[k] for k in ('schema','catalog_sha256','named_record_count','literal_input_count','background_count','intro_count','additional_backgrounds','group_convention','deduplication','record_coverage','intro_coverage','categories','orbit_uniqueness','quotient_group_uniqueness','source_collections')}
    coverage['backgrounds']=[{k:r[k] for k in ('background_id','representative_record','group','bosonic_order','fermionic_order','aliases','intro_rows','graded_extension_orbit_signature')} for r in rows]
    outputs['COVERAGE_4D.json']=json.dumps(coverage,indent=2,sort_keys=True)+'\n'
    outputs['FOUR_DIMENSIONAL_BACKGROUNDS.md']=BACKGROUND_DEFINITIONS
    outputs['CALIBRATIONS_4D.md']=r'''# 4+1D cochain and geometric controls

These tests retain a chosen decoration, explicit cochain values, detector
cycles or geometric periods. They are not extra symmetry-classification rows.
Their associated finite backgrounds already appear in the
[classification tables](tables/internal_4d.md), where applicable.

| Control | Scope | Saved evidence |
|---|---|---|
| $G_b=Q_8$, split unitary symmetry | Tests the final p+ip $d_3$ class for each nonzero character and its legal Majorana lifts. | [Detector cycles](../finite_examples/calibrations/q8_d3_detectors.json) |
| $G_b=\mathbb Z_2^2$, $s_1=x$, $\omega_2=x^2+xy+y^2$ | Tests the normalized terminal obstruction and a separate cocycle detector on the Euler input. | [Cochains and pairings](../finite_examples/calibrations/v4_euler.json) |
| $G_b=D_4$ of order eight, $s_1=0$, $\omega_2=y^2$ | Tests the final p+ip $d_4$ class against six cycles after legal lower adjustments. Here $y(t)=1$ is the reflection character. | [Detector pairings](../finite_examples/calibrations/d8_reflection_square_d4.json) |
| $G_f=\mathbb Z_4^f$, unitary | Checks the complete local representatives and the phase change to the current formulas. | [Current cochains](../calibrations/Z4f_current_cochains.md); [earlier coordinate](../finite_examples/calibrations/c2_exact_phase.json) |
| Spin-c decoration on $T^2\times\mathbb {CP}^2$ | Tests the signed six-simplex period and gravitational normalization. | [Geometric certificate](../finite_examples/calibrations/spinc_t2_cp2.json) |

A nonzero obstruction cochain can still be exact. Only a nontrivial final
class after the allowed lower adjustments obstructs a decoration. The
[certificate conventions](../finite_examples/calibrations/README.md)
specify the cochain indexing, coefficient denominators and the scope of each
saved check. Historical witnesses remain in their recorded phase coordinate.
The dihedral certificate calls the reflection character $x$; it is $y$ in
the common rotation/reflection convention used here. The certificate itself
is preserved unchanged.
'''
    return outputs


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    result=build()
    outputs=build_outputs(result)
    for name,content in outputs.items():
        path=HERE/name
        if args.check:assert path.read_text()==content,name
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print(json.dumps({k:result[k] for k in ('named_record_count','literal_input_count','background_count','intro_count','additional_backgrounds','categories')},indent=2))

if __name__=='__main__':main()
