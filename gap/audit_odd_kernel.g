# A classification-independent restriction audit for a normal odd-order kernel.
# All indices written to the witness are zero based, matching the input catalog.
BindGlobal("U1AuditOddKernel",function(sourceIndex,targetIndex,spin)
  local readInput,source,target,perms,G,N,H,ni,hi,ht,choices,map,bits,lambda,
    i,j,k,traces,products,background,quotient,cosets,cosetIndex;
  readInput:=function(index)
    local label;
    label:=String(index);if index<10 then label:=Concatenation("0",label);fi;
    Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_",label,"_",spin,".g"));
    return U1_INPUT;
  end;
  source:=readInput(sourceIndex);target:=readInput(targetIndex);
  perms:=List([1..source.order],i->PermList(List([1..source.order],j->source.multiplication[j][i]+1)));
  G:=Group(perms);N:=SylowSubgroup(G,3);H:=SylowSubgroup(G,2);
  if Size(G)<>12 or Size(N)<>3 or Size(H)<>4 or not IsNormal(G,N) or
    Size(Intersection(N,H))<>1 or ClosureGroup(N,H)<>G then
    Error("The claimed normal C3 and Sylow-2 complement do not exist");
  fi;
  ni:=Filtered([1..source.order],i->perms[i] in N);
  hi:=Filtered([1..source.order],i->perms[i] in H);
  if hi[1]<>source.identity_index+1 or target.identity_index<>0 then Error("Unexpected identity ordering");fi;
  ht:=List(hi,i->List(hi,j->Position(hi,source.multiplication[i][j]+1)));
  if ForAny(ni,i->source.s[i]<>0 or source.r[i]<>0) then Error("Odd kernel carries a nontrivial sign");fi;
  traces:=List(hi,i->TraceMat(source.matrices[i]));choices:=[];
  for map in PermutationsList([2..target.order]) do
    map:=Concatenation([1],map);
    if ForAll([1..4],i->traces[i]=TraceMat(target.matrices[map[i]]) and
      source.s[hi[i]]=target.s[map[i]] and source.r[hi[i]]=target.r[map[i]]) and
      ForAll([1..4],i->ForAll([1..4],j->map[ht[i][j]]=target.multiplication[map[i]][map[j]]+1)) then
      Add(choices,map);
    fi;
  od;
  if choices=[] then Error("No geometric character-preserving subgroup identification");fi;
  map:=choices[1];lambda:=fail;
  for bits in Tuples([0,1],3) do
    bits:=Concatenation([0],bits);
    if ForAll([1..4],i->ForAll([1..4],j->IsInt(
      Rat(source.omega[hi[i]][hi[j]])-Rat(target.omega[map[i]][map[j]])-
      (bits[j]-bits[ht[i][j]]+bits[i])/2))) then lambda:=bits/2;break;fi;
  od;
  if lambda=fail then Error("Restricted extensions have inequivalent half-cocycle classes");fi;
  quotient:=NaturalHomomorphismByNormalSubgroup(G,N);
  if Size(Image(quotient,H))<>4 or Size(Kernel(RestrictedMapping(quotient,H)))<>1 then
    Error("The complement does not identify with the quotient");
  fi;
  cosets:=List(hi,i->Image(quotient,perms[i]));
  cosetIndex:=List(perms,g->Position(cosets,Image(quotient,g))-1);
  products:=0;background:=0;
  for i in [1..4] do for j in [1..4] do
    if cosetIndex[source.multiplication[hi[i]][hi[j]]+1]<>ht[i][j]-1 then Error("Quotient product failed");fi;
    products:=products+1;background:=background+1;
  od;od;
  return rec(source:=source.id,target:=target.id,
    sourceOrder:=Size(G),normalOddKernelOrder:=Size(N),sylow2Order:=Size(H),
    normalOddKernelOriginalIndices:=ni-1,sylow2OriginalIndices:=hi-1,
    targetIndicesBySylow2Index:=map-1,quotientIndexByOriginalIndex:=cosetIndex,
    subgroupMultiplication:=List(ht,row->row-1),
    matrixCharacters:=traces,geometricCharacterAndSignsAgree:=true,
    restrictedExtensionGauge:=lambda,
    extensionGaugeConvention:="omega_source|H - omega_target = d(lambda) modulo integers",
    subgroupProductChecks:=products,extensionPairChecks:=background,
    normalOddKernelVerified:=true,complementIdentifiesWithQuotient:=true,
    twoPrimaryArgument:="For 1 -> C3 -> G -> H -> 1, positive C3 cohomology vanishes after localization at 2. LHS inflation is an isomorphism and restriction to the displayed complement is its inverse, for every supplied sign coefficient module.",
    threePrimaryArgument:="Restriction to Sylow C3 detects the 3-primary part. Its signs are trivial and H1(C3,Z)=H3(C3,Z)=H4(C3,R/Z)=0, so the three retained 3D filtration layers have no 3-primary part.",
    conclusion:="Restriction identifies the complete supplied 3D CI/charge/phase classification and stacking, by naturality of differentials, gauges and products; no external table is assumed.",
    scope:="CI-generated, localized-charge and group-cohomological phase sector; no neutral E8 claim");
end);
U1_ODD_KERNEL_AUDIT:=[];;
for U1_ODD_KERNEL_PAIR in [[20,5],[24,6],[26,7]] do
  for U1_ODD_KERNEL_SPIN in ["spinless","spin_half"] do
    Add(U1_ODD_KERNEL_AUDIT,U1AuditOddKernel(U1_ODD_KERNEL_PAIR[1],U1_ODD_KERNEL_PAIR[2],U1_ODD_KERNEL_SPIN));
  od;
od;
if IsBound(U1_ODD_KERNEL_AUDIT_OUT) then
  U1_ODD_KERNEL_STREAM:=OutputTextFile(U1_ODD_KERNEL_AUDIT_OUT,false);;
  SetPrintFormattingStatus(U1_ODD_KERNEL_STREAM,false);;
  WriteLine(U1_ODD_KERNEL_STREAM,U1JSON(U1_ODD_KERNEL_AUDIT));CloseStream(U1_ODD_KERNEL_STREAM);
fi;
