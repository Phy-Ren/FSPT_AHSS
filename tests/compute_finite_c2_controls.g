# Post-freeze external comparison controls. This harness contains no expected
# results. Finite C2 is used only for the collaborator's finite examples and
# never substitutes for an affine space group in production.
AFS_ROOT:=GAPInfo.SystemEnvironment.AFS_TEST_SOURCE;;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","backend_diagonal.g","formula_data.g",
    "formula_fast.g","pip_o5_program.g","pip_o5_sign.g","formulas.g",
    "classification.g","pip.g","stacking.g","pip_coordinate_data.g",
    "pip_coordinates.g","pip_diagonal_data.g","pip_c4_data.g","pip_stacking.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
rows:=[];;
for signBit in [0,1] do
  G:=CyclicGroup(IsPcpGroup,2);;
  ctx:=rec(number:=0,G:=G,differentialCache:=rec(),smithCache:=rec(),
    cohomologyCache:=rec(),f2SolveCache:=rec());;
  if signBit=0 then ctx.sign:=g->1;ctx.s:=AFSZero;
  else ctx.sign:=function(g) if g=One(G) then return 1;else return -1;fi;end;
    ctx.s:=g->(1-ctx.sign(g))/2;
  fi;
  ctx.action:=ctx.sign;
  ctx.R:=ResolutionFiniteGroup(G,6,false,0,"extendible");;
  ctx.bar:=AFSComparison(ctx.R);;
  C:=AFSClassify(ctx);;stacking:=AFSExplicitPipStacking(C);;
  Add(rows,rec(group:="CyclicGroup(2)",spatialDimension:=3,omega:=0,s:=signBit,
    status:=stacking.status,invariants:=stacking.invariants,
    layers:=rec(pip:=C.summary.pip.orders,majorana:=C.summary.majorana,
      fermion:=C.summary.complex_fermion,bosonic:=C.summary.bosonic)));
od;
LoadPackage("json");;
stream:=OutputTextFile("runs/finite_c2_controls.json",false);;
SetPrintFormattingStatus(stream,false);;
WriteAll(stream,GapToJsonString(rec(
  scope:="independent-3D-omega0-finite-C2-comparison-controls",source:=AFS_ROOT,results:=rows)));;
CloseStream(stream);;
Print("FINITE_C2_CONTROLS_COMPUTED ",List(rows,r->[r.s,r.invariants]),"\n");
QUIT_GAP(0);
