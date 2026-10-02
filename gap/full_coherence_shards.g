# Optional partition of the existing coherence reductions AND flatness checks.
# Every shard still constructs the complete marked presentation independently.
# This file does not change any source, product, inverse, gauge or reduction.
BindGlobal("AFSFullCoherenceCheckKey",function(C,kind,indices)
  return JoinStringsWithSeparator(Concatenation([kind],List(indices,i->C.generators[i].name)),":");
end);

BindGlobal("AFSFullCoherenceShardPlan",function(C,count,index)
  local n,selected,indices,layer,names,plan,add,i,j,k,strata,stratum,bucket,offset,entry;
  if not IsInt(count) or count<2 or count>64 or not IsInt(index) or index<0 or index>=count then
    Error("invalid coherence shard count/index");
  fi;
  n:=Length(C.generators);selected:=[1..n];
  if n>4 then
    selected:=Filtered([1..n],i->C.generators[i].layer>0);
    if Length(selected)>4 then
      selected:=[];
      for layer in [1..3] do
        indices:=Filtered([1..n],i->C.generators[i].layer=layer);
        if Length(indices)>0 then AddSet(selected,indices[1]);AddSet(selected,indices[Length(indices)]);fi;
      od;
    fi;
    if Length(selected)=0 then selected:=[1];fi;
  fi;
  if IsBoundGlobal("AFS_FULL_AUDIT_GENERATORS") then
    names:=ValueGlobal("AFS_FULL_AUDIT_GENERATORS");
    selected:=Filtered([1..n],i->C.generators[i].name in names);
    if Length(selected)<>Length(Set(names)) then Error("unknown named coherence-audit generator");fi;
  fi;
  plan:=[];
  add:=function(kind,indices)
    Add(plan,rec(key:=AFSFullCoherenceCheckKey(C,kind,indices),kind:=kind,
      generators:=indices,integerOccurrences:=Number(indices,i->C.generators[i].layer=3)));
  end;
  for i in [1..n] do
    add("generator-flat",[i]);add("right-inverse",[i]);add("left-inverse",[i]);
    if C.generators[i].order<>0 then add("power-flat",[i]);fi;
  od;
  for i in selected do for j in selected do
    add("product-flat-left",[i,j]);add("product-flat-right",[i,j]);
    add("commutator",[i,j]);
    for k in selected do add("associator",[i,j,k]);od;
  od;od;
  # Lexicographic [integer occurrences, kind] strata, with original check
  # order retained within each. Occurrences first prevents singleton heavy
  # buckets from repeatedly aligning on one worker at kind boundaries.
  # The continuing offset balances total counts and rotates the rare buckets.
  strata:=Set(List(plan,e->[e.integerOccurrences,e.kind]));offset:=0;
  for stratum in strata do
    bucket:=Filtered(plan,e->[e.integerOccurrences,e.kind]=stratum);
    for j in [1..Length(bucket)] do bucket[j].shard:=(offset+j-1) mod count;od;
    offset:=offset+Length(bucket);
  od;
  return rec(schema:="fspt-coherence-shard-v3",policy:="integer-occurrence-first-stratified-round-robin-v3",
    index:=index,count:=count,totalChecks:=Length(plan),selectedGenerators:=selected,
    totalReductionChecks:=Number(plan,e->e.kind in ["right-inverse","left-inverse","commutator","associator"]),
    totalFlatnessChecks:=Number(plan,e->not e.kind in ["right-inverse","left-inverse","commutator","associator"]),
    plannedAllGeneratorTriples:=Length(selected)=n,
    allCheckKeys:=List(plan,e->e.key),assignedCheckKeys:=List(Filtered(plan,e->e.shard=index),e->e.key),
    checkPlan:=plan);
end);

