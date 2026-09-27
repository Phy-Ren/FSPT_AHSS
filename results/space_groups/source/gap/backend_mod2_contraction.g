# Exact mod-two perturbation contraction of the affine extension resolution.
# Cancel after every linear stage instead of expanding integer words to the end.
BindGlobal("AFSMod2NativeReduce",function(terms)
  return List(Filtered(AFSCombineChain(terms,false),t->t[1] mod 2=1),
    t->[1,t[2],t[3]]);
end);
BindGlobal("AFSMod2HorizontalBoundary",function(b,k,terms)
  local out,t,w,p,g;
  out:=[];
  for t in terms do
    p:=b.R!.intToVector(k,t[2])[1];
    for w in BoundaryMap(b.R)(k,t[2]) do
      if b.R!.intToVector(k-1,AbsInt(w[1]))[1]<p then
        Add(out,[1,AbsInt(w[1]),t[3]*b.R!.elts[w[2]]]);
      fi;
    od;
  od;
  return AFSMod2NativeReduce(out);
end);
DeclareGlobalFunction("AFSMod2GradedContract");
BindGlobal("AFSMod2ContractWord",function(b,k,terms,vertical)
  local out,t;
  out:=[];
  for t in terms do Append(out,AFSMod2GradedContract(b,k,t[2],t[3],vertical));od;
  return AFSMod2NativeReduce(out);
end);
InstallGlobalFunction(AFSMod2GradedContract,function(b,k,i,g,vertical)
  local cache,key,flag,v,F,p,q,r,s,pg,lift,ng,ip,il,out,t,pt,u,cor;
  if not IsBound(b.R!.afsFactors) then
    return AFSMod2NativeReduce(AFSContractCell(b,k,i,g));
  fi;
  if not IsBound(b.mod2HCache) then b.mod2HCache:=[];fi;
  if not IsBound(b.mod2HCache[k+1]) then b.mod2HCache[k+1]:=[NewDictionary([1],true),NewDictionary([1],true)];fi;
  if vertical then flag:=2;else flag:=1;fi;
  cache:=b.mod2HCache[k+1][flag];key:=Concatenation([i],AFSKey([g]));
  v:=LookupDictionary(cache,key);if v<>fail then return v;fi;
  F:=b.R!.afsFactors;v:=b.R!.intToVector(k,i);p:=v[1];q:=v[2];r:=v[3];s:=v[4];
  pg:=Image(F.quotient,g);lift:=F.section(pg);ng:=lift^-1*g;
  ip:=F.pointIndex(pg);il:=F.latticeIndex(ng);out:=[];
  for t in F.lattice!.homotopy(q,[s,il]) do
    Add(out,[1,b.R!.vectorToInt(p,q+1,r,AbsInt(t[1])),lift*F.lattice!.elts[t[2]]]);
  od;
  out:=AFSMod2NativeReduce(out);
  if (p=0 and q>0) or vertical then AddDictionary(cache,key,out);return out;fi;
  if p>0 then
    cor:=AFSMod2ContractWord(b,k,AFSMod2HorizontalBoundary(b,k+1,out),false);
    out:=AFSMod2NativeReduce(Concatenation(out,cor));
  fi;
  if q>0 then AddDictionary(cache,key,out);return out;fi;
  pt:=[];
  for t in F.point!.homotopy(p,[r,ip]) do
    Add(pt,[1,b.R!.vectorToInt(p+1,0,AbsInt(t[1]),s),F.section(F.point!.elts[t[2]])]);
  od;
  pt:=AFSMod2NativeReduce(pt);out:=AFSMod2NativeReduce(Concatenation(out,pt));
  u:=AFSMod2ContractWord(b,k,AFSMod2HorizontalBoundary(b,k+1,pt),true);
  out:=AFSMod2NativeReduce(Concatenation(out,u));
  cor:=AFSMod2ContractWord(b,k,AFSMod2HorizontalBoundary(b,k+1,u),false);
  out:=AFSMod2NativeReduce(Concatenation(out,cor));
  AddDictionary(cache,key,out);return out;
end);
BindGlobal("AFSContractCellMod2",function(b,k,i,g)
  return AFSMod2GradedContract(b,k,i,g,false);
end);
