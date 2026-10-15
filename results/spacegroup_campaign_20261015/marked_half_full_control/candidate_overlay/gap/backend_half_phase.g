# Generic half-valued phase transfer adapted from FSPT_AHSS main commit
# 0864495b90297d3e1a0747b77aae17980f6d1f3f, gap/backend_half_phase.g.
# No superconducting formula is imported. The caller must certify the domain.
# Optional transfers for cochains taking values in (1/2)Z/Z only.
# Even chain coefficients contribute integers, and both coefficient signs
# and orientation signs act trivially on this subgroup of U1_s.
BindGlobal("U1EvaluateHalfPhaseChain",function(chain,f)
  local t,value,part;
  value:=0;
  for t in chain do
    if t[1] mod 2=1 then
      part:=CallFuncList(f,t[3]);
      if not IsInt(2*part) then Error("half-phase transfer received a value outside (1/2)Z/Z");fi;
      value:=value+part;
    fi;
  od;
  return U1Mod1(value);
end);
BindGlobal("U1NativeHalfPhase",function(c,k,f)
  local n,v,i,chain,start;
  n:=Dimension(c.R)(k);v:=List([1..n],i->0);
  if f=U1Zero then return v;fi;
  start:=Runtime();
  for i in [1..n] do
    chain:=U1ChainToBar(c.bar,k,i);v[i]:=U1EvaluateHalfPhaseChain(chain,f);
    if IsBound(c.halfPhaseProgress) then
      c.halfPhaseProgress(k,i,n,Length(chain),Number(chain,t->t[1] mod 2=1),Runtime()-start);
    fi;
  od;
  return v;
end);
BindGlobal("U1NativeHalfPhaseSmith",function(c,k,f)
  local n,s,columns,w,i,chain,start;
  if k<1 then Error("Smith half-phase transfer requires degree >= 1");fi;
  n:=Dimension(c.R)(k);w:=List([1..n],i->0);
  if f=U1Zero or n=0 then return w;fi;
  s:=U1DifferentialSmith(c,k-1,"Zs");columns:=TransposedMat(s.V);start:=Runtime();
  for i in [1..n] do
    chain:=U1ChainToBarCombination(c.bar,k,columns[i]);w[i]:=U1EvaluateHalfPhaseChain(chain,f);
    if IsBound(c.halfPhaseProgress) then
      c.halfPhaseProgress(k,i,n,Length(chain),Number(chain,t->t[1] mod 2=1),Runtime()-start);
    fi;
  od;
  return List(w*s.Vi,U1Mod1);
end);

# Same canonical native solve and integral comparison-homotopy correction
# as U1SolveData; only the certified half-valued source transfer is reduced.
BindGlobal("U1SolveHalfPhaseData",function(c,k,f)
  local a,b,bf,hf,primitive;
  if k<1 then Error("half-phase solve requires degree >= 1");fi;
  if f=U1Zero then return U1SolveData(c,k,"U1s",f);fi;
  a:=U1NativeHalfPhase(c,k,f);b:=U1SolveNative(c,k,"U1s",a);
  if b=fail then return fail;fi;
  bf:=U1Bar(c,k-1,"U1s",b);hf:=U1HomotopyPullback(c.bar,"U1s",f);
  primitive:=U1Memo(function(xs...)
    return U1Mod1(CallFuncList(bf,xs)-CallFuncList(hf,xs));
  end);
  return rec(primitive:=primitive,nativePrimitive:=b,nativeObstruction:=a);
end);

# Same normalized cup_1 expression as the generic U1 cup, with short faces
# evaluated before their composed partner. q is a normalized F2 bar cochain.
# The certificate caller separately proves integral charge closure and the
# half-integral background; coefficient signs vanish only in the half phase.
BindGlobal("U1ClosedChargeSource3Lazy",function(c,q)
  if q=U1Zero then return U1Zero;fi;
  return U1Memo(function(g,h,j,l,m)
    local one,x,tail,value;
    one:=Identity(c.G);
    if one in [g,h,j,l,m] then return 0;fi;
    tail:=q(j,l,m) mod 2;value:=0;
    if tail=1 then value:=(2*c.omega(g,h)) mod 2;fi;
    if q(g,h,j) mod 2=1 then
      x:=g*h*j;if x<>one then value:=value+q(x,l,m);fi;
    fi;
    if q(h,j,l) mod 2=1 then
      x:=h*j*l;if x<>one then value:=value+q(g,x,m);fi;
    fi;
    if tail=1 then
      x:=j*l*m;if x<>one then value:=value+q(g,h,x);fi;
    fi;
    return (value mod 2)/2;
  end);
end);

