AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=2;fi;
c:=AFSBackend(AFS_SG);; ref:=AFSComparison(c.R);;
ReferenceH:=function(b,xs)
 local k,key,val,terms,w,t;
 k:=Length(xs);if k=0 or b.one in xs then return [];fi;
 if not IsBound(b.H[k+1]) then b.H[k+1]:=NewDictionary([1],true);fi;
 key:=AFSKey(xs);val:=LookupDictionary(b.H[k+1],key);
 if val=fail then
  terms:=[[-1,b.one,xs]];
  for w in AFSBarBoundary(b.one,xs) do
   for t in ReferenceH(b,w{[3..Length(w)]}) do Add(terms,[-w[1]*t[1],w[2]*t[2],t[3]]);od;
  od;
  for w in AFSChainFromBar(b,xs) do
   for t in AFSChainToBar(b,k,w[2]) do Add(terms,[w[1]*t[1],w[3]*t[2],t[3]]);od;
  od;
  val:=AFSCombineChain(AFSBarContract(b,AFSCombineChain(terms,true)),true);
  AddDictionary(b.H[k+1],key,val);
 fi;
 return val;
end;;
xs:=[];;actual:=[];;expected:=[];;
gens:=GeneratorsOfGroup(c.G);;elts:=Concatenation(gens,List(gens,g->g^-1));;
for k in [1..3] do
 for trial in [1..8] do
  xs:=List([1..k],i->Random(elts));;
  actual:=ShallowCopy(AFSChainHomotopy(c.bar,xs));;expected:=ReferenceH(ref,xs);;
  Append(actual,List(expected,t->[-t[1],t[2],t[3]]));;
  if AFSCombineChain(actual,true)<>[] then Error("homotopy pruning changed chain");fi;
 od;
od;
Print("AFS_HOMOTOPY_PRUNING_PASS ",AFS_SG,"\n");QUIT_GAP(0);
