# HAP finite resolutions can depend strongly on the presentation. Transport
# from standard finite groups when the holonomy is S4 or S4 x C2. This changes
# only the resolution, never the affine space group or its translations.
# HAP's default finite constructor omits the last contraction table. The
# "extendible" option retains it, certifying h through degree depth-1.
BindGlobal("AFSFiniteHolonomyResolution",function(P,depth)
  local id,Q,R,map,R1,R2;
  id:=IdGroup(P);
  if id=[24,12] then
    Q:=SymmetricGroup(4); R:=ResolutionFiniteGroup(Q,depth,false,0,"extendible");
  elif id=[48,48] then
    R1:=ResolutionFiniteGroup(SymmetricGroup(4),depth,false,0,"extendible");
    R2:=ResolutionFiniteGroup(Group((1,2)),depth,false,0,"extendible");
    R:=ResolutionFiniteDirectProduct(R1,R2); Q:=R!.group;
  else return ResolutionFiniteGroup(P,depth,false,0,"extendible");
  fi;
  map:=IsomorphismGroups(Q,P);
  if map=fail then Error("holonomy resolution transport is not isomorphic"); fi;
  R!.elts:=List(R!.elts,x->Image(map,x)); R!.group:=P;
  return R;
end);

# Build the full affine space-group resolution with HAP's extension API.
# The lattice section is chosen in a centered fundamental parallelepiped.
# No classification package or finite quotient replaces the space group.
# Mutable group-element registry. Synchronize with HAP's lazily appended
# elements before each lookup; the dictionary changes only indexing cost.
BindGlobal("AFSElementRegistry",function(elements,grow)
  local reg;
  reg:=rec(elements:=elements,seen:=0,dict:=NewDictionary([1],true));
  reg.sync:=function()
    while reg.seen<Length(reg.elements) do
      reg.seen:=reg.seen+1;
      AddDictionary(reg.dict,AFSKey([reg.elements[reg.seen]]),reg.seen);
    od;
  end;
  reg.index:=function(g)
    local k,i;
    reg.sync(); k:=AFSKey([g]); i:=LookupDictionary(reg.dict,k);
    if i<>fail then return i; fi;
    if grow<>fail then grow(g); reg.sync(); i:=LookupDictionary(reg.dict,k); fi;
    if i=fail then
      Add(reg.elements,g); reg.sync(); i:=LookupDictionary(reg.dict,k);
    fi;
    return i;
  end;
  reg.sync(); return reg;
end);

# Koszul resolution of the translation lattice Z^3. The tensor contraction
# is h1 tensor id tensor id + eta*eps tensor h2 tensor id
# + eta*eps tensor eta*eps tensor h3. Exponents are exact Pcp coordinates;
# there is no search for a power of a lattice generator.
BindGlobal("AFSLatticeResolution",function(L,depth)
  local pc,gens,subsets,elements,registry,dim,boundary,contract,R;
  pc:=Pcp(L,"snf"); gens:=List([1..Length(pc)],i->pc[i]);
  if Length(gens)<>3 or not IsAbelian(L) or ForAny(RelativeOrdersOfPcp(pc),x->x<>0) then
    Error("free rank-three translation lattice expected");
  fi;
  subsets:=List([0..3],k->Combinations([1..3],k));
  elements:=[Identity(L)]; registry:=AFSElementRegistry(elements,fail);
  for R in gens do registry.index(R); registry.index(R^-1); od;
  dim:=function(k) if k<0 or k>3 then return 0; fi; return Length(subsets[k+1]); end;
  boundary:=function(k,i)
    local I,out,j,J,b,sgn;
    if k=0 then return []; fi;
    I:=subsets[k+1][AbsInt(i)]; out:=[];
    for j in [1..k] do
      J:=ShallowCopy(I); Remove(J,j); b:=Position(subsets[k],J);
      sgn:=SignInt(i)*(-1)^(j-1);
      Add(out,[sgn*b,registry.index(gens[I[j]])]); Add(out,[-sgn*b,1]);
    od;
    return out;
  end;
  contract:=function(k,x)
    local I,a,out,limit,j,J,b,tail,l,p,step,start,stop,sgn,g;
    if k<0 then return [[SignInt(x[1]),1]]; fi;
    if k>=3 then return []; fi;
    I:=subsets[k+1][AbsInt(x[1])]; a:=ExponentsByPcp(pc,elements[x[2]]);
    if I=[] then limit:=3; else limit:=Minimum(I)-1; fi;
    out:=[];
    for j in [1..limit] do
      if a[j]=0 then continue; fi;
      J:=Concatenation([j],I); b:=Position(subsets[k+2],J);
      tail:=Identity(L);
      for l in [j+1..3] do tail:=tail*gens[l]^a[l]; od;
      if a[j]>0 then start:=0; stop:=a[j]-1; sgn:=SignInt(x[1]);
      else start:=a[j]; stop:=-1; sgn:=-SignInt(x[1]); fi;
      g:=gens[j]^start*tail;
      for p in [start..stop] do
        Add(out,[sgn*b,registry.index(g)]); g:=g*gens[j];
      od;
    od;
    return out;
  end;
  R:=Objectify(HapResolution,rec(group:=L,dimension:=dim,boundary:=boundary,
    homotopy:=contract,elts:=elements,appendToElts:=function(g) registry.index(g); end,
    afsLatticeGenerators:=gens,
    properties:=[["type","resolution"],["length",depth],["characteristic",0]]));
  return R;
end);

