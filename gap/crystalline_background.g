# Exact crystalline spinless background: omega_eff = w2(V) + w1(V)^2.
# A finite point group is used only to construct the pulled-back background;
# the cohomology and classification group remain the full affine group.
# No SptSet code, floating arithmetic or external answer table is used.

BindGlobal("AFSPinMinusPointGroup",function(P)
  local elements,n,identity,index,metric,R,S,basis,v,u,i,j,k,norms,Q,
    bits,cliffordProduct,even,lifts,rows,row,e,image,b,q,space,first,
    reverse,norm,product,multiplication,omega,lambda,signs,data;
  elements:=Elements(P);n:=Length(elements);identity:=Position(elements,One(P));
  if not ForAll(elements,R->DimensionsMat(R)=[3,3] and
      ForAll(R,row->ForAll(row,IsRat)) and AbsInt(DeterminantMat(R))=1) then
    Error("Pin-minus background requires exact rational 3D point matrices");
  fi;
  index:=R->Position(elements,R);
  # Column-vector convention: R^T metric R = metric for every R in P.
  metric:=Sum(elements,R->TransposedMat(R)*R);
  for R in elements do
    if TransposedMat(R)*metric*R<>metric then Error("invariant metric failed");fi;
  od;
  # Rational orthogonal basis, with positive diagonal metric norms.
  basis:=[];norms:=[];
  for i in [1..3] do
    v:=IdentityMat(3)[i];
    for j in [1..Length(basis)] do
      u:=basis[j];v:=v-((v*metric)*u)/norms[j]*u;
    od;
    Add(basis,v);Add(norms,(v*metric)*v);
    if norms[i]<=0 then Error("point metric is not positive definite");fi;
  od;
  S:=TransposedMat(basis);
  if TransposedMat(S)*metric*S<>DiagonalMat(norms) then
    Error("rational orthogonalization failed");
  fi;
  # Cl(0,3): e_i^2=-norms[i]. Coefficients are exact rational numbers.
  # A blade is indexed by its three-bit mask. Positive normalization factors
  # are unnecessary: the sign of a proportionality scalar is already exact.
  bits:=List([0..7],a->List([0..2],i->QuoInt(a,2^i) mod 2));
  cliffordProduct:=function(a,b)
    local result,x,y,t,swaps,factor,mask,ii,jj;
    result:=List([1..8],i->0);
    for x in [0..7] do
      if a[x+1]=0 then continue;fi;
      for y in [0..7] do
        if b[y+1]=0 then continue;fi;
        swaps:=0;factor:=a[x+1]*b[y+1];mask:=0;
        for ii in [1..3] do
          for jj in [1..ii-1] do swaps:=swaps+bits[x+1][ii]*bits[y+1][jj];od;
          if bits[x+1][ii]=1 and bits[y+1][ii]=1 then factor:=-factor*norms[ii];fi;
          if bits[x+1][ii]<>bits[y+1][ii] then mask:=mask+2^(ii-1);fi;
        od;
        result[mask+1]:=result[mask+1]+(-1)^swaps*factor;
      od;
    od;
    return result;
  end;
  # J(R)=det(R)R is an oriented 3D representation. Its spin extension is
  # w2(J)=w2(V)+w1(V)^2. Solve q e_i = J(R)(e_i) q in the even algebra.
  even:=[0,3,5,6];lifts:=[];signs:=[];
  for R in elements do
    Q:=Inverse(S)*(DeterminantMat(R)*R)*S;
    if DeterminantMat(Q)<>1 or TransposedMat(Q)*DiagonalMat(norms)*Q<>DiagonalMat(norms) then
      Error("orientation-twisted matrix is not special orthogonal");
    fi;
    rows:=[];
    for b in even do
      q:=List([1..8],i->0);q[b+1]:=1;row:=[];
      for i in [1..3] do
        e:=List([1..8],j->0);e[2^(i-1)+1]:=1;
        image:=List([1..8],j->0);
        for j in [1..3] do image[2^(j-1)+1]:=Q[j][i];od;
        Append(row,cliffordProduct(q,e)-cliffordProduct(image,q));
      od;
      Add(rows,row);
    od;
    space:=NullspaceMat(rows);
    if Length(space)<>1 then Error("spin lift has non-scalar ambiguity");fi;
    v:=space[1];first:=PositionProperty(v,x->x<>0);v:=v/v[first];
    q:=List([1..8],i->0);
    for i in [1..4] do q[even[i]+1]:=v[i];od;
    reverse:=ShallowCopy(q);for i in [3,5,6] do reverse[i+1]:=-reverse[i+1];od;
    norm:=cliffordProduct(reverse,q);
    if norm[1]<=0 or ForAny(norm{[2..8]},x->x<>0) then Error("invalid positive spin norm");fi;
    Add(lifts,q);Add(signs,(1-DeterminantMat(R))/2);
  od;
  if lifts[identity]<>[1,0,0,0,0,0,0,0] then Error("spin section is not normalized");fi;
  multiplication:=List(elements,R->List(elements,S->index(R*S)));
  omega:=List([1..n],i->List([1..n],j->0));
  for i in [1..n] do
    for j in [1..n] do
      k:=multiplication[i][j];product:=cliffordProduct(lifts[i],lifts[j]);
      first:=PositionProperty(lifts[k],x->x<>0);lambda:=product[first]/lifts[k][first];
      if lambda=0 or product<>lambda*lifts[k] then Error("spin product is not scalar");fi;
      if lambda<0 then omega[i][j]:=1;fi;
    od;
  od;
  for i in [1..n] do
    if omega[identity][i]<>0 or omega[i][identity]<>0 then Error("omega is not normalized");fi;
    for j in [1..n] do
      for k in [1..n] do
        if (omega[j][k]+omega[multiplication[i][j]][k]
            +omega[i][multiplication[j][k]]+omega[i][j]) mod 2<>0 then
          Error("Pin-minus cocycle identity failed");
        fi;
      od;
    od;
  od;
  data:=rec(pointGroup:=P,pointElements:=elements,pointOrder:=n,
    identityIndex:=identity,multiplication:=multiplication,omegaTable:=omega,
    signTable:=signs,metric:=metric,orthogonalBasis:=S,metricDiagonal:=norms,
    rationalSpinLifts:=lifts,
    construction:="exact-rational-spin-lift-of-det-times-point-representation",
    characteristicClass:="w2(V)+w1(V)^2",normalizedCocycleChecked:=true);
  data.index:=index;
  data.omega2:=function(g,h) return omega[index(g)][index(h)];end;
  return data;
end);

