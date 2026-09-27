AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=47; fi;
c:=AFSBackend(AFS_SG);;
Print("BACKEND_GROUP ",AFS_SG," dimensions=",List([0..6],k->Dimension(c.R)(k)),"\n");
for ck in [[0,"Zs"],[1,"Zs"],[1,"F2"],[2,"F2"],[3,"F2"],[4,"F2"],[4,"U1s"],[5,"U1s"]] do
  H:=AFSCohomology(c,ck[1],ck[2]);;
  Print("H ",ck," ",H.orders,"\n");
  for j in [1..Length(H.generators)] do
    e:=List(H.orders,x->0);; e[j]:=1;;
    if H.coordinates(H.generators[j])<>e then Error("native basis coordinates"); fi;
    f:=AFSBar(c,ck[1],ck[2],H.generators[j]);;
    v:=AFSNative(c,ck[1],ck[2],f);;
    if H.coordinates(v)<>e then Error("comparison cohomology identity"); fi;
  od;
od;
Print("AFS_BACKEND_CASE_PASS ",AFS_SG,"\n");
QUIT_GAP(0);
