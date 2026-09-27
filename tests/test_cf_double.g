AFS_ROOT:=".";;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/backend_diagonal.g");;
Read("gap/formula_data.g");;
Read("gap/formula_fast.g");;
Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;
Read("gap/classification.g");;
Read("gap/pip.g");;
Read("gap/stacking.g");;
ctx:=AFSBackend(11);;C:=AFSClassify(ctx);;
f:=AFSCombination(ctx,3,"F2",C.H3,C.cfFinalBasis[1]);;
x:=AFSStackLift(ctx,1,f).state;;
Assert(0,AFSCoadd(2,[f,AFSZero,f])=AFSZero);
Assert(0,AFSCoadd(1,[AFSZero,AFSZero])=AFSZero);
Assert(0,AFSComul(1,0,f)=AFSZero);
# Compare exact identity/bosonic translations to the unsimplified supplied
# CA polynomial, so the test does not compare the shortcut to itself.
bos:=AFSStackZero();;
bos.v:=AFSBar(ctx,4,"U1s",C.H4U.generators[1]);;
off:=AFSStackZero();;
raw:=List([1..Dimension(ctx.R)(3)],i->i mod 2);;
off.c:=AFSBar(ctx,3,"F2",raw);;
for pair in [[AFSStackZero(),x],[x,AFSStackZero()],[bos,x],[x,bos],
             [x,x],[off,x],[x,off],[off,off]] do
  simplified:=AFSStackProduct(ctx,pair[1],pair[2]);;
  correction:=AFSFormula("stacking",ctx,rec(p:=2,a:=pair[1].a,c:=pair[1].c,
    b:=pair[2].a,cp:=pair[2].c));;
  expected:=AFSCoadd(1,[pair[1].v,pair[2].v,correction]);;
  Assert(0,AFSStackSupportZero(ctx,4,1,AFSCoadd(1,[simplified.v,AFSComul(1,-1,expected)])));
od;
fast:=AFSStackPower(ctx,x,2);;
literal:=AFSStackProduct(ctx,x,x);;
Assert(0,AFSStackSupportZero(ctx,4,1,AFSCoadd(1,[fast.v,AFSComul(1,-1,literal.v)])));
co:=C.H4U.coordinates(AFSNative(ctx,4,"U1s",fast.v));;
Assert(0,C.bosQuotient.project(co)=[1]);
Print("SAME_MARKED_CF_DOUBLE_PASS SG11 nonzero bosonic carry\n");
QUIT_GAP(0);
