#!/usr/bin/env python3
"""Verify archived comparisons, exact Smith certificates, and independent runs."""
import argparse,hashlib,json
from collections import Counter
from itertools import combinations_with_replacement,product
from math import comb,gcd,lcm
from pathlib import Path
from sympy import Matrix,Symbol,expand,sympify,zeros
from split_closed_formula import invariant_factors as split_group,canonical_primary
from nonsplit_closed_formula import nonsplit_closed_formula,block
from two_factor_cubic_lattice import coordinates,factors as two_factor_group
from cyclic_eta_smith import eta_presentation
from supercohomology_blocks import compute
from higher_support import closed
from koszul_stabilization import all_signatures,signature,certificate,certificate_three
from one_spectator_symbolic_certificate import symbolic_certificate

ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def cleaned(ns):return sorted(n for n in ns if n>1)

def check_archived():
    report=[]
    for row in read('data/archived_51.json')['selected_backgrounds']:
        if not any(row['power_bits']):
            actual=split_group(row['orders']);kind='split'
        else:
            m=row.get('normalized_distinguished_order')
            ns=row.get('normalized_spectator_orders')
            if m is None:
                active=[i for i,b in enumerate(row['power_bits']) if b]
                i=max(active,key=lambda i:((row['orders'][i]&-row['orders'][i]),row['orders'][i]))
                m=row['orders'][i];ns=row['orders'][:i]+row['orders'][i+1:]
            actual=nonsplit_closed_formula(m,ns);kind='nonsplit'
        assert canonical_primary(actual)==canonical_primary(row['full_group']),(row['background_id'],actual,row['full_group'])
        report.append({'background_id':row['background_id'],'kind':kind,'invariant_factors':actual,'status':'passed'})
    assert len(report)==51
    return {'split':sum(x['kind']=='split' for x in report),'nonsplit':sum(x['kind']=='nonsplit' for x in report),'cases':report}

def check_corollaries():
    for r in range(9):
        split=[2]*(3*comb(r,3)+3*comb(r,4)+comb(r,5))
        nonsplit=sorted([16]+[8]*r+[4]*comb(r,2)+[2]*(2*comb(r,2)+6*comb(r,3)+4*comb(r,4)+comb(r,5)))
        assert split_group([2]*r)==split
        assert nonsplit_closed_formula(2,[2]*r)==nonsplit
    for m in range(1,33):
        assert nonsplit_closed_formula(m)==eta_presentation(m)[1]
    for a,b in product(range(1,9),repeat=2):
        m,n=2**a,2**b
        assert two_factor_group(m,n)==sorted(block(m,[])+block(m,[n]))
    return {'elementary_ranks':'0 through 8, both split and C4f','cyclic_eta_cases':32,'rank_two_integer_Smith_cases':64}

def check_higher_archived():
    results=[]
    for row in read('data/archived_51.json')['distinguished_factor_support_blocks']:
        ns=row['spectator_orders']
        if len(ns)<2:continue
        actual=compute((row['distinguished_order'],*ns))
        expand_group=lambda d:cleaned([int(n) for n,k in d.items() for _ in range(k)])
        assert actual['full_group']==expand_group(row['primary_multiplicities'])
        assert actual['bosonic']==expand_group(row['layer_support']['bosonic'])
        assert actual['complex_fermion_rank']==sum(row['layer_support']['complex_fermion'].values())
        assert actual['full_group']==closed(row['distinguished_order'],ns)
        results.append(row['background_id'])
    return results

def check_symbolic():
    answer={'one_spectator':symbolic_certificate()}
    t=Symbol('t',integer=True,positive=True)
    for support,method in [(2,certificate),(3,certificate_three)]:
        certs=read(f'data/support{support}_symbolic_certificates.json')['certificates']
        expected={signature(ns) for ns in all_signatures(support)}
        assert {signature(c['orders']) for c in certs}==expected
        for c in certs:
            # Regeneration also checks the exact reduction from the cochain model.
            generated=method(tuple(c['orders']))
            assert json.loads(json.dumps(generated))==c
            parse=lambda a:Matrix([[sympify(x,locals={'t':t}) for x in row] for row in a])
            a,left,right=map(parse,(c['matrix'],c['left'],c['right']))
            reduced=(left*a*right).applyfunc(expand)
            diagonal=[sympify(x,locals={'t':t}) for x in c['normalized_diagonal']]
            assert all(expand(reduced[i,j]-(diagonal[i] if i==j else 0))==0 for i in range(reduced.rows) for j in range(reduced.cols))
            assert left.det() in (1,-1) and right.det() in (1,-1)
        answer[f'{support}_spectators']={'exhaustive_order_signatures':len(certs),'symbolic_unimodular_identities':'passed; arbitrary exponents'}
    data=read('data/primitive_index_lattice.json')
    assert Matrix(data['integral_left_inverse'])*Matrix(data['index_rows'])==Matrix.eye(6)
    assert abs(Matrix([coordinates(*q) for q in data['evaluation_points']]).det())==1
    answer['primitive_index_lattice']='integral left inverse and determinant-one evaluation verified'
    return answer

