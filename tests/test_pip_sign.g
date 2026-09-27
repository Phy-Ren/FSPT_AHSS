OnBreak:=function() Where(25);QUIT_GAP(1);end;;
Read("gap/formula_data.g");;Read("gap/formula_fast.g");;Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;Read("gap/pip_o5_sign.g");;Read("tests/pip_sign_cases.g");;
AFSPipSignGroup:=AbelianGroup(IsPcGroup,[256]);;AFSPipSignGenerator:=GeneratorsOfGroup(AFSPipSignGroup)[1];;
Fixture:=function(rows)
 local keys,values;keys:=List(rows,r->List(r[1],k->AFSPipSignGenerator^k));values:=List(rows,r->r[2]);
 return function(xs...)local i;i:=Position(keys,xs);if i=fail then return 0;fi;return values[i];end;
end;;
for case in AFSPipSignCases do
 f:=rec(p:=1);;for field in case[2] do f.(field[1]):=Fixture(field[2]);od;
 f.n:=f.s;;ctx:=rec(G:=AFSPipSignGroup,s:=f.s);;
 AFSUseSignPipO5:=true;;fn:=AFSPipO5(ctx,f);;
 actual:=CallFuncList(fn,List([0..4],i->AFSPipSignGenerator^(2^i)));;
 if actual<>case[1]/16 then Error("Sign-specialized Python/GAP discrepancy");fi;
 AFSUseSignPipO5:=false;;fn:=AFSPipO5(ctx,f);;
 generic:=CallFuncList(fn,List([0..4],i->AFSPipSignGenerator^(2^i)));;
 if actual<>generic then Error("Sign-specialized/generic GAP discrepancy");fi;
od;
Print("PASS32 exact sign-specialized O5 GAP/generic/Python fixtures\n");
QUIT_GAP(0);
