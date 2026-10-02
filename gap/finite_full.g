# One serial classification-to-stacking pipeline for finite internal symmetry.
# Outgoing permanent classes retain explicit flat lifts. Incoming gauge images
# are imposed only after their complete upper-layer carries have been measured.

# In positive degree a finite group's rational cohomology vanishes, so the
# torsion Smith construction for U(1)_s is valid also below degree four. The
# affine backend intentionally excludes these degrees because its free U(1)
# classes need an additional adapter. Negative degree denotes an absent layer.
BindGlobal("AFSFullH",function(c,k,coeff)
  local H,s,inds,D,key;
  if k<0 then
    H:=rec(degree:=k,coefficient:=coeff,orders:=[],generators:=[]);
    H.coordinates:=v->[];return H;
  fi;
  if coeff<>"U1s" or k>=4 then return AFSCohomology(c,k,coeff);fi;
  if k<1 or not IsFinite(c.G) then Error("low-degree complete U1 adapter requires a finite group and positive degree");fi;
  key:=Concatenation(coeff,String(k));
  if IsBound(c.cohomologyCache.(key)) then return c.cohomologyCache.(key);fi;
  s:=AFSDifferentialSmith(c,k,"Zs");inds:=Filtered([1..s.rank],i->AbsInt(s.diag[i])>1);
  H:=rec(degree:=k,coefficient:=coeff,generators:=List(inds,i->List(s.U[i]/s.diag[i],AFSMod1)),
    orders:=List(inds,i->AbsInt(s.diag[i])),smith:=s);
  D:=AFSDifferential(c,k,"Zs");
  H.coordinates:=function(v)
    local b,co;b:=v*D;if not ForAll(b,IsInt) then return fail;fi;co:=b*s.V;
    return List(inds,j->co[j] mod AbsInt(s.diag[j]));
  end;
  c.cohomologyCache.(key):=H;return H;
end);

BindGlobal("AFSFullClass",function(c,degree,coeff,H,f)
  local co;
  if degree<0 then
    if f<>AFSZero then Error("nonzero absent negative-degree field");fi;return [];
  fi;
  if coeff="U1s" then co:=AFSU1BarCoordinates(c,degree,H,f);
  else co:=H.coordinates(AFSNative(c,degree,coeff,f));fi;
  if co=fail then Error("complete formula did not give a closed cochain");fi;
  return co;
end);

BindGlobal("AFSFullAbelianSolve",function(rows,orders,target)
  local relations,i,row,answer;
  relations:=ShallowCopy(rows);
  for i in [1..Length(orders)] do
    if orders[i]<>0 then
      row:=List(orders,x->0);row[i]:=orders[i];Add(relations,row);
    fi;
  od;
  answer:=AFSStackLatticeSolver(relations,Length(orders))(target);
  if answer=fail then return fail;fi;
  return answer{[1..Length(rows)]};
end);

# Kernel of a homomorphism of finitely generated abelian groups. This retains
# a cyclic basis and its actual ambient representatives without enumerating
# group elements, and therefore also applies to free space-group p+ip layers.
BindGlobal("AFSFullAbelianKernel",function(S,images,targetOrders)
  local m,t,M,i,row,smith,K,B,relations,answer,Q,active,generators,v,j,orders;
  m:=Length(S.orders);t:=Length(targetOrders);
  if Length(images)<>m then Error("abelian kernel source size mismatch");fi;
  if m=0 then return rec(ambientOrders:=S.ambientOrders,orders:=[],generators:=[]);fi;
  for i in [1..m] do
    if S.orders[i]<>0 then
      for j in [1..t] do
        if targetOrders[j]=0 then
          if S.orders[i]*images[i][j]<>0 then Error("map violates a finite source relation");fi;
        elif (S.orders[i]*images[i][j]) mod targetOrders[j]<>0 then
          Error("map violates a finite source relation");
        fi;
      od;
    fi;
  od;
  M:=ShallowCopy(images);
  for i in [1..t] do
    if targetOrders[i]<>0 then row:=List(targetOrders,x->0);row[i]:=-targetOrders[i];Add(M,row);fi;
  od;
  smith:=AFSSmith(M,Length(M),t);
  K:=List(smith.U{[smith.rank+1..Length(M)]},row->row{[1..m]});
  K:=Filtered(K,row->ForAny(row,x->x<>0));
  smith:=AFSSmith(K,Length(K),m);
  B:=[];if Length(K)>0 then B:=(smith.U*K){[1..smith.rank]};fi;
  relations:=[];
  for i in [1..m] do
    if S.orders[i]<>0 then
      row:=List([1..m],j->0);row[i]:=S.orders[i];
      answer:=AFSStackLatticeSolver(B,m)(row);
      if answer=fail then Error("kernel lattice lost a source relation");fi;
      Add(relations,answer);
    fi;
  od;
  Q:=AFSSmith(relations,Length(relations),Length(B));
  active:=Filtered([1..Length(B)],i->i>Q.rank or AbsInt(Q.diag[i])>1);
  orders:=List(active,function(i)if i>Q.rank then return 0;else return AbsInt(Q.diag[i]);fi;end);
  generators:=[];
  for i in active do
    v:=Q.Vi[i]*B;v:=v*S.generators;
    for j in [1..Length(v)] do if S.ambientOrders[j]<>0 then v[j]:=v[j] mod S.ambientOrders[j];fi;od;
    Add(generators,v);
  od;
  return rec(ambientOrders:=S.ambientOrders,orders:=orders,generators:=generators,
    kernelLatticeBasis:=B,kernelLatticeRelations:=relations);
end);

# Exact finite-unitary primitive for the proven pure even-integer source.
# All group pairs certify h=delta A, so no native-zero inference is involved.
BindGlobal("AFSFullCubePrimitive",function(C,x)
  local c,h,A,phase,record;
  c:=C.ctx;
  if not c.fullCertifiedCubePrimitive or x.n=AFSZero or x.a<>AFSZero or x.c<>AFSZero or
    c.s<>AFSZero or c.omega2<>AFSZero or not IsBound(c.elements) then return fail;fi;
  h:=List(c.elements,g->List(c.elements,k->CallFuncList(x.n,[g,k])/2));
  if not ForAll(h,row->ForAll(row,IsInt)) then return fail;fi;
  A:=List(h,row->Sum(row)/Length(c.elements));
  if not ForAll(c.elements,g->ForAll(c.elements,k->
    A[c.elementIndex(g)]+A[c.elementIndex(k)]-A[c.elementIndex(g*k)]=h[c.elementIndex(g)][c.elementIndex(k)])) then
    return fail;
  fi;
  phase:=AFSMemo(function(g1,g2,g3,g4,g5)
    return AFSMod1(A[c.elementIndex(g1)]*h[c.elementIndex(g2)][c.elementIndex(g3)]*
      h[c.elementIndex(g4)][c.elementIndex(g5)]/6);
  end);
  record:=rec(identifier:="pip-even-integral-cocycle-terminal-cube-v1",
    sourceIdentity:="O6(2h,0,0;0,0)=h cup h cup h/6 modulo one",
    primitive:="nu5=A cup h cup h/6; delta A=h on every group pair",
    averageValuesByContextElement:=List(A,z->[NumeratorRat(z),DenominatorRat(z)]),
    nativeInteger:=AFSNative(c,2,"Z",x.n),checkedPairs:=Length(c.elements)^2,
    markedPhaseConvention:="explicit rational primitive; may differ from generic homotopy primitive by a bosonic cocycle");
  Add(C.cubePrimitiveCertificates,record);
  return phase;
end);

# The normalized binary current-coordinate source is a universal cube plus
# an exact five-simplex lookup coboundary, verified on all legal local patterns.
BindGlobal("AFSFullBinaryPrimitive",function(C,x)
  local c,n,A,phase,record,data;
  c:=C.ctx;
  if not c.fullCertifiedBinaryPrimitive or x.n=AFSZero or x.a<>AFSZero or x.c<>AFSZero or
    c.s<>AFSZero or not IsBound(c.elements) then return fail;fi;
  n:=List(c.elements,g->List(c.elements,h->CallFuncList(x.n,[g,h])));
  if not ForAll(n,row->ForAll(row,z->z in [0,1])) then return fail;fi;
  if not ForAll(c.elements,g->ForAll(c.elements,h->
    n[c.elementIndex(g)][c.elementIndex(h)]=CallFuncList(c.omega2,[g,h]))) then return fail;fi;
  A:=List(n,row->Sum(row)/Length(c.elements));
  if not ForAll(c.elements,g->ForAll(c.elements,h->
    A[c.elementIndex(g)]+A[c.elementIndex(h)]-A[c.elementIndex(g*h)]=n[c.elementIndex(g)][c.elementIndex(h)])) then return fail;fi;
  if not IsBoundGlobal("AFS_FULL_BINARY_TERMINAL_DATA") then
    Read(Concatenation(AFS_ROOT,"/gap/full_binary_terminal_data.g"));
  fi;
  data:=ValueGlobal("AFS_FULL_BINARY_TERMINAL_DATA");
  phase:=AFSMemo(function(g1,g2,g3,g4,g5)
    local vertices,g,key,bit,i,j,k;
    vertices:=[];g:=Identity(c.G);
    for k in [g1,g2,g3,g4,g5] do g:=g*k;Add(vertices,g);od;
    key:=0;bit:=1;
    for i in [1..4] do for j in [i+1..5] do
      key:=key+bit*n[c.elementIndex(vertices[i])][c.elementIndex(vertices[i]^-1*vertices[j])];bit:=bit*2;
    od;od;
    k:=LookupDictionary(data.lookup,key);if k=fail then Error("nonbinary-integral terminal face pattern");fi;
    return AFSMod1(data.numerator48*A[c.elementIndex(g1)]*
      n[c.elementIndex(g2)][c.elementIndex(g3)]*n[c.elementIndex(g4)][c.elementIndex(g5)]/48+k/4);
  end);
  record:=rec(identifier:="pip-binary-integral-matched-omega-terminal-lookup-v1",
    certificateSha256:=data.certificateSha256,
    averageValuesByContextElement:=List(A,z->[NumeratorRat(z),DenominatorRat(z)]),
    nativeInteger:=AFSNative(c,2,"Z",x.n),checkedPairs:=Length(c.elements)^2,
    primitive:="25 A cup n cup n/48 + K5/4; delta A=n and omega=n pointwise");
  Add(C.binaryPrimitiveCertificates,record);return phase;
end);

