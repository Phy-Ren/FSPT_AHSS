# Independent finite-group 4+1D AHSS layer classification.
# HAP is used only to build a free resolution. All maps/quotients are explicit.

BindGlobal("AFSD4Context",function(data)
  local perms,Q,pc,pp,G,es,c,i,j,k,start;
  start:=Runtime();
  perms:=List([1..data.order],i->PermList(List([1..data.order],j->data.productTable[j][i])));
  Q:=Group(perms);pc:=IsomorphismPcGroup(Q);pp:=IsomorphismPcpGroup(Image(pc));G:=Image(pp);
  es:=List(perms,x->Image(pp,Image(pc,x)));
  for i in [1..data.order] do for j in [1..data.order] do
    if es[i]*es[j]<>es[data.productTable[i][j]] then Error("model multiplication failed");fi;
    if data.s1[data.productTable[i][j]]<>(data.s1[i]+data.s1[j]) mod 2 then Error("sign character failed");fi;
    for k in [1..data.order] do
      if (data.omega2[j][k]+data.omega2[data.productTable[i][j]][k]+data.omega2[i][data.productTable[j][k]]+data.omega2[i][j]) mod 2<>0 then Error("extension cocycle failed");fi;
    od;
  od;od;
  c:=rec(number:=data.id,G:=G,model:=data,elements:=es,differentialCache:=rec(),smithCache:=rec(),cohomologyCache:=rec(),f2SolveCache:=rec());
  c.elementIndex:=AFSMemo(g->Position(es,g));
  c.s:=AFSZero;if ForAny(data.s1,x->x<>0) then c.s:=g->data.s1[c.elementIndex(g)];fi;
  c.sign:=g->1-2*c.s(g);c.action:=c.sign;
  c.omega2:=AFSZero;if ForAny(data.omega2,row->ForAny(row,x->x<>0)) then c.omega2:=function(g,h)return data.omega2[c.elementIndex(g)][c.elementIndex(h)];end;fi;
  if IsBoundGlobal("AFS_FINITE_RESOLUTION_OVERRIDE") then
    c.R:=CallFuncList(ValueGlobal("AFS_FINITE_RESOLUTION_OVERRIDE"),[G,7]);
  else c.R:=AFSFiniteHolonomyResolution(G,7);fi;
  c.bar:=AFSComparison(c.R);
  c.buildCpuMs:=Runtime()-start;
  Print("AFS_D4_CONTEXT ",data.id," order=",Size(G)," dimensions=",List([0..7],k->Dimension(c.R)(k)),"\n");
  return c;
end);

BindGlobal("AFSD4Sum",function(fs)
  if Length(fs)=0 then return AFSZero;fi;
  return AFSMemo(function(xs...)return Sum(fs,f->CallFuncList(f,xs)) mod 2;end);
end);
BindGlobal("AFSD4MajoranaSource",function(c,r,b)
  local beta,db;
  db:=AFSCoboundary(c,"Z",b);
  beta:=AFSMemo(function(xs...)local v;v:=CallFuncList(db,xs);if v mod 2<>0 then Error("MC Bockstein input not closed");fi;return (v/2) mod 2;end);
  return AFSD4Sum([AFSCup(r-2,r,b,r,b),AFSCup(0,2,c.omega2,r,b),AFSCup(0,1,c.s,r+1,beta)]);
end);
BindGlobal("AFSD4CFPhase",function(c,q,b)
  return AFSHalf(AFSD4Sum([AFSCup(q-2,q,b,q,b),AFSCup(0,2,c.omega2,q,b)]));
end);
BindGlobal("AFSD4PhaseClass",function(c,k,H,f)
  local co;
  if IsBoundGlobal("AFS4_USE_PHASE_CYCLES") and ValueGlobal("AFS4_USE_PHASE_CYCLES")=true then
    # All callers supply an obstruction on a legal lower tower. Closure is
    # established by that formula identity; evaluate its exact Smith periods.
    return AFSU1BarCoordinates(c,k,H,f);
  fi;
  co:=H.coordinates(AFSNative(c,k,"U1s",f));
  if co=fail then Error("dimension-four phase not closed at degree ",k);fi;return co;
end);
BindGlobal("AFSD4HasTwo",function(orders)return ForAny(orders,o->o=0 or o mod 2=0);end);

