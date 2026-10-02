# Exact, persistent transport to the current formula evaluator. One process is
# shared by all simplex requests in a finite-symmetry computation.

# An injective typed key for the currently specified integer face packets.
# Unknown operations, extra fields, nonintegers, and malformed array shapes
# retain the original JSON key path instead of sharing an incomplete key.
BindGlobal("AFSFullRequestIntegerKey",function(request)
  local d,operation,stage,expected,records,names,outer,key,i,j,values;
  if not IsRecord(request) or not IsBound(request.dimension) or
    not IsBound(request.operation) or not IsBound(request.stage) then return fail;fi;
  d:=request.dimension;if not IsInt(d) or not d in [1..4] then return fail;fi;
  stage:=Position(["majorana","fermion","bosonic"],request.stage);
  if stage=fail then return fail;fi;
  if request.operation="source" then
    operation:=1;outer:=["dimension","operation","stage","fields"];
    if not IsBound(request.fields) then return fail;fi;
    records:=[request.fields];names:=[["n","a","c","w","s"]];expected:=2^(d+stage);
  elif request.operation="product" then
    operation:=2;outer:=["dimension","operation","stage","left","right","background"];
    if not IsBound(request.left) or not IsBound(request.right) or not IsBound(request.background) then return fail;fi;
    records:=[request.left,request.right,request.background];
    names:=[["n","a","c"],["n","a","c"],["w","s"]];expected:=2^(d+stage-1);
  elif request.operation="vacuum-majorana-gauge" and d=4 and stage in [2,3] then
    operation:=3;outer:=["dimension","operation","stage","fields"];
    if not IsBound(request.fields) then return fail;fi;
    records:=[request.fields];names:=[["beta","w","s"]];expected:=2^(stage+3);
  elif request.operation="vacuum-fermion-gauge" and d=4 and stage=3 then
    operation:=4;outer:=["dimension","operation","stage","fields"];
    if not IsBound(request.fields) then return fail;fi;
    records:=[request.fields];names:=[["gamma","w","s"]];expected:=64;
  elif request.operation="majorana-gauge-n0" and d in [3,4] and stage in [2,3] then
    operation:=5;outer:=["dimension","operation","stage","fields"];
    if not IsBound(request.fields) then return fail;fi;
    records:=[request.fields];names:=[["a","c","beta","w","s"]];expected:=2^(d+stage-1);
  elif request.operation="fermion-gauge-n0" and d in [3,4] and stage=3 then
    operation:=6;outer:=["dimension","operation","stage","fields"];
    if not IsBound(request.fields) then return fail;fi;
    records:=[request.fields];names:=[["c","gamma","w","s"]];expected:=2^(d+2);
  else return fail;fi;
  if Set(RecNames(request))<>Set(outer) then return fail;fi;
  key:=[d,operation,stage,expected];
  for i in [1..Length(records)] do
    if not IsRecord(records[i]) or Set(RecNames(records[i]))<>Set(names[i]) then return fail;fi;
    for j in names[i] do
      values:=records[i].(j);
      if not IsList(values) or not IsDenseList(values) or Length(values)<>expected or
        not ForAll(values,IsInt) then return fail;fi;
      Append(key,values);
    od;
  od;
  return key;
end);

BindGlobal("AFSFullFormulaOpen",function(c)
  local python,worker,stream,args,coordinate;
  if IsBound(c.fullFormulaTransport) then return c.fullFormulaTransport;fi;
  LoadPackage("json");LoadPackage("io");
  python:="python3";if IsBoundGlobal("AFS_FULL_PYTHON") then python:=ValueGlobal("AFS_FULL_PYTHON");fi;
  worker:=Concatenation(AFS_ROOT,"/scripts/full_formula_worker.py");
  args:=["-u",worker];
  if IsBoundGlobal("AFS_FULL_PURE_CF_SOURCE") and ValueGlobal("AFS_FULL_PURE_CF_SOURCE")=true then
    Add(args,"--pure-cf-source");
  fi;
  if IsBoundGlobal("AFS_FULL_N0_SOURCE") and ValueGlobal("AFS_FULL_N0_SOURCE")=true then
    Add(args,"--n0-source");
  fi;
  if IsBoundGlobal("AFS_FULL_COORDINATE") and ValueGlobal("AFS_FULL_COORDINATE")<>"publication" then
    coordinate:=ValueGlobal("AFS_FULL_COORDINATE");
    if not coordinate in ["majorana-ca","majorana-operator"] then Error("unknown coordinate");fi;
    worker:=Concatenation(AFS_ROOT,"/scripts/closed_majorana_worker.py");
    if coordinate="majorana-ca" then coordinate:="ca";else coordinate:="operator";fi;
    args:=["-u",worker,"--coordinate",coordinate];
  fi;
  stream:=IO_Popen2(python,args);
  if stream=fail then Error("could not start complete-formula worker");fi;
  c.fullFormulaTransport:=rec(stream:=stream,requests:=0,cache:=NewDictionary("",true));
  c.fullFormulaTransport.vectorCacheLookups:=0;c.fullFormulaTransport.vectorCacheHits:=0;
  if IsBoundGlobal("AFS_FULL_VECTOR_REQUEST_CACHE") and ValueGlobal("AFS_FULL_VECTOR_REQUEST_CACHE")=true then
    c.fullFormulaTransport.vectorCache:=NewDictionary([1],true);
  fi;
  if IsBoundGlobal("AFS_FULL_TRACE") then
    c.fullFormulaTransport.trace:=OutputTextFile(ValueGlobal("AFS_FULL_TRACE"),true);
    SetPrintFormattingStatus(c.fullFormulaTransport.trace,false);
  fi;
  return c.fullFormulaTransport;
end);

