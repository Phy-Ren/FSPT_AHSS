if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));;
Read(Concatenation(AFS_ROOT,"/gap/stacking_closed_cf.g"));;
G:=CyclicGroup(IsPermGroup,3);;a:=GeneratorsOfGroup(G)[1];;AFSTestElements:=[One(a),a,a^2];;
MakeC:=function(mask,raw)
  return function(g,h,j)
    local x,y,z,k;
    x:=Position(AFSTestElements,g)-1;y:=Position(AFSTestElements,h)-1;z:=Position(AFSTestElements,j)-1;
    if raw then return (x*y+3*y*z+x*z+mask*(x+2*y+z)+mask^2) mod 7-3;fi;
    if 0 in [x,y,z] then return 0;fi;
    k:=4*(x-1)+2*(y-1)+z-1;return QuoInt(mask,2^k) mod 2;
  end;
end;;
count:=0;;
for raw in [false,true] do
  if raw then masks:=[0..15];tupleValues:=AFSTestElements;
  else masks:=[0..255];tupleValues:=[a,a^2];fi;
  for mask in masks do
    f:=MakeC(mask,raw);;reference:=AFSClosedCFObstruction(f);;eager:=AFSClosedCFObstructionDirect(f);;lazy:=AFSClosedCFObstructionLazy(f);;
    for xs in Tuples(tupleValues,5) do
      expected:=CallFuncList(reference,xs);
      if CallFuncList(eager,xs)<>expected or CallFuncList(lazy,xs)<>expected then Error("lazy cup1 normalization or scalar value differs");fi;
      count:=count+1;
    od;
  od;
od;
Print("AFS_CLOSED_CF_LAZY_PASS cases=",count,"\n");QUIT_GAP(0);