# Construct a normalized binary integral lift of a finite unitary character.
BindGlobal("AFSFullBinaryCharacter",function(C,v)
  local c,n,average,rho,q,h;
  c:=C.ctx;n:=AFSBar(c,2,"Z",v);
  average:=List(c.elements,g->Sum(c.elements,k->CallFuncList(n,[g,k]))/Length(c.elements));
  rho:=List(average,AFSMod1);q:=average-rho;
  h:=List(c.elements,g->List(c.elements,k->rho[c.elementIndex(g)]+rho[c.elementIndex(k)]-rho[c.elementIndex(g*k)]));
  if not ForAll(h,row->ForAll(row,z->z in [0,1])) then Error("binary character construction failed");fi;
  if not ForAll(c.elements,g->ForAll(c.elements,k->CallFuncList(n,[g,k])-h[c.elementIndex(g)][c.elementIndex(k)]=
    q[c.elementIndex(g)]+q[c.elementIndex(k)]-q[c.elementIndex(g*k)])) then Error("binary character integer shift failed");fi;
  return rec(h:=h,A:=rho,integerShift:=q,nativeInteger:=v);
end);

BindGlobal("AFSFullCFSquareLift",function(C,coordinates)
  local c,v,character,h,A,matched,square,co,phase,x,old,shift;
  c:=C.ctx;
  if not c.fullCertifiedCFSquare or c.s<>AFSZero or not IsBound(c.elements) then return fail;fi;
  if not IsBound(C.binaryCharacters) then
    C.binaryCharacters:=List(C.Hn.generators,v->AFSFullBinaryCharacter(C,v));
  fi;
  for character in C.binaryCharacters do
    h:=character.h;A:=character.A;matched:=false;
    if c.omega2<>AFSZero then
      matched:=ForAll(c.elements,g->ForAll(c.elements,k->
        CallFuncList(c.omega2,[g,k])=h[c.elementIndex(g)][c.elementIndex(k)]));
      if not matched then continue;fi;
    fi;
    square:=AFSMemo(function(g1,g2,g3,g4)
      return h[c.elementIndex(g1)][c.elementIndex(g2)]*h[c.elementIndex(g3)][c.elementIndex(g4)];
    end);
    co:=AFSFullClass(c,4,"F2",C.Hc,square);
    if co<>coordinates then continue;fi;
    # Literal AW word1231343 has the single face term h023*h012*h235*h345.
    phase:=AFSMemo(function(g1,g2,g3,g4,g5)
      local value;
      value:=h[c.elementIndex(g1)][c.elementIndex(g2)]*h[c.elementIndex(g1*g2)][c.elementIndex(g3)]*
        h[c.elementIndex(g3)][c.elementIndex(g4*g5)]*h[c.elementIndex(g4)][c.elementIndex(g5)]/2;
      if matched then value:=value+A[c.elementIndex(g1)]*
        h[c.elementIndex(g2)][c.elementIndex(g3)]*h[c.elementIndex(g4)][c.elementIndex(g5)]/2;fi;
      return AFSMod1(value);
    end);
    old:=AFSCombination(c,4,"F2",C.Hc,coordinates);
    shift:=AFSSolve(c,4,"F2",AFSCoadd(2,[old,square]));
    if shift=fail then Error("CF square representative has no exact shift");fi;
    Add(C.cfSquareCertificates,rec(identifier:="pure-cf-binary-integral-square-cartan-v1",
      cfClass:=co,nativeOriginalCF:=AFSNative(c,4,"F2",old),nativeSquareCF:=AFSNative(c,4,"F2",square),
      nativeRepresentativeShift:=AFSNative(c,3,"F2",shift),
      integralLift:=character.nativeInteger,integerShiftValues:=character.integerShift,
      characterValues:=List(A,z->[NumeratorRat(z),DenominatorRat(z)]),
      matchedOmega:=matched,checkedIntegerPairs:=Length(c.elements)^2,
      primitive:="word1231343(h,h,h,h)/2; add A cup h cup h/2 when omega=h",
      scope:="independent flat lift of the same CF cohomology class; marked phase may change"));
    x:=AFSFullZero();x.c:=square;x.v:=phase;return x;
  od;
  return fail;
end);

# The cache belongs to one classification context and only stores the literal
# n=0 partial states constructed by AFSFullMCLift. Function identities prevent
# a copied certificate from surviving a later field or background change.
BindGlobal("AFSFullMCPartialEntryForState",function(C,x)
  local entry;
  if C.mcPartialCacheStats.limit=0 or not IsBound(x.partialMCEntry) then return fail;fi;
  entry:=x.partialMCEntry;
  if not IsIdenticalObj(entry.owner,C.mcPartialCacheOwner) or
    entry.dimension<>C.dimension or entry.coordinate<>C.coordinate or
    entry.sign<>C.ctx.s or entry.omega<>C.ctx.omega2 or x.n<>AFSZero or
    entry.state.n<>x.n or entry.state.a<>x.a or entry.state.c<>x.c then return fail;fi;
  return entry;
end);

BindGlobal("AFSFullMCSourceData",function(C,x)
  local entry,source,co;
  entry:=AFSFullMCPartialEntryForState(C,x);
  if entry<>fail and IsBound(entry.source) then
    source:=entry.source;
    C.mcPartialCacheStats.bosonicSourceHits:=C.mcPartialCacheStats.bosonicSourceHits+1;
  else
    source:=AFSFullSource(C.ctx,C.dimension,"bosonic",x);
    C.mcPartialCacheStats.bosonicSourceBuilds:=C.mcPartialCacheStats.bosonicSourceBuilds+1;
    if entry<>fail then entry.source:=source;fi;
  fi;
  if entry<>fail and IsBound(entry.originalClass) then
    co:=entry.originalClass;
    C.mcPartialCacheStats.originalClassHits:=C.mcPartialCacheStats.originalClassHits+1;
  else
    co:=AFSFullClass(C.ctx,C.dimension+2,"U1s",C.Htop,source);
    C.mcPartialCacheStats.originalClassProjections:=C.mcPartialCacheStats.originalClassProjections+1;
    if entry<>fail then entry.originalClass:=ShallowCopy(co);fi;
  fi;
  return rec(source:=source,originalClass:=co);
end);

BindGlobal("AFSFullAdjustCF",function(C,x)
  local source,co,adjust,primitive,data;
  data:=AFSFullMCSourceData(C,x);source:=data.source;co:=data.originalClass;
  adjust:=AFSFullAbelianSolve(C.cfPrimary,C.Htop.orders,-co);
  if adjust=fail then return fail;fi;
  x:=ShallowCopy(x);
  if C.mcPartialCacheStats.limit>0 and ForAll(adjust,z->z=0) then
    # The cochain adjustment is identically zero, not just exact or trivial in
    # cohomology. Retain both the original c function and its memoized source.
    C.mcPartialCacheStats.zeroAdjustmentSourceReuses:=C.mcPartialCacheStats.zeroAdjustmentSourceReuses+1;
  else
    x.c:=AFSCoadd(2,[x.c,AFSCombination(C.ctx,C.dimension,"F2",C.Hc,adjust)]);
    source:=AFSFullSource(C.ctx,C.dimension,"bosonic",x);
    C.mcPartialCacheStats.bosonicSourceBuilds:=C.mcPartialCacheStats.bosonicSourceBuilds+1;
  fi;
  # A terminal state does not carry a partial-state cache certificate onward.
  if IsBound(x.partialMCEntry) then Unbind(x.partialMCEntry);fi;
  primitive:=AFSFullCubePrimitive(C,x);
  if primitive=fail then primitive:=AFSFullBinaryPrimitive(C,x);fi;
  if primitive=fail then x.v:=AFSSolve(C.ctx,C.dimension+2,"U1s",source);
  else x.v:=primitive;fi;
  if x.v=fail then Error("CF terminal adjustment did not remove the phase class");fi;
  x.closedCFAdjustment:=adjust;
  return x;
end);

# Evaluate a normalized local lookup on actual group cochains. The integer
# triangle bits precede the closed-character edge bits, as in the certificate.
BindGlobal("AFSFullCharacterLookup",function(c,h,chi,table,denominator)
  return AFSMemo(function(xs...)
    local vertices,g,t,key,bit,i,j,value;
    vertices:=[];g:=Identity(c.G);
    for t in xs do g:=g*t;Add(vertices,g);od;
    key:=0;bit:=1;
    for i in [1..Length(vertices)-1] do for j in [i+1..Length(vertices)] do
      key:=key+bit*h[c.elementIndex(vertices[i])][c.elementIndex(vertices[i]^-1*vertices[j])];bit:=bit*2;
    od;od;
    for g in vertices do key:=key+bit*chi[c.elementIndex(g)];bit:=bit*2;od;
    value:=LookupDictionary(table,key);
    if value=fail then Error("illegal closed character/integral cocycle face pattern");fi;
    return value/denominator;
  end);
end);

