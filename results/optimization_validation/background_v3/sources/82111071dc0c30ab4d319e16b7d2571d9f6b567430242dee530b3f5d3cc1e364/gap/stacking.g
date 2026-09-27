# Independent three-layer stacking, in the delivered manuscript CA coordinate.
# The integer p+ip layer uses its separately certified diagonal operation.
# Abstract extension certificates and full cochain witnesses are distinguished.
# All group cochains are lazy functions on the INFINITE affine group. No finite
# point-group substitution and no table of all phases is used.

BindGlobal("AFSCoadd",function(modulus,fs)
  local reduced,f,pos;
  fs:=Filtered(fs,f->f<>AFSZero);
  if modulus=2 then
    reduced:=[];
    for f in fs do
      pos:=Position(reduced,f);
      if pos=fail then Add(reduced,f);else Remove(reduced,pos);fi;
    od;
    fs:=reduced;
  fi;
  if Length(fs)=0 then return AFSZero;fi;
  return AFSMemo(function(xs...)
    local value,f;
    value:=0;
    for f in fs do value:=value+CallFuncList(f,xs); od;
    if modulus=1 then return AFSMod1(value); fi;
    if modulus=2 then return value mod 2; fi;
    return value;
  end);
end);
BindGlobal("AFSComul",function(modulus,n,f)
  if n=0 or f=AFSZero then return AFSZero;fi;
  return AFSMemo(function(xs...)
    local value;
    value:=n*CallFuncList(f,xs);
    if modulus=1 then return AFSMod1(value); fi;
    if modulus=2 then return value mod 2; fi;
    return value;
  end);
end);

BindGlobal("AFSStackZero",function()
  return rec(a:=AFSZero,c:=AFSZero,v:=AFSZero,construction:="zero");
end);

BindGlobal("AFSStackProduct",function(ctx,x,y)
  local m,u;
  # The normalized CA product has no cross term when either input has
  # zero MC and CF layers. Preserve exact zeros instead of wrapping them in
  # generic formula callbacks; bosonic translation is ordinary addition.
  if x.a=AFSZero and x.c=AFSZero then
    if x.v=AFSZero then return ShallowCopy(y);fi;
    return rec(a:=y.a,c:=y.c,v:=AFSCoadd(1,[x.v,y.v]),
      construction:="CA-product-with-pure-bosonic-left-factor");
  fi;
  if y.a=AFSZero and y.c=AFSZero then
    if y.v=AFSZero then return ShallowCopy(x);fi;
    return rec(a:=x.a,c:=x.c,v:=AFSCoadd(1,[x.v,y.v]),
      construction:="CA-product-with-pure-bosonic-right-factor");
  fi;
  if x.a=AFSZero and y.a=AFSZero then
    # Literal off-shell restriction of the supplied CA polynomial. Retain
    # delta(c) cup3 c' even though it vanishes on flat pure-CF states.
    u:=AFSComul(1,1/2,AFSCoadd(2,[AFSCup(2,3,x.c,3,y.c),
      AFSCup(3,4,AFSCoboundary(ctx,"F2",x.c),3,y.c)]));
    return rec(a:=AFSZero,c:=AFSCoadd(2,[x.c,y.c]),
      v:=AFSCoadd(1,[x.v,y.v,u]),construction:="literal-pure-CF-CA-product");
  fi;
  m:=AFSFormula("majorana_product",ctx,rec(p:=2,a:=x.a,b:=y.a));
  u:=AFSFormula("stacking",ctx,rec(p:=2,a:=x.a,c:=x.c,b:=y.a,cp:=y.c));
  return rec(a:=AFSCoadd(2,[x.a,y.a]),c:=AFSCoadd(2,[x.c,y.c,m]),
    v:=AFSCoadd(1,[x.v,y.v,u]),construction:="delivered-CA-product");
end);

BindGlobal("AFSStackInverse",function(ctx,x)
  local m,c,u;
  m:=AFSFormula("majorana_product",ctx,rec(p:=2,a:=x.a,b:=x.a));
  c:=AFSCoadd(2,[x.c,m]);
  u:=AFSFormula("stacking",ctx,rec(p:=2,a:=x.a,c:=x.c,b:=x.a,cp:=c));
  return rec(a:=x.a,c:=c,v:=AFSComul(1,-1,AFSCoadd(1,[x.v,u])),
    construction:="right-inverse-in-CA-coordinate");
end);

BindGlobal("AFSStackPower",function(ctx,x,n)
  local result,b;
  if not IsInt(n) then Error("stacking power must be an integer"); fi;
  if n=1 then return ShallowCopy(x);fi;
  if n=2 and IsBound(x.cfPhaseNativeSeed) then
    # The comparison correction is O5 composed with an integral homotopy.
    # For pure CF, O5 is half-integral, so twice that correction vanishes
    # pointwise modulo1. This is the SAME marked lift, without expanding h5.
    return rec(a:=AFSZero,c:=AFSZero,v:=AFSCoadd(1,[
      AFSComul(1,2,AFSBar(ctx,4,"U1s",x.cfPhaseNativeSeed)),
      AFSComul(1,1/2,AFSCup(2,3,x.c,3,x.c))]),
      construction:="same-marked-CF-double-with-integral-homotopy-correction-removed");
  fi;
  if n<0 then x:=AFSStackInverse(ctx,x);n:=-n;fi;
  result:=AFSStackZero();b:=x;
  while n>0 do
    if n mod 2=1 then result:=AFSStackProduct(ctx,result,b);fi;
    n:=QuoInt(n,2);
    if n>0 then b:=AFSStackProduct(ctx,b,b);fi;
  od;
  return result;
end);

BindGlobal("AFSStackOrdered",function(ctx,states,coordinates)
  local result,i;
  if Length(states)<>Length(coordinates) then Error("stacking basis mismatch");fi;
  result:=AFSStackZero();
  for i in [1..Length(states)] do
    if not IsInt(coordinates[i]) then Error("nonintegral stacking coordinate");fi;
    if coordinates[i]<>0 then
      result:=AFSStackProduct(ctx,result,AFSStackPower(ctx,states[i],coordinates[i]));
    fi;
  od;
  return result;
end);

