AFSMemo:=f->f;;AFSZero:=function(arg...)return 0;end;;
AFSMod1:=x->(NumeratorRat(x) mod DenominatorRat(x))/DenominatorRat(x);;
Read("gap/formula_data.g");;
Read("gap/formula_fast.g");;
Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;
Read("gap/pip_coordinate_data.g");;
Read("gap/pip_coordinates.g");;
Read("tests/pip_coordinate_cases.g");;
AFCoordGroup:=AbelianGroup(IsPcGroup,[256]);;AFCoordGen:=GeneratorsOfGroup(AFCoordGroup)[1];;
Fixture:=function(rows)
 local keys,values;
 keys:=List(rows,r->List(r[1],k->AFCoordGen^k));values:=List(rows,r->r[2]);
 return function(xs...)
  local i;i:=Position(keys,xs);if i=fail then return 0;fi;return values[i];
 end;
end;;
for case in AFSPipCoordinateCases do
 f:=rec();;
 for field in case[4] do f.(field[1]):=Fixture(field[2]);od;
 ctx:=rec(G:=AFCoordGroup,s:=f.s);;
 if case[1]=0 then callback:=AFSPipIntegerGaugePhase(ctx,f.c);
 elif case[1]=2 then callback:=AFSPipPhaseReferenceShift(ctx,2,AFSZero,f.c);
 else callback:=AFSPipPhaseReferenceShift(ctx,1,f.b,f.c);fi;
 actual:=CallFuncList(callback,List([0..3],i->AFCoordGen^(2^i)));;
 if actual<>case[2]/case[3] then Error("Unary GAP/Python discrepancy ",case[1],actual,case[2]/case[3]);fi;
od;
Print("PASS ",Length(AFSPipCoordinateCases)," exact unary GAP/Python coordinate fixtures\n");
QUIT_GAP(0);