BindGlobal("AFSFullCharacterMCLift",function(C,coordinates)
  local c,H1,character,h,chi,v,bar,a,co,old,shift,data,x;
  c:=C.ctx;
  if not c.fullCertifiedCharacterMC or c.s<>AFSZero or c.omega2=AFSZero or
    not IsBound(c.elements) then return fail;fi;
  if not IsBound(C.binaryCharacters) then
    C.binaryCharacters:=List(C.Hn.generators,v->AFSFullBinaryCharacter(C,v));
  fi;
  H1:=AFSFullH(c,1,"F2");
  for character in C.binaryCharacters do
    h:=character.h;
    if not ForAll(c.elements,g->ForAll(c.elements,k->
      CallFuncList(c.omega2,[g,k])=h[c.elementIndex(g)][c.elementIndex(k)])) then continue;fi;
    for v in H1.generators do
      bar:=AFSBar(c,1,"F2",v);chi:=List(c.elements,g->bar(g));
      if not ForAll(chi,z->z in [0,1]) or not ForAll(c.elements,g->ForAll(c.elements,k->
        chi[c.elementIndex(g*k)]=(chi[c.elementIndex(g)]+chi[c.elementIndex(k)]) mod 2)) then
        Error("Majorana lookup input is not a closed binary character");
      fi;
      a:=AFSMemo(function(g1,g2,g3)
        return chi[c.elementIndex(g1)]*h[c.elementIndex(g2)][c.elementIndex(g3)];
      end);
      co:=AFSFullClass(c,3,"F2",C.Ha,a);
      if co<>coordinates then continue;fi;
      old:=AFSCombination(c,3,"F2",C.Ha,coordinates);
      shift:=AFSSolve(c,3,"F2",AFSCoadd(2,[old,a]));
      if shift=fail then Error("character Majorana representative has no exact shift");fi;
      if not IsBoundGlobal("AFS_FULL_CHARACTER_MC_DATA") then
        Read(Concatenation(AFS_ROOT,"/gap/full_character_majorana_data.g"));
      fi;
      data:=ValueGlobal("AFS_FULL_CHARACTER_MC_DATA");
      x:=AFSFullZero();x.a:=a;
      x.c:=AFSFullCharacterLookup(c,h,chi,data.c,1);
      x.v:=AFSFullCharacterLookup(c,h,chi,data.v,16);
      Add(C.characterMCCertificates,rec(identifier:="closed-character-binary-integral-majorana-flat-lift-v1",
        certificateSha256:=data.certificateSha256,majoranaClass:=co,
        nativeOriginalMajorana:=AFSNative(c,3,"F2",old),nativeCharacterMajorana:=AFSNative(c,3,"F2",a),
        nativeRepresentativeShift:=AFSNative(c,2,"F2",shift),nativeCharacter:=v,
        characterValues:=chi,integralLift:=character.nativeInteger,
        integerLiftCharacterValues:=List(character.A,z->[NumeratorRat(z),DenominatorRat(z)]),
        integerLiftShiftValues:=character.integerShift,checkedCharacterAndOmegaPairs:=Length(c.elements)^2,
        scope:="independent flat lift with the same Majorana class; CF and marked phase may change"));
      return x;
    od;
  od;
  return fail;
end);

BindGlobal("AFSFullMCLift",function(C,coordinates,terminal)
  local x,key,entry,stats;
  stats:=C.mcPartialCacheStats;
  if terminal then
    stats.terminalRequests:=stats.terminalRequests+1;
    x:=AFSFullCharacterMCLift(C,coordinates);if x<>fail then return x;fi;
  fi;
  if Length(coordinates)<>Length(C.Ha.orders) or not ForAll(coordinates,IsInt) then
    Error("invalid exact Majorana coordinate vector");
  fi;
  key:=List(coordinates,z->z mod 2);
  stats.partialLiftRequests:=stats.partialLiftRequests+1;entry:=fail;
  if stats.limit>0 then entry:=LookupDictionary(C.mcPartialCache,key);fi;
  if entry<>fail then
    stats.partialCacheHits:=stats.partialCacheHits+1;
    if terminal then stats.cachedTerminalRequests:=stats.cachedTerminalRequests+1;fi;
    x:=ShallowCopy(entry.state);x.partialMCEntry:=entry;
    if AFSFullMCPartialEntryForState(C,x)=fail then Error("partial Majorana cache context changed");fi;
  else
    stats.partialLiftSolves:=stats.partialLiftSolves+1;
    x:=AFSFullZero();
    x.a:=AFSCombination(C.ctx,C.dimension-1,"F2",C.Ha,key);
    x.c:=AFSSolve(C.ctx,C.dimension+1,"F2",AFSFullSource(C.ctx,C.dimension,"fermion",x));
    if x.c=fail then Error("Majorana primary-kernel lift failed");fi;
    if stats.limit>0 and stats.partialStatesStored<stats.limit then
      entry:=rec(owner:=C.mcPartialCacheOwner,dimension:=C.dimension,coordinate:=C.coordinate,
        sign:=C.ctx.s,omega:=C.ctx.omega2,state:=ShallowCopy(x));
      AddDictionary(C.mcPartialCache,ShallowCopy(key),entry);
      stats.partialStatesStored:=stats.partialStatesStored+1;x.partialMCEntry:=entry;
    elif stats.limit>0 then stats.partialCacheBypasses:=stats.partialCacheBypasses+1;fi;
  fi;
  if terminal then return AFSFullAdjustCF(C,x);fi;
  return x;
end);

# A nonzero native pullback certifies that the bar cochain is nonzero. Its
# vanishing is inconclusive: distinct bar values can cancel on a native cell.
# This extra evaluation is reserved for explicit audit runs.
BindGlobal("AFSFullSourceEvidence",function(c,degree,coeff,source)
  local native,values;
  native:=AFSNative(c,degree,coeff,source);values:=native;
  if coeff="U1s" then values:=List(native,x->[NumeratorRat(x),DenominatorRat(x)]);fi;
  return rec(degree:=degree,coefficient:=coeff,nativeValues:=values,
    nonzeroCochainCertifiedByNativeVector:=ForAny(native,x->x<>0),
    zeroNativeVectorMeaning:="inconclusive about pointwise vanishing of the bar cochain",
    allBarValuesZero:="not-tested");
end);

BindGlobal("AFSFullPipTower",function(C,coordinates,page,terminal)
  local c,d,x,out,source,co,adjust,basis,i,raw,rows,nativeInteger,closed,matchedBinary;
  c:=C.ctx;d:=C.dimension;x:=AFSFullZero();
  if IsBound(C.integerBarBasis) then
    x.n:=AFSCoadd(0,List([1..Length(coordinates)],i->AFSComul(0,coordinates[i],C.integerBarBasis[i])));
  else x.n:=AFSCombination(c,d-2,"Zs",C.Hn,coordinates);fi;
  if c.fullCertifiedZeroLowers and d in [3,4] and c.s=AFSZero then
    nativeInteger:=List([1..Dimension(c.R)(d-2)],i->0);
    for i in [1..Length(coordinates)] do
      nativeInteger:=nativeInteger+coordinates[i]*C.Hn.generators[i];
    od;
    closed:=ForAll(nativeInteger*AFSDifferential(c,d-2,"Z"),v->v=0);
    if not IsBound(C.integerBarBasis) and c.omega2=AFSZero and ForAll(nativeInteger,v->v mod 2=0) and closed then
      # The integral comparison chain map preserves both closure and even
      # divisibility pointwise. This is not a test of a native source vector.
      x.closedEvenIntegerCertificate:=rec(identifier:="pip-even-integral-cocycle-zero-lower-v1",nativeInteger:=nativeInteger,
        method:="integral-chain-map-preserves-closed-even-native-cochain");
    fi;
    if d=4 and closed and IsBound(c.elements) then
      matchedBinary:=LookupDictionary(c.fullBinaryIntegerCertificates,nativeInteger);
      if matchedBinary=fail then
        # This checks every group pair, not only comparison-chain support or
        # cohomology equality. Integrality of the chain map proves closure.
        matchedBinary:=ForAll(c.elements,g->ForAll(c.elements,h->
          CallFuncList(x.n,[g,h]) in [0,1] and
          CallFuncList(x.n,[g,h])=CallFuncList(c.omega2,[g,h])));
        AddDictionary(c.fullBinaryIntegerCertificates,ShallowCopy(nativeInteger),matchedBinary);
      fi;
      if matchedBinary then
        x.binaryIntegerOmegaCertificate:=rec(
          identifier:="pip-binary-integral-cocycle-matched-omega-zero-lower-v1",
          nativeInteger:=nativeInteger,omegaFunction:=c.omega2,
          checkedPairs:=Length(c.elements)^2);
      fi;
    fi;
  fi;
  out:=rec(integerClass:=coordinates,state:=x,status:="survives",page:=2);
  if IsBound(x.closedEvenIntegerCertificate) then
    out.lowerSourceCertificate:=StructuralCopy(x.closedEvenIntegerCertificate);
  elif IsBound(x.binaryIntegerOmegaCertificate) then
    out.lowerSourceCertificate:=ShallowCopy(x.binaryIntegerOmegaCertificate);
    Unbind(out.lowerSourceCertificate.omegaFunction);
  fi;
  source:=AFSFullSource(c,d,"majorana",x);
  out.d2:=AFSFullClass(c,d,"F2",C.Hc,source);
  out.finalObstructionClass:=out.d2;out.obstructed:=ForAny(out.d2,v->v<>0);
  if AFSStackAuditEnabled() then out.d2CochainEvidence:=AFSFullSourceEvidence(c,d,"F2",source);fi;
  if out.obstructed then out.status:="killed";return out;fi;
  if page=2 then return out;fi;
  x.a:=AFSSolve(c,d,"F2",source);
  if x.a=fail then Error("integer d2 kernel has no Majorana primitive");fi;
  source:=AFSFullSource(c,d,"fermion",x);
  co:=AFSFullClass(c,d+1,"F2",C.Hf,source);
  out.d3Raw:=co;out.d3:=C.mcPrimaryTarget.project(co);out.page:=3;
  out.finalObstructionClass:=out.d3;out.obstructed:=ForAny(out.d3,v->v<>0);
  if AFSStackAuditEnabled() then out.d3CochainEvidence:=AFSFullSourceEvidence(c,d+1,"F2",source);fi;
  adjust:=AFSFullAbelianSolve(C.mcPrimary,C.Hf.orders,co);
  if adjust=fail then out.status:="killed";return out;fi;
  x.a:=AFSCoadd(2,[x.a,AFSCombination(c,d-1,"F2",C.Ha,adjust)]);
  source:=AFSFullSource(c,d,"fermion",x);x.c:=AFSSolve(c,d+1,"F2",source);
  if x.c=fail then Error("integer d3 Majorana adjustment failed");fi;
  out.majoranaPrimaryAdjustment:=adjust;
  if page=3 then return out;fi;
  source:=AFSFullSource(c,d,"bosonic",x);
  co:=AFSFullClass(c,d+2,"U1s",C.Htop,source);
  out.d4Raw:=co;out.d4:=C.pipPhaseTarget.project(co);out.page:=4;
  out.finalObstructionClass:=out.d4;out.obstructed:=ForAny(out.d4,v->v<>0);
  if AFSStackAuditEnabled() then out.d4CochainEvidence:=AFSFullSourceEvidence(c,d+2,"U1s",source);fi;
  if out.obstructed then out.status:="killed";return out;fi;
  if not terminal then return out;fi;
  # First remove the MC secondary class modulo CF primary images, then
  # recompute the actual representative and remove its remaining CF image.
  rows:=List(C.mcSecondaryRaw,v->C.cfTarget.project(v));
  adjust:=AFSFullAbelianSolve(rows,C.cfTarget.orders,-C.cfTarget.project(co));
  if adjust=fail then Error("integer terminal class lies outside its recorded indeterminacy");fi;
  basis:=List(C.Ha.orders,v->0);
  for i in [1..Length(adjust)] do basis:=basis+adjust[i]*C.mcKernel[i];od;
  x.a:=AFSCoadd(2,[x.a,AFSCombination(c,d-1,"F2",C.Ha,basis)]);
  x.c:=AFSSolve(c,d+1,"F2",AFSFullSource(c,d,"fermion",x));
  if x.c=fail then Error("secondary adjustment destroyed the Majorana primary equation");fi;
  x:=AFSFullAdjustCF(C,x);
  if x=fail then Error("integer terminal secondary adjustment failed");fi;
  out.state:=x;out.majoranaSecondaryAdjustment:=adjust;
  return out;
end);

