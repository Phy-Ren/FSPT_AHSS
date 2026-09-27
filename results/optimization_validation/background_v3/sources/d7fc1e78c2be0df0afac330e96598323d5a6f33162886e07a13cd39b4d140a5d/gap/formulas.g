# Analytic formulas on normalized inhomogeneous bar cochains.
# Load gap/formula_data.g before this file. No SptSet code is imported.

AFSFormula := function(name, ctx, inputs)
  local key, graph, nodes, top, degree, coeff, fields, x, id, callback, knownzero, i, args;
  inputs:=ShallowCopy(inputs);
  if not IsBound(inputs.w) and IsBound(ctx.omega2) and
     (not IsBoundGlobal("AFSZero") or ctx.omega2<>ValueGlobal("AFSZero")) then
    inputs.w:=ctx.omega2;
  fi;
  if name="pip_obstruction" then return CallFuncList(ValueGlobal("AFSPipO5"),[ctx,inputs]);fi;
  key := Concatenation(name,"_",String(inputs.p));
  if not IsBound(AFSFormulaData.(key)) then Error("Unknown formula ",key); fi;
  graph := AFSFormulaData.(key); top := graph[1]; degree := graph[2];
  nodes := graph[4]; fields := ShallowCopy(inputs);
  fields.afsOmegaZero:=not IsBound(inputs.w) or
    (IsBoundGlobal("AFSZero") and inputs.w=ValueGlobal("AFSZero"));
  if not IsBound(fields.w) then fields.w := function(arg...) return 0; end; fi;
  if not IsBound(fields.s) then fields.s := ctx.s; fi;
  for x in nodes do
    if x[1]="field" and not IsBound(fields.(x[4][1])) then
      Error("Missing formula input ",x[4][1]);
    fi;
  od;
  if IsBoundGlobal("AFSFastPrograms") and
     (not IsBoundGlobal("AFSUseFastFormulas") or ValueGlobal("AFSUseFastFormulas")=true) then
    return CallFuncList(ValueGlobal("AFSMakeFastFormula"),[name,ctx,fields]);
  fi;
  knownzero:=[];
  for i in [1..Length(nodes)] do
    x:=nodes[i];args:=x[4];knownzero[i]:=false;
    if x[1]="zero" then knownzero[i]:=true;
    elif x[1]="field" then
      knownzero[i]:=(args[1]="w" and not IsBound(inputs.w));
      if IsBoundGlobal("AFSZero") and fields.(args[1])=ValueGlobal("AFSZero") then knownzero[i]:=true;fi;
    elif x[1]="add" then knownzero[i]:=knownzero[args[1]] and knownzero[args[2]];
    elif x[1]="scale" then knownzero[i]:=knownzero[args[1]] or args[2]=0;
    elif x[1] in ["reduce","divide","d"] then knownzero[i]:=knownzero[args[1]];
    elif x[1]="word" then knownzero[i]:=Length(args[2])=0 or ForAny(args[1],k->knownzero[k]);
    fi;
  od;
  id := Identity(ctx.G);
  callback := function(arg...)
    local products,cache,visit,i,j,z,ans;
    if Length(arg)<>degree then Error("Formula argument degree mismatch"); fi;
    if ForAny(arg,g->g=id) then return 0; fi;
    products := List([1..degree+1],i->[]);
    for i in [1..degree] do
      z:=id;
      for j in [i+1..degree+1] do z:=z*arg[j-1];products[i][j]:=z;od;
    od;
    cache:=List(nodes,x->[]);
    visit:=function(k,f)
      local code,args,mask,value,v,term,fs,inds,r,sg;
      if knownzero[k] then return 0;fi;
      mask:=Sum(f,v->2^(v-1));
      if IsBound(cache[k][mask]) then return cache[k][mask];fi;
      code:=nodes[k][1];args:=nodes[k][4];
      if code="zero" then value:=0;
      elif code="field" then
        inds:=[];
        if Length(f)>1 then
          for r in [1..Length(f)-1] do Add(inds,products[f[r]][f[r+1]]);od;
        fi;
        if ForAny(inds,g->g=id) then value:=0;
        else value:=CallFuncList(fields.(args[1]),inds);fi;
      elif code="add" then value:=visit(args[1],f)+visit(args[2],f);
      elif code="scale" then value:=visit(args[1],f)*args[2];
      elif code="reduce" then value:=visit(args[1],f);
      elif code="divide" then
        value:=visit(args[1],f);
        if value mod args[2]<>0 then Error("Nonintegral formula quotient");fi;
        value:=QuoInt(value,args[2]);
      elif code="d" then
        value:=0;
        for r in [1..Length(f)] do
          inds:=ShallowCopy(f);Remove(inds,r);
          value:=value+(-1)^(r-1)*visit(args[1],inds);
        od;
      elif code="word" then
        value:=0;
        for term in args[2] do
          if nodes[k][3]=0 then sg:=term[2];else sg:=1;fi;
          for r in [1..Length(args[1])] do
            fs:=f{term[1][r]};sg:=sg*visit(args[1][r],fs);
            if sg=0 then break;fi;
          od;
          value:=value+sg;
        od;
      else Error("Unknown cochain graph instruction");fi;
      if nodes[k][3]<>0 then value:=value mod nodes[k][3];fi;
      cache[k][mask]:=value;return value;
    end;
    ans:=visit(top,[1..degree+1]);
    if name="obstruction" or name="stacking" then return ans/8;fi;
    return ans;
  end;
  if IsBoundGlobal("AFSMemo") then return CallFuncList(ValueGlobal("AFSMemo"),[callback]);fi;
  return callback;
