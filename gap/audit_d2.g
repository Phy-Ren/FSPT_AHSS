# Independent D2 spin-half audit. No classification answer is an input.
# Run after gap/load.g; optionally set U1_D2_AUDIT_OUT to a JSON destination.
BindGlobal("U1AuditD2",function()
  local data,c,x,y,q,nq,O,no,bo,HQ,HO,H6,HF6,q2,polynomial,power,
    bx,qx,px,incoming,lambda,HP,g,h,j,k,tuple,barClosureCount,result,classification;
  data:=rec(identity_index:=0,multiplication:=[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]],
    s:=[0,0,0,0],rho:=[0,0,0,0],omega:=List([1..4],i->List([1..4],j->"0")));
  c:=U1FiniteContext(data,7);
  x:=g->[0,1,0,1][c.elementIndex(g)];y:=g->[0,0,1,1][c.elementIndex(g)];
  # Integral Bockstein of the real lift x cup y: q = d(x cup y)/2.
  q:=function(g,h,k) return x(g)*x(h)*y(k)-x(g)*y(h)*y(k);end;
  nq:=U1Native(c,3,"Z",q);HQ:=U1Cohomology(c,3,"Z");
  if HQ.coordinates(nq)<>[1] then Error("Explicit Bockstein is not the nonzero integral charge class");fi;
  O:=U1ChargeSource(c,3,q);no:=U1Native(c,5,"U1s",O);
  HO:=U1Cohomology(c,5,"U1s");
  bo:=U1ApplyDifferential(c,5,"Zs",no);
  if not ForAll(bo,IsInt) then Error("Phase obstruction Bockstein is not integral");fi;
  H6:=U1Cohomology(c,6,"Z");HF6:=U1Cohomology(c,6,"F2");
  bx:=HF6.coordinates(List(bo,i->i mod 2));
  q2:=U1Cup(c,3,q,"F2",3,q,"F2",0,true);qx:=HF6.coordinates(U1Native(c,6,"F2",q2));
  power:=function(f,n)
    local ans,i;ans:=f;
    for i in [2..n] do ans:=U1Cup(c,i-1,ans,"F2",1,f,"F2",0,true);od;
    return ans;
  end;
  polynomial:=U1Add(U1Cup(c,4,power(x,4),"F2",2,power(y,2),"F2",0,true),
    U1Cup(c,2,power(x,2),"F2",4,power(y,4),"F2",0,true));
  px:=HF6.coordinates(U1Native(c,6,"F2",polynomial));
  if bx<>qx or bx<>px or ForAll(bx,i->i=0) then Error("Nonzero polynomial Bockstein certificate failed");fi;
  if U1SolveNative(c,5,"U1s",no)<>fail then Error("Nonzero terminal obstruction was unexpectedly exact");fi;
  barClosureCount:=0;
  for tuple in Tuples(Filtered(Elements(c.G),g->g<>Identity(c.G)),4) do
    if CallFuncList(U1Coboundary(c,"Z",q),tuple)<>0 then Error("Explicit charge is not closed on bar tuples");fi;
    barClosureCount:=barClosureCount+1;
  od;
  HP:=U1Cohomology(c,4,"U1s");incoming:=[];
  for lambda in U1Cohomology(c,2,"Z").generators do
    Add(incoming,HP.coordinates(U1Native(c,4,"U1s",U1ChargeSource(c,2,U1Bar(c,2,"Z",lambda)))));
  od;
  if ForAny(Flat(incoming),i->i<>0) then Error("Expected vanishing incoming charge images");fi;
  classification:=U1Classify(c,3);
  result:=rec(group:="C2 x C2",background:=rec(s1:=0,rho1:=0,omega2:=0),
    integralChargeFormula:="q(g,h,k)=x(g)x(h)y(k)-x(g)y(h)y(k)=d(x cup y)/2",
    integralChargeOrders:=HQ.orders,integralChargeNative:=nq,integralChargeClass:=HQ.coordinates(nq),
    mod2ChargeClass:="x^2 y+x y^2",phaseObstructionClassPolynomial:="(x^4 y+x y^4)/2",
    phaseObstructionTargetOrders:=HO.orders,phaseObstructionNative:=no,phaseObstructionClass:=HO.coordinates(no),
    phaseObstructionHasPrimitive:=false,integralBocksteinNative:=bo,integralBocksteinClass:=H6.coordinates(bo),
    mod2BocksteinPolynomial:="x^4 y^2+x^2 y^4=(x^2 y+x y^2)^2",
    mod2BocksteinCoordinates:=bx,mod2ChargeSquareCoordinates:=qx,mod2PolynomialCoordinates:=px,
    incomingChargePhaseCoordinates:=incoming,incomingCIChargeFormula:="B3=d(omega2-s1^2/2)=0",
    explicitIntegralBarClosureChecks:=barClosureCount,
    classification:=classification,
    physicalCentreConstraint:="For physical spin-half D2, Rx Ry=(-1)^F Ry Rx. A one-dimensional state has commuting scalar rotations, hence (-1)^F=1 and integer U1 charge must be even.");
  return result;
end);
U1_D2_AUDIT:=U1AuditD2();;
if IsBound(U1_D2_AUDIT_OUT) then
  U1_D2_AUDIT_STREAM:=OutputTextFile(U1_D2_AUDIT_OUT,false);;
  SetPrintFormattingStatus(U1_D2_AUDIT_STREAM,false);;
  WriteLine(U1_D2_AUDIT_STREAM,U1JSON(U1_D2_AUDIT));CloseStream(U1_D2_AUDIT_STREAM);
fi;
