# Exact closed-input specialization of the existing insulator charge source.
# The certificate pattern is adapted from main commit
# 0864495b90297d3e1a0747b77aae17980f6d1f3f, full_stacking.g:143-172;
# the expression below is derived from U1ChargeSource, not an SC formula.
BindGlobal("U1CertifiedClosedChargeState",function(c,d,v)
  local state,certificate,q2,w,source,binarySource,mode,reference,fast;
  if not d in [2,3] or Length(v)<>Dimension(c.R)(d) or not ForAll(v,IsInt) then
    Error("Closed charge state requires an integer native vector in degree 2 or 3");fi;
  if Dimension(c.R)(d+1)>0 and ForAny(v*U1Differential(c,d,"Zr"),x->x<>0) then
    Error("Closed charge state has nonzero integral coboundary");fi;
  # This is exactly the same integral bar pullback as a linear combination
  # of the individual native charge generators. Keep the entire integer q.
  state:=rec(sheet:=U1Zero,charge:=U1Bar(c,d,"Zr",v),phase:=U1Zero);
  mode:="certified";if IsBound(c.closedChargeSourceMode) then mode:=c.closedChargeSourceMode;fi;
  if not mode in ["certified","reference","compare"] then Error("Unknown closed charge source mode");fi;
  if mode="reference" or not IsBound(c.backgroundClosureCertificate) then return state;fi;
  certificate:=c.backgroundClosureCertificate;
  if not IsRecord(certificate) or not IsBound(certificate.actions)
    or certificate.actions<>[c.s,c.rho,c.omega]
    or not IsBound(certificate.integralTwistedCoboundary) or certificate.integralTwistedCoboundary<>true
    or not IsBound(certificate.halfIntegralOmega) or certificate.halfIntegralOmega<>true then return state;fi;
  q2:=U1BarMod2(c,d,List(v,x->x mod 2));
  if q2=U1Zero then source:=U1Zero;
  elif d=3 then source:=U1ClosedChargeSource3Lazy(c,q2);
  else
    w:=U1Memo(function(g,h) return (2*c.omega(g,h)) mod 2;end);
    binarySource:=U1Add(U1Cup(c,2,w,"F2",d,q2,"F2",0,true),
      U1Cup(c,d,q2,"F2",d,q2,"F2",d-2,true));
    source:=U1Memo(function(xs...) return (CallFuncList(binarySource,xs) mod 2)/2;end);
  fi;
  if mode="compare" then
    reference:=U1ChargeSource(c,d,state.charge);fast:=source;
    source:=U1Memo(function(xs...)
      local value;
      value:=CallFuncList(fast,xs);
      if U1Mod1(CallFuncList(reference,xs)-value)<>0 then Error("Closed charge source comparison failed");fi;
      return value;
    end);
  fi;
  state.closedChargeSourceCertificate:=rec(context:=c,dimension:=d,charge:=state.charge,
    nativeCocycle:=ShallowCopy(v),halfValuedPhaseSource:=true,actions:=[c.s,c.rho,c.omega],source:=source);
  return state;
end);
