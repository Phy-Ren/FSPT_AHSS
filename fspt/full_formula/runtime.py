"""Standalone exact evaluator of all 3+1D and 4+1D publication formulas.

There is no import from the supplied package. The arithmetic DAGs are immutable
build artifacts; the finite normalized chain-transfer algorithms below operate
on face arrays. Physical input fields use the native Majorana coordinate.
"""
from __future__ import annotations
from ctypes import CDLL, POINTER, c_int64
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from operator import itemgetter
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEGREES = (1,2,2,3,2,3)  # s,w,n0,u0,m0,v0 in the transfer chart
OPCODES = dict(const=0,field=1,add=2,mul=3,mod=4,div=5,floor=6,bit=7)


class State(tuple):
    """Immutable chart state with a cached hash for repeated chain lookups."""
    def __new__(cls, values):
        result=tuple.__new__(cls, values)
        result.cached_hash=tuple.__hash__(result)
        return result
    def __hash__(self):
        return self.cached_hash


@lru_cache(None)
def faces(d,q):
    return tuple(combinations(range(d+1),q+1))


@lru_cache(None)
def face_masks(d,q):
    return tuple(sum(1<<j for j in f) for f in faces(d,q))


@lru_cache(None)
def face_index(d,q):
    return {f:i for i,f in enumerate(faces(d,q))}


def full_array(d,q,values):
    """Expand one degree's ordered tuple to the public mask-indexed format."""
    out=[0]*(1<<(d+1))
    for mask,value in zip(face_masks(d,q),values):
        out[mask]=value
    return tuple(out)


def restriction(values,projection):
    """Pull back a normalized mask array along an ordered vertex map."""
    d=len(projection)-1
    out=[0]*(1<<(d+1))
    for mask in range(1,len(out)):
        selected=[projection[j] for j in range(d+1) if mask&(1<<j)]
        if len(set(selected))==len(selected):
            out[mask]=values[sum(1<<j for j in selected)]
    return tuple(out)


@lru_cache(maxsize=4096)
def closed_background(d,w,s):
    """Preserve the reference evaluator's domain for local source packets."""
    for degree,values in ((2,w),(1,s)):
        for face in faces(d,degree+1):
            mask=sum(1<<j for j in face)
            if sum(values[mask^(1<<j)] for j in face)%2:
                return False
    return True


class Program:
    def __init__(self,path,native=None):
        self.data=json.loads(Path(path).read_text())
        self.nodes=self.data['program']
        self.outputs=self.data['outputs']
        self.slots=[]
        slots={}
        flat=[]
        for node in self.nodes:
            op=node[0]
            if op=='field':
                key=(node[1],sum(1<<j for j in node[2]))
                if key not in slots:
                    slots[key]=len(self.slots);self.slots.append(key)
                flat.extend((1,slots[key],0))
            else:
                flat.extend((OPCODES[op],node[1],node[2] if len(node)>2 else 0))
        self.native=native
        if native is not None:
            self.native_nodes=(c_int64*len(flat))(*flat)
            self.native_outputs=(c_int64*len(self.outputs))(*self.outputs)

    def __call__(self,fields):
        inputs=[fields[name][mask] for name,mask in self.slots]
        if any(isinstance(x,bool) or not isinstance(x,int) for x in inputs):
            raise TypeError('Formula fields must contain exact integers')
        if self.native is not None and all(-(1<<63)<=x<(1<<63) for x in inputs):
            packed=(c_int64*len(inputs))(*inputs)
            output=(c_int64*len(self.outputs))()
            bad=c_int64(-1)
            status=self.native(self.native_nodes,len(self.nodes),packed,len(inputs),
                               self.native_outputs,len(self.outputs),output,bad)
            if status==0:
                return list(output)
            if status==-3:
                raise ArithmeticError(('Nonintegral lower-tower quotient',self.data['name'],bad.value))
            if status!=-2:
                raise RuntimeError(('Invalid compiled instruction',self.data['name'],bad.value,status))
        return self.evaluate_python(inputs)

    def evaluate_python(self,inputs):
        field_values=dict(zip(self.slots,inputs))
        values=[]
        for node in self.nodes:
            op=node[0]
            if op=='const':v=node[1]
            elif op=='field':v=field_values[node[1],sum(1<<j for j in node[2])]
            elif op=='add':v=values[node[1]]+values[node[2]]
            elif op=='mul':v=values[node[1]]*values[node[2]]
            elif op=='mod':v=values[node[1]]%node[2]
            elif op=='floor':v=values[node[1]]//node[2]
            elif op=='bit':v=(values[node[1]]>>node[2])&1
            elif op=='div':
                v,r=divmod(values[node[1]],node[2])
                if r:raise ArithmeticError(('Nonintegral lower-tower quotient',self.data['name'],node))
            else:raise ValueError(op)
            values.append(v)
        return [values[j] for j in self.outputs]


