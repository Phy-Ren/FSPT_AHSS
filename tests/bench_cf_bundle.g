if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=true;;
for file in ["backend.g","backend_mod2_contraction.g","backend_bar_mod2.g",
  "backend_diagonal.g","backend_half_phase.g","class_coordinates.g",
  "formula_data.g","pip_o5_program.g","formulas.g","formula_fast.g",
  "pip_o5_sign.g","pip_o5_general.g","classification.g","pip.g",
  "stacking_closed_cf.g"] do Read(Concatenation(AFS_ROOT,"/gap/",file));od;
if not IsBound(AFS_SG) then AFS_SG:=219;fi;
ctx:=AFSBackend(AFS_SG);;C:=AFSClassify(ctx);;
Print("CF_BUNDLE_CLASS_COMPLETE sg=",AFS_SG," CF=",Length(C.cfFinalBasis),
  " cpu_ms=",Runtime()," native_mod2=",AFSDiagonalContract=AFSContractCellMod2,"\n");
if Length(C.cfFinalBasis)=0 then Error("bundle benchmark requires a surviving CF generator");fi;
ctx.halfPhaseProgress:=function(k,i,n,allTerms,oddTerms,ms)
  if i mod 10=0 or i=n then Print("CF_BUNDLE_PROGRESS sg=",AFS_SG," cell=",i,"/",n,
    " total_terms=",allTerms," odd_terms=",oddTerms," cpu_ms=",ms,"\n");fi;
end;;
for index in [1..Minimum(2,Length(C.cfFinalBasis))] do
  cf:=AFSCombination(ctx,3,"F2",C.H3,C.cfFinalBasis[index]);;
  phase:=AFSClosedCFObstructionLazy(cf);;t:=Runtime();;
  lift:=AFSSolveHalfPhaseData(ctx,5,phase);;
  if lift=fail then Error("certified surviving CF generator has no phase lift");fi;
  Print("CF_BUNDLE_LIFT_COMPLETE sg=",AFS_SG," index=",index," cpu_ms=",Runtime()-t,"\n");
  Print("CF_BUNDLE_NATIVE_OBSTRUCTION ",lift.nativeObstruction,"\n");
  Print("CF_BUNDLE_NATIVE_PRIMITIVE ",lift.nativePrimitive,"\n");
  # The exact integral homotopy correction is retained. Evaluate a few actual
  # bar values after printing the creation timing, so later relation costs
  # cannot be confused with the native lift-construction cost.
  tuples:=[];;
  for cell in [1..Dimension(ctx.R)(4)] do
    for term in AFSChainToBar(ctx.bar,4,cell) do
      Add(tuples,term[3]);if Length(tuples)=4 then break;fi;
    od;
    if Length(tuples)=4 then break;fi;
  od;
  Print("CF_BUNDLE_PHASE_SAMPLES ",List(tuples,xs->CallFuncList(lift.primitive,xs)),"\n");
od;
Print("AFS_CF_BUNDLE_NEW_ONLY_COMPLETE sg=",AFS_SG,"\n");QUIT_GAP(0);