# This verifies on every bar simplex in the resolution-comparison support,
# without relying on cancellation after projection. Global equality of the
# homotopy-corrected primitives follows from the checked comparison identity
# and the formula's cocycle identity; a support check is retained as evidence.
BindGlobal("AFSStackSupportZero",function(ctx,k,modulus,f)
  local i,t,x,value;
  for i in [1..Dimension(ctx.R)(k)] do
    for t in AFSChainToBar(ctx.bar,k,i) do
      x:=t[3];value:=CallFuncList(f,x);
      if modulus=1 then value:=AFSMod1(value);
      elif modulus=2 then value:=value mod 2;fi;
      if value<>0 then return false;fi;
    od;
  od;
  return true;
end);

BindGlobal("AFSStackAuditEnabled",function()
  return IsBoundGlobal("AFS_STACK_AUDIT") and ValueGlobal("AFS_STACK_AUDIT")=true;
end);

BindGlobal("AFSStackCheckFlat",function(ctx,x)
  local source,obstruction,result;
  if IsBound(x.checkedFlatComparisonSupport) and x.checkedFlatComparisonSupport then return true;fi;
  if not AFSStackSupportZero(ctx,3,2,AFSCoboundary(ctx,"F2",x.a)) then return false;fi;
  source:=AFSFormula("majorana_source",ctx,rec(p:=2,a:=x.a));
  if not AFSStackSupportZero(ctx,4,2,AFSCoadd(2,
      [AFSCoboundary(ctx,"F2",x.c),source])) then return false;fi;
  obstruction:=AFSFormula("obstruction",ctx,rec(p:=2,a:=x.a,c:=x.c));
  result:=AFSStackSupportZero(ctx,5,1,AFSCoadd(1,
    [AFSCoboundary(ctx,"U1s",x.v),AFSComul(1,-1,obstruction)]));
  if result then x.checkedFlatComparisonSupport:=true;fi;
  return result;
end);

BindGlobal("AFSStackLift",function(ctx,layer,cochain)
  local x,source,obstruction,useClosed,solveData;
  x:=AFSStackZero();
  if layer=0 then x.v:=cochain;
  elif layer=1 then
    x.c:=cochain;
    # This lift's input is a closed H3 representative. Restrict the delivered
    # off-shell Sq2 formula only here; nonclosed MC defining cochains below
    # retain the full obstruction. The optimization is opt-in until audited.
    useClosed:=IsBoundGlobal("AFS_USE_CLOSED_CF_OBSTRUCTION") and
       ValueGlobal("AFS_USE_CLOSED_CF_OBSTRUCTION")=true;
    if useClosed then
      if not IsBoundGlobal("AFSClosedCFObstructionLazy") then
        Error("closed-CF option requires gap/stacking_closed_cf.g");
      fi;
      obstruction:=CallFuncList(ValueGlobal("AFSClosedCFObstructionLazy"),[x.c]);
      if IsBound(ctx.omega2) and ctx.omega2<>AFSZero then
        obstruction:=AFSCoadd(1,[obstruction,AFSComul(1,1/2,AFSCup(0,2,ctx.omega2,3,x.c))]);
      fi;
      x.cfObstructionFormula:="closed-H3-cup1-lazy-half-phase-transfer";
    else
      obstruction:=AFSFormula("obstruction",ctx,rec(p:=2,a:=x.a,c:=x.c));
    fi;
    if useClosed then
      if not IsBoundGlobal("AFSSolveHalfPhaseData") then
        Error("closed-CF option requires gap/backend_half_phase.g");
      fi;
      # The source is exactly half-valued. Transfer may discard even bar-chain
      # coefficients; the primitive still uses the full integral comparison
      # homotopy, so the marked phase is unchanged.
      solveData:=CallFuncList(ValueGlobal("AFSSolveHalfPhaseData"),[ctx,5,obstruction]);
      if solveData=fail then x.v:=fail;
      else x.v:=solveData.primitive;x.cfPhaseNativeSeed:=solveData.nativePrimitive;fi;
    else
      x.v:=AFSSolve(ctx,5,"U1s",obstruction);
    fi;
    if x.v=fail then return rec(status:="unresolved",reason:="complex-fermion phase lift");fi;
    if not useClosed then
      x.cfPhaseNativeSeed:=AFSSolveNative(ctx,5,"U1s",AFSNative(ctx,5,"U1s",obstruction));
    fi;
  elif layer=2 then
    x.a:=cochain;
    source:=AFSFormula("majorana_source",ctx,rec(p:=2,a:=x.a));
    x.c:=AFSSolve(ctx,4,"F2",source);
    if x.c=fail then return rec(status:="unresolved",reason:="Majorana complex-fermion lift");fi;
    obstruction:=AFSFormula("obstruction",ctx,rec(p:=2,a:=x.a,c:=x.c));
    x.v:=AFSSolve(ctx,5,"U1s",obstruction);
    if x.v=fail then
      # A different closed C choice may remove the secondary obstruction. The
      # classification engine can pass such a full lift; do not report zero.
      return rec(status:="unresolved",reason:="Majorana phase lift needs closed C adjustment",a:=x.a,c:=x.c);
    fi;
  else return rec(status:="unresolved",reason:="nonzero p+ip product is not provided by this adapter");fi;
  x.construction:="native-cocycle-and-homotopy-corrected-primitive";
  if AFSStackAuditEnabled() and not AFSStackCheckFlat(ctx,x) then Error("constructed lift violates a defining equation");fi;
  return rec(status:="computed",state:=x);
end);

# Pure complex-fermion gauge: delta Q4(beta)=1/2 Sq2(delta beta).
# Its degree-two input need not be closed. Coefficients 1/2 make signs and
# integer lifts unambiguous modulo one, including the orientation local system.
BindGlobal("AFSStackCFBoundary",function(ctx,beta)
  local db,t0,t1,terms;
  db:=AFSCoboundary(ctx,"F2",beta);
  t0:=AFSCup(0,2,beta,2,beta);t1:=AFSCup(1,2,beta,3,db);
  terms:=[t0,t1];
  if IsBound(ctx.omega2) and ctx.omega2<>AFSZero then Add(terms,AFSCup(0,2,ctx.omega2,2,beta));fi;
  return rec(a:=AFSZero,c:=db,v:=AFSComul(1,1/2,AFSCoadd(2,terms)),
    construction:="pure-complex-fermion-boundary",gauge:=beta);
end);

# Closed degree-one Majorana gauge. This is the full incoming CF boundary,
# including its phase; merely recording the source's H3 class is insufficient.
BindGlobal("AFSStackMCBoundary",function(ctx,a)
  local source,phase,x;
  source:=AFSFormula("majorana_source",ctx,rec(p:=1,a:=a));
  phase:=AFSFormula("obstruction",ctx,rec(p:=1,a:=a,c:=AFSZero));
  x:=rec(a:=AFSZero,c:=source,v:=phase,construction:="closed-degree-one-Majorana-boundary",
    gauge:=a);
  if AFSStackAuditEnabled() and not AFSStackCheckFlat(ctx,x) then Error("incoming MC boundary violates its flatness identity");fi;
  return x;
end);

