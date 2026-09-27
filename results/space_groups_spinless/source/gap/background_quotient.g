# Quotient a complete marked CA stacking group by an actual H0 p+ip boundary.
# No operation in this file changes the pre-boundary classification object.
# The filtered quotients are computed from integer lattices, not from orders.

BindGlobal("AFSBackgroundSmithInvariants",function(S,width)
  return Concatenation(List([S.rank+1..width],i->0),
    Filtered(List(S.diag,AbsInt),x->x>1));
end);

# Z^m/row(R), filtered by the given generator layers. For F_i, take the
# integral kernel of the columns above i: U's zero rows are a saturated
# Z-basis of that left kernel. Their combinations of R generate R intersect
# the coordinate subgroup F_i. Quotienting out F_(i-1) then means dropping
# the lower columns. All matrices and combination witnesses are retained.
BindGlobal("AFSBackgroundFilteredPresentation",function(R,layers)
  local width,nrows,level,upper,indices,prefix,tail,S,kernel,intersections,
    projected,subgroup,Sgr,Ssub,record,graded,filtration,row;
  width:=Length(layers);nrows:=Length(R);
  if not ForAll(R,r->Length(r)=width and ForAll(r,IsInt)) then
    Error("background quotient requires an exact rectangular integer presentation");fi;
  if not ForAll(layers,l->l in [0,1,2]) then Error("unknown CA filtration layer");fi;
  graded:=rec();filtration:=[];
  for level in [0..2] do
    upper:=Filtered([1..width],i->layers[i]>level);
    indices:=Filtered([1..width],i->layers[i]=level);
    prefix:=Filtered([1..width],i->layers[i]<=level);
    tail:=List(R,r->r{upper});S:=AFSSmith(tail,nrows,Length(upper));
    kernel:=S.U{[S.rank+1..nrows]};
    intersections:=List(kernel,function(k)
      local sum,j;
      sum:=List([1..width],i->0);
      for j in [1..nrows] do sum:=sum+k[j]*R[j];od;
      return sum;
    end);
    if not ForAll(intersections,r->ForAll(upper,i->r[i]=0)) then
      Error("integer relation intersection has nonzero high-layer entries");fi;
    projected:=List(intersections,r->r{indices});
    subgroup:=List(intersections,r->r{prefix});
    Sgr:=AFSSmith(projected,Length(projected),Length(indices));
    Ssub:=AFSSmith(subgroup,Length(subgroup),Length(prefix));
    record:=rec(layer:=level,generatorIndices:=indices,prefixIndices:=prefix,
      upperIndices:=upper,highColumnMatrix:=tail,highColumnSmith:=S,
      relationCombinationRows:=kernel,intersectionRelationRows:=intersections,
      gradedPresentation:=projected,gradedSmith:=Sgr,
      gradedInvariants:=AFSBackgroundSmithInvariants(Sgr,Length(indices)),
      subgroupPresentation:=subgroup,subgroupSmith:=Ssub,
      subgroupInvariants:=AFSBackgroundSmithInvariants(Ssub,Length(prefix)));
    Add(filtration,record);
    if level=0 then graded.bosonic:=record.gradedInvariants;
    elif level=1 then graded.complex_fermion:=record.gradedInvariants;
    else graded.majorana:=record.gradedInvariants;fi;
  od;
  return rec(graded:=graded,filtration:=filtration);
end);

