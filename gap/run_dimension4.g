# One finite symmetry model; write associated-graded output only after all maps.
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
if not IsBound(AFS_ROOT) or not IsBound(AFS4_MODEL_FILE) or not IsBound(AFS4_MODEL_ID) or not IsBound(AFS_OUT) then Error("dimension-four runner arguments missing");fi;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=false;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
for AFS4_FILE in ["backend_mod2_contraction.g","backend_diagonal.g","class_coordinates.g","formula_data.g","formulas.g","formula_fast.g","classification.g","pip.g","dimension4_phase_p1_zero.g","dimension4_phase_p1_full.g","dimension4_phase_p2_zero.g","dimension4_phase_p2_full.g","dimension4_phase.g","dimension4.g"] do
  if IsExistingFile(Concatenation(AFS_ROOT,"/gap/",AFS4_FILE)) then Read(Concatenation(AFS_ROOT,"/gap/",AFS4_FILE));fi;
od;
Read(AFS4_MODEL_FILE);;
AFS4_MODEL:=First(AFS4_TABLE_MODELS,m->m.id=AFS4_MODEL_ID);;
if AFS4_MODEL=fail then Error("unknown finite model");fi;
AFS4_CONTEXT:=AFSD4Context(AFS4_MODEL);;
AFS4_RESULT:=AFSD4Classify(AFS4_CONTEXT);;
AFS4_RESULT.inputModel:=AFS4_MODEL;;
if IsBound(AFS_SOURCE_ID) then AFS4_RESULT.source_id:=AFS_SOURCE_ID;fi;
LoadPackage("json");;
AFS4_STREAM:=OutputTextFile(AFS_OUT,false);;SetPrintFormattingStatus(AFS4_STREAM,false);;
PrintTo(AFS4_STREAM,GapToJsonString(AFS4_RESULT),"\n");;CloseStream(AFS4_STREAM);;
Print("AFS_DIMENSION4_COMPLETE ",AFS4_MODEL_ID," ",AFS4_RESULT.layers,"\n");;
QUIT_GAP(0);
