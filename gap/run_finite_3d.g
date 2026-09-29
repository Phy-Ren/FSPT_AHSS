# Finite internal symmetry: classification followed by complete known lower stacking.
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=false;;AFS_USE_CLOSED_CF_OBSTRUCTION:=true;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
for AFSF_FILE in ["backend_mod2_contraction.g","backend_diagonal.g","class_coordinates.g","formula_data.g","pip_o5_program.g","formulas.g","formula_fast.g","classification.g","pip.g","background_native_cup.g","background_operations.g","backend_half_phase.g","stacking_closed_cf.g","dimension4_phase_p1_zero.g","dimension4_phase_p1_full.g","dimension4_phase.g","dimension4.g","finite_input.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",AFSF_FILE));
od;
AFSPipO5:=function(c,inputs)return AFSD4Phase(c,1,inputs.n,inputs.b,inputs.c);end;;
Read(AFS4_MODEL_FILE);;
AFSF_MODEL:=First(AFS4_TABLE_MODELS,m->m.id=AFS4_MODEL_ID);;
if AFSF_MODEL=fail then Error("unknown finite model");fi;
AFSF_CONTEXT:=AFSD4Context(AFSF_MODEL);;AFSF_CONTEXT.useBackgroundNativeCup:=true;;
AFSF_INPUT:=AFSPrepareFiniteInput(AFSF_CONTEXT);;
AFSF_RESULT:=AFSClassify(AFSF_CONTEXT);;
for AFSF_FILE in ["stacking.g","pip_incoming_background.g","background_quotient.g","background_stacking.g"] do Read(Concatenation(AFS_ROOT,"/gap/",AFSF_FILE));od;
if AFSF_CONTEXT.omega2=AFSZero then
  AFSF_STACK:=AFSFullStacking(AFSF_RESULT);;
  AFSF_RESULT.summary.stacking:=AFSStackExport(AFSF_RESULT,AFSF_STACK);;
else
  AFSF_STACK:=AFSBackgroundFullStacking(AFSF_RESULT);;
  AFSF_RESULT.summary.stacking:=AFSBackgroundStackingExport(AFSF_RESULT,AFSF_STACK);;
fi;
AFSF_RESULT.summary.publicPipExtension:=AFSFiniteUpperExtension(AFSF_RESULT,AFSF_STACK);;
AFSF_RESULT.summary.finiteInputAudit:=AFSF_INPUT;;
AFSF_RESULT.summary.model:=AFS4_MODEL_ID;;
AFSF_RESULT.summary.total_cpu_ms:=Runtime();;
AFSF_RESULT.summary.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
if AFSF_RESULT.summary.sptset_loaded then Error("SptSet loaded unexpectedly");fi;
LoadPackage("json");;
AFSF_STREAM:=OutputTextFile(AFS_OUT,false);;SetPrintFormattingStatus(AFSF_STREAM,false);;
PrintTo(AFSF_STREAM,GapToJsonString(AFSF_RESULT.summary),"\n");;CloseStream(AFSF_STREAM);;
Print("AFS_FINITE_3D_COMPLETE ",AFS4_MODEL_ID,"\n");;
QUIT_GAP(0);
