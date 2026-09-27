# Full cochain audit after a historical-draft discrepancy. No expected group
# or expected relation is embedded here; preserve the independent result.
AFS_ROOT:=GAPInfo.SystemEnvironment.AFS_TEST_SOURCE;;
AFS_STACK_AUDIT:=true;;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","backend_diagonal.g","formula_data.g",
    "formula_fast.g","pip_o5_program.g","pip_o5_sign.g","pip_o5_general.g","formulas.g",
    "classification.g","pip.g","stacking.g","pip_coordinate_data.g",
    "pip_coordinates.g","pip_diagonal_data.g","pip_c4_data.g","pip_stacking.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
sg:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(sg);;C:=AFSClassify(ctx);;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_GENERIC_PIP) then
  AFS_PIP_USE_C4:=false;
fi;
freeExport:=fail;;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_FREE) then
  Read(Concatenation(AFS_ROOT,"/gap/pip_free.g"));
  free:=AFSFreePipFromClassification(C);
  Assert(0,free.status="computed");
  for x in free.generators do
    Assert(0,C.Hp.coordinates(AFSNative(ctx,1,"Zs",x.n))=x.h1Coordinates);
    Assert(0,AFSStackSupportZero(ctx,2,0,AFSCoboundary(ctx,"Zs",x.n)));
    source:=AFSFormula("pip_majorana",ctx,rec(p:=1,n:=x.n));
    Assert(0,AFSStackSupportZero(ctx,3,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.b),source])));
    source:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=x.n,b:=x.b));
    Assert(0,AFSStackSupportZero(ctx,4,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.c),source])));
    source:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));
    Assert(0,AFSStackSupportZero(ctx,5,1,AFSCoadd(1,[AFSCoboundary(ctx,"U1s",x.v),AFSComul(1,-1,source)])));
    AFSUseGeneralPipO5:=false;
    interpreted:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));
    AFSUseGeneralPipO5:=true;
    checked:=0;
    for cell in [1..Minimum(4,Dimension(ctx.R)(5))] do
      tuples:=AFSChainToBar(ctx.bar,5,cell);
      for term in tuples{[1..Minimum(12,Length(tuples))]} do
        Assert(0,CallFuncList(source,term[3])=CallFuncList(interpreted,term[3]));
        checked:=checked+1;
      od;
    od;
    Print("ACTUAL_FREE_TOWER_GENERAL_COMPILED_INTERPRETED_PASS ",sg," tuples=",checked,"\n");
    x.checkedFlatComparisonSupport:=true;
  od;
  freeExport:=AFSFreePipExport(C,free);
  Print("FREE_PIP_FULL_SUPPORT_PASS ",sg," basis=",free.latticeBasis,"\n");
fi;
result:=AFSExplicitPipStacking(C);;
Assert(0,result.status="computed");
for generator in Filtered(result.lower.generators,g->g.layer=2) do
  x:=generator.state;fast:=AFSStackPower(ctx,x,2);
  # Force the independent expression-graph evaluator of the delivered U4,
  # bypassing its compiled straight-line program and product simplifications.
  AFSUseFastFormulas:=false;
  literalM:=AFSFormula("majorana_product",ctx,rec(p:=2,a:=x.a,b:=x.a));
  literalU:=AFSFormula("stacking",ctx,rec(p:=2,a:=x.a,c:=x.c,b:=x.a,cp:=x.c));
  AFSUseFastFormulas:=true;
  literalV:=AFSCoadd(1,[x.v,x.v,literalU]);
  Assert(0,AFSStackSupportZero(ctx,3,2,AFSCoadd(2,[fast.c,literalM])));
  Assert(0,AFSStackSupportZero(ctx,4,1,AFSCoadd(1,[fast.v,AFSComul(1,-1,literalV)])));
  Print("LITERAL_UNCHANGED_CA_MC_SQUARE_PASS ",sg," ",generator.name,"\n");
od;
if IsBound(result.pipGenerator) then
  x:=result.pipGenerator;
  Assert(0,AFSStackSupportZero(ctx,2,0,AFSCoboundary(ctx,"Zs",x.n)));
  source:=AFSFormula("pip_majorana",ctx,rec(p:=1,n:=x.n));
  Assert(0,AFSStackSupportZero(ctx,3,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.b),source])));
  source:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=x.n,b:=x.b));
  Assert(0,AFSStackSupportZero(ctx,4,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.c),source])));
  source:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));
  Assert(0,AFSStackSupportZero(ctx,5,1,AFSCoadd(1,[AFSCoboundary(ctx,"U1s",x.v),AFSComul(1,-1,source)])));
  Assert(0,AFSStackCheckFlat(ctx,result.pipSquare.target));
  Assert(0,result.pipReduction.witness.checkedComparisonSupport);
fi;
LoadPackage("json");;
record:=rec(space_group:=sg,source:=AFS_ROOT,stacking:=AFSExplicitPipExport(C,result),
  literalUnchangedCAMCSquaresChecked:=Length(Filtered(result.lower.generators,g->g.layer=2)));
if freeExport<>fail then record.freeLattice:=freeExport;fi;
record.genericCompiledCalls:=AFSPipO5GeneralCalls;
tag:="";;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_TAG) then
  tag:=Concatenation("_",GAPInfo.SystemEnvironment.AFS_TEST_TAG);
fi;
stream:=OutputTextFile(Concatenation("runs/draft_extension_audit_sg",String(sg),tag,".json"),false);;
SetPrintFormattingStatus(stream,false);WriteAll(stream,GapToJsonString(record));CloseStream(stream);
Print("DRAFT_DISAGREEMENT_FULL_COCHAIN_AUDIT_PASS ",sg," invariants=",result.invariants,"\n");
QUIT_GAP(0);
