# Audit immutable saved spinless Oh results without rerunning classification.
# U1_OH_SAVED must contain records p32, p15, p29, p30 and p31.
BindGlobal("U1AuditOh",function(saved)
  local source,c,a,HP,HQ,D4,D3,D5,HCI,checks,g,w,q,p,obstruction,phases,
    result,idx,label,target,h,b,indices,elements,embed,restrict,phaseMap,
    chargeMap,sp,v,ker,targetPhaseBasis,i,j,rank,sourcePhaseBasis,
    incoming,sourceIncoming,sourceSquare,phaseQuotientMap;
  Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_32_spinless.g"));
  source:=U1_INPUT;c:=U1CatalogContext(source,7);a:=saved.p32;
  HP:=U1Cohomology(c,4,"U1s");HQ:=U1Cohomology(c,3,"Zr");
  D4:=U1Differential(c,4,"U1s");D3:=U1Differential(c,3,"Zr");D5:=U1Differential(c,5,"U1s");
  checks:=rec(phaseClosure:=0,chargeClosure:=0,phaseCompletion:=0,sourceClosure:=0);
  phases:=Filtered(a.generators,g->g.kind="phase");
  sourcePhaseBasis:=List(phases,g->HP.coordinates(List(g.nativePhase,Rat)));
  if sourcePhaseBasis<>IdentityMat(Length(HP.orders)) then Error("Saved phase coordinates changed");fi;
  for g in a.generators do
    if g.kind="phase" then
      if not ForAll(List(g.nativePhase,Rat)*D4,IsInt) then Error("Saved phase is not closed");fi;
      checks.phaseClosure:=checks.phaseClosure+1;
    elif g.kind="charge" then
      if not ForAll(g.nativeCharge*D3,x->x=0) then Error("Saved charge is not closed");fi;
      checks.chargeClosure:=checks.chargeClosure+1;
    fi;
  od;
  for w in Filtered(a.witnesses,w->w.kind="charge-lift") do
    p:=List(w.nativePhase,Rat);q:=List(w.nativeSource,Rat);
    if not ForAll(p*D4-q,IsInt) then Error("Saved phase does not complete its source");fi;
    if not ForAll(q*D5,IsInt) then Error("Saved phase source is not closed");fi;
    checks.phaseCompletion:=checks.phaseCompletion+1;checks.sourceClosure:=checks.sourceClosure+1;
  od;
  HCI:=U1Cohomology(c,4,"Zr");obstruction:=a.obstructedSheets[1];
  if ForAll(HCI.coordinates(obstruction.nativeSource),x->x=0) then Error("Saved rejected CI sheet is unobstructed");fi;
  incoming:=[];
  for v in U1Cohomology(c,2,"Zr").generators do
    q:=U1Bar(c,2,"Zr",v);p:=U1ChargeGauge(c,3,U1Zero,q);
    Add(incoming,HP.coordinates(U1Native(c,4,"U1s",p)));
  od;
  sourceIncoming:=List(Filtered(a.witnesses,w->w.kind="incoming-charge-gauge"),w->w.phaseCoordinates);
  if incoming<>sourceIncoming then Error("Fresh charge-gauge image differs from saved quotient");fi;
  sourceSquare:=First(a.witnesses,w->w.kind="charge-root" and w.coefficients=[-1,-2,0]).phaseCoordinates;
  result:=rec(group:="Oh",spin:="spinless",checks:=checks,
    savedPhaseBasisCoordinates:=sourcePhaseBasis,
    integerCIObstructionClass:=HCI.coordinates(obstruction.nativeSource),
    freshlyEvaluatedIncomingPhaseCoordinates:=incoming,
    incomingChargeParameterOrders:=U1Cohomology(c,2,"Zr").orders,
    incomingCIParameterOrders:=U1Cohomology(c,0,"Zs").orders,
    rawPhaseOrders:=HP.orders,rawChargeOrders:=HQ.orders,
    finalPhaseOrders:=a.finalPhaseOrders,finalChargeOrders:=a.finalChargeOrders,
    survivingChargeSquarePhase:=sourceSquare,
    savedPresentationSmith:=U1Smith(a.presentation,Length(a.presentation),a.presentationGeneratorCount).diag,
    subgroups:=[]);
  elements:=List([1..source.order],i->First(Elements(c.G),g->c.elementIndex(g)=i));
  for idx in [15,29,30,31] do
    label:=String(idx);Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_",label,"_spinless.g"));
    target:=U1_INPUT;h:=U1CatalogContext(target,7);b:=saved.(Concatenation("p",label));
    indices:=List(target.matrices,m->Position(source.matrices,m));
    if fail in indices then Error("The target catalog is not a literal geometric subgroup");fi;
    for i in [1..target.order] do
      if target.s[i]<>source.s[indices[i]] or target.rho[i]<>source.rho[indices[i]] then Error("Subgroup signs differ");fi;
      for j in [1..target.order] do
        if indices[target.multiplication[i][j]+1]<>source.multiplication[indices[i]][indices[j]]+1 or
          target.omega[i][j]<>source.omega[indices[i]][indices[j]] then Error("Subgroup multiplication/background differs");fi;
      od;
    od;
    embed:=g->elements[indices[h.elementIndex(g)]];
    restrict:=f->function(xs...) return CallFuncList(f,List(xs,embed));end;
    HP:=U1Cohomology(h,4,"U1s");HQ:=U1Cohomology(h,3,"Zr");
    targetPhaseBasis:=List(Filtered(b.generators,g->g.kind="phase"),g->HP.coordinates(List(g.nativePhase,Rat)));
    if targetPhaseBasis<>IdentityMat(Length(HP.orders)) then Error("Saved subgroup phase coordinates changed");fi;
    phaseMap:=List(phases,g->HP.coordinates(U1Native(h,4,"U1s",restrict(U1Bar(c,4,"U1s",List(g.nativePhase,Rat))))));
    chargeMap:=List(Filtered(a.generators,g->g.kind="charge"),g->HQ.coordinates(U1Native(h,3,"Zr",restrict(U1Bar(c,3,"Zr",g.nativeCharge)))));
    for q in chargeMap do
      p:=q*b.chargeObstructionMap;
      if ForAny([1..Length(p)],i->p[i] mod b.chargeObstructionTargetOrders[i]<>0) then
        Error("A completed Oh charge restricts to an obstructed subgroup charge");
      fi;
    od;
    sp:=U1Span(Length(HP.orders));for v in b.filtrationPresentations.phase do U1Insert(sp,v);od;
    phaseQuotientMap:=List(phaseMap,v->U1Reduce(sp,v).remainder);
    for v in sourceIncoming do
      if ForAny(U1Reduce(sp,v*phaseMap).remainder,x->x<>0) then Error("An Oh gauge restricts to a nontrivial subgroup phase");fi;
    od;
    ker:=Filtered(Tuples([0,1],6),v->ForAll(U1Reduce(sp,v*phaseMap).remainder,x->x=0));
    rank:=6-LogInt(Length(ker),2);
    Add(result.subgroups,rec(name:=target.name,order:=target.order,originalIndices:=indices-1,
      literalSignsAndExtensionAgree:=true,rawPhaseRestriction:=phaseMap,
      allCompletedChargeRestrictionsPassTargetObstruction:=true,
      phaseRestrictionModuloIncoming:=phaseQuotientMap,
      completedChargeClassesRestriction:=chargeMap,
      targetPhaseRelations:=b.filtrationPresentations.phase,
      targetFinalPhaseOrders:=b.finalPhaseOrders,targetStackingOrders:=b.torsion,
      finalPhaseImageRank:=rank,finalPhaseKernelRank:=5-rank,
      rawPhaseVectorsRestrictingTriviallyAfterIncoming:=ker,
      chargeSquareRestriction:=U1Reduce(sp,sourceSquare*phaseMap).remainder));
    Print("OH_SUBGROUP_DONE ",target.name,"\n");
  od;
  result.scope:="Exact native equations and subgroup restrictions in the supplied sector; no physical identification of a specific missing reference-table root";
  return result;
end);
U1_OH_AUDIT:=U1AuditOh(U1_OH_SAVED);;
if IsBound(U1_OH_AUDIT_OUT) then
  U1_OH_STREAM:=OutputTextFile(U1_OH_AUDIT_OUT,false);;
  SetPrintFormattingStatus(U1_OH_STREAM,false);;
  WriteLine(U1_OH_STREAM,U1JSON(U1_OH_AUDIT));CloseStream(U1_OH_STREAM);
fi;
