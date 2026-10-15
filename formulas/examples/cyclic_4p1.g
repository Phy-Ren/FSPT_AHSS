# Complete original-four-data classification for unsigned cyclic internal G.
# This isolated pilot deliberately does not extend the general U1Classify API.
# Hypotheses: G=C_N, s=rho=0, omega=0, and no intrinsic r0 coefficient.

BindGlobal("U1FourCILower",a->rec(sheet:=a.n_p,charge:=a.n_p2,phase:=a.nu_p3));
BindGlobal("U1FourZero",function()
  return rec(e_p:=U1Zero,n_p:=U1Zero,n_p2:=U1Zero,nu_p3:=U1Zero);
end);
BindGlobal("U1FourNeutralSource",function(c,e)
  return U1Scale(1/3,U1Cup(c,4,U1Cup(c,2,e,"Z",2,e,"Z",0,false),"Z",2,e,"Z",0,false));
end);
BindGlobal("U1FourNeutralProduct",function(c,e,f)
  local h,diff;
  h:=U1Cup(c,2,e,"Z",2,f,"Z",1,false);diff:=U1Add(e,U1Scale(-1,f));
  return U1Scale(1/3,U1Add(U1Cup(c,3,h,"Z",2,diff,"Z",0,false),
    U1Scale(-1,U1Cup(c,2,diff,"Z",3,h,"Z",0,false))));
end);
BindGlobal("U1FourNeutralGauge",function(c,e,v)
  local out,first,middle,last;
  out:=U1Add(e,U1Coboundary(c,"Zs",v));
  first:=U1Cup(c,1,v,"Z",4,U1Cup(c,2,out,"Z",2,out,"Z",0,false),"Z",0,false);
  middle:=U1Cup(c,3,U1Cup(c,2,e,"Z",1,v,"Z",0,false),"Z",2,out,"Z",0,false);
  last:=U1Cup(c,4,U1Cup(c,2,e,"Z",2,e,"Z",0,false),"Z",1,v,"Z",0,false);
  return U1Scale(1/3,U1Add(U1Add(first,middle),last));
end);
BindGlobal("U1FourSource",function(c,a)
  return U1Add(U1Source(c,4,U1FourCILower(a)),U1FourNeutralSource(c,a.e_p));
end);
BindGlobal("U1FourProduct",function(c,a,b)
  local out;
  out:=U1Product(c,4,U1FourCILower(a),U1FourCILower(b));
  return rec(e_p:=U1Add(a.e_p,b.e_p),n_p:=out.sheet,n_p2:=out.charge,
    nu_p3:=U1Add(out.phase,U1FourNeutralProduct(c,a.e_p,b.e_p)));
end);
BindGlobal("U1FourInverse",function(c,a)
  local out,e;
  out:=U1Inverse(c,4,U1FourCILower(a));e:=U1Scale(-1,a.e_p);
  return rec(e_p:=e,n_p:=out.sheet,n_p2:=out.charge,
    nu_p3:=U1Add(out.phase,U1Scale(-1,U1FourNeutralProduct(c,a.e_p,e))));
end);
BindGlobal("U1FourPower",function(c,a,k)
  local out,base;
  if not IsInt(k) then Error("An integral stacking exponent is required");fi;
  out:=U1FourZero();base:=a;
  if k<0 then base:=U1FourInverse(c,base);k:=-k;fi;
  while k>0 do
    if k mod 2=1 then out:=U1FourProduct(c,out,base);fi;
    k:=QuoInt(k,2);if k>0 then base:=U1FourProduct(c,base,base);fi;
  od;return out;
end);
BindGlobal("U1FourGauge",function(c,a,v,u,w)
  local out;
  out:=U1Gauge(c,4,U1FourCILower(a),u,w);
  return rec(e_p:=U1Add(a.e_p,U1Coboundary(c,"Zs",v)),n_p:=out.sheet,n_p2:=out.charge,
    nu_p3:=U1Add(out.phase,U1FourNeutralGauge(c,a.e_p,v)));
end);
BindGlobal("U1FourNative",function(c,a)
  return rec(e_p:=U1Native(c,2,"Zs",a.e_p),n_p:=U1Native(c,2,"Zs",a.n_p),
    n_p2:=U1Native(c,4,"Zr",a.n_p2),nu_p3:=U1Native(c,5,"U1s",a.nu_p3));
end);
BindGlobal("U1FourCheck",function(c,a)
  local v,integerSource,source;
  v:=U1FourNative(c,a);
  if ForAny(U1ApplyDifferential(c,2,"Zs",v.e_p),x->x<>0) or
     ForAny(U1ApplyDifferential(c,2,"Zs",v.n_p),x->x<>0) then Error("A sheet is not closed");fi;
  integerSource:=U1Native(c,5,"Zr",U1IntegerSource(c,4,a.n_p));
  if U1ApplyDifferential(c,4,"Zr",v.n_p2)<>integerSource then Error("The charge completion failed");fi;
  source:=U1Native(c,6,"U1s",U1FourSource(c,a));
  if ForAny(U1ApplyDifferential(c,5,"Zs",v.nu_p3)-source,x->U1Mod1(x)<>0) then
    Error("The shared phase does not complete both sheet sources");fi;
  if ForAny(U1ApplyDifferential(c,6,"Zs",source),x->U1Mod1(x)<>0) then Error("Terminal source closure failed");fi;
  c.fourCompletionChecks:=c.fourCompletionChecks+1;return v;
end);