# Select an ordered cyclic filtration of a finite subgroup. Relative orders
# may have a power relation involving earlier integer generators, which is
# measured by the same full reduction routine as every other relation.
BindGlobal("AFSFullSubgroupBasis",function(S)
  local basis,orders,T,v,x,k;
  basis:=[];orders:=[];T:=AFSD4Subgroup(S.ambientOrders,[]);
  for v in S.elements do
    if v in T.elements then continue;fi;
    x:=ShallowCopy(v);k:=1;
    while not x in T.elements do
      x:=List([1..Length(v)],i->(x[i]+v[i]) mod S.ambientOrders[i]);k:=k+1;
    od;
    Add(basis,v);Add(orders,k);T:=AFSD4Subgroup(S.ambientOrders,basis);
  od;
  if Length(T.elements)<>Length(S.elements) then Error("integer subgroup basis lost elements");fi;
  return rec(basis:=basis,orders:=orders);
end);

# Only a primary cohomology class is needed here. Native cup diagonals give
# the same cohomology operation as the bar formula without expanding its
# comparison chains. The marked flat lift still uses the full matched bar
# source; no native representative is substituted into that coordinate.
BindGlobal("AFSFullCFPrimaryNative",function(C,v)
  local c,d,sq,w,co;
  c:=C.ctx;d:=C.dimension;
  sq:=AFSNativeSq2U1Coordinates(c,d,v,C.Htop);
  if c.omega2=AFSZero then return sq;fi;
  if not IsBound(c.fullNativeOmega) then c.fullNativeOmega:=AFSNative(c,2,"F2",c.omega2);fi;
  w:=AFSNativeCup(c,0,2,c.fullNativeOmega,d,v);
  co:=C.Htop.coordinates(w/2);
  if co=fail then Error("native pure-CF primary operation is not closed");fi;
  return List([1..Length(sq)],i->(sq[i]+co[i]) mod C.Htop.orders[i]);
end);

BindGlobal("AFSFullMCPrimaryNative",function(C,v)
  local c,r,value,beta,co;
  c:=C.ctx;r:=C.dimension-1;
  if r<2 then value:=List([1..Dimension(c.R)(r+2)],i->0);
  else value:=AFSNativeSq2(c,r,v);fi;
  if c.omega2<>AFSZero then
    if not IsBound(c.fullNativeOmega) then c.fullNativeOmega:=AFSNative(c,2,"F2",c.omega2);fi;
    value:=value+AFSNativeCup(c,0,2,c.fullNativeOmega,r,v);
  fi;
  if c.s<>AFSZero then
    # This is the ordinary integral Bockstein of a binary cocycle. Twisting
    # this differential by s would add a different cohomology operation.
    beta:=v*AFSDifferential(c,r,"Z");
    if ForAny(beta,x->x mod 2<>0) then Error("native Majorana input is not closed modulo two");fi;
    beta:=List(beta,x->(x/2) mod 2);
    if not IsBound(c.fullNativeSign) then c.fullNativeSign:=AFSNative(c,1,"F2",c.s);fi;
    value:=value+AFSNativeCup(c,0,1,c.fullNativeSign,r+1,beta);
  fi;
  co:=C.Hf.coordinates(List(value,x->x mod 2));
  if co=fail then Error("native Majorana primary operation is not closed");fi;
  return co;
end);

# For a finite unitary integral cocycle n, averaging its second argument gives
# A(g)=|G|^-1 sum_h n(g,h) with delta A=n. Thus rho=A mod1 is a character,
# b=delta rho is binary, and n-b=delta floor(A). Both the integer lift change
# and the parity-section change are checked on every group pair. Install the
# actual new integer bar representative before computing any tower source.
BindGlobal("AFSFullNormalizeBinaryExtension",function(C)
  local c,H,wco,v,sgn,n,nco,difference,primitive,dprimitive,original,record,
    j,averages,residues,integerShift,binary,shift,dshift,actualNative;
  c:=C.ctx;
  if C.dimension<>4 or C.coordinate<>"publication" or c.s<>AFSZero or not IsBound(c.elements) then
    Error("binary extension normalization requires a finite unitary d4 publication context");
  fi;
  if c.omega2=AFSZero then return;fi;
  H:=AFSFullH(c,2,"F2");wco:=AFSFullClass(c,2,"F2",H,c.omega2);
  if ForAll(wco,x->x=0) then return;fi;
  for j in [1..Length(C.Hn.generators)] do
    v:=C.Hn.generators[j];
    for sgn in [1,-1] do
      n:=AFSBar(c,2,"Z",sgn*v);nco:=AFSFullClass(c,2,"F2",H,n);
      if nco<>wco then continue;fi;
      if not ForAll(sgn*v*AFSDifferential(c,2,"Z"),x->x=0) then
        Error("binary extension candidate is not an integral native cocycle");
      fi;
      averages:=List(c.elements,g->Sum(c.elements,h->CallFuncList(n,[g,h]))/Length(c.elements));
      residues:=List(averages,AFSMod1);integerShift:=averages-residues;
      if not ForAll(integerShift,IsInt) then Error("averaged integer lift shift is not integral");fi;
      binary:=function(g,h)
        return residues[c.elementIndex(g)]+residues[c.elementIndex(h)]-residues[c.elementIndex(g*h)];
      end;
      shift:=g->integerShift[c.elementIndex(g)];dshift:=AFSCoboundary(c,"Z",shift);
      if not ForAll(c.elements,g->ForAll(c.elements,h->
        binary(g,h) in [0,1] and CallFuncList(n,[g,h])-binary(g,h)=CallFuncList(dshift,[g,h]))) then
        Error("averaging failed its complete integer coboundary certificate");
      fi;
      actualNative:=AFSNative(c,2,"Z",binary);
      if C.Hn.coordinates(actualNative)<>C.Hn.coordinates(sgn*v) then
        Error("binary integer lift changed its integral cohomology class");
      fi;
      original:=c.omega2;difference:=AFSCoadd(2,[original,binary]);
      primitive:=AFSSolve(c,2,"F2",difference);
      if primitive=fail then Error("cohomologous extension cocycles have no section primitive");fi;
      dprimitive:=AFSCoboundary(c,"F2",primitive);
      if not ForAll(c.elements,g->ForAll(c.elements,h->
        CallFuncList(dprimitive,[g,h])=CallFuncList(difference,[g,h]))) then
        Error("extension-section change failed its complete pointwise certificate");
      fi;
      record:=rec(method:="finite-unitary-averaging-and-explicit-parity-section-change",
        integerBasisIndex:=j,integerBasisSign:=sgn,originalNativeInteger:=sgn*v,
        normalizedNativeInteger:=actualNative,
        integerShiftNative:=AFSNative(c,1,"Z",shift),
        integerShiftValuesByContextElement:=integerShift,
        characterValuesByContextElement:=List(residues,x->[NumeratorRat(x),DenominatorRat(x)]),
        integerShiftEquation:="original integer cocycle minus binary cocycle equals delta(integerShift)",
        originalNativeOmega:=AFSNative(c,2,"F2",original),
        normalizedNativeOmega:=AFSNative(c,2,"F2",binary),nativeSectionPrimitive:=AFSNative(c,1,"F2",primitive),
        sectionValuesByContextElement:=List(c.elements,g->CallFuncList(primitive,[g])),
        checkedIntegerPairs:=Length(c.elements)^2,checkedExtensionPairs:=Length(c.elements)^2,
        isomorphism:="(parity,g) maps to (parity+section(g),g)");
      C.integerBarBasis:=List(C.Hn.generators,z->AFSBar(c,2,"Z",z));
      C.integerBarBasis[j]:=AFSComul(0,sgn,binary);
      c.omega2:=binary;
      if IsBound(c.fullNativeOmega) then Unbind(c.fullNativeOmega);fi;
      C.binaryExtensionNormalization:=record;return;
    od;
  od;
end);

