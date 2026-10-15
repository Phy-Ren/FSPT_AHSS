#!/usr/bin/env python3
"""Finite offline native comparisons; diagnostic parents are never accepted."""
import argparse,hashlib,importlib.util,json,subprocess
from collections import Counter
from pathlib import Path
BASE=Path(__file__).resolve().parent
EXECUTION={'formulaCacheStats','formulaWorkerCalls','pairedGeometryReuse','resolutionBuildTimings'}
COMMITS={'G':'c07c6e5d4a69d79c9c2aeb0739ae1e189029f824','H':'ea44c1f55314ddd66587cf452bbaae9331f3a1db'}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,default=Path('/home/xingyu/FSPT_AHSS_insulator'));p.add_argument('--write',action='store_true');a=p.parse_args()
 spec=importlib.util.spec_from_file_location('pinned_integer_checks',BASE/'integer_checks.py'); checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
 original=a.repository/'results/spacegroup_campaign_20261015/overlap_g_h_210/verify.py'
 assert (BASE/'integer_checks.py').read_bytes()==original.read_bytes()
 d=read(BASE/'download.json'); assert not d['failed'] and len(d['pairs'])==12
 for name,meta in d['files'].items():
  raw=(BASE/'raw'/name).read_bytes();assert len(raw)==meta['size'] and sha(raw)==meta['sha256']
 sources={}; rows=[]
 for pair in d['pairs']:
  case=pair['id'];natives={};case_checks={};runtime={}
  assert case!='spacegroup_210_spinless'
  for label in ('G','H'):
   tag=pair[label];root=BASE/'raw'/tag;folder=root/case
   source=read(root/'source.json')
   if tag not in sources:
    assert sha(canon(source['files']))==source['sha256']
    for name,value in source['files'].items():assert sha(subprocess.check_output(['git','show',COMMITS[label]+':'+name],cwd=a.repository))==value
    sources[tag]={'commit':COMMITS[label],'sha256':source['sha256'],'fileCount':len(source['files'])}
   data=read(folder/'input.json');run=read(folder/'run.json');native=read(folder/'native.json')
   assert run['id']==data['id']==case and data['dimension']==3 and data['family']=='spacegroup'
   assert run['sourceSHA256']==source['sha256'] and run['inputSHA256']==sha((folder/'input.json').read_bytes())
   assert (folder/'input.json').read_bytes()==subprocess.check_output(['git','show',COMMITS[label]+':insulator_catalog/generated/'+case+'.json'],cwd=a.repository)
   assert case in read(root/'selection.json')
   ordinary=label=='H' or pair['gOrdinaryComplete']
   if ordinary:
    assert run['status']=='complete' and run['exitCode']==0
    assert read(folder/'result.json')=={'input':data,'run':run,'classification':native}
   else:
    assert not (folder/'result.json').exists() and pair['scope']=='native-only-diagnostic-not-accepted'
    assert run['status']!='complete'
    assert ('U1_PAIR_CASE_DONE '+case).encode() in (folder/'stdout.log').read_bytes().splitlines()
   case_checks[label]=checks.scientific(native)
   natives[label]=native;runtime[label]=read(root/'formula_runtime.json')
  assert runtime['G']['librarySHA256']==runtime['H']['librarySHA256']
  assert (BASE/'raw'/pair['G']/case/'input.json').read_bytes()==(BASE/'raw'/pair['H']/case/'input.json').read_bytes()
  g,h=natives['G'],natives['H'];assert set(g)==set(h)
  diff={k:{'G':g[k],'H':h[k]} for k in g if g[k]!=h[k]}
  scientific={k:v for k,v in g.items() if k not in EXECUTION}
  science_diff=sorted(set(diff)-EXECUTION)
  assert not science_diff,case+':'+repr(science_diff)
  assert case_checks['G']==case_checks['H']
  rows.append({'id':case,'scope':pair['scope'],'gOrdinaryComplete':pair['gOrdinaryComplete'],
   'scientificFieldCount':len(scientific),'scientificFields':sorted(scientific),'scientificFieldsLiterallyEqual':True,
   'canonicalScientificSHA256':sha(canon(scientific)), 'entireNativeObjectsEqual':g==h,
   'executionDifferences':diff,'scientificDifferences':science_diff,
   'independentChecks':case_checks['G'],'group':{k:g[k] for k in ('torsion','freeRank')},
   'acceptancePerformed':False,'coordinateChangeRequired':False})
 report={'status':'PASS','capturedUTC':d['capturedUTC'],'counts':dict(Counter(r['scope'] for r in rows)),
  'cases':rows,'sources':sources,'integerCheckSourceSHA256':sha((BASE/'integer_checks.py').read_bytes()),
  'comparisonScriptSHA256':sha(Path(__file__).read_bytes()),
  'cochainsRecomputed':False,'acceptancePerformed':False,'controlledSpeedupClaimed':False,
  'scope':'Five complete-parent overlaps and seven G-native-only diagnostics; no completion/acceptance is inferred for missing parents.'}
 if a.write:(BASE/'comparison.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 else:assert read(BASE/'comparison.json')==report
 print(json.dumps({'status':'PASS','counts':report['counts'],'cases':[{'id':r['id'],'fields':r['scientificFieldCount'],'scope':r['scope']} for r in rows]},indent=2))
if __name__=='__main__':main()
