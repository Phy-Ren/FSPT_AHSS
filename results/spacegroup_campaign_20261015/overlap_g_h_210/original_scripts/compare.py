#!/usr/bin/env python3
"""Recheck copied SG210 overlap artifacts and compare every scientific field.

No classification, cochain completion or remote action is performed here.
Native certificate fields are checked for consistency/presence; their chain
identities are not independently recomputed by this offline comparison.
"""
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
REPO=Path('/home/xingyu/FSPT_AHSS_insulator')
sys.path.insert(0,str(REPO))
from scripts.recover_paired_campaign import scientific_checks
from insulator.e8_pointgroup import presentation_invariants
ROOT=Path(__file__).resolve().parent
CASE='spacegroup_210_spinless'
SOURCES={'G':('sgfull-20261015-g-n03','c07c6e5d4a69d79c9c2aeb0739ae1e189029f824'),
         'H':('sgfull-20261015-h-remaining-n02','ea44c1f55314ddd66587cf452bbaae9331f3a1db')}
EXECUTION_KEYS={'formulaCacheStats','formulaWorkerCalls','pairedGeometryReuse','resolutionBuildTimings'}

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(p): return json.loads(p.read_bytes())
def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def main():
 download=read(ROOT/'download.json')
 for name,meta in download['files'].items():
  raw=(ROOT/'raw'/name).read_bytes()
  assert len(raw)==meta['size'] and sha(raw)==meta['sha256'],name
 records={}; checks={}
 for label,(tag,commit) in SOURCES.items():
  base=ROOT/'raw'/tag; directory=base/CASE
  source=read(base/'source.json'); runtime=read(base/'formula_runtime.json')
  assert sha(canonical(source['files']))==source['sha256']
  for name,expected in source['files'].items():
   raw=subprocess.check_output(['git','show',commit+':'+name],cwd=REPO)
   assert sha(raw)==expected,(label,name)
  data=read(directory/'input.json'); run=read(directory/'run.json'); native=read(directory/'native.json'); result=read(directory/'result.json')
  assert result=={'input':data,'run':run,'classification':native}
  assert run['status']=='complete' and run['exitCode']==0
  assert run['sourceSHA256']==source['sha256'] and run['inputSHA256']==sha((directory/'input.json').read_bytes())
  assert (REPO/'insulator_catalog/generated'/ (CASE+'.json')).read_bytes()==(directory/'input.json').read_bytes()
  assert CASE in read(base/'selection.json')
  checks[label]=scientific_checks(native,data)
  checks[label].update(sourceCommit=commit,sourceSHA256=source['sha256'],allSourceFileHashesMatchCommit=True,
                       sourceFileCount=len(source['files']),formulaRuntime=runtime,
                       ordinaryComplete=True,exactInputBytesMatchCatalogue=True,nativeEqualsResultClassification=True)
  layers={}
  for name in ('sheet','charge','phase'):
   rows=native['filtrationPresentations'][name]
   count=len(rows[0]) if rows else len(native[name+'Orders'])
   actual=presentation_invariants(rows,count)
   expected={'torsion':native['final'+name.title()+'Orders'],'freeRank':native['final'+name.title()+'FreeRank']}
   assert {k:actual[k] for k in expected}==expected,(label,name)
   layers[name]=expected
  checks[label]['independentFiltrationSmithGroups']=layers
  checks[label]['generatorCount']=len(native['generators'])
  checks[label]['rootWitnessCount']=len(native['witnesses'])
  checks[label]['gaugeWitnessCount']=len(native['gaugeReductionWitnesses'])
  records[label]=result
 g,h=records['G'],records['H']
 assert g['input']==h['input']
 ng,nh=g['classification'],h['classification']
 assert set(ng)==set(nh)
 differences={k:{'G':ng[k],'H':nh[k]} for k in ng if ng[k]!=nh[k]}
 assert set(differences)==EXECUTION_KEYS,differences.keys()
 science={k:v for k,v in ng.items() if k not in EXECUTION_KEYS}
 assert science=={k:v for k,v in nh.items() if k not in EXECUTION_KEYS}
 run_differences={k:{'G':g['run'].get(k),'H':h['run'].get(k),
                    'GPresent':k in g['run'],'HPresent':k in h['run']}
                  for k in set(g['run'])|set(h['run']) if g['run'].get(k)!=h['run'].get(k)}
 report={'status':'PASS','case':CASE,'checkedUTC':datetime.now(timezone.utc).isoformat(),
         'inputByteEquality':True,'entireNativeObjectEquality':ng==nh,
         'scientificFieldsLiterallyEqual':True,'scientificFieldCount':len(science),
         'scientificFields':sorted(science),'canonicalScientificObjectSHA256':sha(canonical(science)),
         'executionMetadataDifferences':differences,'runMetadataDifferences':run_differences,
         'checks':checks,'group':{k:ng[k] for k in ('torsion','freeRank')},
         'elapsedTimingCaveat':'Different nodes, paired/standalone scheduling, memory caps and old-G NFS-derived per-case timings preclude a controlled speedup claim.',
         'scope':'Exact input and all scientific-field equality; independent presentation/filling/filtration checks; saved completed-state/chain/root/gauge certificates retained. No cochain recomputation or new physical-certification claim.',
         'validatorSourceSHA256':{name:sha((REPO/name).read_bytes()) for name in ('scripts/recover_paired_campaign.py','scripts/collect_expansion.py','insulator/e8_pointgroup.py','insulator/e8_h1.py')},
         'comparisonScriptSHA256':sha(Path(__file__).read_bytes())}
 if '--write' in sys.argv:
  (ROOT/'comparison.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 else:
  saved=read(ROOT/'comparison.json')
  saved.pop('checkedUTC'); report.pop('checkedUTC')
  assert saved==report, 'Retained comparison or validator/source identity changed'
 print(json.dumps({'status':'PASS','group':report['group'],'scientificFields':len(science),
                   'executionDifferenceKeys':sorted(differences),'checks':{k:{'completionChecks':v['nativeCompletionChecks'],'filling':v['independentPresentationFillingCheck'],'layers':v['independentFiltrationSmithGroups']} for k,v in checks.items()}},indent=2))
if __name__=='__main__': main()
