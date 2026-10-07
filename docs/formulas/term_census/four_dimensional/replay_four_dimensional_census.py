"""Replay the exact finite-index count using only the adjacent JSON data.

Run: python replay_four_dimensional_census.py
No external package, network call, private source, or project checkout is needed.
Per-kernel counts are the explicit weighted-expression-DAG coefficients in
the JSON; the path multiplicities below are recomputed from the displayed grids.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from math import comb
import json
HERE=Path(__file__).resolve().parent;DATA=json.loads((HERE/'FOUR_DIMENSIONAL_COUNT_DATA.json').read_text())
def grids():
 for k in range(1,5):
  for sigma in product(range(3),repeat=5-k):
   if all(x==2 for x in sigma):continue
   vertices=[(i,i,i)for i in range(k+1)];v=[k,k+sigma.count(0),k+sigma.count(0)+sigma.count(1)];vertices.append(tuple(v))
   for x in sigma:v[x]+=1;vertices.append(tuple(v))
   yield tuple(p[0]for p in vertices[1:])
counts=Counter(grids());assert sum(counts.values())==116
states=Counter({tuple(range(6)):1});map_paths=[]
for J in range(6):
 map_paths.append(sum(states.values()));nextstates=Counter()
 for p,multiplicity in states.items():
  if p[0]==p[1]:continue
  for q,weight in counts.items():nextstates[tuple(p[i]for i in q)]+=multiplicity*weight
 states=nextstates
assert map_paths==[1,116,4176,41760,83520,0]
FIELDS=('cochain_atoms','face_binomial_monomials')
def evaluate(kernel_table,pruned,gamma_cancel=False):
 out={r:{field:0 for field in FIELDS}for r in('1','3','2')}
 for J in range(6):
  base=map_paths[J]if pruned else 116**J
  for h in range(J+1):
   item=kernel_table[str(h)];weight=base*comb(J,h)
   for r in out:
    if gamma_cancel and r=='1'and J:continue
    for field in FIELDS:out[r][field]+=weight*(358*item['kernel'][r][field]+item['tensor'][r][field])
 return out
before=evaluate(DATA['baseline_kernel_by_epsilon_weight'],False)
after=evaluate(DATA['current_kernel_by_epsilon_weight'],True,True)
yc=DATA['source_residual_atoms']*DATA['source_grid_count'];yf=DATA['AW_physical_binomial_occurrences']
rows=[]
for record in DATA['baseline_visible_blocks']:
 law,sector=record['law'],record['sector'];oldc=record['cochain_atoms'];newc=oldc+DATA['current_visible_changes'].get(law+'.'+sector,0);oldf=newf=0
 if law=='O6'and sector=='psi':oldc+=yc;newc+=yc;oldf+=yf;newf+=yf
 if law=='E5'and sector in('gamma','gamma_psi','psi'):
  color={'gamma':'1','gamma_psi':'3','psi':'2'}[sector]
  oldc+=before[color]['cochain_atoms'];newc+=after[color]['cochain_atoms'];oldf+=before[color]['face_binomial_monomials'];newf+=after[color]['face_binomial_monomials']
 rows.append({'dimension':'4+1D','law':law,'sector':sector,'baseline_raw_cochain_atoms':oldc,'baseline_raw_face_binomial_monomials':oldf,'baseline_raw_total':oldc+oldf,'current_raw_cochain_atoms':newc,'current_raw_face_binomial_monomials':newf,'current_raw_total':newc+newf,'collected_nonzero_total':None})
result={'status':'PASS_EXACT_FINITE_COUNT_REPLAY','metric':DATA['metric'],'path_map_counts_by_length':map_paths,'path_occurrences_before_pruning':sum(232**J for J in range(6)),'path_occurrences_after_generic_pruning':sum(map_paths[J]*2**J for J in range(6)),'gamma_path_occurrences_after_sector_cancellation':1,'y6_raw_cochain_atoms':yc,'y6_raw_physical_binomial_monomials':yf,'y6_raw_total':yc+yf,'rows':rows,'scope':'Current counts include the1090-row source table, the lower E4 exact simplifications, generic path pruning, and gamma-only branch cancellation. Counts are before remaining scalar-face normalization and cancellation.'}
(HERE/'FOUR_DIMENSIONAL_CENSUS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