BindGlobal("U1CyclicFourData",function(N)
  local c,HS,HQ,HP,HO,Hincoming1,Hincoming3,a,x,x2,ax2,unitQ,unitP,
    neutral,sheet,charge,phase,seed,roots,names,checks,relations,witnesses,
    i,power,v,u,w,qco,pco,remainder,primitive,relation,smith,orders,result,
    source,da,tuples,tuple,barChecks,baseCharge,rootState;
  if not IsInt(N) or N<1 then Error("A positive cyclic order is required");fi;
  c:=U1CyclicContext(N,0,0,0);c.fourCompletionChecks:=0;
  HS:=U1Cohomology(c,2,"Zs");HQ:=U1Cohomology(c,4,"Zr");HP:=U1Cohomology(c,5,"U1s");
  HO:=U1Cohomology(c,6,"U1s");Hincoming1:=U1Cohomology(c,1,"Zs");Hincoming3:=U1Cohomology(c,3,"Zr");
  if HO.orders<>[] or Hincoming1.orders<>[] or Hincoming3.orders<>[] then
    Error("The cyclic pilot's zero-target/incoming hypotheses failed");fi;
  result:=rec(theory:="U(1)^f insulator",spatialDimension:=4,
    orderedFields:=["e_2","n_2","n_4","nu_5"],group:=rec(family:="internal_cyclic",order:=N),
    background:=rec(s:=0,rho:=0,omega:=0,description:="Unitary internal C_N commuting with U(1)^f; no crystalline spin label"),
    scope:="Complete stacking group of the original four-data model for this cyclic background; intrinsic r0 excluded by scope",
    physicalClassificationCertified:=false,
    physicalScopeCaveat:="Identification of the fixed CI model with the full physical kernel remains separate",
    incomingCohomology:=rec(sheet:=Hincoming1.orders,charge:=Hincoming3.orders),
    terminalObstructionTargetOrders:=HO.orders,integerSourceIdenticallyZero:=true,
    sourceConvention:=rec(calibration:="sheet-linear",cubic:="1/6",epsilon:=0));
  if N=1 then
    if HS.orders<>[] or HQ.orders<>[] or HP.orders<>[] then Error("Trivial-group control failed");fi;
    U1FourCheck(c,U1FourZero());result.torsion:=[];result.freeRank:=0;
    result.presentation:=[];result.presentationGeneratorCount:=0;result.generators:=[];result.witnesses:=[];
    result.nativeCompletionChecks:=c.fourCompletionChecks;result.barCompletionChecks:=0;
    result.expectedOrderFromFiltration:=1;result.actualGroupOrder:=1;return result;
  fi;
  if HS.orders<>[N] or HQ.orders<>[N] or HP.orders<>[N] then Error("Unexpected cyclic cohomology");fi;
  a:=g->g!.exponents[1];
  x:=function(g,h) return QuoInt(g!.exponents[1]+h!.exponents[1],N);end;
  x2:=U1Cup(c,2,x,"Z",2,x,"Z",0,false);
  ax2:=U1Cup(c,1,a,"Z",4,x2,"Z",0,false);
  unitQ:=HQ.coordinates(U1Native(c,4,"Zr",x2))[1];
  unitP:=HP.coordinates(U1Native(c,5,"U1s",U1Scale(1/N,ax2)))[1];
  if GcdInt(HS.coordinates(U1Native(c,2,"Zs",x))[1],N)<>1 or
     GcdInt(unitQ,N)<>1 or GcdInt(unitP,N)<>1 then Error("Canonical cyclic roots do not generate their layers");fi;
  neutral:=rec(e_p:=x,n_p:=U1Zero,n_p2:=U1Zero,nu_p3:=U1Scale(1/(3*N),ax2));
  sheet:=rec(e_p:=U1Zero,n_p:=x,n_p2:=U1Zero,nu_p3:=U1Scale(1/(6*N),ax2));
  seed:=U1SolveData(c,6,"U1s",U1ChargeSource(c,4,x2));
  if seed=fail then Error("The cyclic charge root did not complete");fi;
  charge:=rec(e_p:=U1Zero,n_p:=U1Zero,n_p2:=x2,nu_p3:=seed.primitive);
  phase:=rec(e_p:=U1Zero,n_p:=U1Zero,n_p2:=U1Zero,nu_p3:=U1Scale(1/N,ax2));
  roots:=[neutral,sheet,charge,phase];names:=["neutral-E8","CI-sheet","charge","shared-phase"];
  checks:=List(roots,r->U1FourCheck(c,r));
  # Independent normalized-bar completion checks supplement native-resolution checks.
  tuples:=List([1..Minimum(N-1,3)],j->List([1..6],k->GeneratorsOfGroup(c.G)[1]^j));barChecks:=0;
  for rootState in roots do
    da:=U1Coboundary(c,"U1s",rootState.nu_p3);source:=U1FourSource(c,rootState);
    for tuple in tuples do
      if U1Mod1(CallFuncList(da,tuple)-CallFuncList(source,tuple))<>0 then Error("Explicit bar completion failed");fi;
      barChecks:=barChecks+1;
    od;
  od;
  relations:=[];witnesses:=[];
  for i in [1..4] do
    power:=U1FourPower(c,roots[i],N);U1FourCheck(c,power);
    v:=U1Solve(c,2,"Zs",U1Scale(-1,power.e_p));
    u:=U1Solve(c,2,"Zs",U1Scale(-1,power.n_p));
    if v=fail or u=fail then Error("Root sheets did not become exact");fi;
    power:=U1FourGauge(c,power,v,u,U1Zero);power.e_p:=U1Zero;power.n_p:=U1Zero;
    U1FourCheck(c,power);
    qco:=HQ.coordinates(U1Native(c,4,"Zr",power.n_p2));
    if qco=fail then Error("Reduced root charge is not closed");fi;
    qco:=qco[1]*PowerModInt(unitQ,-1,N) mod N;
    power:=U1FourProduct(c,power,U1FourPower(c,charge,-qco));
    w:=U1Solve(c,4,"Zr",U1Scale(-1,power.n_p2));
    if w=fail then Error("Reduced root charge is not exact");fi;
    power:=U1FourGauge(c,power,U1Zero,U1Zero,w);power.n_p2:=U1Zero;U1FourCheck(c,power);
    pco:=HP.coordinates(U1Native(c,5,"U1s",power.nu_p3));
    if pco=fail then Error("Reduced root phase is not closed");fi;
    pco:=pco[1]*PowerModInt(unitP,-1,N) mod N;
    remainder:=U1Add(power.nu_p3,U1Scale(-pco,phase.nu_p3));
    primitive:=U1SolveData(c,5,"U1s",remainder);
    if primitive=fail then Error("Root relation retains an unrecorded phase");fi;
    relation:=[0,0,-qco,-pco];relation[i]:=relation[i]+N;Add(relations,relation);
    Add(witnesses,rec(root:=names[i],power:=N,chargeCoefficient:=qco,phaseCoefficient:=pco,
      nativeNeutralGauge:=U1Native(c,1,"Zs",v),nativeCIGauge:=U1Native(c,1,"Zs",u),
      nativeChargeGauge:=U1Native(c,3,"Zr",w),nativePhasePrimitive:=primitive.nativePrimitive,
      residualNativePhase:=primitive.nativeObstruction));
  od;
  smith:=U1Smith(relations,Length(relations),4);
  orders:=Filtered(List([1..smith.rank],i->AbsInt(smith.diag[i])),x->x>1);
  if smith.rank<>4 or Product(orders)<>N^4 then Error("Root presentation does not have the required filtration order");fi;
  result.torsion:=orders;result.freeRank:=0;result.presentation:=relations;result.presentationGeneratorCount:=4;
  result.generators:=List([1..4],i->rec(kind:=names[i],nativeState:=checks[i]));result.witnesses:=witnesses;
  result.canonicalCochains:=rec(a1:="least nonnegative exponent",x2:="d a1 / N",charge:="x2 cup x2",
    neutralPhase:="a1 cup x2 cup x2 / (3N)",CIPhase:="a1 cup x2 cup x2 / (6N)",phaseRoot:="a1 cup x2 cup x2 / N");
  result.nativeCompletionChecks:=c.fourCompletionChecks;result.barCompletionChecks:=barChecks;
  result.expectedOrderFromFiltration:=N^4;result.actualGroupOrder:=Product(orders);
  return result;
end);
