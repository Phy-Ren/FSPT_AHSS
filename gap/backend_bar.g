# Generic exact resolution infrastructure adapted from FSPT_AHSS main.
# No superconducting operations are loaded.
# Independent comparison maps between a HAP resolution C and normalized bar B.
# Recurrences use the contracting homotopies: F=s_B F d_C, G=s_C G d_B,
# and h=s_B(FG-id-h d_B), so d_B h+h d_B=FG-id.
# Bar terms [integer, leading group element, tuple]; native terms [integer,
# basis index, group element]. All caches belong to the current context.
BindGlobal("U1Comparison",function(R)
  local b;
  b:=rec(R:=R,G:=GroupOfResolution(R),F:=[],Gcache:=[],H:=[],hc:=[],ids:=NewDictionary([1],true));
  b.one:=Identity(b.G); b.F[1]:=[[[1,b.one,[]]]]; b.idsSeen:=0;
  b.syncIds:=function()
    while b.idsSeen<Length(b.R!.elts) do
      b.idsSeen:=b.idsSeen+1;
      AddDictionary(b.ids,U1Key([b.R!.elts[b.idsSeen]]),b.idsSeen);
    od;
  end;
  b.syncIds(); return b;
end);

BindGlobal("U1CombineChain",function(terms,bar)
  local out,d,t,key,p;
  out:=[]; d:=NewDictionary([1],true);
  for t in terms do
    if t[1]=0 then continue; fi;
    if bar then key:=U1Key(Concatenation([t[2]],t[3]));
    else key:=Concatenation([t[2]],U1Key([t[3]])); fi;
    p:=LookupDictionary(d,key);
    if p=fail then Add(out,ShallowCopy(t)); AddDictionary(d,key,Length(out));
    else out[p][1]:=out[p][1]+t[1]; fi;
  od;
  return Filtered(out,t->t[1]<>0);
end);
BindGlobal("U1BarContract",function(b,terms)
  return List(Filtered(terms,t->t[2]<>b.one),
    t->[t[1],b.one,Concatenation([t[2]],t[3])]);
end);
# Cache the reduced contraction of each translated native cell, not just
# HAP's raw word. The higher diagonal repeatedly asks for these same cells.
BindGlobal("U1ContractCell",function(b,k,i,g)
  local id,key,v,x,terms;
  if not IsBound(b.cellHCache) then b.cellHCache:=[]; fi;
  if not IsBound(b.cellHCache[k+1]) then b.cellHCache[k+1]:=NewDictionary([1],true); fi;
  b.syncIds(); key:=U1Key([g]); id:=LookupDictionary(b.ids,key);
  if id=fail then
    Add(b.R!.elts,g); b.syncIds(); id:=LookupDictionary(b.ids,key);
  fi;
  key:=[i,id]; v:=LookupDictionary(b.cellHCache[k+1],key);
  if v=fail then
    terms:=List(b.R!.homotopy(k,[i,id]),x->[SignInt(x[1]),AbsInt(x[1]),b.R!.elts[x[2]]]);
    v:=U1CombineChain(terms,false); AddDictionary(b.cellHCache[k+1],key,v);
  fi;
  return v;
end);
BindGlobal("U1NativeContract",function(b,k,terms)
  local out,t,x;
  if terms=[] then return []; fi;
  if Length(terms)=1 and terms[1][1]=1 then
    return U1ContractCell(b,k,terms[1][2],terms[1][3]);
  fi;
  out:=[];
  for t in terms do
    for x in U1ContractCell(b,k,t[2],t[3]) do
      Add(out,[t[1]*x[1],x[2],x[3]]);
    od;
  od;
  return U1CombineChain(out,false);
end);
DeclareGlobalFunction("U1ChainToBar");
BindGlobal("U1ChainToBarCombination",function(b,k,z)
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
  for w in U1CombineChain(boundary,false) do
    if w[3]=b.one then continue; fi;
    for t in U1ChainToBar(b,k-1,w[2]) do
      Add(terms,[w[1]*t[1],w[3]*t[2],t[3]]);
    od;
  od;
  return U1BarContract(b,U1CombineChain(terms,true));
end);
InstallGlobalFunction(U1ChainToBar,function(b,k,i)
  local terms,w,t,g;
  if not IsBound(b.F[k+1]) then b.F[k+1]:=[]; fi;
  if not IsBound(b.F[k+1][i]) then
    terms:=[];
    for w in BoundaryMap(b.R)(k,i) do
      g:=b.R!.elts[w[2]];
      if g=b.one then continue; fi;
      for t in U1ChainToBar(b,k-1,AbsInt(w[1])) do
        Add(terms,[SignInt(w[1])*t[1],g*t[2],t[3]]);
      od;
    od;
    b.F[k+1][i]:=U1CombineChain(U1BarContract(b,terms),true);
  fi;
  return b.F[k+1][i];
end);
DeclareGlobalFunction("U1ChainFromBar");
BindGlobal("U1ContractFromBar",function(b,xs)
  local k,key,val;
  k:=Length(xs);
  if not IsBound(b.HGcache) then b.HGcache:=[]; fi;
  if not IsBound(b.HGcache[k+1]) then b.HGcache[k+1]:=NewDictionary([1],true); fi;
  key:=U1Key(xs); val:=LookupDictionary(b.HGcache[k+1],key);
  if val=fail then
    val:=U1NativeContract(b,k,U1ChainFromBar(b,xs));
    AddDictionary(b.HGcache[k+1],key,val);
  fi;
  return val;
end);
InstallGlobalFunction(U1ChainFromBar,function(b,xs)
  local k,key,val,terms,w,t,contracted;
  k:=Length(xs);
  if b.one in xs then return []; fi;
  if k=0 then return [[1,1,b.one]]; fi;
  if not IsBound(b.Gcache[k+1]) then b.Gcache[k+1]:=NewDictionary([1],true); fi;
  key:=U1Key(xs); val:=LookupDictionary(b.Gcache[k+1],key);
  if val=fail then
    terms:=[];
    for w in U1BarBoundary(b.one,xs) do
      if w[2]=b.one then
        contracted:=U1ContractFromBar(b,w{[3..Length(w)]});
      else
        contracted:=U1NativeContract(b,k-1,List(
          U1ChainFromBar(b,w{[3..Length(w)]}),
          t->[t[1],t[2],w[2]*t[3]]));
      fi;
      for t in contracted do
        Add(terms,[w[1]*t[1],t[2],t[3]]);
      od;
    od;
    val:=U1CombineChain(terms,false); AddDictionary(b.Gcache[k+1],key,val);
  fi;
  return val;
end);
DeclareGlobalFunction("U1ChainHomotopy");
InstallGlobalFunction(U1ChainHomotopy,function(b,xs)
  local k,key,val,terms,w,t;
  k:=Length(xs);
  if k=0 or b.one in xs then return []; fi;
  if not IsBound(b.H[k+1]) then b.H[k+1]:=NewDictionary([1],true); fi;
  key:=U1Key(xs); val:=LookupDictionary(b.H[k+1],key);
  if val=fail then
    # F and h on basis cells have leading group one. The bar contraction
    # kills -id and every h(d_bar) face except the first, before recursion.
    terms:=[];
    for t in U1ChainHomotopy(b,xs{[2..k]}) do
      Add(terms,[-t[1],b.one,Concatenation([xs[1]],t[3])]);
    od;
    for w in U1ChainFromBar(b,xs) do
      if w[3]=b.one then continue; fi;
      for t in U1ChainToBar(b,k,w[2]) do
        Add(terms,[w[1]*t[1],b.one,Concatenation([w[3]],t[3])]);
      od;
    od;
    val:=U1CombineChain(terms,true);
    AddDictionary(b.H[k+1],key,val);
  fi;
  return val;
end);

