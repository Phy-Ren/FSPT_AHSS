AFS_ROOT:=".";;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","formula_data.g","formula_fast.g",
    "pip_o5_program.g","formulas.g","stacking.g","pip_free.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
ctx:=AFSInfiniteDihedralContext();;
Print("DIHEDRAL_NATIVE_DIMENSIONS ",List([0..6],i->Dimension(ctx.R)(i)),"\n");
Assert(0,AFSStackSupportZero(ctx,2,0,AFSCoboundary(ctx,"Zs",ctx.integerCharacter)));
for n in [-3..3] do for s in [0,1] do
  g:=ctx.pairElement(n,s);Assert(0,ctx.integerCharacter(g)=n and ctx.s(g)=s);
od;od;
Assert(0,AFSCohomology(ctx,5,"U1s").orders=[]);
x:=AFSInfiniteDihedralEvenLift(ctx);;
source:=AFSFormula("pip_majorana",ctx,rec(p:=1,n:=x.n));;
Assert(0,AFSStackSupportZero(ctx,3,2,source));
Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=x.n,b:=x.b));;
Assert(0,AFSStackSupportZero(ctx,4,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.c),Q])));
O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));;
Assert(0,AFSStackSupportZero(ctx,5,1,AFSCoadd(1,[AFSCoboundary(ctx,"U1s",x.v),AFSComul(1,-1,O)])));
Print("INFINITE_DIHEDRAL_EVEN_PIP_FLAT_LIFT_PASS\n");
QUIT_GAP(0);
