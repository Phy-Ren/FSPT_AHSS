# Complete finite classification and stacking share the same context and lifts.
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=false;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
for AFSFULL_FILE in ["backend_mod2_contraction.g","backend_diagonal.g","class_coordinates.g",
  "formula_data.g","formulas.g","formula_fast.g","classification.g","dimension4.g",
  "stacking.g","full_formula_transport.g","full_stacking.g","finite_full.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",AFSFULL_FILE));
od;
Read(AFS4_MODEL_FILE);;
AFSFULL_MODEL:=First(AFS4_TABLE_MODELS,m->m.id=AFS4_MODEL_ID);;
if AFSFULL_MODEL=fail then Error("unknown complete finite model");fi;
AFSFULL_CONTEXT:=AFSD4Context(AFSFULL_MODEL);;
AFSFULL_CLASSIFICATION:=AFSFullClassify(AFSFULL_CONTEXT,AFS_FULL_DIMENSION);;
Read(Concatenation(AFS_ROOT,"/gap/full_audit_configuration.g"));;
AFSFULL_STACKING:=AFSFullStackingWithValidatedAuditSelectors(AFSFULL_CLASSIFICATION);;
if IsBoundGlobal("AFS_FULL_BAR_AUDIT_SAMPLES") then
  Read(Concatenation(AFS_ROOT,"/gap/full_bar_audit.g"));
  AFSFULL_STACKING.seededBarAudit:=AFSFullSeededBarAudit(AFSFULL_CLASSIFICATION,
    AFS_FULL_BAR_AUDIT_GENERATORS,AFS_FULL_BAR_AUDIT_SAMPLES,AFS_FULL_BAR_AUDIT_SEED);
fi;
if IsBoundGlobal("AFS_FULL_GAUGE_AUDIT_LAYERS") then
  AFSFULL_STACKING.gaugeNullityAudit:=AFSFullGaugeNullityAudit(AFSFULL_CLASSIFICATION,
    AFSFULL_STACKING,ValueGlobal("AFS_FULL_GAUGE_AUDIT_LAYERS"));
fi;
AFSFULL_RESULT:=AFSFullExport(AFSFULL_CLASSIFICATION,AFSFULL_STACKING);;
AFSFULL_RESULT.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
if AFSFULL_RESULT.sptset_loaded then Error("SptSet loaded unexpectedly");fi;
AFSFULL_RESULT.inputModel:=AFSFULL_MODEL;;
LoadPackage("json");;
AFSFULL_STREAM:=OutputTextFile(AFS_OUT,false);;SetPrintFormattingStatus(AFSFULL_STREAM,false);;
PrintTo(AFSFULL_STREAM,GapToJsonString(AFSFULL_RESULT),"\n");;CloseStream(AFSFULL_STREAM);;
AFSFullFormulaClose(AFSFULL_CONTEXT);;
Print("AFS_FULL_FINITE_COMPLETE ",AFS4_MODEL_ID," dimension=",AFS_FULL_DIMENSION,
  " invariants=",AFSFULL_RESULT.invariants,"\n");;
QUIT_GAP(0);
