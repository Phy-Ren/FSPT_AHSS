# Context coefficient actions are immutable. Every cache key includes its action name.
BindGlobal("U1NewContext",function(G,R,s,r,omega,vcd)
  local c;
  c:=rec(G:=G,R:=R,s:=s,r:=r,rho:=g->(r(g)+s(g)) mod 2,omega:=omega,vcd:=vcd,
    differentialCache:=rec(),smithCache:=rec(),cohomologyCache:=rec(),f2SolveCache:=rec());
  c.sign:=g->(-1)^s(g);c.bar:=U1Comparison(R);
  return c;
end);

# Primitive 3-cell charge is the alternating six-term translation bar cycle.
# On translations r=s=omega=0; consequently this restriction is additive
# even for completed CI roots with globally nonclosed integer charge.
BindGlobal("U1SpaceGroupFilling",function(c,result)
  local L,pc,basis,vectors,volume,tmp,states,fillings,perms,perm,state,value,i,rel,
    np,nq,chargeFillings,ciFillings,step,chargeStep,nonzero;
  if c.vcd<>3 or not IsBound(c.affine) then Error("Primitive volume filling requires the full rank-three affine group");fi;
  L:=Kernel(NaturalHomomorphismOnHolonomyGroup(c.G));pc:=Pcp(L,"snf");
  if Length(pc)<>3 or not IsAbelian(L) or RelativeOrdersOfPcp(pc)<>[0,0,0] then Error("Translation kernel is not Z^3");fi;
  basis:=List([1..3],i->pc[i]);
  if Subgroup(c.G,basis)<>L then Error("Translation basis is not primitive");fi;
  vectors:=List(basis,g->PreImageElm(c.iso,g)[4]{[1..3]});volume:=DeterminantMat(vectors);
  if volume=0 then Error("Translation basis has zero volume");fi;
  if volume<0 then
    tmp:=basis[1];basis[1]:=basis[2];basis[2]:=tmp;
    tmp:=vectors[1];vectors[1]:=vectors[2];vectors[2]:=tmp;volume:=-volume;
  fi;
  if ForAny(basis,g->c.s(g)<>0 or c.r(g)<>0)
    or ForAny(basis,g->ForAny(basis,h->c.omega(g,h)<>0)) then Error("Translation background is not normalized trivial");fi;
  perms:=PermutationsList([1,2,3]);
  states:=Concatenation(c.classificationStates.charge,c.classificationStates.sheet);
  fillings:=List(c.classificationStates.phase,x->0);
  for state in states do
    value:=Sum(perms,p->SignPerm(PermList(p))*CallFuncList(state.charge,List(p,i->basis[i])));
    if not IsInt(value) then Error("Primitive translation-cell charge is not integral");fi;
    Add(fillings,value);
  od;
  if Length(fillings)<>result.presentationGeneratorCount then Error("Filling/presentation dimensions disagree");fi;
  for rel in result.presentation do
    if Sum([1..Length(fillings)],i->rel[i]*fillings[i])<>0 then Error("A complete relation changes primitive-cell filling");fi;
  od;
  np:=Length(c.classificationStates.phase);nq:=Length(c.classificationStates.charge);
  chargeFillings:=fillings{[np+1..np+nq]};ciFillings:=fillings{[np+nq+1..Length(fillings)]};
  step:=0;nonzero:=Filtered(fillings,x->x<>0);if nonzero<>[] then step:=Gcd(List(nonzero,AbsInt));fi;
  chargeStep:=0;nonzero:=Filtered(chargeFillings,x->x<>0);if nonzero<>[] then chargeStep:=Gcd(List(nonzero,AbsInt));fi;
  return rec(primitiveTranslationVectors:=vectors,primitiveCellVolume:=volume,
    orientation:="positive determinant in catalog affine coordinates",
    barCycle:="sum over permutations sign(p) [t_p1|t_p2|t_p3]",
    generatorFillings:=fillings,fillingStep:=step,
    chargeRootSubgroupGeneratorFillings:=chargeFillings,chargeRootSubgroupFillingStep:=chargeStep,
    ciGeneratorFillings:=ciFillings,primitiveBasisGeneratesFullTranslationKernel:=true,
    allPresentationRelationsHaveZeroFilling:=true,
    convention:="integer charge per primitive translation 3-cell, with actual completed CI contributions retained");
end);
# Canonical v2 inputs name charge reversal r and circle action rho.
# Legacy interpretation is opt-in and never mutates the supplied record.
BindGlobal("U1MigrateLegacyInput",function(data)
  local out;
  if IsBound(data.r) or (IsBound(data.schema_version) and (not IsInt(data.schema_version) or data.schema_version<>1)) then
    Error("Input is not an unambiguous legacy charge-rho record");fi;
  if IsBound(data.notation) and data.notation<>"legacy-charge-rho" then Error("Unknown legacy notation tag");fi;
  if Length(data.s)<>Length(data.rho) or not ForAll(Concatenation(data.s,data.rho),x->IsInt(x) and x in [0,1]) then Error("Legacy signs must be equal-length bit arrays");fi;
  out:=ShallowCopy(data);out.r:=ShallowCopy(data.rho);
  out.rho:=List([1..Length(out.s)],i->(out.s[i]+out.r[i]) mod 2);
  if IsBound(out.circle_action) and out.circle_action<>out.rho then Error("Legacy circle_action disagrees with its characters");fi;
  out.schema_version:=2;
  if IsBound(out.notation) then Unbind(out.notation);fi;
  return out;
end);
BindGlobal("U1CanonicalInput",function(data)
  local out,expected;
  if not IsBound(data.schema_version) and IsBound(data.s) and IsBound(data.r) then
    data:=ShallowCopy(data);data.schema_version:=2;fi;
  if IsBound(data.schema_version) and data.schema_version=1 then
    if not IsBound(data.notation) or data.notation<>"legacy-charge-rho" then
      Error("schema_version=1 requires notation=legacy-charge-rho");fi;
    data:=U1MigrateLegacyInput(data);
  fi;
  if not IsBound(data.schema_version) or not IsInt(data.schema_version) or data.schema_version<>2 or not IsBound(data.r) or not IsBound(data.s) then
    Error("Use schema_version=2 with s,r,rho; explicitly migrate legacy charge-rho inputs");fi;
  if Length(data.s)<>Length(data.r) or not ForAll(Concatenation(data.s,data.r),x->IsInt(x) and x in [0,1]) then
    Error("s and r must be equal-length bit arrays");fi;
  expected:=List([1..Length(data.s)],i->(data.s[i]+data.r[i]) mod 2);
  if IsBound(data.rho) and data.rho<>expected then Error("rho must equal r+s modulo two");fi;
  if IsBound(data.circle_action) and data.circle_action<>expected then Error("circle_action disagrees with rho");fi;
  out:=ShallowCopy(data);out.rho:=expected;return out;
end);
# Exhaustive exact validation of finite multiplication and twisted extension.
BindGlobal("U1ValidateFiniteInput",function(data)
  local n,one,i,j,k,ij,jk,w,t;
  data:=U1CanonicalInput(data);n:=Length(data.multiplication);one:=data.identity_index+1;
  if not one in [1..n] or Length(data.s)<>n or Length(data.r)<>n or Length(data.omega)<>n then Error("Finite input table lengths disagree");fi;
  if not ForAll(Concatenation(data.s,data.r),x->x in [0,1]) then Error("Sign characters must contain bits");fi;
  if data.s[one]<>0 or data.r[one]<>0 then Error("Sign character is not normalized");fi;
  w:=List(data.omega,row->List(row,Rat));
  for i in [1..n] do
    if Set(data.multiplication[i])<>[0..n-1] or Length(w[i])<>n then Error("Finite table row is not a permutation");fi;
    if data.multiplication[one][i]<>i-1 or data.multiplication[i][one]<>i-1 or w[one][i]<>0 or w[i][one]<>0 then Error("Finite input identity or extension is not normalized");fi;
    for j in [1..n] do
      ij:=data.multiplication[i][j]+1;
      if data.s[ij]<>(data.s[i]+data.s[j]) mod 2 or data.r[ij]<>(data.r[i]+data.r[j]) mod 2 then Error("Input sign is not a group character");fi;
      for k in [1..n] do
        jk:=data.multiplication[j][k]+1;
        if data.multiplication[ij][k]<>data.multiplication[i][jk] then Error("Finite multiplication is not associative");fi;
        t:=(-1)^data.rho[i]*w[j][k]-w[ij][k]+w[i][jk]-w[i][j];
        if not IsInt(t) then Error("Real extension lift is not a twisted U1 cocycle");fi;
      od;
    od;
  od;
  return rec(groupOrder:=n,associativityTriples:=n^3,twistedExtensionTriples:=n^3,independentCharactersChecked:=true);
end);

