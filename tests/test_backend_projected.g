AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if IsBound(AFS_USE_MOD2_CONTRACTION) and AFS_USE_MOD2_CONTRACTION then
 Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));;
fi;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
if not IsBound(AFS_SG) then AFS_SG:=47; fi;
c:=AFSBackend(AFS_SG);;
H:=AFSCohomology(c,3,"F2");;
t:=Runtime();;
actual:=List(H.generators,a->AFSNativeCup1Projected(c,3,a,3,a));;
if IsBound(AFS_USE_MOD2_CONTRACTION) and AFS_USE_MOD2_CONTRACTION then
 Assert(0,AFSDiagonalContract=AFSContractCellMod2);
 Assert(0,IsBound(c.bar.mod2HCache));
 Print("MOD2_CONTRACTION_USED\n");
fi;
Print("PROJECTED_TIME ",Runtime()-t," marginal=",IsBound(c.diagonalRightCache),"\n");
if not IsBound(AFS_BENCH_ONLY) then
  for q in [1..3] do
    for j in [1..Dimension(c.R)(q-1)] do
      seed:=Filtered(AFSHigherDiagonalCapped(c,1,q-1,j,q),t->t[1]=0 and t[4]=q);;
      if seed<>[] then Error("D1 zero-left seed is not zero"); fi;
    od;
  od;
  for i in [1..Length(H.generators)] do
    a:=H.generators[i];;
    if actual[i]<>AFSNativeCupIFull(c,3,3,1,a,a) then Error("projected native vector mismatch"); fi;
  od;
  for i in [1..Minimum(5,Length(H.generators))] do
    a:=H.generators[1];; b:=H.generators[i];;
    if AFSNativeCup1Projected(c,3,a,3,b)<>AFSNativeCupIFull(c,3,3,1,a,b) then
      Error("projected mixed cup mismatch");
    fi;
  od;
fi;
Print("AFS_PROJECTED_TEST_PASS ",AFS_SG,"\n"); QUIT_GAP(0);
