# The optional mod-two contraction is independently checked against the
# integral HAP contraction. Selection is fixed when this file is read.
if IsBoundGlobal("U1_USE_MOD2_CONTRACTION") and
   ValueGlobal("U1_USE_MOD2_CONTRACTION")=true and
   IsBoundGlobal("U1ContractCellMod2") then
  BindGlobal("U1DiagonalContract",ValueGlobal("U1ContractCellMod2"));
else BindGlobal("U1DiagonalContract",U1ContractCell);fi;
BindGlobal("U1DiagonalContractWord",function(b,k,terms)
  local out,t,x;
  out:=[];
  for t in terms do
    for x in U1DiagonalContract(b,k,t[2],t[3]) do
      Add(out,[t[1]*x[1],x[2],x[3]]);
    od;
  od;
  return List(Filtered(U1CombineChain(out,false),t->t[1] mod 2=1),
    t->[1,t[2],t[3]]);
end);
# Native mod-two higher diagonals, constructed from the HAP contraction.
# No bar expansion: D0:C -> C tensor C and D1:C -> (C tensor C)[1].
# d D0 = D0 d; d D1 + D1 d = D0 + tau D0 over F2.
# Tensor term = [left degree, left basis, left group, right degree,
#                right basis, right group]; duplicate terms cancel mod two.
BindGlobal("U1TensorReduce",function(terms)
  local index,out,on,t,key,i;
  index:=NewDictionary([1],true); out:=[]; on:=[];
  for t in terms do
    key:=Concatenation([t[1],t[2],t[4],t[5]],U1Key([t[3],t[6]]));
    i:=LookupDictionary(index,key);
    if i=fail then
      Add(out,t); Add(on,true); AddDictionary(index,key,Length(out));
    else on[i]:=not on[i]; fi;
  od;
  return out{Filtered([1..Length(out)],i->on[i])};
end);
BindGlobal("U1TensorContractCapped",function(c,terms,cap)
  local out,t,v,x,gid;
  gid:=Identity(c.G); out:=[];
  for t in terms do
    if t[1]<cap then
      for x in U1DiagonalContract(c.bar,t[1],t[2],t[3]) do
        if x[1] mod 2=1 then Add(out,[t[1]+1,x[2],x[3],t[4],t[5],t[6]]); fi;
      od;
    fi;
    if t[1]=0 and t[4]<cap then
      for x in U1DiagonalContract(c.bar,t[4],t[5],t[6]) do
        if x[1] mod 2=1 then Add(out,[0,1,gid,t[4]+1,x[2],x[3]]); fi;
      od;
    fi;
  od;
  return U1TensorReduce(out);
end);
DeclareGlobalFunction("U1HigherDiagonalCapped");
InstallGlobalFunction(U1HigherDiagonalCapped,function(c,r,n,i,cap)
  local terms,t,w,g,cache;
  if not IsBound(c.diagonalCache) then c.diagonalCache:=[]; fi;
  if not IsBound(c.diagonalCache[cap+1]) then c.diagonalCache[cap+1]:=[]; fi;
  if not IsBound(c.diagonalCache[cap+1][r+1]) then c.diagonalCache[cap+1][r+1]:=[]; fi;
  cache:=c.diagonalCache[cap+1][r+1];
  if not IsBound(cache[n+1]) then cache[n+1]:=[]; fi;
  if IsBound(cache[n+1][i]) then return cache[n+1][i]; fi;
  if n=0 and r=0 then
    cache[1][i]:=[[0,1,Identity(c.G),0,1,Identity(c.G)]];
    return cache[1][i];
  fi;
  terms:=[];
  if r>0 then
    for t in U1HigherDiagonalCapped(c,r-1,n,i,cap) do
      Add(terms,t); Add(terms,[t[4],t[5],t[6],t[1],t[2],t[3]]);
    od;
  fi;
  if n>0 then
    for w in BoundaryMap(c.R)(n,i) do
      g:=c.R!.elts[w[2]];
      for t in U1HigherDiagonalCapped(c,r,n-1,AbsInt(w[1]),cap) do
        if g=Identity(c.G) then Add(terms,t);
        else Add(terms,[t[1],t[2],g*t[3],t[4],t[5],g*t[6]]); fi;
      od;
    od;
  fi;
  cache[n+1][i]:=U1TensorContractCapped(c,U1TensorReduce(terms),cap);
  return cache[n+1][i];
end);
BindGlobal("U1HigherDiagonal",function(c,r,n,i) return U1HigherDiagonalCapped(c,r,n,i,n+r); end);

