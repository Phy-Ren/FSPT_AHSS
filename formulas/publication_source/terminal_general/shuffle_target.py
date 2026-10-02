from symbolic import *
import time,argparse
from itertools import combinations

def paths(p,q):
 for ones in combinations(range(p+q),p):
    on=set(ones);i=j=0;vs=[(0,0)]
    for k in range(p+q):
        if k in on:i+=1
        else:j+=1
        vs.append((i,j))
    yield tuple(vs)

def target(p,q):
    start=time.time();n,u,j,ln=free_state(p);m,v,j,lm=free_state(q,j)
    r=Bit();top=tuple(range(7));out=[]
    for i,g in enumerate(paths(p,q)):
        nn,uu,mm,vv=(pull(n,[x[0] for x in g]),pull(u,[x[0] for x in g]),pull(m,[x[1] for x in g]),pull(v,[x[1] for x in g]))
        val=as_bit(residual(nn,uu,mm,vv)(top));r+=val
        out.append(len(val.t));print(p,q,i,'support',len(val.t),'sum',len(r.t),'seconds',round(time.time()-start,3),flush=True)
    data={'split':[p,q],'bits':j,'labels_left':ln,'labels_right':lm,'terms':sorted(r.t),'shuffle_sizes':out,'seconds':time.time()-start}
    path=Path(__file__).with_name(f'tensor_R_{p}_{q}.json');path.write_text(json.dumps(data));return data
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('p',type=int,nargs='?',choices=(2,3,4));args=ap.parse_args()
    for degree in ((args.p,) if args.p is not None else (2,3,4)):
        target(degree,6-degree)
