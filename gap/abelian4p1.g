# Exact four-data classification for finite commuting abelian products.
# This specialized engine uses the same cochain source/product/gauge API as
# the cyclic pilot. Its charge obstruction and incoming H^3 are NOT omitted.
Read(Concatenation(U1_ROOT,"/formulas/examples/cyclic_4p1.g"));

BindGlobal("U1AbelianFourContext",function(factors)
  local G,R,c;
  if Length(factors)=0 or ForAny(factors,n->not IsInt(n) or n<2) then
    Error("A nonempty list of cyclic factors of order at least two is required");fi;
  G:=AbelianGroup(IsPcpGroup,factors);
  if List(GeneratorsOfGroup(G),Order)<>factors then Error("Abelian coordinate orders changed");fi;
  R:=U1FiniteHolonomyResolution(G,7);
  c:=U1NewContext(G,R,U1Zero,U1Zero,U1Zero,0);
  c.backgroundClosureCertificate:=rec(actions:=[c.s,c.r,c.omega],integralTwistedCoboundary:=true,halfIntegralOmega:=true);
  c.fourCompletionChecks:=0;c.completedStateChecks:=0;c.reductionWitnesses:=[];
  return c;
end);
BindGlobal("U1AbelianFourCombination",function(c,roots,coeffs)
  local out,i;
  out:=U1FourZero();
  for i in [1..Length(coeffs)] do
    if coeffs[i]<>0 then out:=U1FourProduct(c,out,U1FourPower(c,roots[i],coeffs[i]));fi;
  od;return out;
end);
BindGlobal("U1AbelianFourCoordinate",function(c,index,order)
  local a,x,xx,axx;
  a:=g->g!.exponents[index];
  x:=function(g,h) return QuoInt(g!.exponents[index]+h!.exponents[index],order);end;
  xx:=U1Cup(c,2,x,"Z",2,x,"Z",0,false);
  axx:=U1Cup(c,1,a,"Z",4,xx,"Z",0,false);
  return rec(a:=a,x:=x,
    neutral:=rec(e_p:=x,n_p:=U1Zero,n_p2:=U1Zero,nu_p3:=U1Scale(1/(3*order),axx)),
    ci:=rec(e_p:=U1Zero,n_p:=x,n_p2:=U1Zero,nu_p3:=U1Scale(1/(6*order),axx)));
end);
# A class-only accelerator. It never supplies a phase primitive and never
# replaces the completed bar roots, stacking, or cylinder gauges below.
BindGlobal("U1AbelianFourChargeClass",function(c,H,q,mode)
  local fast,reference;
  if not mode in ["bar","native","compare"] then Error("Unknown abelian charge-primary mode");fi;
  if c.s<>U1Zero or c.r<>U1Zero or c.omega<>U1Zero or c.vcd<>0 then
    Error("Unsigned abelian native charge class requires the exact trivial background");fi;
  if Length(q)<>Dimension(c.R)(4) or not ForAll(q,IsInt) or
    ForAny(U1ApplyDifferential(c,4,"Zr",q),x->x<>0) then
    Error("A charge primary input must be an integral closed native four-cochain");fi;
  if H.degree<>6 or H.coefficient<>"U1s" or not IsIdenticalObj(H,U1Cohomology(c,6,"U1s")) then
    Error("The charge primary target has the wrong context");fi;
  if mode<>"bar" then
    fast:=U1NativeSq2U1Coordinates(c,4,List(q,x->x mod 2),H);
  fi;
  if mode<>"native" then
    reference:=H.coordinates(U1Native(c,6,"U1s",U1ChargeSource(c,4,U1Bar(c,4,"Zr",q))));
    if reference=fail then Error("The bar charge obstruction is not closed");fi;
  fi;
  if mode="compare" and fast<>reference then Error("Native and bar degree-four charge classes disagree");fi;
  if mode="bar" then return reference;fi;
  return fast;
end);
BindGlobal("U1AbelianFourData",function(factors,options...)
  local c,HS,HQ,HP,HO,HI1,HI3,chargeBasis,phaseBasis,sourceMap,K,Ki,
    chargeStates,neutralStates,ciStates,coordinates,sheetCoordinates,checkSmith,
    roots,names,relations,witnesses,checks,np,nq,ns,total,i,j,v,a,source,
    completed,q,p,gauge,co,rel,reduceCharge,reducePhase,makeRelation,S,orders,
    fp,fq,fc,fe,perm,invperm,result,commutators,comm,preIncomingOrder,
    incomingRows,expectedOrder,relationCheck,original,shifted,delta,ix,rootPairs,chargeMode;
  c:=U1AbelianFourContext(factors);
  chargeMode:="bar";if Length(options)>0 then chargeMode:=options[1];fi;
  if not chargeMode in ["bar","native","compare"] then Error("Invalid abelian charge-primary mode");fi;
  Print("U1_ABELIAN stage=cohomology factors=",factors," cpu_ms=",Runtime(),"\n");
  HS:=U1Cohomology(c,2,"Zs");HQ:=U1Cohomology(c,4,"Zr");
  HP:=U1Cohomology(c,5,"U1s");HO:=U1Cohomology(c,6,"U1s");
  HI1:=U1Cohomology(c,1,"Zs");HI3:=U1Cohomology(c,3,"Zr");
  if HI1.orders<>[] then Error("A finite unsigned group has nonzero H1(Z)");fi;
  chargeBasis:=List(HQ.generators,x->U1Bar(c,4,"Zr",x));
  phaseBasis:=List(HP.generators,x->U1Bar(c,5,"U1s",x));
  sourceMap:=List(HQ.generators,q->U1AbelianFourChargeClass(c,HO,q,chargeMode));
  if fail in sourceMap then Error("A charge obstruction is not closed");fi;
  K:=U1MapKernel(sourceMap,HO.orders,Length(chargeBasis));
  if K=[] then Ki:=[];else Ki:=Inverse(K);fi;
  chargeStates:=[];witnesses:=[];checks:=[];
  Print("U1_ABELIAN stage=charge_lifts target=",HO.orders," map=",sourceMap," cpu_ms=",Runtime(),"\n");
  for v in K do
    a:=rec(charge:=U1CochainCombination(chargeBasis,v));
    completed:=U1SolveData(c,6,"U1s",U1ChargeSource(c,4,a.charge));
    if completed=fail then Error("Charge obstruction kernel did not complete");fi;
    q:=rec(e_p:=U1Zero,n_p:=U1Zero,n_p2:=a.charge,nu_p3:=completed.primitive);
    Add(checks,U1FourCheck(c,q));Add(chargeStates,q);
    Add(witnesses,rec(kind:="charge-lift",chargeCohomology:=v,nativeSource:=completed.nativeObstruction,nativePhase:=completed.nativePrimitive));
  od;
  coordinates:=List([1..Length(factors)],i->U1AbelianFourCoordinate(c,i,factors[i]));
  sheetCoordinates:=List(coordinates,a->HS.coordinates(U1Native(c,2,"Zs",a.x)));
  if fail in sheetCoordinates or Product(HS.orders)<>Product(factors) then Error("Incorrect abelian H2 sheet rank/order");fi;
  checkSmith:=U1Smith(Concatenation(sheetCoordinates,DiagonalMat(HS.orders)),Length(sheetCoordinates)+Length(HS.orders),Length(HS.orders));
  if checkSmith.rank<>Length(HS.orders) or ForAny(checkSmith.diag,x->AbsInt(x)<>1) then Error("Pulled-back sheets do not generate H2");fi;
  neutralStates:=List(coordinates,a->a.neutral);ciStates:=List(coordinates,a->a.ci);
  for a in Concatenation(neutralStates,ciStates) do Add(checks,U1FourCheck(c,a));od;
  np:=Length(HP.orders);nq:=Length(chargeStates);ns:=Length(factors);total:=np+nq+2*ns;
  roots:=Concatenation(List(phaseBasis,p->rec(e_p:=U1Zero,n_p:=U1Zero,n_p2:=U1Zero,nu_p3:=p)),chargeStates,ciStates,neutralStates);
  names:=Concatenation(List([1..np],i->Concatenation("phase_",String(i))),List([1..nq],i->Concatenation("charge_",String(i))),List([1..ns],i->Concatenation("CI_",String(i))),List([1..ns],i->Concatenation("E8_",String(i))));
  relations:=[];
  makeRelation:=function(pco,qco,ci,e)
    return Concatenation(pco,qco,ci,e);
  end;
  reducePhase:=function(a)
    local w,reduced,pc,primitive;
    if a.e_p<>U1Zero or a.n_p<>U1Zero then Error("Phase reduction requires removed sheets");fi;
    w:=U1Solve(c,4,"Zr",U1Scale(-1,a.n_p2));
    if w=fail then Error("A purported exact charge is not exact");fi;
    reduced:=U1FourGauge(c,a,U1Zero,U1Zero,w);reduced.n_p2:=U1Zero;
    U1FourCheck(c,reduced);
    pc:=HP.coordinates(U1Native(c,5,"U1s",reduced.nu_p3));
    if pc=fail then Error("Reduced shared phase is not closed");fi;
    primitive:=U1SolveData(c,5,"U1s",U1Add(reduced.nu_p3,U1Scale(-1,U1CochainCombination(phaseBasis,pc))));
    if primitive=fail then Error("Shared phase coordinate left an unrecorded remainder");fi;
    Add(witnesses,rec(kind:="phase-reduction",nativeChargeGauge:=U1Native(c,3,"Zr",w),phaseCoordinates:=pc,nativePhasePrimitive:=primitive.nativePrimitive,nativeResidualPhase:=primitive.nativeObstruction));
    return pc;
  end;
  reduceCharge:=function(a)
    local qc,pc,target,diff;
    U1FourCheck(c,a);
    qc:=HQ.coordinates(U1Native(c,4,"Zr",a.n_p2));
    if qc=fail then Error("Reduced charge is not closed");fi;
    if nq>0 then qc:=qc*Ki;fi;
    if not ForAll(qc,IsInt) then Error("Reduced charge left obstruction kernel");fi;
    target:=U1AbelianFourCombination(c,chargeStates,qc);
    diff:=U1FourProduct(c,a,U1FourInverse(c,target));
    diff.e_p:=U1Zero;diff.n_p:=U1Zero;
    pc:=reducePhase(diff);return rec(charge:=qc,phase:=pc);
  end;
  for i in [1..np] do
    rel:=List([1..total],j->0);rel[i]:=HP.orders[i];Add(relations,rel);
  od;
  Print("U1_ABELIAN stage=root_relations cpu_ms=",Runtime(),"\n");
  for i in [1..Length(HQ.orders)] do
    v:=List(HQ.orders,x->0);v[i]:=HQ.orders[i];v:=v*Ki;
    if not ForAll(v,IsInt) then Error("Charge relation left obstruction kernel");fi;
    a:=U1AbelianFourCombination(c,chargeStates,v);p:=reducePhase(a);
    Add(relations,makeRelation(-p,v,List(factors,x->0),List(factors,x->0)));
    Add(witnesses,rec(kind:="charge-root",coefficients:=v,phaseCoordinates:=p));
  od;
  for i in [1..2*ns] do
    ix:=((i-1) mod ns)+1;
    if i<=ns then a:=ciStates[ix];else a:=neutralStates[ix];fi;
    a:=U1FourPower(c,a,factors[ix]);U1FourCheck(c,a);
    v:=U1Zero;q:=U1Zero;
    if i<=ns then q:=U1Scale(-1,coordinates[ix].a);else v:=U1Scale(-1,coordinates[ix].a);fi;
    a:=U1FourGauge(c,a,v,q,U1Zero);a.e_p:=U1Zero;a.n_p:=U1Zero;
    co:=reduceCharge(a);rel:=makeRelation(-co.phase,-co.charge,List(factors,x->0),List(factors,x->0));
    rel[np+nq+i]:=factors[ix];Add(relations,rel);
    Add(witnesses,rec(kind:="sheet-root",index:=i,order:=factors[ix],nativeNeutralGauge:=U1Native(c,1,"Zs",v),nativeCIGauge:=U1Native(c,1,"Zs",q),chargeCoordinates:=co.charge,phaseCoordinates:=co.phase));
  od;
  S:=U1Smith(relations,Length(relations),total);preIncomingOrder:=Product(List([1..S.rank],i->AbsInt(S.diag[i])));
  if S.rank<>total or preIncomingOrder<>Product(HP.orders)*Product(HQ.orders)*Product(factors)^2/AbsInt(DeterminantMat(K)) then Error("Pre-incoming filtration order failed");fi;
  incomingRows:=[];
  Print("U1_ABELIAN stage=incoming_charge count=",Length(HI3.orders)," cpu_ms=",Runtime(),"\n");
  for i in [1..Length(HI3.generators)] do
    gauge:=U1Bar(c,3,"Zr",HI3.generators[i]);
    # Check vacuum and every lower-root orbit: no state-dependent incoming
    # effect may be silently replaced by the vacuum image.
    for j in [0..nq+2*ns] do
      if j=0 then original:=U1FourZero();else original:=roots[np+j];fi;
      shifted:=U1FourGauge(c,original,U1Zero,U1Zero,gauge);
      delta:=U1FourProduct(c,shifted,U1FourInverse(c,original));
      delta.e_p:=U1Zero;delta.n_p:=U1Zero;
      co:=reduceCharge(delta);
      rel:=makeRelation(co.phase,co.charge,List(factors,x->0),List(factors,x->0));
      Add(relations,rel);Add(incomingRows,rel);
      Add(witnesses,rec(kind:="incoming-charge-gauge",index:=i,baseRoot:=j,phaseCoordinates:=co.phase,chargeCoordinates:=co.charge,nativeGauge:=HI3.generators[i]));
    od;
  od;
  S:=U1Smith(relations,Length(relations),total);
  orders:=Filtered(List([1..S.rank],i->AbsInt(S.diag[i])),x->x>1);
  commutators:=[];rootPairs:=Combinations([np+1..total],2);
  Print("U1_ABELIAN stage=commutators count=",Length(rootPairs)," cpu_ms=",Runtime(),"\n");
  for v in rootPairs do
    a:=U1FourProduct(c,roots[v[1]],roots[v[2]]);
    q:=U1FourProduct(c,roots[v[2]],roots[v[1]]);
    comm:=U1FourProduct(c,a,U1FourInverse(c,q));
    comm.e_p:=U1Zero;comm.n_p:=U1Zero;
    co:=reduceCharge(comm);rel:=makeRelation(co.phase,co.charge,List(factors,x->0),List(factors,x->0));
    relationCheck:=U1IntegerSolveMatrix(relations,Length(relations),total,rel);
    if relationCheck=fail then Error("Nontrivial commutator survived the full gauge quotient");fi;
    Add(commutators,rec(roots:=v,reducedCoordinates:=rel,relationCoefficients:=relationCheck));
  od;
  fp:=U1Filtration(relations,total,0,np);fq:=U1Filtration(relations,total,np,nq);
  fc:=U1Filtration(relations,total,np+nq,ns);fe:=U1Filtration(relations,total,np+nq+ns,ns);
  perm:=Concatenation([np+nq+ns+1..total],[np+nq+1..np+nq+ns],[np+1..np+nq],[1..np]);
  result:=rec(theory:="U(1)^f insulator",spatialDimension:=4,orderedFields:=["e_2","n_2","n_4","nu_5"],
    group:=rec(family:="internal_abelian",factors:=factors),background:=rec(s:=0,r:=0,omega:=0),
    scope:="Complete original four-data relative model for unsigned commuting finite abelian products; intrinsic pair excluded",
    physicalClassificationCertified:=false,physicalScopeCaveat:="Independent bordism comparison remains separate from this formula computation",
    torsion:=orders,freeRank:=total-S.rank,actualGroupOrder:=Product(orders),presentationGeneratorCount:=total,
    presentation:=List(relations,row->row{perm}),
    generators:=List(perm,i->rec(kind:=names[i],nativeState:=U1FourNative(c,roots[i]))),
    finalFiltration:=rec(e:=fe,n:=fc,charge:=fq,phase:=fp),
    cohomology:=rec(sheet:=HS.orders,charge:=HQ.orders,phase:=HP.orders,terminalObstruction:=HO.orders),
    chargeObstructionMap:=sourceMap,chargeKernelLattice:=K,sheetGeneratorCoordinates:=sheetCoordinates,
    chargePrimaryMode:=chargeMode,chargePrimaryCompared:=chargeMode="compare",
    incomingCohomology:=rec(sheet:=HI1.orders,charge:=HI3.orders),incomingRelations:=List(incomingRows,row->row{perm}),
    preIncomingOrder:=preIncomingOrder,witnesses:=witnesses,commutatorWitnesses:=commutators,
    witnessCoordinateOrder:=names,outputColumnPermutation:=perm,
    nativeCompletionChecks:=c.fourCompletionChecks,resolutionDimensions:=List([0..7],k->Dimension(c.R)(k)),
    differentialMatrices:=rec(Zs:=List([0..6],k->U1Differential(c,k,"Zs")),Zr:=List([0..6],k->U1Differential(c,k,"Zr"))),
    sourceConvention:=rec(calibration:="sheet-linear",cubic:="1/6",epsilon:=0),
    formulaWorkerCalls:=0,runtime:=rec(gapVersion:=GAPInfo.Version,hapVersion:=PackageInfo("hap")[1].Version));
  if IsBound(c.workerCalls) then result.formulaWorkerCalls:=c.workerCalls;fi;
  return result;
end);