DeclareGlobalFunction("U1NativeCupI");
DeclareGlobalFunction("U1NativeCup1Projected");
BindGlobal("U1NativeCupIFull",function(c,p,q,r,a,b)
  local n,out,i,t,v,key,forms,pairs,dict,pos,on;
  n:=p+q-r; out:=[]; key:=Concatenation(String(r),"_",String(p),"_",String(q));
  if not IsBound(c.cupPairCache) then c.cupPairCache:=rec(); fi;
  if not IsBound(c.cupPairCache.(key)) then
    forms:=[];
    for i in [1..Dimension(c.R)(n)] do
      pairs:=[]; on:=[]; dict:=NewDictionary([1,1],true);
      for t in U1HigherDiagonalCapped(c,r,n,i,Maximum(p,q)) do
        if t[1]=p and t[4]=q then
          pos:=LookupDictionary(dict,[t[2],t[5]]);
          if pos=fail then
            Add(pairs,[t[2],t[5]]); Add(on,true);
            AddDictionary(dict,[t[2],t[5]],Length(pairs));
          else on[pos]:=not on[pos]; fi;
        fi;
      od;
      Add(forms,pairs{Filtered([1..Length(pairs)],j->on[j])});
    od;
    c.cupPairCache.(key):=forms;
  fi;
  for pairs in c.cupPairCache.(key) do
    v:=0;
    for t in pairs do v:=v+a[t[1]]*b[t[2]]; od;
    Add(out,v mod 2);
  od;
  return out;
end);
BindGlobal("U1NativeSq2",function(c,p,a)
  return U1NativeCupI(c,p,p,p-2,a,a);
end);
# Public ordering follows cup_i(a_p,b_q).
BindGlobal("U1NativeCup",function(c,r,p,a,q,b)
  return U1NativeCupI(c,p,q,r,a,b);
end);

# Evaluate a higher diagonal on a scalar native chain before the final tensor
# contraction.  The contraction is only Z-linear, so group-ring boundary
# terms below use equivariant translates of the individual lower-cell maps.
DeclareGlobalFunction("U1HigherDiagonalCombination");
DeclareGlobalFunction("U1HigherDiagonalCombinationSource");
InstallGlobalFunction(U1HigherDiagonalCombinationSource,function(c,r,n,z,cap)
  local terms,bound,i,w,g,t,gid;
  gid:=Identity(c.G);
  terms:=[];
  if r>0 then
    for t in U1HigherDiagonalCombination(c,r-1,n,z,cap) do
      Add(terms,t); Add(terms,[t[4],t[5],t[6],t[1],t[2],t[3]]);
    od;
  fi;
  if n>0 then
    bound:=[];
    for i in [1..Length(z)] do
      if z[i] mod 2=1 then
        for w in BoundaryMap(c.R)(n,i) do
          Add(bound,[1,AbsInt(w[1]),c.R!.elts[w[2]]]);
        od;
      fi;
    od;
    for w in U1CombineChain(bound,false) do
      if w[1] mod 2=1 then
        g:=w[3];
        for t in U1HigherDiagonalCapped(c,r,n-1,w[2],cap) do
          if g=gid then Add(terms,t);
          else Add(terms,[t[1],t[2],g*t[3],t[4],t[5],g*t[6]]); fi;
        od;
      fi;
    od;
  fi;
  return terms;
end);
InstallGlobalFunction(U1HigherDiagonalCombination,function(c,r,n,z,cap)
  if n=0 and r=0 then
    if Sum(z) mod 2=0 then return []; fi;
    return [[0,1,Identity(c.G),0,1,Identity(c.G)]];
  fi;
  return U1TensorContractCapped(c,U1TensorReduce(
    U1HigherDiagonalCombinationSource(c,r,n,z,cap)),cap);
end);

