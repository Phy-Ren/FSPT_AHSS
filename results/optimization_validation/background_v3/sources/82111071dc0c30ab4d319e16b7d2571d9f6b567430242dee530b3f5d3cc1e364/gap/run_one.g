if not IsBound(AFS_CRYSTALLINE_SPIN) then AFS_CRYSTALLINE_SPIN:="half";fi;
if not AFS_CRYSTALLINE_SPIN in ["half","spinless"] then Error("unknown crystalline spin convention");fi;
if not IsBound(AFS_USE_MOD2_BAR) then AFS_USE_MOD2_BAR:=false;fi;
if not IsBound(AFS_USE_CLOSED_CF_OBSTRUCTION) then AFS_USE_CLOSED_CF_OBSTRUCTION:=true;fi;
if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT"; fi;
if not IsBound(AFS_SG) then Error("AFS_SG required"); fi;
if not IsBound(AFS_OUT) then Error("AFS_OUT required"); fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));
if not IsBound(AFS_USE_MOD2_CONTRACTION) then AFS_USE_MOD2_CONTRACTION:=true; fi;
Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));
if IsBound(AFS_USE_MOD2_BAR) and AFS_USE_MOD2_BAR=true then
  Read(Concatenation(AFS_ROOT,"/gap/backend_bar_mod2.g"));
fi;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));
Print("AFS_NATIVE_CONTRACTION_MODE mod2=",AFSDiagonalContract=AFSContractCellMod2,"\n");
Read(Concatenation(AFS_ROOT,"/gap/class_coordinates.g"));
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));
Read(Concatenation(AFS_ROOT,"/gap/pip_o5_program.g"));
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));
Read(Concatenation(AFS_ROOT,"/gap/formula_fast.g"));
Read(Concatenation(AFS_ROOT,"/gap/pip_o5_sign.g"));
if not IsBound(AFSUseGeneralPipO5) then AFSUseGeneralPipO5:=true; fi;
Read(Concatenation(AFS_ROOT,"/gap/pip_o5_general.g"));
if IsBound(AFS_USE_CLOSED_CF_OBSTRUCTION) and AFS_USE_CLOSED_CF_OBSTRUCTION=true then
  Read(Concatenation(AFS_ROOT,"/gap/backend_half_phase.g"));
  Read(Concatenation(AFS_ROOT,"/gap/stacking_closed_cf.g"));
fi;
Read(Concatenation(AFS_ROOT,"/gap/classification.g"));
Read(Concatenation(AFS_ROOT,"/gap/pip.g"));
AFS_CONTEXT:=AFSBackend(AFS_SG);;
AFS_CONTEXT.omega2:=AFSZero;;
AFS_CONTEXT.crystallineSpin:=AFS_CRYSTALLINE_SPIN;;
if AFS_CRYSTALLINE_SPIN="spinless" then
  Read(Concatenation(AFS_ROOT,"/gap/crystalline_background.g"));
  Read(Concatenation(AFS_ROOT,"/gap/background_operations.g"));
  Read(Concatenation(AFS_ROOT,"/gap/pip_o5_background.g"));
  AFSInstallCrystallineBackground(AFS_CONTEXT);
  AFSReduceCrystallineBackground(AFS_CONTEXT);
fi;
AFS_RESULT:=AFSClassify(AFS_CONTEXT);;
AFS_RESULT.summary.crystalline_spin:=AFS_CRYSTALLINE_SPIN;;
if AFS_CRYSTALLINE_SPIN="spinless" then
  AFS_RESULT.summary.convention:="physical-spinless-det-sign-Pin-minus";
  AFS_RESULT.summary.crystalline_background:=AFSCrystallineBackgroundExport(AFS_CONTEXT);
fi;
AFS_RESULT.summary.classification_status:=AFS_RESULT.status;;
AFS_RESULT.summary.formula_convention:="normalized-pip-aw-edge-transport-v2";;
AFS_RESULT.summary.generic_pip_compiled:=AFSUseGeneralPipO5;;
AFS_RESULT.summary.binary_bar_mod2:=IsBound(AFS_USE_MOD2_BAR) and AFS_USE_MOD2_BAR=true;;
AFS_RESULT.summary.closed_cf_obstruction:=IsBound(AFS_USE_CLOSED_CF_OBSTRUCTION) and AFS_USE_CLOSED_CF_OBSTRUCTION=true;;
AFS_RESULT.summary.native_mod2_contraction:=AFSDiagonalContract=AFSContractCellMod2;;
AFS_RESULT.summary.native_mod2_cache_degrees:=0;;
if IsBound(AFS_CONTEXT.bar.mod2HCache) then
  AFS_RESULT.summary.native_mod2_cache_degrees:=Length(AFS_CONTEXT.bar.mod2HCache);;
fi;
if AFS_CRYSTALLINE_SPIN="spinless" or AFS_RESULT.summary.pip.free_rank>0 or (IsBound(AFS_MODE) and AFS_MODE="full") then
  Read(Concatenation(AFS_ROOT,"/gap/stacking.g"));
fi;
if AFS_RESULT.summary.pip.free_rank>0 then
  Read(Concatenation(AFS_ROOT,"/gap/pip_free.g"));
  if AFS_CRYSTALLINE_SPIN="spinless" then Read(Concatenation(AFS_ROOT,"/gap/background_free.g"));fi;
  AFS_FREE_START:=Runtime();;
  AFS_FREE_RESULT:=AFSFreePipFromClassification(AFS_RESULT);;
  AFS_RESULT.summary.pip.free_lattice:=AFSFreePipExport(AFS_RESULT,AFS_FREE_RESULT);;
  AFS_RESULT.summary.free_pip_cpu_ms:=Runtime()-AFS_FREE_START;;
  AFSStage(AFS_CONTEXT,"free_pip_classification_end");
  AFS_RESULT.summary.cpu_ms:=Runtime();;
