#!/usr/bin/env python3
"""Literal spinless fermionic orbit-state signs and center-relation SNF."""
from itertools import permutations, product
from pathlib import Path
import json
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

G=[(p,s) for p in permutations(range(3)) for s in product((-1,1),repeat=3)]
def act(g,v):p,s=g;return tuple(s[i]*v[p[i]] for i in range(3))
reflections={"M1_coordinate":((0,1,2),(-1,1,1)),"M2_diagonal":((1,0,2),(1,1,1))}
def cycles_of(perm):
 seen=set();out=[]
 for i in range(len(perm)):
  if i in seen:continue
  cycle=[];j=i
  while j not in seen:seen.add(j);cycle.append(j);j=perm[j]
  out.append(cycle)
 return out
rows=[]
for name,point in [('tau1_vertices',(1,1,1)),('tau2_faces',(0,0,1)),('tau3_edges',(0,1,1)),('generic_coordinate_plane',(0,1,2)),('generic_diagonal_plane',(1,1,2)),('generic',(1,2,3))]:
 orbit=sorted({act(g,point) for g in G});index={v:i for i,v in enumerate(orbit)}
 chars={}
 for k,g in reflections.items():
  perm=[index[act(g,v)] for v in orbit];cycles=cycles_of(perm)
  chars[k]={'cycles':cycles,'cycle_lengths':list(map(len,cycles)), 'fermionic_sign':(-1)**(len(orbit)-len(cycles))}
 rows.append({'name':name,'point':point,'orbit':orbit,'charge':len(orbit),'characters':chars})
printed=[[8,0,0],[6,1,0],[12,0,0]]
actual=[[r['charge']]+[int(r['characters'][k]['fermionic_sign']==-1) for k in reflections] for r in rows]
def snf(rs):
 d=smith_normal_form(sp.Matrix([[0,2,0],[0,0,2]]+rs),domain=sp.ZZ)
 return [abs(int(z)) for z in d.diagonal()]
r={'convention':'Coordinates=(integer charge, M1 reflection bit, M2 reflection bit). One spinless scalar fermion at each orbit site, all occupied; many-body symmetry character is permutation determinant.', 'orbit_checks':rows, 'printed_relations':printed,'printed_snf':snf(printed),'explicit_orbit_relations':actual,'corrected_first_three_snf':snf(actual[:3]),'all_six_snf':snf(actual),'conclusion':'The printed tau3 sign is inconsistent with the literal 12-edge filled-orbit state. Correcting it gives Z4, so the printed relation error alone does not establish an extra physical Z2.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='orbit_checks'},indent=2))
