AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=104;fi;
c:=AFSBackend(AFS_SG);;ref:=AFSComparison(c.R);;
ReferenceG:=function(b,xs)
 local k,key,val,terms,w,t;
 k:=Length(xs);if b.one in xs then return [];fi;
 if k=0 then return [[1,1,b.one]];fi;
 if not IsBound(b.Gcache[k+1]) then b.Gcache[k+1]:=NewDictionary([1],true);fi;
 key:=AFSKey(xs);val:=LookupDictionary(b.Gcache[k+1],key);
 if val=fail then
  terms:=[];
  for w in AFSBarBoundary(b.one,xs) do
   for t in ReferenceG(b,w{[3..Length(w)]}) do Add(terms,[w[1]*t[1],t[2],w[2]*t[3]]);od;
  od;
  val:=AFSNativeContract(b,k-1,terms);AddDictionary(b.Gcache[k+1],key,val);
 fi;
 return val;
end;;
xs:=[];;actual:=[];;expected:=[];;
gens:=GeneratorsOfGroup(c.G);;elts:=Concatenation(gens,List(gens,g->g^-1));;
for k in [1..4] do
 for trial in [1..10] do
  xs:=List([1..k],i->Random(elts));;
  actual:=ShallowCopy(AFSChainFromBar(c.bar,xs));;expected:=ReferenceG(ref,xs);;
  Append(actual,List(expected,t->[-t[1],t[2],t[3]]));;
  if AFSCombineChain(actual,false)<>[] then Error("G contraction distribution changed chain");fi;
 od;
od;
Print("AFS_G_PRUNING_PASS ",AFS_SG,"\n");QUIT_GAP(0);