# j Sq^2 needs only the torsion coordinates, rather than every target cell.
# If U D V = diag(d), its j-th coordinate is
#   (d_j/2) * <Sq^2(a), column_j(U^-1)> mod |d_j|.
# Odd target factors receive zero since j Sq^2 has exponent two.
BindGlobal("U1NativeSq2U1Coordinates",function(c,p,a,target)
  local key,s,inds,forms,j,k,z,terms,pairs,on,index,pos,t,x,out,w;
  if Length(target.orders)=0 then return []; fi;
  if p=3 then return target.coordinates(U1NativeCup1Projected(c,3,a,3,a)/2); fi;
  key:=String(p);
  if not IsBound(c.squareClassCache) then c.squareClassCache:=rec(); fi;
  if not IsBound(c.squareClassCache.(key)) then
    s:=target.smith;
    inds:=Filtered([1..s.rank],i->AbsInt(s.diag[i])>1);
    forms:=[];
    for j in inds do
      pairs:=[];
      if s.diag[j] mod 2=0 then
        z:=List(s.Ui,row->row[j] mod 2);
        terms:=U1HigherDiagonalCombinationSource(c,p-2,p+2,z,p);
        # Only h(left) tensor right contributes in bidegree (p,p), p>=2.
        # Forget the final group labels during contraction, avoiding a large
        # intermediate tensor chain that the trivial F2 pairing discards.
        terms:=U1TensorReduce(Filtered(terms,t->t[1]=p-1 and t[4]=p));
        on:=[]; index:=NewDictionary([1,1],true);
        for t in terms do
          for w in U1DiagonalContract(c.bar,p-1,t[2],t[3]) do
            if w[1] mod 2=1 then
            # Squares permit identifying (i,j) with (j,i).
            x:=[Minimum(w[2],t[5]),Maximum(w[2],t[5])];
            pos:=LookupDictionary(index,x);
            if pos=fail then
              Add(pairs,x); Add(on,true); AddDictionary(index,x,Length(pairs));
            else on[pos]:=not on[pos]; fi;
            fi;
          od;
        od;
        pairs:=pairs{Filtered([1..Length(pairs)],i->on[i])};
      fi;
      Add(forms,pairs);
    od;
    c.squareClassCache.(key):=forms;
  fi;
  out:=[]; forms:=c.squareClassCache.(key);
  for k in [1..Length(target.orders)] do
    x:=0;
    for t in forms[k] do x:=x+a[t[1]]*a[t[2]]; od;
    if target.orders[k] mod 2=0 then Add(out,(target.orders[k]/2)*(x mod 2));
    else Add(out,0); fi;
  od;
  return out;
end);

