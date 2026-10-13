# Context coefficient actions are immutable. Every cache key includes its action name.
BindGlobal("U1NewContext",function(G,R,s,rho,omega,vcd)
  local c;
  c:=rec(G:=G,R:=R,s:=s,rho:=rho,omega:=omega,vcd:=vcd,
    differentialCache:=rec(),smithCache:=rec(),cohomologyCache:=rec(),f2SolveCache:=rec());
  c.sign:=g->(-1)^s(g);c.bar:=U1Comparison(R);
  return c;
end);
# Exhaustive exact validation of finite multiplication and twisted extension.
BindGlobal("U1ValidateFiniteInput",function(data)
  local n,one,i,j,k,ij,jk,w,t;
  n:=Length(data.multiplication);one:=data.identity_index+1;
  if not one in [1..n] or Length(data.s)<>n or Length(data.rho)<>n or Length(data.omega)<>n then Error("Finite input table lengths disagree");fi;
  if not ForAll(Concatenation(data.s,data.rho),x->x in [0,1]) then Error("Sign characters must contain bits");fi;
  if data.s[one]<>0 or data.rho[one]<>0 then Error("Sign character is not normalized");fi;
  w:=List(data.omega,row->List(row,Rat));
  for i in [1..n] do
    if Set(data.multiplication[i])<>[0..n-1] or Length(w[i])<>n then Error("Finite table row is not a permutation");fi;
    if data.multiplication[one][i]<>i-1 or data.multiplication[i][one]<>i-1 or w[one][i]<>0 or w[i][one]<>0 then Error("Finite input identity or extension is not normalized");fi;
    for j in [1..n] do
      ij:=data.multiplication[i][j]+1;
      if data.s[ij]<>(data.s[i]+data.s[j]) mod 2 or data.rho[ij]<>(data.rho[i]+data.rho[j]) mod 2 then Error("Input sign is not a group character");fi;
      for k in [1..n] do
        jk:=data.multiplication[j][k]+1;
        if data.multiplication[ij][k]<>data.multiplication[i][jk] then Error("Finite multiplication is not associative");fi;
        t:=(-1)^(data.s[i]+data.rho[i])*w[j][k]-w[ij][k]+w[i][jk]-w[i][j];
        if not IsInt(t) then Error("Real extension lift is not a twisted U1 cocycle");fi;
      od;
    od;
  od;
  return rec(groupOrder:=n,associativityTriples:=n^3,twistedExtensionTriples:=n^3,independentCharactersChecked:=true);
end);