# r is the Majorana degree. This computes both primary operations and the
# secondary Majorana obstruction modulo the image of the CF primary map.
BindGlobal("AFSD4Operations",function(c,r)
  local O,Hb,Hc,Ht,Hf,b,cf,source,co,i,ker,basis,phase,raw,rows,final,v,j;
  O:=rec(r:=r);Hb:=AFSCohomology(c,r,"F2");Hc:=AFSCohomology(c,r+1,"F2");
  Hf:=AFSCohomology(c,r+2,"F2");Ht:=AFSCohomology(c,r+3,"U1s");
  O.Hb:=Hb;O.Hc:=Hc;O.Hf:=Hf;O.Ht:=Ht;O.mcPrimary:=[];O.cfPrimary:=[];
  AFSStage(c,Concatenation("degree",String(r),"_primary"));
  for i in [1..Length(Hb.orders)] do
    b:=AFSBar(c,r,"F2",Hb.generators[i]);source:=AFSD4MajoranaSource(c,r,b);
    co:=Hf.coordinates(AFSNative(c,r+2,"F2",source));
    if co=fail then Error("MC primary is not closed");fi;Add(O.mcPrimary,co);
  od;
  for i in [1..Length(Hc.orders)] do
    if not AFSD4HasTwo(Ht.orders) then co:=List(Ht.orders,x->0);
    else cf:=AFSBar(c,r+1,"F2",Hc.generators[i]);co:=AFSD4PhaseClass(c,r+3,Ht,AFSD4CFPhase(c,r+1,cf));fi;
    AFSOrderTwoBits(Ht.orders,co);Add(O.cfPrimary,co);
  od;
  O.phaseTarget:=AFSQuotient(Ht.orders,O.cfPrimary);
  O.cfKernel:=AFSF2Kernel(List(O.cfPrimary,row->AFSOrderTwoBits(Ht.orders,row)),Length(Hc.orders));
  O.mcKernel:=AFSF2Kernel(O.mcPrimary,Length(Hb.orders));O.mcSecondary:=[];O.lifts:=[];
  AFSStage(c,Concatenation("degree",String(r),"_secondary"));
  for basis in O.mcKernel do
    b:=AFSCombination(c,r,"F2",Hb,basis);source:=AFSD4MajoranaSource(c,r,b);
    cf:=AFSSolve(c,r+2,"F2",source);if cf=fail then Error("MC primary-kernel lift failed");fi;
    if not AFSD4HasTwo(O.phaseTarget.orders) then
      raw:=List(Ht.orders,x->0);co:=List(O.phaseTarget.orders,x->0);phase:=fail;
    else
      phase:=AFSD4Phase(c,r-1,AFSZero,b,cf);raw:=AFSD4PhaseClass(c,r+3,Ht,phase);co:=O.phaseTarget.project(raw);
    fi;
    AFSOrderTwoBits(O.phaseTarget.orders,co);Add(O.mcSecondary,co);
    Add(O.lifts,rec(leading:=basis,b:=b,cf:=cf,phase:=phase,raw:=raw,projected:=co));
  od;
  ker:=AFSF2Kernel(List(O.mcSecondary,row->AFSOrderTwoBits(O.phaseTarget.orders,row)),Length(O.mcKernel));
  O.mcFinal:=[];
  for basis in ker do
    v:=List(Hb.orders,x->0);for i in [1..Length(basis)] do v:=v+basis[i]*O.mcKernel[i];od;
    Add(O.mcFinal,List(v,x->x mod 2));
  od;
  rows:=ShallowCopy(O.cfPrimary);for b in O.lifts do Add(rows,b.raw);od;
  O.pipPhaseTarget:=AFSQuotient(Ht.orders,rows);
  return O;
end);

