# Optional explicit free-layer constructions. This file does not change the
# production finite/torsion classification or marked stacking engine.

BindGlobal("AFSFreePipUnitaryLifts",function(C)
  local ctx,Hp,indices,states,i,n,coordinates;
  ctx:=C.ctx;if ctx.s<>AFSZero or (IsBound(ctx.omega2) and ctx.omega2<>AFSZero) then return fail;fi;
  Hp:=C.Hp;
  indices:=Filtered([1..Length(Hp.orders)],i->Hp.orders[i]=0);
  states:=[];
  for i in indices do
    n:=AFSBar(ctx,1,"Zs",Hp.generators[i]);
    coordinates:=List(Hp.orders,z->0);coordinates[i]:=1;
    Add(states,rec(n:=n,b:=AFSZero,c:=AFSZero,v:=AFSZero,
      nativeInteger1:=Hp.generators[i],integerCohomologyIndex:=i,
      h1Coordinates:=coordinates,
      construction:="unitary-primitive-integer-character-with-zero-lower-tower"));
  od;
  return rec(status:="computed",rank:=Length(states),generators:=states,
    freeIndices:=indices,latticeBasis:=IdentityMat(Length(indices)),
    survivingParityBasis:=IdentityMat(Length(indices)),parityCandidates:=[],
    latticeIndex:=1,certificate:="s=B=C=0-identically-annihilates-full-normalized-O5");
end);

# Complete one already surviving integer tower with its actual full phase.
# This is the generic incoming-image solve; it does not impose n=s, invoke a
# C4 shortcut, or alter the original classification object's torsion tower.
BindGlobal("AFSFreePipCompleteTower",function(C)
  local ctx,n,b,c,O,co,rows,mc,i,row,solve,sol,mcCoefficients,cfCoefficients,Q,v;
  ctx:=C.ctx;n:=C.pipLiftData.n;b:=C.pipLiftData.b;c:=C.pipLiftData.c;
  O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
  co:=C.H5U.coordinates(AFSNative(ctx,5,"U1s",O));
  if co=fail then Error("free defining tower has nonclosed O5");fi;
  mcCoefficients:=List(C.mcLifts,z->0);cfCoefficients:=List(C.H3.orders,z->0);
  if ForAny(co,z->z<>0) then
    rows:=ShallowCopy(C.cfPrimaryRows);
    for mc in C.mcLifts do
      if IsBound(mc.obstructionCoordinates) then Add(rows,mc.obstructionCoordinates);
      else Add(rows,List(C.H5U.orders,z->0));fi;
    od;
    for i in [1..Length(C.H5U.orders)] do
      row:=List(C.H5U.orders,z->0);row[i]:=C.H5U.orders[i];Add(rows,row);
    od;
    solve:=AFSStackLatticeSolver(rows,Length(C.H5U.orders));sol:=solve(-co);
    if sol=fail then Error("surviving free tower outside full incoming image");fi;
    mcCoefficients:=List(sol{[Length(C.H3.orders)+1..Length(C.H3.orders)+Length(C.mcLifts)]},z->z mod 2);
    for i in [1..Length(mcCoefficients)] do
      if mcCoefficients[i]=1 then b:=AFSCoadd(2,[b,C.mcLifts[i].a]);fi;
    od;
    if ForAny(mcCoefficients,z->z<>0) then
      Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=n,b:=b));
      c:=AFSSolve(ctx,4,"F2",Q);
      if c=fail then Error("free MC adjustment lost its CF primitive");fi;
      O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
      co:=C.H5U.coordinates(AFSNative(ctx,5,"U1s",O));
      if co=fail then Error("adjusted free O5 is nonclosed");fi;
    fi;
    rows:=ShallowCopy(C.cfPrimaryRows);
    for i in [1..Length(C.H5U.orders)] do
      row:=List(C.H5U.orders,z->0);row[i]:=C.H5U.orders[i];Add(rows,row);
    od;
    solve:=AFSStackLatticeSolver(rows,Length(C.H5U.orders));sol:=solve(-co);
    if sol=fail then Error("free MC adjustment left a secondary residual");fi;
    cfCoefficients:=List(sol{[1..Length(C.H3.orders)]},z->z mod 2);
    c:=AFSCoadd(2,[c,AFSCombination(ctx,3,"F2",C.H3,cfCoefficients)]);
    O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
  fi;
  v:=AFSSolve(ctx,5,"U1s",O);
  if v=fail then Error("free defining tower has no full phase primitive");fi;
  return rec(n:=n,b:=b,c:=c,v:=v,mcIndeterminacyAdjustment:=mcCoefficients,
    cfIndeterminacyAdjustment:=cfCoefficients,
    construction:="direct-surviving-parity-tower-with-full-phase-primitive");
