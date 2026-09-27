# Independent comparison maps between a HAP resolution C and normalized bar B.
# Recurrences use the contracting homotopies: F=s_B F d_C, G=s_C G d_B,
# and h=s_B(FG-id-h d_B), so d_B h+h d_B=FG-id.
# Bar terms [integer, leading group element, tuple]; native terms [integer,
# basis index, group element]. All caches belong to the current context.
BindGlobal("AFSComparison",function(R)
  local b;
  b:=rec(R:=R,G:=GroupOfResolution(R),F:=[],Gcache:=[],H:=[],hc:=[],ids:=NewDictionary([1],true));
  b.one:=Identity(b.G); b.F[1]:=[[[1,b.one,[]]]]; b.idsSeen:=0;
  b.syncIds:=function()
    while b.idsSeen<Length(b.R!.elts) do
      b.idsSeen:=b.idsSeen+1;
      AddDictionary(b.ids,AFSKey([b.R!.elts[b.idsSeen]]),b.idsSeen);
    od;
  end;
  b.syncIds(); return b;
end);

BindGlobal("AFSCombineChain",function(terms,bar)
  local out,d,t,key,p;
  out:=[]; d:=NewDictionary([1],true);
  for t in terms do
    if t[1]=0 then continue; fi;
    if bar then key:=AFSKey(Concatenation([t[2]],t[3]));
    else key:=Concatenation([t[2]],AFSKey([t[3]])); fi;
    p:=LookupDictionary(d,key);
    if p=fail then Add(out,ShallowCopy(t)); AddDictionary(d,key,Length(out));
    else out[p][1]:=out[p][1]+t[1]; fi;
  od;
  return Filtered(out,t->t[1]<>0);
end);
BindGlobal("AFSBarContract",function(b,terms)
  return List(Filtered(terms,t->t[2]<>b.one),
    t->[t[1],b.one,Concatenation([t[2]],t[3])]);
end);
# Cache the reduced contraction of each translated native cell, not just
# HAP's raw word. The higher diagonal repeatedly asks for these same cells.
BindGlobal("AFSContractCell",function(b,k,i,g)
  local id,key,v,x,terms;
  if not IsBound(b.cellHCache) then b.cellHCache:=[]; fi;
  if not IsBound(b.cellHCache[k+1]) then b.cellHCache[k+1]:=NewDictionary([1],true); fi;
  b.syncIds(); key:=AFSKey([g]); id:=LookupDictionary(b.ids,key);
  if id=fail then
    Add(b.R!.elts,g); b.syncIds(); id:=LookupDictionary(b.ids,key);
  fi;
  key:=[i,id]; v:=LookupDictionary(b.cellHCache[k+1],key);
  if v=fail then
    terms:=List(b.R!.homotopy(k,[i,id]),x->[SignInt(x[1]),AbsInt(x[1]),b.R!.elts[x[2]]]);
    v:=AFSCombineChain(terms,false); AddDictionary(b.cellHCache[k+1],key,v);
  fi;
  return v;
end);
BindGlobal("AFSNativeContract",function(b,k,terms)
  local out,t,x;
  if terms=[] then return []; fi;
  if Length(terms)=1 and terms[1][1]=1 then
    return AFSContractCell(b,k,terms[1][2],terms[1][3]);
  fi;
  out:=[];
  for t in terms do
    for x in AFSContractCell(b,k,t[2],t[3]) do
      Add(out,[t[1]*x[1],x[2],x[3]]);
    od;
  od;
  return AFSCombineChain(out,false);
end);
DeclareGlobalFunction("AFSChainToBar");
BindGlobal("AFSChainToBarCombination",function(b,k,z)
  local boundary,terms,i,w,t,g;
  if k=0 then
    if z=[] or z[1]=0 then return []; fi;
    return [[z[1],b.one,[]]];
  fi;
  boundary:=[];
  for i in [1..Length(z)] do
    if z[i]<>0 then
      for w in BoundaryMap(b.R)(k,i) do
        Add(boundary,[z[i]*SignInt(w[1]),AbsInt(w[1]),b.R!.elts[w[2]]]);
      od;
    fi;
  od;
  terms:=[];
  for w in AFSCombineChain(boundary,false) do
    if w[3]=b.one then continue; fi;
    for t in AFSChainToBar(b,k-1,w[2]) do
      Add(terms,[w[1]*t[1],w[3]*t[2],t[3]]);
    od;
  od;
  return AFSBarContract(b,AFSCombineChain(terms,true));
end);
InstallGlobalFunction(AFSChainToBar,function(b,k,i)
  local terms,w,t,g;
  if not IsBound(b.F[k+1]) then b.F[k+1]:=[]; fi;
  if not IsBound(b.F[k+1][i]) then
    terms:=[];
    for w in BoundaryMap(b.R)(k,i) do
      g:=b.R!.elts[w[2]];
      if g=b.one then continue; fi;
      for t in AFSChainToBar(b,k-1,AbsInt(w[1])) do
        Add(terms,[SignInt(w[1])*t[1],g*t[2],t[3]]);
      od;
    od;
    b.F[k+1][i]:=AFSCombineChain(AFSBarContract(b,terms),true);
  fi;
  return b.F[k+1][i];
end);
DeclareGlobalFunction("AFSChainFromBar");
BindGlobal("AFSContractFromBar",function(b,xs)
  local k,key,val;
  k:=Length(xs);
  if not IsBound(b.HGcache) then b.HGcache:=[]; fi;
  if not IsBound(b.HGcache[k+1]) then b.HGcache[k+1]:=NewDictionary([1],true); fi;
  key:=AFSKey(xs); val:=LookupDictionary(b.HGcache[k+1],key);
  if val=fail then
    val:=AFSNativeContract(b,k,AFSChainFromBar(b,xs));
    AddDictionary(b.HGcache[k+1],key,val);
  fi;
  return val;
end);
InstallGlobalFunction(AFSChainFromBar,function(b,xs)
  local k,key,val,terms,w,t,contracted;
  k:=Length(xs);
  if b.one in xs then return []; fi;
  if k=0 then return [[1,1,b.one]]; fi;
  if not IsBound(b.Gcache[k+1]) then b.Gcache[k+1]:=NewDictionary([1],true); fi;
  key:=AFSKey(xs); val:=LookupDictionary(b.Gcache[k+1],key);
  if val=fail then
    terms:=[];
    for w in AFSBarBoundary(b.one,xs) do
      if w[2]=b.one then
        contracted:=AFSContractFromBar(b,w{[3..Length(w)]});
      else
        contracted:=AFSNativeContract(b,k-1,List(
          AFSChainFromBar(b,w{[3..Length(w)]}),
          t->[t[1],t[2],w[2]*t[3]]));
      fi;
      for t in contracted do
        Add(terms,[w[1]*t[1],t[2],t[3]]);
      od;
    od;
    val:=AFSCombineChain(terms,false); AddDictionary(b.Gcache[k+1],key,val);
  fi;
  return val;
end);
DeclareGlobalFunction("AFSChainHomotopy");
InstallGlobalFunction(AFSChainHomotopy,function(b,xs)
  local k,key,val,terms,w,t;
  k:=Length(xs);
  if k=0 or b.one in xs then return []; fi;
  if not IsBound(b.H[k+1]) then b.H[k+1]:=NewDictionary([1],true); fi;
  key:=AFSKey(xs); val:=LookupDictionary(b.H[k+1],key);
  if val=fail then
    # F and h on basis cells have leading group one. The bar contraction
    # kills -id and every h(d_bar) face except the first, before recursion.
    terms:=[];
    for t in AFSChainHomotopy(b,xs{[2..k]}) do
      Add(terms,[-t[1],b.one,Concatenation([xs[1]],t[3])]);
    od;
    for w in AFSChainFromBar(b,xs) do
      if w[3]=b.one then continue; fi;
      for t in AFSChainToBar(b,k,w[2]) do
        Add(terms,[w[1]*t[1],b.one,Concatenation([w[3]],t[3])]);
      od;
    od;
    val:=AFSCombineChain(terms,true);
    AddDictionary(b.H[k+1],key,val);
  fi;
  return val;
end);

# Evaluate h^*f without materializing its bar chain. Repeated first-face
# substitution gives an alternating sum over suffixes of the input tuple.
# The chain-valued homotopy remains available as an independent witness.
BindGlobal("AFSHomotopyPullback",function(b,coeff,f)
  return AFSMemo(function(xs...)
    local n,j,prefix,tail,w,t,val;
    n:=Length(xs); val:=0;
    if b.one in xs then return 0; fi;
    for j in [0..n-1] do
      prefix:=xs{[1..j]}; tail:=xs{[j+1..n]};
      for w in AFSChainFromBar(b,tail) do
        if w[3]=b.one then continue; fi;
        for t in AFSChainToBar(b,n-j,w[2]) do
          val:=val+(-1)^j*w[1]*t[1]*CallFuncList(f,
            Concatenation(prefix,[w[3]],t[3]));
        od;
      od;
    od;
    if coeff="F2" then return val mod 2;
    elif coeff="U1s" then return AFSMod1(val); else return val; fi;
  end);
end);
