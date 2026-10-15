OnBreak:=function() Where(20);QUIT_GAP(1);end;;
U1_ROOT:="/home/xingyu/AllFSPT_reviews/zero_reduction_callbacks_20261015/candidate";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
Read("/home/xingyu/AllFSPT_reviews/zero_reduction_callbacks_20261015/reference_reduction.g");;
rows:=[];;
for spec in [[0,0],[0,1],[1,0],[1,1]] do
 data:=rec(multiplication:=[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]],identity_index:=0,
 s:=List([0,1,0,1],x->spec[1]*x),rho:=List([0,0,1,1],x->spec[2]*x),
 omega:=[["0","0","0","0"],["0","1/2","0","1/2"],["0","0","0","0"],["0","1/2","0","1/2"]]);;
 c:=U1FiniteContext(data,6);;one:=Identity(c.G);;els:=Filtered(Elements(c.G),g->g<>one);;
 for d in [2,3] do
  if d=2 then
   u:=U1Zero;;v:=function(g) if g=one then return 0;fi;return 2*c.elementIndex(g)-7;end;;
  else
   u:=function() return -3;end;;
   v:=function(g,h) if g=one or h=one then return 0;fi;return 2*c.elementIndex(g)-3*c.elementIndex(h)+1;end;;
  fi;
  a:=U1Gauge(c,d,U1Vacuum(),u,v);;U1CheckCompletedState(c,d,a);;
  raw:=a;;sheetCount:=0;;
  if raw.sheet<>U1Zero then
   gu:=U1Solve(c,d-2,"Zs",U1Scale(-1,raw.sheet));;
   if gu=fail then Error("exact sheet failed");fi;
   raw:=U1Gauge(c,d,raw,gu,U1Zero);;
   for xs in Tuples(els,d-2) do
    if CallFuncList(raw.sheet,xs)<>0 then Error("discarded sheet not pointwise zero");fi;
    sheetCount:=sheetCount+1;
   od;
   raw.sheet:=U1Zero;
  fi;
  dq:=U1Coboundary(c,"Zr",raw.charge);;
  for xs in Tuples(els,d+1) do
   if CallFuncList(dq,xs)<>0 then Error("charge is not closed after sheet gauge");fi;
  od;
  gv:=U1Solve(c,d,"Zr",U1Scale(-1,raw.charge));;
  if gv=fail then Error("exact charge failed");fi;
  raw:=U1Gauge(c,d,raw,U1Zero,gv);;
  for xs in Tuples(els,d) do
   if CallFuncList(raw.charge,xs)<>0 then Error("discarded charge not pointwise zero");fi;
  od;
  reference:=U1ReduceVacuumReference(c,d,a);;oldWitness:=ShallowCopy(c.reductionWitnesses[Length(c.reductionWitnesses)]);;
  candidate:=U1ReduceVacuum(c,d,a);;newWitness:=c.reductionWitnesses[Length(c.reductionWitnesses)];;
  if oldWitness<>newWitness then Error("native gauge/phase witness differs");fi;
  for xs in Tuples(els,d+1) do
   if U1Mod1(CallFuncList(reference,xs)-CallFuncList(candidate,xs))<>0 then Error("phase representative changed");fi;
  od;
  Add(rows,rec(dimension:=d,sSign:=spec[1],rhoSign:=spec[2],sheetValuesChecked:=sheetCount,
   chargeValuesChecked:=3^d,chargeClosureValuesChecked:=3^(d+1),phaseEqualityValuesChecked:=3^(d+1),
   nativeWitnessesIdentical:=true));;
 od;
od;
f:=OutputTextFile("/home/xingyu/AllFSPT_reviews/zero_reduction_callbacks_20261015/zero_identity_checks.json",false);;SetPrintFormattingStatus(f,false);;
WriteLine(f,U1JSON(rec(passed:=true,rows:=rows)));;CloseStream(f);;QUIT_GAP(0);