# Pure integer core. x is in the SAME marked basis as lower.presentation.
# x is a relation to add, not a tuple of independently quotiented layer labels.
BindGlobal("AFSBackgroundQuotientPresentation",function(lower,x,certificate)
  local width,R,S,oldS,sx,order,i,d,step,F,layers,q;
  if lower.status<>"computed" then return lower;fi;
  width:=Length(lower.generators);
  if Length(x)<>width or not ForAll(x,IsInt) then
    Error("incoming H0 coordinate width or coefficient type mismatch");fi;
  oldS:=AFSSmith(lower.presentation,Length(lower.presentation),width);
  if AFSBackgroundSmithInvariants(oldS,width)<>lower.invariants then
    Error("pre-quotient presentation disagrees with its invariants");fi;
  sx:=List([1..width],i->0);
  if width>0 then sx:=x*oldS.V;fi;
  order:=1;
  for i in [1..width] do
    if i>oldS.rank then
      if sx[i]<>0 then order:=0;break;fi;
    else
      d:=AbsInt(oldS.diag[i]);step:=QuoInt(d,Gcd(d,sx[i]));
      order:=Lcm(order,step);
    fi;
  od;
  if IsBound(certificate.orderDivides) and
     (order=0 or certificate.orderDivides mod order<>0) then
    Error("measured incoming order contradicts its cochain power certificate");fi;
  R:=List(lower.presentation,ShallowCopy);Add(R,ShallowCopy(x));
  S:=AFSSmith(R,Length(R),width);
  layers:=List(lower.generators,g->g.layer);
  F:=AFSBackgroundFilteredPresentation(R,layers);
  q:=ShallowCopy(lower);q.presentation:=R;q.smith:=S;
  q.invariants:=AFSBackgroundSmithInvariants(S,width);
  q.scope:="complete-CA-group-modulo-H0-pip-incoming";
  q.finalFiltrationCertificate:=rec(method:="integer-relation-intersections-after-cyclic-quotient",
    bosonic:=F.graded.bosonic,complex_fermion:=F.graded.complex_fermion,
    majorana:=F.graded.majorana,preQuotientCertificate:=lower.finalFiltrationCertificate);
  # Existing marked lifts remain valid representatives, but can be redundant
  # after this quotient. Their old quotientOrder is not the new graded order.
  q.backgroundMarkedGeneratorsMayBeRedundant:=true;
  return rec(status:="computed",preQuotientLower:=lower,lower:=q,
    incomingCoordinates:=ShallowCopy(x),incomingSmithCoordinates:=sx,
    incomingOrder:=order,incomingCertificate:=certificate,
    graded:=F.graded,filtration:=F.filtration,
    quotientCertificate:="append-actual-incoming-coordinate-row-and-compute-integral-filtered-intersections");
end);

# Put the complete incoming state itself into the marked MC basis. This
# avoids identifying cohomologous MC cochains without their nonclosed gauge.
# If [a] is nonzero, replacing a pivot MC class with [a] is invertible over F2.
# If [a]=0 but a is not literally zero, this wrapper refuses to guess a gauge.
BindGlobal("AFSBackgroundQuotient",function(C,X,certificate)
  local ctx,co,coords,pivot,model,old,T,i,g,lower,x,result,red,adjust;
  ctx:=C.ctx;
  if ForAny(GeneratorsOfGroup(ctx.G),g->ctx.s(g)<>0) then
    return rec(status:="unresolved",reason:="H0 integer background boundary wrapper requires unitary sign");fi;
  co:=C.H2.coordinates(AFSNative(ctx,2,"F2",X.a));
  if co=fail then Error("incoming H0 state's MC cochain is not closed");fi;
  coords:=AFSF2SolveRows(C.mcFinalBasis,co);
  if coords=fail then
    return rec(status:="unresolved",reason:="incoming H0 class is outside complete pre-quotient MC layer");fi;
  if ForAll(coords,z->z=0) and X.a<>AFSZero then
    return rec(status:="unresolved",reason:="cohomologically trivial nonzero incoming MC cochain requires an explicit gauge or prior background reduction");fi;
  model:=AFSStackFromClassification(C);
  if model.status<>"computed" then return model;fi;
  old:=List(model.data.majorana,g->g.name);T:=IdentityMat(Length(old));
  pivot:=PositionProperty(coords,z->z mod 2=1);
  if pivot<>fail then
    T[pivot]:=ShallowCopy(coords);
    g:=ShallowCopy(model.data.majorana[pivot]);g.state:=X;
    g.construction:="actual-H0-pip-boundary-used-as-marked-Majorana-lift";
    model.data.majorana[pivot]:=g;
    model.generators:=Concatenation(model.data.boson,model.data.fermion,model.data.majorana);
  fi;
  if AFSStackAuditEnabled() and not AFSStackCheckFlat(ctx,X) then
    Error("actual incoming H0 state fails its complete CA flatness equation");fi;
  lower:=AFSStackClassification(model);
  if lower.status<>"computed" then return lower;fi;
  x:=List(lower.generators,g->0);
  if pivot<>fail then
    x[Length(model.data.boson)+Length(model.data.fermion)+pivot]:=1;
    adjust:=rec(method:="incoming-state-is-literally-a-marked-generator");
  elif X.c=AFSZero and X.v=AFSZero then
    adjust:=rec(method:="literal-zero-incoming-state");
  else
    red:=AFSStackReduce(model,X,true);
    if red.status<>"computed" then return red;fi;
    for i in [1..Length(red.coordinates)] do x[i]:=red.coordinates[i];od;
    adjust:=rec(method:="zero-MC-full-CF-and-phase-cochain-reduction",witness:=red.witness);
  fi;
  result:=AFSBackgroundQuotientPresentation(lower,x,certificate);
  result.basisChange:=rec(oldMCNames:=old,newMCNames:=List(model.data.majorana,g->g.name),
    newMCCohomologyRowsInOldBasis:=T,incomingMCCohomologyCoordinates:=co,
    incomingMCClassCoordinates:=coords);
  if pivot<>fail then result.basisChange.replacedMCPivot:=pivot;fi;
  result.incomingState:=X;result.incomingCoordinateWitness:=adjust;
  result.model:=model;
  return result;
end);

