# Exact geometry/presentation export only. No classification or formula calls.
U1_ROOT:=".";;
Read("gap/load.g");;
LoadPackage("CrystCat");;
U1_SG_EXPORT:=[];;
for n in [1..230] do
  affine:=SpaceGroupBBNWZ(3,n);;
  iso:=IsomorphismPcpGroup(affine);; G:=Image(iso);;
  if not IsAlmostCrystallographic(G) then Error("Affine Pcp image is not almost crystallographic");fi;
  fpiso:=IsomorphismFpGroup(G);; F:=Image(fpiso);;
  fg:=GeneratorsOfGroup(F);;
  ag:=List(fg,x->PreImageElm(iso,PreImageElm(fpiso,x)));;
  rel:=List(RelatorsOfFpGroup(F),LetterRepAssocWord);;
  if ForAny(RelatorsOfFpGroup(F),r->MappedWord(r,FreeGeneratorsOfFpGroup(F),ag)<>One(affine)) then
    Error("Exported affine presentation relation failed");
  fi;
  L:=Kernel(NaturalHomomorphismOnHolonomyGroup(G));; pc:=Pcp(L,"snf");;
  trans:=List([1..Length(pc)],i->pc[i]);;
  if Length(pc)<>3 or RelativeOrdersOfPcp(pc)<>[0,0,0] or not IsAbelian(L) then
    Error("Three-dimensional translation kernel is not Z^3");
  fi;
  Add(U1_SG_EXPORT,rec(number:=n,name:=CR_3.HermannMauguinSymbol[n],
    crystcatParameters:=CrystCatRecord(affine).parameters,
    affineGenerators:=GeneratorsOfGroup(affine),
    pointMatrices:=Elements(Image(PointHomomorphism(affine))),
    presentationGeneratorMatrices:=ag,presentationRelators:=rel,
    translationGeneratorMatrices:=List(trans,g->PreImageElm(iso,g)),
    translationGeneratorWords:=List(trans,g->LetterRepAssocWord(UnderlyingElement(Image(fpiso,g)))),
    presentationIsomorphismVerified:=true));;
od;
out:=OutputTextFile("insulator_catalog/source/spacegroup_gap_export.json",false);;
SetPrintFormattingStatus(out,false);;
PrintTo(out,U1JSON(rec(records:=U1_SG_EXPORT,GAP:=GAPInfo.Version,
  CrystCat:=PackageInfo("CrystCat")[1].Version,Polycyclic:=PackageInfo("Polycyclic")[1].Version)),"\n");;
CloseStream(out);;
Print("EXPORTED_SPACEGROUPS ",Length(U1_SG_EXPORT),"\n");
QUIT;
