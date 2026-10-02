"""Shared-extension transport on ordered Cartan grids, s1=0.
These are background-transport identities, not a complete terminal product.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,primitive

def pull(x,projection):
    out=C(x.deg,fun=lambda f:x(tuple(projection[i] for i in f)),mod=x.mod)
    out.closed=x.closed
    return out

def eta(w,alpha,beta):
    """Degree-one prism: d eta = alpha*w + beta*w."""
    alpha,beta=tuple(alpha),tuple(beta)
    if len(alpha)!=len(beta) or any(a>b for a,b in zip(alpha,beta)):
        raise ValueError('Require equally long pointwise-ordered vertex maps.')
    return C(1,fun=lambda f:w((alpha[f[0]],beta[f[0]],beta[f[1]]))
               +w((alpha[f[0]],alpha[f[1]],beta[f[1]])))

def chi(w,alpha,beta,gamma):
    """Degree-zero coherence between three ordered background maps."""
    return C(0,fun=lambda f:w((alpha[f[0]],beta[f[0]],gamma[f[0]])))

def lift_first(n,u,w,alpha,beta):
    """Pull first decoration into the second projection's fixed background."""
    nn=pull(n,alpha)
    uu=pull(u,alpha)+cup(eta(w,alpha,beta),nn.reduce(2))
    return nn,uu,pull(w,beta)

def characteristic(n,u,w):
    return (u.lift().d()-cup(n,n)-cup(w.lift(),n)).div(2)
