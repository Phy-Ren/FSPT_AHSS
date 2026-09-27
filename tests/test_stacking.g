AFS_ROOT:=".";;
AFS_STACK_AUDIT:=true;;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/formula_data.g");;
Read("gap/formulas.g");;
Read("gap/stacking.g");;

# Correlated images must be treated with one joint Smith presentation.
same:=[[2,0,0,0],[0,2,0,0],[-1,0,2,0],[-1,0,0,2]];;
independent:=[[2,0,0,0],[0,2,0,0],[-1,0,2,0],[0,-1,0,2]];;
s:=AFSSmith(same,4,4);;
Assert(0,Filtered(List(s.diag,AbsInt),x->x>1)=[2,2,4]);
s:=AFSSmith(independent,4,4);;
Assert(0,Filtered(List(s.diag,AbsInt),x->x>1)=[4,4]);
solve:=AFSStackLatticeSolver([[2,0],[1,2]],2);;
x:=solve([4,4]);;Assert(0,x*[[2,0],[1,2]]=[4,4]);
Assert(0,solve([1,1])=fail);

# Missing bosonic carry can be irrelevant to the abstract upper extension.
lower:=rec(generators:=[rec(),rec()],presentation:=[[2,0],[-1,2]]);;
lower.smith:=AFSSmith(lower.presentation,2,2);;
family:=AFSStackExtensionByTwo(lower,[0,1],[1]);;
Assert(0,family.status="computed" and family.invariants=[8]);
Assert(0,family.enumeratedExtensionClasses=0);
# A surviving bosonic ambiguity can also leave the type fixed if the known
# component has a strictly larger 2-adic cyclic order.
lower:=rec(generators:=[rec(),rec()],presentation:=[[2,0],[0,4]]);;
lower.smith:=AFSSmith(lower.presentation,2,2);;
family:=AFSStackExtensionByTwo(lower,[0,1],[1]);;
Assert(0,family.status="computed" and family.invariants=[2,8]);
# When it matters, preserve BOTH possible groups instead of selecting zero.
lower:=rec(generators:=[rec()],presentation:=[[2]]);;
lower.smith:=AFSSmith(lower.presentation,1,1);;
family:=AFSStackExtensionByTwo(lower,[0],[1]);;
Assert(0,family.status="ambiguous" and Set(family.invariantOptions)=Set([[2,2],[4]]));

# An actual infinite space group: Gamma=P1=Z^3. The supplied low-degree
# formulas and native resolution independently compute its entire p+ip=0
# extension. The three free p+ip factors are outside this cochain test.
ctx:=AFSBackend(1);;
Print("STACKING_STAGE backend\n");
h2:=AFSCohomology(ctx,2,"F2");;
h3:=AFSCohomology(ctx,3,"F2");;
h4:=AFSCohomology(ctx,4,"U1s");;
Print("STACKING_STAGE cohomology\n");
Assert(0,Length(h2.orders)=3 and Length(h3.orders)=1 and h4.orders=[]);
data:=rec(boson:=[],fermion:=[],majorana:=[],fermionBoundaries:=[],
  bosonBoundaries:=[],finalFiltrationCertificate:=rec(
    method:="P1-vcd3",H4U1:=[],H5U1:=[],orientation:=0));;
for i in [1..Length(h3.generators)] do
  Print("STACKING_STAGE liftCF ",i,"\n");
  lifted:=AFSStackLift(ctx,1,AFSBar(ctx,3,"F2",h3.generators[i]));;
  Assert(0,lifted.status="computed");
  Add(data.fermion,rec(name:=Concatenation("C",String(i)),layer:=1,order:=2,state:=lifted.state));
od;
for i in [1..Length(h2.generators)] do
  Print("STACKING_STAGE liftMC ",i,"\n");
  lifted:=AFSStackLift(ctx,2,AFSBar(ctx,2,"F2",h2.generators[i]));;
  Assert(0,lifted.status="computed");
  Add(data.majorana,rec(name:=Concatenation("B",String(i)),layer:=2,order:=2,state:=lifted.state));
od;
model:=AFSStackModel(ctx,data);;
Print("STACKING_STAGE model\n");
result:=AFSStackClassification(model);;
Assert(0,result.status="computed");
Assert(0,result.invariants=[2,2,2,2]);
Assert(0,result.enumeratedPhaseProducts=0);
Print("STACKING_TESTS_PASS ",result.invariants,"\n");
QUIT_GAP(0);