end;;

AFSMakeFastFormula := function(name,ctx,fields)
  local key,id,runner,degree,f,fieldname,normalize,callback;
  key:=Concatenation(name,"_",String(fields.p),"_");id:=Identity(ctx.G);
  if fields.afsOmegaZero then
    key:=Concatenation(key,"w");
  fi;
  if name="obstruction" and IsBoundGlobal("AFSZero") and fields.a=ValueGlobal("AFSZero") then key:=Concatenation(key,"a");fi;
  if IsBoundGlobal("AFSZero") and fields.s=ValueGlobal("AFSZero") then key:=Concatenation(key,"s");fi;
  runner:=AFSFastPrograms.(key);degree:=AFSFormulaData.(Concatenation(name,"_",String(fields.p)))[2];
  normalize:=function(fn)
    return function(xs...)
      if ForAny(xs,g->g=id) then return 0;fi;
      return CallFuncList(fn,xs);
    end;
  end;
  f:=ShallowCopy(fields);
  for fieldname in RecNames(f) do
    if IsFunction(f.(fieldname)) then f.(fieldname):=normalize(f.(fieldname));fi;
  od;
  callback:=function(arg...)
    local products,i,j,g;
    if Length(arg)<>degree then Error("Compiled formula degree mismatch");fi;
    if ForAny(arg,g->g=id) then return 0;fi;
    products:=List([1..degree+1],i->[]);
    for i in [1..degree] do
      g:=id;
      for j in [i+1..degree+1] do g:=g*arg[j-1];products[i][j]:=g;od;
    od;
    return runner(f,products);
  end;
  if IsBoundGlobal("AFSMemo") then return CallFuncList(ValueGlobal("AFSMemo"),[callback]);fi;
  return callback;
end;;

# Mod-two cup-i, with separately normalized bar inputs. Negative cup indices
# are zero. Degrees through five are generated; no group enumeration is used.
AFSCup := function(i,p,a,q,b)
  local data,n,key;
  if i<0 or i>Minimum(p,q) then return function(arg...) return 0;end;fi;
  key:=Concatenation("c",String(i),"_",String(p),"_",String(q));
  if not IsBound(AFSCupData.(key)) then Error("Cup degree not generated");fi;
  data:=AFSCupData.(key);n:=p+q-i;
  return function(arg...)
    local id,verts,term,face,fa,fb,ans,r,j;
    if Length(arg)<>n then Error("Cup degree mismatch");fi;
    if n=0 then return (a()*b()) mod 2;fi;
    id:=One(arg[1]);verts:=[id];
    for r in arg do Add(verts,verts[Length(verts)]*r);od;
    ans:=0;
    for term in data do
      face:=term[1][1];fa:=[];
      for j in [1..Length(face)-1] do Add(fa,verts[face[j]]^-1*verts[face[j+1]]);od;
      face:=term[1][2];fb:=[];
      for j in [1..Length(face)-1] do Add(fb,verts[face[j]]^-1*verts[face[j+1]]);od;
      if not ForAny(fa,g->g=id) and not ForAny(fb,g->g=id) then
        ans:=ans+CallFuncList(a,fa)*CallFuncList(b,fb);
      fi;
    od;
    return ans mod 2;
  end;
end;;

