#!/usr/bin/env python3
"""Build or check the saved catalogue file manifest without numerical work."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    index=json.loads((HERE/'index.json').read_text())
    counts=Counter(r['artifact_kind'] for r in index['cases'])
    pending=json.loads((HERE/'pending.json').read_text())['cases']
    files={}
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or p==HERE/'MANIFEST.json' or '__pycache__' in p.parts:
            continue
        assert p.suffix in {'.md','.json','.csv','.py'},p
        raw=p.read_bytes()
        files[str(p.relative_to(HERE))]=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    result=dict(schema='fspt-consolidated-example-files-v1',accepted_records=index['record_count'],
        accepted_scientific_summaries=counts['accepted-scientific-summary'],
        retained_raw_results=counts['retained-complete-raw-result'],pending_inputs=len(pending),files=files,
        scope='Hashes of this additive catalog and its generated files. Earlier complete raw results retain their own original hashes in index.json.')
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    target=HERE/'MANIFEST.json'
    if args.check:assert target.read_text()==data
    else:target.write_text(data)
    print(json.dumps(dict(status='passed',mode='check' if args.check else 'write',files=len(files),records=index['record_count'])))

if __name__=='__main__':main()
