"""Small ordinary polynomial ring over Q (no Boolean relations)."""
from fractions import Fraction
class P:
    def __init__(self,t=0):
        if isinstance(t,P):self.t=t.t;return
        if not isinstance(t,dict):t={():Fraction(t)} if t else {}
        self.t={k:Fraction(v) for k,v in t.items() if v}
    @staticmethod
    def var(i):return P({(i,):1})
    def __add__(self,o):
        o=P(o);t=dict(self.t)
        for k,v in o.t.items():t[k]=t.get(k,0)+v
        return P(t)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.t.items()})
    def __sub__(self,o):return self+-P(o)
    def __rsub__(self,o):return P(o)+-self
    def __mul__(self,o):
        o=P(o);t={}
        for k,v in self.t.items():
            for l,w in o.t.items():
                m=tuple(sorted(k+l));t[m]=t.get(m,0)+v*w
        return P(t)
    __rmul__=__mul__
    def __truediv__(self,k):return P({i:v/k for i,v in self.t.items()})
    __floordiv__=__truediv__
    def __mod__(self,k):
        assert all(v.denominator==1 for v in self.t.values()),'Final coefficient has an unexpected denominator'
        return P({i:int(v)%k for i,v in self.t.items()})
    def __bool__(self):return bool(self.t)
    def __eq__(self,o):return not bool(self-P(o))
    def __repr__(self):return 'P('+str(len(self.t))+' terms)'
