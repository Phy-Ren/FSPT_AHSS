#!/usr/bin/env python3
"""Persistent JSONL worker for complete native publication formulas.

Face arrays are indexed by the bit mask of their vertices (index zero unused).
Binary source/product stages return a bit. The bosonic stage returns a reduced
exact rational modulo one. Product outputs are corrections, never sums of the
input lower fields. One process serves arbitrarily many requests and caches the
compiled programs, pure completions, and transfer states.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys
import traceback
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fspt.full_formula.runtime import Backend
from fspt.full_formula.descent import DescendedBackend
from fspt.full_formula.fmps1 import FMPS1Backend
from fspt.majorana_backend import ClosedMajoranaBackend


def arrays(data):
    out={}
    for key,value in data.items():
        if not isinstance(value,list) or not value or len(value)&(len(value)-1):
            raise ValueError('Each field must be a power-of-two mask array')
        if any(isinstance(x,bool) or not isinstance(x,int) for x in value):
            raise TypeError('Only exact integer field entries are accepted')
        if key not in ('n','m') and any(x not in (0,1) for x in value):
            raise ValueError('Binary fields must have values zero or one')
        out[key]=tuple(value)
    return out


def neutral_chiral_allowed(state,background):
    """Recognize constant neutral p+ip stacks for unitary split symmetry."""
    if any(background['w']) or any(background['s']):
        return False
    values=state['n'];vertices=[values[1<<j] for j in range(len(values).bit_length()-1)]
    return len(set(vertices))==1 and all(value==0 for mask,value in enumerate(values) if not mask or mask&(mask-1))


def respond(backend,request,experimental_descent=False):
    operation=request['operation']
    if operation=='status':
        return dict(ok=True,coordinate='publication-20260930-native',
                    native=backend.native is not None,stats=backend.stats,
                    pure_cf_source=backend.use_pure_cf_source,
                    n0_source=backend.use_n0_source,
                    dimensions=[1,2,3,4],dimension1_scope='independent fMPS; odd sector requires pointwise omega=0 or explicit background trivialization',
                    dimension2_scope='known q1 CA at n=0; neutral chiral direct product when w=s=0',
                    experimental_descent=experimental_descent,
                    low_dimension_status='nonsplit chiral d2 remains unsupported; d1 uses a separate fMPS coordinate')
    dimension,stage=request['dimension'],request['stage']
    if dimension not in (1,2,3,4):raise ValueError('dimension must be 1, 2, 3, or 4')
    coordinate='publication-20260930-native'
    model=backend
    if dimension<3:
        if experimental_descent:
            model=DescendedBackend(backend)
            coordinate='cone-last-descent-experimental-physical-calibration-failed'
        elif dimension==1:
            model=FMPS1Backend()
            coordinate=model.coordinate
        else:
            model=ClosedMajoranaBackend(backend,'ca')
            coordinate='closed-majorana-ca-q1-n-zero'
    if operation=='vacuum-majorana-gauge':
        result=backend.vacuum_majorana_gauge(dimension,stage,arrays(request['fields']))
    elif operation=='vacuum-fermion-gauge':
        result=backend.vacuum_fermion_gauge(dimension,stage,arrays(request['fields']))
    elif operation=='majorana-gauge-n0':
        result=backend.majorana_gauge_n0(dimension,stage,arrays(request['fields']))
    elif operation=='fermion-gauge-n0':
        result=backend.fermion_gauge_n0(dimension,stage,arrays(request['fields']))
    elif operation=='source':
        fields=arrays(request['fields'])
        if dimension==2 and not experimental_descent:
            if any(fields['n']):
                if not neutral_chiral_allowed(fields,fields):
                    raise NotImplementedError('Nonzero d2 chiral fields require constant n and w=s=0; nonsplit chiral coordinate is not validated')
                coordinate='neutral-chiral-direct-product-q1-ca'
            result=0 if stage=='majorana' else model.source(dimension,stage,fields)
        else:
            result=model.source(dimension,stage,fields)
    elif operation=='product':
        left,right,background=arrays(request['left']),arrays(request['right']),arrays(request['background'])
        if dimension==2 and not experimental_descent:
            if any(left['n']) or any(right['n']):
                if not neutral_chiral_allowed(left,background) or not neutral_chiral_allowed(right,background):
                    raise NotImplementedError('Nonzero d2 chiral fields require constant n and w=s=0; nonsplit chiral coordinate is not validated')
                coordinate='neutral-chiral-direct-product-q1-ca'
            result=0 if stage=='majorana' else model.product(dimension,stage,left,right,background)
        else:
            result=model.product(dimension,stage,left,right,background)
    else:raise ValueError('Unknown operation')
    if stage=='bosonic':
        return dict(ok=True,numerator=result.numerator,denominator=result.denominator,coordinate=coordinate)
    return dict(ok=True,value=int(result),modulus=2,coordinate=coordinate)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path)
    parser.add_argument('--native',type=Path)
    parser.add_argument('--python-only',action='store_true')
    parser.add_argument('--debug',action='store_true')
    parser.add_argument('--pure-cf-source',action='store_true',
                        help='Use the exact composed d3 source when n=a=0')
    parser.add_argument('--n0-source',action='store_true',
                        help='Use the exact composed d3 source on legal n=0 towers')
    parser.add_argument('--experimental-descent',action='store_true',
                        help='Explicitly use unvalidated cone descent for all d1/d2 requests')
    args=parser.parse_args()
    backend=Backend(args.data_dir,args.native,not args.python_only,
                    use_pure_cf_source=args.pure_cf_source,use_n0_source=args.n0_source)
    for line in sys.stdin:
        try:
            request=json.loads(line)
            result=respond(backend,request,args.experimental_descent)
            if 'id' in request:result['id']=request['id']
        except Exception as error:
            result=dict(ok=False,error=type(error).__name__,message=str(error))
            if args.debug:traceback.print_exc(file=sys.stderr)
        print(json.dumps(result,separators=(',',':')),flush=True)

if __name__=='__main__':main()
