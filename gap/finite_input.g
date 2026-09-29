# Exact finite input checks and background gauge; no classification table input.
BindGlobal("AFSPrepareFiniteInput",function(ctx)
  local H0,H1,H2,native,co,gauge,audit;
  H0:=AFSCohomology(ctx,0,"Zs");H1:=AFSCohomology(ctx,1,"Zs");
  if ctx.s=AFSZero then
    if H0.orders<>[0] or H1.orders<>[] then Error("finite unitary H0/H1 mismatch");fi;
  elif H0.orders<>[] or H1.orders<>[2] then Error("finite signed H0/H1 mismatch");fi;
  audit:=rec(finiteGroupOrder:=Size(ctx.G),integerH0:=H0.orders,integerH1:=H1.orders,
    backgroundGaugeReducedToZero:=false);
  if ctx.omega2<>AFSZero then
    native:=AFSNative(ctx,2,"F2",ctx.omega2);H2:=AFSCohomology(ctx,2,"F2");co:=H2.coordinates(native);
    if co=fail then Error("finite extension background is not closed");fi;
    audit.nativeOriginalOmega:=native;audit.originalOmegaClass:=co;
    if ForAll(co,x->x=0) then
      gauge:=AFSSolve(ctx,2,"F2",ctx.omega2);if gauge=fail then Error("exact background lacks primitive");fi;
      audit.nativeTrivializing1:=AFSNative(ctx,1,"F2",gauge);
      if List(audit.nativeTrivializing1*AFSDifferential(ctx,1,"F2"),x->x mod 2)<>native then Error("background gauge witness failed");fi;
      ctx.originalOmega2:=ctx.omega2;ctx.omegaTrivialization:=gauge;ctx.omega2:=AFSZero;
      audit.backgroundGaugeReducedToZero:=true;
    fi;
  fi;
  return audit;
end);

# Complete known U4 lower group; retain every unprovided p+ip CF/bosonic carry.
BindGlobal("AFSFiniteUpperExtension",function(C,R)
  local lower,co,coordinates,mc,leading,i,indices;
  if not IsBound(R.lower) or R.lower.status<>"computed" then Error("lower stacking incomplete");fi;
  lower:=R.lower;
  if C.summary.pip.orders=[] then return rec(status:="computed",invariantOptions:=[lower.invariants]);fi;
  if C.summary.pip.orders<>[2] then Error("finite H1(Z_s) torsion must be one C2");fi;
  co:=C.H2.coordinates(AFSNative(C.ctx,2,"F2",C.ctx.omega2));
  coordinates:=AFSF2SolveRows(C.mcFinalBasis,co);
  mc:=Filtered([1..Length(lower.generators)],i->lower.generators[i].layer=2);
  if coordinates=fail or Length(mc)<>Length(coordinates) then Error("p+ip leading MC square mismatch");fi;
  leading:=List(lower.generators,g->0);
  for i in [1..Length(mc)] do leading[mc[i]]:=coordinates[i];od;
  indices:=Filtered([1..Length(lower.generators)],i->lower.generators[i].layer<2);
  return AFSStackExtensionByTwo(lower,leading,indices);
end);
