# Exact periods of a CLOSED bar U1_s cochain on Smith dual cycles.
# This avoids evaluating the cochain on every native cell when only its class
# is needed. Closure is a precondition, supplied by the obstruction identity;
# this routine is not a general substitute for testing an arbitrary cochain.
BindGlobal("AFSU1BarCoordinates",function(ctx,k,H,f)
  local key,s,inds,cycles,j,z,terms,i,t,one,out,v,order;
  if Length(H.orders)=0 then return [];fi;
  key:=String(k);
  if not IsBound(ctx.phaseClassCycles) then ctx.phaseClassCycles:=rec();fi;
  if not IsBound(ctx.phaseClassCycles.(key)) then
    s:=H.smith;inds:=Filtered([1..s.rank],i->AbsInt(s.diag[i])>1);
    cycles:=[];one:=Identity(ctx.G);
    for j in inds do
      z:=List(s.Ui,r->SignInt(s.diag[j])*r[j]);terms:=[];
      # D_(k-1) z=0 over Z_s follows from D_(k-1) D_k=0 and d_j<>0.
      if ForAny(AFSDifferential(ctx,k-1,"Zs")*z,x->x<>0) then
        Error("Smith dual vector is not an integral twisted cycle");fi;
      # F(z)=s_bar F(dz): combine the group-ring boundary before constructing
      # the top bar chain, so individual degree-k F(e_i) are never expanded.
      terms:=List(AFSChainToBarCombination(ctx.bar,k,z),
        t->[t[1]*ctx.sign(t[2]),one,t[3]]);
      Add(cycles,AFSCombineChain(terms,true));
    od;
    ctx.phaseClassCycles.(key):=cycles;
  fi;
  out:=[];cycles:=ctx.phaseClassCycles.(key);
  for i in [1..Length(cycles)] do
    v:=0;order:=H.orders[i];
    for t in cycles[i] do v:=v+t[1]*CallFuncList(f,t[3]);od;
    v:=order*v;
    if not IsInt(v) then Error("closed phase has a nonintegral torsion period");fi;
    Add(out,v mod order);
  od;
  return out;
end);
