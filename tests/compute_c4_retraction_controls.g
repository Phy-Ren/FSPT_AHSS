# An exact retraction certifies a direct-summand constraint on the affine
# classification. It does not compute an affine classification from C4.
AFS_ROOT:=GAPInfo.SystemEnvironment.AFS_TEST_SOURCE;;
OnBreak:=function() Where(25);QUIT_GAP(1);end;;
for sourceFile in ["backend.g","backend_diagonal.g","formula_data.g",
    "formula_fast.g","pip_o5_program.g","pip_o5_sign.g","pip_o5_general.g","formulas.g",
    "classification.g","pip.g","stacking.g","pip_coordinate_data.g",
    "pip_coordinates.g","pip_diagonal_data.g","pip_c4_data.g","pip_stacking.g"] do
  Read(Concatenation(AFS_ROOT,"/gap/",sourceFile));
od;
retractions:=[];;
for sg in [81,82] do
  ctx:=AFSBackend(sg);;h:=NaturalHomomorphismOnHolonomyGroup(ctx.G);;P:=Image(h);;
  Assert(0,Size(P)=4 and IsCyclic(P));
  p:=First(Elements(P),g->Order(g)=4);;r:=PreImagesRepresentative(h,p);;
  Assert(0,Order(r)=4 and ctx.s(r)=1);
  section:=GroupHomomorphismByImages(P,ctx.G,[p],[r]);;
  Assert(0,section<>fail);
  Assert(0,ForAll(Elements(P),g->Image(h,Image(section,g))=g));
  Add(retractions,rec(space_group:=sg,quotient_order:=Size(P),
    section_generator_pcp_exponents:=ExponentsByPcp(Pcp(ctx.G),r),
    section_generator_affine_matrix:=PreImageElm(ctx.iso,r),
    section_generator_order:=Order(r),section_generator_orientation:=ctx.s(r),
    projection_section_identity_verified:=true));
  Print("ACTUAL_AFFINE_C4_RETRACTION_PASS ",sg,"\n");
od;
G:=CyclicGroup(IsPcpGroup,4);;pc:=Pcp(G);;
ctx:=rec(number:=0,G:=G,differentialCache:=rec(),smithCache:=rec(),
  cohomologyCache:=rec(),f2SolveCache:=rec());;
ctx.sign:=g->(-1)^ExponentsByPcp(pc,g)[1];;
ctx.s:=g->ExponentsByPcp(pc,g)[1] mod 2;;ctx.action:=ctx.sign;;
ctx.R:=ResolutionFiniteGroup(G,6,false,0,"extendible");;ctx.bar:=AFSComparison(ctx.R);;
AFS_STACK_AUDIT:=true;;
C:=AFSClassify(ctx);;result:=AFSExplicitPipStacking(C);;
Assert(0,result.status="computed");
LoadPackage("json");;
tag:="";;
if IsBound(GAPInfo.SystemEnvironment.AFS_TEST_TAG) then
  tag:=Concatenation("_",GAPInfo.SystemEnvironment.AFS_TEST_TAG);
fi;
stream:=OutputTextFile(Concatenation("runs/finite_c4_retraction_controls",tag,".json"),false);;
SetPrintFormattingStatus(stream,false);;
WriteAll(stream,GapToJsonString(rec(source:=AFS_ROOT,retractions:=retractions,
  finite_input:=rec(group:="CyclicGroup(4)",orientation_generator:=1,omega:=0,spatial_dimension:=3),
  finite_stacking:=AFSExplicitPipExport(C,result))));;
CloseStream(stream);;
Print("FINITE_C4_FULL_STACKING_CONTROL ",result.invariants," relation=",result.pipRelationCoordinates,"\n");
QUIT_GAP(0);
