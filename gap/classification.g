# Full group presentations from exact charge/CI lifts, products and gauges.
# The default 2+1D scope is relative to uniform IQH (n0=0).
BindGlobal("U1Vacuum",function() return rec(sheet:=U1Zero,charge:=U1Zero,phase:=U1Zero);end);
BindGlobal("U1IntegerSource",function(c,d,sheet)
  if sheet=U1Zero then return U1Zero;fi;
  return U1Formula(c,"integer_obstruction",d,rec(sheet:=sheet,charge:=U1Zero),rec(),fail,d+1);
end);
BindGlobal("U1Source",function(c,d,state)
  local source;
  if IsBound(state.sourceCache) and IsBound(state.sourceCache.context) and
      IsIdenticalObj(state.sourceCache.context,c) and state.sourceCache.dimension=d and
      state.sourceCache.sheet=state.sheet and state.sourceCache.charge=state.charge then return state.sourceCache.source;fi;
  if state.sheet=U1Zero then source:=U1ChargeSource(c,d,state.charge);
  else source:=U1Formula(c,"source",d,state,rec(),fail,d+2);fi;
  state.sourceCache:=rec(context:=c,dimension:=d,sheet:=state.sheet,charge:=state.charge,source:=source);
  return source;
end);
BindGlobal("U1Product",function(c,d,a,b)
  local extra,charge,phase;
  extra:=rec(sheet_prime:=b.sheet,charge_prime:=b.charge);
  charge:=U1Add(a.charge,b.charge);
  if a.sheet<>U1Zero and b.sheet<>U1Zero then
    charge:=U1Add(charge,U1Formula(c,"integer_product",d,a,extra,fail,d));fi;
  if a.sheet=U1Zero and b.sheet=U1Zero then phase:=U1ChargeProduct(c,d,a.charge,b.charge);
  else phase:=U1Formula(c,"product",d,a,extra,"phase",d+1);fi;
  return rec(sheet:=U1Add(a.sheet,b.sheet),charge:=charge,phase:=U1Add(U1Add(a.phase,b.phase),phase));
end);
BindGlobal("U1Inverse",function(c,d,a)
  local b,extra;
  b:=rec(sheet:=U1Scale(-1,a.sheet),charge:=U1Scale(-1,a.charge),phase:=U1Zero);
  if a.sheet<>U1Zero then
    extra:=U1Formula(c,"integer_product",d,a,rec(sheet_prime:=b.sheet,charge_prime:=b.charge),fail,d);
    b.charge:=U1Add(b.charge,U1Scale(-1,extra));fi;
  b.phase:=U1Scale(-1,U1Product(c,d,a,b).phase);return b;
end);
BindGlobal("U1Power",function(c,d,state,power)
  local out,a,n;
  if not IsInt(power) then Error("stacking exponent must be an integer");fi;
  out:=U1Vacuum();n:=power;a:=state;
  if n<0 then a:=U1Inverse(c,d,a);n:=-n;fi;
  while n>0 do
    if n mod 2=1 then out:=U1Product(c,d,out,a);fi;
    n:=QuoInt(n,2);if n>0 then a:=U1Product(c,d,a,a);fi;
  od;return out;
end);
BindGlobal("U1Combination",function(c,d,states,coeffs)
  local out,i;
  out:=U1Vacuum();
  for i in [1..Length(coeffs)] do
    if coeffs[i]<>0 then out:=U1Product(c,d,out,U1Power(c,d,states[i],coeffs[i]));fi;
  od;return out;
end);
BindGlobal("U1Gauge",function(c,d,a,u,v)
  local extra,out;
  if u=U1Zero and v=U1Zero then return a;fi;
  if d=2 then
    if u<>U1Zero then Error("No sheet gauge exists in 2+1D");fi;
    return rec(sheet:=a.sheet,charge:=U1Add(a.charge,U1Coboundary(c,"Zr",v)),phase:=U1Add(a.phase,U1ChargeGauge(c,d,a.charge,v)));
  fi;
  extra:=rec(sheet_parameter:=u,charge_parameter:=v);
  out:=rec(sheet:=U1Add(a.sheet,U1Coboundary(c,"Zs",u)),
    charge:=U1Formula(c,"gauge",d,a,extra,"charge",d),
    phase:=U1Add(a.phase,U1Formula(c,"gauge",d,a,extra,"phase",d+1)));
  return out;
end);
BindGlobal("U1IntegerSolveMatrix",function(M,n,m,b)
  local s,w,y,i;
  if m=0 then return List([1..n],i->0);fi;
  s:=U1Smith(M,n,m);w:=b*s.V;y:=List([1..n],i->0);
  for i in [1..m] do
    if i<=s.rank then
      if w[i] mod s.diag[i]<>0 then return fail;fi;
      y[i]:=w[i]/s.diag[i];
    elif w[i]<>0 then return fail;fi;
  od;return y*s.U;
end);
BindGlobal("U1MapKernel",function(M,orders,rank)
  local t,A,s,K;
  t:=Length(orders);if rank=0 then return [];fi;
  if t=0 then return IdentityMat(rank);fi;
  if ForAny(orders,x->x<=0) then Error("Obstruction target must be finite");fi;
  A:=Concatenation(M,DiagonalMat(orders));s:=U1Smith(A,rank+t,t);
  K:=List(s.U{[s.rank+1..rank+t]},row->row{[1..rank]});
  if Length(K)<>rank or RankMat(K)<>rank then Error("Obstruction kernel lattice rank mismatch");fi;
  return K;
end);
BindGlobal("U1MapPreimage",function(M,orders,rank,b)
  local out;
  if Length(orders)=0 then return List([1..rank],i->0);fi;
  out:=U1IntegerSolveMatrix(Concatenation(M,DiagonalMat(orders)),rank+Length(orders),Length(orders),b);
  if out=fail then return fail;fi;return out{[1..rank]};
end);
BindGlobal("U1CochainCombination",function(fs,coeffs)
  local out,i;out:=U1Zero;
  for i in [1..Length(coeffs)] do out:=U1Add(out,U1Scale(coeffs[i],fs[i]));od;return out;
end);
BindGlobal("U1ClosedPhaseCoordinates",function(c,d,H,f)
  local native,coords;
  native:=U1Native(c,d+1,"U1s",f);coords:=H.coordinates(native);
  if coords=fail then Error("Expected a closed terminal phase");fi;
  return coords;
end);
BindGlobal("U1ApplyDifferential",function(c,k,coeff,vector)
  if Dimension(c.R)(k+1)=0 then return [];fi;
  if vector=[] then return List([1..Dimension(c.R)(k+1)],i->0);fi;
  return vector*U1Differential(c,k,coeff);
end);
BindGlobal("U1CheckCompletedState",function(c,d,state)
  local sheet,charge,phase,integerSource,source;
  sheet:=U1Native(c,d-2,"Zs",state.sheet);charge:=U1Native(c,d,"Zr",state.charge);
  phase:=U1Native(c,d+1,"U1s",state.phase);
  integerSource:=U1Native(c,d+1,"Zr",U1IntegerSource(c,d,state.sheet));
  source:=U1Native(c,d+2,"U1s",U1Source(c,d,state));
  if ForAny(U1ApplyDifferential(c,d-2,"Zs",sheet),x->x<>0) then Error("Completed CI sheet is not closed");fi;
  if U1ApplyDifferential(c,d,"Zr",charge)<>integerSource then Error("Completed charge does not solve the integer source");fi;
  if ForAny(U1ApplyDifferential(c,d+1,"Zs",phase)-source,x->U1Mod1(x)<>0) then Error("Completed phase does not solve its native source");fi;
  if ForAny(U1ApplyDifferential(c,d+1,"Zr",integerSource),x->x<>0) then Error("Integer source is not closed");fi;
  if ForAny(U1ApplyDifferential(c,d+2,"Zs",source),x->U1Mod1(x)<>0) then Error("Terminal source is not closed");fi;
  if not IsBound(c.completedStateChecks) then c.completedStateChecks:=0;fi;
  c.completedStateChecks:=c.completedStateChecks+1;
  return rec(nativeSheet:=sheet,nativeCharge:=charge,nativePhase:=phase);
end);
BindGlobal("U1ReduceVacuum",function(c,d,state)
  local a,u,v,record;
  a:=state;record:=rec(nativeSheetParameter:=[],nativeChargeParameter:=[]);
  if a.sheet<>U1Zero then
    if d=2 then Error("Uniform IQH is not a gauge degree of freedom");fi;
    u:=U1Solve(c,d-2,"Zs",U1Scale(-1,a.sheet));
    if u=fail then Error("Requested sheet reduction is not exact");fi;
    record.nativeSheetParameter:=U1Native(c,d-3,"Zs",u);
    a:=U1Gauge(c,d,a,u,U1Zero);
  fi;
  v:=U1Solve(c,d,"Zr",U1Scale(-1,a.charge));
  if v=fail then Error("Requested charge reduction is not exact");fi;
  record.nativeChargeParameter:=U1Native(c,d-1,"Zr",v);
  a:=U1Gauge(c,d,a,U1Zero,v);U1CheckCompletedState(c,d,a);
  record.nativeFinalPhase:=U1Native(c,d+1,"U1s",a.phase);
  if not IsBound(c.reductionWitnesses) then c.reductionWitnesses:=[];fi;
  Add(c.reductionWitnesses,record);return a.phase;
end);
# Presentation of the indicated filtration subquotient. Relations involving
# later generators are eliminated over Z, not simply discarded.
BindGlobal("U1Filtration",function(relations,total,start,count)
  local after,m,A,S,ker,rels,j,T;
  m:=Length(relations);after:=[start+count+1..total];
  if count=0 then return rec(torsion:=[],freeRank:=0,presentation:=[]);fi;
  if m=0 then return rec(torsion:=[],freeRank:=count,presentation:=[]);fi;
  if Length(after)=0 then ker:=IdentityMat(m);
  else
    A:=List(relations,row->row{after});S:=U1Smith(A,m,Length(after));
    ker:=S.U{[S.rank+1..m]};
  fi;
  if ker=[] then rels:=[];
  else rels:=List(ker*relations,row->row{[start+1..start+count]});fi;
  T:=U1Smith(rels,Length(rels),count);
  return rec(torsion:=Filtered(List([1..T.rank],i->AbsInt(T.diag[i])),x->x>1),
    freeRank:=count-T.rank,presentation:=rels);
end);