BindGlobal("AFSFullFormulaRequest",function(c,request)
  local tr,key,vectorKey,value,line,response,stage;
  tr:=AFSFullFormulaOpen(c);key:=fail;vectorKey:=fail;
  if IsBound(tr.vectorCache) then
    vectorKey:=AFSFullRequestIntegerKey(request);
    if vectorKey<>fail then
      tr.vectorCacheLookups:=tr.vectorCacheLookups+1;
      value:=LookupDictionary(tr.vectorCache,vectorKey);
      if value<>fail then tr.vectorCacheHits:=tr.vectorCacheHits+1;return value;fi;
    fi;
  fi;
  if vectorKey=fail then
    key:=GapToJsonString(request);value:=LookupDictionary(tr.cache,key);
    if value<>fail then return value;fi;
  fi;
  if key=fail then key:=GapToJsonString(request);fi;
  IO_WriteLine(tr.stream.stdin,key);line:=IO_ReadLine(tr.stream.stdout);
  if line=fail or line="" then Error("complete-formula worker terminated unexpectedly");fi;
  response:=JsonStringToGap(line);
  if IsBound(tr.trace) then
    stage:="unknown";if IsBound(c.stageTimings) and Length(c.stageTimings)>0 then stage:=Last(c.stageTimings).stage;fi;
    PrintTo(tr.trace,GapToJsonString(rec(stage:=stage,request:=request,response:=response)),"\n");
  fi;
  if IsBound(response.error) then Error("complete-formula worker: ",response.error," ",response.message);fi;
  if IsBound(response.value) then value:=response.value;
  else value:=response.numerator/response.denominator;fi;
  if vectorKey=fail then AddDictionary(tr.cache,key,value);
  else AddDictionary(tr.vectorCache,vectorKey,value);fi;
  tr.requests:=tr.requests+1;
  return value;
end);

BindGlobal("AFSFullFormulaClose",function(c)
  if IsBound(c.fullFormulaTransport) then
    IO_Close(c.fullFormulaTransport.stream.stdin);IO_Close(c.fullFormulaTransport.stream.stdout);
    if IsBound(c.fullFormulaTransport.trace) then CloseStream(c.fullFormulaTransport.trace);fi;
  fi;
end);

# A face cochain is evaluated in the local trivialization at its first vertex.
# Masks are zero based in the wire format (entry mask+1 in a GAP list).
BindGlobal("AFSFullFaceVector",function(vertices,degree,f)
  local out,face,mask;
  out:=List([1..2^Length(vertices)],i->0);
  if f=AFSZero then return out;fi;
  for face in Combinations([1..Length(vertices)],degree+1) do
    mask:=Sum(face,i->2^(i-1));out[mask+1]:=f(vertices{face});
  od;
  return out;
end);

BindGlobal("AFSFullFaceFields",function(d,vertices,state,background)
  return rec(n:=AFSFullFaceVector(vertices,d-2,state.n),
    a:=AFSFullFaceVector(vertices,d-1,state.a),
    c:=AFSFullFaceVector(vertices,d,state.c),
    w:=AFSFullFaceVector(vertices,2,background.w),
    s:=AFSFullFaceVector(vertices,1,background.s));
end);

BindGlobal("AFSFullSourceSimplex",function(c,d,stage,vertices,state,background)
  return AFSFullFormulaRequest(c,rec(dimension:=d,operation:="source",stage:=stage,
    fields:=AFSFullFaceFields(d,vertices,state,background)));
end);

BindGlobal("AFSFullProductSimplex",function(c,d,stage,vertices,left,right,background)
  local lf,rf,bg;
  lf:=AFSFullFaceFields(d,vertices,left,background);
  rf:=AFSFullFaceFields(d,vertices,right,background);
  bg:=rec(w:=lf.w,s:=lf.s);Unbind(lf.w);Unbind(lf.s);Unbind(rf.w);Unbind(rf.s);
  return AFSFullFormulaRequest(c,rec(dimension:=d,operation:="product",stage:=stage,
    left:=lf,right:=rf,background:=bg));
end);
