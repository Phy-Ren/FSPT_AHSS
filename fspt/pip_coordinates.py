"""Exact coordinate and integer-gauge witnesses for omega=0, n=s.

The finite table is a universal local cochain, derived from analytic O5
identities. It contains no space-group classification or stacking answer.
"""
from functools import lru_cache, reduce
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
from .formulas import field,cup,evaluate,formula,pip_cf_coordinate

INTEGER_GAUGE_ANF=(5,7,13,15,21,23,25,26,27,30,69,71,74,75,77,78,137,139)

@lru_cache(None)
def upper_data():
    return json.loads((Path(__file__).parent/'data/pip_upper_coordinate.json').read_text())

def sign_power(s,f):
    return reduce(lambda a,i:a*s((f[i],f[i+1])),range(len(f)-1),1)

def phase_reference_shift(k,b,c,s,face):
    """T with O_ref(n,b,c+Lambda)-O_native(n,b,c)=d_s T.

    k=1 is valid for db=s^3. k=2 is the doubled-output specialization b=0.
    The latter deliberately has no claim for arbitrary closed b.
    """
    f=tuple(face)
    if k==2:
        if any(b(tuple(f[i] for i in ids)) for ids in combinations(range(5),3)):
            raise ValueError('k=2 bridge requires b=0')
        lam=lambda z:sign_power(s,z)
        cross=evaluate(cup(field('c',3),field('l',3),2),{'c':c,'l':lam},f)
        return (Fraction(-3*sign_power(s,f),16)+Fraction(cross,2))%1
    if k!=1:raise ValueError('Only n=s and doubled output n=2s,b=0 are implemented')
    key=sum(s((f[0],f[i]))<<(i-1) for i in range(1,5))
    key+=sum(b((f[0],f[i],f[j]))<<(4+r) for r,(i,j) in enumerate(combinations(range(1,5),2)))
    data=upper_data();D=Fraction(data['numerators'][key],data['modulus'])
    lam=lambda z:pip_cf_coordinate(1,b,s,z)
    q=lambda z:evaluate(formula('pip_parity',1),{'n':s,'b':b,'s':s,'w':lambda f:0},z)
    cross=cup(field('c',3),field('l',3),2)+cup(field('l',3),field('q',4),3)
    # D was solved in the earlier AW transport coordinate. The corrected
    # supplied coordinate differs on n=s by d_s(-s^4/4).
    return (D+Fraction(sign_power(s,f),4)+Fraction(evaluate(cross,{'c':c,'l':lam,'q':q},f),2))%1

def integer_gauge_phase(c,s,face):
    """Gauge (2s,0,c,v) to (0,0,c+s^3,v+g); assumes dc=0."""
    f=tuple(face)
    bits=[s((f[0],f[i])) for i in range(1,5)]
    bits += [c((f[0],f[i],f[j],f[k])) for i,j,k in combinations(range(1,5),3)]
    active=sum((v%2)<<i for i,v in enumerate(bits))
    binary=sum((active&m)==m for m in INTEGER_GAUGE_ANF)%2
    return (Fraction(13*sign_power(s,f),16)+Fraction(binary,2))%1
