#!/usr/bin/env python3
"""Ordinary E6 finalization using frozen G; legacy E has no formula VM."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
import tarfile

BASE=Path('/home/user/xyren/AllFSPT_insulator')
TAG='sgfull-20261015-e-smoke'
CI=BASE/'runs'/TAG
SOURCE=BASE/'snapshots/sgfull-20261015-e'
POST=BASE/'snapshots/sgfull-20261015-g'
E8=BASE/'runs'/(TAG+'-e8')
ACCEPTED=BASE/'runs'/(TAG+'-accepted')
REPORT=BASE/'runs'/(TAG+'-finalization-v2.json')
LOG=BASE/'runs'/(TAG+'-finalization-v2.log')
EXPECTED_POST={'insulator/e8_pointgroup.py': 'eb8a8043c5e5e5205598e76e7e7b13c4fb92c723dbf5c3ae938dc1c8a2ca26cb', 'insulator/e8_h1.py': 'd39bbe2565e933c65641b6ad5886faf81f175f094643c82fb4cdb1a994c8d272', 'insulator/e8_spacegroup.py': '45be021c4fcf607b553af0e333234c49603d1e561196fd657f4b96b3cb4ef340', 'scripts/extend_e8_3p1.py': '63943b99c4c427545d0096e86b78e77565307a601bea799754a4079af853d904', 'scripts/collect_expansion.py': 'ae310c97ce7c41417fbab2b6ed400e1c5ecbc4b8c0252b0dd9f41c7bfd9b1505', 'docs/e8/3p1.md': 'b6c224f8322c4e7c12772ba2f3c692f9228bc722e6194db0eae5958b09a898f8'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(report):
 tmp=REPORT.with_suffix('.tmp');tmp.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');tmp.replace(REPORT)

def main():
 if socket.gethostname().split('.')[0]!='n08':raise ValueError('Must run on n08')
 report={'schema':'u1-e6-legacy-source-finalization-v2','tag':TAG,'node':'n08','state':'validating',
  'startedUTC':datetime.now(timezone.utc).isoformat(),'pythonVersion':platform.python_version(),
  'source':str(SOURCE),'postprocessor':str(POST),'helperSHA256':sha(Path(__file__)),
  'previousFailureReportSHA256':sha(BASE/'runs'/(TAG+'-finalization.json'))}
 with REPORT.open('x') as f:json.dump(report,f,indent=2,sort_keys=True)
 try:
  if E8.exists() or ACCEPTED.exists() or LOG.exists():raise ValueError('Outputs already exist')
  source=read(CI/'source.json');selection=read(CI/'selection.json')
  if source['sha256']!='6817ca7af3c20dbb89139308046456129171d08340014eab83c7c7d6487b86bd':raise ValueError('Unexpected E source')
  if hashlib.sha256(json.dumps(source['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()!=source['sha256']:raise ValueError('Invalid E manifest')
  for name,expected in source['files'].items():
   if sha(SOURCE/name)!=expected:raise ValueError('E source changed: '+name)
  for name,expected in EXPECTED_POST.items():
   if sha(POST/name)!=expected:raise ValueError('G postprocessor source changed: '+name)
  if (CI/'formula_runtime.json').exists() or (SOURCE/'insulator/_compiled').exists():raise ValueError('Unexpected compiled runtime in legacy E')
  sys.path.insert(0,str(POST))
  from scripts.collect_expansion import load_campaign
  records,checks,provenance=load_campaign(CI,'ci')
  if len(records)!=6:raise ValueError('E6 selection incomplete')
  report.update(sourceSHA256=source['sha256'],sourceVerified=True,verifiedSourceFiles=source['files'],
   postprocessorFilesSHA256=EXPECTED_POST,selectedIDs=selection,selectionSHA256=sha(CI/'selection.json'),
   ordinaryAcceptanceChecks=checks,recoveryOptIn=False,
   formulaRuntimeScope='Legacy ce152c6 has no insulator/_compiled and predates formula_runtime.json; all original Python formula source files verified. No VM check is applicable.',
   state='extending_E8')
  save(report)
  env=dict(os.environ,LC_ALL='C',LANG='C',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
  env['PATH']=str(BASE/'runtime/bin')+':'+env['PATH']
  commands=[[str(BASE/'runtime/bin/python3'),str(POST/'scripts/extend_e8_3p1.py'),'--ci-root',str(CI),'--output',str(E8)],
   [str(BASE/'runtime/bin/python3'),str(POST/'scripts/collect_expansion.py'),'--ci-root',str(CI),'--e8-root',str(E8),'--output',str(ACCEPTED)]]
  report['commands']=commands;save(report)
  with LOG.open('x') as log:
   for command in commands:subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
  collection=read(ACCEPTED/'collection.json')
  if not collection['accepted'] or sum(x['count'] for x in collection['collections'])!=6:raise ValueError('Final collection incomplete')
  for cid in selection:
   if sha(CI/cid/'result.json')!=provenance['resultHashes'][cid]:raise ValueError('CI input mutated')
  archive=BASE/'runs'/(TAG+'-evidence-v2.tar.gz')
  with tarfile.open(archive,'x:gz') as tar:
   for path in (CI,E8,ACCEPTED):tar.add(path,arcname=path.name)
  report.update(state='complete',acceptedCount=6,ciArtifactsUnchanged=True,
   archive=str(archive),archiveSHA256=sha(archive),archiveBytes=archive.stat().st_size,
   endedUTC=datetime.now(timezone.utc).isoformat());save(report)
 except Exception as exc:
  report.update(state='failed',error=type(exc).__name__+': '+str(exc),endedUTC=datetime.now(timezone.utc).isoformat());save(report);raise
 print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()

