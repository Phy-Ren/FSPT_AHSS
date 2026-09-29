# Pure cochain adapter. All group products preserve the bar increment order.
AFSD4Phase := function(ctx,p,n,b,cf)
  local name,runner,id,fields,normalize,callback,field;
  if not p in [1,2] then Error("O5/O6 phase degree required");fi;
  name:=Concatenation("AFSD4PhaseP",String(p));
  if n=AFSZero then name:=Concatenation(name,"ZeroProgram");
  else name:=Concatenation(name,"FullProgram");fi;
  if not IsBoundGlobal(name) then Error("Missing compiled phase: ",name);fi;
  runner:=ValueGlobal(name);id:=Identity(ctx.G);
  fields:=rec(n:=n,b:=b,c:=cf,w:=ctx.omega2,s:=ctx.s);
  normalize:=function(fn)
    return function(xs...)
      if ForAny(xs,g->g=id) then return 0;fi;
      return CallFuncList(fn,xs);
    end;
  end;
  for field in RecNames(fields) do fields.(field):=normalize(fields.(field));od;
  callback:=function(arg...)
    local products,i,j,g;
    if Length(arg)<>p+4 then Error("Phase bar degree mismatch");fi;
    if ForAny(arg,g->g=id) then return 0;fi;
    products:=List([1..p+5],i->[]);
    for i in [1..p+4] do
      g:=id;
      for j in [i+1..p+5] do g:=g*arg[j-1];products[i][j]:=g;od;
    od;
    return runner(fields,products);
  end;
  return AFSMemo(callback);
end;;