BindGlobal("AFSFullClassify",function(c,d)
  local C,i,j,x,source,co,nativeCo,kernel,basis,v,S,page,images,target,R,poly,g,split;
  C:=rec(ctx:=c,dimension:=d,status:="running",generators:=[],pipPages:=[]);
  C.mcPartialCacheStats:=rec(limit:=0,partialLiftRequests:=0,partialLiftSolves:=0,
    partialCacheHits:=0,partialCacheBypasses:=0,partialStatesStored:=0,
    bosonicSourceBuilds:=0,originalClassProjections:=0,bosonicSourceHits:=0,
    originalClassHits:=0,zeroAdjustmentSourceReuses:=0,terminalRequests:=0,cachedTerminalRequests:=0,
    scope:="per-classification exact n=0 Majorana states; source counters also include terminal CF adjustments");
  if IsBoundGlobal("AFS_FULL_MC_PARTIAL_CACHE_LIMIT") then
    C.mcPartialCacheStats.limit:=ValueGlobal("AFS_FULL_MC_PARTIAL_CACHE_LIMIT");
  fi;
  if not IsInt(C.mcPartialCacheStats.limit) or not C.mcPartialCacheStats.limit in [0..1024] then
    Error("partial Majorana cache limit must be an integer from zero through 1024");
  fi;
  C.mcPartialCacheOwner:=rec();C.mcPartialCache:=NewDictionary([1],true);
  c.f2ParityFilter:=IsBoundGlobal("AFS_FULL_F2_PARITY_FILTER") and
    ValueGlobal("AFS_FULL_F2_PARITY_FILTER")=true;
  if c.f2ParityFilter and not d in [3,4] then
    Error("F2 parity filtering is currently gated only in spatial dimensions three and four");
  fi;
  c.f2ParityStats:=rec(nativeTerms:=0,nativeEvenTerms:=0,nativeSourceCalls:=0,
    homotopyEvaluations:=0,homotopyBarTerms:=0,homotopyEvenNativeTerms:=0,
    homotopyEvenBarTerms:=0,homotopyDuplicateTerms:=0,homotopySourceCalls:=0,
    homotopyFlushes:=0,maximumBufferedTuples:=0);
  c.bar.f2ParityFilter:=c.f2ParityFilter;c.bar.f2ParitySupportLimit:=4096;
  c.bar.f2ParityStats:=c.f2ParityStats;
  c.fullCertifiedZeroLowers:=IsBoundGlobal("AFS_FULL_CERTIFIED_ZERO_LOWERS") and
    ValueGlobal("AFS_FULL_CERTIFIED_ZERO_LOWERS")=true;
  c.fullZeroLowerCertificateUses:=0;
  c.fullBinaryIntegerCertificates:=NewDictionary([1],true);
  c.fullCanonicalFaceCache:=IsBoundGlobal("AFS_FULL_CANONICAL_FACE_CACHE") and
    ValueGlobal("AFS_FULL_CANONICAL_FACE_CACHE")=true;
  if c.fullCanonicalFaceCache and IsBound(c.elements) and IsBound(c.elementIndex) then
    if not ForAll([1..Length(c.elements)],i->c.elementIndex(c.elements[i])=i) then
      Error("finite face-cache element indices do not match their declared ordering");
    fi;
    c.fullFaceTranslationIndices:=List(c.elements,g->List(c.elements,h->c.elementIndex(g^-1*h)));
  fi;
  C.zeroChiralFiber:=IsBoundGlobal("AFS_FULL_ZERO_CHIRAL_FIBER") and ValueGlobal("AFS_FULL_ZERO_CHIRAL_FIBER")=true;
  if C.zeroChiralFiber and (d<>2 or c.s<>AFSZero or not IsBound(c.elements)) then
    Error("zero-chiral abstract completion requires finite unitary symmetry in spatial dimension two");
  fi;
  C.coordinate:="publication";
  C.cfPrimaryMode:="bar";
  if IsBoundGlobal("AFS_FULL_CF_PRIMARY") then C.cfPrimaryMode:=ValueGlobal("AFS_FULL_CF_PRIMARY");fi;
  if not C.cfPrimaryMode in ["bar","native","compare"] then Error("invalid CF primary evaluation mode");fi;
  C.mcPrimaryMode:="bar";
  if IsBoundGlobal("AFS_FULL_MC_PRIMARY") then C.mcPrimaryMode:=ValueGlobal("AFS_FULL_MC_PRIMARY");fi;
  if not C.mcPrimaryMode in ["bar","native","compare"] then Error("invalid Majorana primary evaluation mode");fi;
  if IsBoundGlobal("AFS_FULL_COORDINATE") then C.coordinate:=ValueGlobal("AFS_FULL_COORDINATE");fi;
  c.fullVacuumMajoranaKernel:=IsBoundGlobal("AFS_FULL_VACUUM_MC_KERNEL") and
    ValueGlobal("AFS_FULL_VACUUM_MC_KERNEL")=true and d=4 and C.coordinate="publication";
  c.fullCertifiedCubePrimitive:=IsBoundGlobal("AFS_FULL_CERTIFIED_CUBE_PRIMITIVE") and
    ValueGlobal("AFS_FULL_CERTIFIED_CUBE_PRIMITIVE")=true and d=4 and C.coordinate="publication";
  C.cubePrimitiveCertificates:=[];
  c.fullCertifiedBinaryPrimitive:=IsBoundGlobal("AFS_FULL_CERTIFIED_BINARY_PRIMITIVE") and
    ValueGlobal("AFS_FULL_CERTIFIED_BINARY_PRIMITIVE")=true and d=4 and C.coordinate="publication";
  C.binaryPrimitiveCertificates:=[];
  c.fullCertifiedCFSquare:=IsBoundGlobal("AFS_FULL_CERTIFIED_CF_SQUARE") and
    ValueGlobal("AFS_FULL_CERTIFIED_CF_SQUARE")=true and d=4 and C.coordinate="publication";
  C.cfSquareCertificates:=[];
  c.fullCertifiedCharacterMC:=IsBoundGlobal("AFS_FULL_CERTIFIED_CHARACTER_MC") and
    ValueGlobal("AFS_FULL_CERTIFIED_CHARACTER_MC")=true and d=4 and C.coordinate="publication";
  C.characterMCCertificates:=[];
  c.fullTraceReduction:=IsBoundGlobal("AFS_FULL_TRACE_REDUCTION") and
    ValueGlobal("AFS_FULL_TRACE_REDUCTION")=true;
  c.fullReductionSerial:=0;
  c.fullVacuumMajoranaKernelUses:=0;
  c.fullVacuumFermionKernel:=IsBoundGlobal("AFS_FULL_VACUUM_CF_KERNEL") and
    ValueGlobal("AFS_FULL_VACUUM_CF_KERNEL")=true and d=4 and C.coordinate="publication";
  c.fullVacuumFermionKernelUses:=0;
  c.fullMajoranaN0Kernel:=IsBoundGlobal("AFS_FULL_MAJORANA_N0_KERNEL") and
    ValueGlobal("AFS_FULL_MAJORANA_N0_KERNEL")=true and d in [3,4] and C.coordinate="publication";
  c.fullMajoranaN0KernelUses:=0;
  c.fullFermionN0Kernel:=IsBoundGlobal("AFS_FULL_FERMION_N0_KERNEL") and
    ValueGlobal("AFS_FULL_FERMION_N0_KERNEL")=true and d in [3,4] and C.coordinate="publication";
  c.fullFermionN0KernelUses:=0;
  c.fullClosedCFSource:=IsBoundGlobal("AFS_FULL_CLOSED_CF_SOURCE") and
    ValueGlobal("AFS_FULL_CLOSED_CF_SOURCE")=true and d=3 and C.coordinate="publication";
  c.fullClosedCFSourceUses:=0;C.closedCFSourceCertificates:=[];
  if not d in [1..4] then
    Error("the complete endpoint supports spatial dimensions one through four");
  fi;
  if d=1 then
    if C.coordinate<>"publication" then Error("dimension one uses the independent fMPS coordinate");fi;
    if C.cfPrimaryMode<>"bar" or C.mcPrimaryMode<>"bar" then
      Error("native primary shortcuts are not enabled for the independent fMPS endpoint");
    fi;
    C.coordinate:="fmps1-turzillo-you-eq44";
  fi;
  # Odd fMPS states and the neutral chiral section require a split extension.
  # Record an explicit parity-section change before moving an exact, nonzero
  # extension representative to zero. This is a change of symmetry section,
  # not the omission of any obstruction or carry in fixed coordinates.
  if d=1 or (d=2 and C.coordinate="publication" and c.s=AFSZero) then
    if c.omega2<>AFSZero then
      co:=AFSFullClass(c,2,"F2",AFSFullH(c,2,"F2"),c.omega2);
      if ForAll(co,x->x=0) then
        split:=AFSSolve(c,2,"F2",c.omega2);
        if split=fail then Error("exact extension cocycle has no splitting");fi;
        C.exactExtensionSplitting:=rec(originalExtension:=AFSNative(c,2,"F2",c.omega2),
          splittingCochain:=AFSNative(c,1,"F2",split),
          convention:="explicit parity-section change to a pointwise-zero extension cocycle");
        c.omega2:=AFSZero;
      fi;
    fi;
  fi;
  # The production worker uses the supplied q=1 CA law in two dimensions.
  # With trivial sign and extension a neutral chiral p+ip phase supplies an
  # explicit Z section. Otherwise the integer sector must be absent.
  if d=2 and C.coordinate="publication" then
    if C.zeroChiralFiber then C.coordinate:="majorana-ca";
    elif c.s=AFSZero and c.omega2=AFSZero then C.coordinate:="split-neutral-chiral-q1-ca";
    else C.coordinate:="majorana-ca";fi;
  fi;
  AFSStage(c,"full_cohomology");
  C.Hn:=AFSFullH(c,d-2,"Zs");C.Ha:=AFSFullH(c,d-1,"F2");
  C.Hc:=AFSFullH(c,d,"F2");C.Hf:=AFSFullH(c,d+1,"F2");
  C.Hphase:=AFSFullH(c,d+1,"U1s");C.Htop:=AFSFullH(c,d+2,"U1s");
  if not C.coordinate in ["publication","split-neutral-chiral-q1-ca","fmps1-turzillo-you-eq44"] then
    if not C.coordinate in ["majorana-ca","majorana-operator"] or not d in [2,4] then
      Error("independent Majorana coordinate requires spatial dimension two or four");
    fi;
    if d=2 and C.Hn.orders<>[] and not C.zeroChiralFiber then
      Error("known 2D Majorana comparison requires an absent degree-zero integer sector");
    fi;
    if AFSFullH(c,d-3,"Zs").orders<>[] then
      Error("Majorana fiber comparison cannot omit a nonzero incoming integer gauge group");
    fi;
    C.Hn:=AFSFullH(c,-1,"Zs");
  fi;
  C.binaryExtensionNormalizationRequested:=IsBoundGlobal("AFS_FULL_NORMALIZE_BINARY_EXTENSION") and
    ValueGlobal("AFS_FULL_NORMALIZE_BINARY_EXTENSION")=true;
  if C.binaryExtensionNormalizationRequested then
    AFSFullNormalizeBinaryExtension(C);
  fi;
  C.cfPrimary:=[];C.mcPrimary:=[];C.mcSecondaryRaw:=[];
  AFSStage(c,"full_cf_primary");
  for i in [1..Length(C.Hc.orders)] do
    if C.cfPrimaryMode<>"native" then
      x:=AFSFullZero();x.c:=AFSBar(c,d,"F2",C.Hc.generators[i]);
      source:=AFSFullSource(c,d,"bosonic",x);
      co:=AFSFullClass(c,d+2,"U1s",C.Htop,source);
    fi;
    if C.cfPrimaryMode<>"bar" then
      nativeCo:=AFSFullCFPrimaryNative(C,C.Hc.generators[i]);
      if C.cfPrimaryMode="compare" and nativeCo<>co then
        Error("native and full bar CF primary classes disagree: ",i," ",nativeCo," ",co);
      fi;
      co:=nativeCo;
    fi;
    Add(C.cfPrimary,co);
  od;
  C.cfKernel:=AFSF2Kernel(List(C.cfPrimary,r->AFSOrderTwoBits(C.Htop.orders,r)),Length(C.Hc.orders));
  C.cfTarget:=AFSQuotient(C.Htop.orders,C.cfPrimary);
  AFSStage(c,"full_mc_primary");
  for i in [1..Length(C.Ha.orders)] do
    if C.mcPrimaryMode<>"native" then
      x:=AFSFullZero();x.a:=AFSBar(c,d-1,"F2",C.Ha.generators[i]);
      source:=AFSFullSource(c,d,"fermion",x);
      co:=AFSFullClass(c,d+1,"F2",C.Hf,source);
    fi;
    if C.mcPrimaryMode<>"bar" then
      nativeCo:=AFSFullMCPrimaryNative(C,C.Ha.generators[i]);
      if C.mcPrimaryMode="compare" and nativeCo<>co then
        Error("native and full bar Majorana primary classes disagree: ",i," ",nativeCo," ",co);
      fi;
      co:=nativeCo;
    fi;
    Add(C.mcPrimary,co);
  od;
  C.mcPrimaryTarget:=AFSQuotient(C.Hf.orders,C.mcPrimary);
  C.mcKernel:=AFSF2Kernel(C.mcPrimary,Length(C.Ha.orders));
  AFSStage(c,"full_mc_secondary");
  for basis in C.mcKernel do
    x:=AFSFullMCLift(C,basis,false);co:=AFSFullMCSourceData(C,x);
    Add(C.mcSecondaryRaw,co.originalClass);
  od;
  kernel:=AFSF2Kernel(List(C.mcSecondaryRaw,r->AFSOrderTwoBits(C.cfTarget.orders,C.cfTarget.project(r))),Length(C.mcKernel));
  C.mcFinal:=[];
  for basis in kernel do
    v:=List(C.Ha.orders,z->0);for i in [1..Length(basis)] do v:=v+basis[i]*C.mcKernel[i];od;
    Add(C.mcFinal,List(v,z->z mod 2));
  od;
  C.mcPartialCacheStats.secondaryCoordinates:=StructuralCopy(C.mcKernel);
  C.mcPartialCacheStats.survivorCoordinates:=StructuralCopy(C.mcFinal);
  C.mcPartialCacheStats.survivorBasisOverlap:=Number(C.mcFinal,v->v in C.mcKernel);
  C.pipPhaseTarget:=AFSQuotient(C.Htop.orders,Concatenation(C.cfPrimary,C.mcSecondaryRaw));
  S:=rec(ambientOrders:=C.Hn.orders,orders:=C.Hn.orders,generators:=IdentityMat(Length(C.Hn.orders)));
  for page in [2..4] do
    AFSStage(c,Concatenation("full_pip_d",String(page)));images:=[];
    if page=2 then target:=C.Hc.orders;
    elif page=3 then target:=C.mcPrimaryTarget.orders;
    else target:=C.pipPhaseTarget.orders;fi;
    R:=rec(page:=page,sourceOrders:=S.orders,targetOrders:=target,evaluations:=[]);
    for v in S.generators do
      x:=AFSFullPipTower(C,v,page,false);
      if x.page<page then Error("integer kernel generator lost an earlier differential");fi;
      co:=x.(Concatenation("d",String(page)));Add(images,co);
      Unbind(x.state);Add(R.evaluations,x);
    od;
    S:=AFSFullAbelianKernel(S,images,target);R.survivingOrders:=S.orders;Add(C.pipPages,R);
  od;
  C.pipSubgroup:=S;poly:=rec(basis:=S.generators,orders:=S.orders);C.pipBasis:=poly;
  # Retain all outward survivors before the incoming quotient. The full
  # incoming states will impose relations on this same measured presentation.
  AFSStage(c,"full_flat_lifts");
  for i in [1..Length(C.Hphase.orders)] do
    x:=AFSFullZero();x.v:=AFSBar(c,d+1,"U1s",C.Hphase.generators[i]);
    Add(C.generators,rec(name:=Concatenation("D",String(i)),layer:=0,order:=C.Hphase.orders[i],state:=x));
  od;
  for i in [1..Length(C.cfKernel)] do
    AFSStage(c,Concatenation("full_flat_cf_",String(i)));
    x:=AFSFullCFSquareLift(C,C.cfKernel[i]);
    if x=fail then
      x:=AFSFullZero();x.c:=AFSCombination(c,d,"F2",C.Hc,C.cfKernel[i]);
      if c.fullClosedCFSource then
        nativeCo:=List([1..Dimension(c.R)(d)],j->0);
        for j in [1..Length(C.Hc.generators)] do
          nativeCo:=nativeCo+C.cfKernel[i][j]*C.Hc.generators[j];
        od;
        nativeCo:=List(nativeCo,z->z mod 2);
        if ForAny(nativeCo*AFSDifferential(c,d,"F2"),z->z mod 2<>0) then
          Error("closed-CF source certificate has a nonclosed native input");
        fi;
        x.closedCFSourceCertificate:=rec(cochain:=x.c,nativeCocycle:=nativeCo);
        Add(C.closedCFSourceCertificates,rec(generator:=Concatenation("C",String(i)),nativeCocycle:=nativeCo,
          certificate:="closed-cf3-current-source-cup1-v1"));
      fi;
      x.v:=AFSSolve(c,d+2,"U1s",AFSFullSource(c,d,"bosonic",x));
    fi;
    if x.v=fail then Error("CF permanent class has no terminal primitive");fi;
    Add(C.generators,rec(name:=Concatenation("C",String(i)),layer:=1,order:=2,state:=x));
  od;
  for i in [1..Length(C.mcFinal)] do
    AFSStage(c,Concatenation("full_flat_majorana_",String(i)));
    x:=AFSFullMCLift(C,C.mcFinal[i],true);
    if x=fail then Error("MC permanent class has no terminal lift");fi;
    Add(C.generators,rec(name:=Concatenation("B",String(i)),layer:=2,order:=2,state:=x));
  od;
  for i in [1..Length(poly.basis)] do
    AFSStage(c,Concatenation("full_flat_pip_",String(i)));
    x:=AFSFullPipTower(C,poly.basis[i],4,true);
    Add(C.generators,rec(name:=Concatenation("P",String(i)),layer:=3,order:=poly.orders[i],state:=x.state));
  od;
  C.status:="computed";return C;
end);

