#!/usr/bin/env python3
"""Compose the exact publication 3D source at n=0, retaining Majorana and fermion faces."""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.formulas_pip_compile import Builder
from fspt.full_formula.compiler import atomic_write_bytes,compact_program


def main():
    resource.setrlimit(resource.RLIMIT_AS,(8<<30,8<<30));started=time.monotonic()
    directory=ROOT/'fspt/data/full_formula';names=['lift3_source','high6','source_3_fermion']
    raw={name:(directory/(name+'.json')).read_bytes() for name in names};programs={name:json.loads(value) for name,value in raw.items()}
    builder=Builder();zero=builder.scalar(0)
    def run(name,get_field):
        values=[]
        for op,*args in programs[name]['program']:
            if op=='const':value=builder.scalar(args[0])
            elif op=='field':value=get_field(args[0],tuple(args[1]))
            elif op=='add':value=values[args[0]]+values[args[1]]
            elif op=='mul':value=values[args[0]]*values[args[1]]
            elif op=='mod':value=values[args[0]]%args[1]
            elif op=='div':value=builder.divide(values[args[0]],args[1])
            elif op=='floor':value=builder.floor(values[args[0]],args[1])
            elif op=='bit':value=builder.bit(values[args[0]],args[1])
            else:raise ValueError(op)
            values.append(value)
        return [values[i] for i in programs[name]['outputs']]
    def field(name,face):
        if name=='n':return zero
        if name in ('a','c','w','s'):return builder.make('field',name,face)
        raise ValueError(name)
    lifted=run('lift3_source',field);metadata=programs['lift3_source'];total=zero
    for call in metadata['calls']:
        offset=call['offset'];arrays={}
        for name,degree in zip(metadata['high_fields'],metadata['high_degrees']):
            arrays[name]={}
            for face in combinations(range(7),degree+1):arrays[name][face]=lifted[offset];offset+=1
        # The suspended integer field vanishes as a literal symbolic expression,
        # so its Y6 completion is exactly zero, not a cohomological inference.
        assert all(builder.constant(value)==0 for value in arrays['n'].values())
        def high_field(name,face):return zero if name=='y' else arrays[name][face]
        high,cubic=run('high6',high_field);assert builder.constant(cubic)==0
        total+=call['sign']*high
    value=total%16
    data=compact_program(builder,[value],dict(name='source3_majorana_n0_bosonic',top_degree=5,denominator=16,
          coordinate='publication-20260930-native',assumptions='n=0; closed a,w,s; delta c=F4(a); literal original suspended source',
          inputs=dict(a=2,c=3,w=2,s=1),component_sha256={name:hashlib.sha256(value).hexdigest() for name,value in raw.items()}))
    payload=(json.dumps(data,separators=(',',':'))+'\n').encode();atomic_write_bytes(directory/'source3_majorana_n0_bosonic.json',payload)
    lower=[]
    for simplex in combinations(range(6),5):
        def lower_field(name,face):
            if name in ('n','c'):return zero
            return builder.make('field',name,tuple(simplex[i] for i in face))
        lower.append(run('source_3_fermion',lower_field)[0]%2)
    certificate=compact_program(builder,lower,dict(name='source3_majorana_n0_lower',top_degree=5,
          coordinate='publication-20260930-native',assumptions='n=0; closed a,w,s',
          inputs=dict(a=2,w=2,s=1),output_faces=list(combinations(range(6),5)),
          component_sha256={'source_3_fermion':hashlib.sha256(raw['source_3_fermion']).hexdigest()}))
    lower_payload=(json.dumps(certificate,separators=(',',':'))+'\n').encode()
    atomic_write_bytes(directory/'source3_majorana_n0_lower.json',lower_payload)
    print(json.dumps(dict(status='compiled',nodes=len(data['program']),raw_nodes=len(builder.nodes),bytes=len(payload),
                         sha256=hashlib.sha256(payload).hexdigest(),lower_nodes=len(certificate['program']),
                         lower_sha256=hashlib.sha256(lower_payload).hexdigest(),seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':main()
