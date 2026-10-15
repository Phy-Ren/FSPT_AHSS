#!/usr/bin/env python3
"""Prepared post-stop/observed-ended G preservation and offline replay. No signals."""
import argparse,hashlib,json,os,socket,subprocess,sys,tarfile
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
BASE=Path('/home/user/xyren/AllFSPT_insulator')
HELPER=BASE/'snapshots/preservation-helper-c26f3de'
SOURCE=BASE/'snapshots/sgfull-20261015-g'
CATALOG=BASE/'snapshots/sgfull-20261015-h/insulator_catalog/generated'
HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_bytes())
def write(path,x):path.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def now():return datetime.now(timezone.utc).isoformat()
def tree(path):
    result={}
    for p in sorted(path.rglob('*')):
        if p.is_symlink():raise ValueError('Symlink in evidence tree: '+str(p))
        if p.is_file():result[str(p.relative_to(path))]=sha(p)
        elif not p.is_dir():raise ValueError('Nonregular evidence artifact')
    return result

def helper_modules(path,config):
    expected=config['helperSnapshot']['files']
    actual={name:{'sha256':value,'bytes':(path/name).stat().st_size} for name,value in tree(path).items()}
    if actual!=expected:raise ValueError('Deployed c26 helper tree differs from all65 pinned files')
    sys.path.insert(0,str(path))
    from scripts import recover_paired_campaign as recovery
    from scripts import collect_expansion as collector
    from scripts import stop_owned_campaign as stopped
    return recovery,collector,stopped

def required_original(root,report,config,node,catalog,recovery):
    spec=config['nodes'][node]
    if (report['originalCampaignRoot']!=spec['root'] or report['sourceSnapshotPath']!=str(SOURCE)
            or report['sourceSHA256']!=spec['sourceSHA256']):raise ValueError('Report names a different original G campaign')
    batches=recovery.validate_stop_report(report)
    if sha(root/'selection.json')!=spec['selectionSHA256']:raise ValueError('Original G selection changed')
    original=recovery.OriginalArtifacts(root,report)
    source,selection=recovery._campaign(original,report)
    checks={}
    for case in spec['requiredCases']:
        baseline=spec['requiredHashes'][case]
        if sha(root/case/'input.json')!=baseline['inputSHA256'] or sha(root/case/'native.json')!=baseline['nativeSHA256']:
            raise ValueError('Required prelaunch native/input bytes changed: '+case)
        if (root/case/'input.json').read_bytes()!=(catalog/(case+'.json')).read_bytes():raise ValueError('Canonical catalogue mismatch: '+case)
        checked=recovery._inspect_case(original,report,batches,source,selection,case)
        if checked['kind']!='ordinary_complete':raise ValueError('Required G case lacks the expected original ordinary completion: '+case)
        checks[case]=checked['checks']
    original.unchanged()
    return checks

def parent_agreement(ci,e8,collector):
    c,_,_=collector.load_campaign(ci,'ci',allow_recovered=True)
    e,_,_=collector.load_campaign(e8,'e8',allow_recovered=True)
    if set(c)!=set(e):raise ValueError('Preserved full CI/E8 selections differ')
    for case in c:
        if (ci/case/'result.json').read_bytes()!=(e8/case/'ci_result.json').read_bytes():raise ValueError('E8 consumed different original CI bytes')
    return len(c)

def run_command(command,logdir,label):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',LC_ALL='C',LANG='C')
    with (logdir/(label+'.stdout.log')).open('wb') as out,(logdir/(label+'.stderr.log')).open('wb') as err:
        subprocess.run(command,check=True,stdout=out,stderr=err,env=env)

def bundle_hashes(roots):
    return {prefix+'/'+name:h for prefix,root in roots.items() for name,h in tree(root).items()}