# Explicit p+ip lower tower. Report raw and quotient classes separately.
BindGlobal("AFSD4PipTower",function(c,p,n,O,maximumPage)
  local R,source,b,t,co,adjust,cf,phase,raw;
  R:=rec();source:=AFSFormula("pip_majorana",c,rec(p:=p,n:=n));
  R.d2:=O.Hc.coordinates(AFSNative(c,p+2,"F2",source));
  if R.d2=fail then Error("p+ip d2 not closed");fi;
  if ForAny(R.d2,x->x<>0) then R.page:=2;R.status:="killed";return R;fi;
  R.page:=2;R.status:="survives";if maximumPage=2 then return R;fi;
  b:=AFSSolve(c,p+2,"F2",source);if b=fail then Error("p+ip d2 primitive failed");fi;
  t:=AFSFormula("pip_parity",c,rec(p:=p,n:=n,b:=b));
  co:=O.Hf.coordinates(AFSNative(c,p+3,"F2",t));if co=fail then Error("p+ip d3 not closed");fi;
  R.d3Raw:=co;adjust:=AFSF2SolveRows(O.mcPrimary,co);
  R.d3:=AFSQuotient(O.Hf.orders,O.mcPrimary).project(co);
  if adjust=fail then R.page:=3;R.status:="killed";return R;fi;
  if ForAny(adjust,x->x<>0) then b:=AFSAddF2(b,AFSCombination(c,p+1,"F2",O.Hb,adjust));t:=AFSFormula("pip_parity",c,rec(p:=p,n:=n,b:=b));fi;
  cf:=AFSSolve(c,p+3,"F2",t);if cf=fail then Error("p+ip d3 adjustment failed");fi;
  R.majoranaAdjustment:=adjust;R.b:=b;R.cf:=cf;R.page:=3;R.status:="survives";
  if maximumPage=3 then return R;fi;
  if Length(O.pipPhaseTarget.orders)=0 then raw:=List(O.Ht.orders,x->0);co:=[];R.phaseSkipped:="zero-target";
  else
    phase:=AFSD4Phase(c,p,n,b,cf);raw:=AFSD4PhaseClass(c,p+4,O.Ht,phase);co:=O.pipPhaseTarget.project(raw);R.phase:=phase;
  fi;
  R.d4Raw:=raw;R.d4:=co;R.page:=4;R.status:="survives";
  if ForAny(co,x->x<>0) then R.status:="killed";fi;
  return R;
end);

