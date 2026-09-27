# One finite point group, one process, classification followed by stacking.
# This deliberately shares mathematical operations with run_one.g while
# selecting an actual finite resolution with no translation subgroup.
if not IsBound(AFS_ROOT) or not IsBound(AFS_PG) or not IsBound(AFS_OUT) or
    not IsBound(AFS_CLASS_OUT) or not IsBound(AFS_SOURCE_ID) then
  Error("finite point-group driver parameters missing");
fi;
if not IsBound(AFS_CRYSTALLINE_SPIN) then AFS_CRYSTALLINE_SPIN:="half";fi;
if not AFS_CRYSTALLINE_SPIN in ["half","spinless"] then Error("unknown physical convention");fi;
if not IsBound(AFS_USE_MOD2_BAR) then AFS_USE_MOD2_BAR:=false;fi;
if not IsBound(AFS_USE_MOD2_CONTRACTION) then AFS_USE_MOD2_CONTRACTION:=true;fi;
if not IsBound(AFS_USE_CLOSED_CF_OBSTRUCTION) then AFS_USE_CLOSED_CF_OBSTRUCTION:=true;fi;
if not IsBound(AFSUseGeneralPipO5) then AFSUseGeneralPipO5:=true;fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));
Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));
if AFS_USE_MOD2_BAR then Read(Concatenation(AFS_ROOT,"/gap/backend_bar_mod2.g"));fi;
for AFS_FILE in ["backend_diagonal.g","class_coordinates.g","formula_data.g",
    "pip_o5_program.g","formulas.g","formula_fast.g","pip_o5_sign.g",
    "pip_o5_general.g","classification.g","pip.g","point_group_backend.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",AFS_FILE));
od;
if AFS_USE_CLOSED_CF_OBSTRUCTION then
  Read(Concatenation(AFS_ROOT,"/gap/backend_half_phase.g"));
  Read(Concatenation(AFS_ROOT,"/gap/stacking_closed_cf.g"));
fi;
AFS_CONTEXT:=AFSPointGroupBackend(AFS_PG);;
AFS_CONTEXT.crystallineSpin:=AFS_CRYSTALLINE_SPIN;;
if AFS_CRYSTALLINE_SPIN="spinless" then
  for AFS_FILE in ["crystalline_background.g","background_native_cup.g",
      "background_operations.g","pip_o5_background.g","pip_o5_background_even.g",
      "pip_o5_background_sign.g"] do Read(Concatenation(AFS_ROOT,"/gap/",AFS_FILE));od;
  AFS_CONTEXT.useBackgroundNativeCup:=true;;
  AFSInstallPointGroupBackground(AFS_CONTEXT);;
  AFSReduceCrystallineBackground(AFS_CONTEXT);;
fi;
AFS_RESULT:=AFSClassify(AFS_CONTEXT);;
if AFS_RESULT.summary.pip.free_rank<>0 then Error("finite point group has a spurious free p+ip rank");fi;
Unbind(AFS_RESULT.summary.space_group);;
AFS_RESULT.summary.point_group_index:=AFS_PG;;
AFS_RESULT.summary.crystalline_spin:=AFS_CRYSTALLINE_SPIN;;
AFS_RESULT.summary.scope:="3+1D-finite-crystallographic-point-group-associated-graded";;
AFS_RESULT.summary.point_group:=AFSPointGroupExport(AFS_CONTEXT);;
if AFS_CRYSTALLINE_SPIN="spinless" then
  AFS_RESULT.summary.convention:="physical-spinless-det-sign-Pin-minus";
  AFS_RESULT.summary.crystalline_background:=AFSCrystallineBackgroundExport(AFS_CONTEXT);
  AFS_RESULT.summary.crystalline_background.cohomologyGroupScope:="actual finite matrix point group; affineCohomologyCoordinates is a legacy field name for its native H2 coordinates";
  AFS_RESULT.summary.background_projected_native_cup:=AFS_CONTEXT.omega2<>AFSZero;
fi;
AFS_RESULT.summary.classification_status:=AFS_RESULT.status;;
AFS_RESULT.summary.formula_convention:="normalized-pip-aw-edge-transport-v2";;
AFS_RESULT.summary.generic_pip_compiled:=AFSUseGeneralPipO5;;
AFS_RESULT.summary.binary_bar_mod2:=AFS_USE_MOD2_BAR;;
AFS_RESULT.summary.closed_cf_obstruction:=AFS_USE_CLOSED_CF_OBSTRUCTION;;
AFS_RESULT.summary.native_mod2_contraction:=AFSDiagonalContract=AFSContractCellMod2;;
AFS_RESULT.summary.native_mod2_cache_degrees:=0;;
Read(Concatenation(AFS_ROOT,"/gap/stacking.g"));
AFS_BACKGROUND_ACTIVE:=AFS_CRYSTALLINE_SPIN="spinless" and AFS_CONTEXT.omega2<>AFSZero;;
if AFS_BACKGROUND_ACTIVE then
  for AFS_FILE in ["pip_incoming_background.g","background_quotient.g","background_stacking.g"] do
    Read(Concatenation(AFS_ROOT,"/gap/",AFS_FILE));
  od;
  AFS_STACK_RESULT:=AFSBackgroundFullStacking(AFS_RESULT);;
  if not IsBound(AFS_STACK_RESULT.lower) or
      (AFS_CONTEXT.s=AFSZero and not IsBound(AFS_RESULT.backgroundQuotient)) then
    Error("finite background lower group/H0 incoming quotient incomplete");
  fi;
  AFS_RESULT.summary.classification_status:=AFS_RESULT.status;
  AFS_RESULT.summary.cpu_ms:=Runtime();
