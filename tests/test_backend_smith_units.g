AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
expected:=[];;
for dims in [[2,3],[3,2],[5,5],[9,7],[7,9]] do
 for trial in [1..12] do
  M:=List([1..dims[1]],i->List([1..dims[2]],j->Random([-4..4])));;
  S:=AFSSmithUnits(M,dims[1],dims[2]);;
  if S.U*M*S.V<>S.D or S.U*S.Ui<>IdentityMat(dims[1]) or S.V*S.Vi<>IdentityMat(dims[2]) then Error("unit Smith transforms"); fi;
  expected:=SmithNormalFormIntegerMat(M);;
  if List(S.diag,AbsInt)<>List([1..Minimum(dims)],i->AbsInt(expected[i][i])) then Error("unit Smith invariants"); fi;
 od;
od;
Print("AFS_SMITH_UNITS_TEST_PASS\n");
if IsBound(AFS_SG) then
 c:=AFSBackend(AFS_SG);;
 for k in [4,5] do
  D:=AFSDifferential(c,k,"Zs");; t:=Runtime();;
  S:=AFSSmithUnits(D,Length(D),Length(D[1]));;
  Print("UNIT_SMITH_TIME ",k," ",Runtime()-t," diag=",Filtered(S.diag,x->AbsInt(x)>1),"\n");
  if S.U*D*S.V<>S.D or S.U*S.Ui<>IdentityMat(Length(D)) or S.V*S.Vi<>IdentityMat(Length(D[1])) then Error("differential unit Smith transforms"); fi;
  Print("UNIT_SMITH_CERTIFIED ",k,"\n");
 od;
fi;
Print("AFS_SMITH_UNITS_BENCH_PASS\n");QUIT_GAP(0);
