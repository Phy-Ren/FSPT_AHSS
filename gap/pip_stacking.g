# Marked torsion p+ip square, after the independent universal coordinate audit.
# Load after stacking.g, pip_coordinates.g, and pip_diagonal_data.g.
# This file is optional until the diagonal formula and its tests are available.

# Find an ACTUAL orientation lift G -> C4 from degree-one native cocycles.
# No space-group number list enters this construction. Since untwisted
# degree-one coboundaries vanish, t mod2 equals s pointwise, not only in H1.
BindGlobal("AFSPipC4FlatLift",function(C)
  local ctx,sn,D,beta,u,tn,residual,t,tbar,index,c,v,certificate;
  if not IsBoundGlobal("AFSC4PipPhase4") then return fail;fi;
  if IsBoundGlobal("AFS_PIP_USE_C4") and ValueGlobal("AFS_PIP_USE_C4")=false then return fail;fi;
  ctx:=C.ctx;sn:=AFSNative(ctx,1,"F2",ctx.s);D:=AFSDifferential(ctx,1,"Z");
  beta:=sn*D;
  if not ForAll(beta,x->IsInt(x/2)) then Error("orientation Bockstein is nonintegral");fi;
  u:=AFSSolveNative(ctx,2,"F2",List(beta,x->(x/2) mod 2));
  if u=fail then return fail;fi;
  tn:=sn+2*u;residual:=tn*D;
  if not ForAll(residual,x->x mod 4=0) then Error("proposed C4 character is not closed modulo4");fi;
  tbar:=AFSBar(ctx,1,"Z",tn);
  t:=AFSMemo(function(g) return tbar(g) mod 4;end);
  index:=function(values)
    local key,value;
    key:=0;
    for value in values do
      if value=0 then return 0;fi;
      key:=3*key+value-1;
    od;
    return key+1;
  end;
  c:=AFSMemo(function(g,h,j)
    local key;
    key:=index([t(g),t(h),t(j)]);if key=0 then return 0;fi;
    return AFSC4PipC3[key];
  end);
  v:=AFSMemo(function(g,h,j,l)
    local key;
    key:=index([t(g),t(h),t(j),t(l)]);if key=0 then return 0;fi;
    return AFSMod1(AFSC4PipPhase4[key]);
  end);
  certificate:=rec(nativeCharacter1:=tn,integerCharacterDifferential:=residual,
    modulus:=4,orientationReduction:=sn,
    universalFlatTower:="gap/pip_c4_data.g",
    universalCFEquationsChecked:=256,universalPhaseEquationsChecked:=1024,
    proof:="native-degree1-cocycle-pulled-to-bar; reduction-mod2-is-orientation-pointwise");
  if IsBoundGlobal("AFSStage") then AFSStage(ctx,"stack_pip_C4_pullback");fi;
  return rec(status:="computed",state:=rec(n:=ctx.s,
    b:=AFSMemo(function(g,h) return (t(g) mod 2)*QuoInt(t(h),2);end),c:=c,v:=v,
    mcIndeterminacyAdjustment:=[],cfIndeterminacyAdjustment:=[],
    definingTowerOrigin:="universal-C4-pullback-independent-of-AHSS-primitive-choice",
    C4PullbackCertificate:=certificate,
    construction:="proved-orientation-character-pullback-of-complete-universal-C4-tower"));
end);