# Export JSON-compatible mathematics without passing the new H0 witness to
# AFSStackExport's unrelated legacy boundary-type switch. Both the complete
# pre-quotient cochain witnesses and the new integral quotient are preserved.
BindGlobal("AFSBackgroundQuotientExport",function(C,result)
  local old,out,q,F,record,encode,scheme,w;
  if result.status<>"computed" then return result;fi;
  old:=AFSStackExport(C,rec(status:="computed",lower:=result.preQuotientLower,
    invariants:=result.preQuotientLower.invariants));
  out:=ShallowCopy(old);q:=result.lower;out.invariants:=q.invariants;
  out.scope:=q.scope;out.lower:=ShallowCopy(old.lower);
  out.lower.presentation:=q.presentation;out.lower.smithDiagonal:=q.smith.diag;
  out.lower.smithRowTransform:=q.smith.U;out.lower.smithColumnTransform:=q.smith.V;
  out.lower.invariants:=q.invariants;out.lower.scope:=q.scope;
  out.lower.finalFiltrationCertificate:=q.finalFiltrationCertificate;
  out.lower.backgroundMarkedGeneratorsMayBeRedundant:=true;
  # One extra relation, with its own correctly named certificate type.
  out.lower.witnesses:=ShallowCopy(old.lower.witnesses);
  Add(out.lower.witnesses,rec(certificateLevel:="actual-H0-pip-boundary-relation",
    coordinateRow:=result.incomingCoordinates,incomingOrder:=result.incomingOrder,
    certificate:=result.incomingCertificate));
  out.backgroundQuotient:=rec(preQuotientLower:=old.lower,
    incomingCoordinates:=result.incomingCoordinates,
    incomingSmithCoordinates:=result.incomingSmithCoordinates,
    incomingOrder:=result.incomingOrder,certificate:=result.incomingCertificate,
    graded:=result.graded,filtration:=result.filtration,
    quotientCertificate:=result.quotientCertificate);
  if IsBound(result.basisChange) then out.backgroundQuotient.basisChange:=result.basisChange;fi;
  if IsBound(result.incomingState) then
    encode:=v->List(v,z->[NumeratorRat(z),DenominatorRat(z)]);
    out.backgroundQuotient.incomingState:=rec(
      majorana2:=AFSNative(C.ctx,2,"F2",result.incomingState.a),
      fermion3:=AFSNative(C.ctx,3,"F2",result.incomingState.c),
      phase4:=encode(AFSNative(C.ctx,4,"U1s",result.incomingState.v)));
  fi;
  if IsBound(result.incomingCoordinateWitness) then
    scheme:=result.incomingCoordinateWitness;
    out.backgroundQuotient.coordinateMethod:=scheme.method;
    if IsBound(scheme.witness) then
      w:=scheme.witness;
      out.backgroundQuotient.coordinateWitness:=rec(cfIncomingCoordinates:=w.cfIncoming,
        bosonicIncomingCoordinates:=w.bosonicIncoming,
        cfGauge2:=AFSNative(C.ctx,2,"F2",w.cfGauge),
        phaseGauge3:=List(AFSNative(C.ctx,3,"U1s",w.phaseGauge),z->[NumeratorRat(z),DenominatorRat(z)]),
        checkedComparisonSupport:=w.checkedComparisonSupport);
    fi;
  fi;
  Add(out.sourceFiles,"gap/background_quotient.g");
  return out;
end);
