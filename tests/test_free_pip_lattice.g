AFS_ROOT:=".";;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","backend_diagonal.g","formula_data.g",
    "formula_fast.g","pip_o5_program.g","pip_o5_sign.g","formulas.g",
    "classification.g","pip.g","stacking.g","pip_free.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
sg:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(sg);;C:=AFSClassify(ctx);;
originalTower:=fail;;
if IsBound(C.pipLiftData) then originalTower:=C.pipLiftData;fi;
result:=AFSFreePipFromClassification(C);;
Assert(0,result.status="computed" and result.rank=C.summary.pip.free_rank);
if originalTower<>fail then Assert(0,C.pipLiftData=originalTower);fi;
Print("FREE_PIP_LATTICE ",sg," index=",result.latticeIndex,
  " basis=",result.latticeBasis,"\n");
for x in result.generators do
  Assert(0,C.Hp.coordinates(AFSNative(ctx,1,"Zs",x.n))=x.h1Coordinates);
  Assert(0,AFSStackSupportZero(ctx,2,0,AFSCoboundary(ctx,"Zs",x.n)));
  source:=AFSFormula("pip_majorana",ctx,rec(p:=1,n:=x.n));;
  Assert(0,AFSStackSupportZero(ctx,3,2,
    AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.b),source])));
  Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=x.n,b:=x.b));;
  Assert(0,AFSStackSupportZero(ctx,4,2,
    AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.c),Q])));
  O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));;
  Assert(0,AFSStackSupportZero(ctx,5,1,
    AFSCoadd(1,[AFSCoboundary(ctx,"U1s",x.v),AFSComul(1,-1,O)])));
  x.checkedFlatComparisonSupport:=true;
od;
export:=AFSFreePipExport(C,result);;
LoadPackage("json");;
serialized:=GapToJsonString(export);;
Assert(0,Length(serialized)>0);
Print("FREE_PIP_GENERATOR_COORDINATES ",List(export.generators,g->g.h1Coordinates),"\n");
Print("FREE_PIP_LATTICE_FULL_WITNESS_PASS ",sg," JSONbytes=",Length(serialized),"\n");
QUIT_GAP(0);
