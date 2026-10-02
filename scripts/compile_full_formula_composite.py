#!/usr/bin/env python3
"""Compose the exact zero-integer 4D transfer from already verified scalar DAGs.

At n=m=0 the chart perturbation delta is zero and the tensor L is zero by its
(2,3)/(3,2) bidegrees. The surviving Z5 is the finite H*rho sum. This build traces
that sum symbolically and shares common scalar nodes across its fixed cuts.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fspt.formulas_pip_compile import Builder
from fspt.full_formula.compiler import atomic_write_bytes,compact_program
from fspt.full_formula.runtime import faces,ez_homotopy
ROOT=Path(__file__).resolve().parents[1]


def main():
    started=time.monotonic();builder=Builder();zero=builder.scalar(0)
    directory=ROOT/'fspt/data/full_formula'
    programs={name:json.loads((directory/(name+'.json')).read_text()) for name in ('rho4','h6','nonbinary4')}
    def field(name,degree):
        values=[zero]*64
        for f in faces(5,degree):values[sum(1<<j for j in f)]=builder.make('field',name,f)
        return values
    base={name:field(name,degree) for name,degree in [('a',3),('b',3),('c',4),('cp',4),('w',2),('s',1)]}
    base.update(n=[zero]*64,m=[zero]*64)
    def run(name,fields):
        program=programs[name];values=[]
        for op,*args in program['program']:
            if op=='const':value=builder.scalar(args[0])
            elif op=='field':value=fields[args[0]][sum(1<<j for j in args[1])]
            elif op=='add':value=values[args[0]]+values[args[1]]
            elif op=='mul':value=values[args[0]]*values[args[1]]
            elif op=='mod':value=values[args[0]]%args[1]
            elif op=='div':value=builder.divide(values[args[0]],args[1])
            elif op=='floor':value=builder.floor(values[args[0]],args[1])
            elif op=='bit':value=builder.bit(values[args[0]],args[1])
            else:raise ValueError(op)
            values.append(value)
        return [values[i] for i in program['outputs']]
    nonbinary=run('nonbinary4',base)[0];binary=zero;cuts=0
    def pull(values,projection,degree):
        result=[zero]*128
        for face in faces(6,degree):
            image=tuple(projection[j] for j in face)
            if len(set(image))==len(image):
                result[sum(1<<j for j in face)]=values[sum(1<<j for j in image)]
        return result
    for simplex in ez_homotopy(5):
        projections=tuple(tuple(v[j] for v in simplex) for j in range(3))
        if min(len(set(projections[j])) for j in (1,2))<4:continue
        fields=dict(n=[zero]*128,m=[zero]*128,
                    a=pull(base['a'],projections[1],3),b=pull(base['b'],projections[2],3),
                    w=pull(base['w'],projections[0],2),s=pull(base['s'],projections[0],1))
        rho=run('rho4',fields);U=[zero]*128
        for f,value in zip(faces(6,3),rho[1:]):U[sum(1<<j for j in f)]=value
        common=dict(n=[zero]*128,y=[zero]*128,w=fields['w'],s=fields['s'])
        residual=rho[0]
        for a in (fields['a'],fields['b'],U):residual+=run('h6',dict(common,a=a))[0]
        binary+=residual%2;cuts+=1
        if cuts%10==0:print(json.dumps(dict(cuts=cuts,nodes=len(builder.nodes),seconds=time.monotonic()-started)),flush=True)
    result=(nonbinary+24*(binary%2))%48
    data=compact_program(builder,[result],dict(name='majorana4_product_composed',top_degree=5,
          denominator=48,integer_zero=True,finite_homotopy_cuts=cuts,
          coordinate='publication-20260930-native',
          component_sha256={name:hashlib.sha256((directory/(name+'.json')).read_bytes()).hexdigest() for name in programs}))
    path=directory/'majorana4_product_composed.json';raw=(json.dumps(data,separators=(',',':'))+'\n').encode();atomic_write_bytes(path,raw)
    print(json.dumps(dict(success=True,cuts=cuts,nodes=len(data['program']),seconds=time.monotonic()-started,
                          sha256=hashlib.sha256(raw).hexdigest())),flush=True)

if __name__=='__main__':main()
