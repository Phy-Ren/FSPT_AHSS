OnBreak:=function() Where(25);QUIT_GAP(1);end;;
if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));;
Read(Concatenation(AFS_ROOT,"/gap/pip_o5_program.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));;
Read(Concatenation(AFS_ROOT,"/gap/pip_o5_sign.g"));;
Read(Concatenation(AFS_ROOT,"/gap/pip_o5_general.g"));;
Read(Concatenation(AFS_ROOT,"/tests/pip_general_cases.g"));;
if AFSPipGeneralCasesSourceSha256<>AFSPipO5GeneralSourceSha256 then Error("generic fixture/source hash mismatch");fi;
G:=AbelianGroup(IsPcGroup,[256]);;g:=GeneratorsOfGroup(G)[1];;
Fixture:=function(rows)
 local keys,values;keys:=List(rows,r->List(r[1],k->g^k));values:=List(rows,r->r[2]);
 return function(xs...)local i;i:=Position(keys,xs);if i=fail then return 0;fi;return values[i];end;
end;;
args:=List([0..4],i->g^(2^i));;compiled:=[];;interpreted:=[];;
AFSUseSignPipO5:=false;;
for case in AFSPipGeneralCases do
 f:=rec(p:=1);;for field in case[2] do f.(field[1]):=Fixture(field[2]);od;
 ctx:=rec(G:=G,s:=f.s);;
 AFSUseGeneralPipO5:=true;;fn:=AFSPipO5(ctx,f);;
 actual:=CallFuncList(fn,args);;
 AFSUseGeneralPipO5:=false;;ref:=AFSPipO5(ctx,f);;
 expected:=CallFuncList(ref,args);;
 if actual<>expected or actual<>case[1]/16 then Error("generic compiled/interpreter/scalar-graph mismatch");fi;
 Add(compiled,fn);Add(interpreted,ref);
od;
# Sign specialization retains priority when both compiled runners are loaded.
f:=rec(p:=1);;for field in AFSPipGeneralCases[2][2] do f.(field[1]):=Fixture(field[2]);od;
f.n:=f.s;;ctx:=rec(G:=G,s:=f.s);;
AFSUseSignPipO5:=true;;AFSUseGeneralPipO5:=true;;
saved:=AFSPipO5GeneralProgram;;
AFSPipO5GeneralProgram:=function(f,t)Error("generic dispatch bypassed sign specialization");end;;
fn:=AFSPipO5(ctx,f);;signValue:=CallFuncList(fn,args);;
AFSPipO5GeneralProgram:=saved;;AFSUseSignPipO5:=false;;
# Every field must remain normalized on internal identity increments.
G2:=AbelianGroup(IsPcGroup,[2]);;g2:=GeneratorsOfGroup(G2)[1];;
badZero:=function(xs...)if ForAny(xs,x->x=One(G2)) then return 23;fi;return 0;end;;
f:=rec(p:=1,n:=badZero,b:=badZero,c:=badZero,s:=badZero);;ctx:=rec(G:=G2,s:=badZero);;
AFSUseGeneralPipO5:=true;;fn:=AFSPipO5(ctx,f);;
AFSUseGeneralPipO5:=false;;ref:=AFSPipO5(ctx,f);;
for xs in [[g2,g2,g2,g2,g2],[One(G2),g2,g2,g2,g2]] do
 if CallFuncList(fn,xs)<>0 or CallFuncList(ref,xs)<>0 then Error("normalization guard mismatch");fi;
od;
# Repeat uncached callbacks, timing arithmetic and field lookup in both paths.
t:=Runtime();;sumFast:=0;;
for iteration in [1..5] do for fn in compiled do sumFast:=sumFast+CallFuncList(fn,args);od;od;
fastMs:=Runtime()-t;;t:=Runtime();;sumSlow:=0;;
for iteration in [1..5] do for fn in interpreted do sumSlow:=sumSlow+CallFuncList(fn,args);od;od;
slowMs:=Runtime()-t;;
if sumFast<>sumSlow then Error("benchmark outputs differ");fi;
Print("GENERIC_O5_CPU_MS compiled=",fastMs," interpreted=",slowMs," calls=",5*Length(compiled),"\n");
Print("PASS ",Length(compiled)," exact generic O5 GAP/interpreter/scalar-graph fixtures, negative integers and normalized identity guards\n");
QUIT_GAP(0);
