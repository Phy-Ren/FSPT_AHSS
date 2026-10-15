U1_ROOT:="/home/xingyu/AllFSPT_reviews/u1_half_phase_20261015/candidate";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
G:=Group((1,2,3,4),(2,4));;els:=Elements(G);;one:=Identity(G);;
C2:=Group((1,2));;mr:=GroupHomomorphismByImages(G,C2,[(1,2,3,4),(2,4)],[(1,2),Identity(C2)]);;
ms:=GroupHomomorphismByImages(G,C2,[(1,2,3,4),(2,4)],[Identity(C2),(1,2)]);;
r:=function(g)if Image(mr,g)=Identity(C2) then return 0;else return 1;fi;end;;s:=function(g)if Image(ms,g)=Identity(C2) then return 0;else return 1;fi;end;;
c:=rec(G:=G,s:=s,rho:=r,omega:=function(g,h)return (s(g)*r(h))/2;end);;
checks:=0;;
for seed in [0,1,2] do
 q:=function(g,h,j)
  if one in [g,h,j] then return 0;fi;
  return (Position(els,g)+2*Position(els,h)+Position(els,h)*Position(els,j)+seed) mod 5-2;
 end;;
 fast:=U1ClosedChargeSource3Lazy(c,q);;
 w:=function(g,h)return 2*c.omega(g,h);end;;
 generic:=U1Add(U1Cup(c,2,w,"F2",3,q,"F2",0,true),U1Cup(c,3,q,"F2",3,q,"F2",1,true));;
 for xs in Tuples(els,5) do
  if U1Mod1(CallFuncList(generic,xs)/2)<>CallFuncList(fast,xs) then Error("Nonabelian lazy source disagreement");fi;
  checks:=checks+1;
 od;
od;
Print("LAZY_NONABELIAN_NEGATIVE_INTEGER_CHECKS ",checks,"\n");;
# Half-valued transfer must agree with the original full signed evaluator,
# retaining negative/even chain coefficients and group action differences.
halfChecks:=0;;ident:=fail;;es:=[];;
for args in [[2,0,0,0],[2,1,0,1/2],[4,1,1,1/2],[3,0,0,1/3]] do
 c:=CallFuncList(U1CyclicContext,args);;es:=Elements(c.G);;ident:=Identity(c.G);;
 f:=function(xs...)
  if ident in xs then return 0;fi;
  return ((Sum(List([1..Length(xs)],i->i*Position(es,xs[i]))) mod 5)-2)/2;
 end;;
 for k in [2..5] do
  if U1Native(c,k,"U1s",f)<>U1NativeHalfPhase(c,k,f) then Error("Signed half phase native mismatch");fi;
  if U1Native(c,k,"U1s",f)<>U1NativeHalfPhaseSmith(c,k,f) then Error("Half phase Smith native mismatch");fi;
  halfChecks:=halfChecks+2;
 od;
od;
Print("HALF_NATIVE_AND_SMITH_CHECKS ",halfChecks,"\n");;
QUIT_GAP(0);
