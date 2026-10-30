# Generic closed-phase class transfer adapted from main's AFSU1BarCoordinates,
# FSPT_AHSS_public commit 0864495b90297d3e1a0747b77aae17980f6d1f3f,
# gap/class_coordinates.g (no superconducting operations or runtime imports).
# This is a class-only operation. Full native cochains and comparison homotopies
# remain necessary for primitives, completed roots and their gauge witnesses.

# The checked fallback establishes exactly the native cocycle condition used
# by H.coordinates; it is not a test on every tuple of an infinite bar complex.
# Algebraic callers may supply a stronger certificate, as below for the charge
# source. Every certificate is bound to the exact context, action and function.
BindGlobal("U1NativePhaseClosureCertificate",function(c,k,H,f)
  local co;
  if H.coefficient<>"U1s" or H.degree<>k or k<=c.vcd
    or not IsIdenticalObj(H,U1Cohomology(c,k,"U1s")) then
    Error("Phase class certificate has the wrong cohomology context");fi;
  co:=H.coordinates(U1Native(c,k,"U1s",f));
  if co=fail then return fail;fi;
  return rec(context:=c,degree:=k,cochain:=f,actions:=[c.s,c.r,c.omega],
    proof:="native-cocycle-check",nativeCoordinates:=co);
end);

BindGlobal("U1ClosedBarPhaseCoordinates",function(c,k,H,f,certificate)
  local key,s,inds,cycles,j,z,terms,one,out,i,value,order,entry,co;
  if certificate=fail or not IsRecord(certificate)
    or not IsBound(certificate.context) or not IsIdenticalObj(certificate.context,c)
    or not IsBound(certificate.degree) or certificate.degree<>k
    or not IsBound(certificate.cochain) or not IsIdenticalObj(certificate.cochain,f)
    or not IsBound(certificate.actions) or certificate.actions<>[c.s,c.r,c.omega]
    or not IsBound(certificate.proof)
    or not certificate.proof in ["native-cocycle-check","closed-integral-charge-source"] then
    Error("Closed phase coordinates require a matching closure certificate");fi;
  if H.coefficient<>"U1s" or H.degree<>k or k<=c.vcd
    or not IsIdenticalObj(H,U1Cohomology(c,k,"U1s")) then
    Error("Closed phase coordinates have the wrong cohomology context");fi;
  if not IsBound(c.phaseClassCycles) then c.phaseClassCycles:=rec();fi;
  key:=Concatenation("U1s",String(k));
  if IsBound(c.phaseClassCycles.(key)) then
    entry:=c.phaseClassCycles.(key);
    if not IsIdenticalObj(entry.action,c.s) or not IsIdenticalObj(entry.cohomology,H)
      or not IsIdenticalObj(entry.resolution,c.R) then
      Error("Closed phase cycle cache context changed");fi;
    cycles:=entry.cycles;
  else
    cycles:=[];
    if H.orders<>[] then
      s:=H.smith;inds:=Filtered([1..s.rank],i->AbsInt(s.diag[i])>1);
      if List(inds,i->AbsInt(s.diag[i]))<>H.orders then Error("Phase Smith order mismatch");fi;
      one:=Identity(c.G);
      for j in inds do
        z:=List(s.Ui,row->SignInt(s.diag[j])*row[j]);
        if ForAny(U1Differential(c,k-1,"Zs")*z,x->x<>0) then
          Error("Smith dual vector is not an integral twisted cycle");fi;
        # Combine the group-ring boundary before expanding its bar image.
        terms:=List(U1ChainToBarCombination(c.bar,k,z),
          t->[t[1]*U1CoefficientAction(c,"U1s",t[2]),one,t[3]]);
        Add(cycles,U1CombineChain(terms,true));
      od;
    fi;
    c.phaseClassCycles.(key):=rec(cycles:=cycles,action:=c.s,cohomology:=H,resolution:=c.R);
  fi;
  out:=[];
  for i in [1..Length(cycles)] do
    value:=0;order:=H.orders[i];
    for terms in cycles[i] do value:=value+terms[1]*CallFuncList(f,terms[3]);od;
    value:=order*value;
    if not IsInt(value) then Error("Closed phase has a nonintegral torsion period");fi;
    Add(out,value mod order);
  od;
  if certificate.proof="native-cocycle-check" and out<>certificate.nativeCoordinates then
    Error("Closed phase cycle/native coordinate disagreement");fi;
  if IsBound(c.phaseClassMode) and c.phaseClassMode="compare" then
    co:=H.coordinates(U1Native(c,k,"U1s",f));
    if co=fail or co<>out then Error("Closed phase comparison failed");fi;
  fi;
  return out;
end);

# q is constructed here from its actual integer native vector, not accepted as
# an arbitrary callback. The chain-map identity gives delta_r q=0. A validated
# background has integral delta_(r+s) omega. Consequently omega cup q and
# Sq2(q mod 2)/2 have integral signed coboundaries, proving closure modulo one.
BindGlobal("U1ChargeObstructionCoordinatesCycles",function(c,d,H,nativeCharge)
  local q,f,certificate,valid;
  if H.coefficient<>"U1s" or H.degree<>d+2 or d+2<=c.vcd
    or not IsIdenticalObj(H,U1Cohomology(c,d+2,"U1s")) then
    Error("Charge obstruction has the wrong cohomology context");fi;
  if Length(nativeCharge)<>Dimension(c.R)(d) or not ForAll(nativeCharge,IsInt) then
    Error("Charge obstruction requires an integer native cochain");fi;
  if Dimension(c.R)(d+1)>0 and ForAny(nativeCharge*U1Differential(c,d,"Zr"),x->x<>0) then
    Error("Charge obstruction requires a closed integer native cochain");fi;
  q:=U1Bar(c,d,"Zr",nativeCharge);f:=U1ChargeSource(c,d,q);
  if IsBound(c.phaseClassMode) and not c.phaseClassMode in ["cycles","native","compare"] then
    Error("Unknown phase class evaluation mode");fi;
  if IsBound(c.phaseClassMode) and c.phaseClassMode="native" then
    return H.coordinates(U1Native(c,d+2,"U1s",f));fi;
  valid:=IsBound(c.backgroundClosureCertificate)
    and c.backgroundClosureCertificate.actions=[c.s,c.r,c.omega]
    and c.backgroundClosureCertificate.integralTwistedCoboundary=true;
  if valid then
    certificate:=rec(context:=c,degree:=d+2,cochain:=f,actions:=[c.s,c.r,c.omega],
      proof:="closed-integral-charge-source");
  else
    certificate:=U1NativePhaseClosureCertificate(c,d+2,H,f);
    if certificate=fail then return fail;fi;
  fi;
  return U1ClosedBarPhaseCoordinates(c,d+2,H,f,certificate);
end);

# Optional generic native primary operations may provide a class directly.
# Their eligibility/compare checks live in charge_primary.g; fail preserves
# the exact signed Smith-cycle or full-native fallback above.
BindGlobal("U1ChargeObstructionCoordinates",function(c,d,H,nativeCharge)
  local co;
  if IsBoundGlobal("U1NativeChargePrimaryCoordinates") then
    co:=CallFuncList(ValueGlobal("U1NativeChargePrimaryCoordinates"),[c,d,H,nativeCharge]);
    if co<>fail then return co;fi;
  fi;
  return U1ChargeObstructionCoordinatesCycles(c,d,H,nativeCharge);
end);