end);

BindGlobal("AFSFreePipCandidate",function(C,coordinates)
  local copied,n,source,co,result;
  copied:=ShallowCopy(C);
  if IsBound(C.ctx.omega2) and C.ctx.omega2<>AFSZero then copied.pipCandidateOrderBound:=16;fi;
  n:=AFSCombination(C.ctx,1,"Zs",C.Hp,coordinates);
  source:=AFSFormula("pip_majorana",C.ctx,rec(p:=1,n:=n));
  co:=C.H3.coordinates(AFSNative(C.ctx,3,"F2",source));
  if co=fail then Error("integer parity candidate has nonclosed first source");fi;
  if ForAny(co,z->z<>0) then
    return rec(status:="killed",page:=2,h1Coordinates:=coordinates,obstruction:=co);
  fi;
  result:=AFSClassifyPipTorsion(copied,n,source);
  result:=ShallowCopy(result);result.h1Coordinates:=coordinates;
  if result.status="survives" then result.classification:=copied;fi;
  return result;
end);

BindGlobal("AFSFreePipRREF",function(rows,width)
  local M,pivots,row,col,found,i,tmp;
  M:=List(rows,ShallowCopy);pivots:=[];row:=1;
  for col in [1..width] do
    found:=First([row..Length(M)],i->M[i][col]=1);
    if found=fail then continue;fi;
    tmp:=M[row];M[row]:=M[found];M[found]:=tmp;
    for i in [1..Length(M)] do
      if i<>row and M[i][col]=1 then M[i]:=List(M[i]+M[row],z->z mod 2);fi;
    od;
    Add(pivots,col);row:=row+1;
    if row>Length(M) then break;fi;
  od;
  return rec(rows:=M{[1..Length(pivots)]},pivots:=pivots);
end);

BindGlobal("AFSFreePipPullbackEven",function(ctx,character,universal)
  local map,c,v;
  map:=AFSMemo(g->universal.context.pairElement(character(g),ctx.s(g)));
  c:=AFSMemo(function(xs...) return CallFuncList(universal.c,List(xs,map));end);
  v:=AFSMemo(function(xs...) return CallFuncList(universal.v,List(xs,map));end);
  return rec(n:=AFSComul(0,2,character),b:=AFSZero,c:=c,v:=v,
    construction:="proved-signed-character-pullback-of-even-infinite-dihedral-tower");
end);