def remote_run(args,config):
    if socket.gethostname().split('.')[0]!=args.node:raise ValueError('Run on the original compute node')
    recovery,collector,stopped=helper_modules(HELPER,config)
    prepared_bytes=(HERE/'prepared_config.json').read_bytes();script_bytes=Path(__file__).read_bytes()
    root=Path(config['nodes'][args.node]['root']);raw_report=args.report.read_bytes();report=json.loads(raw_report)
    needed=required_original(root,report,config,args.node,CATALOG,recovery)
    verification=stopped.verify_source_runtime(root,SOURCE,read(root/'source.json'))
    if not report.get('formulaRuntimeVerified'):raise ValueError('Report did not verify formula runtime')
    original_before=tree(root)
    tag='sgfull-20261015-g-'+args.node+'-preserved-c26f3de'
    ci=BASE/'runs'/tag;e8=BASE/'runs'/(tag+'-e8');accepted=BASE/'runs'/(tag+'-accepted')
    operation=BASE/'runs'/(tag+'-operation');archive=BASE/'runs'/(tag+'-evidence.tar.gz');completion=BASE/'runs'/(tag+'-completion.json')
    if any(p.exists() for p in [ci,e8,accepted,operation,archive,completion]):raise ValueError('All preservation outputs must be NEW; nothing is overwritten')
    operation.mkdir()
    (operation/'input_report.json').write_bytes(raw_report)
    (operation/'prepared_config.json').write_bytes(prepared_bytes)
    (operation/'postprocess_g.py').write_bytes(script_bytes)
    report_dir=operation/'external_report';report_dir.mkdir();(report_dir/'cancellation.json').write_bytes(raw_report)
    for item in report['evidence']:
        p=args.report.parent/item['path']
        if p.is_symlink() or sha(p)!=item['sha256']:raise ValueError('External report evidence changed')
        target=report_dir/item['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
    ledger=recovery.preserve_campaign(root,args.report,ci)
    required=set(config['nodes'][args.node]['requiredCases'])
    if not required<=set(ledger['preservedCases']) or required&set(ledger['retryCases']):raise ValueError('A required G case was not preserved')
    if not required<=set(ledger['ordinaryCompleteCases']):raise ValueError('Required ordinary execution metadata was not retained')
    commands=[[sys.executable,str(HELPER/'scripts/extend_e8_3p1.py'),'--ci-root',str(ci),'--output',str(e8),'--allow-recovered'],
              [sys.executable,str(HELPER/'scripts/collect_expansion.py'),'--ci-root',str(ci),'--e8-root',str(e8),'--output',str(accepted),'--allow-recovered']]
    for label,command in zip(['e8','collector'],commands):run_command(command,operation,label)
    count=parent_agreement(ci,e8,collector);collection=read(accepted/'collection.json')
    if collection.get('accepted') is not True or sum(x['count'] for x in collection['collections'])!=count:raise ValueError('Preserved collection was not accepted')
    required_original(root,report,config,args.node,CATALOG,recovery)
    if tree(root)!=original_before or args.report.read_bytes()!=raw_report:raise ValueError('Original G/report bytes changed during postprocessing')
    helper_modules(HELPER,config);stopped.verify_source_runtime(root,SOURCE,read(root/'source.json'))
    audit=dict(node=args.node,originalRoot=str(root),sourceSHA256=report['sourceSHA256'],reportSHA256=sha(args.report),
               helperSnapshotCommit=config['helperSnapshot']['commit'],helperTreeSHA256=config['helperSnapshot']['treeSHA256'],
               requiredCases=sorted(required),requiredCount=len(required),preservedCount=count,requiredNativeChecks=needed,
               retries=ledger['retryCases'],commands=commands,originalRawFilesUnchanged=True,signalsSent=False,**verification)
    write(operation/'postprocess.json',audit)
    roots={'original-'+root.name:root,ci.name:ci,e8.name:e8,accepted.name:accepted,operation.name:operation}
    members=bundle_hashes(roots)
    with tarfile.open(archive,'w:gz') as tar:
        for prefix,path in roots.items():
            for name in tree(path):tar.add(path/name,arcname=prefix+'/'+name,recursive=False)
    if members!=bundle_hashes(roots) or original_before!=tree(root):raise ValueError('Evidence changed while archiving')
    if args.report.read_bytes()!=raw_report:raise ValueError('External report changed while archiving')
    for item in report['evidence']:
        if sha(args.report.parent/item['path'])!=item['sha256']:raise ValueError('External report evidence changed while archiving')
    helper_modules(HELPER,config);stopped.verify_source_runtime(root,SOURCE,read(root/'source.json'))
    if (HERE/'prepared_config.json').read_bytes()!=prepared_bytes or Path(__file__).read_bytes()!=script_bytes:raise ValueError('Prepared pipeline/config changed during operation')
    result=dict(schema='u1-preserved-g-bundle-v1',state='accepted-preserved-subset',preparedUTC=now(),tag=tag,node=args.node,
                archive=str(archive),archiveSHA256=sha(archive),archiveBytes=archive.stat().st_size,
                roots={'original':'original-'+root.name,'ci':ci.name,'e8':e8.name,'accepted':accepted.name,'operation':operation.name},
                archiveMembersSHA256=members,requiredCases=sorted(required),preservedCount=count,originalSelectedCount=len(read(root/'selection.json')),
                sourceSHA256=report['sourceSHA256'],reportSHA256=sha(args.report),helperTreeSHA256=config['helperSnapshot']['treeSHA256'],
                configSHA256=sha(HERE/'prepared_config.json'),scriptSHA256=sha(Path(__file__)),sourceVerified=True,runtimeVerified=True,
                originalParentUnmodified=True,signalsSent=False)
    write(completion,result)
    print(json.dumps(dict(completion=str(completion),archive=str(archive),archiveSHA256=result['archiveSHA256'],requiredCount=len(required),preservedCount=count),sort_keys=True))

def offline_verify(args,config):
    recovery,collector,_=helper_modules(args.helper,config);final=read(args.completion)
    if (final.get('schema')!='u1-preserved-g-bundle-v1' or final.get('state')!='accepted-preserved-subset'
            or final['node']!=args.node or not final.get('sourceVerified') or not final.get('runtimeVerified')
            or final['configSHA256']!=sha(HERE/'prepared_config.json') or final['scriptSHA256']!=sha(Path(__file__))):raise ValueError('Unexpected preservation completion proof')
    spec=config['nodes'][args.node];tag='sgfull-20261015-g-'+args.node+'-preserved-c26f3de'
    expected_roots={'original':'original-'+Path(spec['root']).name,'ci':tag,'e8':tag+'-e8','accepted':tag+'-accepted','operation':tag+'-operation'}
    if (final.get('roots')!=expected_roots or final.get('requiredCases')!=sorted(spec['requiredCases'])
            or final.get('sourceSHA256')!=spec['sourceSHA256'] or final.get('helperTreeSHA256')!=config['helperSnapshot']['treeSHA256']
            or final.get('signalsSent') is not False or final.get('originalParentUnmodified') is not True):raise ValueError('Unexpected campaign/required subset/provenance')
    if sha(args.archive)!=final['archiveSHA256'] or args.archive.stat().st_size!=final['archiveBytes']:raise ValueError('Downloaded archive hash/length mismatch')
    if args.output.exists():raise ValueError('Offline replay needs a NEW output directory')
    with tarfile.open(args.archive,'r:gz') as tar:
        members=tar.getmembers();names=[x.name for x in members]
        if len(names)!=len(set(names)) or set(names)!=set(final['archiveMembersSHA256']):raise ValueError('Archive members differ from complete manifest')
        for m in members:
            if not m.isfile() or Path(m.name).is_absolute() or '..' in Path(m.name).parts:raise ValueError('Unsafe archive member')
            if hashlib.sha256(tar.extractfile(m).read()).hexdigest()!=final['archiveMembersSHA256'][m.name]:raise ValueError('Archive member hash mismatch')
        args.output.mkdir(parents=True)
        for m in members:
            p=args.output/m.name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(tar.extractfile(m).read())
    roots={k:args.output/n for k,n in final['roots'].items()}
    report_path=roots['operation']/'external_report/cancellation.json'
    if (sha(report_path)!=final['reportSHA256'] or sha(roots['operation']/'postprocess_g.py')!=final['scriptSHA256']
            or sha(roots['operation']/'prepared_config.json')!=final['configSHA256']):raise ValueError('Archived operation differs from completion proof')
    report=read(report_path)
    required_original(roots['original'],report,config,args.node,args.catalog,recovery)
    count=parent_agreement(roots['ci'],roots['e8'],collector)
    if count!=final['preservedCount']:raise ValueError('Preserved count differs')
    ledger=read(roots['ci']/'recovery.json');required=set(config['nodes'][args.node]['requiredCases'])
    if not required<=set(ledger['ordinaryCompleteCases']) or required&set(ledger['retryCases']):raise ValueError('Required cases missing after download')
    replay=args.output/'local-rechecked'
    command=[sys.executable,str(args.helper/'scripts/collect_expansion.py'),'--ci-root',str(roots['ci']),'--e8-root',str(roots['e8']),'--output',str(replay),'--allow-recovered']
    run_command(command,args.output,'local_collector_replay')
    collection=read(roots['accepted']/'collection.json')
    if collection.get('accepted') is not True or sum(x['count'] for x in collection['collections'])!=count:raise ValueError('Original preserved collection was not accepted')
    if final['originalSelectedCount']!=len(read(roots['original']/'selection.json')):raise ValueError('Original selection count differs')
    for item in collection['collections']:
        for name in ['results.json','ci_results.json','validation.json']:
            if sha(replay/item['path']/name)!=item['filesSHA256'][name]:raise ValueError('Frozen collector replay differs: '+name)
    for name,h in final['archiveMembersSHA256'].items():
        if sha(args.output/name)!=h:raise ValueError('Original extracted evidence changed during replay')
    (args.output/'completion.json').write_bytes(args.completion.read_bytes())
    entry=dict(label='Preserved G '+args.node,ci=str(roots['ci']),e8=str(roots['e8']),cases=sorted(required),reason='Exact original G complement; full preserved parent validated')
    write(args.output/'assembly_entry.json',entry)
    proof=dict(verifiedUTC=now(),archiveSHA256=final['archiveSHA256'],completionSHA256=sha(args.completion),requiredCases=sorted(required),
               preservedCount=count,frozenCollectorExactReplay=True,originalExtractedFilesUnchanged=True,helperCommit=config['helperSnapshot']['commit'],
               helperTreeSHA256=config['helperSnapshot']['treeSHA256'],signalsSent=False)
    write(args.output/'download_verification.json',proof);print(json.dumps(proof,sort_keys=True))

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='mode',required=True)
    run=sub.add_parser('run');run.add_argument('--node',required=True,choices=['n02','n03']);run.add_argument('--report',required=True,type=Path)
    v=sub.add_parser('verify');v.add_argument('--node',required=True,choices=['n02','n03']);v.add_argument('--archive',required=True,type=Path);v.add_argument('--completion',required=True,type=Path);v.add_argument('--output',required=True,type=Path);v.add_argument('--helper',required=True,type=Path);v.add_argument('--catalog',required=True,type=Path)
    a=p.parse_args();config=read(HERE/'prepared_config.json')
    if a.mode=='run':remote_run(a,config)
    else:offline_verify(a,config)
if __name__=='__main__':main()