# Complete the entire signed H1 lattice for a rank-three affine group. Both
# obstruction targets are finite because their degrees exceed vcd=3. The
# terminal map is additive only after quotienting by the charge-source image;
# its actual lift uses full stacking, including the nonlinear charge twister.
BindGlobal("U1AffineSheetLattice",function(c,HQ,HO,chargeBasis,sourceMap)
  local HC,HI,basis,integerMap,K3,seeds,v,a,q,terminalMap,quotient,inds,
    quotientOrders,projected,K4,K,Ki,states,orders,relations,witnesses,co,
    adjustment,phase,residual,i,j,order,relation;
  HC:=U1Cohomology(c,1,"Zs");HI:=U1Cohomology(c,4,"Zr");
  if ForAny(HI.orders,x->x<=0) or ForAny(HO.orders,x->x<=0) then
    Error("Affine sheet obstruction targets must be finite above vcd=3");fi;
  basis:=List(HC.generators,x->U1Bar(c,1,"Zs",x));
  integerMap:=List(basis,n->HI.coordinates(U1Native(c,4,"Zr",U1IntegerSource(c,3,n))));
  if fail in integerMap then Error("CI integer obstruction is not closed");fi;
  K3:=U1MapKernel(integerMap,HI.orders,Length(basis));seeds:=[];
  for v in K3 do
    a:=rec(sheet:=U1CochainCombination(basis,v),charge:=U1Zero,phase:=U1Zero);
    q:=U1Solve(c,4,"Zr",U1IntegerSource(c,3,a.sheet));
    if q=fail then Error("Affine integer sheet kernel did not lift");fi;
    a.charge:=q;Add(seeds,a);
  od;
  terminalMap:=List(seeds,a->HO.coordinates(U1Native(c,5,"U1s",U1Source(c,3,a))));
  if fail in terminalMap then Error("Affine CI terminal source is not closed");fi;
  if HO.orders=[] then quotientOrders:=[];projected:=List(seeds,a->[]);
  else
    quotient:=U1Smith(Concatenation(DiagonalMat(HO.orders),sourceMap),Length(HO.orders)+Length(sourceMap),Length(HO.orders));
    if quotient.rank<>Length(HO.orders) then Error("Terminal quotient unexpectedly has a free part");fi;
    inds:=Filtered([1..quotient.rank],i->AbsInt(quotient.diag[i])>1);
    quotientOrders:=List(inds,i->AbsInt(quotient.diag[i]));
    projected:=List(terminalMap,row->(row*quotient.V){inds});
  fi;
  K4:=U1MapKernel(projected,quotientOrders,Length(seeds));
  if K3=[] then K:=[];Ki:=[];else K:=K4*K3;Ki:=Inverse(K);fi;
  states:=[];orders:=[];witnesses:=[];
  for i in [1..Length(K4)] do
    a:=U1Combination(c,3,seeds,K4[i]);
    co:=HO.coordinates(U1Native(c,5,"U1s",U1Source(c,3,a)));
    if co=fail then Error("Stacked affine CI source is not closed");fi;
    adjustment:=U1MapPreimage(sourceMap,HO.orders,Length(chargeBasis),-co);
    if adjustment=fail then Error("Affine terminal quotient kernel did not admit a charge adjustment");fi;
    a.charge:=U1Add(a.charge,U1CochainCombination(chargeBasis,adjustment));
    residual:=U1Add(U1Source(c,3,a),U1Scale(-1,U1Coboundary(c,"U1s",a.phase)));
    phase:=U1SolveData(c,5,"U1s",residual);
    if phase=fail then Error("Affine terminal kernel did not admit a phase completion");fi;
    a.phase:=U1Add(a.phase,phase.primitive);U1CheckCompletedState(c,3,a);Add(states,a);
    order:=1;
    for j in [1..Length(HC.orders)] do
      if K[i][j]<>0 then
        if HC.orders[j]=0 then order:=0;break;fi;
        order:=Lcm(order,HC.orders[j]/Gcd(HC.orders[j],K[i][j]));
      fi;
    od;
    Add(orders,order);
    Add(witnesses,rec(kind:="affine-CI-lift",sheetCoordinates:=K[i],integerKernelCoordinates:=K4[i],
      chargeAdjustment:=adjustment,nativeResidualSource:=phase.nativeObstruction,nativePhaseCorrection:=phase.nativePrimitive));
  od;
  relations:=[];
  for i in [1..Length(HC.orders)] do
    if HC.orders[i]=0 then continue;fi;
    relation:=List(HC.orders,x->0);relation[i]:=HC.orders[i];relation:=relation*Ki;
    if not ForAll(relation,IsInt) then Error("A sheet torsion relation left the full obstruction kernel");fi;
    Add(relations,relation);
  od;
  return rec(states:=states,orders:=orders,relations:=relations,witnesses:=witnesses,
    certificate:=rec(rawH1Orders:=HC.orders,integerObstructionTargetOrders:=HI.orders,
      integerObstructionMap:=integerMap,integerKernelLattice:=K3,
      terminalObstructionMap:=terminalMap,terminalQuotientOrders:=quotientOrders,
      terminalQuotientMap:=projected,terminalKernelLattice:=K4,
      finalSheetLattice:=K,originalTorsionRelationCoordinates:=relations,
      construction:="full integer kernels, terminal quotient by charge sources, complete nonlinear stack lifts"));
end);

