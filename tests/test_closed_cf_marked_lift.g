# Compare marked CF lifts in one classification and one fixed cohomology basis.
AFS_ROOT:=GAPInfo.SystemEnvironment.AFS_TEST_SOURCE;;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","backend_mod2_contraction.g","backend_bar_mod2.g","backend_half_phase.g",
    "backend_diagonal.g","formula_data.g","formula_fast.g","pip_o5_program.g",
    "pip_o5_sign.g","pip_o5_general.g","formulas.g","classification.g",
    "pip.g","stacking.g","stacking_closed_cf.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
AFS_USE_MOD2_BAR:=false;;AFS_USE_CLOSED_CF_OBSTRUCTION:=false;;
AFS_USE_MOD2_CONTRACTION:=true;;
sg:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(sg);;C:=AFSClassify(ctx);;
Assert(0,Length(C.cfFinalBasis)>0);
count:=Minimum(2,Length(C.cfFinalBasis));;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_CF_COUNT) then
  count:=Minimum(count,Int(GAPInfo.SystemEnvironment.AFS_TEST_CF_COUNT));
fi;
phaseLimit:=infinity;;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_PHASE_LIMIT) then
  phaseLimit:=Int(GAPInfo.SystemEnvironment.AFS_TEST_PHASE_LIMIT);
fi;
records:=[];;
for index in [1..count] do
  AFS_USE_MOD2_BAR:=false;AFS_USE_CLOSED_CF_OBSTRUCTION:=false;
  f:=AFSCombination(ctx,3,"F2",C.H3,C.cfFinalBasis[index]);
  start:=Runtime();old:=AFSStackLift(ctx,1,f);oldTime:=Runtime()-start;
  Assert(0,old.status="computed");
  AFS_USE_MOD2_BAR:=true;AFS_USE_CLOSED_CF_OBSTRUCTION:=true;
  f:=AFSCombination(ctx,3,"F2",C.H3,C.cfFinalBasis[index]);
  start:=Runtime();new:=AFSStackLift(ctx,1,f);newTime:=Runtime()-start;
  Assert(0,new.status="computed");
  Assert(0,old.state.cfPhaseNativeSeed=new.state.cfPhaseNativeSeed);
  Assert(0,AFSStackSupportZero(ctx,3,2,AFSCoadd(2,[old.state.c,new.state.c])));
  fullO:=AFSFormula("obstruction",ctx,rec(p:=2,a:=AFSZero,c:=old.state.c));
  shortO:=AFSClosedCFObstructionLazy(new.state.c);
  Assert(0,AFSStackSupportZero(ctx,5,1,AFSCoadd(1,[fullO,AFSComul(1,-1,shortO)])));
  checked:=0;
  for cell in [1..Dimension(ctx.R)(4)] do
    for term in AFSChainToBar(ctx.bar,4,cell) do
      if checked>=phaseLimit then break;fi;
      Assert(0,AFSMod1(CallFuncList(old.state.v,term[3])-CallFuncList(new.state.v,term[3]))=0);
      checked:=checked+1;
    od;
    if checked>=phaseLimit then break;fi;
  od;
  Add(records,rec(generatorIndex:=index,oldLiftCPUms:=oldTime,newLiftCPUms:=newTime,
    identicalNativePrimitive:=true,identicalCFComparisonSupport:=true,
    identicalObstructionComparisonSupport:=true,identicalPhaseTuplesChecked:=checked,
    phaseSupportComplete:=phaseLimit=infinity));
  Print("CLOSED_CF_SAME_MARKED_LIFT_PASS ",sg," C",index,
    " old_ms=",oldTime," new_ms=",newTime," phase_tuples=",checked,"\n");
od;
LoadPackage("json");;
outputName:=Concatenation("runs/closed_cf_half_phase_marked_lift_sg",String(sg),".json");;
stream:=OutputTextFile(outputName,false);;
SetPrintFormattingStatus(stream,false);
WriteAll(stream,GapToJsonString(rec(space_group:=sg,source:=AFS_ROOT,
  classificationMod2Contraction:=true,
  optionalFormula:="closed-H3-cup1-lazy-half-phase-transfer",checks:=records)));
CloseStream(stream);QUIT_GAP(0);
