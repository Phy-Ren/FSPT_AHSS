Read("gap/formula_data.g");;
Read("gap/formula_fast.g");;
Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;
Read("tests/formula_cases.g");;
_AFTestGroup:=AbelianGroup(IsPcGroup,[256]);;
_AFTestGen:=GeneratorsOfGroup(_AFTestGroup)[1];;
_AFFixtureCallback:=function(rows)
  local keys,values;
  keys:=List(rows,r->List(r[1],k->_AFTestGen^k));values:=List(rows,r->r[2]);
  return function(xs...)
    local i;i:=Position(keys,xs);if i=fail then return 0;fi;return values[i];
  end;
end;;
for case in AFSFormulaCases do
  input:=rec(p:=case[2]);;
  for field in case[6] do
    if field[1]<>"w" or ForAny(field[2],row->row[2]<>0) then
      input.(field[1]):=_AFFixtureCallback(field[2]);
    fi;
  od;
  ctx:=rec(G:=_AFTestGroup,s:=input.s);;
  callback:=AFSFormula(case[1],ctx,input);;
  actual:=CallFuncList(callback,List([0..case[3]-1],i->_AFTestGen^(2^i)));;
  if actual<>case[5]/case[4] then
    Print("FAIL ",case[1]," p=",case[2]," expected ",case[5]/case[4]," got ",actual,"\n");
    QUIT_GAP(1);
  fi;
  AFSUseFastFormulas:=false;;
  reference:=AFSFormula(case[1],ctx,input);;
  if CallFuncList(reference,List([0..case[3]-1],i->_AFTestGen^(2^i)))<>actual then
    Error("Compiled/reference formula discrepancy");
  fi;
  AFSUseFastFormulas:=true;;
od;
Print("PASS ",Length(AFSFormulaCases)," exact cross-language formula fixtures\n");
QUIT_GAP(0);
