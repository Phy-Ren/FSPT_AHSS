# Higher p+ip obstruction on the actual lower defining tower.
# Lower choices are quotiented by their incoming operations, never an s^2 gate.

BindGlobal("AFSF2SolveRows",function(rows,target)
  local v;
  if ForAll(target,x->x mod 2=0) then return List(rows,x->0); fi;
  if Length(rows)=0 then return fail; fi;
  v:=SolutionMat(List(rows,r->List(r,x->(x mod 2)*One(GF(2)))),List(target,x->(x mod 2)*One(GF(2))));
  if v=fail then return fail; fi;
  return List(v,IntFFE);
end);

BindGlobal("AFSClassifyPipTorsion",function(C,n,source)
  local ctx,b,t,H4,co,adjust,deltaB,cf,phase,rows,lift,target,result,zero,d3co,bound;
  ctx:=C.ctx;
  AFSStage(ctx,"pip_d3");
  b:=AFSSolve(ctx,3,"F2",source);
  if b=fail then Error("p+ip d2 primitive failure"); fi;
  t:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=n,b:=b));
  H4:=AFSCohomology(ctx,4,"F2");
  co:=H4.coordinates(AFSNative(ctx,4,"F2",t));
  if co=fail then Error("p+ip d3 source not closed on lower tower"); fi;
  d3co:=ShallowCopy(co);
  adjust:=AFSF2SolveRows(C.mcPrimaryRows,co);
  if adjust=fail then return rec(status:="killed",page:=3,obstruction:=co); fi;
  if ForAny(adjust,x->x<>0) then
    deltaB:=AFSCombination(ctx,2,"F2",C.H2,adjust);
    b:=AFSAddF2(b,deltaB);
    t:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=n,b:=b));
  fi;
  cf:=AFSSolve(ctx,4,"F2",t);
  if cf=fail then Error("p+ip d3 lower-choice adjustment failed"); fi;
  C.pipLiftData:=rec(n:=n,b:=b,c:=cf);
  rows:=ShallowCopy(C.cfPrimaryRows);
  for lift in C.mcLifts do
    if IsBound(lift.obstructionCoordinates) then Add(rows,lift.obstructionCoordinates); fi;
  od;
  target:=AFSQuotient(C.H5U.orders,rows);
  if ForAll(target.orders,o->o<>0 and o mod 2=1) then
    return rec(status:="survives",page:=4,certificate:="d2-and-d3-primitives-zero-two-primary-d4-target",d3_initial_coordinates:=co,majorana_adjustment:=adjust,d4_target:=target.orders);
  fi;
  AFSStage(ctx,"pip_d4");
  phase:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=cf));
  co:=AFSClosedPhaseClass(ctx,5,C.H5U,phase);
  if co=fail then Error("p+ip d4 phase is not closed"); fi;
  C.pipLiftData.obstruction:=phase; C.pipLiftData.obstructionCoordinates:=co;
  result:=target.project(co);
  bound:=2;if IsBound(C.pipCandidateOrderBound) then bound:=C.pipCandidateOrderBound;fi;
  if bound=2 then AFSOrderTwoBits(target.orders,result);
  elif not ForAll([1..Length(result)],i->
      (target.orders[i]=0 and result[i]=0) or
      (target.orders[i]<>0 and (bound*result[i]) mod target.orders[i]=0)) then
    Error("p+ip obstruction exceeds the certified integer-period bound");
  fi;
  if ForAny(result,x->x<>0) then
    return rec(status:="killed",page:=4,obstruction:=result,d3_initial_coordinates:=d3co,majorana_adjustment:=adjust,d4_raw_coordinates:=co,d4_target:=target.orders);
  fi;
  return rec(status:="survives",page:=4,certificate:="explicit-full-O5-in-E4-quotient",d3_initial_coordinates:=d3co,d4_projected_coordinates:=result,majorana_adjustment:=adjust,d4_raw_coordinates:=co,d4_target:=target.orders);
end);
