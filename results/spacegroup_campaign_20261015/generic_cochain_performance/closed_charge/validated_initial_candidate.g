# Isolated exact source specialization; no production file is imported from main.
BindGlobal("U1CertifiedClosedChargeState",function(c,d,v)
  local state,certificate,q2,w,source,binarySource;
  if not d in [2,3] or Length(v)<>Dimension(c.R)(d) or not ForAll(v,IsInt) then
    Error("Closed charge state requires an integer native vector in degree 2 or 3");fi;
  if Dimension(c.R)(d+1)>0 and ForAny(v*U1Differential(c,d,"Zr"),x->x<>0) then
    Error("Closed charge state has nonzero integral coboundary");fi;
  state:=rec(sheet:=U1Zero,charge:=U1Bar(c,d,"Zr",v),phase:=U1Zero);
  if not IsBound(c.backgroundClosureCertificate) then return state;fi;
  certificate:=c.backgroundClosureCertificate;
  if certificate.actions<>[c.s,c.rho,c.omega] or not certificate.integralTwistedCoboundary
    or not IsBound(certificate.halfIntegralOmega) or not certificate.halfIntegralOmega then return state;fi;
  q2:=U1Bar(c,d,"F2",List(v,x->x mod 2));
  if q2=U1Zero then source:=U1Zero;
  else
    w:=U1Memo(function(g,h) return (2*c.omega(g,h)) mod 2;end);
    binarySource:=U1Add(U1Cup(c,2,w,"F2",d,q2,"F2",0,true),
      U1Cup(c,d,q2,"F2",d,q2,"F2",d-2,true));
    source:=U1Memo(function(xs...) return (CallFuncList(binarySource,xs) mod 2)/2;end);
  fi;
  state.closedChargeSourceCertificate:=rec(context:=c,dimension:=d,charge:=state.charge,
    nativeCocycle:=ShallowCopy(v),actions:=[c.s,c.rho,c.omega],source:=source);
  return state;
end);
