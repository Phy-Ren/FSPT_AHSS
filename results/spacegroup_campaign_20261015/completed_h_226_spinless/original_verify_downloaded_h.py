#!/usr/bin/env python3
"""Offline additional H/source/runtime/input pins after the existing frozen replay."""
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent
TAG='sgfull-20261015-h-226-spinless-32g-shadow-n08';CASE='spacegroup_226_spinless'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())

def main():
    p=argparse.ArgumentParser();p.add_argument('--download',type=Path,default=Path('/home/xingyu/insulator-campaign-download')/(TAG+'-finalized'));a=p.parse_args()
    expected=read(HERE/'expected.json');proof=read(a.download/'download_verification.json');final=read(a.download/'finalization.json')
    assert final['state']=='complete' and final['selectedCount']==final['acceptedCount']==1 and final['tag']==TAG
    assert proof['frozenCollectorExactReplay'] is True and proof['originalFilesUnchanged'] is True
    assert sha(a.download/'finalization.json')==proof['finalizationSHA256']
    assert sha(a.download/Path(final['archive']).name)==proof['archiveSHA256']==final['archiveSHA256']
    for name,digest in proof['originalFilesSHA256'].items():assert sha(a.download/name)==digest
    root=a.download/TAG
    assert read(root/'source.json')==expected['sourceH']['source']
    assert read(root/'formula_runtime.json')==expected['sourceH']['formulaRuntime']
    assert read(root/'selection.json')==[CASE]
    assert sha(root/CASE/'input.json')==expected['sourceH']['inputSHA256'][CASE]
    native=read(root/CASE/'native.json');result=read(root/CASE/'result.json');run=read(root/CASE/'run.json')
    assert result['classification']==native and result['run']==run and result['input']==read(root/CASE/'input.json')
    assert run['status']=='complete' and type(run['exitCode']) is int and run['exitCode']==0
    assert run['command'][run['command'].index('-K')+1]=='32g' and run['timeoutSeconds']==14400
    assert native['nativeChainIdentitiesVerified'] is True
    print(json.dumps({'status':'PASS','acceptedOrdinaryHShadow':True,'case':CASE,'catalogueSelectionPerformed':False,'sourceSHA256':expected['sourceH']['source']['sha256'],'nativeSHA256':sha(root/CASE/'native.json'),'resultSHA256':sha(root/CASE/'result.json'),'archiveSHA256':final['archiveSHA256']},indent=2))
if __name__=='__main__':main()
