# Seeded pointwise probes use fresh nondegenerate bar tuples, independent of
# cancellation on a native cell or membership in the comparison-map support.
BindGlobal("AFSFullSeededBarProbe",function(C,x,label,samples,seed,clearedLayer)
  local c,d,elements,rng,records,test,stage,field,degree,coeff,modulus,source,diff;
  c:=C.ctx;d:=C.dimension;elements:=Filtered(c.elements,g->g<>Identity(c.G));
  if Length(elements)=0 then return rec(label:=label,status:="vacuous-trivial-group",checks:=[]);fi;
  rng:=RandomSource(IsMersenneTwister,seed);records:=[];
  test:=function(name,k,modulus,f)
    local count,limit,seen,xs,key,value,i;
    limit:=Minimum(samples,Length(elements)^k);seen:=NewDictionary([1],true);count:=0;
    while count<limit do
      xs:=List([1..k],i->Random(rng,elements));key:=List(xs,c.elementIndex);
      if LookupDictionary(seen,key)<>fail then continue;fi;
      AddDictionary(seen,key,true);value:=CallFuncList(f,xs);
      if modulus=1 then value:=AFSMod1(value);elif modulus=2 then value:=value mod 2;fi;
      if value<>0 then Error("seeded pointwise bar audit failed: ",label," ",name," ",key," residual=",value);fi;
      count:=count+1;
    od;
    Add(records,rec(equation:=name,degree:=k,samples:=count));
  end;
  test("integer-closed",d-1,0,AFSCoboundary(c,"Zs",x.n));
  for stage in ["majorana","fermion","bosonic"] do
    if stage="majorana" then field:=x.a;degree:=d;coeff:="F2";modulus:=2;
    elif stage="fermion" then field:=x.c;degree:=d+1;coeff:="F2";modulus:=2;
    else field:=x.v;degree:=d+2;coeff:="U1s";modulus:=1;fi;
    source:=AFSFullSource(c,d,stage,x);
    diff:=AFSCoadd(modulus,[AFSCoboundary(c,coeff,field),AFSComul(modulus,-1,source)]);
    test(Concatenation(stage,"-flat"),degree,modulus,diff);
  od;
  # Inspect an actual gauge endpoint before the reducer replaces its removed
  # field by the exact zero function. This prevents that assignment from
  # hiding a failure of the primitive or cylinder calculation.
  if clearedLayer in [1,2,3] then
    test("cleared-integer-field",d-2,0,x.n);
    if clearedLayer<=2 then test("cleared-Majorana-field",d-1,2,x.a);fi;
    if clearedLayer<=1 then test("cleared-fermion-field",d,2,x.c);fi;
  fi;
  return rec(label:=label,status:="passed",seed:=seed,checks:=records);
end);

BindGlobal("AFSFullSeededBarAudit",function(C,names,samples,seed)
  local i,g,indices,records,target,reduced,serial,power,powerLabel,allowed;
  if not IsBound(C.ctx.elements) or not IsBound(C.ctx.elementIndex) then
    Error("seeded pointwise audit currently requires the finite-group adapter");
  fi;
  indices:=Filtered([1..Length(C.generators)],i->C.generators[i].name in names);
  if Length(indices)<>Length(Set(names)) then Error("unknown marked generator in seeded bar audit");fi;
  records:=[];serial:=0;
  for i in indices do
    g:=C.generators[i];
    AFSStage(C.ctx,Concatenation("full_seeded_bar_",g.name));
    Add(records,AFSFullSeededBarProbe(C,g.state,g.name,samples,seed+serial,-1));serial:=serial+1;
    power:=g.order;allowed:=[1..i-1];
    if power=0 then power:=2;allowed:=[1..i];fi;
    powerLabel:=Concatenation("power-",String(power),"-",g.name);
    target:=AFSFullPower(C.ctx,C.dimension,g.state,power);
    Add(records,AFSFullSeededBarProbe(C,target,powerLabel,samples,seed+serial,-1));serial:=serial+1;
    C.reductionProbe:=function(layer,state)
      local label;
      label:=Concatenation(powerLabel,"-gauge-end-layer-",String(layer));
      AFSStage(C.ctx,Concatenation("full_seeded_bar_",label));
      Add(records,AFSFullSeededBarProbe(C,state,label,samples,seed+serial,layer));serial:=serial+1;
    end;
    reduced:=AFSFullReduce(C,target,allowed);
    Unbind(C.reductionProbe);
  od;
  return rec(status:="passed",requestedSamplesPerEquation:=samples,initialSeed:=seed,
    generators:=names,scope:="seeded distinct nondegenerate bar tuples; not exhaustive",records:=records);
end);
