AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
if not IsBound(AFS_SG) then AFS_SG:=47; fi;
t:=Runtime();; c:=AFSBackend(AFS_SG);; Print("RESOLUTION_MS ",Runtime()-t,"\n");
for p in [2,3] do
  H:=AFSCohomology(c,p,"F2");;
  t:=Runtime();;
  for a in H.generators do x:=AFSNativeSq2(c,p,a);; od;
  Print("NATIVE_ALL ",p," generators=",Length(H.generators)," ms=",Runtime()-t,"\n");
od;
Print("AFS_NATIVE_BENCH_PASS\n"); QUIT_GAP(0);