@lru_cache(None)
def shuffles3(n):
    out=[]
    for a in range(n+1):
        for b in range(a,n+1):
            counts=[a,b-a,n-b]
            path=[(0,a,b)]
            def walk():
                if not any(counts):out.append(tuple(path));return
                for j in range(3):
                    if counts[j]:
                        counts[j]-=1
                        v=list(path[-1]);v[j]+=1;path.append(tuple(v))
                        walk();path.pop();counts[j]+=1
            walk()
    return tuple(out)


@lru_cache(None)
def ez_homotopy(n):
    if n==0:return ()
    origin=(0,0,0)
    out=set()
    for simplex in shuffles3(n):
        if simplex[0]!=origin:
            out.symmetric_difference_update(((origin,)+simplex,))
    for simplex in ez_homotopy(n-1):
        out.symmetric_difference_update(((origin,)+tuple(tuple(c+1 for c in v) for v in simplex),))
    return tuple(sorted(out))


@lru_cache(None)
def transfer_cuts(n,first_background_step=False):
    out=[]
    for simplex in ez_homotopy(n):
        if first_background_step and simplex[0][0]==simplex[1][0]:continue
        projections=tuple(tuple(v[j] for v in simplex) for j in range(3))
        if min(len(set(projections[j])) for j in (1,2))>=3:
            out.append(projections)
    return tuple(out)


def xor_insert(chain,value):
    if value in chain:chain.remove(value)
    else:chain.add(value)


@lru_cache(None)
def pull_indices(d,q,projection):
    index=face_index(d,q)
    result=[]
    for f in faces(len(projection)-1,q):
        g=tuple(projection[i] for i in f)
        result.append(-1 if len(set(g))<len(g) else index[g])
    return tuple(result)


@lru_cache(None)
def pull_getter(d,q,projection):
    indices=pull_indices(d,q,projection)
    if not indices:return lambda values: ()
    length=len(faces(d,q))
    getter=itemgetter(*(length if i<0 else i for i in indices))
    if len(indices)==1:return lambda values: (getter(values),)
    return getter


@lru_cache(maxsize=50000)
def state_pull(state,projections):
    d=state[0];nd=len(projections[0])-1
    arrays=[]
    for j,q in enumerate(DEGREES):
        projection=projections[0 if j<2 else 1 if j<4 else 2]
        arr=state[j+1]
        getter=pull_getter(d,q,projection)
        arrays.append(getter(arr+(0,)))
    return State((nd,)+tuple(arrays))


def state_face(state,j):
    p=tuple(i for i in range(state[0]+1) if i!=j)
    return state_pull(state,(p,p,p))


@lru_cache(maxsize=50000)
def normalized(state):
    d=state[0]
    if (not any(state[3]) and not any(state[4])) or (not any(state[5]) and not any(state[6])):
        return False
    for j in range(d):
        p=tuple(i if i<=j else i-1 for i in range(d+1))
        if state_pull(state_face(state,j+1),(p,p,p))==state:return False
    return True


def encode(d,n,u,m,v,w,s):
    """Enter the shared-background chart; all arguments are mask arrays."""
    def one(ni,ui):
        normal=[];upper=[]
        for f,mask in zip(faces(d,2),face_masks(d,2)):
            normal.append(ni[mask]*(1 if f[0]==0 else 1-2*s[(1<<f[0])|1]))
        for f,mask in zip(faces(d,3),face_masks(d,3)):
            correction=0
            if f[0]:
                W=w[1|(1<<f[0])|(1<<f[1])]^(
                    s[1|(1<<f[0])]&s[(1<<f[0])|(1<<f[1])])
                correction=W*(ni[sum(1<<j for j in f[1:])]%2)
            upper.append(ui[mask]^correction)
        return tuple(normal),tuple(upper)
    nn,uu=one(n,u);mm,vv=one(m,v)
    return State((d,tuple(s[j] for j in face_masks(d,1)),tuple(w[j] for j in face_masks(d,2)),nn,uu,mm,vv))