BindGlobal("AFSStackSecondaryBoundary",function(ctx,a,c)
  local x,first,second,dc,h,dh,phase;
  first:=AFSStackMCBoundary(ctx,a);second:=AFSStackCFBoundary(ctx,c);
  x:=AFSStackProduct(ctx,first,second);dc:=AFSCoboundary(ctx,"F2",c);
  # The raw ordered boundary product differs from the manuscript O4(a,c) by
  # 1/2 source cup2 source = delta[1/2(c cup1 c+c cup2 delta c)].
  h:=AFSComul(1,1/2,AFSCoadd(2,[AFSCup(1,2,c,2,c),AFSCup(2,2,c,3,dc)]));
  dh:=AFSCoboundary(ctx,"U1s",h);
  phase:=AFSFormula("obstruction",ctx,rec(p:=1,a:=a,c:=c));
  if AFSStackAuditEnabled() and not AFSStackSupportZero(ctx,3,2,x.c) then Error("secondary boundary has nonzero CF layer");fi;
  if AFSStackAuditEnabled() and not AFSStackSupportZero(ctx,4,1,AFSCoadd(1,[x.v,AFSComul(1,-1,phase),AFSComul(1,-1,dh)])) then
    Error("secondary boundary coordinate correction failed");fi;
  return rec(a:=AFSZero,c:=AFSZero,v:=phase,
    construction:="Majorana-CF-boundary-with-explicit-top-coordinate-correction",
    gauge:=rec(majorana:=a,complex:=c,top:=AFSComul(1,-1,h)));
end);

# A small integer lattice solve with one Smith preparation for many targets.
BindGlobal("AFSStackLatticeSolver",function(rows,width)
  local smith;
  smith:=AFSSmith(rows,Length(rows),width);
  return function(target)
    local w,y,i;
    if Length(target)<>width then Error("lattice target width mismatch");fi;
    if width=0 then return List(rows,r->0);fi;
    w:=target*smith.V;y:=List(rows,r->0);
    for i in [1..width] do
      if i<=smith.rank then
        if w[i] mod smith.diag[i]<>0 then return fail;fi;
        y[i]:=w[i]/smith.diag[i];
      elif w[i]<>0 then return fail;fi;
    od;
    return y*smith.U;
  end;
end);

# Input final quotients retain their actual cochain lifts. Boundary states are
# outputs of incoming DIFFERENTIALS together with preceding-degree gauge data;
# an image rank alone cannot define this model.
BindGlobal("AFSStackModel",function(ctx,data)
  local model,H3,H4,cf,bf,rows,rels,i,row,phaseStates;
  if not IsBound(data.finalFiltrationCertificate) then
    return rec(status:="unresolved",reason:="missing final filtration certificate");fi;
  model:=rec(status:="computed",ctx:=ctx,data:=data,
    generators:=Concatenation(data.boson,data.fermion,data.majorana));
  H3:=AFSCohomology(ctx,3,"F2");H4:=AFSCohomology(ctx,4,"U1s");
  cf:=List(data.fermion,g->g.state);bf:=data.fermionBoundaries;
  rows:=List(Concatenation(cf,bf),x->H3.coordinates(AFSNative(ctx,3,"F2",x.c)));
  if fail in rows then Error("nonclosed complex-fermion comparison class");fi;
  rels:=2*IdentityMat(Length(H3.orders));
  model.cfSolve:=AFSStackLatticeSolver(Concatenation(rows,rels),Length(H3.orders));
  model.cfStates:=cf;model.cfBoundaryStates:=bf;model.H3:=H3;model.H4:=H4;
  phaseStates:=Concatenation(List(data.boson,g->g.state),data.bosonBoundaries);
  rows:=List(phaseStates,x->H4.coordinates(AFSNative(ctx,4,"U1s",x.v)));
  if fail in rows then Error("nonclosed bosonic comparison class");fi;
  rels:=[];
  for i in [1..Length(H4.orders)] do
    row:=List(H4.orders,x->0);row[i]:=H4.orders[i];Add(rels,row);
  od;
  model.phaseSolve:=AFSStackLatticeSolver(Concatenation(rows,rels),Length(H4.orders));
  model.phaseRows:=rows;
  model.phaseBoundarySolve:=AFSStackLatticeSolver(
    Concatenation(rows{[Length(data.boson)+1..Length(rows)]},rels),Length(H4.orders));
  return model;
end);

