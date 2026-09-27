AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
AFSAssert:=function(ok,label) if not ok then Error(label); fi; end;;
for sg in [1,2,7] do
  c:=AFSBackend(sg);;
  Print("BACKEND_GROUP ",sg," dimensions=",List([0..6],k->Dimension(c.R)(k)),"\n");
  for coeff in ["Z","Zs","F2"] do
    for k in [0..4] do
      if Dimension(c.R)(k)=0 or Dimension(c.R)(k+1)=0 or Dimension(c.R)(k+2)=0 then continue; fi;
      AFSAssert(ForAll(Flat(AFSDifferential(c,k,coeff)*AFSDifferential(c,k+1,coeff)),
        function(x) if coeff="F2" then return x mod 2=0; else return x=0; fi; end),"native d^2");
    od;
  od;
  for ck in [[0,"Zs"],[1,"Zs"],[1,"F2"],[2,"F2"],[3,"F2"],[4,"F2"],[4,"U1s"],[5,"U1s"]] do
    H:=AFSCohomology(c,ck[1],ck[2]);;
    Print("H ",ck," ",H.orders,"\n");
    for j in [1..Length(H.generators)] do
      u:=H.coordinates(H.generators[j]);; e:=List(H.orders,x->0);; e[j]:=1;;
      AFSAssert(u=e,"cohomology representative coordinates");
    od;
  od;
  if sg=1 then
    AFSAssert(Length(AFSCohomology(c,1,"F2").generators)=3,"Z3 H1");
    AFSAssert(Length(AFSCohomology(c,2,"F2").generators)=3,"Z3 H2");
    AFSAssert(Length(AFSCohomology(c,3,"F2").generators)=1,"Z3 H3");
    AFSAssert(AFSCohomology(c,4,"U1s").orders=[],"Z3 high U1");
  fi;
  elts:=Concatenation([Identity(c.G)],GeneratorsOfGroup(c.G));;
  Append(elts,List(GeneratorsOfGroup(c.G),g->g^-1));;
  for coeff in ["F2","U1s"] do
    # Arbitrary bar 2-cochain, not necessarily the pullback of a native cochain.
    q:=function(g,h)
      local x,y;
      if g=Identity(c.G) or h=Identity(c.G) then return 0; fi;
      x:=g!.exponents; y:=h!.exponents;
      if coeff="F2" then return (Sum(x)^2*Sum(y)+Sum(y)^3) mod 2;
      else return AFSMod1((Sum(x)^2*Sum(y)+Sum(y)^3)/8); fi;
    end;;
    dq:=AFSCoboundary(c,coeff,q);; p:=AFSSolve(c,3,coeff,dq);;
    AFSAssert(p<>fail,"known boundary primitive exists");;
    dp:=AFSCoboundary(c,coeff,p);;
    for i in [1..12] do
      xs:=List([1..3],j->Random(elts));;
      AFSAssert(CallFuncList(dp,xs)=CallFuncList(dq,xs),"bar corrected primitive");
    od;
  od;
  Print("BACKEND_GROUP_PASS ",sg,"\n");
od;
Print("AFS_BACKEND_TEST_PASS\n");
QUIT_GAP(0);
