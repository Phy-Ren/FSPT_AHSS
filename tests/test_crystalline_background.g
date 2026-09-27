AFS_ROOT:=".";;
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/crystalline_background.g");;

# Minimal Pin-minus geometric conventions, including the identity and inversion.
mir:=DiagonalMat([-1,1,1]);;rot:=DiagonalMat([-1,-1,1]);;inv:=-IdentityMat(3);;
for pair in [[mir,1],[rot,1],[inv,0]] do
  d:=AFSPinMinusPointGroup(Group([pair[1]]));;
  Assert(0,d.omega2(pair[1],pair[1])=pair[2]);
  Assert(0,d.omega2(One(d.pointGroup),pair[1])=0);
  Assert(0,d.omega2(pair[1],One(d.pointGroup))=0);
od;
Print("PIN_MINUS_BASIC_PASS\n");

# Independent double-group relation: orthogonal proper pi rotations anticommute.
r1:=DiagonalMat([1,-1,-1]);;r2:=DiagonalMat([-1,1,-1]);;
d:=AFSPinMinusPointGroup(Group([r1,r2]));;
Assert(0,(d.omega2(r1,r2)+d.omega2(r2,r1)) mod 2=1);
# The same check in a nonorthogonal rational lattice basis excludes a hidden
# Euclidean-metric assumption. It checks the gauge-invariant commutator.
change:=[[1,1,0],[0,2,1],[0,0,3]];;
r1c:=Inverse(change)*r1*change;;r2c:=Inverse(change)*r2*change;;
dc:=AFSPinMinusPointGroup(Group([r1c,r2c]));;
Assert(0,(dc.omega2(r1c,r2c)+dc.omega2(r2c,r1c)) mod 2=1);
Print("PIN_MINUS_RATIONAL_BASIS_PASS\n");

# Exhaust every actual crystallographic point group and every affine generator
# projection. No group classification or expected FSPT answer is consulted.
for number in [1..230] do
  affine:=SpaceGroupBBNWZ(3,number);;iso:=IsomorphismPcpGroup(affine);;
  c:=rec(number:=number,affine:=affine,iso:=iso,G:=Image(iso));;
  c.s:=AFSMemo(g->(1-DeterminantMat(PreImageElm(c.iso,g)))/2);;
  d:=AFSInstallCrystallineBackground(c);;
  Assert(0,d.normalizedCocycleChecked=true);
  gs:=GeneratorsOfGroup(c.G);;xs:=Concatenation([One(c.G)],gs,List(gs,Inverse));;
  for a in xs do
    for b in xs do
      Assert(0,c.omega2(a,b)=d.omega2(Image(d.projection,a),Image(d.projection,b)));
      Assert(0,c.omega2(One(c.G),a)=0 and c.omega2(a,One(c.G))=0);
    od;
  od;
  if number mod 20=0 or number=230 then Print("PIN_MINUS_AFFINE_PASS ",number,"\n");fi;
od;

# Comparison-map pullback and native closure on complete affine resolutions.
for number in [1,2,3,6,19,146] do
  c:=AFSBackend(number);;d:=AFSInstallCrystallineBackground(c);;
  w:=AFSCrystallineOmegaNative(c);;
  Assert(0,ForAll(w*AFSDifferential(c,2,"F2"),x->x mod 2=0));
  h:=AFSCohomology(c,2,"F2");;coords:=h.coordinates(w);;
  Assert(0,coords<>fail);
  Print("PIN_MINUS_NATIVE_PASS ",number," cohomology_coordinates=",coords,"\n");
od;
Print("CRYSTALLINE_BACKGROUND_TEST_PASS\n");
QUIT_GAP(0);
