# Complete matched-coordinate stacking and gauge transport. The cylinder
# construction propagates an integer coboundary through every upper layer.
# It uses d H + H d = identity - retraction on normalized simplicial cochains;
# no upper carry is assigned zero or inferred from a filtration order.

BindGlobal("AFSFullZero",function()
  return rec(n:=AFSZero,a:=AFSZero,c:=AFSZero,v:=AFSZero);
end);

BindGlobal("AFSFullFaceMemo",function(c,f)
  local cache;
  cache:=NewDictionary([1],true);
  return function(vertices)
    local key,value,x,g,base,origin;
    key:=[];
    base:=fail;
    # Production face functions use the local frame at their first vertex:
    # simultaneous left translation leaves all relative edges and times
    # unchanged. Arbitrary cochains used by the Stokes unit test need not have
    # this property, so the optimization requires an explicit context flag.
    if IsBound(c.fullCanonicalFaceCache) and c.fullCanonicalFaceCache then
      if IsBound(c.fullFaceTranslationIndices) then
        origin:=c.elementIndex(vertices[1][1]);
        for x in vertices do
          Add(key,c.fullFaceTranslationIndices[origin][c.elementIndex(x[1])]);
          Add(key,x[2]);
        od;
        value:=LookupDictionary(cache,key);
        if value=fail then value:=f(vertices);AddDictionary(cache,key,value);fi;
        return value;
      fi;
      base:=vertices[1][1]^-1;
    fi;
    for x in vertices do
      g:=x[1];if base<>fail then g:=base*g;fi;
      if IsBound(c.elementIndex) then Add(key,c.elementIndex(g));
      else Append(key,AFSKey([g]));fi;
      Add(key,x[2]);
    od;
    value:=LookupDictionary(cache,key);
    if value=fail then value:=f(vertices);AddDictionary(cache,key,value);fi;
    return value;
  end;
end);

BindGlobal("AFSFullDegenerate",function(vertices)
  local i;for i in [1..Length(vertices)-1] do
    if vertices[i]=vertices[i+1] then return true;fi;
  od;return false;
end);

BindGlobal("AFSFullPullBar",function(c,f)
  if f=AFSZero then return AFSZero;fi;
  return AFSFullFaceMemo(c,function(vertices)
    local xs,i;xs:=[];
    for i in [1..Length(vertices)-1] do
      Add(xs,vertices[i][1]^-1*vertices[i+1][1]);
    od;
    if Identity(c.G) in xs then return 0;fi;
    return CallFuncList(f,xs);
  end);
end);

BindGlobal("AFSFullEndpoint",function(c,f,time)
  if f=AFSZero then return AFSZero;fi;
  return AFSMemo(function(xs...)
    local vertices,g,x;
    g:=Identity(c.G);vertices:=[[g,time]];
    for x in xs do g:=g*x;Add(vertices,[g,time]);od;
    return f(vertices);
  end);
end);

BindGlobal("AFSFullFaceSum",function(c,modulus,fs)
  fs:=Filtered(fs,f->f<>AFSZero);if Length(fs)=0 then return AFSZero;fi;
  return AFSFullFaceMemo(c,function(v)
    local x;x:=Sum(fs,f->f(v));
    if modulus=1 then return AFSMod1(x);elif modulus=2 then return x mod 2;fi;
    return x;
  end);
end);

BindGlobal("AFSFullFaceD",function(c,coeff,f)
  if f=AFSZero then return AFSZero;fi;
  return AFSFullFaceMemo(c,function(vertices)
    local i,face,value,sign;
    if AFSFullDegenerate(vertices) then return 0;fi;
    value:=0;
    for i in [1..Length(vertices)] do
      face:=ShallowCopy(vertices);Remove(face,i);sign:=(-1)^(i-1);
      if i=1 and coeff in ["Zs","U1s"] then
        sign:=sign*c.sign(vertices[1][1]^-1*vertices[2][1]);
      fi;
      value:=value+sign*f(face);
    od;
    if coeff="F2" then return value mod 2;
    elif coeff="U1s" then return AFSMod1(value);fi;
    return value;
  end);
end);

