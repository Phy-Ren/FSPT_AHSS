# Nonzero-background free integer layer. The delivered shift-eight identity
# implies O5(16m,0,0)=0 pointwise, with P=Q=0. Thus 16H1 survives.+# The only nonzero-background space groups with free H1 have rank one;
# their surviving projection has index 1,2,4,8 or16. Every candidate is tested
# with all possible orientation-torsion shifts before choosing its index.
BindGlobal("AFSBackgroundFreePipLifts",function(C)
  local ctx,Hp,free,torsion,r,period,k,mask,coordinates,i,candidate,candidates,
    state,n,result,chosen;
  ctx:=C.ctx;Hp:=C.Hp;
  free:=Filtered([1..Length(Hp.orders)],i->Hp.orders[i]=0);r:=Length(free);
  if r=0 then return rec(status:="computed",rank:=0,generators:=[],freeIndices:=[],
    latticeBasis:=[],survivingParityBasis:=[],latticeIndex:=1,parityCandidates:=[],
    period:=16,certificate:="no-free-integer-layer");fi;
  if r<>1 then Error("nonzero-background rank exceeds the certified rank-one search");fi;
  torsion:=Filtered([1..Length(Hp.orders)],i->Hp.orders[i]<>0);
  if not ForAll(torsion,i->Hp.orders[i]=2) then Error("unexpected integer H1 torsion");fi;
  candidates:=[];chosen:=fail;period:=16;
  for k in [1,2,4,8] do
    AFSStage(ctx,Concatenation("background_free_index_",String(k)));
    for mask in [0..2^Length(torsion)-1] do
      coordinates:=List(Hp.orders,z->0);coordinates[free[1]]:=k;
      for i in [1..Length(torsion)] do coordinates[torsion[i]]:=QuoInt(mask,2^(i-1)) mod 2;od;
      candidate:=AFSFreePipCandidate(C,coordinates);Add(candidates,candidate);
      if candidate.status="survives" then chosen:=candidate;period:=k;break;
      elif candidate.status<>"killed" then Error("undetermined background free candidate");fi;
    od;
    if chosen<>fail then break;fi;
  od;
  if chosen=fail then
    coordinates:=List(Hp.orders,z->0);coordinates[free[1]]:=16;
    n:=AFSCombination(ctx,1,"Zs",Hp,coordinates);
    state:=rec(n:=n,b:=AFSZero,c:=AFSZero,v:=AFSZero,h1Coordinates:=coordinates,
      construction:="strict-universal-16H-zero-lower-tower-from-twice-shift-eight");
  else
    state:=AFSFreePipCompleteTower(chosen.classification);
    state.h1Coordinates:=chosen.h1Coordinates;
  fi;
  result:=rec(status:="computed",rank:=1,generators:=[state],freeIndices:=free,
    latticeBasis:=[[period]],survivingParityBasis:=[],parityCandidates:=candidates,
    latticeIndex:=period,period:=16,
    certificate:="strict-16H-survival-and-complete-rank-one-power-of-two-index-search");
  return result;
end);
