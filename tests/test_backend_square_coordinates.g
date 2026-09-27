AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
if not IsBound(AFS_SG) then AFS_SG:=47; fi;
c:=AFSBackend(AFS_SG);;
for p in [2,3] do
  H:=AFSCohomology(c,p,"F2");; T:=AFSCohomology(c,p+2,"U1s");;
  t:=Runtime();;
  for a in H.generators do
    actual:=AFSNativeSq2U1Coordinates(c,p,a,T);;
    expected:=T.coordinates(AFSNativeSq2(c,p,a)/2);;
    if actual<>expected then
      Print("BAD ",p," actual=",actual," expected=",expected,"\n");
      Error("direct square coordinates mismatch");
    fi;
  od;
  if Length(H.generators)>1 then
    a:=List(Sum(H.generators),x->x mod 2);;
    if AFSNativeSq2U1Coordinates(c,p,a,T)<>T.coordinates(AFSNativeSq2(c,p,a)/2) then
      Error("direct square sum mismatch");
    fi;
  fi;
  Print("SQUARE_COORDINATES ",p," generators=",Length(H.generators)," ms=",Runtime()-t,"\n");
od;
Print("AFS_SQUARE_COORDINATES_PASS ",AFS_SG,"\n"); QUIT_GAP(0);