BindGlobal("AFSStackReduce",function(model,target,allowCF)
  local ctx,d,H3,H4,cv,sol,nc,nb,cfco,bc,canonical,boundary,combined,
    residual,beta,gauge,phase,pc,pco,bco,bphase,primitive,witness,i,remainder;
  ctx:=model.ctx;d:=model.data;H3:=model.H3;H4:=model.H4;
  cv:=H3.coordinates(AFSNative(ctx,3,"F2",target.c));
  if cv=fail then Error("relation target has nonclosed complex-fermion layer");fi;
  sol:=model.cfSolve(cv);
  if sol=fail then return rec(status:="unresolved",reason:="CF residual not in final quotient plus incoming images");fi;
  nc:=Length(d.fermion);nb:=Length(d.fermionBoundaries);
  cfco:=List(sol{[1..nc]},x->x mod 2);bc:=List(sol{[nc+1..nc+nb]},x->x mod 2);
  if not allowCF and ForAny(cfco,x->x<>0) then
    return rec(status:="unresolved",reason:="relation unexpectedly retains same-layer CF class");fi;
  canonical:=AFSStackOrdered(ctx,List(d.fermion,g->g.state),cfco);
  boundary:=AFSStackOrdered(ctx,d.fermionBoundaries,bc);
  combined:=AFSStackProduct(ctx,boundary,canonical);
  residual:=AFSCoadd(2,[target.c,combined.c]);
  beta:=AFSSolve(ctx,3,"F2",residual);
  if beta=fail then Error("CF class reduction did not leave an exact cochain");fi;
  gauge:=AFSStackCFBoundary(ctx,beta);
  boundary:=AFSStackProduct(ctx,gauge,boundary);
  combined:=AFSStackProduct(ctx,boundary,canonical);
  if AFSStackAuditEnabled() and not AFSStackSupportZero(ctx,3,2,AFSCoadd(2,[target.c,combined.c])) then
    Error("homotopy-corrected CF boundary failed exact comparison support");fi;
  phase:=AFSCoadd(1,[target.v,AFSComul(1,-1,combined.v)]);
  pc:=H4.coordinates(AFSNative(ctx,4,"U1s",phase));
  if pc=fail then Error("lower relation phase is not a cocycle");fi;
  sol:=model.phaseSolve(pc);
  if sol=fail then return rec(status:="unresolved",reason:="phase residual outside final bosonic quotient plus incoming images");fi;
  nc:=Length(d.boson);nb:=Length(d.bosonBoundaries);
  pco:=sol{[1..nc]};
  for i in [1..nc] do
    if d.boson[i].order<>0 then pco[i]:=pco[i] mod d.boson[i].order;fi;
  od;
  remainder:=ShallowCopy(pc);
  for i in [1..nc] do remainder:=remainder-pco[i]*model.phaseRows[i];od;
  sol:=model.phaseBoundarySolve(remainder);
  if sol=fail then Error("canonical bosonic quotient coordinates do not reduce modulo incoming images");fi;
  bco:=sol{[1..nb]};
  bphase:=AFSStackOrdered(ctx,d.bosonBoundaries,bco);
  boundary:=AFSStackProduct(ctx,bphase,boundary);
  canonical:=AFSStackProduct(ctx,AFSStackOrdered(ctx,List(d.boson,g->g.state),pco),canonical);
  combined:=AFSStackProduct(ctx,boundary,canonical);
  phase:=AFSCoadd(1,[target.v,AFSComul(1,-1,combined.v)]);
  primitive:=AFSSolve(ctx,4,"U1s",phase);
  if primitive=fail then Error("bosonic quotient did not leave an exact phase");fi;
  bphase:=AFSStackZero();bphase.v:=AFSCoboundary(ctx,"U1s",primitive);
  boundary:=AFSStackProduct(ctx,bphase,boundary);
  combined:=AFSStackProduct(ctx,boundary,canonical);
  if AFSStackAuditEnabled() and not AFSStackSupportZero(ctx,4,1,AFSCoadd(1,[target.v,AFSComul(1,-1,combined.v)])) then
    Error("phase primitive failed exact comparison support");fi;
  witness:=rec(cfIncoming:=bc,cfGauge:=beta,bosonicIncoming:=bco,phaseGauge:=primitive,
    boundary:=boundary,canonical:=canonical,certificateLevel:="comparison-homotopy",
    checkedComparisonSupport:=AFSStackAuditEnabled());
  return rec(status:="computed",coordinates:=Concatenation(pco,cfco),witness:=witness);
end);

BindGlobal("AFSStackClassification",function(model)
  local ctx,gens,relations,witnesses,i,g,target,reduction,row,j,smith,invariants;
  if model.status<>"computed" then return model;fi;
  ctx:=model.ctx;gens:=model.generators;relations:=[];witnesses:=[];
  for i in [1..Length(gens)] do
    g:=gens[i];
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,Concatenation("stack_relation_",g.name));fi;
    if g.layer=0 then
      # These are already invariant-factor generators of the final bosonic
      # cohomology quotient. Their order relations are certified by its Smith
      # presentation, and have no lower layer requiring nonlinear measurement.
      row:=List(gens,x->0);row[i]:=g.order;Add(relations,row);
      Add(witnesses,rec(certificateLevel:="final-bosonic-quotient",
        generator:=g.name,order:=g.order));
      continue;
    fi;
    if AFSStackAuditEnabled() and not AFSStackCheckFlat(ctx,g.state) then Error("nonflat marked stacking lift");fi;
    if g.order<>0 then
      target:=AFSStackPower(ctx,g.state,g.order);
      reduction:=AFSStackReduce(model,target,g.layer=2);
      if reduction.status<>"computed" then
        return rec(status:="unresolved",reason:=reduction.reason,generator:=g.name,
          partialRelations:=relations,witnesses:=witnesses);fi;
      row:=List(gens,x->0);row[i]:=g.order;
      for j in [1..Length(reduction.coordinates)] do
        if gens[j].layer>=g.layer and reduction.coordinates[j]<>0 then
          Error("stacking relation uses a nonlower filtration generator");fi;
        row[j]:=row[j]-reduction.coordinates[j];
      od;
      Add(relations,row);Add(witnesses,reduction.witness);
    fi;
  od;
  smith:=AFSSmith(relations,Length(relations),Length(gens));
  invariants:=Concatenation(List([smith.rank+1..Length(gens)],i->0),
    Filtered(List(smith.diag,AbsInt),x->x>1));
  return rec(status:="computed",scope:="p+ip-zero-three-layer-extension",
    invariants:=invariants,presentation:=relations,witnesses:=witnesses,
    generators:=gens,smith:=smith,enumeratedPhaseProducts:=0,
    finalFiltrationCertificate:=model.data.finalFiltrationCertificate);
end);

# Complete a Majorana lift using the actual CF primary image in H5(U1s).
# This is one finite-field/lattice solve, not enumeration of C choices.
BindGlobal("AFSStackLiftMC",function(C,a,solveIndeterminacy)
  local ctx,x,source,op,co,sol,adjust,primitive;
  ctx:=C.ctx;x:=AFSStackZero();x.a:=a;
  source:=AFSFormula("majorana_source",ctx,rec(p:=2,a:=a));
  x.c:=AFSSolve(ctx,4,"F2",source);
  if x.c=fail then return rec(status:="unresolved",reason:="Majorana primary lift");fi;
  op:=AFSFormula("obstruction",ctx,rec(p:=2,a:=a,c:=x.c));
  co:=C.H5U.coordinates(AFSNative(ctx,5,"U1s",op));
  if co=fail then Error("Majorana lifted obstruction is not closed");fi;
  if ForAny(co,z->z<>0) then
    sol:=solveIndeterminacy(List(co,z->-z));
    if sol=fail then return rec(status:="unresolved",reason:="Majorana secondary class outside CF image");fi;
    adjust:=AFSCombination(ctx,3,"F2",C.H3,List(sol{[1..Length(C.H3.orders)]},z->z mod 2));
    x.c:=AFSCoadd(2,[x.c,adjust]);
    op:=AFSFormula("obstruction",ctx,rec(p:=2,a:=a,c:=x.c));
  fi;
  x.v:=AFSSolve(ctx,5,"U1s",op);
  if x.v=fail then Error("CF indeterminacy adjustment did not trivialize Majorana obstruction");fi;
  x.construction:="full-Majorana-lift-with-linear-CF-indeterminacy-solve";
  if AFSStackAuditEnabled() and not AFSStackCheckFlat(ctx,x) then Error("completed Majorana lift is not flat");fi;
  return rec(status:="computed",state:=x);
end);