fi;
LoadPackage("json");;
AFS_CHECKPOINT:=ShallowCopy(AFS_RESULT.summary);;
AFS_CHECKPOINT.source_id:=AFS_SOURCE_ID;;
AFS_CHECKPOINT.source_snapshot:=AFS_ROOT;;
AFS_CHECKPOINT.point_group:=AFSPointGroupExport(AFS_CONTEXT);;
AFS_CHECKPOINT.checkpoint_stage:="classification-complete-before-stacking";;
if AFS_BACKGROUND_ACTIVE then
  AFS_CHECKPOINT.checkpoint_stage:="classification-complete-including-background-stacking-and-H0-incoming";
fi;
AFS_CHECKPOINT.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
AFS_CLASS_STREAM:=OutputTextFile(AFS_CLASS_OUT,false);;
SetPrintFormattingStatus(AFS_CLASS_STREAM,false);
PrintTo(AFS_CLASS_STREAM,GapToJsonString(AFS_CHECKPOINT),"\n");
CloseStream(AFS_CLASS_STREAM);
if AFS_BACKGROUND_ACTIVE then
  AFS_RESULT.summary.stacking:=AFSBackgroundStackingExport(AFS_RESULT,AFS_STACK_RESULT);;
else
  for AFS_FILE in ["pip_coordinate_data.g","pip_coordinates.g","pip_diagonal_data.g",
      "pip_c4_data.g","pip_stacking.g"] do Read(Concatenation(AFS_ROOT,"/gap/",AFS_FILE));od;
  AFS_STACK_RESULT:=AFSExplicitPipStacking(AFS_RESULT);;
  AFS_RESULT.summary.stacking:=AFSExplicitPipExport(AFS_RESULT,AFS_STACK_RESULT);;
fi;
AFS_RESULT.summary.stacking.physicalConvention:=AFS_RESULT.summary.convention;;
AFS_RESULT.summary.stacking.scope:="3+1D-finite-crystallographic-point-group-stacking";;
AFSPointGroupExportLabels(AFS_RESULT.summary.stacking);;
if AFS_RESULT.summary.stacking.status<>"computed" then AFS_RESULT.summary.status:="unresolved";fi;
AFS_RESULT.summary.total_cpu_ms:=Runtime();;
AFS_RESULT.summary.generic_pip_compiled_calls:=AFSPipO5GeneralCalls;;
if AFS_CRYSTALLINE_SPIN="spinless" then
  AFS_RESULT.summary.background_pip_compiled_calls:=AFSPipO5BackgroundCalls;
  AFS_RESULT.summary.background_even_pip_compiled_calls:=AFSPipO5BackgroundEvenCalls;
  AFS_RESULT.summary.background_sign_pip_compiled_calls:=AFSPipO5BackgroundSignCalls;
fi;
if IsBound(AFS_CONTEXT.bar.mod2HCache) then
  AFS_RESULT.summary.native_mod2_cache_degrees:=Length(AFS_CONTEXT.bar.mod2HCache);
fi;
AFS_RESULT.summary.stage_timings:=AFS_CONTEXT.stageTimings;;
AFS_RESULT.summary.resolution_timings:=AFS_CONTEXT.R!.afsTimings;;
AFS_RESULT.summary.point_group:=AFSPointGroupExport(AFS_CONTEXT);;
AFS_RESULT.summary.libraries:=rec(GAP:=GAPInfo.Version,HAP:=PackageInfo("hap")[1].Version,
  CrystCat:=PackageInfo("crystcat")[1].Version,Polycyclic:=PackageInfo("polycyclic")[1].Version);;
AFS_RESULT.summary.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
if AFS_RESULT.summary.sptset_loaded then Error("SptSet must not be loaded");fi;
AFS_STREAM:=OutputTextFile(AFS_OUT,false);;
SetPrintFormattingStatus(AFS_STREAM,false);
PrintTo(AFS_STREAM,GapToJsonString(AFS_RESULT.summary),"\n");
CloseStream(AFS_STREAM);
Print("AFS_POINT_GROUP_WRITTEN ",AFS_PG," ",AFS_CRYSTALLINE_SPIN," ",AFS_RESULT.summary.status,"\n");
QUIT_GAP(0);
