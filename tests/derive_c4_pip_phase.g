OnBreak:=function() Where(25);QUIT_GAP(1);end;;
Read("runs/formula_audit/c4_pip_matrix.g");;
D:=TransposedMat(AFS_C4_D5);;
S:=SmithNormalFormIntegerMatTransforms(D);;
w:=AFS_C4_O5*S.coltrans;;
y:=List([1..81],i->0);;
for i in [1..243] do
 if i<=81 and S.normal[i][i]<>0 then y[i]:=w[i]/S.normal[i][i];
 else Assert(0,IsInt(w[i]));fi;
od;
nu:=y*S.rowtrans;;
Assert(0,ForAll(nu*D-AFS_C4_O5,IsInt));
LoadPackage("json");;
out:=rec(phase4:=List(nu,x->[NumeratorRat(x),DenominatorRat(x)]),
 phasePrimitiveVerified:=true,normalizedFiveTuples:=243,CFDefiningCochain:=AFS_C4_C3,
 construction:="exact-finite-C4-universal-flat-tower-for-pullback");;
stream:=OutputTextFile("runs/formula_audit/c4_pip_phase.json",false);;
SetPrintFormattingStatus(stream,false);;PrintTo(stream,GapToJsonString(out),"\n");;CloseStream(stream);;
Print("C4_PIP_PHASE_PRIMITIVE_PASS ",Set(List(nu,DenominatorRat)),"\n");
QUIT_GAP(0);
