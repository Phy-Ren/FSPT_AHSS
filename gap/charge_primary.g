# Class-only primary charge obstruction for a certified half-integral extension.
# For an integral rho-cocycle q and w=2*omega mod 2,
# [omega cup q + Sq2(q)/2] = j([w cup (q mod 2) + Sq2(q mod 2)]),
# where j:F2 -> (Q/Z)_s sends 1 to 1/2. This coefficient map is equivariant
# for every sign s; its induced cohomology map need not be injective.
# All integral charge lattices, original bar completions, and gauges remain
# in classification.g. This helper returns only coordinates of a closed class.
BindGlobal("U1NativeChargePrimaryCoordinates",function(c,d,H,nativeCharge)
  local mode,certificate,w,q,v,co,reference,entry;
  if not IsBound(c.chargePrimaryStats) then
    c.chargePrimaryStats:=rec(nativeCalls:=0,barFallbacks:=0,comparisons:=0,
      omegaClosureChecks:=0,emptyTargetClasses:=0,phaseModeOverrides:=0);
  fi;
  mode:="native";
  if IsBound(c.chargePrimaryMode) then mode:=c.chargePrimaryMode;fi;
  if not mode in ["bar","native","compare"] then Error("Unknown charge primary mode");fi;
  if mode="bar" or (not IsBound(c.chargePrimaryMode) and IsBound(c.phaseClassMode)) then
    c.chargePrimaryStats.barFallbacks:=c.chargePrimaryStats.barFallbacks+1;
    if mode<>"bar" and IsBound(c.phaseClassMode) then
      c.chargePrimaryStats.phaseModeOverrides:=c.chargePrimaryStats.phaseModeOverrides+1;
    fi;
    return fail;
  fi;
  if not IsBound(c.backgroundClosureCertificate) then
    c.chargePrimaryStats.barFallbacks:=c.chargePrimaryStats.barFallbacks+1;return fail;
  fi;
  certificate:=c.backgroundClosureCertificate;
  if not IsRecord(certificate) or not IsBound(certificate.actions)
    or certificate.actions<>[c.s,c.rho,c.omega]
    or not IsBound(certificate.integralTwistedCoboundary)
    or certificate.integralTwistedCoboundary<>true
    or not IsBound(certificate.halfIntegralOmega)
    or certificate.halfIntegralOmega<>true then
    c.chargePrimaryStats.barFallbacks:=c.chargePrimaryStats.barFallbacks+1;return fail;
  fi;
  if not d in [2,3] then Error("Native charge primary supports spatial dimensions two and three");fi;
  if Length(nativeCharge)<>Dimension(c.R)(d) or not ForAll(nativeCharge,IsInt) then
    Error("Native charge primary requires an integer native cochain");fi;
  if nativeCharge<>[] and Dimension(c.R)(d+1)>0 and ForAny(nativeCharge*U1Differential(c,d,"Zr"),x->x<>0) then
    Error("Native charge primary requires an integrally closed charge");fi;
  if H.coefficient<>"U1s" or H.degree<>d+2 or d+2<=c.vcd
    or not IsIdenticalObj(H,U1Cohomology(c,d+2,"U1s")) then
    Error("Native charge primary has the wrong signed target cohomology");fi;
  if IsBound(c.nativeChargePrimaryOmega) then
    entry:=c.nativeChargePrimaryOmega;
    if entry.actions<>[c.s,c.rho,c.omega] or not IsIdenticalObj(entry.resolution,c.R) then
      Error("Native charge primary cache context changed");fi;
    w:=entry.cocycle;
  else
    w:=U1Native(c,2,"F2",function(g,h)
      local value;
      value:=2*c.omega(g,h);
      if not IsInt(value) then Error("Certified extension is not half integral");fi;
      return value mod 2;
    end);
    if w<>[] and Dimension(c.R)(3)>0 and ForAny(w*U1Differential(c,2,"F2"),x->x mod 2<>0) then
      Error("Doubled extension is not a native binary cocycle");fi;
    c.nativeChargePrimaryOmega:=rec(actions:=[c.s,c.rho,c.omega],resolution:=c.R,cocycle:=w);
    c.chargePrimaryStats.omegaClosureChecks:=c.chargePrimaryStats.omegaClosureChecks+1;
  fi;
  c.chargePrimaryStats.nativeCalls:=c.chargePrimaryStats.nativeCalls+1;
  # Closure is certified above. An empty target needs no diagonal evaluation.
  if H.orders=[] then
    co:=[];c.chargePrimaryStats.emptyTargetClasses:=c.chargePrimaryStats.emptyTargetClasses+1;
  else
    q:=List(nativeCharge,x->x mod 2);
    v:=List([1..Dimension(c.R)(d+2)],i->0);
    if ForAny(q,x->x<>0) then
      v:=U1NativeSq2(c,d,q);
      if ForAny(w,x->x<>0) then v:=v+U1NativeCupI(c,2,d,0,w,q);fi;
    fi;
    v:=List(v,x->(x mod 2)/2);
    co:=H.coordinates(v);
    if co=fail then Error("Native half-valued charge source is not a cocycle");fi;
  fi;
  if mode="compare" then
    reference:=U1ChargeObstructionCoordinatesCycles(c,d,H,nativeCharge);
    if reference=fail or co<>reference then Error("Native and bar charge obstruction classes disagree");fi;
    c.chargePrimaryStats.comparisons:=c.chargePrimaryStats.comparisons+1;
  fi;
  return co;
end);
