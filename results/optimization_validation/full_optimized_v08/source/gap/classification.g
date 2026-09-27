# Independent 3+1D spin-half space-group AHSS.
# No space-group classification table or SptSet operation is consulted.

BindGlobal("AFSQuotient",function(orders,relations)
  local n,M,i,row,S,active,Q;
  n:=Length(orders); M:=[];
  for i in [1..n] do
    if orders[i]<>0 then row:=List([1..n],j->0); row[i]:=orders[i]; Add(M,row); fi;
  od;
  Append(M,relations); S:=AFSSmith(M,Length(M),n);
  active:=Filtered([1..n],i->i>S.rank or AbsInt(S.diag[i])>1);
  Q:=rec(smith:=S,active:=active,relations:=M,ambientOrders:=orders,
    orders:=List(active,function(i) if i>S.rank then return 0; else return AbsInt(S.diag[i]); fi; end));
  Q.project:=function(v)
    local w;
    if n=0 then return []; fi;
    w:=v*S.V;
    return List(active,function(i) if i>S.rank then return w[i]; else return w[i] mod AbsInt(S.diag[i]); fi; end);
  end;
  Q.lift:=function(v)
    local w,j;
    w:=List([1..n],i->0);
    for j in [1..Length(active)] do w:=w+v[j]*S.Vi[active[j]]; od;
    return w;
  end;
  return Q;
end);

BindGlobal("AFSOrderTwoBits",function(orders,v)
  local out,i,m;
  out:=[];
  for i in [1..Length(orders)] do
    m:=orders[i];
    if m=0 then
      if v[i]<>0 then Error("order-two map has nonzero free image"); fi;
    elif m mod 2=1 then
      if v[i] mod m<>0 then Error("order-two map has nonzero odd image"); fi;
    else
      if (2*v[i]) mod m<>0 then Error("map image does not have order at most two"); fi;
      Add(out,(2*(v[i] mod m))/m);
    fi;
  od;
  return out;
end);

BindGlobal("AFSF2Kernel",function(rows,n)
  if n=0 then return []; fi;
  if Length(rows)<>n then Error("source matrix dimension mismatch"); fi;
  if Length(rows[1])=0 then return IdentityMat(n); fi;
  return List(NullspaceMat(List(rows,r->List(r,x->(x mod 2)*One(GF(2))))),r->List(r,IntFFE));
end);

BindGlobal("AFSF2Subquotient",function(kernel,incoming,n)
  local sp,spk,x,out;
  sp:=AFSSpan(n); spk:=AFSSpan(n);
  for x in kernel do AFSInsert(spk,x); od;
  for x in incoming do
    if ForAny(AFSReduce(spk,x).remainder,z->z<>0) then Error("incoming image is outside outgoing kernel"); fi;
    AFSInsert(sp,x);
  od;
  out:=[];
  for x in kernel do
    if AFSInsert(sp,x) then Add(out,ShallowCopy(sp.rows[Length(sp.rows)])); fi;
  od;
  return out;
end);

BindGlobal("AFSCombination",function(c,k,coeff,H,coordinates)
  local v,i;
  v:=List([1..Dimension(c.R)(k)],j->0);
  for i in [1..Length(coordinates)] do v:=v+coordinates[i]*H.generators[i]; od;
  return AFSBar(c,k,coeff,v);
end);

BindGlobal("AFSAddF2",function(f,g)
  return AFSMemo(function(xs...) return (CallFuncList(f,xs)+CallFuncList(g,xs)) mod 2; end);
end);

BindGlobal("AFSHalf",function(f)
  return AFSMemo(function(xs...) return (CallFuncList(f,xs) mod 2)/2; end);
end);

BindGlobal("AFSClosedPhaseClass",function(c,k,H,f)
  if k=5 and IsBound(AFSU1BarCoordinates) and
      (not IsBound(AFS_USE_PHASE_PERIODS) or AFS_USE_PHASE_PERIODS=true) then
    return AFSU1BarCoordinates(c,k,H,f);
  fi;
  return H.coordinates(AFSNative(c,k,"U1s",f));
end);

BindGlobal("AFSStage",function(c,name)
  if not IsBound(c.stageTimings) then c.stageTimings:=[]; fi;
  Add(c.stageTimings,rec(stage:=name,cpu_ms:=Runtime()));
  Print("AFS_STAGE ",c.number," ",name," cpu_ms=",Runtime(),"\n");
end);

