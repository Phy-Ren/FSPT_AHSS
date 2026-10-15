# Generic exact resolution infrastructure adapted from FSPT_AHSS main.
# No superconducting operations are loaded.
# AllFSPT independent native cochain backend.
# Matrices act on row cochains on the right. Exact integers/rationals only.
# HAP supplies only the free resolution; cochain algebra and comparisons are local.
LoadPackage("HAP");;

BindGlobal("U1Key",function(xs)
  local k,x;
  k:=[];
  for x in xs do
    if IsPcpElementRep(x) then Append(k,x!.exponents);
    else return xs; fi;
  od;
  return k;
end);
BindGlobal("U1BarBoundary",function(gid,xs)
  local n,out,i,t;
  n:=Length(xs); out:=[];
  if n=0 then return out; fi;
  Add(out,Concatenation([1,xs[1]],xs{[2..n]}));
  for i in [1..n-1] do
    t:=ShallowCopy(xs); t[i]:=t[i]*t[i+1]; Remove(t,i+1);
    Add(out,Concatenation([(-1)^i,gid],t));
  od;
  Add(out,Concatenation([(-1)^n,gid],xs{[1..n-1]}));
  return out;
end);
BindGlobal("U1Memo",function(f)
  local cache;
  cache:=NewDictionary([1],true);
  return function(xs...)
    local k,v;
    k:=U1Key(xs); v:=LookupDictionary(cache,k);
    if v=fail then v:=CallFuncList(f,xs); AddDictionary(cache,k,v); fi;
    return v;
  end;
end);
BindGlobal("U1Zero",function(xs...) return 0; end);
BindGlobal("U1Floor",function(x) local y; y:=Int(x); if y>x then return y-1; fi; return y; end);
BindGlobal("U1Mod1",function(x) return x-U1Floor(x); end);

if not IsBound(U1_ROOT) then U1_ROOT:="."; fi;
if not IsBound(U1_USE_KOSZUL) then U1_USE_KOSZUL:=false; fi;
Read(Concatenation(U1_ROOT,"/gap/backend_resolution.g"));
Read(Concatenation(U1_ROOT,"/gap/backend_bar.g"));

BindGlobal("U1CoefficientAction",function(c,coeff,g)
  if coeff="Zs" or coeff="U1s" then return (-1)^c.s(g); fi;
  if coeff="Zr" then return (-1)^c.rho(g); fi;
  if coeff="Zt" then return (-1)^(c.s(g)+c.rho(g)); fi;
  if coeff="Z" or coeff="F2" then return 1; fi;
  Error("Unknown coefficient system: ",coeff);
end);

BindGlobal("U1Differential",function(c,k,coeff)
  local key,m,n,D,j,w,sgn;
  key:=Concatenation(coeff,String(k));
  if IsBound(c.differentialCache.(key)) then return c.differentialCache.(key); fi;
  m:=Dimension(c.R)(k); n:=Dimension(c.R)(k+1); D:=NullMat(m,n);
  for j in [1..n] do
    for w in BoundaryMap(c.R)(k+1,j) do
      sgn:=SignInt(w[1]);
      sgn:=sgn*U1CoefficientAction(c,coeff,c.R!.elts[w[2]]);
      D[AbsInt(w[1])][j]:=D[AbsInt(w[1])][j]+sgn;
    od;
  od;
  if coeff="F2" then D:=List(D,row->List(row,x->x mod 2)); fi;
  c.differentialCache.(key):=D; return D;
end);

BindGlobal("U1Smith",function(M,n,m)
  local s,d,r,i;
  if n=0 or m=0 then
    return rec(U:=IdentityMat(n),V:=IdentityMat(m),Ui:=IdentityMat(n),
      Vi:=IdentityMat(m),D:=NullMat(n,m),rank:=0,diag:=[]);
  fi;
  s:=SmithNormalFormIntegerMatTransforms(M); d:=[]; r:=0;
  for i in [1..Minimum(n,m)] do
    Add(d,s.normal[i][i]); if s.normal[i][i]<>0 then r:=r+1; fi;
  od;
  return rec(U:=s.rowtrans,V:=s.coltrans,Ui:=Inverse(s.rowtrans),
    Vi:=Inverse(s.coltrans),D:=s.normal,rank:=r,diag:=d);
end);
DeclareGlobalFunction("U1SmithUnits");
BindGlobal("U1DifferentialSmith",function(c,k,coeff)
  local key,D,s;
  key:=Concatenation(coeff,String(k));
  if IsBound(c.smithCache.(key)) then return c.smithCache.(key); fi;
  D:=U1Differential(c,k,coeff);
  if Minimum(Dimension(c.R)(k),Dimension(c.R)(k+1))>=32 then
    s:=U1SmithUnits(D,Dimension(c.R)(k),Dimension(c.R)(k+1));
  else s:=U1Smith(D,Dimension(c.R)(k),Dimension(c.R)(k+1)); fi;
  c.smithCache.(key):=s; return s;
end);

