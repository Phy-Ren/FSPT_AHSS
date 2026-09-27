AFS_ROOT:=".";;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
Read("gap/backend.g");;
Read("gap/backend_diagonal.g");;
Read("gap/formula_data.g");;
Read("gap/pip_o5_program.g");;
Read("gap/formulas.g");;
Read("gap/classification.g");;
Read("gap/pip.g");;
Read("gap/stacking.g");;
sg:=Int(GAPInfo.SystemEnvironment.AFS_TEST_SG);;
ctx:=AFSBackend(sg);;
C:=AFSClassify(ctx);;
Print("STACKING_CLASSIFICATION_LAYERS ",sg," ",C.summary,"\n");
result:=AFSFullStacking(C);;
Print("STACKING_CLASSIFICATION_RESULT ",sg," ",result.status,"\n");
if result.status="computed" then
  Print("STACKING_CLASSIFICATION_INVARIANTS ",sg," ",result.invariants,"\n");
  Print("STACKING_CLASSIFICATION_PRESENTATION ",sg," ",result.lower.presentation,"\n");
  if sg=1 then Assert(0,result.invariants=[0,0,0,2,2,2,2]);fi;
else
  Print("STACKING_CLASSIFICATION_REASON ",result.reason,"\n");
fi;
LoadPackage("json");;
serialized:=GapToJsonString(AFSStackExport(C,result));;
Assert(0,Length(serialized)>0);
Print("STACKING_JSON_BYTES ",Length(serialized),"\n");
Print("STACKING_CLASSIFICATION_TEST_DONE ",sg,"\n");
QUIT_GAP(0);