BindGlobal("U1Classify",function(c,d,options...)
  local HQ,HP,HO,HC,Hlow,chargeBasis,phaseBasis,sourceMap,K,Ki,chargeStates,
    np,nq,ns,relations,witnesses,i,j,v,state,source,phase,co,relation,
    sheetStates,sheetOrders,sheetBasis,integerSource,qseed,adjustment,root,
    coordinates,reduceCharge,gauge,orders,S,rank,result,obstructedSheets,fp,fq,fs,uniform,HI,multiple,terminalMultiple,trial,found,relative,relativeFilling,affineSheets,sheetRelations;
  c.completedStateChecks:=0;c.reductionWitnesses:=[];
  uniform:=d=2 and Length(options)>0 and IsBound(options[1].uniformIQH) and options[1].uniformIQH=true;
  if not d in [2,3] then Error("Global classification currently supports spatial dimensions 2 and 3");fi;
  if d=3 and not c.vcd in [0,3] then Error("3+1D requires a finite group or a full rank-three affine group");fi;
  HQ:=U1Cohomology(c,d,"Zr");HP:=U1Cohomology(c,d+1,"U1s");HO:=U1Cohomology(c,d+2,"U1s");
  chargeBasis:=List(HQ.generators,x->U1Bar(c,d,"Zr",x));
  phaseBasis:=List(HP.generators,x->U1Bar(c,d+1,"U1s",x));
  sourceMap:=List(chargeBasis,q->HO.coordinates(U1Native(c,d+2,"U1s",U1ChargeSource(c,d,q))));
  if fail in sourceMap then Error("Charge obstruction was not a cocycle");fi;
  K:=U1MapKernel(sourceMap,HO.orders,Length(chargeBasis));
  if K=[] then Ki:=[];else Ki:=Inverse(K);fi;
  chargeStates:=[];witnesses:=[];
  for v in K do
    state:=rec(sheet:=U1Zero,charge:=U1CochainCombination(chargeBasis,v),phase:=U1Zero);
    source:=U1Source(c,d,state);phase:=U1SolveData(c,d+2,"U1s",source);
    if phase=fail then Error("Kernel charge lift has a terminal obstruction");fi;
    state.phase:=phase.primitive;U1CheckCompletedState(c,d,state);Add(chargeStates,state);
    Add(witnesses,rec(kind:="charge-lift",chargeCohomology:=v,nativeSource:=phase.nativeObstruction,nativePhase:=phase.nativePrimitive));
  od;
  np:=Length(HP.orders);nq:=Length(K);sheetStates:=[];sheetOrders:=[];obstructedSheets:=[];
  if uniform then
    HC:=U1Cohomology(c,0,"Zs");HI:=U1Cohomology(c,3,"Zr");
    for i in [1..Length(HC.generators)] do
      state:=rec(sheet:=U1Bar(c,0,"Zs",HC.generators[i]),charge:=U1Zero,phase:=U1Zero);
      integerSource:=U1IntegerSource(c,2,state.sheet);
      co:=HI.coordinates(U1Native(c,3,"Zr",integerSource));
      if co=fail then Error("Uniform IQH integer source was not closed");fi;
      multiple:=1;
      for j in [1..Length(co)] do
        if co[j]<>0 then
          if HI.orders[j]=0 then multiple:=0;break;fi;
          multiple:=Lcm(multiple,HI.orders[j]/Gcd(HI.orders[j],co[j]));
        fi;
      od;
      if multiple=0 then Add(obstructedSheets,rec(index:=i,stage:="d3-free",rawClass:=co));continue;fi;
      state.sheet:=U1Scale(multiple,state.sheet);qseed:=U1Solve(c,3,"Zr",U1IntegerSource(c,2,state.sheet));
      if qseed=fail then Error("Uniform IQH integer kernel failed to lift");fi;
      state.charge:=qseed;co:=HO.coordinates(U1Native(c,4,"U1s",U1Source(c,2,state)));
      if co=fail then Error("Uniform IQH phase source was not closed");fi;
      # The quotient obstruction has finite order; retain the first actual lift.
      terminalMultiple:=1;if HO.orders<>[] then terminalMultiple:=Lcm(HO.orders);fi;
      found:=false;
      for j in [1..terminalMultiple] do
        adjustment:=U1MapPreimage(sourceMap,HO.orders,Length(chargeBasis),-j*co);
        if adjustment<>fail then terminalMultiple:=j;found:=true;break;fi;
      od;
      if not found then Error("Finite uniform IQH obstruction had no finite-order kernel");fi;
      state.sheet:=U1Scale(terminalMultiple,state.sheet);
      state.charge:=U1Add(U1Scale(terminalMultiple,qseed),U1CochainCombination(chargeBasis,adjustment));
      phase:=U1SolveData(c,4,"U1s",U1Source(c,2,state));
      if phase=fail then Error("Uniform IQH terminal kernel failed to lift");fi;
      state.phase:=phase.primitive;U1CheckCompletedState(c,d,state);Add(sheetStates,state);Add(sheetOrders,0);
      Add(witnesses,rec(kind:="uniform-IQH-lift",sheetMultiplicity:=multiple*terminalMultiple,
        integerObstructionMultiplicity:=multiple,terminalObstructionMultiplicity:=terminalMultiple,
        chargeAdjustment:=adjustment,nativeSource:=phase.nativeObstruction,nativePhase:=phase.nativePrimitive));
    od;
  fi;
  if d=3 and c.vcd=3 then
    affineSheets:=U1AffineSheetLattice(c,HQ,HO,chargeBasis,sourceMap);
    sheetStates:=affineSheets.states;sheetOrders:=affineSheets.orders;
    Append(witnesses,affineSheets.witnesses);sheetRelations:=affineSheets.relations;
  elif d=3 then
    HC:=U1Cohomology(c,1,"Zs");
    if not HC.orders in [[],[2]] then Error("Finite signed H1 must be zero or Z2");fi;
    for i in [1..Length(HC.orders)] do
      state:=rec(sheet:=U1Bar(c,1,"Zs",HC.generators[i]),charge:=U1Zero,phase:=U1Zero);
      integerSource:=U1IntegerSource(c,d,state.sheet);qseed:=U1Solve(c,d+1,"Zr",integerSource);
      if qseed=fail then Add(obstructedSheets,rec(index:=i,stage:="d3",nativeSource:=U1Native(c,d+1,"Zr",integerSource)));continue;fi;
      state.charge:=qseed;source:=U1Source(c,d,state);co:=HO.coordinates(U1Native(c,d+2,"U1s",source));
      if co=fail then Error("CI terminal source was not closed");fi;
      adjustment:=U1MapPreimage(sourceMap,HO.orders,Length(chargeBasis),-co);
      if adjustment=fail then Add(obstructedSheets,rec(index:=i,stage:="d4-mod-d2",rawClass:=co));continue;fi;
      state.charge:=U1Add(qseed,U1CochainCombination(chargeBasis,adjustment));
      phase:=U1SolveData(c,d+2,"U1s",U1Source(c,d,state));
      if phase=fail then Error("Adjusted CI source failed to lift");fi;
      state.phase:=phase.primitive;U1CheckCompletedState(c,d,state);Add(sheetStates,state);Add(sheetOrders,HC.orders[i]);
      Add(witnesses,rec(kind:="CI-lift",sheetIndex:=i,chargeAdjustment:=adjustment,nativeSource:=phase.nativeObstruction,nativePhase:=phase.nativePrimitive));
    od;
  fi;
  if not (d=3 and c.vcd=3) then
    sheetRelations:=[];
    for i in [1..Length(sheetOrders)] do
      if sheetOrders[i]=0 then continue;fi;
      v:=List(sheetOrders,x->0);v[i]:=sheetOrders[i];Add(sheetRelations,v);
    od;
  fi;
  ns:=Length(sheetStates);relations:=[];
  for i in [1..np] do
    relation:=List([1..np+nq+ns],j->0);relation[i]:=HP.orders[i];Add(relations,relation);
  od;
  # Every original charge torsion relation lifts to a complete phase root.
  for i in [1..Length(HQ.orders)] do
    if HQ.orders[i]=0 then continue;fi;
    v:=List(HQ.orders,x->0);v[i]:=HQ.orders[i];v:=v*Ki;
    if not ForAll(v,IsInt) then Error("Charge relation left the obstruction kernel");fi;
    state:=U1Combination(c,d,chargeStates,v);phase:=U1ReduceVacuum(c,d,state);
    co:=U1ClosedPhaseCoordinates(c,d,HP,phase);
    Add(relations,Concatenation(-co,v,List([1..ns],j->0)));
    Add(witnesses,rec(kind:="charge-root",coefficients:=v,phaseCoordinates:=co));
  od;
  reduceCharge:=function(a)
    local qco,coords,target,diff,pco;
    U1CheckCompletedState(c,d,a);
    qco:=HQ.coordinates(U1Native(c,d,"Zr",a.charge));
    if qco=fail then Error("Root charge is not closed");fi;
    if nq=0 then coords:=[];else coords:=qco*Ki;fi;
    if not ForAll(coords,IsInt) then Error("Root charge not in obstruction kernel");fi;
    target:=U1Combination(c,d,chargeStates,coords);diff:=U1Product(c,d,a,U1Inverse(c,d,target));
    pco:=U1ClosedPhaseCoordinates(c,d,HP,U1ReduceVacuum(c,d,diff));
    return rec(charge:=coords,phase:=pco);
  end;
  for i in [1..Length(sheetRelations)] do
    v:=sheetRelations[i];root:=U1Combination(c,d,sheetStates,v);
    # A finite-order sheet is first removed by its full integer gauge.
    gauge:=U1Solve(c,d-2,"Zs",U1Scale(-1,root.sheet));
    if gauge=fail then Error("CI root did not become an exact sheet");fi;
    root:=U1Gauge(c,d,root,gauge,U1Zero);root.sheet:=U1Zero;
    coordinates:=reduceCharge(root);
    Add(relations,Concatenation(-coordinates.phase,-coordinates.charge,v));
    Add(witnesses,rec(kind:="CI-root",index:=i,sheetCoefficients:=v,chargeCoordinates:=coordinates.charge,phaseCoordinates:=coordinates.phase));
    if not (d=3 and c.vcd=3) then witnesses[Length(witnesses)].order:=Gcd(v);fi;
  od;
  # Incoming charge gauges quotient the terminal phase by actual cochain images.
  Hlow:=U1Cohomology(c,d-1,"Zr");
  for i in [1..Length(Hlow.generators)] do
    gauge:=U1Bar(c,d-1,"Zr",Hlow.generators[i]);state:=U1Gauge(c,d,U1Vacuum(),U1Zero,gauge);
    coordinates:=reduceCharge(state);
    Add(relations,Concatenation(coordinates.phase,coordinates.charge,List([1..ns],j->0)));
    Add(witnesses,rec(kind:="incoming-charge-gauge",index:=i,phaseCoordinates:=coordinates.phase,chargeCoordinates:=coordinates.charge));
  od;
  if d=3 then
    Hlow:=U1Cohomology(c,0,"Zs");
    for i in [1..Length(Hlow.generators)] do
      gauge:=U1Bar(c,0,"Zs",Hlow.generators[i]);state:=U1Gauge(c,d,U1Vacuum(),gauge,U1Zero);state.sheet:=U1Zero;
      coordinates:=reduceCharge(state);
      Add(relations,Concatenation(coordinates.phase,coordinates.charge,List([1..ns],j->0)));
      Add(witnesses,rec(kind:="incoming-CI-gauge",index:=i,phaseCoordinates:=coordinates.phase,chargeCoordinates:=coordinates.charge));
    od;
  fi;
  rank:=np+nq+ns;S:=U1Smith(relations,Length(relations),rank);
  orders:=Filtered(List([1..S.rank],i->AbsInt(S.diag[i])),x->x>1);
  result:=rec(theory:="U(1)^f insulator",spatialDimension:=d,
    scope:="CI-generated, localized-charge and group-cohomological phase sector",
    uniformIQHIncluded:=uniform,freeRank:=rank-S.rank,torsion:=orders,
    presentation:=relations,presentationGeneratorCount:=rank,
    phaseOrders:=HP.orders,chargeOrders:=HQ.orders,chargeObstructionTargetOrders:=HO.orders,
    chargeObstructionMap:=sourceMap,chargeKernelLattice:=K,sheetOrders:=sheetOrders,
    obstructedSheets:=obstructedSheets,witnesses:=witnesses,
    coefficientActions:=["CI: s1","charge: rho1","extension: rho1+s1","phase: s1"],
    resolutionDimensions:=List([0..d+3],k->Dimension(c.R)(k)));
  if d=2 and not uniform then result.scope:=Concatenation(result.scope,"; relative n0=0");fi;
  fp:=U1Filtration(relations,rank,0,np);fq:=U1Filtration(relations,rank,np,nq);fs:=U1Filtration(relations,rank,np+nq,ns);
  result.finalPhaseOrders:=fp.torsion;result.finalPhaseFreeRank:=fp.freeRank;
  result.finalChargeOrders:=fq.torsion;result.finalChargeFreeRank:=fq.freeRank;
  result.finalSheetOrders:=fs.torsion;result.finalSheetFreeRank:=fs.freeRank;
  result.filtrationPresentations:=rec(phase:=fp.presentation,charge:=fq.presentation,sheet:=fs.presentation);
  result.generators:=Concatenation(
    List(HP.generators,x->rec(kind:="phase",nativePhase:=x)),
    List(chargeStates,x->rec(kind:="charge",nativeCharge:=U1Native(c,d,"Zr",x.charge),nativePhase:=U1Native(c,d+1,"U1s",x.phase))),
    List(sheetStates,x->rec(kind:="CI",nativeSheet:=U1Native(c,d-2,"Zs",x.sheet),nativeCharge:=U1Native(c,d,"Zr",x.charge),nativePhase:=U1Native(c,d+1,"U1s",x.phase))));
  result.nativeCompletionChecks:=c.completedStateChecks;
  result.formulaWorkerCalls:=0;if IsBound(c.workerCalls) then result.formulaWorkerCalls:=c.workerCalls;fi;
  result.formulaCacheStats:=rec(entryLimitPerCache:=8192);
  if IsBound(c.requestCache) then
    result.formulaCacheStats.requestHits:=c.requestCacheHits;
    result.formulaCacheStats.requestEntries:=c.requestCacheSize;
    result.formulaCacheStats.requestFlushes:=c.requestCacheFlushes;
  fi;
  if IsBound(c.formulaGeometryCache) then
    result.formulaCacheStats.geometryHits:=c.formulaGeometryHits;
    result.formulaCacheStats.geometryEntries:=c.formulaGeometryCount;
    result.formulaCacheStats.geometryFlushes:=c.formulaGeometryFlushes;
  fi;
  if IsBound(c.R!.afsTimings) then result.resolutionBuildTimings:=c.R!.afsTimings;fi;
  result.pairedGeometryReuse:=IsBound(c.pairedGeometryReuse) and c.pairedGeometryReuse;
  result.nativeChainIdentitiesVerified:=true;result.gaugeReductionWitnesses:=c.reductionWitnesses;
  if IsBound(c.inputValidation) then result.inputValidation:=c.inputValidation;fi;
  if d=3 and c.vcd=3 then result.spaceGroupSheetLattice:=affineSheets.certificate;fi;
  if d=3 then result.neutralE8AbsentByCohomology:=U1Cohomology(c,1,"Zs").orders=[];fi;
  c.classificationStates:=rec(phase:=phaseBasis,charge:=chargeStates,sheet:=sheetStates);
  if d=2 and c.vcd=2 then result.wallpaperFilling:=U1WallpaperFilling(c,result);fi;
  if d=3 and c.vcd=3 then result.spaceGroupFilling:=U1SpaceGroupFilling(c,result);fi;
  if uniform then
    # n0 of a surviving uniform generator is a nonzero integer. Its kernel is
    # precisely the charge/phase subgroup; eliminate later relation columns.
    if ForAny(sheetOrders,x->x<>0) or ns>1 then Error("Unexpected uniform IQH sheet structure");fi;
    relative:=U1Filtration(relations,rank,0,np+nq);
    result.relativeUniformIQH0:=rec(theory:=result.theory,spatialDimension:=2,
      scope:="relative n0=0 subgroup of the complete uniform-IQH presentation",
      uniformIQHIncluded:=false,torsion:=relative.torsion,freeRank:=relative.freeRank,
      presentation:=relative.presentation,presentationGeneratorCount:=np+nq,
      finalChargeOrders:=result.finalChargeOrders,finalChargeFreeRank:=result.finalChargeFreeRank,
      finalPhaseOrders:=result.finalPhaseOrders,finalPhaseFreeRank:=result.finalPhaseFreeRank,
      generators:=result.generators{[1..np+nq]},
      nativeChainIdentitiesVerified:=result.nativeChainIdentitiesVerified,
      construction:="integer elimination of CI columns; kernel of the actual nonzero n0 sheet multiplicity");
    if IsBound(result.wallpaperFilling) then
      relativeFilling:=ShallowCopy(result.wallpaperFilling);
      relativeFilling.generatorFillings:=result.wallpaperFilling.generatorFillings{[1..np+nq]};
      relativeFilling.fillingStep:=result.wallpaperFilling.chargeRootSubgroupFillingStep;
      relativeFilling.ciGeneratorFillings:=[];
      result.relativeUniformIQH0.wallpaperFilling:=relativeFilling;
    fi;
  fi;
  return result;
end);
