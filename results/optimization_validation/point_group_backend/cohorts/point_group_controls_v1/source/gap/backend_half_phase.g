# Optional transfers for cochains taking values in (1/2)Z/Z only.
# Even chain coefficients contribute integers, and both coefficient signs
# and orientation signs act trivially on this subgroup of U1_s.
BindGlobal("AFSEvaluateHalfPhaseChain",function(chain,f)
  local t,value,part;
  value:=0;
  for t in chain do
    if t[1] mod 2=1 then
      part:=CallFuncList(f,t[3]);
      if not IsInt(2*part) then Error("half-phase transfer received a value outside (1/2)Z/Z");fi;
      value:=value+part;
    fi;
  od;
  return AFSMod1(value);
end);
BindGlobal("AFSNativeHalfPhase",function(c,k,f)
  local n,v,i,chain,start;
  n:=Dimension(c.R)(k);v:=List([1..n],i->0);
  if f=AFSZero then return v;fi;
  start:=Runtime();
  for i in [1..n] do
    chain:=AFSChainToBar(c.bar,k,i);v[i]:=AFSEvaluateHalfPhaseChain(chain,f);
    if IsBound(c.halfPhaseProgress) then
      c.halfPhaseProgress(k,i,n,Length(chain),Number(chain,t->t[1] mod 2=1),Runtime()-start);
    fi;
  od;
  return v;
end);
BindGlobal("AFSNativeHalfPhaseSmith",function(c,k,f)
  local n,s,columns,w,i,chain,start;
  if k<1 then Error("Smith half-phase transfer requires degree >= 1");fi;
  n:=Dimension(c.R)(k);w:=List([1..n],i->0);
  if f=AFSZero or n=0 then return w;fi;
  s:=AFSDifferentialSmith(c,k-1,"Zs");columns:=TransposedMat(s.V);start:=Runtime();
  for i in [1..n] do
    chain:=AFSChainToBarCombination(c.bar,k,columns[i]);w[i]:=AFSEvaluateHalfPhaseChain(chain,f);
    if IsBound(c.halfPhaseProgress) then
      c.halfPhaseProgress(k,i,n,Length(chain),Number(chain,t->t[1] mod 2=1),Runtime()-start);
    fi;
  od;
  return List(w*s.Vi,AFSMod1);
end);

# Same canonical native solve and integral comparison-homotopy correction
# as AFSSolveData; only the certified half-valued source transfer is reduced.
BindGlobal("AFSSolveHalfPhaseData",function(c,k,f)
  local a,b,bf,hf,primitive;
  if k<1 then Error("half-phase solve requires degree >= 1");fi;
  a:=AFSNativeHalfPhase(c,k,f);b:=AFSSolveNative(c,k,"U1s",a);
  if b=fail then return fail;fi;
  bf:=AFSBar(c,k-1,"U1s",b);hf:=AFSHomotopyPullback(c.bar,"U1s",f);
  primitive:=AFSMemo(function(xs...)
    return AFSMod1(CallFuncList(bf,xs)-CallFuncList(hf,xs));
  end);
  return rec(primitive:=primitive,nativePrimitive:=b,nativeObstruction:=a);
end);