BindGlobal("AFSFullPrism",function(c,coeff,f)
  if f=AFSZero then return AFSZero;fi;
  return AFSFullFaceMemo(c,function(vertices)
    local i,prism,value;
    if AFSFullDegenerate(vertices) then return 0;fi;
    value:=0;
    for i in [1..Length(vertices)] do
      if vertices[i][2]=0 then continue;fi;
      prism:=Concatenation(List(vertices{[1..i]},v->[v[1],0]),
        vertices{[i..Length(vertices)]});
      if not AFSFullDegenerate(prism) then value:=value+(-1)^(i-1)*f(prism);fi;
    od;
    if coeff="F2" then return value mod 2;
    elif coeff="U1s" then return AFSMod1(value);fi;
    return value;
  end);
end);

BindGlobal("AFSFullGaugeExtension",function(c,f)
  local pulled;
  if f=AFSZero then return AFSZero;fi;pulled:=AFSFullPullBar(c,f);
  return AFSFullFaceMemo(c,function(v)return v[1][2]*pulled(v);end);
end);

BindGlobal("AFSFullBackgroundFaces",function(c)
  return rec(s:=AFSFullPullBar(c,c.s),w:=AFSFullPullBar(c,c.omega2));
end);

BindGlobal("AFSFullSourceFace",function(c,d,stage,state)
  local bg;bg:=AFSFullBackgroundFaces(c);state:=ShallowCopy(state);
  return AFSFullFaceMemo(c,function(v)
    if AFSFullDegenerate(v) then return 0;fi;
    return AFSFullSourceSimplex(c,d,stage,v,state,bg);
  end);
end);

BindGlobal("AFSFullBarToFaces",function(c,x)
  return rec(n:=AFSFullPullBar(c,x.n),a:=AFSFullPullBar(c,x.a),
    c:=AFSFullPullBar(c,x.c),v:=AFSFullPullBar(c,x.v));
end);

BindGlobal("AFSFullClosedCFSource3",function(fermion,omega)
  if fermion=AFSZero then return AFSZero;fi;
  return AFSMemo(function(g,h,j,l,m)
    local one,value,face;
    one:=One(g);if one in [g,h,j,l,m] then return 0;fi;
    value:=0;
    if fermion(g,h,j) mod 2=1 then
      face:=g*h*j;if face<>one then value:=value+fermion(face,l,m);fi;
    fi;
    if fermion(h,j,l) mod 2=1 then
      face:=h*j*l;if face<>one then value:=value+fermion(g,face,m);fi;
    fi;
    if fermion(j,l,m) mod 2=1 then
      face:=j*l*m;if face<>one then value:=value+fermion(g,h,face);fi;
      if omega<>AFSZero then value:=value+omega(g,h);fi;
    fi;
    return (value mod 2)/2;
  end);
end);

BindGlobal("AFSFullSource",function(c,d,stage,x)
  if d=3 and stage="bosonic" and IsBound(c.fullClosedCFSource) and c.fullClosedCFSource and
    x.n=AFSZero and x.a=AFSZero and IsBound(x.closedCFSourceCertificate) and
    x.closedCFSourceCertificate.cochain=x.c then
    # The certificate is attached only to an explicitly checked native closed
    # CF cocycle and its exact comparison-map pullback. Any operation changing
    # c loses this identity guard. The complete formula on closed c is exactly
    # (c cup_1 c + omega cup c)/2; all nonclosed inputs retain the general path.
    c.fullClosedCFSourceUses:=c.fullClosedCFSourceUses+1;
    return AFSFullClosedCFSource3(x.c,c.omega2);
  fi;
  if IsBound(c.fullCertifiedZeroLowers) and c.fullCertifiedZeroLowers and d in [3,4] and
    IsBound(x.closedEvenIntegerCertificate) and c.s=AFSZero and c.omega2=AFSZero and x.a=AFSZero and
    stage in ["majorana","fermion"] then
    # For n=2h and a=w=s=0, the supplied Majorana source is zero. The
    # fermion source is zero in d3 and h cup delta(h) in d4. Integral
    # closure of n makes delta(h mod2)=0 pointwise. The certificate is
    # created only from a checked closed even native integer bar lift.
    c.fullZeroLowerCertificateUses:=c.fullZeroLowerCertificateUses+1;
    return AFSZero;
  fi;
  if d=4 and IsBound(c.fullCertifiedZeroLowers) and c.fullCertifiedZeroLowers and
    IsBound(x.binaryIntegerOmegaCertificate) and c.s=AFSZero and x.a=AFSZero and
    x.binaryIntegerOmegaCertificate.omegaFunction=c.omega2 and stage in ["majorana","fermion"] then
    # Exhaustive binary integral-cocycle identities on a simplex certify both
    # sources for n in {0,1}, omega=n pointwise, and a=s=0. The state marker
    # requires every finite-group pair to satisfy these hypotheses.
    c.fullZeroLowerCertificateUses:=c.fullZeroLowerCertificateUses+1;
    return AFSZero;
  fi;
  return AFSFullEndpoint(c,AFSFullSourceFace(c,d,stage,AFSFullBarToFaces(c,x)),0);
end);

