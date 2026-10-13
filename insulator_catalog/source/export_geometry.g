# Read-only geometry export. Does not build resolutions or compute classifications.
LoadPackage("CrystCat");;
SizeScreen([100000,24]);;
Print("BEGIN_WALLPAPER\n");;
for n in [1..17] do
  G:=SpaceGroupBBNWZ(2,n);;
  P:=Image(PointHomomorphism(G));;
  Print("U1_GEOMETRY ",[n,GeneratorsOfGroup(G),Elements(P)],"\n");
od;
Print("BEGIN_POINT3\n");;
for n in [1,2,3,6,10,16,25,47,75,81,83,89,99,111,123,143,147,149,156,162,168,174,175,177,183,187,191,195,200,207,215,221] do
  P:=MatGroupZClass(3,n);;
  Print("U1_GEOMETRY ",[n,GeneratorsOfGroup(P),Size(P)],"\n");
od;
Print("U1_VERSION ",GAPInfo.Version," ",PackageInfo("CrystCat")[1].Version,"\n");;
QUIT;
