#!/usr/bin/env python3
"""Replay all-field, source, exact parent, Smith and filling checks, without GAP."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

BASE=Path(__file__).resolve().parent
REPO=BASE.parents[2]
sys.path.insert(0,str(REPO))
from scripts.collect_expansion import load_campaign

def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_bytes())
def unpack(path,folder):
    with tarfile.open(path) as tar:
        members=tar.getmembers()
        assert len({m.name for m in members})==len(members)
        assert all(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and (m.isdir() or m.isfile()) for m in members)
        tar.extractall(folder)

def main():
    manifest=read(BASE/'manifest.json')
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
    assert actual==set(manifest['filesSHA256'])
    for name,expected in manifest['filesSHA256'].items():assert sha((BASE/name).read_bytes())==expected,name
    report=read(BASE/'full_comparison.json')
    with tempfile.TemporaryDirectory(prefix='u1-zero-reduction-') as temporary:
        temp=Path(temporary)
        for name in ('baseline','candidate','cli_canonical','cli_reference'):unpack(BASE/(name+'.tar.gz'),temp)
        sources={}
        raw={}
        for label in ('baseline','candidate'):
            records,checks,provenance=load_campaign(temp/label,'ci')
            assert set(records)=={'spacegroup_221_spin_half'}
            raw[label]=records['spacegroup_221_spin_half']['record']
            sources[label]=provenance['source']
            assert sources[label]['sha256']==report[label+'SourceSHA256']
            assert sha((temp/label/'spacegroup_221_spin_half/result.json').read_bytes())==report[label+'ResultSHA256']
        for name,expected in sources['baseline']['files'].items():
            assert sha(subprocess.check_output(['git','show','c07c6e5:'+name],cwd=REPO))==expected,name
        changed=[name for name in sorted(sources['baseline']['files']) if sources['baseline']['files'][name]!=sources['candidate']['files'][name]]
        assert changed==['gap/classification.g']
        assert sha((BASE/'candidate_classification.g').read_bytes())==sources['candidate']['files']['gap/classification.g']
        b,c=raw['baseline'],raw['candidate'];assert b['input']==c['input']
        bc,cc=b['classification'],c['classification'];keys=sorted(set(bc)|set(cc));different=[k for k in keys if bc.get(k)!=cc.get(k)]
        assert keys==report['allFieldNames'] and len(keys)==38
        assert different==report['differentFieldNames']==['formulaCacheStats','formulaWorkerCalls','resolutionBuildTimings']
        assert {k:{'baseline':bc[k],'candidate':cc[k]} for k in different}==report['exactDifferences']
        assert b['run']['elapsedSeconds']==234.922 and c['run']['elapsedSeconds']==127.065
        for label in ('baseline','candidate'):
            assert read(temp/label/'formula_runtime.json')['librarySHA256']==report['sameNativeVM_SHA256']
        for row in read(BASE/'cli_comparison.json')['rows']:
            cid=row['id'];a=read(temp/'cli_canonical'/cid/'result.json');b=read(temp/'cli_reference'/cid/'result.json')
            assert a['run']['vacuumReductionRequested']=='canonical' and b['run']['vacuumReductionRequested']=='reference'
            ac,bc=a['classification'],b['classification']
            assert [k for k in sorted(set(ac)|set(bc)) if ac.get(k)!=bc.get(k)]==row['differentFields']
            assert not(set(row['differentFields'])-{'chargePrimaryStats','formulaWorkerCalls','formulaCacheStats','resolutionBuildTimings'})
    finite=read(BASE/'zero_identity_checks.json')
    assert finite['passed'] and len(finite['rows'])==8
    assert all(row['nativeWitnessesIdentical'] for row in finite['rows'])
    print(json.dumps({'verified':True,'allFieldsCompared':38,'literallyEqualMathematicalFields':35,
        'sourceFilesCheckedAgainstFrozenG':57,'differentSourceFiles':['gap/classification.g'],
        'signedFiniteBarCases':8,'sameNativeVM':True,'CLIReferenceCases':2},indent=2,sort_keys=True))

if __name__=='__main__':main()
