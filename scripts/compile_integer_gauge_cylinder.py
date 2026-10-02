#!/usr/bin/env python3
"""Compile the literal full d4 integer gauge prism, retaining every upper carry.

The native-to-operator Majorana shift and complete Y6 source are composed
explicitly. Outputs are corrections; beta=gamma=0 is the only gauge restriction.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fspt.formulas_pip_compile import Builder
from fspt.full_formula.compiler import atomic_write_bytes,compact_program


def degenerate(vertices):return any(a==b for a,b in zip(vertices,vertices[1:]))


def compile_cylinder(data_dir):
    started=time.monotonic();builder=Builder();zero=builder.scalar(0)
    names=['source_4_majorana','source_4_fermion','y6','high6']
    raw={name:(data_dir/(name+'.json')).read_bytes() for name in names}
    programs={name:json.loads(value) for name,value in raw.items()}
    def run(name,vertices,get_field):
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
    @lru_cache(None)
    def integer(vertices):
        if degenerate(vertices):return zero
        total=pull('n',vertices)
        for i in range(len(vertices)):
            face=vertices[:i]+vertices[i+1:]
            sign=1-2*pull('s',vertices[:2]) if i==0 else builder.scalar((-1)**i)
            total+=sign*face[0][1]*pull('lambda',face)
        return total
    def prism(fun,vertices,modulus):
        if degenerate(vertices):return zero
        total=zero
        for i,v in enumerate(vertices):
            if v[1]:
                simplex=tuple((u[0],0) for u in vertices[:i+1])+vertices[i:]
                if not degenerate(simplex):total+=(-1)**i*fun(simplex)
        return total%modulus
    @lru_cache(None)
    def majorana_source(vertices):
        return zero if degenerate(vertices) else run('source_4_majorana',vertices,native_field)[0]%2
    @lru_cache(None)
    def majorana(vertices):
        return zero if degenerate(vertices) else (pull('a',vertices)+prism(majorana_source,vertices,2))%2
    @lru_cache(None)
    def fermion_source(vertices):
        return zero if degenerate(vertices) else run('source_4_fermion',vertices,native_field)[0]%2
    @lru_cache(None)
    def fermion(vertices):
        return zero if degenerate(vertices) else (pull('c',vertices)+prism(fermion_source,vertices,2))%2
    def native_field(name,vertices):
        if name=='n':return integer(vertices)
        if name=='a':return majorana(vertices)
        if name=='c':return fermion(vertices)
        if name in ('w','s'):return pull(name,vertices)
        raise ValueError(name)
    @lru_cache(None)
    def completion(vertices):
        return zero if degenerate(vertices) else run('y6',vertices,native_field)[0]%2
    def operator_field(name,vertices):
        if name=='a':
            return (majorana(vertices)+pull('s',vertices[:2])*(builder.floor(integer(vertices[1:]),2)%2))%2
        if name=='y':return completion(vertices)
        return native_field(name,vertices)
    @lru_cache(None)
    def upper_source(vertices):
        if degenerate(vertices):return zero
        high,cubic=run('high6',vertices,operator_field)
        return (3*high+4*cubic)%48
    outputs=[('majorana',prism(majorana_source,tuple((i,1) for i in range(4)),2),3,2),
             ('fermion',prism(fermion_source,tuple((i,1) for i in range(5)),2),4,2),
             ('bosonic',prism(upper_source,tuple((i,1) for i in range(6)),48),5,48)]
    reports=[]
    for stage,value,degree,denominator in outputs:
        name='gauge_integer4_'+stage
        data=compact_program(builder,[value],dict(name=name,top_degree=degree,denominator=denominator,
            coordinate='publication-20260930-native',operation='literal-full-integer-gauge-cylinder',
            output_semantics='correction only',inputs=dict(n=2,a=3,c=4,**{'lambda':1},w=2,s=1),
            assumptions='beta=gamma=0; full integer field and parameter retained',
            component_sha256={n:hashlib.sha256(x).hexdigest() for n,x in raw.items()}))
        used=sorted({node[1] for node in data['program'] if node[0]=='field'})
        if stage=='majorana':assert not any(n in used for n in ['a','c'])
        if stage=='fermion':assert 'c' not in used
        data['used_fields']=used
        payload=(json.dumps(data,separators=(',',':'))+'\n').encode()
        atomic_write_bytes(data_dir/(name+'.json'),payload)
        reports.append(dict(name=name,nodes=len(data['program']),bytes=len(payload),used_fields=used,
                            sha256=hashlib.sha256(payload).hexdigest()))
    return dict(status='compiled',seconds=time.monotonic()-started,raw_nodes=len(builder.nodes),kernels=reports)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=ROOT/'fspt/data/full_formula')
    args=parser.parse_args();resource.setrlimit(resource.RLIMIT_AS,(12<<30,12<<30))
    print(json.dumps(compile_cylinder(args.data_dir)),flush=True)


if __name__=='__main__':main()
