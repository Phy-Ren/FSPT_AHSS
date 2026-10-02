# Full matched-coordinate pipeline for the actual finite matrix point group.
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=false;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
for AFSFULL_FILE in ["backend_mod2_contraction.g","backend_diagonal.g","class_coordinates.g",
  "formula_data.g","formulas.g","formula_fast.g","classification.g","dimension4.g",
  "stacking.g","full_formula_transport.g","full_stacking.g","finite_full.g",
  "point_group_backend.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",AFSFULL_FILE));
od;
AFSFULL_CONTEXT:=AFSPointGroupBackend(AFS_PG);;
AFSFULL_CONTEXT.crystallineSpin:=AFS_CRYSTALLINE_SPIN;;
if AFS_CRYSTALLINE_SPIN="spinless" then
  Read(Concatenation(AFS_ROOT,"/gap/crystalline_background.g"));;
  Read(Concatenation(AFS_ROOT,"/gap/background_operations.g"));;
  AFSInstallPointGroupBackground(AFSFULL_CONTEXT);;
  AFSReducePointGroupBackground(AFSFULL_CONTEXT);;
fi;
AFSFULL_CLASSIFICATION:=AFSFullClassify(AFSFULL_CONTEXT,3);;
AFSFULL_STACKING:=AFSFullStackingClassification(AFSFULL_CLASSIFICATION);;
# The trivial point group can complete without any simplex request.
AFSFullFormulaOpen(AFSFULL_CONTEXT);;
AFSFULL_RESULT:=AFSFullExport(AFSFULL_CLASSIFICATION,AFSFULL_STACKING);;
AFSFULL_RESULT.schema:="fspt-complete-point-group-v1";;
AFSFULL_RESULT.model:=Concatenation("PG",String(AFS_PG));;
AFSFULL_RESULT.point_group_index:=AFS_PG;;
AFSFULL_RESULT.point_group:=AFSPointGroupExport(AFSFULL_CONTEXT);;
AFSFULL_RESULT.crystalline_spin:=AFS_CRYSTALLINE_SPIN;;
AFSFULL_RESULT.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
if AFSFULL_RESULT.sptset_loaded then Error("SptSet loaded unexpectedly");fi;
LoadPackage("json");;
AFSFULL_STREAM:=OutputTextFile(AFS_OUT,false);;SetPrintFormattingStatus(AFSFULL_STREAM,false);;
PrintTo(AFSFULL_STREAM,GapToJsonString(AFSFULL_RESULT),"\n");;CloseStream(AFSFULL_STREAM);;
AFSFullFormulaClose(AFSFULL_CONTEXT);;
Print("AFS_FULL_POINT_GROUP_COMPLETE ",AFS_PG," spin=",AFS_CRYSTALLINE_SPIN,
  " invariants=",AFSFULL_RESULT.invariants,"\n");;
QUIT_GAP(0);
