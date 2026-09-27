# Background gauge selection is performed on the full affine resolution.
# The point-group cocycle is only the physical input, never the cohomology
# space used to classify the infinite space group.
BindGlobal("AFSReduceCrystallineBackground",function(ctx)
  local original,native,H,coordinates,gauge,gn;
  if not IsBound(ctx.omega2) then ctx.omega2:=AFSZero;fi;
  if ctx.omega2=AFSZero then return;fi;
  original:=ctx.omega2;
  native:=AFSNative(ctx,2,"F2",original);
  H:=AFSCohomology(ctx,2,"F2");coordinates:=H.coordinates(native);
  if coordinates=fail then Error("physical extension input is not a cocycle");fi;
  ctx.crystallineBackground.nativeOriginalOmega2:=native;
  ctx.crystallineBackground.affineCohomologyCoordinates:=coordinates;
  ctx.crystallineBackground.gaugeReducedToZero:=false;
  if ForAll(coordinates,x->x=0) then
    gauge:=AFSSolve(ctx,2,"F2",original);
    if gauge=fail then Error("cohomologically trivial extension lacks its actual primitive");fi;
    gn:=AFSNative(ctx,1,"F2",gauge);
    if List(gn*AFSDifferential(ctx,1,"F2"),x->x mod 2)<>List(native,x->x mod 2) then
      Error("background trivialization fails the native equation");
    fi;
    ctx.originalOmega2:=original;ctx.omegaTrivialization:=gauge;ctx.omega2:=AFSZero;
    ctx.crystallineBackground.gaugeReducedToZero:=true;
    ctx.crystallineBackground.trivializingNative1:=gn;
    ctx.crystallineBackground.trivializationRecipe:="AFSSolve on the original Pin-minus pullback, including comparison homotopy";
  fi;
end);

BindGlobal("AFSBackgroundNativeOmega",function(ctx)
  if not IsBound(ctx.omega2) or ctx.omega2=AFSZero then
    return List([1..Dimension(ctx.R)(2)],i->0);
  fi;
  if not IsBound(ctx.backgroundNativeOmega) then
    ctx.backgroundNativeOmega:=AFSNative(ctx,2,"F2",ctx.omega2);
  fi;
  return ctx.backgroundNativeOmega;
end);

BindGlobal("AFSBackgroundNonzero",function(ctx)
  return IsBound(ctx.omega2) and ctx.omega2<>AFSZero;
end);

BindGlobal("AFSBackgroundNativeCup",function(ctx,r,p,a,q,b)
  if r=0 and IsBound(ctx.useBackgroundNativeCup) and ctx.useBackgroundNativeCup then
    return CallFuncList(ValueGlobal("AFSBackgroundNativeCup0"),[ctx,p,a,q,b]);
  fi;
  return AFSNativeCup(ctx,r,p,a,q,b);
end);

BindGlobal("AFSCrystallineBackgroundExport",function(ctx)
  local data,out,field,encode;
  data:=ctx.crystallineBackground;out:=rec();
  for field in ["pointOrder","identityIndex","multiplication","omegaTable",
    "signTable","construction","characteristicClass","normalizedCocycleChecked",
    "nativeOriginalOmega2","affineCohomologyCoordinates","gaugeReducedToZero",
    "trivializingNative1","trivializationRecipe"] do
    if IsBound(data.(field)) then out.(field):=data.(field);fi;
  od;
  encode:=function(x)
    if IsRat(x) then return [NumeratorRat(x),DenominatorRat(x)];fi;
    return List(x,encode);
  end;
  for field in ["pointElements","metric","orthogonalBasis","metricDiagonal","rationalSpinLifts"] do
    out.(field):=encode(data.(field));
  od;
  out.nativeDifferential1F2:=List(AFSDifferential(ctx,1,"F2"),r->List(r,x->x mod 2));
  out.nativeDifferential2F2:=List(AFSDifferential(ctx,2,"F2"),r->List(r,x->x mod 2));
  out.nativeH2Generators:=AFSCohomology(ctx,2,"F2").generators;
  out.rationalEncoding:="[numerator,denominator] for all entries of pointElements/metric/orthogonalBasis/metricDiagonal/rationalSpinLifts";
  return out;
end);
