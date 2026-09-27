if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_half_phase.g"));;
for sg in [7,47] do
  c:=AFSBackend(sg);;
  for k in [1..5] do
    f:=function(xs...)
      local j,value;
      if One(c.G) in xs then return 0;fi;
      value:=1;
      for j in [1..Length(xs)] do value:=value*(Sum(xs[j]!.exponents)+j)+Sum(xs[j]!.exponents)^2;od;
      return (value mod 2)/2;
    end;;
    expected:=AFSNative(c,k,"U1s",f);;
    if AFSNativeHalfPhase(c,k,f)<>expected then Error("half-phase coefficient filtering changed native vector");fi;
    if AFSNativeHalfPhaseSmith(c,k,f)<>expected then Error("Smith half-phase coefficient filtering changed native vector");fi;
  od;
  Print("HALF_PHASE_NATIVE_PASS sg=",sg," degrees=1..5\n");
od;
Print("AFS_HALF_PHASE_TEST_PASS\n");QUIT_GAP(0);
