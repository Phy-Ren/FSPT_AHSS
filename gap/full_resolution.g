# Optional exact tensor resolution for finite abelian groups. This changes
# only the free resolution used for cochain arithmetic, never the input group,
# background cocycle, or formulas. Cyclic factors retain the top contraction.
BindGlobal("AFSFullTensorAbelianResolution",function(P,depth)
  local orders,R,next,Q,map,order;
  if not IsAbelian(P) or Size(P)=1 then return AFSFiniteHolonomyResolution(P,depth);fi;
  orders:=AbelianInvariants(P);R:=fail;
  for order in orders do
    Q:=CyclicGroup(IsPermGroup,order);
    next:=ResolutionFiniteGroup(Q,depth,false,0,"extendible");
    if R=fail then R:=next;else R:=ResolutionFiniteDirectProduct(R,next);fi;
  od;
  Q:=GroupOfResolution(R);map:=IsomorphismGroups(Q,P);
  if map=fail then Error("abelian tensor resolution has the wrong group");fi;
  R!.elts:=List(R!.elts,x->Image(map,x));R!.group:=P;
  R!.afsTensorCyclicOrders:=orders;
  return R;
end);

# Build from the supplied finite generators before conversion to a PC sequence.
# The latter may contain many redundant generators for the HAP construction.
# Transport the complete integral resolution and contraction back to P.
BindGlobal("AFSFullInputGeneratorsResolution",function(P,depth,data)
  local generators,Q,R,map;
  generators:=List(data.generatorIndices,i->PermList(
    List([1..data.order],j->data.productTable[j][i])));
  if Length(generators)=0 then
    if data.order<>1 then Error("nontrivial input requires generators");fi;
    return AFSFiniteHolonomyResolution(P,depth);
  fi;
  Q:=Group(generators);
  if Size(Q)<>data.order then Error("input generators do not generate the supplied group");fi;
  map:=IsomorphismGroups(Q,P);
  if map=fail then Error("input-generator resolution group mismatch");fi;
  R:=ResolutionFiniteGroup(Q,depth,false,0,"extendible");
  R!.elts:=List(R!.elts,x->Image(map,x));R!.group:=P;
  R!.afsInputGeneratorResolution:=true;
  return R;
end);

# Independent presentation/contraction check for a dihedral bosonic group.
# The model group and its background remain unchanged; only the resolution is
# built on the standard small permutation representation and transported.
BindGlobal("AFSFullDihedralPermutationResolution",function(P,depth)
  local Q,R,map;
  Q:=DihedralGroup(IsPermGroup,Size(P));map:=IsomorphismGroups(Q,P);
  if map=fail then Error("standard dihedral resolution requires an isomorphic dihedral group");fi;
  R:=ResolutionFiniteGroup(Q,depth,false,0,"extendible");
  R!.elts:=List(R!.elts,x->Image(map,x));R!.group:=P;
  R!.afsStandardDihedralPermutation:=true;
  return R;
end);

# Explicit nonabelian factors avoid a redundant PC generating sequence for
# these direct products. The isomorphism transports every integral boundary
# and contraction coefficient to the original input group, as above.
BindGlobal("AFSFullDirectProductResolution",function(P,depth,family)
  local Q1,Q2,R1,R2,R,Q,map,r,t;
  if family="D8xC2" then
    Q1:=DihedralGroup(IsPermGroup,8);
  elif family="Q8xC2" then
    # Right regular action in normal words r^a t^b, with r^4=1,
    # t^2=r^2 and trt^-1=r^-1. Retain just these two generators.
    r:=PermList(List([0..7],i->(((i mod 4)+(-1)^QuoInt(i,4)) mod 4)
      +4*QuoInt(i,4)+1));
    t:=PermList(List([0..7],i->(((i mod 4)+2*QuoInt(i,4)) mod 4)
      +4*((QuoInt(i,4)+1) mod 2)+1));
    Q1:=Group(r,t);
    if Size(Q1)<>8 or r^4<>One(Q1) or t^2<>r^2 or t*r*t^-1<>r^-1 then
      Error("quaternion factor presentation mismatch");
    fi;
  else Error("unsupported direct-product resolution family");fi;
  Q2:=CyclicGroup(IsPermGroup,2);
  R1:=ResolutionFiniteGroup(Q1,depth,false,0,"extendible");
  R2:=ResolutionFiniteGroup(Q2,depth,false,0,"extendible");
  R:=ResolutionFiniteDirectProduct(R1,R2);Q:=GroupOfResolution(R);
  map:=IsomorphismGroups(Q,P);
  if map=fail then Error("direct-product resolution group mismatch");fi;
  R!.elts:=List(R!.elts,x->Image(map,x));R!.group:=P;
  R!.afsDirectProductFamily:=family;
  R!.afsDirectProductTransport:=map;
  R!.afsDirectProductFactorDimensions:=List([R1,R2],
    F->List([0..depth],k->Dimension(F)(k)));
  return R;
end);