def decode(state):
    d=state[0]
    s,w,n0,u0,m0,v0=(full_array(d,q,a) for q,a in zip(DEGREES,state[1:]))
    def one(ni,ui):
        n=list(ni);u=list(ui)
        for f,mask in zip(faces(d,2),face_masks(d,2)):
            if f[0]:n[mask]*=1-2*s[1|(1<<f[0])]
        for f,mask in zip(faces(d,3),face_masks(d,3)):
            if f[0]:
                W=w[1|(1<<f[0])|(1<<f[1])]^(
                    s[1|(1<<f[0])]&s[(1<<f[0])|(1<<f[1])])
                u[mask]^=W*(n[sum(1<<j for j in f[1:])]%2)
        return tuple(n),tuple(u)
    n,u=one(n0,u0);m,v=one(m0,v0)
    return dict(n=n,a=u,m=m,b=v,w=w,s=s)


@lru_cache(maxsize=50000)
def delta(state):
    d=state[0]
    if d<=2 or (not any(state[1]) and not any(state[2])):return ()
    plain=state_face(state,0)
    fields=decode(state)
    p=tuple(range(1,d+1))
    fields={k:restriction(v,p) for k,v in fields.items()}
    twisted=encode(d-1,fields['n'],fields['a'],fields['m'],fields['b'],fields['w'],fields['s'])
    if twisted==plain:return ()
    return tuple(x for x in (plain,twisted) if normalized(x))


@lru_cache(maxsize=3000)
def homotopy_chain(state):
    out=set()
    for projections in transfer_cuts(state[0]):
        pulled=state_pull(state,projections)
        if normalized(pulled):xor_insert(out,pulled)
    return frozenset(out)


def delta_homotopy(chain):
    out=set()
    for state in chain:
        if not any(state[1]) and not any(state[2]):continue
        for projections in transfer_cuts(state[0],True):
            pulled=state_pull(state,projections)
            if normalized(pulled):
                for term in delta(pulled):xor_insert(out,term)
    return out


@lru_cache(None)
def degeneracy_tests(d,q,i):
    zero=[];equal=[]
    pair=(1<<i)|(1<<(i+1))
    for mask in face_masks(d,q):
        if mask&pair==pair:zero.append(mask)
        elif mask&(1<<(i+1)) and not mask&(1<<i):
            equal.append((mask,mask^pair))
    return tuple(zero),tuple(equal)


def degenerate_fields(d,items):
    for i in range(d):
        valid=True
        for degree,values in items:
            zero,equal=degeneracy_tests(d,degree,i)
            if any(values[k] for k in zero) or any(values[a]!=values[b] for a,b in equal):
                valid=False;break
        if valid:return True
    return False


