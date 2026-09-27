AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
if not IsBound(AFS_SG) then AFS_SG:=230; fi;
t:=Runtime();; c:=AFSBackend(AFS_SG);; Print("RESOLUTION_MS ",Runtime()-t,"\n");
for p in [2,3] do
  H:=AFSCohomology(c,p,"F2");; T:=AFSCohomology(c,p+2,"U1s");;
  Print("SQUARE_TARGET ",p," ",T.orders,"\n");
  t:=Runtime();;
  for a in H.generators do x:=AFSNativeSq2U1Coordinates(c,p,a,T);; Print("SQUARE_COORD ",p," ",x,"\n"); od;
  Print("SQUARE_ALL ",p," generators=",Length(H.generators)," ms=",Runtime()-t,"\n");
od;
Print("AFS_SQUARE_BENCH_PASS\n"); QUIT_GAP(0);
