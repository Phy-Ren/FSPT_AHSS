# Given the computed filtration, determine its sole possible extension using
# the known all-degree Majorana-to-complex-fermion product.
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=false;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
for AFS4_FILE in ["backend_mod2_contraction.g","backend_diagonal.g","class_coordinates.g","formula_data.g","formulas.g","formula_fast.g","classification.g","pip.g","dimension4_phase_p1_zero.g","dimension4_phase_p1_full.g","dimension4_phase_p2_zero.g","dimension4_phase_p2_full.g","dimension4_phase.g","dimension4.g"] do Read(Concatenation(AFS_ROOT,"/gap/",AFS4_FILE));od;
Read(AFS4_MODEL_FILE);;
AFS4_MODEL:=First(AFS4_TABLE_MODELS,m->m.id="Q8_w0_s0");;
AFS4_CONTEXT:=AFSD4Context(AFS4_MODEL);;
AFS4_RESULT:=AFSD4Classify(AFS4_CONTEXT);;
if AFS4_RESULT.layers<>rec(pip:=[],majorana:=[2],complex_fermion:=[2],bosonic:=[]) then Error("Q8 square audit filtration changed");fi;
AFS4_H3:=AFSCohomology(AFS4_CONTEXT,3,"F2");;AFS4_H4:=AFSCohomology(AFS4_CONTEXT,4,"F2");;
AFS4_B:=AFSCombination(AFS4_CONTEXT,3,"F2",AFS4_H3,AFS4_RESULT.witnesses.majoranaBasis[1]);;
AFS4_SQUARE:=AFSCup(2,3,AFS4_B,3,AFS4_B);;
AFS4_NATIVE_SQUARE:=AFSNative(AFS4_CONTEXT,4,"F2",AFS4_SQUARE);;
AFS4_CLASS:=AFS4_H4.coordinates(AFS4_NATIVE_SQUARE);;
if AFS4_CLASS=fail then Error("Majorana square is not closed");fi;
AFS4_QUOTIENT:=AFSQuotient(AFS4_H4.orders,AFS4_RESULT.maps.mcIncomingPrimary);;
AFS4_PROJECTED:=AFS4_QUOTIENT.project(AFS4_CLASS);;
if ForAny(AFS4_PROJECTED,x->x<>0) then Error("Q8 Majorana square is nonzero");fi;
AFS4_PROOF:=rec(model:="Q8_w0_s0",dimension:="4+1D",filtration:=AFS4_RESULT.layers,
  majoranaGeneratorCohomology:=AFS4_RESULT.witnesses.majoranaBasis[1],
  majoranaGeneratorNative:=AFSNative(AFS4_CONTEXT,3,"F2",AFS4_B),
  productFormula:="B cup_2 B = Sq1(B), because r=3 and s1=0",
  nativeSquare:=AFS4_NATIVE_SQUARE,squareH4Class:=AFS4_CLASS,
  cfIncomingPrimary:=AFS4_RESULT.maps.mcIncomingPrimary,projectedSquare:=AFS4_PROJECTED,
  fullGroupInvariants:=[2,2],relations:=["2C=0: its square is bosonic, and the final bosonic layer is zero", "2B=0: its CF square projects to zero and no bosonic class remains"],
  noUnknownHigherTwisterNeeded:=true,cpuMs:=Runtime());;
LoadPackage("json");;AFS4_STREAM:=OutputTextFile(AFS_OUT,false);;SetPrintFormattingStatus(AFS4_STREAM,false);;
PrintTo(AFS4_STREAM,GapToJsonString(AFS4_PROOF),"\n");;CloseStream(AFS4_STREAM);;
Print("AFS_Q8_FULL_GROUP_SQUARE_PASS [2,2]\n");;QUIT_GAP(0);