BindGlobal("AFSFullTwister",function(c,d,stage,x,y)
  local xf,yf,bg;
  if stage="majorana" and x.n=AFSZero and y.n=AFSZero then return AFSZero;fi;
  if stage="fermion" and x.n=AFSZero and y.n=AFSZero and x.a=AFSZero and y.a=AFSZero then return AFSZero;fi;
  xf:=AFSFullBarToFaces(c,x);yf:=AFSFullBarToFaces(c,y);bg:=AFSFullBackgroundFaces(c);
  return AFSFullEndpoint(c,AFSFullFaceMemo(c,function(v)
    if AFSFullDegenerate(v) then return 0;fi;
    return AFSFullProductSimplex(c,d,stage,v,xf,yf,bg);
  end),0);
end);

BindGlobal("AFSFullProduct",function(c,d,x,y)
  local z;z:=AFSFullZero();
  # All supplied products are normalized at a zero lower input. This also
  # preserves the exact zero functions used to prune expensive evaluations.
  if x.n=AFSZero and x.a=AFSZero and x.c=AFSZero then
    z:=ShallowCopy(y);z.v:=AFSCoadd(1,[x.v,y.v]);return z;
  fi;
  if y.n=AFSZero and y.a=AFSZero and y.c=AFSZero then
    z:=ShallowCopy(x);z.v:=AFSCoadd(1,[x.v,y.v]);return z;
  fi;
  z.n:=AFSCoadd(0,[x.n,y.n]);
  z.a:=AFSCoadd(2,[x.a,y.a,AFSFullTwister(c,d,"majorana",x,y)]);
  z.c:=AFSCoadd(2,[x.c,y.c,AFSFullTwister(c,d,"fermion",x,y)]);
  z.v:=AFSCoadd(1,[x.v,y.v,AFSFullTwister(c,d,"bosonic",x,y)]);
  return z;
end);

BindGlobal("AFSFullInverse",function(c,d,x)
  local y;
  if x.n=AFSZero and x.a=AFSZero and x.c=AFSZero then
    y:=ShallowCopy(x);y.v:=AFSComul(1,-1,x.v);return y;
  fi;
  y:=AFSFullZero();y.n:=AFSComul(0,-1,x.n);
  y.a:=AFSCoadd(2,[x.a,AFSFullTwister(c,d,"majorana",x,y)]);
  y.c:=AFSCoadd(2,[x.c,AFSFullTwister(c,d,"fermion",x,y)]);
  y.v:=AFSComul(1,-1,AFSCoadd(1,[x.v,AFSFullTwister(c,d,"bosonic",x,y)]));
  return y;
end);

BindGlobal("AFSFullPower",function(c,d,x,n)
  local out;
  if not IsInt(n) then Error("stacking exponent must be integral");fi;
  if n<0 then x:=AFSFullInverse(c,d,x);n:=-n;fi;
  out:=AFSFullZero();
  while n>0 do
    if n mod 2=1 then out:=AFSFullProduct(c,d,out,x);fi;
    n:=QuoInt(n,2);if n>0 then x:=AFSFullProduct(c,d,x,x);fi;
  od;return out;
end);

# lambda, beta, gamma have degrees d-3, d-2, d-1. They need not be closed.
# An endpoint with an exact integer class is reduced with lambda solving
# d_s lambda=-n. The source transgressions supply every induced upper carry.
BindGlobal("AFSFullVacuumMajoranaGauge",function(c,beta)
  local out,bf,bg,endpoint;
  bf:=AFSFullPullBar(c,beta);bg:=AFSFullBackgroundFaces(c);
  endpoint:=function(stage)
    return AFSFullEndpoint(c,AFSFullFaceMemo(c,function(vertices)
      if AFSFullDegenerate(vertices) then return 0;fi;
      return AFSFullFormulaRequest(c,rec(dimension:=4,operation:="vacuum-majorana-gauge",stage:=stage,
        fields:=rec(beta:=AFSFullFaceVector(vertices,2,bf),
          w:=AFSFullFaceVector(vertices,2,bg.w),s:=AFSFullFaceVector(vertices,1,bg.s))));
    end),1);
  end;
  out:=AFSFullZero();out.a:=AFSCoboundary(c,"F2",beta);
  out.c:=endpoint("fermion");out.v:=endpoint("bosonic");
  out.gauge:=rec(integer:=AFSZero,majorana:=beta,fermion:=AFSZero,
    method:="compiled-exact-normalized-vacuum-Majorana-cylinder");
  c.fullVacuumMajoranaKernelUses:=c.fullVacuumMajoranaKernelUses+1;
  return out;
end);

