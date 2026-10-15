#!/usr/bin/env python3
"""Structural preconditions for the isolated ordered-edge U1Cup rewrite."""
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

root=Path(__file__).resolve().parent
candidate=root.parent/'cup_candidate'
cuts=candidate/'source/gap/cup_data.g'
counts={'cup_tables':0,'terms':0,'edge_accesses':0}
for line in cuts.read_text().splitlines():
    match=re.fullmatch(r'U1CupCuts\.c(\d+)_(\d+)_(\d+):=(.*);;',line)
    if not match:
        continue
    p,q,i=map(int,match.group(1,2,3))
    degree=p+q-i
    counts['cup_tables']+=1
    for left,right,sign in ast.literal_eval(match.group(4)):
        counts['terms']+=1
        assert len(left)==p+1 and len(right)==q+1
        for chain in [left,right]:
            assert all(1<=vertex<=degree+1 for vertex in chain)
            for start,end in zip(chain,chain[1:]):
                counts['edge_accesses']+=1
                assert start<end
gap=subprocess.run(['gap','-q','-b'],input='if [1..0]<>[] or [2..1]<>[] then Error("ranges");fi;Print("PASS\\n");QUIT;\n',
                   text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
assert gap.stdout.strip()=='PASS' and not gap.stderr
out={'status':'PASS','scope':'structural cut-domain and degree-zero range checks; algebraic equivalence is proved in review.md',
     'counts':counts,'gapDegreeZeroRangeCheck':gap.stdout.strip(),
     'hashes':{str(path.relative_to(candidate)):hashlib.sha256(path.read_bytes()).hexdigest()
               for path in [candidate/'change.patch',cuts,candidate/'source/gap/cochains.g']}}
(root/'result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2))