# An echelon row span with exact F2 reduction and retained quotient coordinates.
BindGlobal("U1Span",function(n) return rec(n:=n,rows:=[],pivots:=[]); end);
BindGlobal("U1Reduce",function(sp,v)
  local w,co,i,p;
  w:=List(v,x->x mod 2); co:=List(sp.rows,x->0);
  for i in [1..Length(sp.rows)] do
    p:=sp.pivots[i];
    if w[p]=1 then
      w:=List([1..sp.n],j->(w[j]+sp.rows[i][j]) mod 2); co[i]:=1;
    fi;
  od;
  return rec(remainder:=w,coordinates:=co);
end);
BindGlobal("U1Insert",function(sp,v)
  local r,p;
  r:=U1Reduce(sp,v).remainder; p:=Position(r,1);
  if p=fail then return false; fi;
  Add(sp.rows,r); Add(sp.pivots,p); return true;
end);

BindGlobal("U1Cohomology",function(c,k,coeff)
  local key,H,D,B,Z,sp,nb,z,g,n,m,s,inds,K,Ki,rels,t,a,orders,reps,i,U;
  key:=Concatenation(coeff,String(k));
  if IsBound(c.cohomologyCache.(key)) then return c.cohomologyCache.(key); fi;
  n:=Dimension(c.R)(k);
  if n=0 then
    H:=rec(degree:=k,coefficient:=coeff,generators:=[],orders:=[]);
    H.coordinates:=function(v) if v=[] then return []; else return fail; fi; end;
    c.cohomologyCache.(key):=H; return H;
  fi;
  if coeff="F2" then
    D:=U1Differential(c,k,"F2");
    if Dimension(c.R)(k+1)=0 then Z:=IdentityMat(n);
    else Z:=List(NullspaceMat(List(D,row->List(row,x->x*One(GF(2))))),
      row->List(row,IntFFE)); fi;
    sp:=U1Span(n);
    if k>0 then for z in U1Differential(c,k-1,"F2") do U1Insert(sp,z); od; fi;
    nb:=Length(sp.rows); reps:=[];
    for z in Z do
      if U1Insert(sp,z) then Add(reps,ShallowCopy(sp.rows[Length(sp.rows)])); fi;
    od;
    H:=rec(degree:=k,coefficient:=coeff,generators:=reps,orders:=List(reps,x->2),
      boundaries:=sp.rows{[1..nb]},span:=sp);
    H.coordinates:=function(v)
      local r;
      r:=U1Reduce(sp,v);
      if ForAny(r.remainder,x->x<>0) then return fail; fi;
      return r.coordinates{[nb+1..Length(sp.rows)]};
    end;
  elif coeff="U1s" then
    if k<=c.vcd then Error("U1 cohomology requires degree above virtual cohomological dimension"); fi;
    s:=U1DifferentialSmith(c,k,"Zs");
    inds:=Filtered([1..s.rank],i->AbsInt(s.diag[i])>1);
    H:=rec(degree:=k,coefficient:=coeff,
      generators:=List(inds,i->List(s.U[i]/s.diag[i],U1Mod1)),
      orders:=List(inds,i->AbsInt(s.diag[i])),smith:=s);
    D:=U1Differential(c,k,"Zs");
    H.coordinates:=function(v)
      local b,co,j;
      if Dimension(c.R)(k+1)=0 then b:=[]; else b:=v*D; fi;
      if not ForAll(b,IsInt) then return fail; fi;
      co:=b*s.V;
      return List(inds,j->co[j] mod AbsInt(s.diag[j]));
    end;
  else
    s:=U1DifferentialSmith(c,k,coeff);
    inds:=[s.rank+1..n]; K:=s.U{inds};
    if Length(inds)=0 then
      H:=rec(degree:=k,coefficient:=coeff,generators:=[],orders:=[]);
      H.coordinates:=function(v) if ForAll(v,x->x=0) then return []; else return fail; fi; end;
    else
      if k=0 then rels:=[];
      else
        B:=U1Differential(c,k-1,coeff)*s.Ui;
        rels:=List(B,row->row{inds});
      fi;
      t:=U1Smith(rels,Length(rels),Length(inds));
      a:=Filtered([1..Length(inds)],i->i>t.rank or AbsInt(t.diag[i])>1);
      reps:=List(a,i->t.Vi[i]*K);
      orders:=List(a,function(i) if i>t.rank then return 0; else return AbsInt(t.diag[i]); fi; end);
      H:=rec(degree:=k,coefficient:=coeff,generators:=reps,orders:=orders,
        kernel:=K,relations:=rels,smith:=t);
      H.coordinates:=function(v)
        local vv,j;
        vv:=v*s.Ui;
        if ForAny(vv{[1..s.rank]},x->x<>0) then return fail; fi;
        vv:=vv{inds}*t.V;
        return List([1..Length(a)],function(j)
          if orders[j]=0 then return vv[a[j]]; else return vv[a[j]] mod orders[j]; fi;
        end);
      end;
    fi;
  fi;
  c.cohomologyCache.(key):=H; return H;
end);