# This is the literal full-source prism compiled after substituting the
# vacuum and a pure complex-fermion gauge parameter; no loop dictionary is used.
BindGlobal("AFSFullVacuumFermionGauge",function(c,gamma)
  local out,gf,bg;
  gf:=AFSFullPullBar(c,gamma);bg:=AFSFullBackgroundFaces(c);
  out:=AFSFullZero();out.c:=AFSCoboundary(c,"F2",gamma);
  out.v:=AFSFullEndpoint(c,AFSFullFaceMemo(c,function(vertices)
    if AFSFullDegenerate(vertices) then return 0;fi;
    return AFSFullFormulaRequest(c,rec(dimension:=4,operation:="vacuum-fermion-gauge",stage:="bosonic",
      fields:=rec(gamma:=AFSFullFaceVector(vertices,3,gf),
        w:=AFSFullFaceVector(vertices,2,bg.w),s:=AFSFullFaceVector(vertices,1,bg.s))));
  end),1);
  out.gauge:=rec(integer:=AFSZero,majorana:=AFSZero,fermion:=gamma,
    method:="compiled-exact-normalized-vacuum-complex-fermion-cylinder");
  c.fullVacuumFermionKernelUses:=c.fullVacuumFermionKernelUses+1;
  return out;
end);

# Literal non-vacuum cylinders. Source-independent phase fields are added
# outside the kernels, and every lower carry is retained.
BindGlobal("AFSFullMajoranaGaugeN0",function(c,d,x,beta)
  local out,base,bf,bg,endpoint;
  base:=AFSFullBarToFaces(c,x);bf:=AFSFullPullBar(c,beta);bg:=AFSFullBackgroundFaces(c);
  endpoint:=function(stage)
    return AFSFullEndpoint(c,AFSFullFaceMemo(c,function(vertices)
      local cf;
      if AFSFullDegenerate(vertices) then return 0;fi;
      cf:=base.c;
      # H F5(a+d(eta beta)) is structurally independent of the base c4.
      if stage="fermion" then cf:=AFSZero;fi;
      return AFSFullFormulaRequest(c,rec(dimension:=d,operation:="majorana-gauge-n0",stage:=stage,
        fields:=rec(a:=AFSFullFaceVector(vertices,d-1,base.a),c:=AFSFullFaceVector(vertices,d,cf),
          beta:=AFSFullFaceVector(vertices,d-2,bf),w:=AFSFullFaceVector(vertices,2,bg.w),
          s:=AFSFullFaceVector(vertices,1,bg.s))));
    end),1);
  end;
  out:=ShallowCopy(x);out.a:=AFSCoadd(2,[x.a,AFSCoboundary(c,"F2",beta)]);
  out.c:=AFSCoadd(2,[x.c,endpoint("fermion")]);out.v:=AFSCoadd(1,[x.v,endpoint("bosonic")]);
  out.gauge:=rec(integer:=AFSZero,majorana:=beta,fermion:=AFSZero,
    method:="compiled-exact-normalized-Majorana-cylinder-n0");
  c.fullMajoranaN0KernelUses:=c.fullMajoranaN0KernelUses+1;return out;
end);

BindGlobal("AFSFullFermionGaugeN0",function(c,d,x,gamma)
  local out,cf,gf,bg,carry;
  cf:=AFSFullPullBar(c,x.c);gf:=AFSFullPullBar(c,gamma);bg:=AFSFullBackgroundFaces(c);
  carry:=AFSFullEndpoint(c,AFSFullFaceMemo(c,function(vertices)
    if AFSFullDegenerate(vertices) then return 0;fi;
    return AFSFullFormulaRequest(c,rec(dimension:=d,operation:="fermion-gauge-n0",stage:="bosonic",
      fields:=rec(c:=AFSFullFaceVector(vertices,d,cf),gamma:=AFSFullFaceVector(vertices,d-1,gf),
        w:=AFSFullFaceVector(vertices,2,bg.w),s:=AFSFullFaceVector(vertices,1,bg.s))));
  end),1);
  out:=ShallowCopy(x);out.c:=AFSCoadd(2,[x.c,AFSCoboundary(c,"F2",gamma)]);
  out.v:=AFSCoadd(1,[x.v,carry]);
  out.gauge:=rec(integer:=AFSZero,majorana:=AFSZero,fermion:=gamma,
    method:="compiled-exact-normalized-fermion-cylinder-n0-a0");
  c.fullFermionN0KernelUses:=c.fullFermionN0KernelUses+1;return out;
end);

