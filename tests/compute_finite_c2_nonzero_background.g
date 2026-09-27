# Independent finite controls, never used as affine classification input.
# No expected stacking invariant is embedded in this calculation.
AFS_ROOT:=".";;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
AFS_USE_MOD2_CONTRACTION:=true;;AFS_USE_MOD2_BAR:=false;;
AFS_STACK_AUDIT:=true;;
for sourceFile in ["backend.g","backend_mod2_contraction.g","backend_diagonal.g",
    "class_coordinates.g","formula_data.g","formula_fast.g","pip_o5_program.g",
    "pip_o5_sign.g","pip_o5_general.g","formulas.g","pip_o5_background.g",
    "background_operations.g","classification.g","pip.g","stacking.g",
    "pip_incoming_background.g","background_quotient.g","background_stacking.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;

MakeC2Context:=function(signBit)
  local c,G,character;
  G:=CyclicGroup(IsPcpGroup,2);
  character:=function(g) if g=One(G) then return 0;else return 1;fi;end;
  c:=rec(number:=0,G:=G,differentialCache:=rec(),smithCache:=rec(),
    cohomologyCache:=rec(),f2SolveCache:=rec());
  if signBit=0 then c.sign:=g->1;c.s:=AFSZero;
  else c.sign:=g->(-1)^character(g);c.s:=character;fi;
  c.action:=c.sign;c.omega2:=function(g,h) return character(g)*character(h);end;
  c.R:=ResolutionFiniteGroup(G,6,false,0,"extendible");
  c.bar:=AFSComparison(c.R);
  return c;
end;;

rows:=[];;
for signBit in [0,1] do
  ctx:=MakeC2Context(signBit);;
  C:=AFSClassify(ctx);;
  stack:=AFSBackgroundFullStacking(C);;
  Assert(0,stack.status="computed");
  record:=rec(group:="CyclicGroup(2)",spatialDimension:=3,
    sign:=signBit,omega:="nontrivial-square-of-binary-character",
    layers:=rec(pip:=C.summary.pip.orders,majorana:=C.summary.majorana,
      fermion:=C.summary.complex_fermion,bosonic:=C.summary.bosonic),
    stacking:=AFSBackgroundStackingExport(C,stack));;
  if IsBound(C.summary.preH0IncomingGraded) then
    record.preH0IncomingGraded:=C.summary.preH0IncomingGraded;
  fi;
  Add(rows,record);
  Print("FINITE_C2_NONZERO_BACKGROUND_RESULT s=",signBit," layers=",record.layers,
    " invariants=",stack.invariants,"\n");
od;
LoadPackage("json");;
stream:=OutputTextFile("finite_c2_nonzero_background.json",false);;
SetPrintFormattingStatus(stream,false);
WriteAll(stream,GapToJsonString(rec(scope:="independent-finite-C2-nonzero-omega-control",
  computed_without_expected_answers:=true,results:=rows)));
CloseStream(stream);
Print("FINITE_C2_NONZERO_BACKGROUND_TEST_PASS\n");
QUIT_GAP(0);
