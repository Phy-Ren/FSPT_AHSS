AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=104;fi;
c:=AFSBackend(AFS_SG);;
f2:=AFSMemo(function(gs...)
 local v,i;
 if Identity(c.G) in gs then return 0;fi;
 v:=AFSKey(gs);return Sum([1..Length(v)],i->i*v[i]^2) mod 2;
end);;
fu:=AFSMemo(function(gs...)
 local v,i;
 if Identity(c.G) in gs then return 0;fi;
 v:=AFSKey(gs);return (Sum([1..Length(v)],i->i^2*v[i]) mod 8)/8;
end);;
elts:=GeneratorsOfGroup(c.G);;xs:=[];;
for coeff in ["F2","U1s"] do
 if coeff="F2" then f:=f2;else f:=fu;fi;
 h:=AFSHomotopyPullback(c.bar,coeff,f);;
 for n in [1..3] do
  for trial in [1..12] do
   xs:=List([1..n],i->Random(elts));;
   expected:=Sum(AFSChainHomotopy(c.bar,xs),t->t[1]*CallFuncList(f,t[3]));;
   if coeff="F2" then expected:=expected mod 2;else expected:=AFSMod1(expected);fi;
   if CallFuncList(h,xs)<>expected then Error("scalar homotopy pullback mismatch");fi;
  od;
 od;
od;
Print("AFS_SCALAR_HOMOTOPY_PASS ",AFS_SG,"\n");QUIT_GAP(0);