BindGlobal("AFSFullGauge",function(c,d,x,lambda,beta,gamma)
  local base,y,out,source;
  if lambda=AFSZero and beta=AFSZero and gamma=AFSZero then return ShallowCopy(x);fi;
  if d=4 and IsBound(c.fullVacuumMajoranaKernel) and c.fullVacuumMajoranaKernel and
    lambda=AFSZero and gamma=AFSZero and x.n=AFSZero and x.a=AFSZero and x.c=AFSZero and x.v=AFSZero then
    return AFSFullVacuumMajoranaGauge(c,beta);
  fi;
  if d=4 and IsBound(c.fullVacuumFermionKernel) and c.fullVacuumFermionKernel and
    lambda=AFSZero and beta=AFSZero and x.n=AFSZero and x.a=AFSZero and x.c=AFSZero and x.v=AFSZero then
    return AFSFullVacuumFermionGauge(c,gamma);
  fi;
  if d in [3,4] and IsBound(c.fullMajoranaN0Kernel) and c.fullMajoranaN0Kernel and
    x.n=AFSZero and lambda=AFSZero and gamma=AFSZero then
    return AFSFullMajoranaGaugeN0(c,d,x,beta);
  fi;
  if d in [3,4] and IsBound(c.fullFermionN0Kernel) and c.fullFermionN0Kernel and
    x.n=AFSZero and x.a=AFSZero and lambda=AFSZero and beta=AFSZero then
    return AFSFullFermionGaugeN0(c,d,x,gamma);
  fi;
  base:=AFSFullBarToFaces(c,x);y:=AFSFullZero();
  y.n:=AFSFullFaceSum(c,0,[base.n,AFSFullFaceD(c,"Zs",AFSFullGaugeExtension(c,lambda))]);
  source:=AFSZero;if lambda<>AFSZero then source:=AFSFullSourceFace(c,d,"majorana",y);fi;
  y.a:=AFSFullFaceSum(c,2,[base.a,AFSFullPrism(c,"F2",source),
    AFSFullFaceD(c,"F2",AFSFullGaugeExtension(c,beta))]);
  source:=AFSZero;if lambda<>AFSZero or beta<>AFSZero then source:=AFSFullSourceFace(c,d,"fermion",y);fi;
  y.c:=AFSFullFaceSum(c,2,[base.c,AFSFullPrism(c,"F2",source),
    AFSFullFaceD(c,"F2",AFSFullGaugeExtension(c,gamma))]);
  source:=AFSFullSourceFace(c,d,"bosonic",y);
  y.v:=AFSFullFaceSum(c,1,[base.v,AFSFullPrism(c,"U1s",source)]);
  out:=rec(n:=AFSFullEndpoint(c,y.n,1),a:=AFSFullEndpoint(c,y.a,1),
    c:=AFSFullEndpoint(c,y.c,1),v:=AFSFullEndpoint(c,y.v,1));
  out.gauge:=rec(integer:=lambda,majorana:=beta,fermion:=gamma,
    method:="normalized-simplicial-cylinder-transgression");
  return out;
end);

BindGlobal("AFSFullCheckFlat",function(c,d,x)
  local stage,field,degree,coeff,modulus,src,diff;
  if not AFSStackSupportZero(c,d-1,0,AFSCoboundary(c,"Zs",x.n)) then return false;fi;
  for stage in ["majorana","fermion","bosonic"] do
    if stage="majorana" then field:=x.a;degree:=d;coeff:="F2";modulus:=2;
    elif stage="fermion" then field:=x.c;degree:=d+1;coeff:="F2";modulus:=2;
    else field:=x.v;degree:=d+2;coeff:="U1s";modulus:=1;fi;
    src:=AFSFullSource(c,d,stage,x);
    diff:=AFSCoadd(modulus,[AFSCoboundary(c,coeff,field),AFSComul(modulus,-1,src)]);
    if not AFSStackSupportZero(c,degree,modulus,diff) then return false;fi;
  od;return true;
end);
