# Exact cochain operations. A bar cochain is based at its first vertex.
BindGlobal("U1Add",function(a,b)
  if a=U1Zero then return b;fi;if b=U1Zero then return a;fi;
  return U1Memo(function(xs...) return CallFuncList(a,xs)+CallFuncList(b,xs);end);
end);
BindGlobal("U1Scale",function(n,a)
  if n=0 or a=U1Zero then return U1Zero;fi;if n=1 then return a;fi;
  return U1Memo(function(xs...) return n*CallFuncList(a,xs);end);
end);
BindGlobal("U1Cup",function(c,p,a,ca,q,b,cb,i,binary)
  local degree,cuts;
  if a=U1Zero or b=U1Zero or i<0 or i>Minimum(p,q) then return U1Zero;fi;
  degree:=p+q-i;cuts:=U1CupCuts.(Concatenation("c",String(p),"_",String(q),"_",String(i)));
  return U1Memo(function(xs...)
    local vs,g,term,left,right,value,sg,j,edges,edgeStart,edgeEnd;
    if Length(xs)<>degree then Error("cup arity mismatch");fi;
    # In a nonabelian group, (x1...xi)^-1*(x1...xj)=x(i+1)...xj.
    # Preserve the original order; all coefficient actions still use prefixes.
    edges:=[];
    for edgeStart in [1..degree] do
      edges[edgeStart]:=[];g:=xs[edgeStart];edges[edgeStart][edgeStart+1]:=g;
      for edgeEnd in [edgeStart+2..degree+1] do g:=g*xs[edgeEnd-1];edges[edgeStart][edgeEnd]:=g;od;
    od;
    vs:=[Identity(c.G)];for j in [2..degree+1] do Add(vs,edges[1][j]);od;
    value:=0;
    for term in cuts do
      left:=List([1..Length(term[1])-1],j->edges[term[1][j]][term[1][j+1]]);
      right:=List([1..Length(term[2])-1],j->edges[term[2][j]][term[2][j+1]]);
      sg:=1;
      if not binary then sg:=term[3]*U1CoefficientAction(c,ca,vs[term[1][1]])*U1CoefficientAction(c,cb,vs[term[2][1]]);fi;
      value:=value+sg*CallFuncList(a,left)*CallFuncList(b,right);
    od;
    if binary then return value mod 2;fi;return value;
  end);
end);
BindGlobal("U1Sq2",function(c,p,a)
  return U1Add(U1Cup(c,p,a,"F2",p,a,"F2",p-2,true),
    U1Cup(c,p,a,"F2",p+1,U1Coboundary(c,"F2",a),"F2",p-1,true));
end);
BindGlobal("U1ChargeSource",function(c,d,q)
  return U1Add(U1Cup(c,2,c.omega,"Zt",d,q,"Zr",0,false),U1Scale(1/2,U1Sq2(c,d,q)));
end);
BindGlobal("U1ChargeProduct",function(c,d,q,r)
  return U1Scale(1/2,U1Add(U1Cup(c,d,q,"F2",d,r,"F2",d-1,true),
    U1Cup(c,d+1,U1Coboundary(c,"F2",q),"F2",d,r,"F2",d,true)));
end);
BindGlobal("U1ChargeGauge",function(c,d,q,v)
  return U1Add(U1Add(U1Cup(c,2,c.omega,"Zt",d-1,v,"Zr",0,false),
    U1Scale(1/2,U1Sq2(c,d-1,v))),U1ChargeProduct(c,d,q,U1Coboundary(c,"Zr",v)));
end);