# Full integer-layer terminal obstruction. The generated program is a finite
# compilation of the supplied O5, not a table of space-group answers.
AFSPipO5 := function(ctx,inputs)
  local fields,id,callback,useSign,useGeneral,useBackground,fastfields,normalize,name,names;
  if IsBound(inputs.p) and inputs.p<>1 then Error("Only pip O5 is compiled");fi;
  fields:=ShallowCopy(inputs);id:=Identity(ctx.G);
  if not IsBound(fields.s) then fields.s:=ctx.s;fi;
  if not IsBound(fields.w) and IsBound(ctx.omega2) then fields.w:=ctx.omega2;fi;
  useBackground:=IsBound(fields.w) and
    (not IsBoundGlobal("AFSZero") or fields.w<>ValueGlobal("AFSZero"));
  if useBackground and not IsBoundGlobal("AFSPipO5BackgroundProgram") then
    Error("Nonzero omega requires gap/pip_o5_background.g");
  fi;
  useSign:=not useBackground and IsBoundGlobal("AFSPipO5SignProgram") and inputs.n=ctx.s and fields.s=ctx.s
    and (not IsBoundGlobal("AFSUseSignPipO5") or ValueGlobal("AFSUseSignPipO5")=true);
  useGeneral:=not useBackground and not useSign and IsBoundGlobal("AFSPipO5GeneralProgram")
    and (not IsBoundGlobal("AFSUseGeneralPipO5") or ValueGlobal("AFSUseGeneralPipO5")=true);
  if useSign or useGeneral or useBackground then
    normalize:=function(fn)
      return function(xs...)
        if ForAny(xs,g->g=id) then return 0;fi;
        return CallFuncList(fn,xs);
      end;
    end;
    fastfields:=ShallowCopy(fields);
    if useSign then names:=["b","c","s"];else names:=["n","b","c","s"];fi;
    if useBackground then Add(names,"w");fi;
    for name in names do fastfields.(name):=normalize(fields.(name));od;
  fi;
  callback:=function(arg...)
    local products,i,j,g,values,item,op,value,f,increments;
    if Length(arg)<>5 then Error("pip O5 takes five bar increments");fi;
    if ForAny(arg,g->g=id) then return 0;fi;
    products:=List([1..6],i->[]);
    for i in [1..5] do
      g:=id;
      for j in [i+1..6] do g:=g*arg[j-1];products[i][j]:=g;od;
    od;
    if useSign then return CallFuncList(ValueGlobal("AFSPipO5SignProgram"),[fastfields,products]);fi;
    if useGeneral then return CallFuncList(ValueGlobal("AFSPipO5GeneralProgram"),[fastfields,products]);fi;
    if useBackground then return CallFuncList(ValueGlobal("AFSPipO5BackgroundProgram"),[fastfields,products]);fi;
    values:=[];
    for item in AFSPipO5Program do
      op:=item[1];
      if op="const" then value:=item[2];
      elif op="field" then
        f:=item[3];increments:=[];
        for i in [1..Length(f)-1] do Add(increments,products[f[i]+1][f[i+1]+1]);od;
        if ForAny(increments,g->g=id) then value:=0;
        else value:=CallFuncList(fields.(item[2]),increments);fi;
      elif op="add" then value:=values[item[2]+1]+values[item[3]+1];
      elif op="mul" then value:=values[item[2]+1]*values[item[3]+1];
      elif op="mod" then value:=values[item[2]+1] mod item[3];
      elif op="div" then
        value:=values[item[2]+1];
        if value mod item[3]<>0 then Error("Invalid lower-tower integral quotient in pip O5");fi;
        value:=QuoInt(value,item[3]);
      elif op="floor" then
        value:=values[item[2]+1];value:=(value-(value mod item[3]))/item[3];
      elif op="bit" then
        value:=values[item[2]+1];i:=2^item[3];value:=((value-(value mod i))/i) mod 2;
      else Error("Invalid pip scalar instruction");fi;
      Add(values,value);
    od;
    return values[AFSPipO5Output]/16;
  end;
  if IsBoundGlobal("AFSMemo") then return CallFuncList(ValueGlobal("AFSMemo"),[callback]);fi;
  return callback;
end;;

# Unary C-coordinate bridge for the torsion family n=k*s, omega=0.
# d Lambda_k = normalized native parity + collaborator secondary.
# The four binary polynomials were derived over every legal local simplex;
# they contain no target-group solve and no classification result.
AFSPipCReferenceShift := function(ctx,k,b)
  local polys,masks,callback;
  polys:=[[],[16,24,40,48],[5,7,9,10,14,15,17,23,33,39],
          [5,7,9,10,14,15,16,17,23,24,33,39,40,48]];
  masks:=polys[(k mod 4)+1];
  callback:=function(g,h,j)
    local bits,mask,value,i,term;
    bits:=[ctx.s(g),ctx.s(g*h),ctx.s(g*h*j),b(g,h),b(g,h*j),b(g*h,j)];
    value:=0;
    for mask in masks do
      term:=1;
      for i in [1..6] do
        if QuoInt(mask,2^(i-1)) mod 2=1 then term:=term*bits[i];fi;
      od;
      value:=value+term;
    od;
    return value mod 2;
  end;
  if IsBoundGlobal("AFSMemo") then return CallFuncList(ValueGlobal("AFSMemo"),[callback]);fi;
  return callback;
end;;
