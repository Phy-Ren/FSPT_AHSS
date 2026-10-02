"""Auxiliary unitary Adem normalization, used only to select a cochain branch."""
from pathlib import Path
import sys,itertools as it,json,time
ROOT=Path(__file__).resolve().parents[1]
from pip_third import *
from coherence import signed_H_k,signed_G_k,pull
from descent import susp,tau

def x3(a):
 R=r(a)
 return (word('1213243142',a,a,a,a)+word('1213431412',a,a,a,a)
   +word('1232431421',a,a,a,a)+word('1234314212',a,a,a,a)+cup(R,R,2))
def pure3(a,h):return x3(a)+sq(h,3)
def R3(a,h,b,k):
 t=cup(a,b,2);u=cup(a,b,3);Q=q(a);QQ=q(b)
 return (sq(t,2)+cup(Q,QQ,4)+cup(Q+QQ,t,3)+cup(t,Q+QQ,3)
     +pure3(a+b,h+k+u)+pure3(a,h)+pure3(b,k))
def E3H(a,h,b,k):
 hs=[grid for grid,c in signed_H_k(5,2).items() if c%2 and all(len(set(v[j] for v in grid))>=4 for j in range(2))]
 z=0
 for grid in hs:z=z+R3(pull(a,grid,0),pull(h,grid,0),pull(b,grid,1),pull(k,grid,1)).top()
 return z%2

def B4(a,h):return a*h+cup(r(a),h,1)+h*h
