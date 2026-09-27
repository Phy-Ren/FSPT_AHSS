# Optional projected cup-one evaluation on scalar native cycles. All sums F2.
# Linear combinations are formed before the final two native contractions.
BindGlobal("AFSMod2BoundaryCombination",function(c,n,z)
 local out,i,w;
 out:=[];
 for i in [1..Length(z)] do
  if z[i] mod 2=1 then
   for w in BoundaryMap(c.R)(n,i) do
    Add(out,[1,AbsInt(w[1]),c.R!.elts[w[2]]]);
   od;
  fi;
 od;
 return List(Filtered(AFSCombineChain(out,false),t->t[1] mod 2=1),t->[1,t[2],t[3]]);
end);
BindGlobal("AFSRightComponentCombination",function(c,p,q,z)
 local out,i,w,t,x,gid;
 gid:=Identity(c.G);out:=[];
 if p=0 then
  for i in [1..Length(z)] do
   if z[i] mod 2=1 then
    for t in AFSDiagonalAugmentation(c,q,i) do Add(out,[1,gid,t[2]]);od;
   fi;
  od;
 else
  for w in AFSMod2BoundaryCombination(c,p+q,z) do
   for t in AFSDiagonalRightComponent(c,p-1,q,w[2]) do
    Add(out,[t[1],w[3]*t[2],t[3]]);
   od;
  od;
  t:=[];
  for w in AFSRightCoinvariantReduce(out) do
   for x in AFSDiagonalContract(c.bar,p-1,w[1],w[2]) do
    if x[1] mod 2=1 then Add(t,[x[2],x[3],w[3]]);fi;
   od;
  od;
  out:=t;
 fi;
 return AFSRightCoinvariantReduce(out);
end);
BindGlobal("AFSTransposeRightComponentCombination",function(c,p,q,z)
 local out,i,t,w,x,terms;
 out:=[];
 if p=0 then
  for i in [1..Length(z)] do
   if z[i] mod 2=1 then
    for t in AFSDiagonalAugmentation(c,q,i) do Add(out,[t[2],t[3],1]);od;
   fi;
  od;
 else
  terms:=[];
  for w in AFSMod2BoundaryCombination(c,p+q,z) do
   for t in AFSHigherDiagonalCapped(c,0,p+q-1,w[2],Maximum(p-1,q)) do
    if t[1]=p-1 and t[4]=q then
     Add(terms,[t[1],t[2],w[3]*t[3],t[4],t[5],w[3]*t[6]]);
    fi;
   od;
  od;
  for t in AFSTensorReduce(terms) do
   for x in AFSDiagonalContract(c.bar,p-1,t[2],t[3]) do
    if x[1] mod 2=1 then Add(out,[t[5],t[6],x[2]]);fi;
   od;
  od;
 fi;
 return AFSRightCoinvariantReduce(out);
end);
BindGlobal("AFSCup1CombinationPairs",function(c,p,q,z)
 local out,w,t,x,pairs,index,on,j;
 if p=0 then return [];fi;
 out:=Concatenation(AFSRightComponentCombination(c,p-1,q,z),
                   AFSTransposeRightComponentCombination(c,q,p-1,z));
 for w in AFSMod2BoundaryCombination(c,p+q-1,z) do
  for t in AFSCup1Component(c,p-1,q,w[2]) do
   Add(out,[t[1],w[3]*t[2],t[3]]);
  od;
 od;
 pairs:=[];on:=[];index:=NewDictionary([1,1],true);
 for t in AFSRightCoinvariantReduce(out) do
  for x in AFSDiagonalContract(c.bar,p-1,t[1],t[2]) do
   if x[1] mod 2=1 then
    w:=[x[2],t[3]];j:=LookupDictionary(index,w);
    if j=fail then
     Add(pairs,w);Add(on,true);AddDictionary(index,w,Length(pairs));
    else on[j]:=not on[j];fi;
   fi;
  od;
 od;
 return pairs{Filtered([1..Length(pairs)],i->on[i])};
end);
BindGlobal("AFSProjectedSq2U1Coordinates",function(c,a,H)
 local sm,ids,j,z,pairs,forms,out,v,t;
 if not IsBound(c.projectedSquareCycles) then
  sm:=AFSDifferentialSmith(c,5,"U1s");
  ids:=Filtered([1..sm.rank],i->AbsInt(sm.diag[i])>1);
  forms:=[];
  for j in ids do
   if sm.diag[j] mod 2=0 then
    z:=List(sm.Ui,row->row[j] mod 2);;
    pairs:=AFSCup1CombinationPairs(c,3,3,z);
   else pairs:=[];fi;
   Add(forms,pairs);
  od;
  c.projectedSquareCycles:=forms;
 fi;
 out:=[];
 for j in [1..Length(H.orders)] do
  v:=0;
  for t in c.projectedSquareCycles[j] do v:=v+a[t[1]]*a[t[2]];od;
  if H.orders[j] mod 2=0 then Add(out,(H.orders[j]/2)*(v mod 2));else Add(out,0);fi;
 od;
 return out;
end);
