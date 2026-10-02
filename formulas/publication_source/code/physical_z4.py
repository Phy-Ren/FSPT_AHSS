"""Exact normalized-bar calibration for G_f=Z4^f, G_b=Z2.

This independently enumerates the eight Majorana-sector states and their
64 products, not a lookup of the desired Z8 group. The bordism comparison
uses Hsieh, arXiv:1808.02881, Eqs. (2.66) and (2.72), specialized to m=2.
"""
from cochains import *
from manuscript import *
from stacking import *
from pathlib import Path
from itertools import product
from fractions import Fraction
import json,csv
ROOT=Path(__file__).resolve().parents[1]

def monomial(N,d,coeff=1):
    # Normalized bar generator x^d. Vertices of [t|...|t] have label i mod 2.
    return C(N,d,{f:coeff*int(all((f[j+1]-f[j])%2 for j in range(d))) for f in faces(N,d)})

def obstruction_bit(a,c,omega=1,sigma=0):
    N=6
    return int(Oop(monomial(N,3,a),monomial(N,4,c),monomial(N,2,omega),monomial(N,1,sigma)).top())%8

def parity_bit(a,omega=1,sigma=0):
    N=5
    return int(source(monomial(N,3,a),monomial(N,2,omega),monomial(N,1,sigma)).top())%2

cache={}
def mul(x,y):
    a,c,v=x;b,d,vp=y
    key=(a,c,b,d)
    if key not in cache:
        N=5; aa=monomial(N,3,a);bb=monomial(N,3,b);cc=monomial(N,4,c);dd=monomial(N,4,d)
        ww=monomial(N,2);ss=C(N,1,{})
        m=mk(aa,bb,ss)[(0,1,2,3,4)]
        e=int(correction(aa,cc,bb,dd,ww,ss).top())%8
        # Check the displayed reduced formula, including the separated factors.
        assert m == a*b
        assert int(majorana(aa,bb,ww,ss).top())%8 == 4*a*b
        assert int(complex_factor(aa,cc,bb,dd,ww,ss).top())%8 == 0
        assert int(mixed_factor(aa,cc,bb,dd,ww,ss).top())%8 == 0
        assert e == 4*a*b
        cache[key]=(m,e)
    m,e=cache[key]
    return (a^b,c^d^m,(v+vp+e)%8)

states=[]
for a,c,v in product(range(2),range(2),range(8)):
    if parity_bit(a)==0 and (2*v-obstruction_bit(a,c))%8==0:states.append((a,c,v))
identity=(0,0,0)
for x in states:
 for y in states:
    assert mul(x,y) in states
    assert mul(x,y)==mul(y,x)
    for z in states:assert mul(mul(x,y),z)==mul(x,mul(y,z))
orders={}
for x in states:
 y=identity
 for k in range(1,17):
    y=mul(y,x)
    if y==identity:orders[x]=k;break
root=next(x for x in states if x[0] and not x[1] and orders[x]==8)
powers=[];y=identity
for k in range(8):
 powers.append({'k':k,'n3_coefficient':y[0],'n4_coefficient':y[1],'nu5_numerator_over_8':y[2],
                'eta_charge_mod_16':(2*k)%16,'order':orders[y]})
 y=mul(y,root)
# Independent anomaly formula: m=2, q=1, and N charge-one Weyl fermions.
# alpha=( (2m^2+m+1)N-(m+3)N)/(48m)=N/16,
# beta=(mN+N)/(2m)=3N/4.
eta=[]
for row in powers:
 N=2*row['k']
 alpha=Fraction(N,16)%1;beta=Fraction(3*N,4)%1
 eta.append({'k':row['k'],'weyl_count':N,'alpha':str(alpha),'beta':str(beta)})
controls=[]
for w,s in product(range(2),repeat=2):
 controls.append({'omega_coefficient':w,'s_coefficient':s,'parity_on_n3=x^3':parity_bit(1,w,s),
                  'O6_on_n3=x^3_n4=0_numerator_over_8':obstruction_bit(1,0,w,s),
                  'warning':'O6 is a valid obstruction only after the parity equation has a solution.'})
report={'group':'Z4^f','bosonic_quotient':'Z2','p_ip':'zero','states':states,'products_checked':64,
 'associativity_triples_checked':512,'compact_cyclic_formula_checked':True,'separated_cyclic_factors_checked':True,'all_products_closed':True,'all_commutators_zero':True,
 'all_associators_zero':True,'majorana_sector_group':'Z8','chosen_root':root,'powers':powers,
 'independent_bordism_group':'Omega_5^(Spin x_Z2 Z4)=Z16','embedding':'k -> 2k mod 16',
 'normalization_caveat':'The abstract group and filtration fix this embedding only up to an odd choice of generator; no absolute eta orientation is inferred from group orders.',
 'eta_formula':eta,'controls':controls}
(ROOT/'results/physical_z4.json').write_text(json.dumps(report,indent=2))
with (ROOT/'results/physical_z4_powers.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(powers[0]));writer.writeheader();writer.writerows(powers)
print(json.dumps(report,indent=2))
