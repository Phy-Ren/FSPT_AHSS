AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));;
if not IsBound(AFS_SG) then AFS_SG:=104;fi;
c:=AFSBackend(AFS_SG);;gens:=GeneratorsOfGroup(c.G);;
for k in [0..4] do
 for i in Set([1,Int((1+Dimension(c.R)(k))/2),Dimension(c.R)(k)]) do
  for g in [gens[1],gens[Length(gens)],(gens[1]*gens[Length(gens)])^-1] do
   actual:=AFSContractCellMod2(c.bar,k,i,g);;
   expected:=AFSMod2NativeReduce(AFSContractCell(c.bar,k,i,g));;
   if AFSMod2NativeReduce(Concatenation(actual,expected))<>[] then
    Print("BAD ",k," ",i," ",AFSKey([g]),"\n");Error("mod-two contraction mismatch");
   fi;
  od;
 od;
od;
Print("AFS_MOD2_CONTRACTION_PASS ",AFS_SG,"\n");QUIT_GAP(0);