# Finite subgroups represented by ambient cohomology coordinates. Breadth-first
# enumeration retains words, allowing each computed homomorphism to be checked
# on every relation. Tables here have at most 64 integer-layer classes.
BindGlobal("AFSD4Subgroup",function(orders,generators)
  local z,S,i,j,w,x,k,G,gs,els;
  z:=List(orders,x->0);S:=rec(ambientOrders:=orders,generators:=generators,elements:=[z],words:=[List(generators,x->0)]);
  i:=1;while i<=Length(S.elements) do
    for j in [1..Length(generators)] do
      x:=List([1..Length(orders)],k->(S.elements[i][k]+generators[j][k]) mod orders[k]);
      if not x in S.elements then w:=ShallowCopy(S.words[i]);w[j]:=w[j]+1;Add(S.elements,x);Add(S.words,w);fi;
    od;i:=i+1;
  od;
  if Length(orders)=0 then S.orders:=[];
  else
    G:=AbelianGroup(IsPcGroup,orders);gs:=IndependentGeneratorsOfAbelianGroup(G);
    if List(gs,Order)<>orders then
      # A presentation with explicit ordered cyclic factors avoids relying on
      # GAP's invariant-factor regrouping for the ambient coordinates.
      G:=DirectProduct(List(orders,o->CyclicGroup(IsPermGroup,o)));
      gs:=List([1..Length(orders)],i->Image(Embedding(G,i),GeneratorsOfGroup(Source(Embedding(G,i)))[1]));
    fi;
    els:=List(generators,v->Product([1..Length(orders)],i->gs[i]^v[i]));
    S.orders:=AbelianInvariants(Subgroup(G,els));
  fi;return S;
end);
BindGlobal("AFSD4Kernel",function(S,images,targetOrders)
  local vals,i,j,k,x,y,z,ker,gens,T;
  z:=List(targetOrders,x->0);vals:=[];
  for i in [1..Length(S.elements)] do
    y:=ShallowCopy(z);for j in [1..Length(images)] do y:=y+S.words[i][j]*images[j];od;
    y:=List([1..Length(y)],k->y[k] mod targetOrders[k]);Add(vals,y);
  od;
  for i in [1..Length(S.elements)] do for j in [1..Length(S.generators)] do
    x:=List([1..Length(S.ambientOrders)],k->(S.elements[i][k]+S.generators[j][k]) mod S.ambientOrders[k]);k:=Position(S.elements,x);
    y:=List([1..Length(targetOrders)],q->(vals[i][q]+images[j][q]) mod targetOrders[q]);
    if y<>vals[k] then Error("AHSS operation violates a source-group relation");fi;
  od;od;
  ker:=Filtered([1..Length(vals)],i->vals[i]=z);gens:=[];T:=AFSD4Subgroup(S.ambientOrders,gens);
  for i in ker do if not S.elements[i] in T.elements then Add(gens,S.elements[i]);T:=AFSD4Subgroup(S.ambientOrders,gens);fi;od;
  return T;
end);

