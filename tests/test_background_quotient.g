AFS_ROOT:=".";;
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/background_quotient.g");;

MakeLower:=function(R,layers)
  local S;
  S:=AFSSmith(R,Length(R),Length(layers));
  return rec(status:="computed",presentation:=R,smith:=S,
    invariants:=AFSBackgroundSmithInvariants(S,Length(layers)),
    generators:=List([1..Length(layers)],i->rec(name:=Concatenation("g",String(i)),layer:=layers[i])),
    finalFiltrationCertificate:=rec(testInput:=true));
end;;
Check:=function(name,R,layers,x,inv,graded,order)
  local H,Q,F,i,j,proof;
  H:=MakeLower(R,layers);Q:=AFSBackgroundQuotientPresentation(H,x,rec());
  Assert(0,Q.status="computed" and Q.lower.invariants=inv);
  Assert(0,Q.incomingOrder=order);
  Assert(0,Q.graded.bosonic=graded[1]);
  Assert(0,Q.graded.complex_fermion=graded[2]);
  Assert(0,Q.graded.majorana=graded[3]);
  for F in Q.filtration do
    Assert(0,ForAll(F.intersectionRelationRows,r->ForAll(F.upperIndices,j->r[j]=0)));
    if Length(layers)>0 and Length(F.relationCombinationRows)>0 then
      Assert(0,F.relationCombinationRows*Q.lower.presentation=F.intersectionRelationRows);
    fi;
  od;
  Print("BACKGROUND_QUOTIENT_PASS ",name," incoming_order=",order,
    " invariants=",inv," graded=",graded,"\n");
  return Q;
end;;

# In H=Z8, the three associated graded layers are all Z2. Quotienting the
# actual highest lift kills its square and fourth power in the lower layers.
R8:=[[2,0,0],[-1,2,0],[0,-1,2]];;
Q:=Check("Z8-generator-kills-all-three-layers",R8,[0,1,2],[0,0,1],[],[[],[],[]],8);;
Q:=Check("Z8-even-generator-retains-only-MC",R8,[0,1,2],[0,0,2],[2],[[],[],[2]],4);;
Q:=Check("Z8-fourth-power-kills-only-boson",R8,[0,1,2],[1,0,0],[4],[[],[2],[2]],2);;
Q:=Check("Z8-odd-coordinate-change-same-subgroup",R8,[0,1,2],[1,1,1],[],[[],[],[]],8);;

# Here X=C+B has order4. Its square kills D, while identifying B with C.
# The surviving Z2 lies in the CF filtration, not in the original MC quotient.
Q:=Check("Z4-plus-Z2-diagonal-boundary",[[2,0,0],[-1,2,0],[0,0,2]],
  [0,1,2],[0,1,1],[2],[[],[2],[]],4);;
Q:=Check("split-Z2-boundary-identifies-boson-with-MC",2*IdentityMat(3),
  [0,1,2],[1,0,1],[2,2],[[2],[2],[]],2);;
Q:=Check("odd-cyclic-factor",[[12]],[0],[4],[4],[[4],[],[]],3);;
Q:=Check("trivial-boundary-keeps-filtration",R8,[0,1,2],[2,0,0],[8],[[2],[2],[2]],1);;
Q:=Check("empty-group",[],[],[],[],[[],[],[]],1);;
Q:=Check("free-cyclic-boundary",[[2,0]],[0,2],[1,1],[2],[[2],[],[]],0);;

# Exhaust all 8 elements of Z8 and compare the quotient order to a direct
# subgroup enumeration in Z/8, independently of the relation-intersection code.
for k in [0..7] do
  H:=MakeLower(R8,[0,1,2]);Q:=AFSBackgroundQuotientPresentation(H,[0,0,k],rec());;
  orbit:=Set(List([0..7],j->j*k mod 8));;
  Assert(0,Q.incomingOrder=Length(orbit));
  size:=Product(Q.lower.invariants);Assert(0,size*Length(orbit)=8);
  Assert(0,Product(Concatenation(Q.graded.bosonic,Q.graded.complex_fermion,Q.graded.majorana))=size);
od;
Print("BACKGROUND_QUOTIENT_FINITE_ENUMERATION_PASS 8\n");
Print("BACKGROUND_QUOTIENT_TEST_PASS\n");
QUIT_GAP(0);
