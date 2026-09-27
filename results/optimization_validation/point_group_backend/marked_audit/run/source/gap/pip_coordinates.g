# Exact unary coordinate bridges and canonical integer-layer gauge.
# Load pip_coordinate_data.g after the ordinary formulas. No target-group
# choices or classification data enter these universal local cochains.

AFSPipSignCube := function(ctx)
  return function(g,h,j) return ctx.s(g)*ctx.s(h)*ctx.s(j);end;
end;;

AFSPipPhaseReferenceShift := function(ctx,k,b,c)
  local lambda,Q,first,second,callback;
  if k=1 then
    lambda:=AFSPipCReferenceShift(ctx,1,b);
    Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=ctx.s,b:=b));
    first:=AFSCup(2,3,c,3,lambda);second:=AFSCup(3,3,lambda,4,Q);
    callback:=function(g,h,j,l)
      local bits,key;
      bits:=[ctx.s(g),ctx.s(g*h),ctx.s(g*h*j),ctx.s(g*h*j*l),
             b(g,h),b(g,h*j),b(g,h*j*l),b(g*h,j),b(g*h,j*l),b(g*h*j,l)];
      key:=Sum([1..10],i->2^(i-1)*(bits[i] mod 2));
      return AFSMod1(AFSPipUpperCoordinate[key+1]/AFSPipUpperCoordinateModulus+
                     ctx.s(g)*ctx.s(h)*ctx.s(j)*ctx.s(l)/4+
                     (first(g,h,j,l)+second(g,h,j,l))/2);
    end;
  elif k=2 then
    if b<>AFSZero then Error("The n=2s upper bridge requires the identically zero b callback");fi;
    lambda:=AFSPipSignCube(ctx);first:=AFSCup(2,3,c,3,lambda);
    callback:=function(g,h,j,l)
      return AFSMod1(-3*ctx.s(g)*ctx.s(h)*ctx.s(j)*ctx.s(l)/16+first(g,h,j,l)/2);
    end;
  else Error("Upper bridge is proved for n=s, and n=2s with b=0 only");fi;
  return AFSMemo(callback);
end;;

AFSPipIntegerGaugePhase := function(ctx,c)
  local masks;
  masks:=[5,7,13,15,21,23,25,26,27,30,69,71,74,75,77,78,137,139];
  return AFSMemo(function(g,h,j,l)
    local bits,mask,value,i,term;
    bits:=[ctx.s(g),ctx.s(g*h),ctx.s(g*h*j),ctx.s(g*h*j*l),
           c(g,h,j),c(g,h,j*l),c(g,h*j,l),c(g*h,j,l)];
    value:=0;
    for mask in masks do
      term:=1;
      for i in [1..8] do
        if QuoInt(mask,2^(i-1)) mod 2=1 then term:=term*bits[i];fi;
      od;
      value:=value+term;
    od;
    return AFSMod1(13*ctx.s(g)*ctx.s(h)*ctx.s(j)*ctx.s(l)/16+(value mod 2)/2);
  end);
end;;