BindGlobal("AFSD4PublicTower",function(R)
  local out,key;out:=rec();for key in RecNames(R) do if not IsFunction(R.(key)) then out.(key):=R.(key);fi;od;return out;
end);
BindGlobal("AFSD4Classify",function(c)
  local O2,O3,H1,H2,S,orders,initial,pages,page,images,v,n,R,Q,i,j,k,inMC,inCF,inBos,bosRows,mc,cf,bos,result,incoming,checks,predicted,actual,checkIndices;
  O2:=AFSD4Operations(c,2);O3:=AFSD4Operations(c,3);
  H1:=AFSCohomology(c,1,"Zs");H2:=AFSCohomology(c,2,"Zs");
  if ForAny(H2.orders,x->x=0) then Error("finite H2 has free summand");fi;
  inMC:=[];inCF:=[];inBos:=[];incoming:=[];
  for i in [1..Length(H1.orders)] do
    n:=AFSBar(c,1,"Zs",H1.generators[i]);R:=AFSD4PipTower(c,1,n,O2,4);
    Add(inMC,R.d2);
    if R.page>=3 then Add(inCF,R.d3Raw);fi;
    if R.page>=4 then Add(inBos,R.d4Raw);fi;
    Add(incoming,AFSD4PublicTower(R));
  od;
  mc:=AFSF2Subquotient(O3.mcFinal,inMC,Length(O3.Hb.orders));
  cf:=AFSF2Subquotient(O3.cfKernel,Concatenation(O2.mcPrimary,inCF),Length(O3.Hc.orders));
  bosRows:=ShallowCopy(O2.cfPrimary);for R in O2.lifts do Add(bosRows,R.raw);od;Append(bosRows,inBos);
  bos:=AFSQuotient(O2.Ht.orders,bosRows);
  S:=AFSD4Subgroup(H2.orders,IdentityMat(Length(H2.orders)));initial:=ShallowCopy(S.orders);pages:=[];
  for page in [2..4] do
    AFSStage(c,Concatenation("pip_d",String(page)));images:=[];orders:=[];
    if page=2 then orders:=O3.Hc.orders;
    elif page=3 then orders:=AFSQuotient(O3.Hf.orders,O3.mcPrimary).orders;
    else orders:=O3.pipPhaseTarget.orders;fi;
    result:=rec(page:=page,sourceOrders:=S.orders,targetOrders:=orders,generators:=ShallowCopy(S.generators),evaluations:=[]);
    for v in S.generators do
      n:=AFSCombination(c,2,"Zs",H2,v);R:=AFSD4PipTower(c,2,n,O3,page);
      if R.page<page then Error("kernel generator lost earlier obstruction certificate");fi;
      if page=2 then Add(images,R.d2);elif page=3 then Add(images,R.d3);else Add(images,R.d4);fi;
      Add(result.evaluations,AFSD4PublicTower(R));
    od;
    checks:=[];
    if Length(S.elements)<=8 then checkIndices:=[1..Length(S.elements)];
    else checkIndices:=Set([1,2,Minimum(3,Length(S.elements)),Length(S.elements)]);fi;
    for i in checkIndices do
      v:=S.elements[i];
      if ForAll(v,x->x=0) or v in S.generators then continue;fi;
      predicted:=List(orders,x->0);for j in [1..Length(images)] do predicted:=predicted+S.words[i][j]*images[j];od;
      predicted:=List([1..Length(orders)],k->predicted[k] mod orders[k]);
      n:=AFSCombination(c,2,"Zs",H2,v);R:=AFSD4PipTower(c,2,n,O3,page);
      if R.page<page then Error("direct subgroup-sum evaluation failed prior obstruction");fi;
      if page=2 then actual:=R.d2;elif page=3 then actual:=R.d3;else actual:=R.d4;fi;
      if actual<>predicted then Error("direct cochain AHSS map is not additive on subgroup element ",v);fi;
      Add(checks,rec(source:=v,actual:=actual,predicted:=predicted));
    od;
    result.directAdditivityChecks:=checks;result.allSourceClassesChecked:=Length(S.elements)<=8;
    S:=AFSD4Kernel(S,images,orders);result.survivingOrders:=S.orders;Add(pages,result);
  od;
  result:=rec(model:=c.model.id,dimension:="4+1D",scope:="associated-graded decoration layers; no stacking extensions asserted",status:="computed",sptset_loaded:=IsBound(GAPInfo.PackagesLoaded.sptset),
    initial:=rec(pip:=H2.orders,majorana:=O3.Hb.orders,complex_fermion:=O3.Hc.orders,bosonic:=O2.Ht.orders),
    layers:=rec(pip:=S.orders,majorana:=List(mc,x->2),complex_fermion:=List(cf,x->2),bosonic:=bos.orders),
    pipPages:=pages,incomingPip:=incoming,
    maps:=rec(mcIncomingPrimary:=O2.mcPrimary,mcOutgoingPrimary:=O3.mcPrimary,cfIncomingPrimary:=O2.cfPrimary,cfOutgoingPrimary:=O3.cfPrimary,mcIncomingSecondary:=O2.mcSecondary,mcOutgoingSecondary:=O3.mcSecondary,mcIncomingSecondaryRaw:=List(O2.lifts,x->x.raw),mcOutgoingSecondaryRaw:=List(O3.lifts,x->x.raw)),
    targets:=rec(incomingPhase:=O2.phaseTarget.orders,outgoingPhase:=O3.phaseTarget.orders,pipIncomingTerminal:=O2.pipPhaseTarget.orders,pipOutgoingTerminal:=O3.pipPhaseTarget.orders),
    nativeCohomology:=List([1..6],i->rec(degree:=i,f2:=AFSCohomology(c,i,"F2").orders,zs:=AFSCohomology(c,i,"Zs").orders)),
    witnesses:=rec(majoranaBasis:=mc,complexFermionBasis:=cf,pipBasis:=S.generators,bosonicRelations:=bosRows),
    resolutionDimensions:=List([0..7],k->Dimension(c.R)(k)),cpuMs:=Runtime(),stageTimings:=c.stageTimings);
  if result.sptset_loaded then Error("SptSet loaded unexpectedly");fi;
  return result;
end);
