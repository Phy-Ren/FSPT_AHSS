if not IsBound(AFS_ROOT) then AFS_ROOT:=".";fi;
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));
Read(Concatenation(AFS_ROOT,"/gap/point_group_backend.g"));
RunPointBackendControl:=function()
local spectra,number,d,c,coeff,k,D,ck,H,i,e,elts,q,dq,p,dp,xs;
spectra:=[];;
for number in [1..32] do
  d:=AFSPointGroupInput(number);;
  Add(spectra,d.elementSpectra);
  Print("POINT_INPUT ",number," ",d.hermannMauguin," ",d.schoenflies,
    " order=",d.order," positive=",Number(d.signTable,x->x=0),
    " catalogue=",d.crystCatParameters,"\n");
od;
if Length(Set(spectra))<>32 then Error("point spectra do not distinguish all 32 geometric inputs");fi;
for number in [1,3,4,10,32] do
  c:=AFSPointGroupBackend(number);;
  for coeff in ["Z","Zs","F2"] do
    for k in [0..4] do
      if Minimum(List([k..k+2],i->Dimension(c.R)(i)))=0 then continue;fi;
      D:=AFSDifferential(c,k,coeff)*AFSDifferential(c,k+1,coeff);;
      if coeff="F2" then
        if ForAny(Flat(D),x->x mod 2<>0) then Error("finite differential square");fi;
      elif ForAny(Flat(D),x->x<>0) then Error("finite integral differential square");fi;
    od;
  od;
  for ck in [[0,"Zs"],[1,"Zs"],[2,"F2"],[3,"F2"],[4,"U1s"],[5,"U1s"]] do
    H:=AFSCohomology(c,ck[1],ck[2]);;
    for i in [1..Length(H.generators)] do
      e:=List(H.orders,x->0);e[i]:=1;
      if H.coordinates(H.generators[i])<>e then Error("finite cohomology coordinates");fi;
    od;
  od;
  elts:=Elements(c.G);;
  for coeff in ["F2","U1s"] do
    q:=function(g,h)
      local a;
      if g=One(c.G) or h=One(c.G) then return 0;fi;
      a:=c.matrixIndex(g)^2*c.matrixIndex(h)+c.matrixIndex(h)^3;
      if coeff="F2" then return a mod 2;else return AFSMod1(a/8);fi;
    end;;
    dq:=AFSCoboundary(c,coeff,q);;p:=AFSSolve(c,3,coeff,dq);;
    if p=fail then Error("finite known boundary primitive missing");fi;
    dp:=AFSCoboundary(c,coeff,p);;
    for i in [1..16] do
      xs:=List([1..3],j->elts[1+(i*j+j^2) mod Length(elts)]);;
      if CallFuncList(dp,xs)<>CallFuncList(dq,xs) then Error("finite literal bar primitive");fi;
    od;
  od;
  Print("POINT_BACKEND_PASS ",number,"\n");
od;
end;;
RunPointBackendControl();;
Print("AFS_POINT_BACKEND_TEST_PASS\n");QUIT_GAP(0);
