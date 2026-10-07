"""Replay the exact integer-carry normalization against an earlier coefficient tree.

Usage: python verify_carry_normalization.py --original /path/to/old/tree
The old tree contains gamma_psi/INDEX.json and psi/INDEX.json. It can be
obtained from the preceding repository revision. No private modules are used.

Only B4[n,0]=B4psi[n] is used as a new cochain identity. It follows from
the published open-domain definition B4[n,x]=beta_open(x)+B4psi[n]. The
identity is integral, so all its digits and ordinary differentials agree.
Every original factor, argument, protected numerator, and outer term is
replayed. Hash checks are additional evidence, not the mathematical test.
"""
from pathlib import Path
import argparse,hashlib,json
from normalize_integer_carries import read,Restriction
HERE=Path(__file__).resolve().parent

def verify(original,current,sector):
 old=original/sector;new=current/sector;oi=read(old/'INDEX.json');ni=read(new/'INDEX.json');R=Restriction();hashes={}
 def checked(directory,entry):
  path=directory/entry['file'];raw=path.read_bytes()
  assert hashlib.sha256(raw).hexdigest()==entry['sha256']
  hashes[str(path.relative_to(directory))]=entry['sha256']
  return read(path)
 for entry in oi['files']:
  if entry['kind']=='factors':
   for row in checked(old,entry):
    assert row['id']==len(R.alias)
    if row['kind']=='physical_face':assert "'"not in row['cochain']
    R.factor(row)
 assert set(R.reasons)<= {'B_zero_Majorana_equals_Bpsi','identical_factor'},R.reasons
 terms=set();input_count=0;zero_terms=0
 for entry in oi['files']:
  if entry['kind']!='terms':continue
  for row in checked(old,entry):
   m=R.monomial(row);input_count+=1
   if m is None:zero_terms+=1;continue
   if m in terms:terms.remove(m)
   else:terms.add(m)
 assert input_count==oi['term_count']
 used={i for term in terms for i in term};pending=list(used)
 while pending:
  i=pending.pop();row=R.factors[i];rows=row.get('numerator',[])
  if row['kind'].startswith('standard_'):rows=[term for a in row['arguments']for term in a['terms']]
  for _,ids in rows:
   for j in ids:
    if j not in used:used.add(j);pending.append(j)
 remap={old:new for new,old in enumerate(sorted(used))};expected=[]
 def polynomial(rows):return [[c,[remap[j]for j in ids]]for c,ids in rows]
 for old_id in sorted(used):
  row=R.factors[old_id];out={**row,'id':remap[old_id]}
  if 'numerator'in row:out['numerator']=polynomial(row['numerator'])
  if 'arguments'in row:out['arguments']=[{**a,'terms':polynomial(a['terms'])}for a in row['arguments']]
  expected.append(out)
 actual=[]
 for entry in ni['files']:
  if entry['kind']=='factors':actual.extend(checked(new,entry))
 assert actual==expected
 mapped={tuple(remap[j]for j in term)for term in terms};row_count=0
 for entry in ni['files']:
  if entry['kind']!='terms':continue
  for row in checked(new,entry):
   assert row==sorted(set(row));key=tuple(row);assert key in mapped; mapped.remove(key);row_count+=1
 assert not mapped and row_count==ni['term_count']==len(terms)
 factor_map={'original_to_unpruned':[list(v)if v is not None else None for v in R.alias], 'pruned_to_final':[[old,new]for old,new in sorted(remap.items())]}
 mapbytes=(json.dumps(factor_map,separators=(',',':'))+'\n').encode()
 return {'status':'PASS_EXACT_COMPLETE_EXPRESSION_NORMALIZATION','sector':sector,'source_terms':input_count,'normalized_terms':row_count,'removed_outer_summands':input_count-row_count,'zero_outer_summands':zero_terms,'source_factors':len(R.alias),'normalized_factors':len(expected),'exact_factor_definition_equality':True,'exact_complete_outer_polynomial_equality':True,'allowed_identity':'B4[n,0]=B4psi[n] over the integers, including ordinary differentials and all binary digits','rules':dict(R.reasons),'normalization_map_sha256':hashlib.sha256(mapbytes).hexdigest(),'representative_change':False},mapbytes

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--original',type=Path,required=True);parser.add_argument('--current',type=Path,default=HERE);parser.add_argument('--sector',choices=['gamma_psi','psi']);parser.add_argument('--write',action='store_true');args=parser.parse_args()
 for sector in ([args.sector]if args.sector else ['gamma_psi','psi']):
  result,mapping=verify(args.original,args.current,sector)
  if args.write:
   import gzip
   (args.current/sector/'NORMALIZATION_MAP.json.gz').write_bytes(gzip.compress(mapping,mtime=0))
   (args.current/sector/'NORMALIZATION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
  print(json.dumps(result,indent=2),flush=True)
