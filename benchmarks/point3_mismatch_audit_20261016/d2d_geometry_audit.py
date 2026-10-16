#!/usr/bin/env python3
"""Exact identification of D2d catalogue matrices and the split determinant map."""
import json,hashlib,argparse
from pathlib import Path
from fractions import Fraction
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
args=parser.parse_args()
root=args.repo/'insulator_catalog/generated'
p=root/'point3_14_spinless.json';data=json.loads(p.read_text())
mul=data['multiplication']; mats=data['matrices'];r=2;s=5
assert mul[mul[r][r]][mul[r][r]]==0 and mul[s][s]==0
assert mul[mul[s][r]][s]==mul[mul[r][r]][r]
indices={}
power=0
for m in range(4):
 for l in range(2):indices[(l,m)]=power if l==0 else mul[s][power]
 power=mul[power][r]
assert len(set(indices.values()))==8
u=[0]*8;v=[0]*8
for (l,m),i in indices.items():u[i]=m%2;v[i]=l
checks=0
for i in range(8):
 for j in range(8):
  assert u[mul[i][j]]==(u[i]+u[j])%2
  assert v[mul[i][j]]==(v[i]+v[j])%2
  M,N=mats[i],mats[j]
  assert [[sum(M[a][k]*N[k][b] for k in range(3)) for b in range(3)] for a in range(3)]==mats[mul[i][j]]
  checks+=1
for i,M in enumerate(mats):
 assert M[0][2]==M[1][2]==M[2][0]==M[2][1]==0
 assert M[0][0]*M[1][1]-M[0][1]*M[1][0]==(-1)**v[i]
 assert M[2][2]==(-1)**((u[i]+v[i])%2)
 assert data['s'][i]==u[i]
 assert data['rho'][i]==u[i]
assert all(2*Fraction(data['omega'][i][j])==data['geometric_pin_minus'][i][j] for i in range(8) for j in range(8))
halfpath=root/'point3_14_spin_half.json';half=json.loads(halfpath.read_text())
assert half['matrices']==mats and half['s']==u and half['rho']==u
assert all(Fraction(z)==0 for row in half['omega'] for z in row)
t=mul[s][r]
assert mul[t][t]==0 and u[t]==1
out={'status':'PASS','r_catalogue_index':r,'s_catalogue_index':s,'split_C2_section_generator_index':t,'group_checks':checks,'u':u,'v':v,
 'spatial_decomposition':'V = W_xy + line_(u+v), det(W)=v',
 'source_ring':'F2[u,v,w]/(u^2+uv), w=w2(W)',
 'spinless_Thom':'3-V: w1=u,w2=w+v^2',
 'spin_half_Thom':'det(V)-1: w1=u,w2=0',
 'section':'u:D8->C2 with section1->s*r; the determinant Thom line is its pullback',
 'catalogue_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest(),halfpath.name:hashlib.sha256(halfpath.read_bytes()).hexdigest()}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
