"""Compile the supplied full p+ip O5 specification into scalar integer code.

This build tool reads mathematical expressions and the fixed Y5 coefficients
from the supplied formula bundle. The resulting GAP/Python runtime imports no
vendor engine, group package, or classification result. Exact divisions remain
checked at runtime; integer carries are not replaced by parity-only formulas.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import importlib
import json
import sys


class Scalar:
    __slots__=('builder','index')
    def __init__(self,builder,index):self.builder,self.index=builder,index
    def __add__(self,other):return self.builder.binary('add',self,other)
    __radd__=__add__
    def __mul__(self,other):return self.builder.binary('mul',self,other)
    __rmul__=__mul__
    def __neg__(self):return self*-1
    def __sub__(self,other):return self+-self.builder.scalar(other)
    def __rsub__(self,other):return self.builder.scalar(other)+-self
    def __mod__(self,modulus):return self.builder.modulo(self,modulus)
    def __floordiv__(self,divisor):return self.builder.floor(self,divisor)
    def __xor__(self,other):return (self+other)%2
    __rxor__=__xor__
    def __rpow__(self,base):
        if base!=-1:raise ValueError(base)
        return 1-2*(self%2)
    def __bool__(self):raise TypeError('Symbolic cochain must not control Python branches')


class Builder:
    def __init__(self):self.nodes=[];self.indices={};self.objects={}
    def make(self,op,*args):
        key=(op,)+args
        if key not in self.indices:
            self.indices[key]=len(self.nodes);self.nodes.append(key)
        i=self.indices[key]
        if i not in self.objects:self.objects[i]=Scalar(self,i)
        return self.objects[i]
    def scalar(self,value):return value if isinstance(value,Scalar) else self.make('const',int(value))
    def constant(self,x):
        n=self.nodes[x.index]
        return n[1] if n[0]=='const' else None
    def binary(self,op,a,b):
        a,b=self.scalar(a),self.scalar(b);av,bv=self.constant(a),self.constant(b)
        if av is not None and bv is not None:return self.scalar(av+bv if op=='add' else av*bv)
        if op=='add':
            if av==0:return b
            if bv==0:return a
        if op=='mul':
            if av==0 or bv==0:return self.scalar(0)
            if av==1:return b
            if bv==1:return a
        if a.index>b.index:a,b=b,a
        return self.make(op,a.index,b.index)
    def modulo(self,a,m):
        a=self.scalar(a);av=self.constant(a)
        if av is not None:return self.scalar(av%m)
        n=self.nodes[a.index]
        if n[0]=='mod' and n[2]==m:return a
        return self.make('mod',a.index,m)
    def divide(self,a,k):
        a=self.scalar(a);av=self.constant(a)
        if av is not None:
            if av%k:raise ArithmeticError((av,k))
            return self.scalar(av//k)
        return self.make('div',a.index,k)
    def bit(self,a,k):
        a=self.scalar(a);av=self.constant(a)
        if av is not None:return self.scalar((av>>k)&1)
        return self.make('bit',a.index,k)
    def floor(self,a,k):
        a=self.scalar(a);av=self.constant(a)
        if av is not None:return self.scalar(av//k)
        return self.make('floor',a.index,k)


def compile_pip_o5(omega_zero=True,torsion_sign=False):
    root=Path(__file__).resolve().parents[1]
    vendor=root/'vendor/p_ip_d4_normalized_package/code'
    names=('cochains','compact','polynomial_tables','ez_homotopy','explicit_pip')
    previous={name:sys.modules.pop(name,None) for name in names}
    sys.path.insert(0,str(vendor))
    B=Builder()
    try:
        cc=importlib.import_module('cochains')
        tables=importlib.import_module('polynomial_tables')
        explicit=importlib.import_module('explicit_pip')
        original_div=cc.C.div
        def div(a,k):
            if a.mod is not None:raise ValueError('Expected integral cochain')
            out=cc.C(a.deg,fun=lambda f:B.divide(a(f),k),mod=None)
            out.closed=a.closed
            return out
        cc.C.div=div
        def total_cochain(n,w,s,filename,degree,**kwargs):
            data=json.loads((vendor/filename).read_text())
            def value(face):
                ans=B.scalar(0)
                for block in data['blocks']:
                    i,j,k=block['i'],block['j'],block['k']
                    prefix=B.scalar(1)
                    for t in range(1,i+1):prefix=prefix*s((face[t-1],face[t]))
                    middle=face[i:i+j+1];last=face[i+j:]
                    # Each integer edge has its own initial-vertex frame.
                    # Transporting every edge from middle[0] changes Y5.
                    ns=[(1 if face[0]==middle[t-1] else 1-2*s((face[0],middle[t-1])))
                        *n((middle[t-1],middle[t])) for t in range(1,j+1)]
                    ws=[w((last[u-1],last[u],last[v]))^w((last[u-1],last[u],last[v-1]))
                        for u,v in combinations(range(1,k+1),2)]
                    for nc,wc in block['terms']:
                        term=prefix;nc=int(nc)
                        for e,m in enumerate(ns):
                            mask=(nc>>(4*e))&15
                            for bit in range(4):
                                if mask&(1<<bit):term=term*B.bit(m,bit)
                        for e,m in enumerate(ws):
                            if wc&(1<<e):term=term*m
                        ans=ans+term
                return ans%2
            return cc.C(degree,fun=value)
        tables.total_cochain=total_cochain
        def field(name,degree,mod=2):
            return cc.C(degree,fun=lambda f:B.make('field',name,tuple(f)),mod=mod)
        n,b,c,s=field('n',1,None),field('b',2),field('c',3),field('s',1)
        w=cc.C(2) if omega_zero else field('w',2)
        s.closed=True;w.closed=True
        if torsion_sign:
            if not omega_zero:raise ValueError('Sign specialization requires omega=0')
            # At n=s, h=0, Xi(s)=0, and the full pure integer phase is
            # 9*s^5/16. The last two identities are checked on EVERY local
            # sign simplex against the unspecialized supplied specification.
            O=explicit.sum_terms(explicit.gamma_terms16(b,w,s),5)
            O=O+cc.sq(c,2).lift().scaled(8)
            power=s
            for _ in range(4):power=cc.cup(power,s)
            O=O+power.lift().scaled(9)
        else:O=explicit.O5(n,b,c,w,s)
        output=O(tuple(range(6)))%16
        # Retain only nodes reachable from the result, in dependency order.
        active=set()
        def mark(i):
            if i in active:return
            active.add(i);item=B.nodes[i]
            if item[0] in ('add','mul'):mark(item[1]);mark(item[2])
            elif item[0] in ('mod','div','bit','floor'):mark(item[1])
        mark(output.index)
        indices={old:new for new,old in enumerate(sorted(active))};program=[]
        for old in sorted(active):
            item=list(B.nodes[old]);op=item[0]
            if op in ('add','mul'):item[1]=indices[item[1]];item[2]=indices[item[2]]
            elif op in ('mod','div','bit','floor'):item[1]=indices[item[1]]
            program.append(item)
        return {'formula':'O5 p+ip, normalized manuscript coordinate','denominator':16,
                'omega_zero':omega_zero,'fields':{'n':1,'b':2,'c':3,'s':1,**({} if omega_zero else {'w':2})},
                'program':program,'output':indices[output.index],
                'torsion_sign':torsion_sign,
                'source':'p_ip_d4_normalized_package/code/explicit_pip.py + Y5_word_total.json'}
    finally:
        sys.path.remove(str(vendor))
        for name in names:
            sys.modules.pop(name,None)
            if previous[name] is not None:sys.modules[name]=previous[name]


def evaluate_program(program,fields):
    values=[]
    for node in program['program']:
        op=node[0]
        if op=='const':value=node[1]
        elif op=='field':
            f=fields[node[1]];face=tuple(node[2]);value=f(face) if callable(f) else f[face]
        elif op=='add':value=values[node[1]]+values[node[2]]
        elif op=='mul':value=values[node[1]]*values[node[2]]
        elif op=='mod':value=values[node[1]]%node[2]
        elif op=='bit':value=(values[node[1]]>>node[2])&1
        elif op=='floor':value=values[node[1]]//node[2]
        elif op=='div':
            value,remainder=divmod(values[node[1]],node[2])
            if remainder:raise ArithmeticError(('invalid lower cochain quotient',node))
        else:raise ValueError(op)
        values.append(value)
    return values[program['output']]


def main():
    from .formulas_export import gap_literal
    root=Path(__file__).resolve().parents[1]
    program=compile_pip_o5()
    (root/'gap/pip_o5_program.json').write_text(json.dumps(program,separators=(',',':'))+'\n')
    # GAP stores the same zero-based graph indices; runtime adds one.
    content='AFSPipO5Program := '+gap_literal(program['program'])+';;\n'
    content+='AFSPipO5Output := '+str(program['output']+1)+';;\n'
    (root/'gap/pip_o5_program.g').write_text(content)
    print('Compiled full p+ip O5, omega=0:',len(program['program']),'scalar operations')
    compile_sign_files()


def compile_sign_files():
    """Emit the exact n=s straight-line specialization, retaining generic O5."""
    root=Path(__file__).resolve().parents[1];program=compile_pip_o5(torsion_sign=True)
    (root/'gap/pip_o5_sign.json').write_text(json.dumps(program,separators=(',',':'))+'\n')
    lines=['# Exact n=s specialization of complete O5: no target-group choices.',
           'AFSPipO5SignProgram := function(f,t)','local v;v:=[];']
    for i,item in enumerate(program['program']):
        op,*args=item
        if op=='const':rhs=str(args[0])
        elif op=='field':
            name,face=args
            rhs='f.%s(%s)'%(name,','.join('t[%d][%d]'%(a+1,b+1) for a,b in zip(face,face[1:])))
        elif op=='add':rhs='v[%d]+v[%d]'%(args[0]+1,args[1]+1)
        elif op=='mul':rhs='v[%d]*v[%d]'%(args[0]+1,args[1]+1)
        elif op=='mod':rhs='v[%d] mod %d'%(args[0]+1,args[1])
        elif op=='div':
            value='v[%d]'%(args[0]+1)
            lines.append('if %s mod %d<>0 then Error("Nonintegral sign O5 quotient");fi;'%(value,args[1]))
            rhs='QuoInt(%s,%d)'%(value,args[1])
        else:raise ValueError(op)
        lines.append('v[%d]:=%s;'%(i+1,rhs))
    lines.append('return v[%d]/16;end;;'%(program['output']+1))
    (root/'gap/pip_o5_sign.g').write_text('\n'.join(lines)+'\n')
    print('Compiled complete p+ip O5 at n=s:',len(program['program']),'scalar operations')


if __name__=='__main__':main()
