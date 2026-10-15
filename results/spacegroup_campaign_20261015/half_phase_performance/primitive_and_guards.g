U1_ROOT:="/home/xingyu/AllFSPT_reviews/u1_half_phase_20261015/candidate";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
primitiveChecks:=0;;nativeChecks:=0;;quarterPrimitives:=0;;c:=fail;;
for args in [[2,1,1,0],[2,1,0,1/2],[3,0,0,1/2],[4,1,1,1/2]] do
 c:=CallFuncList(U1CyclicContext,args);;els:=Filtered(Elements(c.G),g->g<>Identity(c.G));;
 for d in [2,3] do
  H:=U1Cohomology(c,d,"Zr");;vectors:=ShallowCopy(H.generators);;Append(vectors,U1Differential(c,d-1,"Zr"));;
  for v in vectors do
   for scale in [-3,1,2] do
    state:=U1CertifiedClosedChargeState(c,d,scale*v);;source:=U1Source(c,d,state);;
    a:=U1SolveData(c,d+2,"U1s",source);;b:=U1SolveCertifiedChargeData(c,d,state);;
    if (a=fail)<>(b=fail) then Error("Half phase solvability changed");fi;
    if a<>fail then
     if a.nativeObstruction<>b.nativeObstruction or a.nativePrimitive<>b.nativePrimitive then Error("Half phase native coordinates changed");fi;
     nativeChecks:=nativeChecks+1;
     if ForAny(b.nativePrimitive,x->DenominatorRat(x)=4) then quarterPrimitives:=quarterPrimitives+1;fi;
     for xs in Tuples(els,d+1) do
      if CallFuncList(a.primitive,xs)<>CallFuncList(b.primitive,xs) then Error("Integral homotopy correction changed");fi;
      primitiveChecks:=primitiveChecks+1;
     od;
    fi;
   od;
  od;
 od;
od;
# An exact non-half background does not receive the half-valued certificate.
c:=U1CyclicContext(3,0,0,1/3);;state:=U1CertifiedClosedChargeState(c,2,[1]);;
if IsBound(state.closedChargeSourceCertificate) then Error("Quarter/third background incorrectly certified");fi;
a:=U1SolveData(c,4,"U1s",U1Source(c,2,state));;b:=U1SolveCertifiedChargeData(c,2,state);;
if (a=fail)<>(b=fail) then Error("Uncertified fallback changed");fi;
# Replacing either the context action or source invalidates its exact identity.
c:=U1CyclicContext(2,1,1,0);;state:=U1CertifiedClosedChargeState(c,3,[1]);;
c.omega:=function(g,h)return 0;end;;
a:=U1SolveData(c,5,"U1s",U1Source(c,3,state));;b:=U1SolveCertifiedChargeData(c,3,state);;
if (a=fail)<>(b=fail) or (a<>fail and a.nativePrimitive<>b.nativePrimitive) then Error("Stale source certificate accepted");fi;
c:=U1CyclicContext(3,0,0,0);;state:=U1CertifiedClosedChargeState(c,2,[1]);;
c.omega:=function(g,h)return QuoInt(g!.exponents[1]+h!.exponents[1],3)/3;end;;
a:=U1SolveData(c,4,"U1s",U1Source(c,2,state));;b:=U1SolveCertifiedChargeData(c,2,state);;
if (a=fail)<>(b=fail) or (a<>fail and a.nativePrimitive<>b.nativePrimitive) then Error("Changed rational background did not fall back");fi;
c:=U1CyclicContext(2,1,1,0);;state:=U1CertifiedClosedChargeState(c,3,[2]);;
zero:=U1SolveCertifiedChargeData(c,3,state);;
if not IsIdenticalObj(zero.primitive,U1Zero) then Error("Certified zero source lost its literal zero primitive");fi;
zero:=U1SolveHalfPhaseData(c,5,U1Zero);;
if not IsIdenticalObj(zero.primitive,U1Zero) then Error("Generic zero source lost its literal zero primitive");fi;
Print("LITERAL_ZERO_PRIMITIVES_PASS\n");;
Print("NATIVE_SOLVES ",nativeChecks," EXACT_PRIMITIVE_VALUES ",primitiveChecks," QUARTER_PRIMITIVES ",quarterPrimitives,"\n");;
QUIT_GAP(0);