# Only the exact source factory's certificate permits the half-valued path.
BindGlobal("U1SolveCertifiedChargeData",function(c,d,state)
  local source,certificate,solved,handle,entry;
  source:=CallFuncList(ValueGlobal("U1Source"),[c,d,state]);
  if IsBound(state.closedChargeSourceCertificate) then
    certificate:=state.closedChargeSourceCertificate;
    if IsRecord(certificate) and IsBound(certificate.context)
      and IsIdenticalObj(certificate.context,c)
      and IsBound(certificate.dimension) and certificate.dimension=d
      and IsBound(certificate.charge) and IsIdenticalObj(certificate.charge,state.charge)
      and IsBound(certificate.actions) and certificate.actions=[c.s,c.rho,c.omega]
      and IsBound(certificate.source) and IsIdenticalObj(certificate.source,source)
      and IsBound(certificate.halfValuedPhaseSource) and certificate.halfValuedPhaseSource=true
      and state.sheet=U1Zero then
      solved:=U1SolveHalfPhaseData(c,d+2,source);
      if d=3 and solved<>fail and IsBound(certificate.nativeCocycle)
        and IsList(certificate.nativeCocycle) and ForAll(certificate.nativeCocycle,IsInt) then
        # The context-owned registry records only this actual certified solve.
        # The public state carries an opaque handle, never a user-provided seed.
        handle:=rec();
        entry:=rec(handle:=handle,state:=state,context:=c,R:=c.R,bar:=c.bar,
          dimension:=d,actions:=[c.s,c.rho,c.omega],charge:=state.charge,
          sourceCertificate:=certificate,source:=source,phase:=solved.primitive,
          nativeCharge:=ShallowCopy(certificate.nativeCocycle),
          
          # U1Bar copies its vector immediately, just as the original bf does.
          # Caller mutation of solved.nativePrimitive cannot change either lift.
          nativePhaseBar:=U1Bar(c,d+1,"U1s",solved.nativePrimitive));
        if not IsBound(c.markedHalfChargeRegistry) then c.markedHalfChargeRegistry:=[];fi;
        Add(c.markedHalfChargeRegistry,entry);state.markedHalfChargeLift:=handle;
      fi;
      return solved;
    fi;
  fi;
  return U1SolveData(c,d+2,"U1s",source);
end);


# Exact marked-lift double in 3+1D. This does not transfer a class-only
# representative, erase the integer charge, or replace any removal gauge.
# If nu=G*b-H*O and O is half-valued, the same integral H gives 2H*O=0
# pointwise modulo one. Keep the original full U1ChargeProduct twister.
BindGlobal("U1TryMarkedHalfChargeDouble",function(c,d,a,b)
  local mode,index,entry,actions,twister,certificate;
  mode:="certified";
  if IsBound(c.markedHalfDoubleMode) then mode:=c.markedHalfDoubleMode;fi;
  if not mode in ["certified","reference"] then Error("Unknown marked half double mode");fi;
  if mode="reference" or d<>3 or not IsIdenticalObj(a,b) or a.sheet<>U1Zero then return fail;fi;
  if not IsBound(a.markedHalfChargeLift) or not IsBound(c.markedHalfChargeRegistry)
    or not IsBound(a.closedChargeSourceCertificate) then return fail;fi;
  certificate:=a.closedChargeSourceCertificate;
  if not IsRecord(certificate) or not IsBound(certificate.source)
    or not IsBound(certificate.halfValuedPhaseSource)
    or not IsBound(certificate.nativeCocycle)
    or not IsList(certificate.nativeCocycle)
    or not IsList(c.markedHalfChargeRegistry) then return fail;fi;
  index:=PositionProperty(c.markedHalfChargeRegistry,
    e->IsRecord(e) and IsBound(e.handle) and IsIdenticalObj(e.handle,a.markedHalfChargeLift));
  if index=fail then return fail;fi;
  entry:=c.markedHalfChargeRegistry[index];actions:=[c.s,c.rho,c.omega];
  if not IsIdenticalObj(entry.state,a) or not IsIdenticalObj(entry.context,c)
    or not IsIdenticalObj(entry.R,c.R) or not IsIdenticalObj(entry.bar,c.bar)
    or entry.dimension<>d or not ForAll([1..3],i->IsIdenticalObj(entry.actions[i],actions[i]))
    or not IsIdenticalObj(entry.charge,a.charge) or not IsIdenticalObj(entry.phase,a.phase)
    or not IsIdenticalObj(entry.sourceCertificate,certificate)
    or not IsIdenticalObj(entry.source,certificate.source)
    or certificate.halfValuedPhaseSource<>true
    or entry.nativeCharge<>certificate.nativeCocycle then return fail;fi;
  if not IsIdenticalObj(entry.source,CallFuncList(ValueGlobal("U1Source"),[c,d,a])) then return fail;fi;
  if not IsBound(c.markedHalfDoubleHits) then c.markedHalfDoubleHits:=0;fi;
  c.markedHalfDoubleHits:=c.markedHalfDoubleHits+1;
  twister:=U1ChargeProduct(c,d,a.charge,a.charge);
  return rec(sheet:=U1Zero,charge:=U1Add(a.charge,a.charge),
    phase:=U1Add(U1Scale(2,entry.nativePhaseBar),twister));
end);
