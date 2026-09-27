# Export real native-resolution lower primitives, then independently replay
# their local parity values in Python. These are the six disputed inputs.
Read("gap/backend.g");;
Read("gap/formula_data.g");;
Read("gap/formulas.g");;
_AFPullFields:=function(xs,degree,fn)
  local id,verts,g,face,increments,rows,i;
  id:=One(xs[1]);verts:=[id];for g in xs do Add(verts,verts[Length(verts)]*g);od;
  rows:=[];
  for face in Combinations([0..Length(xs)],degree+1) do
    increments:=[];
    for i in [1..Length(face)-1] do Add(increments,verts[face[i]+1]^-1*verts[face[i+1]+1]);od;
    Add(rows,[face,CallFuncList(fn,increments)]);
  od;
  return rows;
end;;
for sg in [29,41,45,110,120,219] do
  ctx:=AFSBackend(sg);;n:=ctx.s;;
  source:=AFSFormula("pip_majorana",ctx,rec(p:=1,n:=n));;
  b:=AFSSolve(ctx,3,"F2",source);;
  if b=fail then Print("FAILED first primitive SG ",sg,"\n");QUIT_GAP(1);fi;
  parity:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=n,b:=b));;
  gens:=GeneratorsOfGroup(ctx.G);;rows:=[];;
  for trial in [1..8] do
    xs:=List([1..4],i->gens[((i+trial-2) mod Length(gens))+1]^((-1)^(i+trial)));;
    Add(rows,[_AFPullFields(xs,1,n),_AFPullFields(xs,2,b),_AFPullFields(xs,1,ctx.s),CallFuncList(parity,xs)]);
  od;
  PrintTo(Concatenation("runs/pip_samples_sg",String(sg),".json"),[sg,rows],"\n");
  Print("EXPORTED SG ",sg," native lower-tower samples\n");
od;
QUIT_GAP(0);