BindGlobal("U1Bar",function(c,k,coeff,v)
  local vals;
  vals:=ShallowCopy(v);
  if coeff="U1s" then vals:=List(vals,U1Mod1);
  elif coeff="F2" then vals:=List(vals,x->x mod 2); fi;
  if ForAll(vals,x->x=0) then return U1Zero; fi;
  if coeff="F2" and IsBoundGlobal("U1BarMod2") and
     IsBoundGlobal("U1_USE_MOD2_BAR") and ValueGlobal("U1_USE_MOD2_BAR")=true then
    return CallFuncList(ValueGlobal("U1BarMod2"),[c,k,vals]);
  fi;
  return U1Memo(function(xs...)
    local w,z,ans,sgn;
    if Length(xs)<>k then Error("bar cochain arity mismatch"); fi;
    w:=U1ChainFromBar(c.bar,xs); ans:=0;
    for z in w do
      sgn:=1;
      sgn:=U1CoefficientAction(c,coeff,z[3]);
      ans:=ans+z[1]*sgn*vals[z[2]];
    od;
    if coeff="F2" then return ans mod 2;
    elif coeff="U1s" then return U1Mod1(ans); else return ans; fi;
  end);
end);
BindGlobal("U1Native",function(c,k,coeff,f)
  local v,i,w,t,x,sgn;
  v:=List([1..Dimension(c.R)(k)],i->0);
  if f=U1Zero then return v; fi;
  for i in [1..Length(v)] do
    w:=U1ChainToBar(c.bar,k,i);
    for t in w do
      if coeff="F2" and IsBound(c.f2ParityFilter) and c.f2ParityFilter then
        c.f2ParityStats.nativeTerms:=c.f2ParityStats.nativeTerms+1;
        if t[1] mod 2=0 then
          c.f2ParityStats.nativeEvenTerms:=c.f2ParityStats.nativeEvenTerms+1;continue;
        fi;
        c.f2ParityStats.nativeSourceCalls:=c.f2ParityStats.nativeSourceCalls+1;
        v[i]:=(v[i]+CallFuncList(f,t[3])) mod 2;
      else
        sgn:=1;
        sgn:=U1CoefficientAction(c,coeff,t[2]);
        v[i]:=v[i]+t[1]*sgn*CallFuncList(f,t[3]);
      fi;
    od;
  od;
  if coeff="F2" then return List(v,x->x mod 2); fi;
  if coeff="U1s" then return List(v,U1Mod1); fi;
  return v;
end);
BindGlobal("U1Coboundary",function(c,coeff,f)
  # Preserve the literal zero representative, so later zero-sheet fast paths
  # remain available. No nonzero exact or cohomologically zero input is removed.
  if f=U1Zero then return U1Zero;fi;
  return U1Memo(function(xs...)
    local w,t,val,sgn;
    w:=U1BarBoundary(Identity(c.G),xs); val:=0;
    for t in w do
      sgn:=1;
      sgn:=U1CoefficientAction(c,coeff,t[2]);
      val:=val+t[1]*sgn*CallFuncList(f,t{[3..Length(t)]});
    od;
    if coeff="F2" then return val mod 2;
    elif coeff="U1s" then return U1Mod1(val); else return val; fi;
  end);
end);