BindGlobal("AFSFreePipLifts",function(C)
  local ctx,Hp,free,torsion,r,unitary,candidates,projected,mask,bits,tmask,
    coordinates,i,candidate,chosen,rref,sp,nonpivots,states,basis,row,position,
    state,universal,character,result;
  ctx:=C.ctx;Hp:=C.Hp;free:=Filtered([1..Length(Hp.orders)],i->Hp.orders[i]=0);
  r:=Length(free);
  unitary:=AFSFreePipUnitaryLifts(C);if unitary<>fail then return unitary;fi;
  if r=0 then return rec(status:="computed",rank:=0,generators:=[],freeIndices:=[],
    latticeBasis:=[],survivingParityBasis:=[],latticeIndex:=1,parityCandidates:=[],
    certificate:="no-free-integer-layer");fi;
  torsion:=Filtered([1..Length(Hp.orders)],i->Hp.orders[i]<>0);
  if not ForAll(torsion,i->Hp.orders[i]=2) then Error("unexpected integer H1 torsion");fi;
  candidates:=[];projected:=[];chosen:=[];
  if IsBoundGlobal("AFSStage") then AFSStage(ctx,"free_pip_parity_candidates");fi;
  # Enumerate only H1/2H1 (rank at most three for these space groups), never
  # lower FSPT states. The universal even tower proves this quotient suffices.
  for mask in [1..2^r-1] do
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,Concatenation("free_pip_parity_",String(mask)));fi;
    bits:=List([1..r],i->QuoInt(mask,2^(i-1)) mod 2);
    for tmask in [0..2^Length(torsion)-1] do
      coordinates:=List(Hp.orders,z->0);
      for i in [1..r] do coordinates[free[i]]:=bits[i];od;
      for i in [1..Length(torsion)] do coordinates[torsion[i]]:=QuoInt(tmask,2^(i-1)) mod 2;od;
      candidate:=AFSFreePipCandidate(C,coordinates);Add(candidates,candidate);
      if candidate.status="survives" then
        Add(projected,bits);Add(chosen,candidate);break;
      elif candidate.status<>"killed" then Error("undetermined free parity candidate");fi;
    od;
  od;
  rref:=AFSFreePipRREF(projected,r);sp:=AFSSpan(r);
  for row in rref.rows do AFSInsert(sp,row);od;
  if Length(projected)<>2^Length(rref.rows)-1 or
      not ForAll(projected,row->ForAll(AFSReduce(sp,row).remainder,z->z=0)) then
    Error("surviving free parity projections are not their full F2 span");fi;
  nonpivots:=Filtered([1..r],i->not i in rref.pivots);
  states:=[];basis:=[];
  for row in rref.rows do
    position:=Position(projected,row);
    if position=fail then Error("RREF parity row lacks a directly tested survivor");fi;
    candidate:=chosen[position];
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,"free_pip_surviving_phase_lift");fi;
    state:=AFSFreePipCompleteTower(candidate.classification);
    state.h1Coordinates:=candidate.h1Coordinates;
    Add(states,state);Add(basis,row);
  od;
  if Length(nonpivots)>0 then
    if IsBoundGlobal("AFSStage") then AFSStage(ctx,"free_pip_even_dihedral_pullback");fi;
    universal:=AFSInfiniteDihedralEvenLift(AFSInfiniteDihedralContext());
    for i in nonpivots do
      character:=AFSBar(ctx,1,"Zs",Hp.generators[free[i]]);
      state:=AFSFreePipPullbackEven(ctx,character,universal);
      coordinates:=List(Hp.orders,z->0);coordinates[free[i]]:=2;
      state.h1Coordinates:=coordinates;
      Add(states,state);row:=List([1..r],j->0);row[i]:=2;Add(basis,row);
    od;
  fi;
  if Length(states)<>r or AbsInt(DeterminantMat(basis))<>2^(r-Length(rref.rows)) then
    Error("proposed free marked vectors are not the primitive surviving lattice basis");fi;
  result:=rec(status:="computed",rank:=r,generators:=states,freeIndices:=free,
    latticeBasis:=basis,survivingParityBasis:=rref.rows,parityCandidates:=candidates,
    latticeIndex:=2^(r-Length(rref.rows)),
    certificate:="universal-2H-survival-and-complete-joint-parity-kernel");
  return result;
end);

BindGlobal("AFSFreePipFromClassification",function(C)
  local result,x;
  if IsBound(C.ctx.omega2) and C.ctx.omega2<>AFSZero then
    result:=AFSBackgroundFreePipLifts(C);
  else result:=AFSFreePipLifts(C);fi;
  for x in result.generators do
    if C.Hp.coordinates(AFSNative(C.ctx,1,"Zs",x.n))<>x.h1Coordinates then
      Error("free lift differs from its certified primitive lattice vector");fi;
  od;
  return result;
end);

