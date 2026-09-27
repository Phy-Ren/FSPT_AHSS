"""Compile the independently transcribed formulas to straight-line GAP code.

Both general backgrounds and omega=0 specializations are emitted. Every face restriction, signed interval cut,
canonical lift and exact quotient remains in the compiled arithmetic.
"""
from functools import lru_cache
from pathlib import Path
from .formulas import formula,cuts
from .formulas_pip_compile import Builder


def compile_expression(expression,zero_fields=('w',)):
    B=Builder()
    @lru_cache(None)
    def visit(x,f):
        op,args=x.operation,x.arguments
        if op=='zero':v=B.scalar(0)
        elif op=='field':v=B.scalar(0) if args[0] in zero_fields else B.make('field',args[0],f)
        elif op=='add':v=visit(args[0],f)+visit(args[1],f)
        elif op=='scale':v=args[1]*visit(args[0],f)
        elif op=='reduce':v=visit(args[0],f)
        elif op=='divide':v=B.divide(visit(args[0],f),args[1])
        elif op=='d':v=sum((-1)**i*visit(args[0],f[:i]+f[i+1:]) for i in range(len(f)))
        elif op=='word':
            labels,inputs=args;v=B.scalar(0)
            for fs,sign in cuts(labels,tuple(y.degree for y in inputs)):
                term=B.scalar(sign if x.modulus is None else 1)
                for y,face in zip(inputs,fs):term=term*visit(y,tuple(f[j] for j in face))
                v=v+term
        else:raise ValueError(op)
        return v%x.modulus if x.modulus is not None else v
    result=visit(expression,tuple(range(expression.degree+1)))
    active=set()
    def mark(i):
        if i in active:return
        active.add(i);op,*args=B.nodes[i]
        if op in ('add','mul'):mark(args[0]);mark(args[1])
        elif op in ('mod','div','floor','bit'):mark(args[0])
    mark(result.index)
    return B,result.index,sorted(active)


def main():
    root=Path(__file__).resolve().parents[1]
    lines=['# Generated straight-line exact arithmetic; no lookup of phase values.',
           'AFSFastPrograms := rec();;']
    counts={}
    for name in ('obstruction','stacking','majorana_source','majorana_product','pip_majorana','pip_parity'):
        for p in (1,2):
            zerosets=[(),('s',),('w',),('w','s')]
            if name=='obstruction':zerosets += [('a',),('a','s'),('w','a'),('w','a','s')]
            for zeros in zerosets:
                expression=formula(name,p);B,result,active=compile_expression(expression,zeros)
                ids={old:i+1 for i,old in enumerate(active)}
                key='%s_%d_%s'%(name,p,''.join(zeros));counts[key]=len(active)
                lines.append('AFSFastPrograms.%s := function(f,t)'%key)
                lines.append('local v;v:=[];')
                for old in active:
                    op,*args=B.nodes[old];lhs='v[%d]'%ids[old]
                    if op=='const':rhs=str(args[0])
                    elif op=='field':
                        field,face=args
                        text=','.join('t[%d][%d]'%(i+1,j+1) for i,j in zip(face,face[1:]))
                        rhs='f.%s(%s)'%(field,text)
                    elif op=='add':rhs='v[%d]+v[%d]'%(ids[args[0]],ids[args[1]])
                    elif op=='mul':rhs='v[%d]*v[%d]'%(ids[args[0]],ids[args[1]])
                    elif op=='mod':rhs='v[%d] mod %d'%(ids[args[0]],args[1])
                    elif op=='div':
                        value='v[%d]'%ids[args[0]]
                        lines.append('if %s mod %d<>0 then Error("Nonintegral compiled formula quotient");fi;'%(value,args[1]))
                        rhs='QuoInt(%s,%d)'%(value,args[1])
                    else:raise ValueError(op)
                    lines.append(lhs+':='+rhs+';')
                denominator=8 if name in ('obstruction','stacking') else 1
                lines.append('return v[%d]/%d;end;;'%(ids[result],denominator))
    (root/'gap/formula_fast.g').write_text('\n'.join(lines)+'\n')
    print(counts)


if __name__=='__main__':main()
