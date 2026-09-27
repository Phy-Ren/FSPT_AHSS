AFS_ROOT:=".";;
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/stacking.g");;
Reset(GlobalMersenneTwister,17029);;
for case in [1..36] do
  n:=Random([1..4]);;
  ds:=List([1..n],i->Random([0,2,4,6,8,12,16]));;
  T:=IdentityMat(n);;
  if n>1 then
    for j in [1..5] do
      a:=Random([1..n]);b:=Random(Filtered([1..n],i->i<>a));q:=Random([-2,-1,1,2]);
      for row in T do row[b]:=row[b]+q*row[a];od;
    od;
  fi;
  R:=[];;
  for i in [1..n] do if ds[i]<>0 then Add(R,ds[i]*T[i]);fi;od;
  lower:=rec(generators:=List([1..n],i->rec()),presentation:=R,
    smith:=AFSSmith(R,Length(R),n));;
  leading:=List([1..n],i->Random([-2..2]));;
  indices:=Filtered([1..n],i->Random([0,1])=1);;
  answer:=AFSStackExtensionByTwo(lower,leading,indices);;
  brute:=[];;
  for bits in Tuples([0,1],Length(indices)) do
    z:=ShallowCopy(leading);;
    for i in [1..Length(indices)] do z[indices[i]]:=z[indices[i]]+bits[i];od;
    extensionRows:=List(R,row->Concatenation(row,[0]));Add(extensionRows,Concatenation(-z,[2]));;
    S:=AFSSmith(extensionRows,Length(extensionRows),n+1);;
    inv:=Concatenation(List([S.rank+1..n+1],i->0),Filtered(List(S.diag,AbsInt),x->x>1));;
    if not inv in brute then Add(brute,inv);fi;
  od;
  Assert(0,Set(answer.invariantOptions)=Set(brute));
od;
Print("EXTENSION_HEIGHT_TESTS_PASS 36 independent integer-presentation comparisons\n");
QUIT_GAP(0);
