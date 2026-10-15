from concurrent.futures import ThreadPoolExecutor
import hashlib,json,os,signal,socket,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCE=Path('/home/xingyu/AllFSPT_reviews/point3_optimized_g_20261015/source')

def job(spec):
    sg,mode=spec;case=f'spacegroup_{sg:03d}_spin_half';folder=BASE/f'{case}_{mode}';folder.mkdir()
    def path(name):return json.dumps(str(folder/name))
    driver=f'''U1_ROOT:={json.dumps(str(SOURCE))};;U1_USE_KOSZUL:={str(mode=='koszul').lower()};;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
SizeScreen([200,10000]);;stageStart:=Runtime();;PROFILE_PHASE:="setup";;rootNumber:=0;;
OnBreak:=function()
 Print("INTERRUPTED ",PROFILE_PHASE," ROOT ",rootNumber," CPU_MS ",Runtime()-stageStart,"\\n");
 DisplayProfile(100000000,0);QUIT_GAP(0);
end;;
WriteRecord:=function(path,value)local f;f:=OutputTextFile(path,false);SetPrintFormattingStatus(f,false);WriteLine(f,U1JSON(value));CloseStream(f);end;;
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/{case}.g"));;
setupStart:=Runtime();;c:=U1CatalogContext(U1_INPUT,6);;
c.chargePrimaryMode:="native";;c.phaseClassMode:="cycles";;c.closedChargeSourceMode:="certified";;
Print("CONTEXT_MS ",Runtime()-setupStart,"\\n");;
HQ:=U1Cohomology(c,3,"Zr");;HP:=U1Cohomology(c,4,"U1s");;HO:=U1Cohomology(c,5,"U1s");;
Print("COHOMOLOGY_MS ",Runtime()-setupStart,"\\n");;
ProfileFunctions([U1Native,U1SolveData,U1SolveNative,U1CheckCompletedState,U1ChainFromBar,U1ChainToBar,U1ChainHomotopy,U1ContractCell,U1ContractFromBar,U1CombineChain,U1Key,U1ContractCellMod2]);;
PROFILE_PHASE:="primary";;stageStart:=Runtime();;Print("STAGE_STARTED primary\\n");;
maps:=List(HQ.generators,q->U1ChargeObstructionCoordinates(c,3,HO,q));;
primaryMS:=Runtime()-stageStart;;Print("PRIMARY_COMPLETE CPU_MS ",primaryMS,"\\n");;
K:=U1MapKernel(maps,HO.orders,Length(HQ.generators));;
WriteRecord({path('lower.json')},rec(dimensions:=List([0..6],Dimension(c.R)),chargeOrders:=HQ.orders,phaseOrders:=HP.orders,targetOrders:=HO.orders,chargeGenerators:=HQ.generators,map:=maps,kernel:=K,
 chargeDifferential:=U1Differential(c,3,"Zr"),phaseDifferential:=U1Differential(c,4,"Zs"),
 primaryMilliseconds:=primaryMS));;
PROFILE_PHASE:="completion";;stageStart:=Runtime();;Print("STAGE_STARTED completion\\n");;
roots:=[];;
for v in K do
 rootNumber:=rootNumber+1;rootStart:=Runtime();
 Print("ROOT_BEGIN ",rootNumber," CPU_MS ",Runtime()-stageStart,"\\n");
 state:=U1CertifiedClosedChargeState(c,3,v*HQ.generators);;
 source:=U1Source(c,3,state);;
 Print("SOURCE_READY ",rootNumber," literalZero=",source=U1Zero," CPU_MS ",Runtime()-stageStart,"\\n");
 phase:=U1SolveData(c,5,"U1s",source);;
 if phase=fail then Error("Kernel charge failed completion");fi;
 Print("PRIMITIVE_READY ",rootNumber," CPU_MS ",Runtime()-stageStart,"\\n");
 state.phase:=phase.primitive;;checked:=U1CheckCompletedState(c,3,state);;
 Add(roots,rec(chargeCoordinates:=v,nativeCharge:=v*HQ.generators,nativeSource:=phase.nativeObstruction,nativePrimitive:=phase.nativePrimitive,completedNative:=checked,cpuMilliseconds:=Runtime()-rootStart));;
 WriteRecord({path('completed_roots.json')},roots);
 Print("ROOT_COMPLETE ",rootNumber," CPU_MS ",Runtime()-stageStart,"\\n");
od;
completionMS:=Runtime()-stageStart;;Print("COMPLETION_ALL_DONE CPU_MS ",completionMS,"\\n");;
workerCalls:=0;;if IsBound(c.workerCalls) then workerCalls:=c.workerCalls;fi;
WriteRecord({path('result.json')},rec(primaryMilliseconds:=primaryMS,completionMilliseconds:=completionMS,completedRoots:=Length(roots),workerCalls:=workerCalls,nativeCompletionChecks:=c.completedStateChecks));;
DisplayProfile(100000000,0);;QUIT_GAP(0);
'''
    (folder/'driver.g').write_text(driver)
    command=['gap','-q','-b','-o','4g',str(folder/'driver.g')]
    started=time.monotonic();phase='setup';stage=started;interrupted=False
    with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
        process=subprocess.Popen(command,stdout=out,stderr=err,stdin=subprocess.DEVNULL,start_new_session=True)
        while process.poll() is None:
            raw=(folder/'stdout.log').read_bytes()
            latest='completion' if b'STAGE_STARTED completion' in raw else 'primary' if b'STAGE_STARTED primary' in raw else 'setup'
            if latest!=phase:phase=latest;stage=time.monotonic()
            if time.monotonic()-stage>=120:
                process.send_signal(signal.SIGINT);interrupted=True
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
                break
            time.sleep(.15)
    record=dict(case=case,latticeResolution=mode,command=command,host=socket.gethostname(),elapsedSeconds=time.monotonic()-started,
                lastStage=phase,stageElapsedSeconds=time.monotonic()-stage,interruptedAtBound=interrupted,
                exitCode=process.returncode,complete=(folder/'result.json').is_file(),source=str(SOURCE))
    (folder/'run.json').write_text(json.dumps(record,indent=2)+'\n');return record
with ThreadPoolExecutor(max_workers=4) as pool:
    rows=list(pool.map(job,[(141,'koszul'),(141,'hap'),(229,'koszul'),(229,'hap')]))
manifest={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((SOURCE/'gap').glob('*.g'))}
for sg in (141,229):
 p=SOURCE/f'insulator_catalog/generated/spacegroup_{sg:03d}_spin_half.g';manifest[str(p.relative_to(SOURCE))]=hashlib.sha256(p.read_bytes()).hexdigest()
summary=dict(scope='Full initial charge completion and native identities only, no sheet/gauge/root presentation; four simultaneous local jobs',runs=rows,sourceFiles=manifest)
(BASE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary['runs'],indent=2))
