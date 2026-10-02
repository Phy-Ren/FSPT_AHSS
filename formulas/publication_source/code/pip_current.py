"""The single current third-stage p+ip multiplication.

The frozen algebra engine in pip_third supplies reference operations.  The
terminal-compatible degree-two correction is applied here before any public
output.  It vanishes at leading degree one by instability.
"""
from pip_third import *
import pip_third as _reference

def pure_product_compact(a,h,b,k,W,s,short=True):
 ans=_reference.pure_product_compact(a,h,b,k,W,s,short=short)
 return ans+a*b if a.d==2 else ans

def product_compact(a,h,c,b,k,e,W,s,short=True):
 return upper_product(a,c,b,e,s)+pure_product_compact(a,h,b,k,W,s,short=short)
