"""Compile the calibrated diagonal p+ip product on universal legal simplices.

The optional reference checkout is a mathematical formula oracle for this
DERIVATION only. Neither the generated evaluator nor any SG computation imports
it. Keys encode 4 orientation bits, 6 Majorana cone faces, and 4 CF cone faces.
Every value is evaluated with exact rational arithmetic. Source inputs are the
user's normalized first three layers, translated to the reference CF coordinate.
"""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from fractions import Fraction
import argparse
import gc
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fspt.formulas import evaluate,formula,pip_cf_coordinate


def legal_tower(sign_bits, b_bits, c_bits):
    eps=[0]+[(sign_bits>>i)&1 for i in range(4)]
    def s(f):return (eps[f[0]]+eps[f[1]])%2
    bv={(0,)+f:(b_bits>>i)&1 for i,f in enumerate(combinations(range(1,5),2))}
    @lru_cache(None)
    def b(f):
        if len(set(f))<3:return 0
        if 0 in f:return bv[f]
        return (s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))
                +sum(bv[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
    fields={'n':s,'b':b,'s':s,'w':lambda f:0}
    cv={(0,)+f:(c_bits>>i)&1 for i,f in enumerate(combinations(range(1,5),3))}
    @lru_cache(None)
    def c(f):
        if len(set(f))<4:return 0
        if 0 in f:return cv[f]
        return (evaluate(formula('pip_parity',1),fields,(0,)+f)
                +sum(cv[(0,)+f[:i]+f[i+1:]] for i in range(4)))%2
    @lru_cache(None)
    def cref(f):return (c(f)+pip_cf_coordinate(1,b,s,f))%2
    return s,b,c,cref


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--reference-root',required=True,type=Path)
    parser.add_argument('--sign',type=int,required=True)
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--count',type=int,default=1024)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--trace',action='store_true')
    parser.add_argument('--batch-c',action='store_true',help='Evaluate all16 free CF coordinates in one exact vector pass')
    args=parser.parse_args();ref=args.reference_root.resolve()
    if args.trace:
        import faulthandler
        faulthandler.dump_traceback_later(30,repeat=True)
    sys.path.insert(0,str(ref/'python'/'stacking_model'))
    sys.path.insert(0,str(ref/'python'))
    import production_gamma4 as product
    p=product.p
    if args.batch_c:
        import numpy as np
        import cochain_tools as ct
        import cochains as cc
        def batch_word(module):
            def word_op(word,*cochains,integral_index=None):
                degree=sum(c.degree for c in cochains)-(len(word)-len(cochains))
                terms=module.cut_terms(word,tuple(c.degree for c in cochains),integral_index)
                def value(z):
                    out=0
                    for faces,weight in terms:
                        term=weight
                        for c,f in zip(cochains,faces):
                            term=term*c(tuple(z[j] for j in f))
                            if isinstance(term,(int,Fraction)) and term==0:break
                        out=out+term
                    return out if integral_index is not None else out%2
                return module.Cochain(degree,value)
            return word_op
        ct.word_op=batch_word(ct);p.word_op=ct.word_op;cc.word_op=batch_word(cc)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ref,text=True).strip() if (ref/'.git').exists() else (ref/'ORACLE_REVISION').read_text().strip()
    records=[];beta_values=[];started=time.time()
    limit=64 if args.batch_c else 1024
    for index in range(args.start,min(limit,args.start+args.count)):
        b_bits=index%64;c_bits=np.arange(16,dtype=np.int64) if args.batch_c else index//64
        s,b,c,cref=legal_tower(args.sign,b_bits,c_bits)
        A=p.Cochain(1,s);B=p.Cochain(2,b);C=p.Cochain(3,cref);S=A;W=p.zero(2)
        phase=product.phase4(A,B,C,A,B,C,S,W)((0,1,2,3,4))
        values=np.broadcast_to(phase,(16,)) if args.batch_c else [phase]
        nums=[]
        for value in values:
            value=Fraction(value)%1
            if (16*value).denominator!=1:raise ArithmeticError(('unexpected denominator',value))
            nums.append(int(16*value))
        records.append(nums if args.batch_c else nums[0])
        beta=product.upper.beta_sharp(A,B,A,B,S,W)((0,1,2,3))
        beta_values.append(int(beta));gc.collect()
        if index<args.start+3 or index%16==15:
            print(json.dumps(dict(sign=args.sign,index=index,numerator=records[-1],elapsed_s=time.time()-started)),flush=True)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(dict(reference_revision=revision,
        formula='production_gamma4.phase4 diagonal n=s,omega=0',
        input_coordinate='normalized CF followed by Lambda1',
        output_coordinate='reference n=2s,B=0',
        sign=args.sign,start=args.start,batched_CF=args.batch_c,modulus=16,numerators=records,beta_reference_0123=beta_values,
        elapsed_s=time.time()-started),indent=2)+'\n')

if __name__=='__main__':main()
