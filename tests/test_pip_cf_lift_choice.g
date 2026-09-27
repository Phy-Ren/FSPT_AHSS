# Change a genuine surviving CF defining choice in the nonzero integer tower.
# Both squares are reduced against ONE classification and ONE marked lower
# model. No space-group answer table enters this lift-independence check.
AFS_ROOT:=".";;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_SOURCE) then
  AFS_ROOT:=GAPInfo.SystemEnvironment.AFS_TEST_SOURCE;
fi;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","backend_diagonal.g","formula_data.g",
    "formula_fast.g","pip_o5_program.g","pip_o5_sign.g","formulas.g",
    "classification.g","pip.g","stacking.g","pip_coordinate_data.g",
    "pip_coordinates.g","pip_diagonal_data.g","pip_c4_data.g","pip_stacking.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
AFS_PIP_USE_C4:=false;;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_USE_C4) then
  AFS_PIP_USE_C4:=GAPInfo.SystemEnvironment.AFS_TEST_USE_C4="1";
fi;
sg:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(sg);;C:=AFSClassify(ctx);;
Assert(0,2 in C.summary.pip.orders);
Assert(0,Length(C.cfFinalBasis)>0);
model:=AFSStackFromClassification(C);;
lower:=AFSStackClassification(model);;
original:=AFSStackPipLift(C);;
Assert(0,original.status="computed");
square0:=AFSStackPipSquare(ctx,original.state);;
reduced0:=AFSStackReduce(model,square0.target,true);;
Assert(0,reduced0.status="computed");
Print("ORIGINAL_SAME_BASIS_RELATION ",reduced0.coordinates,"\n");

cfIndex:=1;;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_CF_INDEX) then
  cfIndex:=Int(GAPInfo.SystemEnvironment.AFS_TEST_CF_INDEX);
fi;
shift:=AFSCombination(ctx,3,"F2",C.H3,C.cfFinalBasis[cfIndex]);;
Assert(0,ForAny(C.H3.coordinates(AFSNative(ctx,3,"F2",shift)),z->z<>0));
changed:=ShallowCopy(original.state);;
changed.c:=AFSCoadd(2,[changed.c,shift]);;
obstruction:=AFSFormula("pip_obstruction",ctx,
  rec(p:=1,n:=changed.n,b:=changed.b,c:=changed.c));;
AFSStage(ctx,"test_changed_CF_upper_phase");
changed.v:=AFSSolve(ctx,5,"U1s",obstruction);;
Assert(0,changed.v<>fail);
# This is an actual flat defining tower, not merely a change of coordinates.
Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=changed.n,b:=changed.b));;
Assert(0,AFSStackSupportZero(ctx,4,2,
  AFSCoadd(2,[AFSCoboundary(ctx,"F2",changed.c),Q])));
Assert(0,AFSStackSupportZero(ctx,5,1,
  AFSCoadd(1,[AFSCoboundary(ctx,"U1s",changed.v),AFSComul(1,-1,obstruction)])));
AFSStage(ctx,"test_changed_CF_upper_square");
square1:=AFSStackPipSquare(ctx,changed);;
reduced1:=AFSStackReduce(model,square1.target,true);;
Assert(0,reduced1.status="computed");
Print("CHANGED_CF_SAME_BASIS_RELATION ",reduced1.coordinates,"\n");
difference:=reduced1.coordinates-reduced0.coordinates;;
while Length(difference)<Length(lower.generators) do Add(difference,0);od;
rows:=Concatenation(lower.presentation,2*IdentityMat(Length(lower.generators)));;
solve:=AFSStackLatticeSolver(rows,Length(lower.generators));;
witness:=solve(difference);;
Assert(0,witness<>fail);
Assert(0,witness*rows=difference);
if ForAll(lower.invariants,x->x=2) then
  Assert(0,reduced1.coordinates=reduced0.coordinates);
fi;
Print("CF_LIFT_CHOICE_DIFFERENCE_IN_2H_WITNESS ",witness,"\n");
Print("CF_LIFT_CHOICE_SAME_MARKED_LOWER_BASIS_PASS ",sg,"\n");
QUIT_GAP(0);
