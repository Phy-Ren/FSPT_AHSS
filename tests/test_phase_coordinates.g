AFS_ROOT:=".";;
Read("gap/backend.g");;
Read("gap/backend_diagonal.g");;
Read("gap/formula_data.g");;
Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;
Read("gap/formula_fast.g");;
Read("gap/classification.g");;
Read("gap/pip.g");;
Read("gap/class_coordinates.g");;
ctx:=AFSBackend(Int(GAPInfo.SystemEnvironment.AFS_TEST_SG));;
for k in [4,5] do
  H:=AFSCohomology(ctx,k,"U1s");;
  for v in H.generators do
    f:=AFSBar(ctx,k,"U1s",v);;
    Assert(0,AFSU1BarCoordinates(ctx,k,H,f)=H.coordinates(AFSNative(ctx,k,"U1s",f)));
  od;
od;
C:=AFSClassify(ctx);;
for m in C.mcLifts do
  if IsBound(m.obstruction) then
    Assert(0,AFSU1BarCoordinates(ctx,5,C.H5U,m.obstruction)=C.H5U.coordinates(AFSNative(ctx,5,"U1s",m.obstruction)));
  fi;
od;
Print("PHASE_COORDINATES_PASS ",ctx.number,"\n");
QUIT_GAP(0);
