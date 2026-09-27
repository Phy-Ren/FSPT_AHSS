# Full explicit upper relation, with every lower gauge checked on bar support.
AFS_ROOT:=".";;AFS_STACK_AUDIT:=true;;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/backend_diagonal.g");;
Read("gap/formula_data.g");;
Read("gap/formula_fast.g");;
Read("gap/pip_o5_program.g");;
Read("gap/pip_o5_sign.g");;
Read("gap/formulas.g");;
Read("gap/pip_coordinate_data.g");;
Read("gap/pip_coordinates.g");;
Read("gap/pip_diagonal_data.g");;
Read("gap/classification.g");;
Read("gap/pip.g");;
Read("gap/stacking.g");;
Read("gap/pip_stacking.g");;
sg:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(sg);;C:=AFSClassify(ctx);;
if C.summary.pip.status<>"computed" or not 2 in C.summary.pip.orders then
 Error("Review group must have a surviving torsion p+ip class");fi;
result:=AFSExplicitPipStacking(C);;
if result.status<>"computed" then Error("Actual marked upper relation failed: ",result.reason);fi;
x:=result.pipGenerator;;
if not AFSStackSupportZero(ctx,2,0,AFSCoboundary(ctx,"Zs",x.n)) then Error("integer lift equation");fi;
source:=AFSFormula("pip_majorana",ctx,rec(p:=1,n:=x.n));;
if not AFSStackSupportZero(ctx,3,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.b),source])) then Error("Majorana lift equation");fi;
source:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=x.n,b:=x.b));;
if not AFSStackSupportZero(ctx,4,2,AFSCoadd(2,[AFSCoboundary(ctx,"F2",x.c),source])) then Error("CF lift equation");fi;
source:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=x.n,b:=x.b,c:=x.c));;
if not AFSStackSupportZero(ctx,5,1,AFSCoadd(1,[AFSCoboundary(ctx,"U1s",x.v),AFSComul(1,-1,source)])) then Error("phase lift equation");fi;
if not AFSStackCheckFlat(ctx,result.pipSquare.target) then Error("actual square is not flat");fi;
if not result.pipReduction.witness.checkedComparisonSupport then Error("Missing full gauge-support check");fi;
Print("PASS_MARKED_PIP_REVIEW SG",sg," invariants=",result.invariants,
 " relation=",result.pipRelationCoordinates," MCadjust=",x.mcIndeterminacyAdjustment,
 " CFadjust=",x.cfIndeterminacyAdjustment,"\n");
QUIT_GAP(0);
