AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
sg:=SpaceGroupBBNWZ(3,1);; iso:=IsomorphismPcpGroup(sg);; L:=Image(iso);;
R:=AFSLatticeResolution(L,6);; br:=AFSComparison(R);;
gens:=R!.afsLatticeGenerators;;
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
for k in [0..3] do
  for i in [1..R!.dimension(k)] do
    for a in [[0,0,0],[2,-1,3],[-2,1,-1],[0,-3,2]] do
      g:=Product([1..3],j->gens[j]^a[j]);;
      t:=[1,i,g];;
      lhs:=Concatenation(ND(k+1,AFSNativeContract(br,k,[t])),
                        AFSNativeContract(br,k-1,ND(k,[t])));;
      Add(lhs,[-1,i,g]);;
      if k=0 then Add(lhs,[1,1,Identity(L)]); fi;
      if AFSCombineChain(lhs,false)<>[] then Error("Koszul contraction identity"); fi;
    od;
  od;
od;
Print("AFS_KOSZUL_CONTRACTION_PASS\n"); QUIT_GAP(0);
