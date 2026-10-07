"""Verify the explicit finite coefficient tables using only the standard library.

Run from any directory: python verify_coefficients.py
The script checks the complete factor definitions, nonlinear scopes, row
uniqueness, file hashes, and the stated summand counts for both contributions.
"""
from pathlib import Path
import hashlib,json,gzip
ROOT=Path(__file__).resolve().parent

def check(sector):
 directory=ROOT/sector;index=json.loads((directory/'INDEX.json').read_text())
 factors=[];seen=set();count=0;interiors=0;arguments=0
 def expression(rows,limit,modulus):
  nonlocal interiors
  for coefficient,ids in rows:
   assert 0<coefficient<modulus
   assert ids==sorted(set(ids)) and all(0<=i<limit for i in ids)
 for entry in index['files']:
  raw=(directory/entry['file']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==entry['sha256']
  payload=gzip.decompress(raw)if entry['file'].endswith('.gz')else raw
  rows=json.loads(payload);assert len(rows)==entry['rows'] and len(raw)==entry['bytes']
  if 'uncompressed_sha256'in entry:assert hashlib.sha256(payload).hexdigest()==entry['uncompressed_sha256']
  if entry['kind']=='factors':
   for factor in rows:
    identifier=factor['id'];assert identifier==len(factors)
    kind=factor['kind']
    if kind=='physical_face':
     assert factor['face']==sorted(set(factor['face']))
    elif kind.startswith('standard_'):
     assert factor['operation'] and factor['degree']>=1
     for arg in factor['arguments']:
      expression(arg['terms'],identifier,1<<arg['precision_bits']);arguments+=len(arg['terms'])
    else:
     assert kind in ('canonical_binary_lift','binary_floor_digit')
     expression(factor['numerator'],identifier,factor['modulus']);interiors+=len(factor['numerator'])
     assert factor['divisor']>0
    factors.append(factor)
  else:
   assert entry['kind']=='terms'
   for ids in rows:
    assert ids==sorted(set(ids)) and all(0<=i<len(factors)for i in ids)
    row=tuple(ids);assert row not in seen;seen.add(row);count+=1
 assert len(factors)==index['factor_count']
 assert count==index['term_count']
 assert interiors==index['nonlinear_interior_terms']
 assert arguments==index['lower_argument_terms']
 print(sector,{'terms':count,'factors':len(factors),'nonlinear_interior_terms':interiors,'standard_operation_argument_terms':arguments})
 return {'sector':sector,'terms':count,'factors':len(factors),'nonlinear_interior_terms':interiors,'standard_operation_argument_terms':arguments}

if __name__=='__main__':
 result=[check(sector)for sector in ('gamma_psi','psi')]
 print('PASS: complete explicit coefficient tables, hashes, and term counts')
