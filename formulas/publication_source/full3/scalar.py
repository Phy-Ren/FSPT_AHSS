from source import *
from cochains import random_cochain
import random,itertools

def make(dim,seed,mode='both'):
 random.seed(seed)
 s=random_cochain(0,dim).d() if mode!='omega' else C(1)
 w=random_cochain(1,dim).d() if mode!='s' else C(2)
 W=w+cup(s,s)
 def one():
  n=ds(C(0,values={(i,):random.randrange(-9,10) for i in range(dim+1)},mod=None),s)
  u=primitive(cup(W,n.reduce(2)))+random_cochain(1,dim).d()
  c=primitive(shifted_parity(n,u,w,s))+random_cochain(2,dim).d()
  return n,u,c
 return (*one(),*one(),w,s)
