AFS_ROOT:=".";;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","formula_data.g","formula_fast.g",
    "pip_o5_program.g","formulas.g","stacking.g","pip_free.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
ctx:=AFSInfiniteDihedralContext();;x:=AFSInfiniteDihedralEvenLift(ctx);;
Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=x.n,b:=x.b));;
dC:=AFSCoboundary(ctx,"F2",x.c);;
O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));;
dV:=AFSCoboundary(ctx,"U1s",x.v);;
fixtures:=[[[1,0],[0,1],[-1,0],[1,1],[0,1]],
  [[-2,1],[1,0],[1,1],[0,1],[2,0]],
  [[2,0],[-1,1],[0,1],[-2,0],[1,1]],
  [[0,0],[2,1],[-1,0],[1,1],[-2,1]]];;
for fixture in fixtures do
  xs:=List(fixture,p->ctx.pairElement(p[1],p[2]));
  for i in [1..4] do
    Assert(0,ctx.integerCharacter(xs[i]*xs[i+1])=
      ctx.integerCharacter(xs[i])+ctx.sign(xs[i])*ctx.integerCharacter(xs[i+1]));
  od;
  Assert(0,CallFuncList(dC,xs{[1..4]})=CallFuncList(Q,xs{[1..4]}));
  Assert(0,AFSMod1(CallFuncList(dV,xs)-CallFuncList(O,xs))=0);
  Print("DIHEDRAL_EXTRA_BAR_TUPLE_PASS ",fixture," cpu_ms=",Runtime(),"\n");
od;
Print("DIHEDRAL_NON_NATIVE_BAR_FLATNESS_PASS\n");
QUIT_GAP(0);