class Backend:
    def __init__(self,data_dir=None,native_path=None,use_native=True,use_specializations=True,
                 use_pure_cf_source=False,use_n0_source=False):
        self.data_dir=Path(data_dir or ROOT/'fspt/data/full_formula')
        self.programs={}
        self.use_specializations=use_specializations
        self.use_pure_cf_source=use_pure_cf_source
        self.use_n0_source=use_n0_source
        self.native=None
        if use_native:
            path=Path(native_path or Path(__file__).with_name('native.so'))
            if path.exists():
                library=CDLL(str(path))
                self.library=library
                self.native=library.fspt_formula_eval
                self.native.argtypes=[POINTER(c_int64),c_int64,POINTER(c_int64),c_int64,
                                      POINTER(c_int64),c_int64,POINTER(c_int64),POINTER(c_int64)]
                self.native.restype=int
        self.stats=dict(program_calls=0,source_calls=0,product_calls=0,
                        transfer_states=0,residual_calls=0,specialized_product_calls=0,
                        specialized_pure_cf_source_calls=0,specialized_n0_source_calls=0)

    def program(self,name,fields):
        if name not in self.programs:
            self.programs[name]=Program(self.data_dir/(name+'.json'),self.native)
        self.stats['program_calls']+=1
        return self.programs[name](fields)

    def shift(self,dimension,fields):
        p=dimension-2
        a=list(fields['a'])
        d=(len(a).bit_length()-1)-1
        for f,mask in zip(faces(d,p+1),face_masks(d,p+1)):
            edge=(1<<f[0])|(1<<f[1])
            tail=sum(1<<j for j in f[1:])
            a[mask]^=fields['s'][edge]*((fields['n'][tail]//2)%2)
        return dict(fields,a=tuple(a))

    @lru_cache(maxsize=12000)
    def y6(self,n,w,s):
        if not any(n) or degenerate_fields(6,((2,n),(2,w),(1,s))):return 0
        return self.program('y6',dict(n=n,w=w,s=s))[0]%2

    @lru_cache(maxsize=12000)
    def h6(self,n,a,w,s):
        if degenerate_fields(6,((2,n),(3,a),(2,w),(1,s))):return 0
        y=[0]*128;y[127]=self.y6(n,w,s)
        return self.program('h6',dict(n=n,a=a,w=w,s=s,y=y))[0]%2

    def high6(self,fields):
        f=dict(fields);y=[0]*128
        y[127]=self.y6(tuple(f['n']),tuple(f['w']),tuple(f['s']))
        f['y']=y
        return self.program('high6',f)

    def suspended(self,operation,fields):
        name='lift3_'+operation
        outputs=self.program(name,fields)
        metadata=self.programs[name].data
        result=0
        for call in metadata['calls']:
            offset=call['offset'];values={}
            for field,degree in zip(metadata['high_fields'],metadata['high_degrees']):
                count=len(faces(6,degree))
                values[field]=full_array(6,degree,outputs[offset:offset+count]);offset+=count
            result+=call['sign']*self.high6(values)[0]
        return result%16

    @lru_cache(maxsize=12000)
    def rho4(self,state):
        if not normalized(state):return 0
        self.stats['residual_calls']+=1
        fields=decode(state)
        values=self.program('rho4',fields)
        N=tuple(x+y for x,y in zip(fields['n'],fields['m']))
        U=full_array(6,3,values[1:])
        w,s=fields['w'],fields['s']
        return (values[0]^self.h6(N,U,w,s)^self.h6(fields['n'],fields['a'],w,s)
                ^self.h6(fields['m'],fields['b'],w,s))%2

    def tensor4(self,state):
        fields={name:full_array(5,q,state[j]) for name,q,j in
                (('n',2,3),('a',3,4),('m',2,5),('b',3,6))}
        value=self.program('tensor4',fields)[0]
        s=full_array(5,1,state[1]);n=full_array(5,2,state[3]);m=full_array(5,2,state[5])
        x=n[(1<<1)|(1<<2)|(1<<3)];y=m[(1<<3)|(1<<4)|(1<<5)]
        a,h,g=x%2,(x//2)%2,(x//4)%2
        b,k,l=y%2,(y//2)%2,(y//4)%2
        negation=((a+h)*k*(1+b)+h*(b+l)+g*b*(1+k))%2
        return (value+s[3]*negation)%2

    @lru_cache(maxsize=3000)
    def binary4(self,state):
        if not normalized(state):return 0
        answer=0;chain={state}
        for iteration in range(6):
            if not chain:return answer%2
            hchain=set()
            for term in chain:
                self.stats['transfer_states']+=1
                answer^=self.tensor4(term)
                for pulled in homotopy_chain(term):xor_insert(hchain,pulled)
            for pulled in hchain:answer^=self.rho4(pulled)
            chain=delta_homotopy(chain)
        if chain:raise ArithmeticError('Background filtration did not terminate after six steps')
        return answer%2

    @lru_cache(maxsize=2048)
    def source3_n0_lower(self,a,w,s):
        """Exact local domain certificate, cached independently of c."""
        if not closed_background(5,w,s):return None
        for face in faces(5,3):
            mask=sum(1<<j for j in face)
            if sum(a[mask^(1<<j)] for j in face)%2:return None
        return tuple(value%2 for value in self.program('source3_majorana_n0_lower',dict(a=a,w=w,s=s)))

    def source(self,dimension,stage,fields):
        self.stats['source_calls']+=1
        if stage in ('majorana','fermion'):
            return self.program('source_{}_{}'.format(dimension,stage),fields)[0]%2
        if stage!='bosonic':raise ValueError(stage)
        if dimension==3:
            if (self.use_specializations and self.use_pure_cf_source
                    and not any(fields['n']) and not any(fields['a'])
                    and closed_background(5,tuple(fields['w']),tuple(fields['s']))):
                # Literal lift3_source/high6 composition, including the
                # publication's off-shell CF coordinate and signed background.
                self.stats['specialized_pure_cf_source_calls']+=1
                value=self.program('source3_pure_cf_bosonic',fields)[0]
                return Fraction(value%16,16)
            if self.use_specializations and self.use_n0_source and not any(fields['n']):
                lower=self.source3_n0_lower(tuple(fields['a']),tuple(fields['w']),tuple(fields['s']))
                if lower is not None:
                    legal=True
                    for face,expected in zip(faces(5,4),lower):
                        mask=sum(1<<j for j in face)
                        if sum(fields['c'][mask^(1<<j)] for j in face)%2!=expected:
                            legal=False;break
                    if legal:
                        self.stats['specialized_n0_source_calls']+=1
                        value=self.program('source3_majorana_n0_bosonic',fields)[0]
                        return Fraction(value%16,16)
            return Fraction(self.suspended('source',fields),16)
        if dimension==4:
            shifted=self.shift(4,fields)
            high,cubic=self.high6(shifted)
            return Fraction((3*high+4*cubic)%48,48)
        raise ValueError('Only spatial dimensions 3 and 4 are supported')

    def majorana_gauge_n0(self,dimension,stage,fields):
        """Literal non-vacuum d3/d4 prism with n=lambda=gamma=0.

        Both stages return corrections. The fermion correction is independent
        of base c; callers may supply zero c faces for that stage only.
        """
        if dimension not in (3,4) or stage not in ('fermion','bosonic'):
            raise ValueError('Non-vacuum Majorana gauge supports d3/d4 fermion/bosonic')
        if set(fields)!=set(('a','c','beta','w','s')):
            raise ValueError('Non-vacuum Majorana gauge requires a,c,beta,w,s')
        value=self.program('gauge_mc{}_n0_'.format(dimension)+stage,fields)[0]
        modulus=16 if dimension==3 else 48
        return value%2 if stage=='fermion' else Fraction(value%modulus,modulus)

    def fermion_gauge_n0(self,dimension,stage,fields):
        """Literal d3/d4 pure-CF gauge carry with n=a=lambda=beta=0."""
        if dimension not in (3,4) or stage!='bosonic':
            raise ValueError('Non-vacuum fermion gauge supports d3/d4 bosonic only')
        if set(fields)!=set(('c','gamma','w','s')):
            raise ValueError('Non-vacuum fermion gauge requires c,gamma,w,s')
        value=self.program('gauge_cf{}_n0_bosonic'.format(dimension),fields)[0]
        modulus=16 if dimension==3 else 48
        return Fraction(value%modulus,modulus)

    def vacuum_majorana_gauge(self,dimension,stage,fields):
        """Literal current-coordinate vacuum cylinder, lambda=gamma=0.

        This is a compiled substitution into the full source, not a lower-
        dimensional source formula. beta may be nonclosed. The caller must
        establish that every initial decoration is exactly zero.
        """
        if dimension!=4 or stage not in ('fermion','bosonic'):
            raise ValueError('Vacuum Majorana gauge kernel supports d4 fermion/bosonic stages')
        if set(fields)!=set(('beta','w','s')):
            raise ValueError('Vacuum Majorana gauge kernel requires exactly beta,w,s')
        value=self.program('vacuum_mc4_'+stage,fields)[0]
        return value%2 if stage=='fermion' else Fraction(value%48,48)

    def vacuum_cf4(self,background,gamma):
        """Literal publication d4 vacuum CF gauge carry; lower input is zero."""
        if set(background)!=set(('w','s')):
            raise ValueError('Vacuum fermion background requires exactly w,s')
        value=self.program('vacuum_cf4_bosonic',dict(background,gamma=gamma))[0]
        return Fraction(value%48,48)

    def vacuum_fermion_gauge(self,dimension,stage,fields):
        if dimension!=4 or stage!='bosonic':
            raise ValueError('Vacuum fermion gauge kernel supports only d4 bosonic stage')
        if set(fields)!=set(('gamma','w','s')):
            raise ValueError('Vacuum fermion gauge kernel requires exactly gamma,w,s')
        return self.vacuum_cf4(dict(w=fields['w'],s=fields['s']),fields['gamma'])

    def product(self,dimension,stage,left,right,background):
        self.stats['product_calls']+=1
        fields=dict(background,**left)
        fields.update(m=right['n'],b=right['a'],cp=right['c'])
        if stage in ('majorana','fermion'):
            return self.program('product_{}_{}'.format(dimension,stage),fields)[0]%2
        if stage!='bosonic':raise ValueError(stage)
        if dimension==3:
            return Fraction(self.suspended('product',fields),16)
        if dimension!=4:raise ValueError('Only spatial dimensions 3 and 4 are supported')
        if self.use_specializations and not any(left['n']) and not any(right['n']):
            self.stats['specialized_product_calls']+=1
            return Fraction(self.program('majorana4_product_composed',fields)[0]%48,48)
        l=self.shift(4,dict(background,**left));r=self.shift(4,dict(background,**right))
        fields.update(a=l['a'],b=r['a'])
        value=self.program('nonbinary4',fields)[0]
        state=encode(5,fields['n'],fields['a'],fields['m'],fields['b'],fields['w'],fields['s'])
        value+=24*self.binary4(state)
        return Fraction(value%48,48)