# Adapter for gap/classification.g's independent final layer calculation.
BindGlobal("AFSStackFromClassification",function(C)
  local ctx,data,i,u,co,f,lift,g,rows,row,solveIndeterminacy;
  ctx:=C.ctx;
  if not IsBound(C.bosQuotient) or not IsBound(C.mcFinalBasis) then
    return rec(status:="unresolved",reason:="final lower-layer classification is incomplete");fi;
  data:=rec(boson:=[],fermion:=[],majorana:=[],fermionBoundaries:=[],bosonBoundaries:=[],
    finalFiltrationCertificate:=rec(spaceGroup:=ctx.number,convention:="spin-half-omega0-det",
      boson:=C.bosQuotient.orders,fermionRank:=Length(C.cfFinalBasis),majoranaRank:=Length(C.mcFinalBasis)));
  if IsBound(ctx.crystallineSpin) and ctx.crystallineSpin="spinless" then
    data.finalFiltrationCertificate.convention:="physical-spinless-det-sign-Pin-minus";
    data.finalFiltrationCertificate.beforeH0Incoming:=ctx.s=AFSZero and ctx.omega2<>AFSZero;
  fi;
  for i in [1..Length(C.bosQuotient.orders)] do
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,Concatenation("stack_lift_D",String(i)));fi;
    u:=List(C.bosQuotient.orders,z->0);u[i]:=1;co:=C.bosQuotient.lift(u);
    f:=AFSCombination(ctx,4,"U1s",C.H4U,co);
    lift:=rec(state:=rec(a:=AFSZero,c:=AFSZero,v:=f,construction:="final-bosonic-quotient-cocycle"));
    Add(data.boson,rec(name:=Concatenation("D",String(i)),layer:=0,
      order:=C.bosQuotient.orders[i],state:=lift.state));
  od;
  for i in [1..Length(C.cfFinalBasis)] do
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,Concatenation("stack_lift_C",String(i)));fi;
    f:=AFSCombination(ctx,3,"F2",C.H3,C.cfFinalBasis[i]);
    lift:=AFSStackLift(ctx,1,f);
    if lift.status<>"computed" then return lift;fi;
    Add(data.fermion,rec(name:=Concatenation("C",String(i)),layer:=1,order:=2,state:=lift.state));
  od;
  rows:=ShallowCopy(C.cfPrimaryRows);
  for i in [1..Length(C.H5U.orders)] do
    row:=List(C.H5U.orders,z->0);row[i]:=C.H5U.orders[i];Add(rows,row);
  od;
  solveIndeterminacy:=AFSStackLatticeSolver(rows,Length(C.H5U.orders));
  for i in [1..Length(C.mcFinalBasis)] do
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,Concatenation("stack_lift_B",String(i)));fi;
    f:=AFSCombination(ctx,2,"F2",C.H2,C.mcFinalBasis[i]);
    lift:=AFSStackLiftMC(C,f,solveIndeterminacy);
    if lift.status<>"computed" then return lift;fi;
    Add(data.majorana,rec(name:=Concatenation("B",String(i)),layer:=2,order:=2,state:=lift.state));
  od;
  for g in C.incomingMC1 do Add(data.fermionBoundaries,AFSStackMCBoundary(ctx,g.a));od;
  for i in [1..Length(C.H2.generators)] do
    f:=AFSBar(ctx,2,"F2",C.H2.generators[i]);
    Add(data.bosonBoundaries,AFSStackCFBoundary(ctx,f));
  od;
  for g in C.incomingBos do Add(data.bosonBoundaries,AFSStackSecondaryBoundary(ctx,g.a,g.c));od;
  return AFSStackModel(ctx,data);
end);

BindGlobal("AFSStackBosonOnly",function(C)
  local orders,gens,R,i,co,v,j,S,cert;
  orders:=C.bosQuotient.orders;gens:=[];R:=[];
  for i in [1..Length(orders)] do
    co:=List(orders,x->0);co[i]:=1;co:=C.bosQuotient.lift(co);
    v:=List([1..Dimension(C.ctx.R)(4)],x->0);
    for j in [1..Length(co)] do v:=v+co[j]*C.H4U.generators[j];od;
    Add(gens,rec(name:=Concatenation("D",String(i)),layer:=0,order:=orders[i],nativePhase4Seed:=v));
    co:=List(orders,x->0);co[i]:=orders[i];Add(R,co);
  od;
  S:=AFSSmith(R,Length(R),Length(orders));
  cert:=rec(method:="single-nonzero-filtration-layer",ambientOrders:=C.H4U.orders,
    quotientRelations:=C.bosQuotient.relations,
    quotientSmithColumns:=C.bosQuotient.smith.V);
  return rec(status:="computed",scope:="p+ip-zero-three-layer-extension",invariants:=orders,
    presentation:=R,smith:=S,generators:=gens,enumeratedPhaseProducts:=0,
    witnesses:=List(gens,g->rec(certificateLevel:="final-bosonic-quotient",generator:=g.name,order:=g.order)),
    finalFiltrationCertificate:=cert);
end);

# Reconstruct the actual marked bar lift chosen by the native CF-only path.
# This is evaluated on demand; its half-integral correction cancels under the
# power relation, so the batch calculation need not expand it in advance.
BindGlobal("AFSReconstructNativeCFLift",function(ctx,generator)
  local c,v,op,dv,source,h;
  c:=AFSBar(ctx,3,"F2",generator.nativeCF3Seed);
  v:=AFSBar(ctx,4,"U1s",generator.nativePhase4Seed);
  op:=AFSFormula("obstruction",ctx,rec(p:=2,a:=AFSZero,c:=c));
  dv:=AFSCoboundary(ctx,"U1s",v);
  source:=AFSMemo(function(xs...)
    local value;
    value:=2*(CallFuncList(op,xs)-CallFuncList(dv,xs));
    if not IsInt(value) then Error("native CF comparison difference is not half-integral");fi;
    return value mod 2;
  end);
  h:=AFSSolve(ctx,5,"F2",source);
  if h=fail then Error("native/bar Sq2 comparison failed to be an exact binary cochain");fi;
  return rec(a:=AFSZero,c:=c,v:=AFSCoadd(1,[v,AFSComul(1,1/2,h)]),
    cfPhaseNativeSeed:=generator.nativePhase4Seed,
    nativeCFComparisonGauge:=h,
    construction:="native-Gu-Wen-primitive-with-exact-half-integral-comparison-correction");
end);

