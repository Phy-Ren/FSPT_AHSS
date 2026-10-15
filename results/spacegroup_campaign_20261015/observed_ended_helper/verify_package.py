#!/usr/bin/env python3
"""Portable byte/provenance checks only; never queries or signals processes."""
import hashlib
import io
import json
from pathlib import Path
import tarfile

ROOT=Path(__file__).resolve().parent

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(name): return json.loads((ROOT/name).read_bytes())

def main():
    manifest=read('artifact_manifest.json')
    for name,item in manifest['files'].items():
        raw=(ROOT/name).read_bytes()
        assert sha(raw)==item['sha256'] and len(raw)==item['bytes'],name
    snapshot=read('snapshot_manifest.json')
    archive=(ROOT/snapshot['archive']).read_bytes()
    assert sha(archive)==snapshot['archiveSHA256']
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tar:
        members=tar.getmembers()
        assert len(members)==snapshot['fileCount'] and {m.name for m in members}==set(snapshot['files'])
        raw_files={}
        for member in members:
            assert member.isfile() and not member.name.startswith('/') and '..' not in Path(member.name).parts
            raw=tar.extractfile(member).read();item=snapshot['files'][member.name]
            assert sha(raw)==item['sha256'] and len(raw)==item['bytes']
            raw_files[member.name]=raw
    assert raw_files['attest_natural_exit.py']==(ROOT/'attest_natural_exit.py').read_bytes()
    assert sha(raw_files['stop_owned_campaign.py'])=='574ee600775d6daa858cb6b20f97bb60843c126669a576daa82b4723dd467871'
    assert sha(raw_files['attest_natural_exit.py'])=='1f2df5fbed694bb85e959f501bbc66f5a81e75975b19f214ae890ae7bf7cba57'
    result=read('local_test_result.json')
    assert result['status']=='PASS' and len(result['testChecks'])==14
    cli=[x for x in result['testChecks'] if x.get('realCLISubprocess')]
    assert len(cli)==3 and sorted(x['exitCode'] for x in cli)==[0,1,1]
    assert all(x['signalsAttempted']==0 and x['passed'] for x in result['testChecks'])
    provenance=read('provenance.json')
    raw=(ROOT/'local_cli_evidence.tar.gz').read_bytes()
    assert sha(raw)==provenance['finalLocalEvidenceSHA256']
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tar:
        traces=[m for m in tar.getmembers() if m.name.endswith('.signals.jsonl')]
        assert len(traces)==3 and all(tar.extractfile(m).read()==b'' for m in traces)
    assert provenance['original217FileLedgerUnchanged'] is True
    print(json.dumps({'status':'PASS','snapshotFiles':snapshot['fileCount'],'localChecks':14,'realCLIChecks':3,'signals':0},sort_keys=True))
if __name__=='__main__':main()
