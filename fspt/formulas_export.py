"""Compile the independent formula expression graphs into literal GAP data."""
from pathlib import Path
from .formulas import Cochain, cuts, formula


def encode(expression):
    ordered=[]; ids={}
    def visit(x):
        if x in ids:return ids[x]
        op,args=x.operation,x.arguments
        if op in ('zero','field'):data=list(args)
        elif op in ('add','scale','divide'):
            data=[visit(args[0]),visit(args[1]) if isinstance(args[1],Cochain) else args[1]]
        elif op in ('reduce','d'):data=[visit(args[0])]
        elif op=='word':
            labels,inputs=args
            data=[[visit(a) for a in inputs],
                  [[[[j+1 for j in f] for f in fs],sg]
                   for fs,sg in cuts(labels,tuple(a.degree for a in inputs))]]
        else:raise ValueError(op)
        ordered.append([op,x.degree,x.modulus or 0,data]);ids[x]=len(ordered)
        return ids[x]
    root=visit(expression)
    return [root,expression.degree,expression.modulus or 0,ordered]


def gap_literal(value):
    if isinstance(value,str):return '"'+value.replace('\\','\\\\').replace('"','\\"')+'"'
    if isinstance(value,(tuple,list)):return '['+','.join(gap_literal(x) for x in value)+']'
    return str(value)


def main():
    root=Path(__file__).resolve().parents[1]
    names=('majorana_source','majorana_product','obstruction','stacking','pip_majorana','pip_parity')
    lines=['# Generated from fspt/formulas.py; exact coefficients, no classification results.',
           'AFSFormulaData := rec();;']
    for name in names:
        for p in (1,2):
            lines.append('AFSFormulaData.%s_%d := %s;;'%(name,p,gap_literal(encode(formula(name,p)))))
    # Generic binary operations used by the independent stacking reduction.
    lines.append('AFSCupData := rec();;')
    for p in range(0,6):
        for q in range(0,6):
            for i in range(0,min(p,q)+1):
                terms=cuts(tuple(1+j%2 for j in range(i+2)),(p,q))
                data=[[[[j+1 for j in f] for f in fs],sg] for fs,sg in terms]
                lines.append('AFSCupData.c%d_%d_%d := %s;;'%(i,p,q,gap_literal(data)))
    (root/'gap'/'formula_data.g').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':main()