BindGlobal("AFSFullReduce",function(C,target,allowed)
  local c,d,remaining,coordinates,witnesses,layer,indices,H,degree,coeff,field,
    rows,co,answer,i,j,gauge,primitive,correction,entry,note,serial,nativePrimitive;
  c:=C.ctx;d:=C.dimension;remaining:=ShallowCopy(target);
  c.fullReductionSerial:=c.fullReductionSerial+1;serial:=c.fullReductionSerial;
  note:=function(stage)
    if c.fullTraceReduction then
      AFSStage(c,Concatenation("full_reduce_",String(serial),"_",stage));
    fi;
  end;
  coordinates:=List(C.generators,g->0);witnesses:=[];
  for layer in [3,2,1,0] do
    if layer=3 and d=1 then continue;fi;
    if layer=3 then H:=C.Hn;degree:=d-2;coeff:="Zs";field:="n";
    elif layer=2 then H:=C.Ha;degree:=d-1;coeff:="F2";field:="a";
    elif layer=1 then H:=C.Hc;degree:=d;coeff:="F2";field:="c";
    else H:=C.Hphase;degree:=d+1;coeff:="U1s";field:="v";fi;
    note(Concatenation("layer_",String(layer),"_class"));
    indices:=Filtered(allowed,i->C.generators[i].layer=layer);
    co:=AFSFullClass(c,degree,coeff,H,remaining.(field));
    note(Concatenation("layer_",String(layer),"_representatives"));
    rows:=List(indices,i->AFSFullClass(c,degree,coeff,H,C.generators[i].state.(field)));
    answer:=AFSFullAbelianSolve(rows,H.orders,co);
    if answer=fail then Error("stacking target outside the outward surviving layer ",layer," class ",co);fi;
    note(Concatenation("layer_",String(layer),"_subtract"));
    for j in [1..Length(indices)] do
      i:=indices[j];coordinates[i]:=answer[j];
      if answer[j]<>0 then
        correction:=AFSFullPower(c,d,C.generators[i].state,-answer[j]);
        remaining:=AFSFullProduct(c,d,remaining,correction);
      fi;
    od;
    if degree=0 then
      if ForAny(AFSNative(c,0,coeff,remaining.(field)),x->x<>0) then Error("degree-zero exact field is nonzero");fi;
      remaining.(field):=AFSZero;
      Add(witnesses,rec(layer:=layer,classBefore:=co,generatorIndices:=indices,coordinates:=answer,
        certificate:="degree-zero-field-vanishes-pointwise"));
      continue;
    fi;
    note(Concatenation("layer_",String(layer),"_primitive"));
    primitive:=AFSSolve(c,degree,coeff,remaining.(field));
    if primitive=fail then Error("cohomology reduction did not leave an exact field");fi;
    note(Concatenation("layer_",String(layer),"_primitive_native"));
    nativePrimitive:=AFSNative(c,degree-1,coeff,primitive);
    entry:=rec(layer:=layer,classBefore:=co,generatorIndices:=indices,coordinates:=answer,
      primitiveDegree:=degree-1,primitiveCoefficient:=coeff,
      nativePrimitive:=nativePrimitive);
    note(Concatenation("layer_",String(layer),"_gauge"));
    if layer=3 then
      remaining:=AFSFullGauge(c,d,remaining,AFSComul(0,-1,primitive),AFSZero,AFSZero);
      if IsBound(C.reductionProbe) and primitive<>AFSZero then C.reductionProbe(layer,remaining);fi;
      remaining.n:=AFSZero;
    elif layer=2 then
      remaining:=AFSFullGauge(c,d,remaining,AFSZero,primitive,AFSZero);
      if IsBound(C.reductionProbe) and primitive<>AFSZero then C.reductionProbe(layer,remaining);fi;
      remaining.n:=AFSZero;remaining.a:=AFSZero;
    elif layer=1 then
      remaining:=AFSFullGauge(c,d,remaining,AFSZero,AFSZero,primitive);
      if IsBound(C.reductionProbe) and primitive<>AFSZero then C.reductionProbe(layer,remaining);fi;
      remaining.n:=AFSZero;remaining.a:=AFSZero;remaining.c:=AFSZero;
    else remaining.v:=AFSZero;fi;
    Add(witnesses,entry);
    note(Concatenation("layer_",String(layer),"_done"));
  od;
  return rec(coordinates:=coordinates,witnesses:=witnesses,
    certificate:="complete-lower-field-reduction-with-simplicial-cylinder-carries");
end);

