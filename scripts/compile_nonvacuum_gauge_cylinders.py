#!/usr/bin/env python3
"""Compile exact publication d4 gauge prisms with nonzero base decorations.

All operations are literal substitutions into the frozen complete source DAG.
Outputs are corrections, never endpoint totals. No source or product law is
changed, and no lower-dimensional looping identity is used.
"""
import argparse
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fspt.formulas_pip_compile import Builder
from fspt.full_formula.compiler import atomic_write_bytes,compact_program


def degenerate(v):return any(a==b for a,b in zip(v,v[1:]))


def compile_mode(data_dir,mode,dimension=4):
    started=time.monotonic();builder=Builder();zero=builder.scalar(0)
    lower_name='source_{}_fermion'.format(dimension)
    phase_modulus=48 if dimension==4 else 16
    names=['high6']+([lower_name] if mode=='majorana' else [])+(['lift3_source'] if dimension==3 else [])
    raw={name:(data_dir/(name+'.json')).read_bytes() for name in names}
    programs={name:json.loads(value) for name,value in raw.items()}
    def run(name,vertices,get_field=None):
        get_field=field if get_field is None else get_field
        values=[]
        for op,*args in programs[name]['program']:
            if op=='const':value=builder.scalar(args[0])
            elif op=='field':value=get_field(args[0],tuple(vertices[i] for i in args[1]))
            elif op=='add':value=values[args[0]]+values[args[1]]
            elif op=='mul':value=values[args[0]]*values[args[1]]
            elif op=='mod':value=values[args[0]]%args[1]
            elif op=='div':value=builder.divide(values[args[0]],args[1])
            elif op=='floor':value=builder.floor(values[args[0]],args[1])
            elif op=='bit':value=builder.bit(values[args[0]],args[1])
            else:raise ValueError(op)
            values.append(value)
        return [values[i] for i in programs[name]['outputs']]
    @lru_cache(None)
    def pull(name,vertices):
        base=tuple(v[0] for v in vertices)
        return zero if degenerate(base) else builder.make('field',name,base)
    def d_eta(name,vertices):
        total=zero
        for i in range(len(vertices)):
            face=vertices[:i]+vertices[i+1:]
            total+=(-1)**i*face[0][1]*pull(name,face)
        return total%2
    @lru_cache(None)
    def majorana(vertices):
        if mode=='fermion' or degenerate(vertices):return zero
        return (pull('a',vertices)+d_eta('beta',vertices))%2
    def prism(fun,vertices,modulus):
        if degenerate(vertices):return zero
        total=zero
        for i,v in enumerate(vertices):
            if v[1]:
                simplex=tuple((u[0],0) for u in vertices[:i+1])+vertices[i:]
                if not degenerate(simplex):total+=(-1)**i*fun(simplex)
        return total%modulus
    @lru_cache(None)
    def lower_source(vertices):
        return zero if degenerate(vertices) else run(lower_name,vertices)[0]%2
    @lru_cache(None)
    def fermion(vertices):
        if degenerate(vertices):return zero
        correction=prism(lower_source,vertices,2) if mode=='majorana' else d_eta('gamma',vertices)
        return (pull('c',vertices)+correction)%2
    def field(name,vertices):
        if name in ('n','y'):return zero
        if name in ('w','s'):return pull(name,vertices)
        if name=='a':return majorana(vertices)
        if name=='c':return fermion(vertices)
        raise ValueError(name)
    @lru_cache(None)
    def upper_source(vertices):
        if degenerate(vertices):return zero
        if dimension==4:
            high,cubic=run('high6',vertices)
            return (3*high+4*cubic)%48
        outputs=run('lift3_source',vertices);metadata=programs['lift3_source'];total=zero
        for call in metadata['calls']:
            offset=call['offset'];arrays={}
            for name,degree in zip(metadata['high_fields'],metadata['high_degrees']):
                arrays[name]={}
                for face in combinations(range(7),degree+1):
                    arrays[name][face]=outputs[offset];offset+=1
            assert all(builder.constant(value)==0 for value in arrays['n'].values())
            def high_field(name,face):
                return zero if name=='y' else arrays[name][face]
            high,cubic=run('high6',tuple(range(7)),high_field)
            assert builder.constant(cubic)==0
            total+=call['sign']*high
        return total%16
    outputs=[('bosonic',prism(upper_source,tuple((i,1) for i in range(dimension+2)),phase_modulus),dimension+1,phase_modulus)]
    if mode=='majorana':outputs.insert(0,('fermion',prism(lower_source,tuple((i,1) for i in range(dimension+1)),2),dimension,2))
    manifests=[]
    for stage,value,degree,denominator in outputs:
        name=('gauge_mc{}_n0_' if mode=='majorana' else 'gauge_cf{}_n0_').format(dimension)+stage
        inputs=dict(a=dimension-1,c=dimension,beta=dimension-2,w=2,s=1) if mode=='majorana' else dict(c=dimension,gamma=dimension-1,w=2,s=1)
        data=compact_program(builder,[value],dict(name=name,top_degree=degree,denominator=denominator,
            coordinate='publication-20260930-native',operation='literal-nonvacuum-'+mode+'-gauge-cylinder',
            output_semantics='correction only',inputs=inputs,
            assumptions='n=0; lambda=gamma=0' if mode=='majorana' else 'n=a=0; lambda=beta=0',
            component_sha256={n:hashlib.sha256(x).hexdigest() for n,x in raw.items()}))
        used=sorted({node[1] for node in data['program'] if node[0]=='field'})
        if mode=='majorana' and stage=='fermion':assert 'c' not in used
        data['used_fields']=used
        payload=(json.dumps(data,separators=(',',':'))+'\n').encode()
        atomic_write_bytes(data_dir/(name+'.json'),payload)
        manifests.append(dict(name=name,nodes=len(data['program']),bytes=len(payload),used_fields=used,sha256=hashlib.sha256(payload).hexdigest()))
    return dict(status='compiled',mode=mode,dimension=dimension,seconds=time.monotonic()-started,raw_nodes=len(builder.nodes),kernels=manifests)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parents[1]/'fspt/data/full_formula')
    ap.add_argument('--mode',choices=['majorana','fermion'],required=True)
    ap.add_argument('--dimension',type=int,choices=[3,4],default=4)
    args=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(8 << 30,8 << 30))
    print(json.dumps(compile_mode(args.data_dir,args.mode,args.dimension)),flush=True)


if __name__=='__main__':main()
