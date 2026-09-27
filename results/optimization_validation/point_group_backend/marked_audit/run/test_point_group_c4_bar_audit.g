# Exhaustive finite C4 control. The frozen mathematical source is supplied
# through AFS_ROOT. No reference answer or affine space-group result is read.
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
if not IsBound(AFS_ROOT) or not IsBound(AFS_TEST_OUT) then
  Error("AFS_ROOT and AFS_TEST_OUT are required");
fi;
AFS_STACK_AUDIT:=true;;
AFS_USE_MOD2_CONTRACTION:=false;;
AFS_USE_MOD2_BAR:=false;;
AFS_USE_CLOSED_CF_OBSTRUCTION:=false;;
AFSUseFastFormulas:=false;;
AFSUseGeneralPipO5:=true;;
for AFS_FILE in ["backend.g","backend_mod2_contraction.g","backend_diagonal.g",
    "class_coordinates.g","formula_data.g","pip_o5_program.g","formulas.g",
    "formula_fast.g","pip_o5_sign.g","pip_o5_general.g","classification.g",
    "pip.g","point_group_backend.g","crystalline_background.g",
    "background_native_cup.g","background_operations.g","pip_o5_background.g",
    "pip_o5_background_even.g","pip_o5_background_sign.g","stacking.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",AFS_FILE));
od;

AFSC4BarAudit:=function()
  local ctx,C,model,lower,elements,counts,checkZero,checkFlat,x,y,power,literal,
    g,reduced,combined,relations,out,stream,i;
  ctx:=AFSPointGroupBackend(10);ctx.crystallineSpin:="spinless";
  ctx.useBackgroundNativeCup:=false;
  AFSInstallPointGroupBackground(ctx);AFSReducePointGroupBackground(ctx);
  C:=AFSClassify(ctx);
  model:=AFSStackFromClassification(C);
  if model.status<>"computed" then Error("full bar lower model incomplete");fi;
  lower:=AFSStackClassification(model);
  if lower.status<>"computed" then Error("full bar lower relations incomplete");fi;
  elements:=Filtered(Elements(ctx.G),g->g<>Identity(ctx.G));
  if Length(elements)<>3 then Error("this control requires actual finite C4");fi;
  counts:=rec(degree2:=0,degree3:=0,degree4:=0,degree5:=0);
  checkZero:=function(k,modulus,f)
    local tuple,value,key;
    key:=Concatenation("degree",String(k));
    for tuple in Tuples(elements,k) do
      value:=CallFuncList(f,tuple);
      if modulus=1 then value:=AFSMod1(value);else value:=value mod modulus;fi;
      if value<>0 then Error("exhaustive normalized bar equality failed at degree ",k);fi;
      counts.(key):=counts.(key)+1;
    od;
  end;
  checkFlat:=function(state)
    local source,op;
    checkZero(3,2,AFSCoboundary(ctx,"F2",state.a));
    source:=AFSFormula("majorana_source",ctx,rec(p:=2,a:=state.a));
    checkZero(4,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",state.c),source]));
    op:=AFSFormula("obstruction",ctx,rec(p:=2,a:=state.a,c:=state.c));
    checkZero(5,1,AFSCoadd(1,[AFSCoboundary(ctx,"U1s",state.v),AFSComul(1,-1,op)]));
  end;
  for g in model.generators do checkFlat(g.state);od;
  for x in model.generators do
    for y in model.generators do
      checkFlat(AFSStackProduct(ctx,x.state,y.state));
    od;
  od;
  relations:=[];
  for g in model.generators do
    if g.order<>2 then Error("control expects order-two graded generators");fi;
    literal:=AFSStackProduct(ctx,g.state,g.state);
    power:=AFSStackPower(ctx,g.state,2);
    checkZero(2,2,AFSCoadd(2,[power.a,literal.a]));
    checkZero(3,2,AFSCoadd(2,[power.c,literal.c]));
    checkZero(4,1,AFSCoadd(1,[power.v,AFSComul(1,-1,literal.v)]));
    reduced:=AFSStackReduce(model,literal,g.layer=2);
    if reduced.status<>"computed" then Error("literal square relation unresolved");fi;
    combined:=AFSStackProduct(ctx,reduced.witness.boundary,reduced.witness.canonical);
    checkZero(3,2,AFSCoadd(2,[literal.c,combined.c]));
    checkZero(4,1,AFSCoadd(1,[literal.v,AFSComul(1,-1,combined.v)]));
    Add(relations,rec(generator:=g.name,coordinates:=reduced.coordinates));
  od;
  out:=AFSStackExport(C,rec(status:="computed",lower:=lower));
  out.point_group:=AFSPointGroupExport(ctx);out.checks:=counts;
  out.literalSquareCoordinates:=relations;
  out.options:=rec(stackAudit:=true,closedCF:=false,mod2Contraction:=false,
    mod2Bar:=false,compiledCA:=false,backgroundProjectedCup0:=false);
  out.scope:="Full bar lower model; exhaustive equality on all nondegenerate finite C4 tuples through degree five, with normalized callbacks. No reference answers used.";
  LoadPackage("json");stream:=OutputTextFile(AFS_TEST_OUT,false);
  SetPrintFormattingStatus(stream,false);PrintTo(stream,GapToJsonString(out),"\n");
  CloseStream(stream);Print("AFS_C4_BAR_AUDIT_PASS ",counts,"\n");
end;;
AFSC4BarAudit();
QUIT_GAP(0);
