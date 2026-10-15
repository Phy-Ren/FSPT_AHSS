# Generic exact comparison only, copied with symbol-prefix rename from main
# commit 0864495b90297d3e1a0747b77aae17980f6d1f3f. No SC operations.
# Optional exact reduction modulo two of the bar-to-native comparison map.
# G_k = h_(k-1) G_(k-1) d_bar. Every operation in this recurrence is
# Z-linear, so reducing each intermediate word gives precisely G_k mod 2.
# Only F2-valued cochains may use this map; integer/phase transfers keep G.
DeclareGlobalFunction("U1ChainFromBarMod2");
InstallGlobalFunction(U1ChainFromBarMod2,function(b,xs)
  local k,key,val,terms,w,t;
  k:=Length(xs);
  if b.one in xs then return []; fi;
  if k=0 then return [[1,1,b.one]]; fi;
  if not IsBound(b.Gmod2Cache) then b.Gmod2Cache:=[]; fi;
  if not IsBound(b.Gmod2Cache[k+1]) then b.Gmod2Cache[k+1]:=NewDictionary([1],true); fi;
  key:=U1Key(xs); val:=LookupDictionary(b.Gmod2Cache[k+1],key);
  if val=fail then
    terms:=[];
    for w in U1BarBoundary(b.one,xs) do
      for t in U1ChainFromBarMod2(b,w{[3..Length(w)]}) do
        Add(terms,[1,t[2],w[2]*t[3]]);
      od;
    od;
    terms:=U1Mod2NativeReduce(terms);
    val:=U1Mod2ContractWord(b,k-1,terms,false);
    AddDictionary(b.Gmod2Cache[k+1],key,val);
  fi;
  return val;
end);

BindGlobal("U1BarMod2",function(c,k,v)
  local vals;
  vals:=List(v,x->x mod 2);
  if ForAll(vals,x->x=0) then return U1Zero; fi;
  return U1Memo(function(xs...)
    local ans,z;
    if Length(xs)<>k then Error("bar cochain arity mismatch"); fi;
    ans:=0;
    for z in U1ChainFromBarMod2(c.bar,xs) do ans:=ans+vals[z[2]]; od;
    return ans mod 2;
  end);
end);