BindGlobal("AFSStackPipLift",function(C)
  local ctx,n,b,c,op,co,rows,i,row,solve,sol,adjust,v,mc,mccoeff,cfcoeff,Q,pulled;
  ctx:=C.ctx;
  pulled:=AFSPipC4FlatLift(C);if pulled<>fail then return pulled;fi;
  if not IsBound(C.pipLiftData) then
    return rec(status:="unresolved",reason:="p+ip defining tower is missing");fi;
  n:=C.pipLiftData.n;b:=C.pipLiftData.b;c:=C.pipLiftData.c;
  if not AFSStackSupportZero(ctx,1,0,AFSCoadd(0,[n,AFSComul(0,-1,ctx.s)])) then
    return rec(status:="unresolved",reason:="marked p+ip square requires canonical integral orientation cocycle");fi;
  if IsBoundGlobal("AFSStage") then AFSStage(ctx,"stack_pip_phase_lift");fi;
  op:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
  co:=C.H5U.coordinates(AFSNative(ctx,5,"U1s",op));
  if co=fail then Error("p+ip defining tower has a nonclosed top obstruction");fi;
  mccoeff:=List(C.mcLifts,z->0);cfcoeff:=List(C.H3.orders,z->0);
  if ForAny(co,z->z<>0) then
    # First use the full incoming image, including nonpermanent MC cycles.
    # Reevaluate the nonlinear tower after changing B; its actual residual
    # must then lie in the CF primary image, rather than being assumed zero.
    rows:=ShallowCopy(C.cfPrimaryRows);
    for mc in C.mcLifts do
      if IsBound(mc.obstructionCoordinates) then Add(rows,mc.obstructionCoordinates);
      else Add(rows,List(C.H5U.orders,z->0));fi;
    od;
    for i in [1..Length(C.H5U.orders)] do
      row:=List(C.H5U.orders,z->0);row[i]:=C.H5U.orders[i];Add(rows,row);
    od;
    solve:=AFSStackLatticeSolver(rows,Length(C.H5U.orders));sol:=solve(-co);
    if sol=fail then
      return rec(status:="unresolved",reason:="p+ip obstruction outside the full incoming image",
        obstructionCoordinates:=co);fi;
    mccoeff:=List(sol{[Length(C.H3.orders)+1..Length(C.H3.orders)+Length(C.mcLifts)]},z->z mod 2);
    for i in [1..Length(mccoeff)] do
      if mccoeff[i]=1 then b:=AFSCoadd(2,[b,C.mcLifts[i].a]);fi;
    od;
    if ForAny(mccoeff,z->z<>0) then
      Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=n,b:=b));
      c:=AFSSolve(ctx,4,"F2",Q);
      if c=fail then Error("p+ip MC adjustment failed its defining CF equation");fi;
      op:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
      co:=C.H5U.coordinates(AFSNative(ctx,5,"U1s",op));
      if co=fail then Error("p+ip adjusted obstruction is not closed");fi;
    fi;
    rows:=ShallowCopy(C.cfPrimaryRows);
    for i in [1..Length(C.H5U.orders)] do
      row:=List(C.H5U.orders,z->0);row[i]:=C.H5U.orders[i];Add(rows,row);
    od;
    solve:=AFSStackLatticeSolver(rows,Length(C.H5U.orders));sol:=solve(-co);
    if sol=fail then Error("p+ip MC adjustment did not remove the actual secondary obstruction");fi;
    cfcoeff:=List(sol{[1..Length(C.H3.orders)]},z->z mod 2);
    adjust:=AFSCombination(ctx,3,"F2",C.H3,cfcoeff);
    c:=AFSCoadd(2,[c,adjust]);
    op:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
  fi;
  v:=AFSSolve(ctx,5,"U1s",op);
  if v=fail then Error("p+ip CF indeterminacy adjustment failed the full primitive equation");fi;
  return rec(status:="computed",state:=rec(n:=n,b:=b,c:=c,v:=v,
    mcIndeterminacyAdjustment:=mccoeff,cfIndeterminacyAdjustment:=cfcoeff,
    construction:="canonical-orientation-torsion-with-full-phase-primitive"));
end);

BindGlobal("AFSStackPipSquare",function(ctx,x)
  local db,K,s3,beta,T1,T2,Gamma,gauge,target;
  db:=AFSCoboundary(ctx,"F2",x.b);
  K:=AFSCoadd(2,[AFSCup(1,2,x.b,2,x.b),AFSCup(2,2,x.b,3,db),AFSCup(0,1,ctx.s,2,x.b)]);
  s3:=AFSPipSignCube(ctx);beta:=AFSCoadd(2,[K,s3]);
  # Input reference-coordinate change; its diagonal output is (2s,0,beta).
  # The native output before integer reduction is C0=beta+Lambda2=K.
  T1:=AFSPipPhaseReferenceShift(ctx,1,x.b,x.c);
  T2:=AFSPipPhaseReferenceShift(ctx,2,AFSZero,K);
  Gamma:=AFSPipReferenceDiagonal(ctx,x.b,x.c);
  gauge:=AFSPipIntegerGaugePhase(ctx,K);
  target:=rec(a:=AFSZero,c:=beta,v:=AFSCoadd(1,[AFSComul(1,2,x.v),
      AFSComul(1,2,T1),Gamma,AFSComul(1,-1,T2),gauge]),
    construction:="canonical-torsion-square-with-explicit-integer-layer-gauge");
  if AFSStackAuditEnabled() and not AFSStackCheckFlat(ctx,target) then
    Error("marked p+ip square violates the lower flatness identity");fi;
  return rec(target:=target,nativeDoubledCFBeforeIntegerGauge:=K,
    inputPhaseCoordinateShift:=T1,outputPhaseCoordinateShift:=T2,
    referenceDiagonalPhase:=Gamma,integerGaugePhase:=gauge,
    integerGauge:=1,referenceDiagonalCF:=beta);
end);