BindGlobal("U1FiniteContext",function(data,depth)
  local n,perms,G,iso,elements,index,c,R,identity,validation;
  data:=U1CanonicalInput(data);validation:=U1ValidateFiniteInput(data);n:=Length(data.multiplication);
  perms:=List([1..n],i->PermList(List([1..n],j->data.multiplication[j][i]+1)));
  G:=Group(perms);iso:=IsomorphismPcpGroup(G);elements:=List(perms,p->Image(iso,p));G:=Image(iso);
  index:=U1Memo(g->Position(elements,g));
  R:=U1FiniteHolonomyResolution(G,depth);
  c:=U1NewContext(G,R,g->data.s[index(g)],g->data.r[index(g)],
    function(g,h) return Rat(data.omega[index(g)][index(h)]);end,0);
  c.input:=data;c.elementIndex:=index;c.inputValidation:=validation;
  c.backgroundClosureCertificate:=rec(actions:=[c.s,c.r,c.omega],integralTwistedCoboundary:=true,
    halfIntegralOmega:=ForAll(Concatenation(data.omega),x->IsInt(2*Rat(x))));
  return c;
end);
BindGlobal("U1CyclicContext",function(n,sbit,rbit,extension)
  local G,g,R,s,r,omega,c;
  if not IsInt(n) or n<1 or not sbit in [0,1] or not rbit in [0,1] then Error("Invalid cyclic group or character");fi;
  if n mod 2=1 and (sbit<>0 or rbit<>0) then Error("An odd cyclic group has no nontrivial sign character");fi;
  if not IsRat(extension) then Error("Extension lift must be exact rational");fi;
  if (sbit+rbit) mod 2=1 and not IsInt(2*extension) then Error("Signed cyclic extension must be fixed modulo integers");fi;
  if n=1 and extension<>0 then Error("The trivial group has normalized zero extension");fi;
  if n=1 then G:=Group(());else G:=CyclicGroup(IsPcpGroup,n);fi;g:=GeneratorsOfGroup(G);
  if n=1 then s:=U1Zero;r:=U1Zero;omega:=U1Zero;
  else
    g:=g[1];
    # Pcp exponents avoid dependence on free-word representations.
    s:=x->(x!.exponents[1]*sbit) mod 2;
    r:=x->(x!.exponents[1]*rbit) mod 2;
    omega:=function(x,y) return extension*QuoInt(x!.exponents[1]+y!.exponents[1],n);end;
  fi;
  R:=U1FiniteHolonomyResolution(G,7);c:=U1NewContext(G,R,s,r,omega,0);
  c.backgroundClosureCertificate:=rec(actions:=[c.s,c.r,c.omega],integralTwistedCoboundary:=true,
    halfIntegralOmega:=IsInt(2*extension));return c;
end);
BindGlobal("U1AffineContext",function(data,depth)
  local affine,iso,G,pointMap,pointIndex,R,c,validation,matrices,expected;
  LoadPackage("CrystCat");data:=U1CanonicalInput(data);validation:=U1ValidateFiniteInput(data);
  if not data.dimension in [2,3] then Error("Only rank-two and rank-three affine groups are supported");fi;
  affine:=SpaceGroupBBNWZ(data.dimension,data.catalog_number);
  if IsBound(data.affine_generators) then
    expected:=List(data.affine_generators,m->List(m,row->List(row,Rat)));
    if GeneratorsOfGroup(affine)<>expected then Error("Affine generators do not match the immutable catalog input");fi;
  fi;
  iso:=IsomorphismPcpGroup(affine);G:=Image(iso);
  pointMap:=PointHomomorphism(affine);
  matrices:=List(data.matrices,m->List(m,row->List(row,Rat)));
  pointIndex:=U1Memo(g->Position(matrices,Image(pointMap,PreImageElm(iso,g))));
  if ForAny(GeneratorsOfGroup(G),g->pointIndex(g)=fail) then Error("Affine holonomy does not match catalog matrices");fi;
  R:=U1ResolutionSpaceGroup(iso,depth);
  c:=U1NewContext(G,R,g->data.s[pointIndex(g)],g->data.r[pointIndex(g)],
    function(g,h) return Rat(data.omega[pointIndex(g)][pointIndex(h)]);end,data.dimension);
  c.input:=data;c.inputValidation:=validation;c.affine:=affine;c.iso:=iso;c.pointIndex:=pointIndex;
  c.backgroundClosureCertificate:=rec(actions:=[c.s,c.r,c.omega],integralTwistedCoboundary:=true,
    halfIntegralOmega:=ForAll(Concatenation(data.omega),x->IsInt(2*Rat(x))));return c;
end);
BindGlobal("U1WallpaperContext",U1AffineContext);
BindGlobal("U1CatalogContext",function(data,depth)
  if data.family in ["wallpaper","spacegroup"] then return U1AffineContext(data,depth);fi;
  return U1FiniteContext(data,depth);
end);
# Paired physical spins share only geometry and identical coefficient actions.
# Formula/source cochain caches remain attached to their new context. The worker
# may be shared because every request contains its full exact signs/background/
# lower cochains and the worker cache is keyed by that complete request content.
BindGlobal("U1SiblingContext",function(previous,data)
  local c,validation,index;
  data:=U1CanonicalInput(data);
  if not IsBound(previous.input) then Error("Sibling reuse requires catalog input");fi;
  if data.family<>previous.input.family or data.index<>previous.input.index
    or data.dimension<>previous.input.dimension or data.matrices<>previous.input.matrices
    or data.multiplication<>previous.input.multiplication or data.s<>previous.input.s
    or data.r<>previous.input.r then Error("Sibling group or coefficient actions changed");fi;
  if IsBound(previous.affine) and data.affine_generators<>previous.input.affine_generators then
    Error("Sibling affine extension geometry changed");fi;
  validation:=U1ValidateFiniteInput(data);
  if IsBound(previous.pointIndex) then index:=previous.pointIndex;else index:=previous.elementIndex;fi;
  c:=U1NewContext(previous.G,previous.R,previous.s,previous.r,
    function(g,h) return Rat(data.omega[index(g)][index(h)]);end,previous.vcd);
  c.bar:=previous.bar;c.differentialCache:=previous.differentialCache;
  c.smithCache:=previous.smithCache;c.cohomologyCache:=previous.cohomologyCache;
  c.f2SolveCache:=previous.f2SolveCache;c.input:=data;c.inputValidation:=validation;
  c.backgroundClosureCertificate:=rec(actions:=[c.s,c.r,c.omega],integralTwistedCoboundary:=true,
    halfIntegralOmega:=ForAll(Concatenation(data.omega),x->IsInt(2*Rat(x))));
  if IsBound(previous.affine) then
    c.affine:=previous.affine;c.iso:=previous.iso;c.pointIndex:=previous.pointIndex;
  else c.elementIndex:=previous.elementIndex;fi;
  if IsBound(previous.worker) then c.worker:=previous.worker;c.workerCalls:=0;fi;
  c.pairedGeometryReuse:=true;return c;
end);
# Physical filling is the restriction to the full primitive translation kernel,
# evaluated on its oriented fundamental bar two-cycle [tx|ty]-[ty|tx].
BindGlobal("U1WallpaperFilling",function(c,result)
  local holonomy,L,pc,basis,vectors,area,tmp,states,fillings,values,g,h,i,rel,nphase,ncharge,chargeFillings,ciFillings,chargeStep;
  if c.vcd<>2 or not IsBound(c.affine) then Error("Wallpaper filling requires the full affine context");fi;
  holonomy:=NaturalHomomorphismOnHolonomyGroup(c.G);L:=Kernel(holonomy);pc:=Pcp(L,"snf");
  if Length(pc)<>2 or not IsAbelian(L) or RelativeOrdersOfPcp(pc)<>[0,0] then Error("Wallpaper translation kernel is not free abelian of rank two");fi;
  basis:=[pc[1],pc[2]];
  if Subgroup(c.G,basis)<>L then Error("Translation basis does not generate the full kernel");fi;
  vectors:=List(basis,g->PreImageElm(c.iso,g)[3]{[1,2]});area:=DeterminantMat(vectors);
  if area=0 then Error("Translation basis is not geometrically independent");fi;
  if area<0 then tmp:=basis[1];basis[1]:=basis[2];basis[2]:=tmp;vectors:=Reversed(vectors);area:=-area;fi;
  g:=basis[1];h:=basis[2];
  if g*h<>h*g or c.s(g)<>0 or c.s(h)<>0 or c.r(g)<>0 or c.r(h)<>0 then Error("Translation orientation/charge action failed");fi;
  states:=Concatenation(c.classificationStates.charge,c.classificationStates.sheet);
  fillings:=List(c.classificationStates.phase,x->0);
  for tmp in states do
    i:=tmp.charge(g,h)-tmp.charge(h,g);
    if not IsInt(i) then Error("Primitive translation filling is not integral");fi;
    Add(fillings,i);
  od;
  if Length(fillings)<>result.presentationGeneratorCount then Error("Filling and presentation generators disagree");fi;
  for rel in result.presentation do
    if Sum([1..Length(fillings)],i->rel[i]*fillings[i])<>0 then Error("A stacking/gauge relation changed physical filling");fi;
  od;
  values:=Filtered(fillings,x->x<>0);i:=0;if values<>[] then i:=Gcd(List(values,AbsInt));fi;
  nphase:=Length(c.classificationStates.phase);ncharge:=Length(c.classificationStates.charge);
  chargeFillings:=fillings{[nphase+1..nphase+ncharge]};ciFillings:=fillings{[nphase+ncharge+1..Length(fillings)]};
  chargeStep:=0;values:=Filtered(chargeFillings,x->x<>0);if values<>[] then chargeStep:=Gcd(List(values,AbsInt));fi;
  return rec(primitiveTranslationVectors:=vectors,primitiveCellArea:=area,
    chargeRootSubgroupGeneratorFillings:=chargeFillings,chargeRootSubgroupFillingStep:=chargeStep,
    ciGeneratorFillings:=ciFillings,
    primitiveBasisGeneratesFullTranslationKernel:=true,orientation:="positive determinant in catalog affine coordinates",
    barCycle:="[tx|ty]-[ty|tx]",generatorFillings:=fillings,fillingStep:=i,
    allPresentationRelationsHaveZeroFilling:=true,
    convention:="localized integer charge per primitive translation cell; uniform IQH scope recorded separately");
end);
