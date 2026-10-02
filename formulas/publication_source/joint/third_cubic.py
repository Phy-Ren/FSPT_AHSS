"""One-third-cubic source transport, with explicit signed word conventions.
Outputs are integer numerators over three. Not the full terminal fSPT twister.
"""
from cubic_repair import C,cup,ds
from cochains import interval_terms

def integer_word(word,*args,s=None):
    """Unrephased Berger--Fresse interval-cut word, transporting each sign input.
    Each argument has the sign local system of s, and must be an integer cochain.
    The cut sign is the one returned by the source's interval_terms.
    """
    degrees=tuple(x.deg for x in args);wd=tuple(map(int,word))
    if any(x.mod is not None for x in args):raise ValueError('integer inputs required')
    cuts=interval_terms(wd,degrees)
    def evaluate(f):
        total=0
        for inds,sign in cuts:
            value=sign
            for x,ids in zip(args,inds):
                ff=tuple(f[i] for i in ids)
                if s is not None and ff[0]!=f[0]:value*=(-1)**s((f[0],ff[0]))
                value*=x(ff)
            total+=value
        return total
    return C(sum(degrees)-len(wd)+len(args),fun=evaluate,mod=None)

def third_cubic3(n,m,s):
    L=cup(n,m,1,s=s,twists=(1,1));D=m-n
    return cup(D,L,s=s,twists=(1,0))-cup(L,D,s=s,twists=(0,1))

def third_commutator3(n,m,s):
    Q=cup(n,m,2,s=s,twists=(1,1));D=m-n
    return (cup(D,Q,s=s,twists=(1,0))-cup(Q,D,s=s,twists=(0,1))).scaled(-1)
