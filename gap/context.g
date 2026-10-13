# Context coefficient actions are immutable. Every cache key includes its action name.
BindGlobal("U1NewContext",function(G,R,s,rho,omega,vcd)
  local c;
  c:=rec(G:=G,R:=R,s:=s,rho:=rho,omega:=omega,vcd:=vcd,
    differentialCache:=rec(),smithCache:=rec(),cohomologyCache:=rec(),f2SolveCache:=rec());
  c.sign:=g->(-1)^s(g);c.bar:=U1Comparison(R);
  return c;
end);
BindGlobal("U1FiniteContext",function(data,depth)
  local n,perms,G,iso,elements,index,c,R,identity;
  n:=Length(data.multiplication);
  if Length(data.s)<>n or Length(data.rho)<>n or Length(data.omega)<>n then Error("Finite input table lengths disagree");fi;
  perms:=List([1..n],i->PermList(List([1..n],j->data.multiplication[j][i]+1)));
  G:=Group(perms);iso:=IsomorphismPcpGroup(G);elements:=List(perms,p->Image(iso,p));G:=Image(iso);
  index:=U1Memo(g->Position(elements,g));
  R:=U1FiniteHolonomyResolution(G,depth);
  c:=U1NewContext(G,R,g->data.s[index(g)],g->data.rho[index(g)],
    function(g,h) return Rat(data.omega[index(g)][index(h)]);end,0);
  c.input:=data;c.elementIndex:=index;
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
  local affine,iso,G,pointMap,pointIndex,R,c;
  LoadPackage("CrystCat");
  affine:=SpaceGroupBBNWZ(2,data.catalog_number);iso:=IsomorphismPcpGroup(affine);G:=Image(iso);
  pointMap:=PointHomomorphism(affine);
  pointIndex:=U1Memo(g->Position(data.matrices,Image(pointMap,PreImageElm(iso,g))));
  if ForAny(GeneratorsOfGroup(G),g->pointIndex(g)=fail) then Error("Wallpaper holonomy does not match catalog matrices");fi;
  R:=U1ResolutionSpaceGroup(iso,depth);
  c:=U1NewContext(G,R,g->data.s[pointIndex(g)],g->data.rho[pointIndex(g)],
    function(g,h) return Rat(data.omega[pointIndex(g)][pointIndex(h)]);end,2);
  c.input:=data;c.affine:=affine;c.iso:=iso;c.pointIndex:=pointIndex;return c;
end);
BindGlobal("U1CatalogContext",function(data,depth)
  if data.family="wallpaper" then return U1WallpaperContext(data,depth);fi;
  return U1FiniteContext(data,depth);
end);
