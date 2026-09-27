AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_cup_slant.g"));;
if not IsBound(AFS_SG) then AFS_SG:=47;fi;
c:=AFSBackend(AFS_SG);;H:=AFSCohomology(c,3,"F2");;
t:=Runtime();;
if IsBound(AFS_BENCH_ONLY) then inputs:=H.generators;
else inputs:=H.generators{[1..Minimum(4,Length(H.generators))]};fi;
actual:=List(inputs,a->AFSNativeCup1Slant(c,3,a,3,a));;
Print("SLANT_TIME ",Runtime()-t," generators=",Length(inputs),"\n");
if not IsBound(AFS_BENCH_ONLY) then
 for i in [1..Length(inputs)] do
  if actual[i]<>AFSNativeCupIFull(c,3,3,1,inputs[i],inputs[i]) then Error("slant native square mismatch");fi;
  if AFSNativeCup1Slant(c,3,inputs[1],3,inputs[i])<>AFSNativeCupIFull(c,3,3,1,inputs[1],inputs[i]) then Error("slant mixed cup mismatch");fi;
 od;
fi;
Print("AFS_SLANT_TEST_PASS ",AFS_SG,"\n");QUIT_GAP(0);