BindGlobal("AFSExplicitPipStacking",function(C)
  local ctx,model,lower,lift,square,reduction,R,row,i,S,inv,result;
  ctx:=C.ctx;
  if not IsBoundGlobal("AFSPipReferenceDiagonal") then
    return rec(status:="unresolved",reason:="diagonal p+ip formula has not been loaded");fi;
  if C.summary.pip.status<>"computed" or not 2 in C.summary.pip.orders then
    return AFSFullStacking(C);fi;
  # Use the same full marked lower lifts in every relation, including the upper
  # one. Do not splice a relation onto an independently chosen lower basis.
  model:=AFSStackFromClassification(C);
  if model.status<>"computed" then return model;fi;
  lower:=AFSStackClassification(model);
  if lower.status<>"computed" then return lower;fi;
  lift:=AFSStackPipLift(C);
  if lift.status<>"computed" then return rec(status:="unresolved",reason:=lift.reason,lower:=lower);fi;
  if IsBoundGlobal("AFSStage") then AFSStage(ctx,"stack_pip_square");fi;
  square:=AFSStackPipSquare(ctx,lift.state);
  reduction:=AFSStackReduce(model,square.target,true);
  if reduction.status<>"computed" then
    return rec(status:="unresolved",reason:=reduction.reason,lower:=lower);fi;
  R:=List(lower.presentation,r->Concatenation(r,[0]));
  row:=List(lower.generators,g->0);
  for i in [1..Length(reduction.coordinates)] do row[i]:=-reduction.coordinates[i];od;
  Add(row,2);Add(R,row);
  S:=AFSSmith(R,Length(R),Length(lower.generators)+1);
  inv:=Concatenation(List([S.rank+1..Length(lower.generators)+1],i->0),
    Filtered(List(S.diag,AbsInt),x->x>1));
  result:=rec(status:="computed",scope:="full-3+1D-spin-half-affine-stacking",
    invariants:=Concatenation(List([1..C.summary.pip.free_rank],i->0),inv),
    lower:=lower,freePipRank:=C.summary.pip.free_rank,
    freePipCertificate:="free-associated-graded-quotient-splits-in-abelian-category",
    upperCompletion:="actual-marked-torsion-square-with-cochain-gauges",
    fullUpperPhaseWitness:=true,
    pipGenerator:=lift.state,pipSquare:=square,pipReduction:=reduction,
    fullPresentation:=R,fullSmith:=S,pipRelationCoordinates:=reduction.coordinates);
  return result;
end);

BindGlobal("AFSExplicitPipExport",function(C,result)
  local out,ctx,encode,x,s,w;
  out:=AFSStackExport(C,result);
  if not IsBound(result.pipGenerator) then return out;fi;
  ctx:=C.ctx;encode:=v->List(v,a->[NumeratorRat(a),DenominatorRat(a)]);
  x:=result.pipGenerator;s:=result.pipSquare;w:=result.pipReduction.witness;
  out.fullPresentation:=result.fullPresentation;
  out.fullSmithDiagonal:=result.fullSmith.diag;
  out.fullSmithRowTransform:=result.fullSmith.U;
  out.fullSmithColumnTransform:=result.fullSmith.V;
  out.pipGenerator:=rec(name:="P1",layer:=3,quotientOrder:=2,
    integer1:=AFSNative(ctx,1,"Zs",x.n),majorana2:=AFSNative(ctx,2,"F2",x.b),
    fermion3:=AFSNative(ctx,3,"F2",x.c),phase4:=encode(AFSNative(ctx,4,"U1s",x.v)),
    construction:=x.construction,mcIndeterminacyAdjustment:=x.mcIndeterminacyAdjustment,
    cfIndeterminacyAdjustment:=x.cfIndeterminacyAdjustment);
  if IsBound(x.C4PullbackCertificate) then
    out.pipGenerator.C4PullbackCertificate:=x.C4PullbackCertificate;
    out.pipGenerator.definingTowerOrigin:=x.definingTowerOrigin;
    Add(out.sourceFiles,"gap/pip_c4_data.g");
  fi;
  out.pipRelation:=rec(lowerCoordinates:=result.pipRelationCoordinates,
    squareCF3:=AFSNative(ctx,3,"F2",s.target.c),
    squarePhase4:=encode(AFSNative(ctx,4,"U1s",s.target.v)),
    referenceDiagonalPhase4:=encode(AFSNative(ctx,4,"U1s",s.referenceDiagonalPhase)),
    inputCoordinateShift4:=encode(AFSNative(ctx,4,"U1s",s.inputPhaseCoordinateShift)),
    outputCoordinateShift4:=encode(AFSNative(ctx,4,"U1s",s.outputPhaseCoordinateShift)),
    integerGaugePhase4:=encode(AFSNative(ctx,4,"U1s",s.integerGaugePhase)),
    integerGauge0:=s.integerGauge,cfGauge2:=AFSNative(ctx,2,"F2",w.cfGauge),
    phaseGauge3:=encode(AFSNative(ctx,3,"U1s",w.phaseGauge)),
    cfIncomingCoordinates:=w.cfIncoming,bosonicIncomingCoordinates:=w.bosonicIncoming,
    certificateLevel:="full-diagonal-formula-and-comparison-homotopy",
    checkedComparisonSupport:=w.checkedComparisonSupport);
  Append(out.sourceFiles,["gap/pip_coordinate_data.g","gap/pip_coordinates.g",
    "gap/pip_diagonal_data.g","gap/pip_stacking.g"]);
  return out;
end);
