# Finite crystallographic point groups in their actual three-dimensional
# integer representations. IT numbers below select geometry from CrystCat;
# no space-group cohomology or classification result is used.
LoadPackage("CrystCat");;

BindGlobal("AFSPointGroupCatalogue",[
  ["1","C1",1,1,true], ["-1","Ci",2,2,false],
  ["2","C2",3,2,true], ["m","Cs",6,2,false],
  ["2/m","C2h",10,4,false], ["222","D2",16,4,true],
  ["mm2","C2v",25,4,false], ["mmm","D2h",47,8,false],
  ["4","C4",75,4,true], ["-4","S4",81,4,false],
  ["4/m","C4h",83,8,false], ["422","D4",89,8,true],
  ["4mm","C4v",99,8,false], ["-42m","D2d",111,8,false],
  ["4/mmm","D4h",123,16,false], ["3","C3",143,3,true],
  ["-3","C3i",147,6,false], ["32","D3",149,6,true],
  ["3m","C3v",156,6,false], ["-3m","D3d",162,12,false],
  ["6","C6",168,6,true], ["-6","C3h",174,6,false],
  ["6/m","C6h",175,12,false], ["622","D6",177,12,true],
  ["6mm","C6v",183,12,false], ["-6m2","D3h",187,12,false],
  ["6/mmm","D6h",191,24,false], ["23","T",195,12,true],
  ["m-3","Th",200,24,false], ["432","O",207,24,true],
  ["-43m","Td",215,24,false], ["m-3m","Oh",221,48,false]
]);

BindGlobal("AFSPointGroupInput",function(number)
  local entry,P,elements,signs,multiplication,i,j;
  if not IsInt(number) or not number in [1..32] then Error("point-group index must be 1..32");fi;
  entry:=AFSPointGroupCatalogue[number];
  P:=MatGroupZClass(3,entry[3]);elements:=Elements(P);
  if Length(elements)<>entry[4] then Error("point catalogue order mismatch");fi;
  if not ForAll(elements,R->DimensionsMat(R)=[3,3] and
      ForAll(R,row->ForAll(row,IsInt)) and AbsInt(DeterminantMat(R))=1) then
    Error("point catalogue is not a finite integer 3D representation");
  fi;
  signs:=List(elements,R->(1-DeterminantMat(R))/2);
  if ForAll(signs,x->x=0)<>entry[5] then Error("point catalogue determinant mismatch");fi;
  multiplication:=List(elements,R->List(elements,S->Position(elements,R*S)));
  for i in [1..Length(elements)] do
    for j in [1..Length(elements)] do
      if multiplication[i][j]=fail or
          signs[multiplication[i][j]]<>(signs[i]+signs[j]) mod 2 then
        Error("finite matrix multiplication or determinant character failed");
      fi;
    od;
  od;
  return rec(index:=number,hermannMauguin:=entry[1],schoenflies:=entry[2],
    representativeITNumber:=entry[3],order:=Length(elements),unitary:=entry[5],
    matrices:=elements,matrixGenerators:=GeneratorsOfGroup(P),signTable:=signs,
    multiplication:=multiplication,identityIndex:=Position(elements,One(P)),
    pointGroup:=P,crystCatParameters:=CrystCatRecord(P).parameters,
    elementSpectra:=Collected(List(elements,R->[Order(R),TraceMat(R),DeterminantMat(R)])),
    catalogue:="CrystCat MatGroupZClass(3, representativeITNumber)",
    catalogueKeyScope:="IT number selects only a finite linear representation; no affine group or answer table is used");
end);

