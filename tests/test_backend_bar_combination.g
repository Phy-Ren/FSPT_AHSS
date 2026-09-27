AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=2;fi;
c:=AFSBackend(AFS_SG);;
for k in [3,4,5] do
 H:=AFSCohomology(c,k,"F2");;
 z:=List([1..Dimension(c.R)(k)],i->((3*i+1) mod 5)-2);;
 actual:=AFSChainToBarCombination(c.bar,k,z);;expected:=[];;
 for i in [1..Length(z)] do
  for t in AFSChainToBar(c.bar,k,i) do Add(expected,[z[i]*t[1],t[2],t[3]]);od;
 od;
 Append(actual,List(expected,t->[-t[1],t[2],t[3]]));;
 if AFSCombineChain(actual,true)<>[] then Error("bar scalar combination identity");fi;
od;
Print("AFS_BAR_COMBINATION_PASS ",AFS_SG,"\n");QUIT_GAP(0);
