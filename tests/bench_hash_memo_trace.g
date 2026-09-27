if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_hash_cache.g"));;
if not IsBound(AFS_SG) then AFS_SG:=219;fi;
c:=AFSBackend(AFS_SG);;trace:=[];;
for i in [1..Dimension(c.R)(5)] do
  for term in AFSChainToBar(c.bar,5,i) do Add(trace,term[3]);od;
od;
Print("HASH_MEMO_REAL_TRACE sg=",AFS_SG," accesses=",Length(trace),"\n");
sortedMiss:=0;;hashMiss:=0;;
sf:=AFSMemo(function(xs...) sortedMiss:=sortedMiss+1;return Sum(xs,x->Sum(x!.exponents)^2);end);;
hf:=AFSHashMemo(function(xs...) hashMiss:=hashMiss+1;return Sum(xs,x->Sum(x!.exponents)^2);end);;
t:=Runtime();;sa:=List(trace,xs->CallFuncList(sf,xs));;sortedMs:=Runtime()-t;;
Print("SORTED_MEMO_TRACE_COMPLETE sg=",AFS_SG," cpu_ms=",sortedMs," misses=",sortedMiss,"\n");
t:=Runtime();;ha:=List(trace,xs->CallFuncList(hf,xs));;hashMs:=Runtime()-t;;
if sa<>ha or sortedMiss<>hashMiss then Error("real access trace memoization differs");fi;
Print("HASH_MEMO_TRACE_COMPLETE sg=",AFS_SG," cpu_ms=",hashMs," misses=",hashMiss,"\n");
Print("AFS_HASH_MEMO_TRACE_PASS\n");QUIT_GAP(0);
