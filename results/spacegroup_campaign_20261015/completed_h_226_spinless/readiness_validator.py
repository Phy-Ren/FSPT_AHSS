#!/usr/bin/env python3
"""Read-only snapshot gate. Never sends signals or creates accepted output."""
import argparse, datetime, hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = Path('/home/xingyu/FSPT_AHSS_insulator')
BASE = HERE.parent
DOWNLOAD = Path('/home/xingyu/insulator-campaign-download')
HPLAN = Path('/home/xingyu/AllFSPT_reviews/spacegroup_h_remaining_20261015/plan.json')
HELPER = HERE / 'preservation-helper-c26f3de'
sys.dont_write_bytecode = True
sys.path.insert(0, str(HELPER))
from scripts.collect_expansion import load_campaign
from scripts.recover_paired_campaign import scientific_checks

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_bytes())
def write(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def parent_entry(tag, cases, label):
    p=DOWNLOAD/(tag+'-finalized')/tag
    return dict(ci=str(p),e8=str(p)+'-e8',cases=sorted(cases),label=label)
def verify_h_download(ci,e8,count):
    """Require the pinned H/G/VM path and immutable accepted download evidence."""
    folder=ci.parent; tag=ci.name
    expected_source='80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b'
    expected_e8='994af05b2ab8cea90002e6c75dd2442736b3f1096bf0ceab98703f6e90dc2214'
    expected_vm='0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2'
    f=read(folder/'finalization.json');d=read(folder/'download_verification.json')
    if (f.get('state')!='complete' or f.get('tag')!=tag or f.get('acceptedCount')!=count
            or f.get('selectedCount')!=count or f.get('sourceVerified') is not True
            or f.get('runtimeVerified') is not True or f.get('sourceSHA256')!=expected_source
            or f.get('source')!='/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-h'
            or f.get('postprocessor')!='/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-g'):
        raise ValueError('H finalization is not the expected complete frozen-source campaign')
    if (read(ci/'source.json')['sha256']!=expected_source
            or read(e8/'source.json')['sha256']!=expected_e8
            or f['selectionSHA256']!=sha(ci/'selection.json')):
        raise ValueError('H CI/E8 source or original selection pin differs')
    runtime=read(ci/'formula_runtime.json')
    if (runtime.get('librarySHA256')!=expected_vm or runtime.get('libraryPresent') is not True
            or runtime.get('libraryPath')!='/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-h/insulator/_compiled/u1_dag_vm.so'):
        raise ValueError('H formula runtime differs from pinned VM')
    if (d.get('finalizationSHA256')!=sha(folder/'finalization.json')
            or d.get('finalizationUnchangedAcrossDownload') is not True
            or d.get('archiveMemberSafetyVerified') is not True
            or d.get('frozenCollectorExactReplay') is not True
            or d.get('frozenCollectorExitCode')!=0 or d.get('acceptedCount')!=count):
        raise ValueError('Missing exact accepted-download replay proof')
    archive=folder/(tag+'-evidence.tar.gz')
    if (sha(archive)!=f['archiveSHA256'] or d.get('archiveSHA256')!=f['archiveSHA256']
            or archive.stat().st_size!=f['archiveBytes']):
        raise ValueError('Finalized evidence archive changed')
    hashes=d.get('originalFilesSHA256')
    if not isinstance(hashes,dict) or not hashes: raise ValueError('Missing original download file hashes')
    for name,h in hashes.items():
        q=folder/name
        if folder not in q.resolve().parents or sha(q)!=h: raise ValueError('Downloaded original bytes changed: '+name)
    accepted=folder/(tag+'-accepted');collection=read(accepted/'collection.json')
    if collection.get('accepted') is not True or len(collection.get('collections',[]))!=1:
        raise ValueError('H download lacks accepted collection')
    row=collection['collections'][0]
    if (row['family'],row['path'],row['count'])!=('spacegroup','3p1d/space_groups',count):
        raise ValueError('H accepted collection has wrong coverage')
    for name,h in row['filesSHA256'].items():
        if sha(accepted/row['path']/name)!=h: raise ValueError('Accepted collection changed')
    for name,kind in [('ci_results.json',ci),('results.json',e8)]:
        records=read(accepted/row['path']/name)
        if len(records)!=count or {x['input']['id'] for x in records}!=set(read(ci/'selection.json')):
            raise ValueError('Accepted record IDs differ from full parent')
        if any(x!=read(kind/x['input']['id']/'result.json') for x in records):
            raise ValueError('Accepted records differ from exact original results')
    return dict(finalizationSHA256=sha(folder/'finalization.json'),downloadProofSHA256=sha(folder/'download_verification.json'),
                acceptedCollectionSHA256=sha(accepted/'collection.json'),archiveSHA256=sha(archive),
                ciSourceSHA256=expected_source,e8SourceSHA256=expected_e8,formulaVMSHA256=expected_vm)

def validate_parent(item):
    ci,e8=Path(item['ci']),Path(item['e8'])
    if not ci.is_dir() or not e8.is_dir():
        return dict(state='awaiting_downloaded_accepted_parent',label=item['label'],cases=item['cases'])
    c,_,cp=load_campaign(ci,'ci',allow_recovered=True)
    e,_,ep=load_campaign(e8,'e8',allow_recovered=True)
    if set(c)!=set(e): raise ValueError('CI/E8 complete parent selections differ')
    for k in c:
        if (e[k]['directory']/'ci_result.json').read_bytes()!=(c[k]['directory']/'result.json').read_bytes():
            raise ValueError('Exact full-parent CI/E8 bytes disagree: '+k)
    download = verify_h_download(ci,e8,len(c)) if ci.name.startswith('sgfull-20261015-h-') else None
    selected=item.get('cases',sorted(c))
    if not set(selected)<=set(c): raise ValueError('Requested parent cases absent')
    checks=[]
    for k in selected:
        raw=(REPO/'insulator_catalog/generated'/(k+'.json')).read_bytes()
        if (c[k]['directory']/'input.json').read_bytes()!=raw or c[k]['record']['input']!=json.loads(raw):
            raise ValueError('Catalogue input differs: '+k)
        checks.append(dict(id=k,**scientific_checks(c[k]['record']['classification'],json.loads(raw))))
    return dict(state='validated',label=item['label'],cases=selected,ci=cp,e8=ep,scientificChecks=checks,acceptedDownloadEvidence=download)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--n02-probe',type=Path,default=HERE/'n02-final-helper-probe.json')
    ap.add_argument('--n03-probe',type=Path,default=HERE/'n03-final-helper-probe.json')
    ap.add_argument('--tail-manifest',type=Path,help='Explicit fully validated alternative CI/E8 parents selecting exactly the four tail IDs')
    ap.add_argument('--freshness-seconds',type=float,default=300)
    args=ap.parse_args()
    if args.output.exists(): raise ValueError('Use a new readiness output path')
    snapshot=read(HERE/'preservation_helper_snapshot.json')
    actual={str(p.relative_to(HELPER)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in HELPER.rglob('*') if p.is_file()}
    if actual!=snapshot['files']: raise ValueError('Pinned helper tree changed')
    original=read(BASE/'planned_full_manifest.json')['campaigns']
    plan=read(HPLAN); baseline={x['id']:x for x in plan['availabilityObservations']}
    expected={'spacegroup_%03d_%s'%(n,s) for n in range(1,231) for s in ('spinless','spin_half')}
    tail=set(plan['excludedTailCases']); replacement=set(plan['candidateCases'])
    assert len(tail)==4 and len(replacement)==24 and not tail&replacement
    static=[x for x in original if x['label'] not in ('Frozen G n02','Frozen G n03')]
    for x in static:
        if 'cases' not in x: x['cases']=read(Path(x['ci'])/'selection.json')
    static_checks=[validate_parent(x) for x in static]
    assert all(x['state']=='validated' for x in static_checks)
    assert sum(len(x['cases']) for x in static)==344
    additions=[parent_entry('sgfull-20261015-h-remaining-'+n,plan['assignments'][n],'H replacement '+n) for n in ('n02','n03')]
    tail_entries=read(args.tail_manifest)['campaigns'] if args.tail_manifest else [parent_entry('sgfull-20261015-h-tail-n08',tail,'H original paired tail')]
    flat=[k for x in tail_entries for k in x['cases']]
    if len(flat)!=4 or set(flat)!=tail: raise ValueError('Tail alternative must select exactly four unique tail IDs')
    additions+=tail_entries
    added_checks=[validate_parent(x) for x in additions]
    probes=[]; needed_entries=[]; mapping={}
    now=datetime.datetime.now(datetime.timezone.utc)
    for n,path in [('n02',args.n02_probe),('n03',args.n03_probe)]:
        p=read(path); rows=p['cases']; ids={x['id'] for x in rows}
        required=set(plan['GSelections'][p['root']])-replacement-tail
        if ids!=required: raise ValueError('Wrong G complement probe: '+n)
        if p['selectionSHA256']!=plan['GSelectionSHA256'][p['root']]: raise ValueError('G original selection changed')
        if not p['sourceRuntimeVerification']['sourceSnapshotVerified'] or not p['sourceRuntimeVerification']['formulaRuntimeVerified']: raise ValueError('Source/runtime not verified')
        if p['plannedRecoveryHelperSHA256']!=sha(HELPER/'scripts/recover_paired_campaign.py'): raise ValueError('Wrong planned recovery helper')
        if not p['processPreflight']['valid'] or not p['processPreflight']['noSignalsSent']: raise ValueError('Not a successful read-only ownership preflight')
        for r in rows:
            b=baseline[r['id']]
            if not all([r['nativeAvailable'],r['nativeUnchangedAcrossRead'],r['plannedPreservationHelperSupportsCase'],b['nativeAvailable']]): raise ValueError('G native evidence missing')
            if r['hashes']['native.json']!=b['nativeSHA256'] or r['hashes']['input.json']!=b['inputSHA256']: raise ValueError('G launch-baseline native/input bytes changed')
            if r['hashes']['input.json']!=sha(REPO/'insulator_catalog/generated'/(r['id']+'.json')): raise ValueError('G input outside exact catalogue')
            if r['ordinaryComplete'] and not r.get('plannedHelperOrdinaryInspectionPassed'): raise ValueError('Ordinary helper guard not tested')
            if not r['ordinaryComplete'] and not r['potentialPairedRecovery']: raise ValueError('No rigorous pending-pair path')
        age=(now-datetime.datetime.fromisoformat(p['sampleUTC'])).total_seconds()
        probes.append(dict(node=n,path=str(path),sha256=sha(path),sampleUTC=p['sampleUTC'],ageSeconds=age,fresh=0<=age<=args.freshness_seconds,
                           ordinaryCount=sum(x['ordinaryComplete'] for x in rows),pendingPairedCases=[x['id'] for x in rows if not x['ordinaryComplete']],
                           nativeCount=len(rows),allNativeBytesEqualPrelaunchEvidence=True,runner=p['processPreflight']['runner']))
        # These are proposed NEW destinations, never created by this script.
        tag='sgfull-20261015-g-'+n+'-preserved-c26f3de'
        root=DOWNLOAD/'sgfull-20261015-g-preserved-c26f3de'/tag
        needed_entries.append(dict(ci=str(root),e8=str(root)+'-e8',cases=sorted(ids),label='Proposed preserved G '+n,reason='Original complete parent validated after deliberate stop; select the exact complement of H replacements'))
    for x in static+needed_entries+additions:
        for k in x['cases']:
            if k in mapping: raise ValueError('Duplicate partition ID: '+k)
            mapping[k]=x['label']
    if set(mapping)!=expected: raise ValueError('Partition does not cover exactly460 inputs')
    if sum(x['nativeCount'] for x in probes)!=88: raise ValueError('G complement must be88')
    hready=all(x['state']=='validated' for x in added_checks)
    report=dict(schema='u1-accelerated-readiness-v1',sampleUTC=now.isoformat(),exactPlannedCoverage=460,
                acceptedStaticSelectedCount=344,requiredGComplementCount=88,requiredHReplacementCount=28,
                originalManifestSHA256=sha(BASE/'planned_full_manifest.json'),launchPlanSHA256=sha(HPLAN),
                helperSnapshot=snapshot,staticParents=static_checks,replacementParents=added_checks,gReadOnlyProbes=probes,
                coverageMap=mapping,h28Accepted=hready,allG88PreviouslyAvailableAndUnchanged=True,
                readyForRootStopReview=hready and all(x['fresh'] for x in probes),authorizesSignals=False,
                caveat='G evidence is not stopped recovery or final acceptance. Root must repeat live ownership checks at stop; H parents must be fully accepted. A partial pair cannot be selected out of a running parent.',
                candidateManifest=dict(schema='u1-spacegroup-assembly-v1',campaigns=static+needed_entries+additions))
    write(args.output,report)
    print(json.dumps({k:report[k] for k in ('exactPlannedCoverage','acceptedStaticSelectedCount','requiredGComplementCount','h28Accepted','readyForRootStopReview','authorizesSignals')},sort_keys=True))
if __name__=='__main__': main()