# TTP calls the factor contractions repeatedly on the same translated cells.
# Cache exact words; always return a fresh list of pairs because HAP may mutate.
BindGlobal("AFSMemoResolutionFactor",function(R)
  local rawH,rawD,HC,DC,stats;
  if IsBound(R!.afsFactorCache) then return; fi;
  rawH:=R!.homotopy; rawD:=R!.boundary; HC:=[]; DC:=[];
  stats:=rec(hits:=0,misses:=0); R!.afsFactorCache:=stats;
  R!.homotopy:=function(k,x)
    local key,v,out;
    if not IsBound(HC[k+1]) then HC[k+1]:=NewDictionary([1,1],true); fi;
    key:=[AbsInt(x[1]),x[2]]; v:=LookupDictionary(HC[k+1],key);
    if v=fail then
      v:=List(rawH(k,key),ShallowCopy); AddDictionary(HC[k+1],key,v);
      stats.misses:=stats.misses+1;
    else stats.hits:=stats.hits+1; fi;
    if x[1]<0 then return List(v,t->[-t[1],t[2]]); fi;
    return List(v,ShallowCopy);
  end;
  R!.boundary:=function(k,i)
    local v;
    if not IsBound(DC[k+1]) then DC[k+1]:=[]; fi;
    if not IsBound(DC[k+1][AbsInt(i)]) then
      DC[k+1][AbsInt(i)]:=List(rawD(k,AbsInt(i)),ShallowCopy);
    fi;
    v:=DC[k+1][AbsInt(i)];
    if i<0 then return List(v,t->[-t[1],t[2]]); fi;
    return List(v,ShallowCopy);
  end;
end);

BindGlobal("AFSExtensionResolution",function(h,RL,RP,section)
  local G,E,er,lr,pr,gn,grow,R;
  AFSMemoResolutionFactor(RL); AFSMemoResolutionFactor(RP);
  G:=Source(h); E:=[Identity(G)];
  for gn in GeneratorsOfGroup(G) do
    if not gn in E then Add(E,gn); fi;
    if not gn^-1 in E then Add(E,gn^-1); fi;
  od;
  er:=AFSElementRegistry(E,fail); grow:=fail;
  if IsBound(RL!.appendToElts) then grow:=RL!.appendToElts; fi;
  lr:=AFSElementRegistry(RL!.elts,grow);
  pr:=AFSElementRegistry(RP!.elts,fail);
  R:=TwistedTensorProduct(RP,RL,
    i->pr.index(Image(h,E[i])),
    i->er.index(section(RP!.elts[i])),
    i->er.index(RL!.elts[i]),
    i->lr.index(E[i]),E,
    function(i,j) return er.index(E[i]*E[j]); end,
    i->er.index(E[i]^-1));
  R!.group:=G; R!.afsFactorStats:=[RP!.afsFactorCache,RL!.afsFactorCache];
  R!.afsFactors:=rec(point:=RP,lattice:=RL,quotient:=h,section:=section,
    pointIndex:=pr.index,latticeIndex:=lr.index);
  R!.appendToElts:=function(g) er.index(g); end;
  return R;
end);

BindGlobal("AFSResolutionSpaceGroup",function(iso,depth)
  local G,h,P,L,RP,RL,basis,invbasis,lattice,section,pe,pg,lift,v,i,lookup,t,timing,R;
  G:=Image(iso); timing:=rec(); t:=Runtime();
  Print("AFS_BUILD holonomy_start cpu_ms=",Runtime(),"\n");
  if not IsAlmostCrystallographic(G) then Error("affine group expected"); fi;
  h:=NaturalHomomorphismOnHolonomyGroup(G); P:=Image(h); L:=Kernel(h);
  Print("AFS_BUILD RP_start order=",Size(P)," cpu_ms=",Runtime(),"\n");
  if Size(P)=1 then return ResolutionNilpotentGroup(G,depth); fi;
  timing.holonomy_ms:=Runtime()-t; t:=Runtime();
  RP:=AFSFiniteHolonomyResolution(P,depth); timing.RP_ms:=Runtime()-t; t:=Runtime();
  Print("AFS_BUILD RL_start cpu_ms=",Runtime(),"\n");
  if IsBound(AFS_USE_KOSZUL) and AFS_USE_KOSZUL then RL:=AFSLatticeResolution(L,depth);
  else RL:=ResolutionNilpotentGroup(L,depth); fi;
  timing.RL_ms:=Runtime()-t; t:=Runtime();
  Print("AFS_BUILD section_start cpu_ms=",Runtime(),"\n");
  if IsBound(RL!.afsLatticeGenerators) then lattice:=RL!.afsLatticeGenerators;
  else lattice:=GeneratorsOfGroup(L); fi;
  basis:=List(lattice,x->PreImageElm(iso,x)[4]{[1..3]});
  if Length(basis)<>3 or RankMat(basis)<>3 then Error("rank-three lattice expected"); fi;
  invbasis:=Inverse(basis); pe:=Elements(P); section:=[];
  for pg in pe do
    lift:=PreImagesRepresentative(h,pg);
    v:=PreImageElm(iso,lift)[4]{[1..3]}*invbasis;
    for i in [1..3] do lift:=lift*lattice[i]^(-AFSFloor(v[i]+1/2)); od;
    if Image(h,lift)<>pg then Error("section projection failed"); fi;
    Add(section,lift);
  od;
  lookup:=x->section[Position(pe,x)];
  timing.section_ms:=Runtime()-t; t:=Runtime();
  Print("AFS_BUILD extension_start cpu_ms=",Runtime(),"\n");
  R:=AFSExtensionResolution(h,RL,RP,lookup); timing.extension_ms:=Runtime()-t;
  R!.afsTimings:=timing;
  Print("AFS_BUILD extension_done timings=",timing,"\n");
  return R;
end);