BindGlobal("AFSInstallCrystallineBackground",function(ctx)
  local pointMap,P,data,generators,images,projection,pointIndex,g;
  if IsBound(ctx.crystallineBackground) then return ctx.crystallineBackground;fi;
  if not IsBound(ctx.affine) or not IsBound(ctx.iso) then
    Error("crystalline background needs the actual affine group and Pcp isomorphism");
  fi;
  pointMap:=PointHomomorphism(ctx.affine);P:=Image(pointMap);
  data:=AFSPinMinusPointGroup(P);
  generators:=GeneratorsOfGroup(ctx.G);
  images:=List(generators,g->Image(pointMap,PreImageElm(ctx.iso,g)));
  # This is the known composition pointMap o inverse(iso), specified on
  # generators so future evaluations do not reconstruct affine matrices.
  projection:=GroupHomomorphismByImagesNC(ctx.G,P,generators,images);
  if projection=fail then Error("Pcp point projection construction failed");fi;
  pointIndex:=AFSMemo(g->data.index(Image(projection,g)));
  for g in generators do
    if data.signTable[pointIndex(g)]<>ctx.s(g) then Error("orientation character mismatch");fi;
  od;
  data.projection:=projection;data.pointIndex:=pointIndex;
  ctx.omega2:=function(g,h) return data.omegaTable[pointIndex(g)][pointIndex(h)];end;
  ctx.crystallineBackground:=data;
  return data;
end);

BindGlobal("AFSCrystallineOmegaNative",function(ctx)
  local data;
  data:=AFSInstallCrystallineBackground(ctx);
  if not IsBound(data.nativeOmega2) then
    data.nativeOmega2:=AFSNative(ctx,2,"F2",ctx.omega2);
    if ForAny(data.nativeOmega2*AFSDifferential(ctx,2,"F2"),x->x mod 2<>0) then
      Error("pulled-back native omega is not a cocycle");
    fi;
  fi;
  return data.nativeOmega2;
end);
