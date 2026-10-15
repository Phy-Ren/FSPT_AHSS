#!/usr/bin/env python3
"""Recheck immutable E6, exact E8 parents and all four preserved-D overlaps."""
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

def digest(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_bytes())
def main():
    manifest=read(BASE/'manifest.json')
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
    assert actual==set(manifest['filesSHA256'])
    for name,expected in manifest['filesSHA256'].items():assert digest((BASE/name).read_bytes())==expected,name
    report=read(BASE/'sgfull-20261015-e-smoke-finalization-v2.json')
    archive=BASE/Path(report['archive']).name
    assert digest(archive.read_bytes())==report['archiveSHA256'] and archive.stat().st_size==report['archiveBytes']
    assert report['state']=='complete' and report['acceptedCount']==6 and report['ciArtifactsUnchanged']
    assert report['helperSHA256']==digest((BASE/'finalize_e6_v2.py').read_bytes())
    previous=BASE/'sgfull-20261015-e-smoke-finalization.json'
    assert digest(previous.read_bytes())==report['previousFailureReportSHA256']
    assert read(previous)['state']=='failed' and 'formula_runtime.json' in read(previous)['error']
    for name,expected in report['verifiedSourceFiles'].items():
        assert digest(subprocess.check_output(['git','show','ce152c6:'+name],cwd=REPO))==expected,name
    for name,expected in report['postprocessorFilesSHA256'].items():
        assert digest(subprocess.check_output(['git','show','c07c6e5:'+name],cwd=REPO))==expected,name
    duplicate_audit=read(BASE/'finalized_validation.json')['duplicateComparisons']
    d_raw={}
    for d_archive in (BASE.parent/'preserved_d/archives').glob('*.tar.gz'):
        with tarfile.open(d_archive) as tar:
            for row in duplicate_audit:
                suffix='/'+row['id']+'/result.json'
                matches=[m for m in tar.getmembers() if '-preserved/' in m.name and m.name.endswith(suffix)]
                for member in matches:
                    assert row['id'] not in d_raw
                    d_raw[row['id']]=tar.extractfile(member).read()
    assert len(d_raw)==4
    with tempfile.TemporaryDirectory(prefix='u1-e6-verify-') as temporary:
        temp=Path(temporary)
        with tarfile.open(archive) as tar:
            members=tar.getmembers()
            assert len({m.name for m in members})==len(members)
            assert all(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and (m.isfile() or m.isdir()) for m in members)
            tar.extractall(temp)
        ci_root=temp/'sgfull-20261015-e-smoke';e8_root=temp/'sgfull-20261015-e-smoke-e8'
        ci,ci_checks,cp=load_campaign(ci_root,'ci',allow_recovered=False)
        e8,e8_checks,ep=load_campaign(e8_root,'e8',allow_recovered=False)
        assert set(ci)==set(e8)==set(report['selectedIDs']) and len(ci)==6
        assert cp['source']['sha256']==report['sourceSHA256']
        for cid in ci:
            assert (ci_root/cid/'result.json').read_bytes()==(e8_root/cid/'ci_result.json').read_bytes()
        collection_root=temp/'sgfull-20261015-e-smoke-accepted'
        collection=read(collection_root/'collection.json')
        assert collection['accepted'] and sum(x['count'] for x in collection['collections'])==6
        for item in collection['collections']:
            for name,expected in item['filesSHA256'].items():
                assert digest((collection_root/item['path']/name).read_bytes())==expected
        for row in duplicate_audit:
            cid=row['id'];assert digest(d_raw[cid])==row['DResultSHA256']
            assert digest((ci_root/cid/'result.json').read_bytes())==row['EResultSHA256']
            d=json.loads(d_raw[cid]);e=ci[cid]['record'];assert d['input']==e['input']
            dc,ec=d['classification'],e['classification']
            keys=sorted(dc.keys()|ec.keys());diff=[k for k in keys if dc.get(k)!=ec.get(k)]
            assert diff==row['differingFieldNames']==['resolutionBuildTimings']
            assert len(keys)==37 and dc['presentation']==ec['presentation']
            assert {k:{'D':dc.get(k),'E':ec.get(k)} for k in diff}==row['exactDifferences']
    print(json.dumps({'verified':True,'ordinaryCICases':6,'E8Cases':6,'sourceFilesAgainstGit':45,
        'exactCIE8Parents':6,'duplicateDComparisons':4,'scientificDifferences':0,
        'onlyDifferingField':'resolutionBuildTimings','recoveryRequired':False},indent=2,sort_keys=True))

if __name__=='__main__':main()