BindGlobal("AFSFullStackingClassification",function(C)
  local c,d,n,relations,witnesses,i,j,g,target,reduced,row,layer,H,degree,coeff,
    primitive,lambda,beta,gamma,S,orders,out;
  c:=C.ctx;d:=C.dimension;n:=Length(C.generators);relations:=[];witnesses:=[];
  for i in [1..n] do
    g:=C.generators[i];AFSStage(c,Concatenation("full_relation_",g.name));
    if g.order=0 then
      Add(witnesses,rec(kind:="free-permanent-generator",generator:=g.name,
        certificate:="actual-flat-lift-with-no-finite-power-relation"));
      continue;
    fi;
    if g.layer=0 then
      row:=List([1..n],j->0);row[i]:=g.order;Add(relations,row);
      Add(witnesses,rec(kind:="bosonic-cohomology-order",generator:=g.name,order:=g.order));
    else
      target:=AFSFullPower(c,d,g.state,g.order);
      reduced:=AFSFullReduce(C,target,[1..i-1]);row:=-reduced.coordinates;row[i]:=row[i]+g.order;
      Add(relations,row);Add(witnesses,rec(kind:="full-power-relation",generator:=g.name,order:=g.order,reduction:=reduced));
    fi;
  od;
  # Closed gauge parameters generate the incoming relation subgroup. Their
  # images include all upper carries, even when the first image is exact.
  for layer in [3,2,1] do
    if layer=3 then degree:=d-3;coeff:="Zs";
    elif layer=2 then degree:=d-2;coeff:="F2";
    else degree:=d-1;coeff:="F2";fi;
    H:=AFSFullH(c,degree,coeff);
    for i in [1..Length(H.generators)] do
      AFSStage(c,Concatenation("full_incoming_",String(layer),"_",String(i)));
      primitive:=AFSBar(c,degree,coeff,H.generators[i]);lambda:=AFSZero;beta:=AFSZero;gamma:=AFSZero;
      if layer=3 then lambda:=primitive;elif layer=2 then beta:=primitive;else gamma:=primitive;fi;
      target:=AFSFullGauge(c,d,AFSFullZero(),lambda,beta,gamma);target.n:=AFSZero;
      if layer<3 then target.a:=AFSZero;fi;if layer<2 then target.c:=AFSZero;fi;
      if AFSStackAuditEnabled() and not AFSFullCheckFlat(c,d,target) then
        Error("incoming gauge endpoint is not flat: ",layer," ",i);
      fi;
      reduced:=AFSFullReduce(C,target,[1..n]);Add(relations,reduced.coordinates);
      Add(witnesses,rec(kind:="incoming-gauge-relation",gaugeLayer:=layer,gaugeOrder:=H.orders[i],
        gaugeDegree:=degree,gaugeCoefficient:=coeff,nativeGauge:=H.generators[i],reduction:=reduced));
    od;
  od;
  S:=AFSSmith(relations,Length(relations),n);
  orders:=Concatenation(List([S.rank+1..n],i->0),Filtered(List(S.diag,AbsInt),x->x>1));
  out:=rec(status:="computed",dimension:=d,invariants:=orders,presentation:=relations,
    smith:=S,witnesses:=witnesses,generators:=C.generators,
    scope:="all-supplied-obstructions-and-stacking-twisters-with-full-incoming-gauge-quotient");
  if d<3 then out.scope:="experimental-cone-descent-physical-normalization-not-established";fi;
  if C.coordinate<>"publication" then
    out.scope:="independent-Majorana-fiber-with-absent-incoming-integer-gauge-group";
    if d=2 then out.scope:="known-Majorana-theory-with-absent-integer-sector";fi;
  fi;
  if C.coordinate="split-neutral-chiral-q1-ca" then
    out.scope:="neutral-chiral-integer-section-plus-known-q1-Majorana-theory-trivial-background";
  fi;
  if C.zeroChiralFiber then
    out.scope:="computed-zero-chiral-subgroup-with-known-q1-law";
  fi;
  if C.coordinate="fmps1-turzillo-you-eq44" then
    out.scope:="independent-one-dimensional-fMPS-law-with-full-parity-gauge-quotient";
  fi;
  if AFSStackAuditEnabled() then
    Print("AFS_FULL_PENDING_AUDIT_INVARIANTS ",c.number," dimension=",d," invariants=",orders,"\n");
    AFSStage(c,"full_coherence");out.coherenceAudit:=AFSFullCoherenceAudit(C,out);
    AFSStage(c,"full_coherence_complete");
    if out.coherenceAudit.status="passed-shard" then out.status:="computed-coherence-shard";fi;
  fi;
  return out;
end);

# Coherence is checked in the actual quotient, not by demanding a pointwise
# associative cochain representative. All tiny-model generator triples are
# included; larger models use every generator inverse plus selected triples.
Read(Concatenation(AFS_ROOT,"/gap/full_coherence_shards.g"));
BindGlobal("AFSFullCoherenceAudit",function(C,S)
  local c,d,n,selected,indices,layer,names,i,j,k,x,y,z,left,right,target,reduced,solve,records,check;
  if IsBoundGlobal("AFS_FULL_COHERENCE_SHARDS") and ValueGlobal("AFS_FULL_COHERENCE_SHARDS")>1 then
    return AFSFullCoherenceAuditShard(C,S);
  fi;
  c:=C.ctx;d:=C.dimension;n:=Length(C.generators);
  solve:=AFSStackLatticeSolver(S.presentation,n);records:=[];
  check:=function(kind,indices,target)
    local reduced,relation;
    reduced:=AFSFullReduce(C,target,[1..n]);relation:=solve(reduced.coordinates);
    if relation=fail then Error("complete quotient coherence failed: ",kind," ",indices," ",reduced.coordinates);fi;
    Add(records,rec(kind:=kind,generators:=indices,coordinates:=reduced.coordinates,relationCombination:=relation));
  end;
  for i in [1..n] do
    x:=C.generators[i].state;
    if not AFSFullCheckFlat(c,d,x) then Error("complete marked generator is not flat: ",i);fi;
    y:=AFSFullInverse(c,d,x);
    check("right-inverse",[i],AFSFullProduct(c,d,x,y));
    check("left-inverse",[i],AFSFullProduct(c,d,y,x));
    if C.generators[i].order<>0 then
      target:=AFSFullPower(c,d,x,C.generators[i].order);
      if not AFSFullCheckFlat(c,d,target) then Error("power relation target is not flat: ",i);fi;
    fi;
  od;
  selected:=[1..n];
  if n>4 then
    # Pure bosonic translations cannot reveal a nonlinear associator. Retain
    # every nonbosonic generator when there are at most four; otherwise keep
    # both ends of each nonempty layer, so an early Majorana is never hidden
    # behind numerous bosonic generators in the ordered presentation.
    selected:=Filtered([1..n],i->C.generators[i].layer>0);
    if Length(selected)>4 then
      selected:=[];
      for layer in [1..3] do
        indices:=Filtered([1..n],i->C.generators[i].layer=layer);
        if Length(indices)>0 then AddSet(selected,indices[1]);AddSet(selected,indices[Length(indices)]);fi;
      od;
    fi;
    if Length(selected)=0 then selected:=[1];fi;
  fi;
  if IsBoundGlobal("AFS_FULL_AUDIT_GENERATORS") then
    names:=ValueGlobal("AFS_FULL_AUDIT_GENERATORS");
    selected:=Filtered([1..n],i->C.generators[i].name in names);
    if Length(selected)<>Length(Set(names)) then Error("unknown named coherence-audit generator");fi;
  fi;
  for i in selected do for j in selected do
    x:=C.generators[i].state;y:=C.generators[j].state;
    left:=AFSFullProduct(c,d,x,y);right:=AFSFullProduct(c,d,y,x);
    if not AFSFullCheckFlat(c,d,left) or not AFSFullCheckFlat(c,d,right) then
      Error("product is not flat: ",i," ",j);
    fi;
    check("commutator",[i,j],AFSFullProduct(c,d,left,AFSFullInverse(c,d,right)));
    for k in selected do
      z:=C.generators[k].state;
      left:=AFSFullProduct(c,d,AFSFullProduct(c,d,x,y),z);
      right:=AFSFullProduct(c,d,x,AFSFullProduct(c,d,y,z));
      check("associator",[i,j,k],AFSFullProduct(c,d,left,AFSFullInverse(c,d,right)));
    od;
  od;od;
  return rec(status:="passed",allGeneratorTriples:=Length(selected)=n,selectedGenerators:=selected,
    checks:=records,comparisonSupportFlatness:=true);
end);

