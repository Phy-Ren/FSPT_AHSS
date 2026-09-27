# Optional native cup0 control. Run only on an allocated compute node.
# AFS_BIG=true limits the expensive full-tensor comparison to degree (2,3).
if not IsBound(AFS_ROOT) then AFS_ROOT:=".";fi;
if not IsBound(AFS_SG) then AFS_SG:=3;fi;
if not IsBound(AFS_BIG) then AFS_BIG:=false;fi;
if not IsBound(AFS_OUT) then AFS_OUT:="background_native_cup.json";fi;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
AFS_USE_MOD2_CONTRACTION:=true;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));;
Read(Concatenation(AFS_ROOT,"/gap/crystalline_background.g"));;
Read(Concatenation(AFS_ROOT,"/gap/background_native_cup.g"));;

ctx:=AFSBackend(AFS_SG);;
AFSInstallCrystallineBackground(ctx);;
if AFS_BIG then degreePairs:=[[2,3]];
else degreePairs:=[[0,0],[0,2],[2,0],[1,1],[1,3],[2,2],[2,3],[3,2]];fi;
records:=[];;
for pq in degreePairs do
  p:=pq[1];q:=pq[2];;
  a:=List([1..Dimension(ctx.R)(p)],i->(3*i+1) mod 7-3);;
  b:=List([1..Dimension(ctx.R)(q)],i->(5*i+2) mod 11-5);;
  start:=Runtime();;
  actual:=AFSBackgroundNativeCup0(ctx,p,a,q,b);;
  shortCPU:=Runtime()-start;;
  Print("BACKGROUND_CUP0_PROJECTED sg=",AFS_SG," degrees=",pq,
    " cpu_ms=",shortCPU,"\n");
  start:=Runtime();;
  expected:=AFSNativeCupIFull(ctx,p,q,0,a,b);;
  fullCPU:=Runtime()-start;;
  Assert(0,actual=expected);
  key:=Concatenation("0_",String(p),"_",String(q));;
  pairsNew:=AFSBackgroundNativeCup0Forms(ctx,p,q);;
  pairsOld:=ctx.cupPairCache.(key);;
  Assert(0,Length(pairsNew)=Length(pairsOld));
  for i in [1..Length(pairsNew)] do
    Assert(0,Set(pairsNew[i])=Set(pairsOld[i]));
  od;
  # Equality of the complete pair form proves equality for EVERY pair of
  # native cochains, including nonclosed cochains, at this degree.
  Add(records,rec(degrees:=pq,projected_cpu_ms:=shortCPU,full_cpu_ms:=fullCPU,
    native_cells:=Length(actual),pair_count:=Sum(List(pairsNew,Length)),
    complete_bilinear_forms_equal:=true,actual_vectors_equal:=true));
  Print("BACKGROUND_CUP0_FULL_EQUAL sg=",AFS_SG," degrees=",pq,
    " cpu_ms=",fullCPU,"\n");
od;

# Exact background cup products, with cohomology comparison against the
# separately constructed bar cup. Sign acts trivially on binary cochains,
# but is RETAINED by the U1_s target and its signed integral differential.
wNative:=AFSNative(ctx,2,"F2",ctx.omega2);;
cohomologyChecks:=[];;
for q in [2,3] do
  if AFS_BIG and q<>3 then continue;fi;
  H:=AFSCohomology(ctx,q,"F2");;
  HF:=AFSCohomology(ctx,q+2,"F2");;
  HU:=AFSCohomology(ctx,q+2,"U1s");;
  if AFS_BIG then selected:=[1..Minimum(1,Length(H.generators))];
  else selected:=[1..Length(H.generators)];fi;
  for i in selected do
    v:=AFSBackgroundNativeCup0(ctx,2,wNative,q,H.generators[i]);;
    Assert(0,v=AFSNativeCupIFull(ctx,2,q,0,wNative,H.generators[i]));
    fn:=AFSBar(ctx,q,"F2",H.generators[i]);;
    barProduct:=AFSCup(0,2,ctx.omega2,q,fn);;
    start:=Runtime();;
    barNative:=AFSNative(ctx,q+2,"F2",barProduct);;
    barCPU:=Runtime()-start;;
    cf:=HF.coordinates(v);cb:=HF.coordinates(barNative);;
    Assert(0,cf<>fail and cb<>fail and cf=cb);
    cu:=HU.coordinates(v/2);cub:=HU.coordinates(barNative/2);;
    Assert(0,cu<>fail and cub<>fail and cu=cub);
    Add(cohomologyChecks,rec(degree:=q,generator:=i,F2_coordinates:=cf,
      signed_U1_coordinates:=cu,bar_cpu_ms:=barCPU));
  od;
od;
LoadPackage("json");;
stream:=OutputTextFile(AFS_OUT,false);;
SetPrintFormattingStatus(stream,false);
WriteAll(stream,GapToJsonString(rec(space_group:=AFS_SG,
  scope:="same-native-D0-cup0-exact-F2-optimization",production_dispatch_changed:=false,
  resolution_dimensions:=List([0..6],k->Dimension(ctx.R)(k)),
  mod2_contraction:=AFSDiagonalContract=AFSContractCellMod2,
  vector_checks:=records,bar_cohomology_checks:=cohomologyChecks)));
CloseStream(stream);
Print("BACKGROUND_NATIVE_CUP_TEST_PASS ",AFS_SG,"\n");
QUIT_GAP(0);