BindGlobal("AFSClassify",function(c)
  local C,H1,H2,H3,H4,H5,H4F,m1,m2,m3,i,j,a,b,cf,op,v,co,
    sourceRows,sourceFns,Q3,Q2,primaryMC,mcKernel,cfKernel,cfBasis,
    bos3,incomingBos,bosRows,kerIncoming,O4,O5,secondaryRows,mcSecond,
    basis,record,source,phase,target5,Hp,pip,n1,ds,rank,finalMC,useNative,useTargetCycles,sNative,beta;
  C:=rec(ctx:=c,status:="running");
  useNative:=IsBound(AFSNativeCup) and (not IsBound(AFS_USE_NATIVE) or AFS_USE_NATIVE=true);
  useTargetCycles:=useNative and IsBound(AFSNativeSq2U1Coordinates) and
    (not IsBound(AFS_USE_TARGET_CYCLES) or AFS_USE_TARGET_CYCLES=true);
  sNative:=AFSNative(c,1,"F2",c.s);
  AFSStage(c,"cohomology");
  H1:=AFSCohomology(c,1,"F2"); H2:=AFSCohomology(c,2,"F2");
  H3:=AFSCohomology(c,3,"F2"); H4F:=AFSCohomology(c,4,"F2");
  H4:=AFSCohomology(c,4,"U1s"); H5:=AFSCohomology(c,5,"U1s");
  C.H1:=H1; C.H2:=H2; C.H3:=H3; C.H4U:=H4; C.H5U:=H5;
  m1:=Length(H1.orders); m2:=Length(H2.orders); m3:=Length(H3.orders);

  AFSStage(c,"primary_cf");
  Q3:=[];
  for i in [1..m3] do
    if ForAll(H5.orders,o->o<>0 and o mod 2=1) then co:=List(H5.orders,o->0);
    elif useTargetCycles then co:=AFSNativeSq2U1Coordinates(c,3,H3.generators[i],H5);
    else
      if useNative then
        v:=AFSNativeCup(c,1,3,H3.generators[i],3,H3.generators[i])/2;
      else
        cf:=AFSBar(c,3,"F2",H3.generators[i]);
        # A closed degree-three CF cochain has O5 = (c cup_1 c)/2.
        phase:=AFSHalf(AFSCup(1,3,cf,3,cf)); v:=AFSNative(c,5,"U1s",phase);
      fi;
      co:=H5.coordinates(v);
    fi;
    if co=fail then Error("CF primary phase is not closed"); fi;
    AFSOrderTwoBits(H5.orders,co); Add(Q3,co);
  od;
  C.cfPrimaryRows:=Q3;
  cfKernel:=AFSF2Kernel(List(Q3,r->AFSOrderTwoBits(H5.orders,r)),m3);
  target5:=AFSQuotient(H5.orders,Q3); C.secondaryTarget:=target5;

  AFSStage(c,"primary_mc_and_bos");
  primaryMC:=[]; Q2:=[];
  for i in [1..m2] do
    b:=AFSBar(c,2,"F2",H2.generators[i]);
    if Length(H4F.orders)=0 then co:=[];
    else
      if useNative then
        beta:=H2.generators[i]*AFSDifferential(c,2,"Z");
        if not ForAll(beta,x->IsInt(x/2)) then Error("nonintegral closed-cochain Bockstein"); fi;
        beta:=List(beta,x->(x/2) mod 2);
        v:=AFSNativeCup(c,0,2,H2.generators[i],2,H2.generators[i])+AFSNativeCup(c,0,1,sNative,3,beta);
        co:=H4F.coordinates(List(v,x->x mod 2));
      else
        source:=AFSFormula("majorana_source",c,rec(p:=2,a:=b));
        co:=H4F.coordinates(AFSNative(c,4,"F2",source));
      fi;
    fi;
    if co=fail then Error("MC primary source is not closed"); fi;
    Add(primaryMC,co);
    if ForAll(H4.orders,o->o<>0 and o mod 2=1) then co:=List(H4.orders,o->0);
    elif useTargetCycles then co:=AFSNativeSq2U1Coordinates(c,2,H2.generators[i],H4);
    else
      if useNative then
        v:=AFSNativeCup(c,0,2,H2.generators[i],2,H2.generators[i])/2;
      else
        # A closed degree-two CF cochain has O4 = (b cup b)/2.
        phase:=AFSHalf(AFSCup(0,2,b,2,b));v:=AFSNative(c,4,"U1s",phase);
      fi;
      co:=H4.coordinates(v);
    fi;
    if co=fail then Error("incoming bosonic primary is not closed"); fi;
    Add(Q2,co);
  od;
  C.mcPrimaryRows:=primaryMC; C.bosPrimaryRows:=Q2;
  mcKernel:=AFSF2Kernel(primaryMC,m2); C.mcPrimaryKernel:=mcKernel;
  bos3:=AFSQuotient(H4.orders,Q2);

  AFSStage(c,"incoming_mc");
  sourceRows:=[]; C.incomingMC1:=[];
  for i in [1..m1] do
    a:=AFSBar(c,1,"F2",H1.generators[i]);
    source:=AFSFormula("majorana_source",c,rec(p:=1,a:=a));
    co:=H3.coordinates(AFSNative(c,3,"F2",source));
    if co=fail then Error("incoming MC source is not closed"); fi;
    Add(sourceRows,co); Add(C.incomingMC1,rec(a:=a,source:=source,coords:=co));
  od;
  cfBasis:=AFSF2Subquotient(cfKernel,sourceRows,m3); C.cfFinalBasis:=cfBasis;

  AFSStage(c,"secondary_bos");
  kerIncoming:=AFSF2Kernel(sourceRows,m1); incomingBos:=[]; bosRows:=ShallowCopy(Q2);
  for basis in kerIncoming do
    if ForAll(bos3.orders,o->o<>0 and o mod 2=1) then continue; fi;
    a:=AFSCombination(c,1,"F2",H1,basis);
    source:=AFSFormula("majorana_source",c,rec(p:=1,a:=a));
    cf:=AFSSolve(c,3,"F2",source);
    if cf=fail then Error("incoming primary-kernel lift failed"); fi;
    phase:=AFSFormula("obstruction",c,rec(p:=1,a:=a,c:=cf));
    co:=H4.coordinates(AFSNative(c,4,"U1s",phase));
    if co=fail then Error("incoming secondary phase is not closed"); fi;
    AFSOrderTwoBits(bos3.orders,bos3.project(co));
    Add(incomingBos,rec(a:=a,c:=cf,phase:=phase,coords:=co,leading:=basis)); Add(bosRows,co);
  od;
  C.incomingBos:=incomingBos; C.bosQuotient:=AFSQuotient(H4.orders,bosRows);

  AFSStage(c,"secondary_mc");
  secondaryRows:=[]; C.mcLifts:=[];
  for basis in mcKernel do
    b:=AFSCombination(c,2,"F2",H2,basis);
    record:=rec(a:=b,leading:=basis);
    if ForAll(target5.orders,o->o<>0 and o mod 2=1) then
      Add(secondaryRows,List(target5.orders,o->0));
      record.secondaryCertificate:="zero-two-primary-target";
    else
      source:=AFSFormula("majorana_source",c,rec(p:=2,a:=b));
      cf:=AFSSolve(c,4,"F2",source);
      if cf=fail then Error("MC primary-kernel lift failed"); fi;
      phase:=AFSFormula("obstruction",c,rec(p:=2,a:=b,c:=cf));
      co:=AFSClosedPhaseClass(c,5,H5,phase);
      if co=fail then Error("MC secondary phase is not closed"); fi;
      Add(secondaryRows,target5.project(co));
      record.c:=cf; record.obstruction:=phase; record.obstructionCoordinates:=co;
    fi;
    Add(C.mcLifts,record);
  od;
  mcSecond:=AFSF2Kernel(List(secondaryRows,r->AFSOrderTwoBits(target5.orders,r)),Length(mcKernel));
  finalMC:=[];
  for basis in mcSecond do
    v:=List([1..m2],i->0);
    for i in [1..Length(mcKernel)] do v:=v+basis[i]*mcKernel[i]; od;
    Add(finalMC,List(v,x->x mod 2));
  od;
  C.mcFinalBasis:=finalMC; C.mcSecondaryRows:=secondaryRows;

  AFSStage(c,"pip");
  Hp:=AFSCohomology(c,1,"Zs"); C.Hp:=Hp;
  pip:=rec(free_rank:=Number(Hp.orders,o->o=0),status:="computed",orders:=Filtered(Hp.orders,o->o=0),torsion:=[]);
  for i in [1..Length(Hp.orders)] do
    if Hp.orders[i]=0 then continue; fi;
    if Hp.orders[i]<>2 then Error("unexpected torsion in H1(Zs)"); fi;
    # The unique H1(Z_s) torsion generator is the canonical sign cocycle.
    # Keeping this representative also fixes the integer carry in stacking.
    n1:=c.s;
    co:=Hp.coordinates(AFSNative(c,1,"Zs",n1));
    if co=fail or co[i]<>1 then Error("canonical sign cocycle is not the H1 torsion generator"); fi;
    op:=AFSFormula("pip_majorana",c,rec(p:=1,n:=n1));
    co:=H3.coordinates(AFSNative(c,3,"F2",op));
    if co=fail then Error("pip primary source is not closed"); fi;
    if ForAny(co,x->x<>0) then
      Add(pip.torsion,rec(status:="killed",page:=2,obstruction:=co));
    elif IsBound(AFSClassifyPipTorsion) then
      record:=AFSClassifyPipTorsion(C,n1,op);
      Add(pip.torsion,record);
      if record.status="survives" then Add(pip.orders,2);
      elif record.status<>"killed" then pip.status:="unresolved"; fi;
    else
      Add(pip.torsion,rec(status:="unresolved",reason:="higher-pip-differentials-pending"));
      pip.status:="unresolved";
    fi;
  od;
  C.summary:=rec(space_group:=c.number,convention:="physical-spin-half-det-sign-omega0",scope:="3+1D-full-affine-associated-graded",pip:=pip,
    majorana:=List(finalMC,x->2),complex_fermion:=List(cfBasis,x->2),bosonic:=C.bosQuotient.orders,
    ranks:=rec(H1F2:=m1,H2F2:=m2,H3F2:=m3,MC_primary:=m2-Length(mcKernel),MC_secondary:=Length(mcKernel)-Length(finalMC),CF_primary:=m3-Length(cfKernel),CF_incoming:=Length(cfKernel)-Length(cfBasis)),
    native_primary_operations:=useNative,
    native_target_cycles:=useTargetCycles,
    resolution_dimensions:=List([0..6],k->Dimension(c.R)(k)),cpu_ms:=Runtime());
  C.status:=pip.status; C.summary.status:=C.status;
  AFSStage(c,"classification_end");
  return C;
end);