BindGlobal("AFSFullEncodeVector",function(v)
  return List(v,x->[NumeratorRat(x),DenominatorRat(x)]);
end);

# The ordinary incoming quotient is generated by closed gauge classes. This
# independent diagnostic also applies nonclosed native cochain parameters to
# the vacuum, then removes their exact lower fields through the complete
# cylinder. Every resulting coordinate must lie in the same relation lattice.
# It checks the reduction/composition assumption rather than adding relations
# chosen to force a desired abstract group.
BindGlobal("AFSFullGaugeNullityAudit",function(C,S,layers)
  local c,d,n,solve,records,layer,degree,coeff,i,v,p,lambda,beta,gamma,
    target,reduced,relation,flat,entry;
  c:=C.ctx;d:=C.dimension;n:=Length(C.generators);
  solve:=AFSStackLatticeSolver(S.presentation,n);records:=[];
  for layer in layers do
    if layer=3 then degree:=d-3;coeff:="Zs";
    elif layer=2 then degree:=d-2;coeff:="F2";
    else degree:=d-1;coeff:="F2";fi;
    if degree<0 then continue;fi;
    if layer=3 and C.coordinate<>"publication" then
      Error("nonclosed integer gauge audit requires full publication coordinates");
    fi;
    for i in [1..Dimension(c.R)(degree)] do
      v:=List([1..Dimension(c.R)(degree)],j->0);v[i]:=1;
      AFSStage(c,Concatenation("full_nonclosed_gauge_",String(layer),"_",String(i)));
      p:=AFSBar(c,degree,coeff,v);lambda:=AFSZero;beta:=AFSZero;gamma:=AFSZero;
      if layer=3 then lambda:=p;elif layer=2 then beta:=p;else gamma:=p;fi;
      target:=AFSFullGauge(c,d,AFSFullZero(),lambda,beta,gamma);
      flat:=AFSFullCheckFlat(c,d,target);
      if not flat then Error("native gauge endpoint failed flatness: ",layer," ",i);fi;
      reduced:=AFSFullReduce(C,target,[1..n]);relation:=solve(reduced.coordinates);
      entry:=rec(layer:=layer,degree:=degree,coefficient:=coeff,nativeParameter:=v,
        flat:=flat,reduction:=reduced,belongsToIncomingRelationLattice:=relation<>fail);
      if relation<>fail then entry.relationCombination:=relation;fi;
      Add(records,entry);
    od;
  od;
  return rec(status:=ForAll(records,r->r.belongsToIncomingRelationLattice),
    checks:=records,scope:="all native basis gauge parameters in the requested layers, including nonclosed parameters");
end);

BindGlobal("AFSFullExport",function(C,S)
  local c,d,out,g,x,w,entry,step,model,integer;
  c:=C.ctx;d:=C.dimension;
  if IsBound(c.model) then model:=c.model.id;else model:=Concatenation("SG",String(c.number));fi;
  out:=rec(schema:="fspt-complete-finite-v1",model:=model,dimension:=d,
    status:=S.status,scope:=S.scope,invariants:=S.invariants,presentation:=S.presentation,
    smithDiagonal:=S.smith.diag,smithRows:=S.smith.U,smithColumns:=S.smith.V,
    rawSurvivingLayers:=rec(pip:=C.pipSubgroup.orders,majorana:=List(C.mcFinal,v->2),
      complexFermion:=List(C.cfKernel,v->2),bosonic:=C.Hphase.orders),
    pipPages:=C.pipPages,generators:=[],witnesses:=[],
    pipDiagnosticSemantics:=rec(
      d2:="cohomology class of the first source; no preceding-layer adjustment quotient",
      d3Raw:="original cohomology class before allowed Majorana adjustment; not a cochain value",
      d3:="final cohomology class modulo allowed Majorana primary images",
      d4Raw:="original cohomology class of the chosen provisional tower; not a cochain value",
      d4:="final cohomology class modulo allowed CF primary and Majorana secondary images",
      obstructed:="true exactly when the final obstruction class on the recorded page is nontrivial",
      cochainEvidence:="audit-only native source vectors; a zero native vector does not prove a zero bar cochain"),
    formulaCoordinates:=C.coordinate,zeroChiralFiber:=C.zeroChiralFiber,
    canonicalFaceCache:=c.fullCanonicalFaceCache,
    certifiedZeroLowerSources:=c.fullCertifiedZeroLowers,
    certifiedZeroLowerSourceUses:=c.fullZeroLowerCertificateUses,
    certifiedCubePrimitive:=c.fullCertifiedCubePrimitive,
    cubePrimitiveCertificates:=C.cubePrimitiveCertificates,
    certifiedBinaryPrimitive:=c.fullCertifiedBinaryPrimitive,
    binaryPrimitiveCertificates:=C.binaryPrimitiveCertificates,
    certifiedCFSquare:=c.fullCertifiedCFSquare,cfSquareCertificates:=C.cfSquareCertificates,
    certifiedCharacterMajorana:=c.fullCertifiedCharacterMC,characterMCCertificates:=C.characterMCCertificates,
    reductionStageTrace:=c.fullTraceReduction,
    vacuumMajoranaKernel:=c.fullVacuumMajoranaKernel,
    vacuumMajoranaKernelUses:=c.fullVacuumMajoranaKernelUses,
    vacuumFermionKernel:=c.fullVacuumFermionKernel,
    vacuumFermionKernelUses:=c.fullVacuumFermionKernelUses,
    majoranaN0Kernel:=c.fullMajoranaN0Kernel,majoranaN0KernelUses:=c.fullMajoranaN0KernelUses,
    fermionN0Kernel:=c.fullFermionN0Kernel,fermionN0KernelUses:=c.fullFermionN0KernelUses,
    closedCFSource:=c.fullClosedCFSource,closedCFSourceUses:=c.fullClosedCFSourceUses,
    closedCFSourceCertificates:=C.closedCFSourceCertificates,
    partialMajoranaCache:=C.mcPartialCacheStats,
    f2ParityFilter:=c.f2ParityFilter,f2ParitySupportLimit:=c.bar.f2ParitySupportLimit,
    f2ParityStats:=c.f2ParityStats,
    binaryExtensionNormalizationRequested:=C.binaryExtensionNormalizationRequested,
    cfPrimaryEvaluation:=C.cfPrimaryMode,
    mcPrimaryEvaluation:=C.mcPrimaryMode,
    obstructionMaps:=rec(complexFermionPrimary:=C.cfPrimary,majoranaPrimary:=C.mcPrimary,
      majoranaSecondaryOriginal:=C.mcSecondaryRaw),
    gaugeMethod:="normalized-simplicial-cylinder-transgression",
    formulaWorkerRequests:=0,
    resolutionDimensions:=List([0..d+3],i->Dimension(c.R)(i)),stageTimings:=c.stageTimings);
  if IsBound(c.fullFormulaTransport) then
    out.formulaWorkerRequests:=c.fullFormulaTransport.requests;
    out.formulaIntegerVectorCache:=IsBound(c.fullFormulaTransport.vectorCache);
    out.formulaIntegerVectorCacheLookups:=c.fullFormulaTransport.vectorCacheLookups;
    out.formulaIntegerVectorCacheHits:=c.fullFormulaTransport.vectorCacheHits;
  fi;
  for g in S.generators do
    x:=g.state;
    integer:=[];if d>=2 then integer:=AFSNative(c,d-2,"Zs",x.n);fi;
    Add(out.generators,rec(name:=g.name,layer:=g.layer,quotientOrder:=g.order,
      integer:=integer,majorana:=AFSNative(c,d-1,"F2",x.a),
      complexFermion:=AFSNative(c,d,"F2",x.c),phase:=AFSFullEncodeVector(AFSNative(c,d+1,"U1s",x.v))));
  od;
  for w in S.witnesses do
    entry:=StructuralCopy(w);
    if IsBound(entry.reduction) then
      for step in entry.reduction.witnesses do
        if IsBound(step.primitiveCoefficient) and step.primitiveCoefficient="U1s" then step.nativePrimitive:=AFSFullEncodeVector(step.nativePrimitive);fi;
      od;
    fi;
    Add(out.witnesses,entry);
  od;
  if IsBound(S.coherenceAudit) then out.coherenceAudit:=S.coherenceAudit;fi;
  if IsBound(C.exactExtensionSplitting) then out.exactExtensionSplitting:=C.exactExtensionSplitting;fi;
  if IsBound(C.binaryExtensionNormalization) then out.binaryExtensionNormalization:=C.binaryExtensionNormalization;fi;
  if C.zeroChiralFiber then
    out.abstractChiralCompletion:=rec(invariants:=Concatenation([0],S.invariants),
      zeroChiralInvariants:=S.invariants,
      scope:="full-abstract-group-only-no-marked-chiral-cochains",
      theorem:="nonzero chiral image mZ from an odd fermionic representation; free quotient splits abstractly",
      minimalChiralIndex:="not-computed",markedFreeGenerator:="not-computed",
      presentationScope:="main presentation and witnesses describe only the zero-chiral subgroup");
  fi;
  if IsBound(S.seededBarAudit) then out.seededBarAudit:=S.seededBarAudit;fi;
  if IsBound(S.gaugeNullityAudit) then
    out.gaugeNullityAudit:=StructuralCopy(S.gaugeNullityAudit);
    for entry in out.gaugeNullityAudit.checks do
      for step in entry.reduction.witnesses do
        if IsBound(step.primitiveCoefficient) and step.primitiveCoefficient="U1s" then
          step.nativePrimitive:=AFSFullEncodeVector(step.nativePrimitive);
        fi;
      od;
    od;
  fi;
  out.cpuMs:=Runtime();return out;
end);
