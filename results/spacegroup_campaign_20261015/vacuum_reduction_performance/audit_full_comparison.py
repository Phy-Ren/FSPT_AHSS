#!/usr/bin/env python3
"""Compare every saved field and independently recheck source, SNF and filling."""
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent
BASELINE=Path('/home/xingyu/AllFSPT_reviews/point3_optimized_g_20261015')
sys.path.insert(0,str(ROOT/'candidate'))
from scripts.collect_expansion import load_campaign

def read(path):return json.loads(path.read_bytes())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    records,checks,provenance=load_campaign(ROOT/'sg221','ci')
    cid='spacegroup_221_spin_half';assert set(records)=={cid}
    bpath=BASELINE/'sg221_spin_half'/cid/'result.json';cpath=ROOT/'sg221'/cid/'result.json'
    b=read(bpath);c=read(cpath);assert b['input']==c['input']
    bk=read(BASELINE/'sg221_spin_half/source.json');ck=read(ROOT/'sg221/source.json')
    changed=[name for name in sorted(set(bk['files'])|set(ck['files'])) if bk['files'].get(name)!=ck['files'].get(name)]
    assert changed==['gap/classification.g']
    for name,expected in ck['files'].items():assert sha(ROOT/'candidate'/name)==expected
    bc,cc=b['classification'],c['classification'];fields=sorted(set(bc)|set(cc))
    different=[k for k in fields if bc.get(k)!=cc.get(k)]
    expected=['formulaCacheStats','formulaWorkerCalls','resolutionBuildTimings']
    assert different==expected
    same=[k for k in fields if bc.get(k)==cc.get(k)]
    vm_name='insulator/_compiled/native.so'
    # The recorded formula manifest identifies the actual library filename.
    br=read(BASELINE/'sg221_spin_half/formula_runtime.json');cr=read(ROOT/'sg221/formula_runtime.json')
    assert br['librarySHA256']==cr['librarySHA256'] and br['libraryPresent'] and cr['libraryPresent']
    result={'schema':'u1-zero-reduction-full-comparison-v1','passed':True,'id':cid,
        'baselineResultSHA256':sha(bpath),'candidateResultSHA256':sha(cpath),
        'baselineSourceSHA256':bk['sha256'],'candidateSourceSHA256':ck['sha256'],
        'changedRunnerSourceFiles':changed,'sourceFileCount':len(ck['files']),
        'sameNativeVM_SHA256':br['librarySHA256'],'sameExactInput':True,
        'allFieldNames':fields,'allFieldCount':len(fields),'exactlyEqualFieldNames':same,
        'mathematicalFieldCount':len(same),'differentFieldNames':different,
        'exactDifferences':{k:{'baseline':bc[k],'candidate':cc[k]} for k in different},
        'baselineElapsedSeconds':b['run']['elapsedSeconds'],'candidateElapsedSeconds':c['run']['elapsedSeconds'],
        'observedWallTimeRatio':b['run']['elapsedSeconds']/c['run']['elapsedSeconds'],
        'independentAcceptanceChecks':checks,'scriptSHA256':sha(Path(__file__))}
    (ROOT/'full_comparison.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['passed','allFieldCount','mathematicalFieldCount','differentFieldNames','observedWallTimeRatio']},indent=2))

if __name__=='__main__':main()
