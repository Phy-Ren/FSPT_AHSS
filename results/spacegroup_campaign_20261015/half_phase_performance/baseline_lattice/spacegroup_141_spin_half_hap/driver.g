U1_ROOT:="/home/xingyu/AllFSPT_reviews/point3_optimized_g_20261015/source";;U1_USE_KOSZUL:=false;;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
SizeScreen([200,10000]);;stageStart:=Runtime();;PROFILE_PHASE:="setup";;rootNumber:=0;;
OnBreak:=function()
 Print("INTERRUPTED ",PROFILE_PHASE," ROOT ",rootNumber," CPU_MS ",Runtime()-stageStart,"\n");
 DisplayProfile(100000000,0);QUIT_GAP(0);
end;;
WriteRecord:=function(path,value)local f;f:=OutputTextFile(path,false);SetPrintFormattingStatus(f,false);WriteLine(f,U1JSON(value));CloseStream(f);end;;
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/spacegroup_141_spin_half.g"));;
setupStart:=Runtime();;c:=U1CatalogContext(U1_INPUT,6);;
c.chargePrimaryMode:="native";;c.phaseClassMode:="cycles";;c.closedChargeSourceMode:="certified";;
Print("CONTEXT_MS ",Runtime()-setupStart,"\n");;
HQ:=U1Cohomology(c,3,"Zr");;HP:=U1Cohomology(c,4,"U1s");;HO:=U1Cohomology(c,5,"U1s");;
Print("COHOMOLOGY_MS ",Runtime()-setupStart,"\n");;
ProfileFunctions([U1Native,U1SolveData,U1SolveNative,U1CheckCompletedState,U1ChainFromBar,U1ChainToBar,U1ChainHomotopy,U1ContractCell,U1ContractFromBar,U1CombineChain,U1Key,U1ContractCellMod2]);;
PROFILE_PHASE:="primary";;stageStart:=Runtime();;Print("STAGE_STARTED primary\n");;
maps:=List(HQ.generators,q->U1ChargeObstructionCoordinates(c,3,HO,q));;
primaryMS:=Runtime()-stageStart;;Print("PRIMARY_COMPLETE CPU_MS ",primaryMS,"\n");;
K:=U1MapKernel(maps,HO.orders,Length(HQ.generators));;
WriteRecord("/home/xingyu/AllFSPT_reviews/spacegroup_lattice_contraction_20261015/spacegroup_141_spin_half_hap/lower.json",rec(dimensions:=List([0..6],Dimension(c.R)),chargeOrders:=HQ.orders,phaseOrders:=HP.orders,targetOrders:=HO.orders,chargeGenerators:=HQ.generators,map:=maps,kernel:=K,
 chargeDifferential:=U1Differential(c,3,"Zr"),phaseDifferential:=U1Differential(c,4,"Zs"),
 primaryMilliseconds:=primaryMS));;
PROFILE_PHASE:="completion";;stageStart:=Runtime();;Print("STAGE_STARTED completion\n");;
roots:=[];;
for v in K do
 rootNumber:=rootNumber+1;rootStart:=Runtime();
 Print("ROOT_BEGIN ",rootNumber," CPU_MS ",Runtime()-stageStart,"\n");
 state:=U1CertifiedClosedChargeState(c,3,v*HQ.generators);;
 source:=U1Source(c,3,state);;
 Print("SOURCE_READY ",rootNumber," literalZero=",source=U1Zero," CPU_MS ",Runtime()-stageStart,"\n");
 phase:=U1SolveData(c,5,"U1s",source);;
 if phase=fail then Error("Kernel charge failed completion");fi;
 Print("PRIMITIVE_READY ",rootNumber," CPU_MS ",Runtime()-stageStart,"\n");
 state.phase:=phase.primitive;;checked:=U1CheckCompletedState(c,3,state);;
 Add(roots,rec(chargeCoordinates:=v,nativeCharge:=v*HQ.generators,nativeSource:=phase.nativeObstruction,nativePrimitive:=phase.nativePrimitive,completedNative:=checked,cpuMilliseconds:=Runtime()-rootStart));;
 WriteRecord("/home/xingyu/AllFSPT_reviews/spacegroup_lattice_contraction_20261015/spacegroup_141_spin_half_hap/completed_roots.json",roots);
 Print("ROOT_COMPLETE ",rootNumber," CPU_MS ",Runtime()-stageStart,"\n");
od;
completionMS:=Runtime()-stageStart;;Print("COMPLETION_ALL_DONE CPU_MS ",completionMS,"\n");;
workerCalls:=0;;if IsBound(c.workerCalls) then workerCalls:=c.workerCalls;fi;
WriteRecord("/home/xingyu/AllFSPT_reviews/spacegroup_lattice_contraction_20261015/spacegroup_141_spin_half_hap/result.json",rec(primaryMilliseconds:=primaryMS,completionMilliseconds:=completionMS,completedRoots:=Length(roots),workerCalls:=workerCalls,nativeCompletionChecks:=c.completedStateChecks));;
DisplayProfile(100000000,0);;QUIT_GAP(0);
