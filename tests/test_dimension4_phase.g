# Test generated GAP arithmetic against fresh Python/API fixtures.
OnBreak:=function() Where(12);QUIT_GAP(1);end;;
for p in [1,2] do
  for z in ["zero","full"] do
    Read(Concatenation(AFS_ROOT,"/gap/dimension4_phase_p",String(p),"_",z,".g"));
  od;
od;
Read(AFS_CASES);;
MakeField:=function(data)
  return function(args...)
    local f,a,pos;
    f:=[args[1][1]];
    for a in args do Add(f,a[2]);od;
    pos:=PositionProperty(data,x->x[1]=f);
    if pos=fail then Error("Missing complete fixture face ",f);fi;
    return data[pos][2];
  end;
end;;
for case in AFSD4PhaseCases do
  p:=case[1];
  name:=Concatenation("AFSD4PhaseP",String(p));
  if case[2]=1 then name:=Concatenation(name,"ZeroProgram");
  else name:=Concatenation(name,"FullProgram");fi;
  fields:=rec();
  for i in [1..5] do fields.(["n","b","c","w","s"][i]):=MakeField(case[4][i]);od;
  t:=List([1..p+5],i->List([1..p+5],j->[i-1,j-1]));
  value:=CallFuncList(ValueGlobal(name),[fields,t]);
  if value<>case[3]/16 then Error("Compiled GAP phase mismatch ",case[1]," ",case[2]);fi;
od;
Print("PASS ",Length(AFSD4PhaseCases)," exact GAP phase fixtures\n");
QUIT_GAP(0);