BindGlobal("AFSFullCoherenceAuditShard",function(C,S)
  local c,d,n,plan,assigned,solve,records,actual,reductionKeys,flatRecords,flatGenerators,flatPowers,flatProducts,
    key,selected,i,j,k,x,y,z,left,right,target,check,wanted,flat;
  c:=C.ctx;d:=C.dimension;n:=Length(C.generators);
  plan:=AFSFullCoherenceShardPlan(C,ValueGlobal("AFS_FULL_COHERENCE_SHARDS"),
    ValueGlobal("AFS_FULL_COHERENCE_SHARD_INDEX"));
  assigned:=Set(plan.assignedCheckKeys);selected:=plan.selectedGenerators;
  solve:=AFSStackLatticeSolver(S.presentation,n);records:=[];actual:=[];reductionKeys:=[];flatRecords:=[];
  flatGenerators:=[];flatPowers:=[];flatProducts:=[];
  wanted:=function(kind,indices)return AFSFullCoherenceCheckKey(C,kind,indices) in assigned;end;
  check:=function(kind,indices,target)
    local reduced,relation,checkKey;
    checkKey:=AFSFullCoherenceCheckKey(C,kind,indices);
    if not checkKey in assigned or checkKey in actual then Error("coherence shard executed an unassigned or duplicate check");fi;
    AFSStage(c,Concatenation("full_coherence_check_",checkKey));
    reduced:=AFSFullReduce(C,target,[1..n]);relation:=solve(reduced.coordinates);
    if relation=fail then Error("complete quotient coherence failed: ",kind," ",indices," ",reduced.coordinates);fi;
    Add(records,rec(kind:=kind,generators:=indices,coordinates:=reduced.coordinates,relationCombination:=relation));
    Add(actual,checkKey);Add(reductionKeys,checkKey);
    AFSStage(c,Concatenation("full_coherence_check_complete_",checkKey));
  end;
  flat:=function(kind,indices,target)
    local checkKey;
    checkKey:=AFSFullCoherenceCheckKey(C,kind,indices);
    if not checkKey in assigned or checkKey in actual then Error("coherence shard executed an unassigned or duplicate flatness check");fi;
    AFSStage(c,Concatenation("full_coherence_check_",checkKey));
    if not AFSFullCheckFlat(c,d,target) then Error("coherence flatness failed: ",kind," ",indices);fi;
    Add(flatRecords,rec(key:=checkKey,kind:=kind,generators:=indices,status:="passed"));
    Add(actual,checkKey);
    if kind="generator-flat" then Add(flatGenerators,checkKey);
    elif kind="power-flat" then Add(flatPowers,checkKey);
    else Add(flatProducts,checkKey);fi;
    AFSStage(c,Concatenation("full_coherence_check_complete_",checkKey));
  end;
  for i in [1..n] do
    x:=C.generators[i].state;
    if wanted("generator-flat",[i]) then flat("generator-flat",[i],x);fi;
    if wanted("right-inverse",[i]) or wanted("left-inverse",[i]) then
      y:=AFSFullInverse(c,d,x);
      if wanted("right-inverse",[i]) then check("right-inverse",[i],AFSFullProduct(c,d,x,y));fi;
      if wanted("left-inverse",[i]) then check("left-inverse",[i],AFSFullProduct(c,d,y,x));fi;
    fi;
    if C.generators[i].order<>0 and wanted("power-flat",[i]) then
      target:=AFSFullPower(c,d,x,C.generators[i].order);
      flat("power-flat",[i],target);
    fi;
  od;
  for i in selected do for j in selected do
    x:=C.generators[i].state;y:=C.generators[j].state;
    left:=AFSFullProduct(c,d,x,y);right:=AFSFullProduct(c,d,y,x);
    if wanted("product-flat-left",[i,j]) then flat("product-flat-left",[i,j],left);fi;
    if wanted("product-flat-right",[i,j]) then flat("product-flat-right",[i,j],right);fi;
    if wanted("commutator",[i,j]) then
      check("commutator",[i,j],AFSFullProduct(c,d,left,AFSFullInverse(c,d,right)));
    fi;
    for k in selected do
      if wanted("associator",[i,j,k]) then
        z:=C.generators[k].state;
        left:=AFSFullProduct(c,d,AFSFullProduct(c,d,x,y),z);
        right:=AFSFullProduct(c,d,x,AFSFullProduct(c,d,y,z));
        check("associator",[i,j,k],AFSFullProduct(c,d,left,AFSFullInverse(c,d,right)));
      fi;
    od;
  od;od;
  if actual<>plan.assignedCheckKeys then Error("coherence shard did not complete its exact assigned list");fi;
  return rec(status:="passed-shard",completeAudit:=false,
    scope:="only assigned coherence reductions and flatness checks; complete disjoint aggregate required",
    allGeneratorTriples:=false,selectedGenerators:=selected,shard:=plan,
    actualCheckKeys:=actual,actualReductionKeys:=reductionKeys,actualFlatnessChecks:=flatRecords,
    checks:=records,comparisonSupportFlatness:=false,assignedComparisonSupportFlatness:=true,
    markedGeneratorFlatnessKeys:=flatGenerators,powerFlatnessKeys:=flatPowers,
    selectedProductFlatnessKeys:=flatProducts);
end);