# Pure Gu-Wen extension on native cochains. A change of the representative of
# Sq2(c) by delta h changes its phase lift by h/2, which disappears on doubling.
# A different phase primitive changes the relation by twice a bosonic class,
# precisely a change of the marked CF lift. Consequently these native relation
# classes determine the same abstract abelian extension as the full bar law.
BindGlobal("AFSStackCFOnly",function(C)
  local ctx,lower,nd,nc,n,gens,R,witnesses,i,j,g,v,obstruction,nu,beta,
    phase,co,lowerco,row,S,inv,D4,integerResidual;
  ctx:=C.ctx;lower:=AFSStackBosonOnly(C);nd:=Length(lower.generators);
  nc:=Length(C.cfFinalBasis);n:=nd+nc;gens:=ShallowCopy(lower.generators);
  R:=List(lower.presentation,r->Concatenation(r,List([1..nc],i->0)));
  witnesses:=ShallowCopy(lower.witnesses);D4:=AFSDifferential(ctx,4,"Zs");
  for i in [1..nc] do
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,Concatenation("stack_native_CF",String(i)));fi;
    v:=List([1..Dimension(ctx.R)(3)],i->0);
    for j in [1..Length(C.H3.orders)] do v:=v+C.cfFinalBasis[i][j]*C.H3.generators[j];od;
    v:=List(v,x->x mod 2);
    obstruction:=AFSNativeCup(ctx,1,3,v,3,v)/2;
    if IsBound(ctx.omega2) and ctx.omega2<>AFSZero then
      obstruction:=obstruction+AFSNativeCup(ctx,0,2,AFSNative(ctx,2,"F2",ctx.omega2),3,v)/2;
    fi;
    nu:=AFSSolveNative(ctx,5,"U1s",obstruction);
    if nu=fail then Error("final CF class has no native Gu-Wen phase primitive");fi;
    integerResidual:=nu*D4-obstruction;
    if not ForAll(integerResidual,IsInt) then Error("native Gu-Wen primitive equation failed");fi;
    beta:=v*AFSDifferential(ctx,3,"Z");
    if not ForAll(beta,x->x mod 2=0) then Error("CF native seed is not closed modulo two");fi;
    beta:=List(beta,x->(x/2) mod 2);
    phase:=List(2*nu+beta/2,AFSMod1);
    co:=C.H4U.coordinates(phase);
    if co=fail then Error("native CF double is not a closed phase");fi;
    lowerco:=C.bosQuotient.project(co);
    row:=List([1..n],i->0);row[nd+i]:=2;
    for j in [1..nd] do row[j]:=-lowerco[j];od;Add(R,row);
    Add(gens,rec(name:=Concatenation("C",String(i)),layer:=1,order:=2,
      nativeCF3Seed:=v,nativePhase4Seed:=nu,
      cochainReconstruction:="AFSReconstructNativeCFLift"));
    Add(witnesses,rec(certificateLevel:="native-Gu-Wen-doubling-class",
      generator:=Concatenation("C",String(i)),order:=2,nativeCF3Seed:=v,
      nativeObstruction5:=obstruction,nativePhase4Primitive:=nu,
      primitiveIntegerResidual:=integerResidual,nativeSq1:=beta,
      nativeDoublePhase4:=phase,bosonicCohomologyCoordinates:=co,
      finalBosonicCoordinates:=lowerco,fullBarPhaseWitness:=false));
  od;
  S:=AFSSmith(R,Length(R),n);
  inv:=Concatenation(List([S.rank+1..n],i->0),Filtered(List(S.diag,AbsInt),x->x>1));
  return rec(status:="computed",scope:="p+ip-zero-three-layer-extension",invariants:=inv,
    presentation:=R,smith:=S,generators:=gens,witnesses:=witnesses,enumeratedPhaseProducts:=0,
    finalFiltrationCertificate:=rec(method:="native-Gu-Wen-extension-with-no-Majorana-layer",
      bosonic:=C.bosQuotient.orders,fermionRank:=nc,
      doublingFormula:="2 phasePrimitive + half ordinary Bockstein(CF3)"));
end);

# Solve lambda*M=target over F2 and retain every homogeneous direction. This
# operates on presentation coordinates, never on a list of physical phases.
BindGlobal("AFSStackBinaryAffine",function(M,target)
  local n,A,b,k;
  n:=Length(M);
  if Length(target)=0 then return rec(base:=List(M,r->0),kernel:=IdentityMat(n));fi;
  if n=0 then
    if ForAll(target,x->x mod 2=0) then return rec(base:=[],kernel:=[]);else return fail;fi;
  fi;
  A:=List(M,r->List(r,x->(x mod 2)*One(GF(2))));
  b:=SolutionMat(A,List(target,x->(x mod 2)*One(GF(2))));
  if b=fail then return fail;fi;
  k:=NullspaceMat(A);
  return rec(base:=List(b,IntFFE),kernel:=List(k,r->List(r,IntFFE)));
end);

