if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formula_fast.g"));;
Read(Concatenation(AFS_ROOT,"/gap/stacking_closed_cf.g"));;
g:=CyclicGroup(IsPermGroup,3);; a:=GeneratorsOfGroup(g)[1];;
c:=rec(G:=g,s:=AFSZero,sign:=x->1);;
nonclosed:=function(x,y,z)
  if x=a and y=a and z=a then return 1;else return 0;fi;
end;;
delta:=AFSCoboundary(c,"F2",nonclosed);;
if ForAll(Tuples([a,a^2],4),xs->CallFuncList(delta,xs)=0) then Error("domain counterexample is accidentally closed");fi;
full:=AFSFormula("obstruction",c,rec(p:=2,a:=AFSZero,c:=nonclosed));;
short:=AFSClosedCFObstruction(nonclosed);;count:=0;;
for xs in Tuples([a,a^2],5) do
  if CallFuncList(full,xs)<>CallFuncList(short,xs) then count:=count+1;fi;
od;
if count=0 then Error("nonclosed-domain counterexample did not distinguish formulas");fi;
Print("AFS_CLOSED_CF_DOMAIN_PASS nonclosed_mismatches=",count,"\n");
QUIT_GAP(0);
