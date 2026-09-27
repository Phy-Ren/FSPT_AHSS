AFS_ROOT:=".";;
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/backend_diagonal.g");;
Read("gap/classification.g");;
Read("gap/formula_data.g");;
Read("gap/formulas.g");;
Read("gap/stacking.g");;
Read("gap/crystalline_background.g");;
Read("gap/pip_incoming_background.g");;

# Every source equation is evaluated on actual infinite-affine comparison
# supports. Doubles are compared with the literal general-w CA product.
incoming:=fail;;
for number in [3,16,75,143] do
  ctx:=AFSBackend(number);;bg:=AFSInstallCrystallineBackground(ctx);;
  incoming:=AFSBackgroundIncomingPowers(ctx);;
  for state in incoming.powers do
    dA:=AFSCoboundary(ctx,"F2",state.a);;
    Assert(0,ForAll(AFSNative(ctx,3,"F2",dA),x->x=0));
    Q:=AFSFormula("majorana_source",ctx,rec(p:=2,a:=state.a,w:=ctx.omega2));;
    dC:=AFSCoboundary(ctx,"F2",state.c);;
    Assert(0,ForAll(AFSNative(ctx,4,"F2",AFSCoadd(2,[dC,Q])),x->x=0));
    O:=AFSFormula("obstruction",ctx,rec(p:=2,a:=state.a,c:=state.c,w:=ctx.omega2));;
    dV:=AFSCoboundary(ctx,"U1s",state.v);;
    Assert(0,ForAll(AFSNative(ctx,5,"U1s",AFSCoadd(1,[dV,AFSComul(1,-1,O)])),x->x=0));
  od;
  for power in [1..4] do
    product:=AFSStackProduct(ctx,incoming.powers[power],incoming.powers[power]);;
    expected:=incoming.powers[power+1];;
    for component in [["a",2,"F2",2],["c",3,"F2",2],["v",4,"U1s",1]] do
      difference:=AFSCoadd(component[4],[product.(component[1]),AFSComul(component[4],-1,expected.(component[1]))]);;
      Assert(0,ForAll(AFSNative(ctx,component[2],component[3],difference),x->x=0));
    od;
  od;
  dEta:=AFSCoboundary(ctx,"U1s",incoming.quadruplePhaseGauge3);;
  canonical4:=AFSMemo(function(xs...) return AFSMod1(-CallFuncList(incoming.pontryagin4,xs)/4);end);;
  Assert(0,ForAll(AFSNative(ctx,4,"U1s",AFSCoadd(1,[incoming.powers[3].v,AFSComul(1,-1,canonical4),dEta])),x->x=0));
  Print("PIP_INCOMING_NATIVE_PASS ",number,"\n");
od;
Print("PIP_INCOMING_BACKGROUND_TEST_PASS\n");
QUIT_GAP(0);
