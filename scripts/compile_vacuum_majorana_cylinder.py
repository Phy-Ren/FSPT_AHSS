#!/usr/bin/env python3
"""Compile the literal complete 4D vacuum Majorana gauge cylinder.

This substitutes A=d(eta beta), C=H F(A), V=H O(A,C) into the already verified
source DAGs. H is exactly the normalized prism used by gap/full_stacking.g.
No dimensional descent identity or coordinate change is assumed.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fspt.formulas_pip_compile import Builder
from fspt.full_formula.compiler import atomic_write_bytes,compact_program


def degenerate(vertices):return any(a==b for a,b in zip(vertices,vertices[1:]))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parents[1]/'fspt/data/full_formula')
    args=ap.parse_args();started=time.monotonic();builder=Builder();zero=builder.scalar(0)
    programs={name:json.loads((args.data_dir/(name+'.json')).read_text())
              for name in ['source_4_fermion','high6']}
    def run(name,vertices,field):
        values=[];program=programs[name]
        for op,*x in program['program']:
            if op=='const':value=builder.scalar(x[0])
            elif op=='field':value=field(x[0],tuple(vertices[j] for j in x[1]))
            elif op=='add':value=values[x[0]]+values[x[1]]
            elif op=='mul':value=values[x[0]]*values[x[1]]
            elif op=='mod':value=values[x[0]]%x[1]
            elif op=='div':value=builder.divide(values[x[0]],x[1])
            elif op=='floor':value=builder.floor(values[x[0]],x[1])
            elif op=='bit':value=builder.bit(values[x[0]],x[1])
            else:raise ValueError(op)
            values.append(value)
        return [values[i] for i in program['outputs']]
    @lru_cache(None)
    def pull(name,vertices):
        base=tuple(v[0] for v in vertices)
        return zero if degenerate(base) else builder.make('field',name,base)
    @lru_cache(None)
    def majorana(vertices):
        if degenerate(vertices):return zero
        value=zero
        for i in range(len(vertices)):
            face=vertices[:i]+vertices[i+1:]
            value+=(-1)**i*face[0][1]*pull('beta',face)
        return value%2
    def fields(name,vertices):
        if name in ('n','y'):return zero
        if name in ('s','w'):return pull(name,vertices)
        if name=='a':return majorana(vertices)
        if name=='c':return fermion(vertices)
        raise ValueError(name)
    @lru_cache(None)
    def lower_source(vertices):
        return zero if degenerate(vertices) else run('source_4_fermion',vertices,fields)[0]%2
    def prism(function,vertices,modulus):
        if degenerate(vertices):return zero
        value=zero
        for i,v in enumerate(vertices):
            if v[1]==0:continue
            face=tuple((x[0],0) for x in vertices[:i+1])+vertices[i:]
            if not degenerate(face):value+=(-1)**i*function(face)
        return value%modulus
    @lru_cache(None)
    def fermion(vertices):return prism(lower_source,vertices,2)
    @lru_cache(None)
    def upper_source(vertices):
        if degenerate(vertices):return zero
        high,cubic=run('high6',vertices,fields)
        return (3*high+4*cubic)%48
    outputs=[fermion(tuple((i,1) for i in range(5))),
             prism(upper_source,tuple((i,1) for i in range(6)),48)]
    manifests=[]
    for index,stage in enumerate(['fermion','bosonic']):
        name='vacuum_mc4_'+stage
        data=compact_program(builder,[outputs[index]],dict(name=name,top_degree=index+4,
            denominator=2 if index==0 else 48,coordinate='publication-20260930-native',
            operation='literal-vacuum-Majorana-gauge-cylinder',
            inputs=dict(beta=2,w=2,s=1),assumptions='vacuum input; lambda=gamma=0; arbitrary beta2',
            component_sha256={n:hashlib.sha256((args.data_dir/(n+'.json')).read_bytes()).hexdigest() for n in programs}))
        path=args.data_dir/(name+'.json');raw=(json.dumps(data,separators=(',',':'))+'\n').encode();atomic_write_bytes(path,raw)
        manifests.append(dict(name=name,nodes=len(data['program']),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    print(json.dumps(dict(status='compiled',seconds=time.monotonic()-started,raw_nodes=len(builder.nodes),kernels=manifests)),flush=True)


if __name__=='__main__':main()
