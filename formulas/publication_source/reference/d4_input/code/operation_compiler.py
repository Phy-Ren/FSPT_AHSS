"""Reconstruct the residual operation DAG from the readable Python formula.

No simplex evaluation or sample is used. Equality means equality of expression
DAGs, including every signed interval-cut table (modulo binary coefficient signs).
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
import cochains as cc
pool={};expressions=[]
def intern(key):
    if key not in pool:pool[key]=len(expressions);expressions.append(key)
    return pool[key]

def canonical_cuts(terms,mod,overall=1):
    return tuple((sign*overall if mod!=2 else 1,faces) for faces,sign in terms)

class Scalar:
    def __init__(self,cochain):self.c=cochain
    def __floordiv__(self,n):return Scalar(T.make(6,self.c.deg,None,(self.c.node,),(n,)))

class T:
    def __init__(self,degree,values=None,fun=None,mod=2,node=None):
        self.deg=degree;self.mod=mod
        if node is not None:self.node=node
        elif fun is not None:
            value=fun(tuple(range(degree+1)))
            if not isinstance(value,Scalar):raise TypeError(value)
            self.node=intern((4,degree,mod,(value.c.node,),()))
        else:
            if values not in (None,{}):raise ValueError('unexpected literal cochain')
            self.node=intern((0,degree,mod,(),()))
        self.known_zero=expressions[self.node][0]==0
        self.closed=self.known_zero
    @classmethod
    def make(cls,op,degree,mod,children=(),params=()):
        return cls(degree,mod=mod,node=intern((op,degree,mod,tuple(children),tuple(params))))
    def __call__(self,face):return Scalar(self)
    def __add__(self,other):
        assert self.deg==other.deg and self.mod==other.mod
        if self.known_zero:return other
        if other.known_zero:return self
        out=T.make(1,self.deg,self.mod,(self.node,other.node));out.closed=self.closed and other.closed;return out
    def __sub__(self,other):
        assert self.deg==other.deg and self.mod==other.mod
        if other.known_zero:return self
        out=T.make(2,self.deg,self.mod,(self.node,other.node));out.closed=self.closed and other.closed;return out
    def scaled(self,k):
        if not k or self.known_zero:return T(self.deg,mod=self.mod)
        out=T.make(3,self.deg,self.mod,(self.node,),(k,));out.closed=self.closed;return out
    def reduce(self,mod):
        if self.known_zero:return T(self.deg,mod=mod)
        out=T.make(4,self.deg,mod,(self.node,));out.closed=self.closed and self.mod is None;return out
    def lift(self):return self.reduce(None)
    def div(self,k):
        assert self.mod is None
        if self.known_zero:return T(self.deg,mod=None)
        out=T.make(5,self.deg,None,(self.node,),(k,));out.closed=self.closed;return out
    def d(self):
        if self.closed:return T(self.deg+1,mod=self.mod)
        out=T.make(7,self.deg+1,self.mod,(self.node,));out.closed=True;return out

def traced_cup(a,b,i=0,s=None,twists=(0,0)):
    assert a.mod==b.mod
    degree=a.deg+b.deg-i
    if i<0 or a.known_zero or b.known_zero:return T(degree,mod=a.mod)
    word=tuple(1+j%2 for j in range(i+2))
    terms=cc.interval_terms(word,(a.deg,b.deg))
    overall=(-1)**((i*(a.deg+b.deg)+i*(i-1)//2)%2)
    cuts=canonical_cuts(terms,a.mod,overall)
    out=T.make(8,degree,a.mod,(a.node,b.node,-1 if s is None else s.node),(cuts,)+twists)
    out.closed=(a.closed and b.closed and (i==0 or (a is b and a.mod==2))) and s is None
    return out

def traced_word(word,*args):
    w=tuple(map(int,word));degrees=tuple(a.deg for a in args);degree=sum(degrees)-len(w)+len(args)
    if any(a.known_zero for a in args):return T(degree)
    terms=cc.interval_terms(w,degrees)
    return T.make(9,degree,2,tuple(a.node for a in args),(canonical_cuts(terms,2),))



def compile_new_residual(filename='word_residual_program.txt'):
    """Compile the displayed residual itself into finite signed interval cuts."""
    import compact,explicit_pip
    modules=[cc,compact,explicit_pip];saved=[]
    for module in modules:
        for name,replacement in [('C',T),('cup',traced_cup),('op',traced_word)]:
            if hasattr(module,name):saved.append((module,name,getattr(module,name)));setattr(module,name,replacement)
    try:
        n=T.make(10,2,None);w=T.make(11,2,2);s=T.make(12,1,2)
        root=explicit_pip.residual(n,w,s).node
    finally:
        for module,name,value in saved:setattr(module,name,value)
    # Discard unreferenced nodes so the program is an explicit minimal dependency DAG.
    active=set()
    def visit(i):
        if i<0 or i in active:return
        active.add(i)
        for c in expressions[i][3]:visit(c)
    visit(root);order=sorted(active);remap={old:new for new,old in enumerate(order)}
    tables=[];table_index={};rows=[]
    for old in order:
        op,degree,mod,ch,pa=expressions[old];ch=tuple(remap[c] if c>=0 else -1 for c in ch)
        if op in (8,9):
            cuts=pa[0]
            if cuts not in table_index:table_index[cuts]=len(tables);tables.append((2 if op==8 else len(ch),cuts))
            pa=(table_index[cuts],)+pa[1:]
        rows.append(' '.join(map(str,(op,degree,mod or 0,len(ch),*ch,len(pa),*pa))))
    output=[f'{len(rows)} {len(tables)} {remap[root]}',*rows]
    for arity,cuts in tables:
        output.append(f'{arity} {len(cuts)}')
        for sign,faces in cuts:
            data=[sign]
            for face in faces:data.extend((len(face),*face))
            output.append(' '.join(map(str,data)))
    path=ROOT/filename;path.write_text('\n'.join(output)+'\n')
    report={'source':'explicit_pip.residual','nodes':len(rows),'signed_interval_cut_tables':len(tables),
            'compilation':'Direct operation-DAG trace; no fitted values',
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT/'word_program_certificate.json').write_text(json.dumps(report,indent=2))
    print(report)
    return report

if __name__=='__main__':compile_new_residual()
