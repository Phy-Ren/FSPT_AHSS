# Exact D2d differential, root-gauge and proper-D2 restriction audit.
# This diagnoses supplied-model/source disagreements without fitting tables.
BindGlobal("U1AuditD2d",function(spin)
  local input,c,HQ,HP,HO,HC,HI,proper,subdata,h,fullElements,embed,
    restrict,subHQ,subHO,roots,i,q,source,seed,state,root,v,full,short,
    incoming,z,sheet,intSource,result;
  Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_14_",spin,".g"));
  input:=U1_INPUT;c:=U1CatalogContext(input,7);
  HQ:=U1Cohomology(c,3,"Zr");HP:=U1Cohomology(c,4,"U1s");HO:=U1Cohomology(c,5,"U1s");
  HC:=U1Cohomology(c,1,"Zs");HI:=U1Cohomology(c,4,"Zr");
  proper:=Filtered([1..Length(input.s)],i->input.s[i]=0);
  subdata:=rec(identity_index:=Position(proper,input.identity_index+1)-1,
    multiplication:=List(proper,i->List(proper,j->Position(proper,input.multiplication[i][j]+1)-1)),
    s:=input.s{proper},rho:=input.rho{proper},omega:=List(proper,i->input.omega[i]{proper}));
  h:=U1FiniteContext(subdata,7);
  fullElements:=List([1..Length(input.s)],i->First(Elements(c.G),g->c.elementIndex(g)=i));
  embed:=g->fullElements[proper[h.elementIndex(g)]];
  for i in Elements(h.G) do for z in Elements(h.G) do
    if embed(i*z)<>embed(i)*embed(z) then Error("Proper subgroup embedding failed");fi;
  od;od;
  restrict:=f->function(xs...) return CallFuncList(f,List(xs,embed));end;
  subHQ:=U1Cohomology(h,3,"Zr");subHO:=U1Cohomology(h,5,"U1s");roots:=[];
  for i in [1..Length(HQ.generators)] do
    q:=U1Bar(c,3,"Zr",HQ.generators[i]);source:=U1ChargeSource(c,3,q);
    result:=rec(index:=i,nativeCharge:=HQ.generators[i],
      nativeSource:=U1Native(c,5,"U1s",source),
      obstructionClass:=HO.coordinates(U1Native(c,5,"U1s",source)),
      properD2ChargeClass:=subHQ.coordinates(U1Native(h,3,"Zr",restrict(q))),
      properD2ObstructionClass:=subHO.coordinates(U1Native(h,5,"U1s",restrict(source))));
    seed:=U1Solve(c,5,"U1s",source);result.obstructed:=seed=fail;
    if seed<>fail then
      state:=rec(sheet:=U1Zero,charge:=q,phase:=seed);root:=U1Power(c,3,state,HQ.orders[i]);
      v:=U1Solve(c,3,"Zr",U1Scale(-1,root.charge));
      if v=fail then Error("Charge torsion power was not exact");fi;
      full:=U1Gauge(c,3,root,U1Zero,v);short:=U1Add(root.phase,U1ChargeGauge(c,3,root.charge,v));
      result.fullGaugeRootPhase:=HP.coordinates(U1Native(c,4,"U1s",full.phase));
      result.shortGaugeRootPhase:=HP.coordinates(U1Native(c,4,"U1s",short));
      result.nativeGauge:=U1Native(c,2,"Zr",v);
      if result.fullGaugeRootPhase<>result.shortGaugeRootPhase then Error("Full and short charge gauges disagree in cohomology");fi;
    fi;
    Add(roots,result);
  od;
  incoming:=[];
  for z in U1Cohomology(c,2,"Zr").generators do
    v:=U1Bar(c,2,"Zr",z);full:=U1Gauge(c,3,U1Vacuum(),U1Zero,v);short:=U1ChargeGauge(c,3,U1Zero,v);
    Add(incoming,rec(nativeParameter:=z,
      full:=HP.coordinates(U1Native(c,4,"U1s",full.phase)),
      short:=HP.coordinates(U1Native(c,4,"U1s",short))));
  od;
  sheet:=U1Bar(c,1,"Zs",HC.generators[1]);intSource:=U1Native(c,4,"Zr",U1IntegerSource(c,3,sheet));
  return rec(group:="D2d",spin:=spin,rawChargeOrders:=HQ.orders,rawPhaseOrders:=HP.orders,
    chargeObstructionTargetOrders:=HO.orders,chargeRoots:=roots,incomingCharge:=incoming,
    rawSheetOrders:=HC.orders,integerCIObstructionNative:=intSource,
    integerCIObstructionTargetOrders:=HI.orders,integerCIObstructionClass:=HI.coordinates(intSource),
    properSubgroupOriginalIndices:=proper,properSubgroupOrders:=rec(charge:=subHQ.orders,obstruction:=subHO.orders),
    gaugeComparison:="Both supplied gauge representatives give identical root and incoming cohomology classes",
    status:="Diagnostic evidence; does not assume agreement with an external classification table");
end);
U1_D2D_AUDIT:=rec(spinless:=U1AuditD2d("spinless"),spin_half:=U1AuditD2d("spin_half"));;
if IsBound(U1_D2D_AUDIT_OUT) then
  U1_D2D_AUDIT_STREAM:=OutputTextFile(U1_D2D_AUDIT_OUT,false);;
  SetPrintFormattingStatus(U1_D2D_AUDIT_STREAM,false);;
  WriteLine(U1_D2D_AUDIT_STREAM,U1JSON(U1_D2D_AUDIT));CloseStream(U1_D2D_AUDIT_STREAM);
fi;
