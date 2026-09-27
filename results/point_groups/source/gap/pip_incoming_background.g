# H^0(G,Z) incoming p+ip boundary in the delivered CA coordinate (s=0).
# Derivation: tests/derive_pip_incoming_background.py, all 1024 local closed
# omega five-simplices. Calibrate the square by the supplied R0(A=2,b=0).
# The residual half-phase freedom is exact plus omega^2/2 = 8X; hence every
# permitted choice generates the same cyclic subgroup of lower phases.

BindGlobal("AFSBackgroundIncomingState",function(ctx)
  local values,w,F,state;
  if ForAny(GeneratorsOfGroup(ctx.G),g->ctx.s(g)<>0) then
    Error("H0 integer background boundary requires a unitary group");
  fi;
  if not IsBound(ctx.omega2) then Error("background omega2 has not been installed");fi;
  w:=ctx.omega2;
  values:=[0,0,14,0,0,0,0,0,0,1,0,3,0,9,6,3,
    0,5,0,13,0,3,8,1,0,0,8,0,8,14,0,0,
    0,3,12,9,14,11,14,3,0,10,0,0,10,2,2,2,
    0,8,4,0,0,0,14,0,0,5,14,3,0,1,0,3];
  if w=AFSZero then
    return rec(a:=AFSZero,c:=AFSZero,v:=AFSZero,
      construction:="unitary-incoming-H0-zero-background",integerGauge0:=1);
  fi;
  F:=AFSMemo(function(g,h,j,k)
    local key;
    if ForAny([g,h,j,k],x->x=One(ctx.G)) then return 0;fi;
    key:=w(g,h)+2*w(g,h*j)+4*w(g,h*j*k)
        +8*w(g*h,j)+16*w(g*h,j*k)+32*w(g*h*j,k);
    return values[key+1]/16;
  end);
  state:=rec(a:=w,c:=AFSZero,v:=F,integerGauge0:=1,
    construction:="exact-CA-incoming-H0-with-calibrated-even-square",
    boundaryCertificate:="1024-closure-64-square-normalized-ambiguity-mod-8X");
  return state;
end);

BindGlobal("AFSBackgroundIncomingPowers",function(ctx)
  local X,w,dw,P,r,rr,two,four,eight,sixteen,eta;
  X:=AFSBackgroundIncomingState(ctx);w:=ctx.omega2;
  dw:=AFSCoboundary(ctx,"Z",w);
  P:=AFSMemo(function(g,h,j,k)
    return w(g,h)*w(j,k)+w(g*h*j,k)*dw(g,h,j)+w(g,h*j*k)*dw(h,j,k);
  end);
  r:=AFSMemo(function(g,h,j) return (dw(g,h,j)/2) mod 2;end);
  rr:=AFSCup(2,3,r,3,r);
  two:=rec(a:=AFSZero,c:=r,
    v:=AFSMemo(function(xs...) return AFSMod1(-CallFuncList(P,xs)/8);end),
    integerGauge0:=2,construction:="calibrated-2X-Sq1omega-minus-P-over8");
  four:=rec(a:=AFSZero,c:=AFSZero,
    v:=AFSMemo(function(xs...) return AFSMod1(-CallFuncList(P,xs)/4+CallFuncList(rr,xs)/2);end),
    integerGauge0:=4,construction:="literal-CA-square-of-2X");
  eight:=rec(a:=AFSZero,c:=AFSZero,
    v:=AFSMemo(function(xs...) return AFSMod1(-CallFuncList(P,xs)/2);end),
    integerGauge0:=8,construction:="literal-8X-omega-square-half");
  sixteen:=rec(a:=AFSZero,c:=AFSZero,v:=AFSZero,integerGauge0:=16,
    construction:="literal-16X-zero");
  eta:=AFSMemo(function(g,h,j)
    return (1-w(g,h))*w(g,h*j)*(1-w(g*h,j))/2;
  end);
  return rec(generator:=X,powers:=[X,two,four,eight,sixteen],
    integerPowers:=[1,2,4,8,16],pontryagin4:=P,
    quadruplePhaseGauge3:=eta,
    firstImage:="omega",secondImage:="Sq1(omega)",
    thirdImage:="-Pontryagin(omega)/4 modulo an explicit phase gauge",
    ambiguity:="exact half phase plus 8X; incoming cyclic subgroup unchanged");
end);
