"""Paired conservative 2-adic interpretation of the immutable parity DAGs.

Track the divisibility of each value and of its change under a sixteen-sheet
shift. UNKNOWN is not a failed formula, and is never promoted to a proof.
"""
from pathlib import Path
import argparse
import hashlib
import json

INF=10**9
ap=argparse.ArgumentParser()
ap.add_argument('--public-reference',type=Path,default=Path('/home/xingyu/FSPT_AHSS_public'))
args=ap.parse_args()
ROOT=args.public_reference/'fspt/data/full_formula'


def v2(x):
    return INF if not x else (abs(x)&-abs(x)).bit_length()-1


def bounded_sum(a,b):
    return min(INF,a+b)


def single(op,a,ca,b=None,cb=None,k=None,same=False):
    if op in ('add','mul'):
        if ca is not None and cb is not None:
            c=ca+cb if op=='add' else ca*cb
            return v2(c),c
        if op=='add':return (min(INF,a+1),None) if same else (min(a,b),None)
        if ca==0 or cb==0:return INF,0
        return bounded_sum(a,b),None
    if ca is not None:
        if op=='mod':c=ca%k
        elif op in ('floor','div'):
            if op=='div':assert ca%k==0
            c=ca//k
        elif op=='bit':c=(ca>>k)&1
        else:raise ValueError(op)
        return v2(c),c
    if op=='mod':
        return (INF,0) if k&(k-1)==0 and a>=v2(k) else (min(a,v2(k)),None)
    if op=='bit':return (INF,0) if a>k else (0,None)
    if op in ('floor','div'):
        return (max(0,a-v2(k)),None) if k&(k-1)==0 or op=='div' else (0,None)
    raise ValueError(op)


def audit(name,shifted,zero_fields=(),y_delta=INF):
    raw=(ROOT/(name+'.json')).read_bytes()
    data=json.loads(raw);values=[];unproved=0
    for node in data['program']:
        op=node[0]
        if op=='const':
            value=node[1];out=(v2(value),value,v2(value),value,INF)
        elif op=='field':
            name_field=node[1]
            if name_field=='y':out=(0,None,0,None,y_delta)
            elif name_field in shifted:
                out=(INF,0,4,None,4) if name_field in zero_fields else (0,None,0,None,4)
            elif name_field in zero_fields:out=(INF,0,INF,0,INF)
            else:out=(0,None,0,None,INF)
        else:
            av,ac,apv,apc,ad=values[node[1]]
            if op in ('add','mul'):
                bv,bc,bpv,bpc,bd=values[node[2]]
                same=node[1]==node[2]
                v,c=single(op,av,ac,bv,bc,same=same)
                pv,pc=single(op,apv,apc,bpv,bpc,same=same)
                if op=='add':delta=bounded_sum(ad,1) if same else min(ad,bd)
                elif same:delta=min(bounded_sum(bounded_sum(av,ad),1),bounded_sum(ad,ad))
                else:delta=min(bounded_sum(av,bd),bounded_sum(bv,ad),bounded_sum(ad,bd))
            else:
                k=node[2]
                if op=='div' and (av<v2(k) or apv<v2(k)):unproved+=1
                v,c=single(op,av,ac,k=k);pv,pc=single(op,apv,apc,k=k)
                if op=='mod':
                    delta=INF if k&(k-1)==0 and ad>=v2(k) else min(ad,v2(k))
                elif op=='bit':delta=INF if ad>k else 0
                elif op=='floor':
                    delta=max(0,ad-v2(k)) if k&(k-1)==0 and ad>=v2(k) else 0
                elif op=='div':delta=max(0,ad-v2(k))
                else:raise ValueError(op)
            if c is not None and pc is not None:delta=v2(pc-c)
            # A formally unchanged input stays exactly unchanged under every deterministic operation.
            if (op in ('add','mul') and ad==bd==INF) or (op not in ('add','mul') and ad==INF):delta=INF
            out=(v,c,pv,pc,delta)
        values.append(out)
    return {'packet':name,'sha256':hashlib.sha256(raw).hexdigest(),
            'nodes':len(values),'outputs':[{'base_v2':values[i][0],'perturbed_v2':values[i][2],
                'difference_v2':values[i][4]} for i in data['outputs']],
            'exact_divisions_not_independently_proved':unproved}


packets=('source_4_majorana','source_4_fermion','product_4_majorana','product_4_fermion',
         'y6','h6','high6','rho4','tensor4','nonbinary4')
scenarios=[]
for label,shifted,zero in (
    ('arbitrary_first_shift',('n',),()),
    ('arbitrary_both_shift',('n','m'),()),
    ('right_neutral_from_identity',('m',),('m','b','cp')),
    ('left_neutral_from_identity',('n',),('n','a','c'))):
    records=[];y_delta=INF
    for packet in packets:
        result=audit(packet,shifted,zero,y_delta)
        if packet=='y6':
            raw_delta=result['outputs'][0]['difference_v2']
            y_delta=INF if raw_delta>=1 else 0
        threshold=4 if packet in ('high6','nonbinary4') else 1
        considered=result['outputs'][:1] if packet=='high6' else result['outputs']
        result['required_difference_v2']=threshold
        result['certificate_status']='PROVED' if all(x['difference_v2']>=threshold for x in considered) else 'UNKNOWN'
        records.append(result)
    scenarios.append({'name':label,'shifted_fields':shifted,'zero_base_fields':zero,'packets':records})
report={'status':'COMPLETE','claim':'Per-packet conservative periodicity certificates only; UNKNOWN is not disproved',
        'scope':'Legal integral parity cochains; shift n and/or m by arbitrary multiples of sixteen',
        'public_reference':str(args.public_reference),'scenarios':scenarios}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
for scenario in scenarios:
    print(json.dumps({'scenario':scenario['name'],
          'packets':[(p['packet'],p['certificate_status'],[o['difference_v2'] for o in p['outputs']]) for p in scenario['packets']]}))
