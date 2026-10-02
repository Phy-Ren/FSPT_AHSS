"""Exact cubic source/product pair for Z_s-valued integer two-cocycles.
This is the three-primary component, not the full terminal FSPT product.
The extension background omega_2 is arbitrary and does not enter this component.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,ds

def mul(a,b,s,ta,tb,i=0):
    return cup(a,b,i,s=s,twists=(ta,tb))

def source3(n,s):
    """Three times the source, with coefficient twist s."""
    return mul(mul(n,n,s,1,1),n,s,0,1)

def product3(n,m,s):
    """Three times the product phase; no restriction on either parity."""
    q=mul(n,m,s,1,1,1);t=m-n
    return mul(t,q,s,1,0)-mul(q,t,s,0,1)

def commutator3(n,m,s):
    q=mul(n,m,s,1,1,2);t=m-n
    return mul(t,q,s,1,0)-mul(q,t,s,0,1)

def associator3(n,m,k,s):
    return mul(mul(n,m,s,1,1,1),k,s,0,1,1)