# Evaluate h^*f without materializing its bar chain. Repeated first-face
# substitution gives an alternating sum over suffixes of the input tuple.
# The chain-valued homotopy remains available as an independent witness.
# Exact F2 evaluation of the SAME integral homotopy. The bounded buffer
# combines equal bar tuples before evaluating f; flushing only loses possible
# cancellations across chunks, never changes the value modulo two.
BindGlobal("U1F2HomotopyPullbackFiltered",function(b,f)
  return U1Memo(function(xs...)
    local n,j,prefix,tail,w,t,value,keys,tuples,parities,key,pos,tuple,flush,stats;
    n:=Length(xs);value:=0;
    if b.one in xs then return 0;fi;
    stats:=b.f2ParityStats;stats.homotopyEvaluations:=stats.homotopyEvaluations+1;
    keys:=NewDictionary([1],true);tuples:=[];parities:=[];
    flush:=function()
      local i;
      for i in [1..Length(tuples)] do
        if parities[i]=1 then
          value:=(value+CallFuncList(f,tuples[i])) mod 2;
          stats.homotopySourceCalls:=stats.homotopySourceCalls+1;
        fi;
      od;
      stats.homotopyFlushes:=stats.homotopyFlushes+1;
      keys:=NewDictionary([1],true);tuples:=[];parities:=[];
    end;
    for j in [0..n-1] do
      prefix:=xs{[1..j]};tail:=xs{[j+1..n]};
      for w in U1ChainFromBar(b,tail) do
        if w[3]=b.one then continue;fi;
        if w[1] mod 2=0 then
          stats.homotopyEvenNativeTerms:=stats.homotopyEvenNativeTerms+1;continue;
        fi;
        for t in U1ChainToBar(b,n-j,w[2]) do
          stats.homotopyBarTerms:=stats.homotopyBarTerms+1;
          if t[1] mod 2=0 then
            stats.homotopyEvenBarTerms:=stats.homotopyEvenBarTerms+1;continue;
          fi;
          tuple:=Concatenation(prefix,[w[3]],t[3]);key:=U1Key(tuple);
          pos:=LookupDictionary(keys,key);
          if pos=fail then
            if Length(tuples)>=b.f2ParitySupportLimit then flush();fi;
            Add(tuples,tuple);Add(parities,1);AddDictionary(keys,key,Length(tuples));
            stats.maximumBufferedTuples:=Maximum(stats.maximumBufferedTuples,Length(tuples));
          else
            parities[pos]:=1-parities[pos];
            stats.homotopyDuplicateTerms:=stats.homotopyDuplicateTerms+1;
          fi;
        od;
      od;
    od;
    flush();return value;
  end);
end);

BindGlobal("U1HomotopyPullback",function(b,coeff,f)
  if coeff="F2" and IsBound(b.f2ParityFilter) and b.f2ParityFilter then
    return U1F2HomotopyPullbackFiltered(b,f);
  fi;
  return U1Memo(function(xs...)
    local n,j,prefix,tail,w,t,val;
    n:=Length(xs); val:=0;
    if b.one in xs then return 0; fi;
    for j in [0..n-1] do
      prefix:=xs{[1..j]}; tail:=xs{[j+1..n]};
      for w in U1ChainFromBar(b,tail) do
        if w[3]=b.one then continue; fi;
        for t in U1ChainToBar(b,n-j,w[2]) do
          val:=val+(-1)^j*w[1]*t[1]*CallFuncList(f,
            Concatenation(prefix,[w[3]],t[3]));
        od;
      od;
    od;
    if coeff="F2" then return val mod 2;
    elif coeff="U1s" then return U1Mod1(val); else return val; fi;
  end);
end);
