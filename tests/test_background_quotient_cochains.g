AFS_ROOT:=GAPInfo.SystemEnvironment.AFS_BQ_SOURCE;;
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
for name in ["backend.g","backend_mod2_contraction.g","backend_diagonal.g",
  "class_coordinates.g","formula_data.g","pip_o5_program.g","formulas.g",
  "formula_fast.g","pip_o5_sign.g","pip_o5_general.g","crystalline_background.g",
  "background_operations.g","pip_o5_background.g","classification.g","pip.g",
  "stacking.g","pip_incoming_background.g","background_quotient.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",name));
od;
number:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(number);;AFSInstallCrystallineBackground(ctx);;AFSReduceCrystallineBackground(ctx);;
Assert(0,ctx.s=AFSZero and ctx.omega2<>AFSZero);
C:=AFSClassify(ctx);;before:=StructuralCopy(C.summary);;
incomingState:=AFSBackgroundIncomingState(ctx);;
Assert(0,AFSStackCheckFlat(ctx,incomingState));
Q:=AFSBackgroundQuotient(C,incomingState,rec(orderDivides:=16,
  formula:="normalized-CA-H0-pip-boundary",source:="gap/pip_incoming_background.g"));;
Assert(0,Q.status="computed");
Assert(0,C.summary=before);
Assert(0,IsBound(Q.basisChange.replacedMCPivot));
Assert(0,Sum(Q.incomingCoordinates)=1 and Q.incomingOrder>1);
Assert(0,Product(Q.lower.invariants)*Q.incomingOrder=Product(Q.preQuotientLower.invariants));
Assert(0,Product(Concatenation(Q.graded.bosonic,Q.graded.complex_fermion,Q.graded.majorana))=Product(Q.lower.invariants));

# Re-evaluate the measured full order of the actual incoming lift, then solve
# its CF and top residual with the original comparison-homotopy machinery.
power:=AFSStackPower(ctx,incomingState,Q.incomingOrder);;
Assert(0,AFSStackSupportZero(ctx,2,2,power.a));
red:=AFSStackReduce(Q.model,power,true);;
Assert(0,red.status="computed" and ForAll(red.coordinates,x->x=0));
out:=AFSBackgroundQuotientExport(C,Q);;
LoadPackage("json");;serialized:=GapToJsonString(out);;
stream:=OutputTextFile(GAPInfo.SystemEnvironment.AFS_BQ_OUT,false);;
SetPrintFormattingStatus(stream,false);;PrintTo(stream,serialized,"\n");;CloseStream(stream);;
Print("BACKGROUND_QUOTIENT_COCHAIN_PASS sg=",number," incoming_order=",Q.incomingOrder,
  " before=",Q.preQuotientLower.invariants," after=",Q.lower.invariants,
  " graded=",Q.graded,"\n");
QUIT_GAP(0);
