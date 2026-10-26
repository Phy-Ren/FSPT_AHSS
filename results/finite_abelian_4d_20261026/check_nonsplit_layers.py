#!/usr/bin/env python3
"""Check final nonsplit decoration layers independently of stacking factors."""
import json
from math import comb
from pathlib import Path
from sympy import factorint
try:
    from .nonsplit_layers import nonsplit_2primary_layers,support_layers,nonsplit_layers
    from .nonsplit_layer_certificates import all_certificates
    from .supercohomology_blocks import compute_cf_bosonic
except ImportError:
    from nonsplit_layers import nonsplit_2primary_layers,support_layers,nonsplit_layers
    from nonsplit_layer_certificates import all_certificates
    from supercohomology_blocks import compute_cf_bosonic
ROOT=Path(__file__).resolve().parent

def primary_two(ns):
    return sorted(2**int(factorint(n)[2]) for n in ns if n%2==0)

def run():
    data=json.loads((ROOT/'data/archived_51.json').read_text())
    checked=[]
    for row in data['selected_backgrounds']:
        if not any(row['power_bits']):continue
        m=row.get('normalized_distinguished_order')
        ns=row.get('normalized_spectator_orders')
        if m is None:
            active=[i for i,b in enumerate(row['power_bits']) if b]
            i=max(active,key=lambda i:row['orders'][i]&-row['orders'][i])
            m=row['orders'][i];ns=row['orders'][:i]+row['orders'][i+1:]
        actual=nonsplit_layers(m,ns)
        from split_layers import invariant_factors
        expected={k:invariant_factors(v) for k,v in row['final_layers'].items()}
        assert actual==expected,(row['background_id'],actual,expected)
        checked.append(row['background_id'])
    support_count=0
    for row in data['distinguished_factor_support_blocks']:
        m=row['distinguished_order'];ns=row['spectator_orders']
        expected={k:sorted(int(n) for n,a in v.items() for _ in range(a)) for k,v in row['layer_support'].items()}
        assert support_layers(m,ns)==expected,(row,support_layers(m,ns))
        support_count+=1
    saved=json.loads((ROOT/'data/nonsplit_layer_certificates.json').read_text())['certificates']
    assert all_certificates()==saved
    for r in range(9):
        actual=nonsplit_2primary_layers(2,[2]*r)
        ranks={'pip':1,'majorana':1+r,'complex_fermion':1+r+comb(r,2),
               'bosonic':1+r+3*comb(r,2)+6*comb(r,3)+4*comb(r,4)+comb(r,5)}
        assert actual=={k:[2]*n for k,n in ranks.items()}
    # No surviving Majorana layer occurs in these higher supports, so the
    # exact CF/bosonic subsystem gives their complete final layers.
    for r in range(2,6):
        exact=compute_cf_bosonic((2,)*(r+1))
        expected=support_layers(2,[2]*r)
        assert exact['bosonic']==expected['bosonic']
        assert [2]*exact['complex_fermion_rank']==expected['complex_fermion']
    return {'archived_nonsplit_final_layer_comparisons':len(checked),
            'archived_support_layer_comparisons':support_count,
            'exhaustive_symbolic_bosonic_layer_certificates':len(saved),
            'elementary_corollary_ranks':'0 through 8',
            'independent_elementary_higher_support_matrices':4,
            'status':'passed'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