# Only strings, exact numbers, booleans, records and lists enter this serializer.
DeclareGlobalFunction("U1JSON");
InstallGlobalFunction(U1JSON,function(x)
  local names;
  if IsStringRep(x) then return Concatenation("\"",ReplacedString(ReplacedString(x,"\\","\\\\"),"\"","\\\""),"\"");fi;
  if x=true then return "true";fi;if x=false then return "false";fi;
  if IsInt(x) then return String(x);fi;
  if IsRat(x) then return U1JSON(String(x));fi;
  if IsList(x) then return Concatenation("[",JoinStringsWithSeparator(List(x,U1JSON),","),"]");fi;
  if IsRecord(x) then
    names:=RecNames(x);return Concatenation("{",JoinStringsWithSeparator(List(names,k->Concatenation(U1JSON(k),":",U1JSON(x.(k)))),","),"}");fi;
  Error("Unsupported JSON type");
end);
BindGlobal("U1Worker",function(c,request)
  local line,out,key,cached;
  # Cache the complete exact request, including all signs, background/lower
  # cochains, operation, dimensions and output component. Bound retained memory
  # by clearing at capacity; eviction changes only execution cost.
  request.response_format:="gap";request.("return"):="top";request.validate:=false;
  key:=U1JSON(request);
  if not IsBound(c.requestCache) then c.requestCache:=NewDictionary("",true);c.requestCacheSize:=0;c.requestCacheHits:=0;c.requestCacheFlushes:=0;fi;
  cached:=LookupDictionary(c.requestCache,key);
  if cached<>fail then c.requestCacheHits:=c.requestCacheHits+1;return cached;fi;
  if not IsBound(c.worker) then
    c.worker:=InputOutputLocalProcess(Directory(U1_ROOT),Filename(DirectoriesSystemPrograms(),"python3"),["-u",Concatenation(U1_ROOT,"/scripts/formula_worker.py")]);
    c.workerCalls:=0;
  fi;
  WriteLine(c.worker,key);line:=ReadLine(c.worker);
  if line=fail then Error("U1 formula worker closed its stream");fi;
  out:=EvalString(line);
  if not out.ok then Error("U1 formula worker: ",out.error);fi;
  c.workerCalls:=c.workerCalls+1;
  cached:=EvalString(out.result);
  if c.requestCacheSize>=8192 then
    c.requestCache:=NewDictionary("",true);c.requestCacheSize:=0;c.requestCacheFlushes:=c.requestCacheFlushes+1;
  fi;
  AddDictionary(c.requestCache,key,cached);c.requestCacheSize:=c.requestCacheSize+1;
  return cached;
end);
BindGlobal("U1LocalField",function(c,p,f,vs)
  local out,face,xs,val,key;
  out:=rec();if f=U1Zero then return out;fi;
  for face in Combinations([1..Length(vs)],p+1) do
    xs:=List([1..Length(face)-1],j->vs[face[j]]^-1*vs[face[j+1]]);
    val:=CallFuncList(f,xs);if val=0 then continue;fi;
    key:=JoinStringsWithSeparator(List(face,i->String(i-1)),",");out.(key):=String(val);
  od;return out;
end);
DeclareGlobalFunction("U1LocalFieldGeometry");
# Geometry depends on the exact tuple and this immutable symmetry context.
# For vertices v_j=x_1...x_j, v_i^-1 v_j=x_(i+1)...x_j, also in a nonabelian
# group. Cache these consecutive products instead of repeatedly inverting
# prefixes on every face. Contexts for paired spins do not share this cache.
BindGlobal("U1FormulaGeometry",function(c,xs)
  local key,geom,g,i,j;
  if not IsBound(c.formulaGeometryCache) or c.formulaGeometryBackground<>[c.s,c.rho,c.omega] then
    c.formulaGeometryCache:=NewDictionary([1],true);c.formulaGeometryCount:=0;c.formulaGeometryHits:=0;c.formulaGeometryFlushes:=0;
    c.formulaGeometryBackground:=[c.s,c.rho,c.omega];
  fi;
  key:=U1Key(xs);geom:=LookupDictionary(c.formulaGeometryCache,key);
  if geom<>fail then c.formulaGeometryHits:=c.formulaGeometryHits+1;return geom;fi;
  geom:=rec(vs:=[Identity(c.G)],faces:=rec(),edges:=[]);
  for i in [1..Length(xs)] do
    geom.edges[i]:=[];g:=Identity(c.G);
    for j in [i+1..Length(xs)+1] do g:=g*xs[j-1];geom.edges[i][j]:=g;od;
  od;
  for j in [2..Length(xs)+1] do Add(geom.vs,geom.edges[1][j]);od;
  geom.s:=List(geom.vs,c.s);geom.rho:=List(geom.vs,c.rho);
  geom.omega:=U1LocalFieldGeometry(c,2,c.omega,geom);
  if c.formulaGeometryCount>=8192 then
    c.formulaGeometryCache:=NewDictionary([1],true);c.formulaGeometryCount:=0;c.formulaGeometryFlushes:=c.formulaGeometryFlushes+1;
  fi;
  AddDictionary(c.formulaGeometryCache,key,geom);c.formulaGeometryCount:=c.formulaGeometryCount+1;
  return geom;
end);
InstallGlobalFunction(U1LocalFieldGeometry,function(c,p,f,geom)
  local out,face,xs,val,key,entry;
  out:=rec();if f=U1Zero then return out;fi;
  key:=String(p);
  if not IsBound(geom.faces.(key)) then
    geom.faces.(key):=[];
    for face in Combinations([1..Length(geom.vs)],p+1) do
      xs:=List([1..Length(face)-1],j->geom.edges[face[j]][face[j+1]]);
      Add(geom.faces.(key),[JoinStringsWithSeparator(List(face,i->String(i-1)),","),xs]);
    od;
  fi;
  for entry in geom.faces.(key) do
    val:=CallFuncList(f,entry[2]);if val<>0 then out.(entry[1]):=String(val);fi;
  od;
  return out;
end);
BindGlobal("U1Formula",function(c,op,d,state,extra,component,degree)
  state:=ShallowCopy(state);extra:=ShallowCopy(extra);
  return U1Memo(function(xs...)
    local geom,request,name,p;
    if Length(xs)<>degree then Error("formula arity mismatch");fi;
    if Identity(c.G) in xs then return 0;fi;
    geom:=U1FormulaGeometry(c,xs);
    request:=rec(op:=op,dimension:=d,simplex_dimension:=degree,s:=geom.s,rho:=geom.rho,
      omega:=geom.omega,sheet:=U1LocalFieldGeometry(c,d-2,state.sheet,geom),charge:=U1LocalFieldGeometry(c,d,state.charge,geom));
    if component<>fail then request.output_component:=component;fi;
    for name in RecNames(extra) do
      if name="sheet_prime" then p:=d-2;
      elif name="charge_prime" then p:=d;
      elif name="sheet_parameter" then p:=d-3;
      elif name="charge_parameter" then p:=d-1;
      else Error("Unknown formula field");fi;
      request.(name):=U1LocalFieldGeometry(c,p,extra.(name),geom);
    od;
    return U1Worker(c,request);
  end);
end);
