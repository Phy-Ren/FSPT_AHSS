# Genuine secondary additivity after quotienting the primary image.
# Lower primitives for the sum are solved afresh, not obtained by stacking.
Read("gap/backend.g");;
Read("gap/formula_data.g");;
Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;
Read("gap/classification.g");;
checks:=0;;
for sg in [35,47] do
  C:=AFSClassify(AFSBackend(sg));;ctx:=C.ctx;;
  lim:=Minimum(3,Length(C.mcPrimaryKernel));;
  for i in [1..lim] do
    for j in [i..lim] do
      basis:=List(C.mcPrimaryKernel[i]+C.mcPrimaryKernel[j],x->x mod 2);;
      a:=AFSCombination(ctx,2,"F2",C.H2,basis);;
      source:=AFSFormula("majorana_source",ctx,rec(p:=2,a:=a));;
      c:=AFSSolve(ctx,4,"F2",source);;
      if c=fail then Error("sum of primary-kernel classes failed to lift");fi;
      O:=AFSFormula("obstruction",ctx,rec(p:=2,a:=a,c:=c));;
      value:=C.H5U.coordinates(AFSNative(ctx,5,"U1s",O));;
      if value=fail then Error("secondary sum is not closed");fi;
      actual:=C.secondaryTarget.project(value);;
      expected:=C.mcSecondaryRows[i]+C.mcSecondaryRows[j];;
      for k in [1..Length(actual)] do
        if C.secondaryTarget.orders[k]<>0 then expected[k]:=expected[k] mod C.secondaryTarget.orders[k];fi;
      od;
      if actual<>expected then Error("secondary additivity failed in quotient SG ",sg);fi;
      checks:=checks+1;
    od;
  od;
  Print("SECONDARY ADDITIVITY SG ",sg," target ",C.secondaryTarget.orders," checks ",checks,"\n");
od;
Print("PASS independently solved native secondary sums: ",checks,"\n");
QUIT_GAP(0);