# All abelian extensions 0->H->E->Z2->0 are classes in H/2H. If a nonzero
# class has largest 2-adic cyclic order 2^h, its extension doubles a cyclic
# factor at that height. Lower-height components are removed by automorphisms.
# Thus an affine uncertainty subspace can be classified by linear equations
# at each height: no enumeration of its 2^rank possible elements is needed.
BindGlobal("AFSStackExtensionByTwo",function(lower,leading,ambiguousIndices)
  local n,S,active,weights,i,d,h,levels,z,W,free,poss,aff,high,at,
    projected,M,row,base,changed,k,options,classes,v,R,smith,inv,index,result;
  n:=Length(lower.generators);S:=lower.smith;
  if Length(leading)<>n then Error("upper relation dimension mismatch");fi;
  active:=[];weights:=[];
  for i in [1..n] do
    if i>S.rank then Add(active,i);Add(weights,-1);
    elif AbsInt(S.diag[i]) mod 2=0 then
      Add(active,i);d:=AbsInt(S.diag[i]);h:=0;
      while d mod 2=0 do d:=QuoInt(d,2);h:=h+1;od;
      Add(weights,h);
    fi;
  od;
  if n=0 then z:=[];else z:=List((leading*S.V){active},x->x mod 2);fi;
  W:=List(ambiguousIndices,i->List(S.V[i]{active},x->x mod 2));
  poss:=[];
  if AFSStackBinaryAffine(W,z)<>fail then Add(poss,0);fi;
  levels:=Set(Filtered(weights,h->h<>-1));
  for h in levels do
    high:=Filtered([1..Length(active)],i->weights[i]=-1 or weights[i]>h);
    at:=Filtered([1..Length(active)],i->weights[i]=h);
    aff:=AFSStackBinaryAffine(List(W,r->r{high}),z{high});
    if aff=fail then continue;fi;
    base:=ShallowCopy(z{at});
    for i in [1..Length(W)] do base:=base+aff.base[i]*W[i]{at};od;
    changed:=ForAny(base,x->x mod 2<>0);
    if not changed then
      for k in aff.kernel do
        row:=List(at,j->0);
        for i in [1..Length(W)] do row:=row+k[i]*W[i]{at};od;
        if ForAny(row,x->x mod 2<>0) then changed:=true;break;fi;
      od;
    fi;
    if changed then Add(poss,h);fi;
  od;
  free:=Filtered([1..Length(active)],i->weights[i]=-1);
  if ForAny(z{free},x->x<>0) or ForAny(W,r->ForAny(r{free},x->x<>0)) then Add(poss,-1);fi;
  options:=[];classes:=[];
  for h in poss do
    v:=List([1..n],i->0);
    if h<>0 then index:=active[Position(weights,h)];v:=ShallowCopy(S.Vi[index]);fi;
    R:=List(lower.presentation,r->Concatenation(r,[0]));Add(R,Concatenation(-v,[2]));
    smith:=AFSSmith(R,Length(R),n+1);
    inv:=Concatenation(List([smith.rank+1..n+1],i->0),Filtered(List(smith.diag,AbsInt),x->x>1));
    if not inv in options then Add(options,inv);fi;
    Add(classes,rec(height:=h,invariants:=inv));
  od;
  if Length(poss)=0 then Error("nonempty affine extension family lost every height");fi;
  result:=rec(status:="ambiguous",method:="abelian-Ext1-height-stratification",
    inputRelationModuloAmbiguity:=leading,ambiguousGeneratorIndices:=ambiguousIndices,
    modTwoCyclicColumns:=active,modTwoWeights:=weights,modTwoRelation:=z,
    modTwoAmbiguityRows:=W,possibleHeights:=poss,heightResults:=classes,
    invariantOptions:=options,enumeratedExtensionClasses:=0);
  if Length(options)=1 then result.status:="computed";result.invariants:=options[1];fi;
  return result;
end);

# Torsion p+ip square in the final CF quotient, without its bosonic carry.
# For n=c_s and delta B=s^3, the normalized diagonal product has alpha=0
# and beta=S^1(B)+s B modulo a pure-s multiple of s^3. The latter is an
# incoming Majorana boundary. The integer zero-cochain gauge removing 2c_s
# has no B component (omega=0); its C component is again pulled back from
# C2 and hence a multiple of s^3. The exact unary coordinate comparison is
# recorded separately in runs/formula_audit/pip_c_coordinate_torsion.json.
BindGlobal("AFSStackPipSquareModuloBoson",function(C,lower)
  local ctx,b,db,K,co,rows,sol,nc,nd,i,relation,parity;
  ctx:=C.ctx;
  if IsBound(ctx.omega2) and ctx.omega2<>AFSZero then Error("omega-zero p+ip square cannot be used with a nonzero background");fi;
  if not IsBound(C.pipLiftData) then return rec(status:="unresolved",reason:="missing p+ip lower defining tower");fi;
  if Length(C.mcFinalBasis)<>Length(C.mcPrimaryKernel) then
    return rec(status:="unresolved",reason:="p+ip top lift may need a nonpermanent Majorana adjustment");fi;
  b:=C.pipLiftData.b;db:=AFSCoboundary(ctx,"F2",b);
  parity:=AFSMemo(function(g) return (C.pipLiftData.n(g)+ctx.s(g)) mod 2;end);
  if not AFSStackSupportZero(ctx,1,2,parity) then
    return rec(status:="unresolved",reason:="torsion p+ip representative is not the orientation class modulo two");fi;
  K:=AFSCoadd(2,[AFSCup(1,2,b,2,b),AFSCup(2,2,b,3,db),AFSCup(0,1,ctx.s,2,b)]);
  if not AFSStackSupportZero(ctx,4,2,AFSCoboundary(ctx,"F2",K)) then
    Error("torsion p+ip square CF operation is not closed");fi;
  co:=C.H3.coordinates(AFSNative(ctx,3,"F2",K));
  if co=fail then Error("p+ip square lacks a CF cohomology class");fi;
  rows:=Concatenation(C.cfFinalBasis,List(C.incomingMC1,x->x.coords),2*IdentityMat(Length(co)));
  sol:=AFSStackLatticeSolver(rows,Length(co))(co);
  if sol=fail then return rec(status:="unresolved",reason:="p+ip square outside the final CF quotient plus incoming image");fi;
  nc:=Length(C.cfFinalBasis);nd:=Length(C.bosQuotient.orders);
  relation:=List(lower.generators,g->0);
  for i in [1..nc] do relation[nd+i]:=sol[i] mod 2;od;
  return rec(status:="computed",relationModuloBoson:=relation,
    certificate:=rec(method:="torsion-pip-diagonal-square-modulo-boson",
      nativeMajoranaDefiningCochain:=AFSNative(ctx,2,"F2",b),
      nativeClosedSquareCF:=AFSNative(ctx,3,"F2",K),CFClass:=co,
      finalCFCoordinates:=List(sol{[1..nc]},x->x mod 2),
      formula:="S1(B)+s cup B, S1(B)=B cup1 B+B cup2 delta B",
      pureSignCFIndeterminacy:="s^3 equals incoming majorana_source(s)",
      integerGaugeMajorana:="QD(integer constant modulo2)=0 at omega0",
      coordinateDictionary:="pip_c_coordinate_torsion.json",
      fullUpperPhaseWitness:=false));
end);

