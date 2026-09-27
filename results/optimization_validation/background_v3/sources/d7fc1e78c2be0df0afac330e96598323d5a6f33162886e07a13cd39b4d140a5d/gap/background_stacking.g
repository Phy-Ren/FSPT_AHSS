# Nonzero physical extension. The lower CA product is known in full.
# For the surviving canonical torsion p+ip lift the leading square is [omega].
# Missing lower carries are retained as the entire affine Ext^1 family.
BindGlobal("AFSBackgroundLowerStacking",function(C)
  local model;
  if Length(C.cfFinalBasis)=0 and Length(C.mcFinalBasis)=0 then
    return AFSStackBosonOnly(C);
  elif Length(C.mcFinalBasis)=0 then return AFSStackCFOnly(C);fi;
  model:=AFSStackFromClassification(C);
  if model.status<>"computed" then return model;fi;
  return AFSStackClassification(model);
end);

BindGlobal("AFSBackgroundFullStacking",function(C)
  local ctx,lower,X,BQ,result,co,mc,leading,indices,i,family,ambiguous,diagnostic;
  ctx:=C.ctx;
  if not AFSBackgroundNonzero(ctx) then Error("background stacking requires a nonzero cocycle");fi;
  if ctx.s=AFSZero then
    X:=AFSBackgroundIncomingState(ctx);
    BQ:=AFSBackgroundQuotient(C,X,rec(
      formula:="normalized-CA-H0-pip-boundary",cochainSource:="gap/pip_incoming_background.g",
      square:="(0,Sq1(omega),-Pontryagin(omega)/8)",
      ambiguity:="exact plus 8X, hence identical cyclic incoming subgroup"));
    if BQ.status<>"computed" then return BQ;fi;
    C.backgroundQuotient:=BQ;lower:=BQ.lower;
    C.summary.preH0IncomingGraded:=rec(majorana:=C.summary.majorana,
      complex_fermion:=C.summary.complex_fermion,bosonic:=C.summary.bosonic);
    C.summary.majorana:=BQ.graded.majorana;
    C.summary.complex_fermion:=BQ.graded.complex_fermion;
    C.summary.bosonic:=BQ.graded.bosonic;
    C.summary.h0PipIncoming:=rec(order:=BQ.incomingOrder,coordinates:=BQ.incomingCoordinates);
  else lower:=AFSBackgroundLowerStacking(C);fi;
  if lower.status<>"computed" then return lower;fi;
  result:=rec(status:="computed",scope:="full-3+1D-crystalline-spinless-affine-stacking",
    lower:=lower,freePipRank:=C.summary.pip.free_rank,
    freePipCertificate:="certified-surviving-integer-lattice-free-quotient-splits");
  if ForAny(C.summary.pip.orders,o->o<>0) then
    if ctx.s=AFSZero then Error("unitary integer H1 unexpectedly has torsion");fi;
    co:=C.H2.coordinates(AFSNative(ctx,2,"F2",ctx.omega2));
    mc:=AFSF2SolveRows(C.mcFinalBasis,co);
    if mc=fail then Error("surviving torsion p+ip square omega is outside permanent MC cycles");fi;
    indices:=Filtered([1..Length(lower.generators)],i->lower.generators[i].layer=2);
    if Length(indices)<>Length(mc) then Error("MC square basis mismatch");fi;
    leading:=List(lower.generators,g->0);
    for i in [1..Length(mc)] do leading[indices[i]]:=mc[i];od;
    ambiguous:=Filtered([1..Length(lower.generators)],i->lower.generators[i].layer<2);
    family:=AFSStackExtensionByTwo(lower,leading,ambiguous);
    result.pipExtensionCertificate:=family;
    result.pipSquareCertificate:=rec(method:="integer-sign-cocycle-gauge-leading-square",
      majoranaCohomologyClass:=co,majoranaCoordinates:=mc,
      identity:="2P has Majorana class omega after removing integer 2s",
      unknownCarries:=["complex-fermion","bosonic"],fullUpperPhaseWitness:=false);
    result.fullUpperPhaseWitness:=false;
    if family.status="computed" then
      result.invariants:=Concatenation(List([1..result.freePipRank],i->0),family.invariants);
      result.upperCompletion:="abstract-group-independent-of-all-CF-and-bosonic-carries";
    else
      result.status:="unresolved";
      result.reason:="unknown p+ip CF or bosonic carry changes the abstract group";
    fi;
  else
    result.invariants:=Concatenation(List([1..result.freePipRank],i->0),lower.invariants);
    result.upperCompletion:="no-torsion-pip-extension-required";
  fi;
  return result;
end);

BindGlobal("AFSBackgroundStackingExport",function(C,result)
  local out,wrapped;
  if IsBound(C.backgroundQuotient) then
    wrapped:=ShallowCopy(result);wrapped.lower:=C.backgroundQuotient.preQuotientLower;
    out:=AFSStackExport(C,wrapped);
    out.h0IncomingQuotient:=AFSBackgroundQuotientExport(C,C.backgroundQuotient);
    out.lowerBeforeH0Incoming:=out.lower;
    # The quotient export contains its own exact marked relation certificate.
    Unbind(out.lower);
  else out:=AFSStackExport(C,result);fi;
  return out;
end);