fi;
# The H0 incoming quotient requires the actual lower stacking group. It is
# part of classification in this convention, so the checkpoint follows it.
AFS_BACKGROUND_ACTIVE:=AFS_CRYSTALLINE_SPIN="spinless" and AFS_CONTEXT.omega2<>AFSZero;;
if AFS_BACKGROUND_ACTIVE then
  Read(Concatenation(AFS_ROOT,"/gap/pip_incoming_background.g"));
  Read(Concatenation(AFS_ROOT,"/gap/background_quotient.g"));
  Read(Concatenation(AFS_ROOT,"/gap/background_stacking.g"));
  AFS_STACK_RESULT:=AFSBackgroundFullStacking(AFS_RESULT);;
  if not IsBound(AFS_STACK_RESULT.lower) or
      (AFS_CONTEXT.s=AFSZero and not IsBound(AFS_RESULT.backgroundQuotient)) then
    Error("background lower group or H0 quotient incomplete");
  fi;
  AFS_RESULT.summary.classification_status:=AFS_RESULT.status;
  AFS_RESULT.summary.cpu_ms:=Runtime();
fi;
if IsBound(AFS_CLASS_OUT) then
  LoadPackage("json");;
  AFS_CHECKPOINT:=ShallowCopy(AFS_RESULT.summary);;
  AFS_CHECKPOINT.source_id:=AFS_SOURCE_ID;;
  AFS_CHECKPOINT.source_snapshot:=AFS_ROOT;;
  AFS_CHECKPOINT.checkpoint_stage:="classification-complete-before-stacking";;
  if AFS_BACKGROUND_ACTIVE then
    AFS_CHECKPOINT.checkpoint_stage:="classification-complete-including-lower-stacking-and-H0-incoming";
  fi;
  AFS_CHECKPOINT.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
  AFS_CLASS_STREAM:=OutputTextFile(AFS_CLASS_OUT,false);;
  SetPrintFormattingStatus(AFS_CLASS_STREAM,false);
  PrintTo(AFS_CLASS_STREAM,GapToJsonString(AFS_CHECKPOINT),"\n");
  CloseStream(AFS_CLASS_STREAM);
fi;
if IsBound(AFS_MODE) and AFS_MODE="full" then
  if AFS_BACKGROUND_ACTIVE then
    AFS_RESULT.summary.stacking:=AFSBackgroundStackingExport(AFS_RESULT,AFS_STACK_RESULT);;
  else
  Read(Concatenation(AFS_ROOT,"/gap/pip_coordinate_data.g"));
  Read(Concatenation(AFS_ROOT,"/gap/pip_coordinates.g"));
  Read(Concatenation(AFS_ROOT,"/gap/pip_diagonal_data.g"));
  Read(Concatenation(AFS_ROOT,"/gap/pip_c4_data.g"));
  Read(Concatenation(AFS_ROOT,"/gap/pip_stacking.g"));
  AFS_STACK_RESULT:=AFSExplicitPipStacking(AFS_RESULT);;
  AFS_RESULT.summary.stacking:=AFSExplicitPipExport(AFS_RESULT,AFS_STACK_RESULT);;
  fi;
  AFS_RESULT.summary.stacking.physicalConvention:=AFS_RESULT.summary.convention;;
  if AFS_CRYSTALLINE_SPIN="spinless" then AFS_RESULT.summary.stacking.scope:="3+1D-crystalline-spinless-affine-stacking";fi;
  if AFS_RESULT.summary.stacking.status<>"computed" then
    AFS_RESULT.summary.status:="unresolved";;
  fi;
fi;
AFS_RESULT.summary.total_cpu_ms:=Runtime();;
AFS_RESULT.summary.generic_pip_compiled_calls:=AFSPipO5GeneralCalls;;
if IsBound(AFS_CONTEXT.bar.mod2HCache) then
  AFS_RESULT.summary.native_mod2_cache_degrees:=Length(AFS_CONTEXT.bar.mod2HCache);;
fi;
AFS_RESULT.summary.stage_timings:=AFS_CONTEXT.stageTimings;;
if IsBound(AFS_CONTEXT.R!.afsTimings) then
  AFS_RESULT.summary.resolution_timings:=AFS_CONTEXT.R!.afsTimings;;
fi;
AFS_RESULT.summary.libraries:=rec(GAP:=GAPInfo.Version,HAP:=PackageInfo("hap")[1].Version,CrystCat:=PackageInfo("crystcat")[1].Version,Polycyclic:=PackageInfo("polycyclic")[1].Version);;
AFS_RESULT.summary.sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset);;
if AFS_RESULT.summary.sptset_loaded then Error("SptSet must not be loaded by the independent computation"); fi;
LoadPackage("json");;
AFS_STREAM:=OutputTextFile(AFS_OUT,false);;
SetPrintFormattingStatus(AFS_STREAM,false);
PrintTo(AFS_STREAM,GapToJsonString(AFS_RESULT.summary),"\n");
CloseStream(AFS_STREAM);
Print("AFS_RESULT_WRITTEN ",AFS_SG," ",AFS_RESULT.status,"\n");
QUIT_GAP(0);