# For cup_1 with trivial F2 coefficients, retain only the left group label.
# Once the output bidegree has positive left degree, tensor contraction acts
# only on the left. The p=0 seed is computed in the full tensor complex.
BindGlobal("U1RightCoinvariantReduce",function(terms)
  local index,out,on,t,key,i;
  index:=NewDictionary([1],true); out:=[]; on:=[];
  for t in terms do
    key:=Concatenation([t[1],t[3]],U1Key([t[2]]));
    i:=LookupDictionary(index,key);
    if i=fail then
      Add(out,t); Add(on,true); AddDictionary(index,key,Length(out));
    else on[i]:=not on[i]; fi;
  od;
  return out{Filtered([1..Length(out)],i->on[i])};
end);
# Both augmented D0 components equal this native chain map T=h T d.
DeclareGlobalFunction("U1DiagonalAugmentation");
InstallGlobalFunction(U1DiagonalAugmentation,function(c,n,i)
  local cache,terms,w,t,v;
  if not IsBound(c.diagonalAugCache) then c.diagonalAugCache:=[]; fi;
  if not IsBound(c.diagonalAugCache[n+1]) then c.diagonalAugCache[n+1]:=[]; fi;
  cache:=c.diagonalAugCache[n+1];
  if IsBound(cache[i]) then return cache[i]; fi;
  if n=0 then cache[i]:=[[1,1,Identity(c.G)]]; return cache[i]; fi;
  terms:=[];
  for w in BoundaryMap(c.R)(n,i) do
    for t in U1DiagonalAugmentation(c,n-1,AbsInt(w[1])) do
      Add(terms,[1,t[2],c.R!.elts[w[2]]*t[3]]);
    od;
  od;
  terms:=List(Filtered(U1CombineChain(terms,false),t->t[1] mod 2=1),t->[1,t[2],t[3]]);
  v:=U1DiagonalContractWord(c.bar,n-1,terms);
  cache[i]:=List(Filtered(v,t->t[1] mod 2=1),t->[1,t[2],t[3]]);
  return cache[i];
end);
# Exact D0 marginals needed by the right-coinvariant D1 recursion.
DeclareGlobalFunction("U1DiagonalRightComponent");
InstallGlobalFunction(U1DiagonalRightComponent,function(c,p,q,i)
  local key,cache,out,t,w,g,gid,x;
  key:=Concatenation(String(p),"_",String(q)); gid:=Identity(c.G);
  if not IsBound(c.diagonalRightCache) then c.diagonalRightCache:=rec(); fi;
  if not IsBound(c.diagonalRightCache.(key)) then c.diagonalRightCache.(key):=[]; fi;
  cache:=c.diagonalRightCache.(key);
  if IsBound(cache[i]) then return cache[i]; fi;
  out:=[];
  if p=0 then
    for t in U1DiagonalAugmentation(c,q,i) do Add(out,[1,gid,t[2]]); od;
  else
    for w in BoundaryMap(c.R)(p+q,i) do
      g:=c.R!.elts[w[2]];
      for t in U1DiagonalRightComponent(c,p-1,q,AbsInt(w[1])) do
        if g=gid then Add(out,t); else Add(out,[t[1],g*t[2],t[3]]); fi;
      od;
    od;
    out:=U1RightCoinvariantReduce(out); t:=[];
    for w in out do
      for x in U1DiagonalContract(c.bar,p-1,w[1],w[2]) do
        if x[1] mod 2=1 then Add(t,[x[2],x[3],w[3]]); fi;
      od;
    od;
    out:=t;
  fi;
  cache[i]:=U1RightCoinvariantReduce(out); return cache[i];
end);
BindGlobal("U1DiagonalTransposeRightComponent",function(c,p,q,i)
  local key,cache,out,t,w,g,x,terms;
  key:=Concatenation(String(p),"_",String(q));
  if not IsBound(c.diagonalTransposeRightCache) then c.diagonalTransposeRightCache:=rec(); fi;
  if not IsBound(c.diagonalTransposeRightCache.(key)) then c.diagonalTransposeRightCache.(key):=[]; fi;
  cache:=c.diagonalTransposeRightCache.(key);
  if IsBound(cache[i]) then return cache[i]; fi;
  out:=[];
  if p=0 then
    for t in U1DiagonalAugmentation(c,q,i) do Add(out,[t[2],t[3],1]); od;
  else
    terms:=[];
    for w in BoundaryMap(c.R)(p+q,i) do
      g:=c.R!.elts[w[2]];
      for t in U1HigherDiagonalCapped(c,0,p+q-1,AbsInt(w[1]),Maximum(p-1,q)) do
        if t[1]=p-1 and t[4]=q then
          Add(terms,[t[1],t[2],g*t[3],t[4],t[5],g*t[6]]);
        fi;
      od;
    od;
    for t in U1TensorReduce(terms) do
      for x in U1DiagonalContract(c.bar,p-1,t[2],t[3]) do
        if x[1] mod 2=1 then Add(out,[t[5],t[6],x[2]]); fi;
      od;
    od;
  fi;
  cache[i]:=U1RightCoinvariantReduce(out); return cache[i];
end);
DeclareGlobalFunction("U1Cup1ComponentSource");
DeclareGlobalFunction("U1Cup1Component");
InstallGlobalFunction(U1Cup1ComponentSource,function(c,p,q,i)
  local n,out,t,w,g,gid;
  n:=p+q-1; gid:=Identity(c.G);
  out:=Concatenation(U1DiagonalRightComponent(c,p-1,q,i),
                    U1DiagonalTransposeRightComponent(c,q,p-1,i));
  if n>0 then
    for w in BoundaryMap(c.R)(n,i) do
      g:=c.R!.elts[w[2]];
      for t in U1Cup1Component(c,p-1,q,AbsInt(w[1])) do
        if g=gid then Add(out,t); else Add(out,[t[1],g*t[2],t[3]]); fi;
      od;
    od;
  fi;
  return out;
end);
InstallGlobalFunction(U1Cup1Component,function(c,p,q,i)
  local key,cache,out,t,x,n;
  n:=p+q-1;
  if n<0 then return []; fi;
  key:=Concatenation(String(p),"_",String(q));
  if not IsBound(c.cup1ComponentCache) then c.cup1ComponentCache:=rec(); fi;
  if not IsBound(c.cup1ComponentCache.(key)) then c.cup1ComponentCache.(key):=[]; fi;
  cache:=c.cup1ComponentCache.(key);
  if IsBound(cache[i]) then return cache[i]; fi;
  out:=[];
  if p=0 then
    # The two augmented D0 source components are equal T and cancel over F2.
    # The remaining lower D1 component is zero inductively.
    out:=[];
  else
    for t in U1RightCoinvariantReduce(U1Cup1ComponentSource(c,p,q,i)) do
      for x in U1DiagonalContract(c.bar,p-1,t[1],t[2]) do
        if x[1] mod 2=1 then Add(out,[x[2],x[3],t[3]]); fi;
      od;
    od;
  fi;
  cache[i]:=U1RightCoinvariantReduce(out); return cache[i];
end);
InstallGlobalFunction(U1NativeCup1Projected,function(c,p,a,q,b)
  local out,i,t,val,key,forms,pairs,on,index,pos,x,w;
  key:=Concatenation(String(p),"_",String(q));
  if not IsBound(c.cup1PairCache) then c.cup1PairCache:=rec(); fi;
  if not IsBound(c.cup1PairCache.(key)) then
    forms:=[];
    for i in [1..Dimension(c.R)(p+q-1)] do
      pairs:=[]; on:=[]; index:=NewDictionary([1,1],true);
      if p=0 then
        w:=List(U1Cup1Component(c,p,q,i),t->[t[1],t[3]]);
      else
        w:=[];
        for t in U1RightCoinvariantReduce(U1Cup1ComponentSource(c,p,q,i)) do
          for x in U1DiagonalContract(c.bar,p-1,t[1],t[2]) do
            if x[1] mod 2=1 then Add(w,[x[2],t[3]]); fi;
          od;
        od;
      fi;
      for t in w do
        pos:=LookupDictionary(index,t);
        if pos=fail then
          Add(pairs,t); Add(on,true); AddDictionary(index,t,Length(pairs));
        else on[pos]:=not on[pos]; fi;
      od;
      Add(forms,pairs{Filtered([1..Length(pairs)],j->on[j])});
    od;
    c.cup1PairCache.(key):=forms;
  fi;
  out:=[];
  for pairs in c.cup1PairCache.(key) do
    val:=0;
    for t in pairs do val:=val+a[t[1]]*b[t[2]]; od;
    Add(out,val mod 2);
  od;
  return out;
end);
InstallGlobalFunction(U1NativeCupI,function(c,p,q,r,a,b)
  if r=1 and p=3 and q=3 then return U1NativeCup1Projected(c,p,a,q,b); fi;
  return U1NativeCupIFull(c,p,q,r,a,b);
end);