BindGlobal("U1FiniteContext",function(data,depth)
  local n,perms,G,iso,elements,index,c,R,identity,validation;
  validation:=U1ValidateFiniteInput(data);n:=Length(data.multiplication);
  perms:=List([1..n],i->PermList(List([1..n],j->data.multiplication[j][i]+1)));
  G:=Group(perms);iso:=IsomorphismPcpGroup(G);elements:=List(perms,p->Image(iso,p));G:=Image(iso);
  index:=U1Memo(g->Position(elements,g));
  R:=U1FiniteHolonomyResolution(G,depth);
  c:=U1NewContext(G,R,g->data.s[index(g)],g->data.rho[index(g)],
    function(g,h) return Rat(data.omega[index(g)][index(h)]);end,0);
  c.input:=data;c.elementIndex:=index;c.inputValidation:=validation;
  return c;
end);
BindGlobal("U1CyclicContext",function(n,sbit,rbit,extension)
  local G,g,R,s,rho,omega,c;
  if not IsInt(n) or n<1 or not sbit in [0,1] or not rbit in [0,1] then Error("Invalid cyclic group or character");fi;
  if n mod 2=1 and (sbit<>0 or rbit<>0) then Error("An odd cyclic group has no nontrivial sign character");fi;
  if not IsRat(extension) then Error("Extension lift must be exact rational");fi;
  if (sbit+rbit) mod 2=1 and not IsInt(2*extension) then Error("Signed cyclic extension must be fixed modulo integers");fi;
  if n=1 and extension<>0 then Error("The trivial group has normalized zero extension");fi;
  if n=1 then G:=Group(());else G:=CyclicGroup(IsPcpGroup,n);fi;g:=GeneratorsOfGroup(G);
  if n=1 then s:=U1Zero;rho:=U1Zero;omega:=U1Zero;
  else
    g:=g[1];
    # Pcp exponents avoid dependence on free-word representations.
    s:=x->(x!.exponents[1]*sbit) mod 2;
    rho:=x->(x!.exponents[1]*rbit) mod 2;
    omega:=function(x,y) return extension*QuoInt(x!.exponents[1]+y!.exponents[1],n);end;
  fi;
  R:=U1FiniteHolonomyResolution(G,7);c:=U1NewContext(G,R,s,rho,omega,0);return c;
end);
BindGlobal("U1WallpaperContext",function(data,depth)
  local affine,iso,G,pointMap,pointIndex,R,c,validation;
  LoadPackage("CrystCat");validation:=U1ValidateFiniteInput(data);
  affine:=SpaceGroupBBNWZ(2,data.catalog_number);iso:=IsomorphismPcpGroup(affine);G:=Image(iso);
  pointMap:=PointHomomorphism(affine);
  pointIndex:=U1Memo(g->Position(data.matrices,Image(pointMap,PreImageElm(iso,g))));
  if ForAny(GeneratorsOfGroup(G),g->pointIndex(g)=fail) then Error("Wallpaper holonomy does not match catalog matrices");fi;
  R:=U1ResolutionSpaceGroup(iso,depth);
  c:=U1NewContext(G,R,g->data.s[pointIndex(g)],g->data.rho[pointIndex(g)],
    function(g,h) return Rat(data.omega[pointIndex(g)][pointIndex(h)]);end,2);
  c.input:=data;c.inputValidation:=validation;c.affine:=affine;c.iso:=iso;c.pointIndex:=pointIndex;return c;
end);
BindGlobal("U1CatalogContext",function(data,depth)
  if data.family="wallpaper" then return U1WallpaperContext(data,depth);fi;
  return U1FiniteContext(data,depth);
end);
# Physical filling is the restriction to the full primitive translation kernel,
# evaluated on its oriented fundamental bar two-cycle [tx|ty]-[ty|tx].
BindGlobal("U1WallpaperFilling",function(c,result)
  local holonomy,L,pc,basis,vectors,area,tmp,states,fillings,values,g,h,i,rel;
  if c.vcd<>2 or not IsBound(c.affine) then Error("Wallpaper filling requires the full affine context");fi;
  holonomy:=NaturalHomomorphismOnHolonomyGroup(c.G);L:=Kernel(holonomy);pc:=Pcp(L,"snf");
  if Length(pc)<>2 or not IsAbelian(L) or RelativeOrdersOfPcp(pc)<>[0,0] then Error("Wallpaper translation kernel is not free abelian of rank two");fi;
  basis:=[pc[1],pc[2]];
  if Subgroup(c.G,basis)<>L then Error("Translation basis does not generate the full kernel");fi;
  vectors:=List(basis,g->PreImageElm(c.iso,g)[3]{[1,2]});area:=DeterminantMat(vectors);
  if area=0 then Error("Translation basis is not geometrically independent");fi;
  if area<0 then tmp:=basis[1];basis[1]:=basis[2];basis[2]:=tmp;vectors:=Reversed(vectors);area:=-area;fi;
  g:=basis[1];h:=basis[2];
  if g*h<>h*g or c.s(g)<>0 or c.s(h)<>0 or c.rho(g)<>0 or c.rho(h)<>0 then Error("Translation orientation/charge action failed");fi;
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
  return rec(primitiveTranslationVectors:=vectors,primitiveCellArea:=area,
    primitiveBasisGeneratesFullTranslationKernel:=true,orientation:="positive determinant in catalog affine coordinates",
    barCycle:="[tx|ty]-[ty|tx]",generatorFillings:=fillings,fillingStep:=i,
    allPresentationRelationsHaveZeroFilling:=true,
    convention:="localized integer charge per primitive translation cell; uniform IQH scope recorded separately");
end);