BindGlobal("AFSFullStacking",function(C)
  local lower,model,pip,square,family,bosonIndices;
  if Length(C.cfFinalBasis)=0 and Length(C.mcFinalBasis)=0 then
    lower:=AFSStackBosonOnly(C);
  elif Length(C.mcFinalBasis)=0 and IsBoundGlobal("AFSNativeCup") then
    lower:=AFSStackCFOnly(C);
  else
    model:=AFSStackFromClassification(C);
    if model.status<>"computed" then return model;fi;
    lower:=AFSStackClassification(model);
  fi;
  if lower.status<>"computed" then return lower;fi;
  pip:=C.summary.pip;
  if pip.status<>"computed" then
    return rec(status:="unresolved",reason:="p+ip permanent cycles incomplete",lower:=lower);fi;
  if ForAny(pip.orders,o->o<>0) then
    if Number(pip.orders,o->o<>0)<>1 or not 2 in pip.orders then
      return rec(status:="unresolved",reason:="unexpected p+ip torsion quotient",lower:=lower);fi;
    square:=AFSStackPipSquareModuloBoson(C,lower);
    if square.status<>"computed" then return rec(status:="unresolved",reason:=square.reason,lower:=lower);fi;
    bosonIndices:=Filtered([1..Length(lower.generators)],i->lower.generators[i].layer=0);
    family:=AFSStackExtensionByTwo(lower,square.relationModuloBoson,bosonIndices);
    if family.status<>"computed" then
      return rec(status:="unresolved",reason:="bosonic p+ip carry changes the abstract extension group",
        lower:=lower,pipSquareCertificate:=square.certificate,pipExtensionCertificate:=family);
    fi;
    return rec(status:="computed",scope:="full-abstract-3+1D-spin-half-affine-stacking",
      invariants:=Concatenation(List([1..pip.free_rank],i->0),family.invariants),
      lower:=lower,freePipRank:=pip.free_rank,
      freePipCertificate:="free-associated-graded-quotient-splits-in-abelian-category",
      pipSquareCertificate:=square.certificate,pipExtensionCertificate:=family,
      upperCompletion:="abstract-group-independent-of-every-bosonic-carry",
      fullUpperPhaseWitness:=false);
  fi;
  # Ext^1_Z(Z^r,H)=0 in the abelian stacking category. This determines the
  # abstract group without choosing a primitive cochain for each free lift.
  return rec(status:="computed",scope:="full-3+1D-spin-half-affine-stacking",
    invariants:=Concatenation(List([1..pip.free_rank],i->0),lower.invariants),
    lower:=lower,freePipRank:=pip.free_rank,
    freePipCertificate:="free-associated-graded-quotient-splits-in-abelian-category");
end);

BindGlobal("AFSStackExport",function(C,result)
  local ctx,encode,state,lower,out,L,g,w,ex,i;
  ctx:=C.ctx;
  encode:=v->List(v,x->[NumeratorRat(x),DenominatorRat(x)]);
  state:=x->rec(majorana2:=AFSNative(ctx,2,"F2",x.a),
    fermion3:=AFSNative(ctx,3,"F2",x.c),phase4:=encode(AFSNative(ctx,4,"U1s",x.v)),
    construction:=x.construction);
  out:=rec(status:=result.status,
    persistedWitnessType:="native-vectors-plus-explicit-comparison-homotopy-recipes",
    fullBarCochainsPersisted:=false,sourceFiles:=["gap/backend.g","gap/backend_bar.g",
      "gap/formulas.g","gap/formula_data.g","gap/stacking.g"]);
  if IsBound(result.scope) then out.scope:=result.scope;fi;
  if IsBound(result.reason) then out.reason:=result.reason;fi;
  if IsBound(result.invariants) then out.invariants:=result.invariants;fi;
  if IsBound(result.pipSquareCertificate) then out.pipSquareCertificate:=result.pipSquareCertificate;fi;
  if IsBound(result.pipExtensionCertificate) then out.pipExtensionCertificate:=result.pipExtensionCertificate;fi;
  if IsBound(result.upperCompletion) then out.upperCompletion:=result.upperCompletion;fi;
  if IsBound(result.fullUpperPhaseWitness) then out.fullUpperPhaseWitness:=result.fullUpperPhaseWitness;fi;
  if IsBound(result.freePipRank) then out.freePipRank:=result.freePipRank;out.freePipCertificate:=result.freePipCertificate;fi;
  if IsBound(result.lower) then lower:=result.lower;
  elif IsBound(result.presentation) then lower:=result;
  else
    if IsBound(result.partialRelations) then out.partialRelations:=result.partialRelations;fi;
    if IsBound(result.generator) then out.generator:=result.generator;fi;
    return out;
  fi;
  L:=rec(status:=lower.status,scope:=lower.scope,invariants:=lower.invariants,
    presentation:=lower.presentation,smithDiagonal:=lower.smith.diag,
    smithRowTransform:=lower.smith.U,smithColumnTransform:=lower.smith.V,
    generators:=[],witnesses:=[],enumeratedPhaseProducts:=lower.enumeratedPhaseProducts,
    finalFiltrationCertificate:=lower.finalFiltrationCertificate);
  for g in lower.generators do
    ex:=rec(name:=g.name,layer:=g.layer,quotientOrder:=g.order);
    if IsBound(g.state) then ex.lift:=state(g.state);
    else
      ex.nativePhase4Seed:=encode(g.nativePhase4Seed);
      if IsBound(g.nativeCF3Seed) then
        ex.nativeCF3Seed:=g.nativeCF3Seed;ex.construction:="native-Gu-Wen-primitive-class";
      else ex.construction:="bosonic-cohomology-quotient";fi;
    fi;
    Add(L.generators,ex);
  od;
  for w in lower.witnesses do
    if w.certificateLevel="final-bosonic-quotient" then Add(L.witnesses,ShallowCopy(w));continue;fi;
    if w.certificateLevel="native-Gu-Wen-doubling-class" then
      ex:=ShallowCopy(w);ex.nativeObstruction5:=encode(w.nativeObstruction5);
      ex.nativePhase4Primitive:=encode(w.nativePhase4Primitive);ex.nativeDoublePhase4:=encode(w.nativeDoublePhase4);
      Add(L.witnesses,ex);continue;
    fi;
    ex:=rec(certificateLevel:=w.certificateLevel,checkedComparisonSupport:=w.checkedComparisonSupport,
      cfIncomingCoordinates:=w.cfIncoming,bosonicIncomingCoordinates:=w.bosonicIncoming,
      cfGauge2:=AFSNative(ctx,2,"F2",w.cfGauge),
      phaseGauge3:=encode(AFSNative(ctx,3,"U1s",w.phaseGauge)),
      canonical:=state(w.canonical),boundary:=state(w.boundary));
    Add(L.witnesses,ex);
  od;
  out.lower:=L;return out;
end);