BindGlobal("AFSPointGroupBackend",function(number)
  local data,P,iso,G,c,projection,elements,i,j,g,H0,H1,start;
  start:=Runtime();data:=AFSPointGroupInput(number);P:=data.pointGroup;
  iso:=IsomorphismPcpGroup(P);
  if iso=fail then Error("finite point group lacks a Pcp isomorphism");fi;
  G:=Image(iso);projection:=InverseGeneralMapping(iso);
  if Size(G)<>data.order then Error("finite point-group isomorphism changed the order");fi;
  elements:=List(data.matrices,R->Image(iso,R));
  for i in [1..data.order] do
    if Image(projection,elements[i])<>data.matrices[i] then Error("matrix isomorphism does not roundtrip");fi;
    for j in [1..data.order] do
      if elements[i]*elements[j]<>elements[data.multiplication[i][j]] then
        Error("matrix/Pcp multiplication mismatch");
      fi;
    od;
  od;
  c:=rec(number:=number,G:=G,pointGroup:=P,matrixIso:=iso,matrixProjection:=projection,
    pointInput:=data,differentialCache:=rec(),smithCache:=rec(),
    cohomologyCache:=rec(),f2SolveCache:=rec(),omega2:=AFSZero);
  c.matrixIndex:=AFSMemo(g->Position(data.matrices,Image(projection,g)));
  if data.unitary then c.sign:=g->1;c.s:=AFSZero;
  else c.sign:=g->DeterminantMat(Image(projection,g));c.s:=g->data.signTable[c.matrixIndex(g)];fi;
  c.action:=c.sign;
  # The already validated finite helper uses compact standard presentations
  # for S4 and S4 x C2, transporting the resolution back to this exact G.
  c.R:=AFSFiniteHolonomyResolution(G,6);
  c.R!.afsTimings:=rec(finiteResolutionCpuMs:=Runtime()-start);
  c.bar:=AFSComparison(c.R);
  H0:=AFSCohomology(c,0,"Zs");H1:=AFSCohomology(c,1,"Zs");
  if data.unitary then
    if H0.orders<>[0] or H1.orders<>[] then Error("finite unitary H0/H1 structure failed");fi;
  else
    if H0.orders<>[] or H1.orders<>[2] then Error("finite signed H0/H1 structure failed");fi;
    if H1.coordinates(AFSNative(c,1,"Zs",c.s))<>[1] then Error("canonical sign is not the signed H1 generator");fi;
  fi;
  c.finiteH0Orders:=H0.orders;c.finiteH1Orders:=H1.orders;
  Print("AFS_FINITE_BACKEND ",number," ",data.hermannMauguin," order=",data.order,
    " dimensions=",List([0..6],k->Dimension(c.R)(k))," cpu_ms=",Runtime(),"\n");
  return c;
end);

BindGlobal("AFSInstallPointGroupBackground",function(ctx)
  local data;
  data:=AFSPinMinusPointGroup(ctx.pointGroup);
  if data.pointElements<>ctx.pointInput.matrices or data.signTable<>ctx.pointInput.signTable then
    Error("Pin-minus point matrices/character disagree with the finite input");
  fi;
  data.projection:=ctx.matrixProjection;data.pointIndex:=ctx.matrixIndex;
  ctx.crystallineBackground:=data;
  ctx.omega2:=function(g,h) return data.omegaTable[ctx.matrixIndex(g)][ctx.matrixIndex(h)];end;
  return data;
end);

BindGlobal("AFSPointGroupExport",function(ctx)
  local out,key;
  out:=rec();
  for key in ["index","hermannMauguin","schoenflies","representativeITNumber",
      "order","unitary","matrices","matrixGenerators","signTable",
      "multiplication","identityIndex","catalogue","catalogueKeyScope",
      "crystCatParameters","elementSpectra"] do
    out.(key):=ctx.pointInput.(key);
  od;
  out.kind:="finite-crystallographic-point-group";out.representationDimension:=3;
  out.translationSubgroupPresent:=false;
  out.determinantDistribution:=rec(positive:=Number(out.signTable,x->x=0),
    negative:=Number(out.signTable,x->x=1));
  out.pcpGeneratorMatrixIndices:=List(GeneratorsOfGroup(ctx.G),ctx.matrixIndex);
  out.resolutionElementMatrixIndices:=List(ctx.R!.elts,ctx.matrixIndex);
  out.finiteH0ZsOrders:=ctx.finiteH0Orders;out.finiteH1ZsOrders:=ctx.finiteH1Orders;
  out.matrixIsomorphismCheckedAllProducts:=true;
  return out;
end);

# Relabel only geometric provenance inherited from the shared exporter.
# Cochains, presentations, bases and all numerical certificates stay unchanged.
BindGlobal("AFSPointGroupExportLabels",function(x)
  local k;
  if IsRecord(x) then
    if IsBound(x.spaceGroup) then x.pointGroupIndex:=x.spaceGroup;Unbind(x.spaceGroup);fi;
    for k in RecNames(x) do AFSPointGroupExportLabels(x.(k));od;
  elif IsList(x) and not IsString(x) then
    for k in [1..Length(x)] do AFSPointGroupExportLabels(x[k]);od;
  fi;
end);