BindGlobal("AFSFreePipExport",function(C,result)
  local out,encode,i,x,g,record,candidate,field;
  encode:=v->List(v,z->[NumeratorRat(z),DenominatorRat(z)]);
  out:=rec(status:=result.status,rank:=result.rank,freeIndices:=result.freeIndices,
    latticeBasis:=result.latticeBasis,latticeIndex:=result.latticeIndex,
    survivingParityBasis:=result.survivingParityBasis,certificate:=result.certificate,
    generators:=[],parityCandidates:=[],sourceFiles:=["gap/pip_free.g"],
    h1BasisOrders:=C.Hp.orders,h1BasisNative1:=C.Hp.generators,
    certificateLevel:="explicit-universal-pullback-or-comparison-homotopy-primitive",
    checkedComparisonSupport:=ForAll(result.generators,x->
      IsBound(x.checkedFlatComparisonSupport) and x.checkedFlatComparisonSupport),
    fullFreePhaseWitness:=true);
  if IsBound(result.period) then out.certifiedIntegerPeriod:=result.period;out.sourceFiles:=["gap/pip_free.g","gap/background_free.g"];fi;
  for i in [1..Length(result.generators)] do
    x:=result.generators[i];g:=rec(name:=Concatenation("Pfree",String(i)),
      h1Coordinates:=x.h1Coordinates,integer1:=AFSNative(C.ctx,1,"Zs",x.n),
      majorana2:=AFSNative(C.ctx,2,"F2",x.b),fermion3:=AFSNative(C.ctx,3,"F2",x.c),
      phase4:=encode(AFSNative(C.ctx,4,"U1s",x.v)),construction:=x.construction);
    for field in ["mcIndeterminacyAdjustment","cfIndeterminacyAdjustment"] do
      if IsBound(x.(field)) then g.(field):=x.(field);fi;
    od;
    Add(out.generators,g);
  od;
  for candidate in result.parityCandidates do
    record:=rec();
    for field in RecNames(candidate) do
      if field<>"classification" then record.(field):=candidate.(field);fi;
    od;
    Add(out.parityCandidates,record);
  od;
  return out;
end);

# An actual infinite-dihedral context with its rank-one translation kernel.
# The two Pcp generators are r,t, with r^2=1 and r t r=t^-1. In the normal
# form r^e t^k, n=(-1)^e k is an integer cocycle with orientation sign (-1)^e.
BindGlobal("AFSInfiniteDihedralContext",function()
  local G,pc,r,t,P,p,h,L,RL,RP,section,c;
  G:=DihedralGroup(IsPcpGroup,infinity);pc:=Pcp(G);
  r:=pc[1];t:=pc[2];P:=CyclicGroup(IsPcGroup,2);p:=GeneratorsOfGroup(P)[1];
  h:=GroupHomomorphismByImages(G,P,[r,t],[p,One(P)]);
  if h=fail then Error("infinite-dihedral orientation quotient failed");fi;
  L:=Kernel(h);RL:=ResolutionNilpotentGroup(L,6);
  RP:=ResolutionFiniteGroup(P,6,false,0,"extendible");
  section:=function(x) if x=One(P) then return One(G);else return r;fi;end;
  c:=rec(number:=0,G:=G,differentialCache:=rec(),smithCache:=rec(),
    cohomologyCache:=rec(),f2SolveCache:=rec(),reflection:=r,translation:=t);
  c.sign:=AFSMemo(g->(-1)^ExponentsByPcp(pc,g)[1]);c.action:=c.sign;
  c.s:=AFSMemo(g->ExponentsByPcp(pc,g)[1] mod 2);
  c.integerCharacter:=AFSMemo(g->c.sign(g)*ExponentsByPcp(pc,g)[2]);
  c.pairElement:=function(n,s) return r^s*t^((-1)^s*n);end;
  c.R:=AFSExtensionResolution(h,RL,RP,section);c.bar:=AFSComparison(c.R);
  return c;
end);

BindGlobal("AFSInfiniteDihedralEvenLift",function(ctx)
  local n,b,Q,c,O,v;
  n:=AFSComul(0,2,ctx.integerCharacter);b:=AFSZero;
  Q:=AFSFormula("pip_parity",ctx,rec(p:=1,n:=n,b:=b));
  c:=AFSSolve(ctx,4,"F2",Q);
  if c=fail then Error("universal even dihedral CF primitive is obstructed");fi;
  O:=AFSFormula("pip_obstruction",ctx,rec(p:=1,n:=n,b:=b,c:=c));
  v:=AFSSolve(ctx,5,"U1s",O);
  if v=fail then Error("universal even dihedral full phase primitive is obstructed");fi;
  return rec(n:=n,b:=b,c:=c,v:=v,context:=ctx,
    construction:="full-infinite-dihedral-even-character-tower");
end);
