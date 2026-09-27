AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=230; fi;
c:=AFSBackend(AFS_SG);; R:=c.R;;
ND:=function(k,terms)
  local out,t,w;
  out:=[]; if k=0 then return out; fi;
  for t in terms do
    for w in R!.boundary(k,t[2]) do
      Add(out,[t[1]*SignInt(w[1]),AbsInt(w[1]),t[3]*R!.elts[w[2]]]);
    od;
  od;
  return AFSCombineChain(out,false);
end;;
for k in [2..6] do
  for i in [1..R!.dimension(k)] do
    if ND(k-1,ND(k,[[1,i,Identity(c.G)]]))<>[] then Error("group-ring d^2"); fi;
  od;
od;
Print("CUBIC_GROUP_RING_D2_PASS ",AFS_SG,"\n");
gens:=GeneratorsOfGroup(c.G);;
for k in [0..5] do
  for i in Set([1,R!.dimension(k)]) do
    for g in [gens[1],gens[Length(gens)],(gens[1]*gens[Length(gens)])^-1] do
      Print("CUBIC_CONTRACT_CELL ",k," ",i," ",AFSKey([g]),"\n");
      lhs:=Concatenation(ND(k+1,AFSNativeContract(c.bar,k,[[1,i,g]])),
                        AFSNativeContract(c.bar,k-1,ND(k,[[1,i,g]])));;
      Add(lhs,[-1,i,g]);;
      if k=0 then Add(lhs,[1,1,Identity(c.G)]); fi;
      if AFSCombineChain(lhs,false)<>[] then Error("affine contraction identity"); fi;
    od;
  od;
od;
Print("CUBIC_CONTRACTION_PASS ",AFS_SG,"\n");
for k in [1..5] do
  H:=AFSCohomology(c,k,"F2");; Print("CUBIC_H_F2 ",k," ",H.orders,"\n");
od;
for k in [4,5] do
  H:=AFSCohomology(c,k,"U1s");; Print("CUBIC_H_U1 ",k," ",H.orders,"\n");
  for i in [1..Length(H.generators)] do
    e:=List(H.orders,x->0);; e[i]:=1;;
    if H.coordinates(H.generators[i])<>e then Error("cubic U1 coordinates"); fi;
  od;
od;
Print("AFS_CUBIC_BACKEND_PASS ",AFS_SG,"\n"); QUIT_GAP(0);
