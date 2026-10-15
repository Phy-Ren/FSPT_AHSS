OnBreak:=function() Where(10);QUIT_GAP(1);end;;
U1_ROOT:="/home/xingyu/FSPT_AHSS_insulator";;Read(Concatenation(U1_ROOT,"/gap/load.g"));
for entry in [[3,[3,3]],[5,[5,5]],[6,[3,12]],[9,[9,9]]] do
 n:=entry[1];;c:=U1CyclicContext(n,0,0,0);;r:=U1Classify(c,2);;
 if r.torsion<>entry[2] or r.freeRank<>0 then Error("Odd-primary cyclic extension");fi;
 a:=c.classificationStates.charge[1];;
 cancel:=U1Product(c,2,a,U1Inverse(c,2,a));;
 HP:=U1Cohomology(c,3,"U1s");;
 if ForAny(HP.coordinates(U1Native(c,3,"U1s",U1ReduceVacuum(c,2,cancel))),x->x<>0) then Error("Complete charge inverse");fi;
 order:=Maximum(r.torsion);;root:=U1Power(c,2,a,order);;
 if ForAny(HP.coordinates(U1Native(c,3,"U1s",U1ReduceVacuum(c,2,root))),x->x<>0) then Error("Complete mixed-primary root power");fi;
 Print("CYCLIC_",n,"=",r.torsion,";complete_inverse_and_power=PASS\n");
od;
QUIT_GAP(0);
