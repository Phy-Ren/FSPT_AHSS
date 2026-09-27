if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_half_phase.g"));;
for sg in [7,47] do
  ctx:=AFSBackend(sg);;
  psi:=function(g,h)
    if One(ctx.G) in [g,h] then return 0;fi;
    return ((Sum(g!.exponents)^2*Sum(h!.exponents)+Sum(h!.exponents)^3) mod 2)/2;
  end;;
  source:=AFSCoboundary(ctx,"U1s",psi);;old:=AFSSolve(ctx,3,"U1s",source);;
  data:=AFSSolveHalfPhaseData(ctx,3,source);;
  if old=fail or data=fail then Error("known half-valued boundary has no primitive");fi;
  nv:=AFSNative(ctx,3,"U1s",source);;
  if data.nativeObstruction<>nv or data.nativePrimitive<>AFSSolveNative(ctx,3,"U1s",nv) then Error("half phase solve changed canonical native data");fi;
  dnew:=AFSCoboundary(ctx,"U1s",data.primitive);;
  gs:=GeneratorsOfGroup(ctx.G);;elts:=Concatenation(gs,List(gs,g->g^-1),[gs[1]^2,gs[1]*gs[Length(gs)]]);;
  for j in [1..24] do
    xs:=List([1..2],i->elts[1+((3*j+i^2) mod Length(elts))]);;
    if CallFuncList(old,xs)<>CallFuncList(data.primitive,xs) then Error("half phase solve changed marked bar primitive");fi;
    xs:=List([1..3],i->elts[1+((3*j+i^2) mod Length(elts))]);;
    if CallFuncList(dnew,xs)<>CallFuncList(source,xs) then Error("half phase corrected bar primitive equation failed");fi;
  od;
  Print("HALF_PHASE_PRIMITIVE_PASS sg=",sg," translated_cases=24\n");
od;
Print("AFS_HALF_PHASE_PRIMITIVE_TEST_PASS\n");QUIT_GAP(0);