def check_marked():
    results=[];source_ids=set()
    for row in read('checkpoints/threshold_comparison.json'):
        path=ROOT/row['source'];data=json.loads(path.read_text())
        assert sha(path)==row['sha256']
        assert data['markedCohomologyClass']==row['coordinates']
        assert data['phaseTargetOrders']==row['originalTarget']
        assert data['secondaryOriginalClasses'][0]==row['originalClass']
        assert data['cfQuotientOrders']==row['finalTarget']
        assert data['secondaryFinalClasses'][0]==row['finalClass']
        order=lcm(*(n//gcd(n,int(c)) for n,c in zip(row['finalTarget'],row['finalClass'])))
        assert order==row['finalClassOrder'] and (order==1)==row['survives']
        source_ids.add(data['source_id'])
        results.append({'model':row['model'],'survives':row['survives'],'final_class_order':order,'sha256_verified':row['sha256']})
    for name in ['source_pin.json','source_pin_threshold.json']:
        assert read('checkpoints/'+name)['source_id'] in source_ids
    assert len(source_ids)==1
    return {'source_id':source_ids.pop(),'cases':results}

def check_full_run():
    folder=ROOT/'full_results/split_C4_C4_C4'
    receipt=json.loads((folder/'receipt.json').read_text());data=json.loads((folder/'result.json').read_text())
    assert sha(folder/'result.json')==receipt['bundled_result_sha256']
    scientific={k:v for k,v in data.items() if k!='source_snapshot'}
    digest=hashlib.sha256(json.dumps(scientific,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert digest==receipt['scientific_content_sha256']
    a,left,right=map(Matrix,(data['presentation'],data['smithRows'],data['smithColumns']))
    reduced=left*a*right
    assert all(reduced[i,j]==(data['smithDiagonal'][i] if i==j else 0) for i in range(reduced.rows) for j in range(reduced.cols))
    assert abs(left.det())==abs(right.det())==1
    assert cleaned(data['smithDiagonal'])==split_group([4,4,4])==data['invariants']
    return {'model':data['model'],'invariant_factors':data['invariants'],'exact_Smith_identity':'passed','original_result_sha256':receipt['original_result_sha256']}

def check_deep():
    counts={}
    for support,max_exponent in [(2,8),(3,8),(4,5),(5,4)]:
        count=0
        for a in range(1,max_exponent+1):
            for bs in combinations_with_replacement(range(1,max_exponent+1),support):
                ns=tuple(2**b for b in bs);m=2**a
                assert compute((m,*ns))['full_group']==closed(m,ns)
                count+=1
        counts[str(support)]=count
    return counts

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deep',action='store_true',help='Also repeat the optional 1822-case numeric regression grid.')
    parser.add_argument('--output',type=Path,help='Optional output report path; otherwise print the report.')
    args=parser.parse_args()
    report={'status':'passed','archived':check_archived(),'elementary_and_cyclic':check_corollaries(),
            'higher_support_archived':check_higher_archived(),'all_exponent_proof':check_symbolic(),
            'marked_Majorana':check_marked(),'independent_full_run':check_full_run()}
    if args.deep:report['optional_numeric_grid']=check_deep()
    manifest=ROOT/'SHA256SUMS.json'
    if manifest.exists():
        entries=json.loads(manifest.read_text())
        for name,digest in entries.items():assert sha(ROOT/name)==digest,name
        report['bundled_file_hashes_verified']=len(entries)
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(json.dumps({'status':report['status'],'archived_split':report['archived']['split'],'archived_nonsplit':report['archived']['nonsplit'],'symbolic_order_patterns':56,'marked_Majorana_cases':4,'independent_full_run':report['independent_full_run']['invariant_factors']},indent=2))

if __name__=='__main__':main()
