# Exact scalar controls only: no space-group construction or classification.
AFS_SPECIALIZE_ROOT:=GAPInfo.SystemEnvironment.AFS_SPECIALIZE_ROOT;;
Read(Concatenation(AFS_SPECIALIZE_ROOT,"/pip_o5_background.g"));
Read(Concatenation(AFS_SPECIALIZE_ROOT,"/pip_o5_background_even.g"));
Read(Concatenation(AFS_SPECIALIZE_ROOT,"/pip_o5_background_sign.g"));
Read(Concatenation(AFS_SPECIALIZE_ROOT,"/cases.g"));

AFSBackgroundSpecializeTest:=function()
  local field,prepare,t,cases,case,fields,full,fast,counts,choice,start,
    timing,index,iteration;
  field:=function(rows)
    local dict,row;
    dict:=NewDictionary([1],true);
    for row in rows do AddDictionary(dict,row[1],row[2]);od;
    return function(xs...) return LookupDictionary(dict,xs);end;
  end;
  prepare:=function(rows)
    local f,row;f:=rec();
    for row in rows do f.(row[1]):=field(row[2]);od;
    return f;
  end;
  t:=List([0..5],i->List([0..5],function(j)
    if j<=i then return 0;fi;return 2^j-2^i;
  end));
  cases:=List(AFSBackgroundSpecializationCases,x->[x[1],x[2],prepare(x[3])]);
  if IsBound(GAPInfo.SystemEnvironment.AFS_SPECIALIZE_ODD) then
    fields:=cases[1][3];fields.n:=function(xs...) return -3;end;
    AFSPipO5BackgroundEvenProgram(fields,t);
    Error("Odd precondition failure was accepted");
  fi;
  counts:=[0,0];
  for case in cases do
    fields:=case[3];full:=AFSPipO5BackgroundProgram(fields,t);
    if case[1]="even" then fast:=AFSPipO5BackgroundEvenProgram(fields,t);index:=1;
    else fast:=AFSPipO5BackgroundSignProgram(fields,t);index:=2;fi;
    if full<>case[2]/16 or fast<>full then Error("Specialized GAP / full GAP / original oracle mismatch");fi;
    counts[index]:=counts[index]+1;
  od;
  for choice in ["even","sign"] do
    timing:=[0,0];
    for iteration in [1..3] do
      for index in (function() if iteration mod 2=0 then return [2,1];else return [1,2];fi;end)() do
        start:=Runtime();
        for case in cases do
          if case[1]<>choice then continue;fi;
          if index=1 then full:=AFSPipO5BackgroundProgram(case[3],t);
          elif choice="even" then full:=AFSPipO5BackgroundEvenProgram(case[3],t);
          else full:=AFSPipO5BackgroundSignProgram(case[3],t);fi;
        od;
        timing[index]:=timing[index]+Runtime()-start;
      od;
    od;
    Print("AFS_BACKGROUND_SPECIALIZATION_TIMING mode=",choice," full_ms=",timing[1],
      " specialized_ms=",timing[2]," loops=3 cases=64\n");
  od;
  if counts<>[64,64] then Error("Incomplete specialization fixture coverage");fi;
  Print("AFS_BACKGROUND_SPECIALIZATION_GAP_PASS even=",counts[1]," sign=",counts[2],"\n");
end;;
AFSBackgroundSpecializeTest();
QUIT_GAP(0);