# Factor an F2 coboundary once and retain explicit preimages of row pivots.
BindGlobal("U1F2SolveFactor",function(D,n)
  local sp,witnesses,i,row,w,j,p;
  sp:=U1Span(n); witnesses:=[];
  for i in [1..Length(D)] do
    row:=List(D[i],x->x mod 2); w:=List(D,x->0); w[i]:=1;
    for j in [1..Length(sp.rows)] do
      p:=sp.pivots[j];
      if row[p]=1 then
        row:=List([1..n],k->(row[k]+sp.rows[j][k]) mod 2);
        w:=List([1..Length(D)],k->(w[k]+witnesses[j][k]) mod 2);
      fi;
    od;
    p:=Position(row,1);
    if p<>fail then Add(sp.rows,row); Add(sp.pivots,p); Add(witnesses,w); fi;
  od;
  return rec(span:=sp,witnesses:=witnesses,sourceDimension:=Length(D));
end);
BindGlobal("U1F2SolveFactored",function(s,v)
  local r,w,i;
  r:=U1Reduce(s.span,v);
  if ForAny(r.remainder,x->x<>0) then return fail; fi;
  w:=List([1..s.sourceDimension],i->0);
  for i in [1..Length(r.coordinates)] do
    if r.coordinates[i]=1 then
      w:=List([1..Length(w)],j->(w[j]+s.witnesses[i][j]) mod 2);
    fi;
  od;
  return w;
end);

BindGlobal("U1SolveNative",function(c,k,coeff,v)
  local D,s,w,y,i,b;
  if k<1 then return fail; fi;
  D:=U1Differential(c,k-1,coeff);
  if v=[] then return List([1..Dimension(c.R)(k-1)],i->0); fi;
  if coeff="F2" then
    if not IsBound(c.f2SolveCache.(String(k))) then
      c.f2SolveCache.(String(k)):=U1F2SolveFactor(D,Length(v));
    fi;
    return U1F2SolveFactored(c.f2SolveCache.(String(k)),v);
  fi;
  if coeff="U1s" then s:=U1DifferentialSmith(c,k-1,"Zs");
  else s:=U1DifferentialSmith(c,k-1,coeff); fi;
  w:=v*s.V; y:=List([1..Length(D)],i->0);
  for i in [1..Length(w)] do
    if i<=s.rank then
      if coeff<>"U1s" and w[i] mod s.diag[i]<>0 then return fail; fi;
      y[i]:=w[i]/s.diag[i];
    elif coeff="U1s" then
      if not IsInt(w[i]) then return fail; fi;
    elif w[i]<>0 then return fail;
    fi;
  od;
  if coeff="U1s" then return List(y*s.U,U1Mod1); fi;
  return y*s.U;
end);
BindGlobal("U1Solve",function(c,k,coeff,f)
  local a,b,bf,hf;
  if f=U1Zero then return U1Zero; fi;
  a:=U1Native(c,k,coeff,f); b:=U1SolveNative(c,k,coeff,a);
  if b=fail then return fail; fi;
  bf:=U1Bar(c,k-1,coeff,b);
  hf:=U1HomotopyPullback(c.bar,coeff,f);
  return U1Memo(function(xs...)
    local v;
    v:=CallFuncList(bf,xs)-CallFuncList(hf,xs);
    if coeff="F2" then return v mod 2;
    elif coeff="U1s" then return U1Mod1(v); else return v; fi;
  end);
end);

# Optional data-returning form for callers that retain the native phase seed.
# The ordinary U1Solve path above is unchanged; this performs its same
# comparison-map correction while exposing the already computed vectors.
BindGlobal("U1SolveData",function(c,k,coeff,f)
  local a,b,bf,hf,primitive;
  if f=U1Zero then
    return rec(primitive:=U1Zero,
      nativePrimitive:=List([1..Dimension(c.R)(k-1)],i->0),
      nativeObstruction:=List([1..Dimension(c.R)(k)],i->0));
  fi;
  a:=U1Native(c,k,coeff,f);b:=U1SolveNative(c,k,coeff,a);
  if b=fail then return fail;fi;
  bf:=U1Bar(c,k-1,coeff,b);hf:=U1HomotopyPullback(c.bar,coeff,f);
  primitive:=U1Memo(function(xs...)
    local value;
    value:=CallFuncList(bf,xs)-CallFuncList(hf,xs);
    if coeff="F2" then return value mod 2;
    elif coeff="U1s" then return U1Mod1(value);else return value;fi;
  end);
  return rec(primitive:=primitive,nativePrimitive:=b,nativeObstruction:=a);
end);

Read(Concatenation(U1_ROOT,"/gap/backend_smith_units.g"));
