#!/usr/bin/env bash
# PREPARED ONLY. Root invokes after the unchanged-H SG226 singleton shadow is fully accepted and downloaded.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
repo=/home/xingyu/FSPT_AHSS_insulator
review=/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015
prepared="$review/final_singleton_publication_prepared"
manifest="$prepared/final460_manifest.json"
collection="$repo/results/spacegroup_full_20261015"
audit="$review/final460_singleton_assembly"
tables="$review/final460_singleton_table_candidate"
test ! -e "$collection"
test ! -e "$audit"
test ! -e "$tables"
test ! -e "$prepared/tail_acceptance.json"
python3 - "$prepared/tail_acceptance.json" <<'PREFLIGHT_PY'
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
repo=Path('/home/xingyu/FSPT_AHSS_insulator')
prepared=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/final_singleton_publication_prepared')
p=prepared.parent/'accelerated_gate/check_readiness.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='7195eabfd9f8da16f5b2a500000cb1ffb6959bb9269a222893a3dc6bd6fbc317'
spec=importlib.util.spec_from_file_location('existing_readonly_gate',p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
manifest=prepared/'final460_manifest.json';assert g.sha(manifest)=='3b2162c9c18e9996454e90d9519a1be113b58afc223281f2a0008b9991342b73'
package=repo/'results/spacegroup_campaign_20261015/preserved_h_230_spinless'
subprocess.run([sys.executable,str(package/'verify.py'),'--repository',str(repo)],check=True)
approval=g.read(package/'approval.json')
stage=Path('/home/xingyu/AllFSPT_reviews/spacegroup_230_spinless_singleton_20261015')
assert g.sha(stage/'manifest.json')==approval['stagedManifestSHA256']
assert g.sha(stage/'staged_accepted/collection.json')==approval['acceptedCollectionSHA256']
assert g.sha(stage/'ci_view/spacegroup_230_spinless/result.json')==approval['ciResultSHA256']
assert g.sha(stage/'e8_view/spacegroup_230_spinless/result.json')==approval['e8ResultSHA256']
rows=[]
for tag,cases,memory in [
 ('sgfull-20261015-h-tail-highmem-n02',['spacegroup_226_spin_half','spacegroup_230_spin_half'],'32g'),
 ('sgfull-20261015-h-226-spinless-32g-shadow-n08',['spacegroup_226_spinless'],'32g')]:
 item=g.parent_entry(tag,cases,'Ordinary accepted H tail parent')
 checked=g.validate_parent(item)
 if checked['state']!='validated':raise ValueError('Required ordinary parent is not accepted/downloaded: '+tag)
 ci=Path(item['ci']);assert g.read(ci/'selection.json')==cases
 for case in cases:
  run=g.read(ci/case/'run.json')
  assert run['status']=='complete' and type(run['exitCode']) is int and run['exitCode']==0
  assert not run.get('pairedSpins') and not any(k.startswith('batch') for k in run)
  assert run['command'][run['command'].index('-K')+1]==memory
  assert run['command'][-1]=='/home/user/xyren/AllFSPT_insulator/runs/'+tag+'/'+case+'/driver.g'
 rows.append(dict(tag=tag,validation=checked))
flat=[]
for row in g.read(manifest)['campaigns']:flat.extend(row.get('cases') or g.read(Path(row['ci'])/'selection.json'))
expected={'spacegroup_%03d_%s'%(n,s) for n in range(1,231) for s in ('spinless','spin_half')}
assert len(flat)==len(set(flat))==460 and set(flat)==expected
assert all('sgfull-20261015-h-tail-spinless-n08-finalized' not in row['ci'] for row in g.read(manifest)['campaigns'])
Path(sys.argv[1]).write_text(json.dumps(dict(acceptedTailCount=4,readOnlyValidation=True,parents=rows,approvedSingleton='spacegroup_230_spinless',approvedSingletonPackageSHA256=g.sha(package/'manifest.json'),originalSpinlessParentAccepted=False,existingValidatorSHA256=g.sha(p),manifestSHA256=g.sha(manifest)),indent=2,sort_keys=True)+'\n')
PREFLIGHT_PY
python3 "$review/assemble_full460.py" --manifest "$manifest" \
  --audit-dir "$audit" --output "$collection" --repository "$repo" --allow-recovered \
  > "$prepared/assembly.stdout.log" 2> "$prepared/assembly.stderr.log"
python3 "$repo/scripts/build_current_tables.py" --output "$tables" \
  --expansion "$repo/results/expansion_20261015" \
  --expansion "$repo/results/point3_current_20261015" \
  --expansion "$collection" > "$prepared/candidate.stdout.log" 2> "$prepared/candidate.stderr.log"
python3 "$repo/scripts/build_current_tables.py" --check --output "$tables" \
  --expansion "$repo/results/expansion_20261015" \
  --expansion "$repo/results/point3_current_20261015" \
  --expansion "$collection" > "$prepared/candidate_check.stdout.log" 2> "$prepared/candidate_check.stderr.log"
python3 - "$repo" "$audit" "$tables" "$prepared/candidate_postconditions.json" <<'PY'
import csv,hashlib,json,sys
from pathlib import Path
repo,audit,tables,out=map(Path,sys.argv[1:]);read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=read(audit/'assembly.json');assert a['accepted'] and a['selectedCount']==a['expectedCount']==460
expected={'spacegroup_%03d_%s'%(n,s) for n in range(1,231) for s in ('spinless','spin_half')}
assert set(a['selectedCases'])==expected
seen=set();rows=[]
for spin in ('spinless','spin_half'):
 p=tables/'3p1d'/spin/'space_groups.json';t=read(p);ids=[r['id'] for r in t['rows']]
 assert len(ids)==len(set(ids))==230 and not seen&set(ids);seen.update(ids)
 assert all(r['physical_spin']==spin for r in t['rows'])
 assert [c['key'] for c in t['columns']][:5]==['e','n','charge','phase','stacking']
 assert 'fourth column only: neutral' in t['sources']['SXH_neutral']['location']
 assert all('not full electronic classification' in r['cells']['SXH_neutral']['scope'] for r in t['rows'])
 assert all(r['cells']['physical_reference']['availability']=='unverified' for r in t['rows'])
 with p.with_suffix('.csv').open() as f:assert len(list(csv.DictReader(f)))==230
 rows.append(dict(spin=spin,count=230,tableSHA256=sha(p),E8First=True,SXHNeutralOnly=True))
assert seen==expected
summary=read(tables/'manifest.json')
assert (summary['table_count'],summary['sector_entry_count'],summary['background_count'])==(13,638,584)
index=read(tables/'index.json')
assert len({r['id'] for r in index if r['family']!='internal_cyclic'})==578
assert len({r['id'] for r in index if r['family']=='internal_cyclic'})==6
physical_flags=0
for name in ['results/spacegroup_full_20261015/3p1d/space_groups/results.json','results/point3_current_20261015/3p1d/point_groups/results.json','results/expansion_20261015/4p1d/internal_cyclic/results.json']:
 for record in read(repo/name):
  c=record['classification']
  if 'physicalClassificationCertified' in c:
   assert c['physicalClassificationCertified'] is False;physical_flags+=1
assert physical_flags>=460
assert read(tables/'collections.json')['accepted_expansion_directories']==['results/expansion_20261015','results/point3_current_20261015','results/spacegroup_full_20261015']
out.write_text(json.dumps(dict(acceptedCount=460,tableCount=13,sectorEntries=638,distinctBackgrounds=584,crystallineBackgrounds=578,internalBackgrounds=6,physicalCertificationFalseRecords=physical_flags,tables=rows,assemblySHA256=sha(audit/'assembly.json'),tableManifestSHA256=sha(tables/'manifest.json'),publicationPerformed=False),indent=2,sort_keys=True)+'\n')
PY
# STOP HERE. Root reviews the accepted collection, provenance and candidate tables.
