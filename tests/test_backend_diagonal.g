AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_diagonal.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));;
if not IsBound(AFS_SG) then AFS_SG:=2; fi;
c:=AFSBackend(AFS_SG);;
for p in [2,3] do
  H:=AFSCohomology(c,p,"F2");; T:=AFSCohomology(c,p+2,"U1s");;
  Print("DIAGONAL_TEST ",AFS_SG," p=",p," count=",Length(H.generators),"\n");
  for a in H.generators do
    native:=AFSNativeSq2(c,p,a)/2;;
    f:=AFSBar(c,p,"F2",a);;
    phase:=AFSFormula("obstruction",c,rec(p:=p-1,a:=AFSZero,c:=f));;
    expected:=AFSNative(c,p+2,"U1s",phase);;
    x:=T.coordinates(native);; y:=T.coordinates(expected);;
    if x=fail or y=fail or x<>y then
      Print("BAD ",x," ",y,"\n"); Error("native versus bar square mismatch");
    fi;
    TF:=AFSCohomology(c,p+2,"F2");;
    if TF.coordinates(2*native)<>TF.coordinates(2*expected) then
      Error("native versus bar square F2 mismatch");
    fi;
  od;
od;
H:=AFSCohomology(c,2,"F2");; T:=AFSCohomology(c,4,"F2");;
svec:=AFSNative(c,1,"F2",c.s);;
for a in H.generators do
  beta:=(a*AFSDifferential(c,2,"Z"))/2;;
  if not ForAll(beta,IsInt) then Error("nonintegral ordinary Bockstein"); fi;
  native:=AFSNativeCup(c,0,2,a,2,a)+AFSNativeCup(c,0,1,svec,3,beta);;
  native:=List(native,x->x mod 2);;
  f:=AFSBar(c,2,"F2",a);;
  expected:=AFSNative(c,4,"F2",AFSFormula("majorana_source",c,rec(p:=2,a:=f)));;
  if T.coordinates(native)<>T.coordinates(expected) then Error("native MC Bockstein map mismatch"); fi;
od;
Print("AFS_DIAGONAL_TEST_PASS ",AFS_SG,"\n");
QUIT_GAP(0);
