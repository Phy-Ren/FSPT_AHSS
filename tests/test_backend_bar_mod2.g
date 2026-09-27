if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_bar_mod2.g"));;
if not IsBound(AFS_SG) then AFS_SG:=29;fi;
c:=AFSBackend(AFS_SG);; gs:=GeneratorsOfGroup(c.G);;
elts:=Concatenation(gs,List(gs,g->g^-1),[gs[1]^2,gs[1]*gs[Length(gs)],gs[Length(gs)]^-2]);;
count:=0;;t0:=Runtime();;
for k in [1..4] do
  for j in [1..6] do
    xs:=List([1..k],i->elts[1+((3*j+i^2) mod Length(elts))]);;
    a:=AFSChainFromBar(c.bar,xs);;b:=AFSChainFromBarMod2(c.bar,xs);;
    if AFSMod2NativeReduce(Concatenation(a,b))<>[] then Error("full translated G words differ");fi;
    count:=count+1;
  od;
od;
Print("MOD2_G_TRANSLATED_PASS sg=",AFS_SG," cases=",count," cpu_ms=",Runtime()-t0,"\n");
for k in [1..3] do
  v:=List([1..Dimension(c.R)(k)],i->(i^2+QuoInt(i,3)) mod 2);;
  old:=AFSBar(c,k,"F2",v);;new:=AFSBarMod2(c,k,v);;
  if AFSNative(c,k,"F2",old)<>AFSNative(c,k,"F2",new) then Error("full native G pullback vectors differ");fi;
od;
Print("MOD2_G_NATIVE_VECTOR_PASS sg=",AFS_SG,"\n");
psi:=function(g,h)
  if g=Identity(c.G) or h=Identity(c.G) then return 0;fi;
  return (Sum(g!.exponents)^2*Sum(h!.exponents)+Sum(h!.exponents)^3) mod 2;
end;;
f:=AFSCoboundary(c,"F2",psi);;v:=AFSSolveNative(c,3,"F2",AFSNative(c,3,"F2",f));;
if v=fail then Error("known F2 boundary has no native primitive");fi;
bf:=AFSBarMod2(c,2,v);;hf:=AFSHomotopyPullback(c.bar,"F2",f);;
primitive:=function(xs...) return (CallFuncList(bf,xs)-CallFuncList(hf,xs)) mod 2;end;;
df:=AFSCoboundary(c,"F2",primitive);;
for j in [1..18] do
  xs:=List([1..3],i->elts[1+((5*j+i^2) mod Length(elts))]);;
  if CallFuncList(df,xs)<>CallFuncList(f,xs) then Error("mod2 G exact bar primitive identity");fi;
od;
Print("AFS_MOD2_G_TEST_PASS sg=",AFS_SG," total_cpu_ms=",Runtime()-t0,"\n");
QUIT_GAP(0);
