if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_hash_cache.g"));;
# Equal keys with different storage/unused capacity must hash identically.
for n in [0..40] do
  a:=[1..n];b:=[];Append(b,a);c:=List(a,x->x);
  if AFSExactKeyHash(a)<>AFSExactKeyHash(b) or AFSExactKeyHash(b)<>AFSExactKeyHash(c) then Error("equal list representations hash differently");fi;
od;
a:=[2^90+123,-2^100+53,0,17];b:=[2^90+120+3,-2^100+50+3,0,17];
if a<>b or AFSExactKeyHash(a)<>AFSExactKeyHash(b) then Error("equal large signed integer keys hash differently");fi;
# Force collisions by supplying the official dictionary a constant hash.
d:=AFSNewHashCache(x->0);;
for i in [1..300] do AddDictionary(d,Immutable([i,-i,i^2]),i^3);od;
for i in [1..300] do if LookupDictionary(d,[i,-i,i^2])<>i^3 then Error("hash collision lost exact key equality");fi;od;
AddDictionary(d,[123,-123,123^2],false);;
if LookupDictionary(d,[123,-123,123^2])<>false then Error("cache replacement failed");fi;
AddDictionary(d,[],fail);;
if not KnowsDictionary(d,[]) or LookupDictionary(d,[])<>fail then Error("stored fail and empty-key semantics differ");fi;
key:=[-19,2^90];AddDictionary(d,key,71);key[1]:=5;
if LookupDictionary(d,[-19,2^90])<>71 or KnowsDictionary(d,key) then Error("mutation of caller key corrupted stored key");fi;
AddDictionary(d,[(1,2),(1,2,3)],23);
if LookupDictionary(d,[(2,1),(2,3,1)])<>23 then Error("non-Pcp key equality fallback differs");fi;
g:=AFSBackend(1).G;;x:=GeneratorsOfGroup(g)[1];;
calls:=0;;f:=AFSHashMemo(function(xs...) calls:=calls+1;return List(xs,y->ShallowCopy(y!.exponents));end);;
for n in [-30..30] do
  if f(x^n,x^(2*n))<>f(x^n,x^(2*n)) then Error("memoized group callback changed value");fi;
od;
if calls<>61 then Error("memoized group callback miss count differs");fi;
fails:=0;;f:=AFSHashMemo(function(xs...) fails:=fails+1;return fail;end);;
if f(x)<>fail or f(x)<>fail or fails<>2 then Error("fail cache semantics differ");fi;
Print("AFS_HASH_CACHE_EXACT_PASS\n");QUIT_GAP(0);
