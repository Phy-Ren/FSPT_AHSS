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
