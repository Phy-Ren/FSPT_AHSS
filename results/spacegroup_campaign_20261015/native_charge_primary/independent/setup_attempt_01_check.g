OnBreak:=function() Where(12);QUIT_GAP(1);end;;
REVIEW_ROOT:="/home/xingyu/AllFSPT_reviews/z2_charge_primary_reuse_20261015";;
U1_ROOT:=Concatenation(REVIEW_ROOT,"/source");;
U1_USE_KOSZUL:=true;;U1_USE_MOD2_CONTRACTION:=true;;U1_USE_MOD2_BAR:=false;;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
Read(Concatenation(REVIEW_ROOT,"/backend_mod2_contraction.g"));;
Read(Concatenation(REVIEW_ROOT,"/backend_diagonal.g"));;
rows:=[];;
for n in [1,2,4,6,14,19] do
  for spin in ["spinless","spin_half"] do
    label:=String(n);while Length(label)<3 do label:=Concatenation("0",label);od;
    Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/spacegroup_",label,"_",spin,".g"));
    t:=Runtime();c:=U1CatalogContext(U1_INPUT,6);setupMs:=Runtime()-t;
    if not ForAll(Concatenation(U1_INPUT.omega),x->IsInt(2*Rat(x))) then Error("Omega is not half integral");fi;
    HQ:=U1Cohomology(c,3,"Zr");HO:=U1Cohomology(c,5,"U1s");
    w:=U1Native(c,2,"F2",function(g,h) return (2*c.omega(g,h)) mod 2;end);
    if ForAny(w*U1Differential(c,2,"F2"),x->x mod 2<>0) then Error("w is not closed");fi;
    witnesses:=[];
    for q in HQ.generators do
      if ForAny(q*U1Differential(c,3,"Zr"),x->x<>0) then Error("q is not integrally closed");fi;
      qb:=List(q,x->x mod 2);
      t:=Runtime();v:=U1NativeCupI(c,2,3,0,w,qb)+U1NativeSq2(c,3,qb);
      v:=List(v,x->(x mod 2)/2);nativeCoordinates:=HO.coordinates(v);nativeMs:=Runtime()-t;
      if nativeCoordinates=fail then Error("Native half phase is not closed");fi;
      t:=Runtime();barVector:=U1Native(c,5,"U1s",U1ChargeSource(c,3,U1Bar(c,3,"Zr",q)));
      barCoordinates:=HO.coordinates(barVector);barMs:=Runtime()-t;
      if barCoordinates=fail or nativeCoordinates<>barCoordinates then Error("Native and bar classes disagree");fi;
      difference:=List(barVector-v,U1Mod1);primitive:=U1SolveNative(c,5,"U1s",difference);
      if primitive=fail then Error("Class difference has no exact native primitive");fi;
      if ForAny(primitive*U1Differential(c,4,"Zs")-difference,x->not IsInt(x)) then Error("Primitive does not bound the difference");fi;
      Add(witnesses,rec(integerCharge:=q,nativeBinaryOmega:=w,
        nativeHalfPhase:=v,barHalfPhase:=barVector,
        classCoordinates:=nativeCoordinates,differencePrimitive:=primitive,
        nativeMilliseconds:=nativeMs,barMilliseconds:=barMs));
    od;
    row:=rec(id:=U1_INPUT.id,setupMilliseconds:=setupMs,chargeOrders:=HQ.orders,
      phaseTargetOrders:=HO.orders,witnesses:=witnesses,
      halfIntegralOmegaVerified:=true,integerChargeClosureVerified:=true,
      binaryOmegaClosureVerified:=true,allClassesEqual:=true,
      allDifferencePrimitivesVerified:=true);
    Add(rows,row);Print("PRIMARY_CLASS_PASS ",U1_INPUT.id," ",Length(witnesses)," charge roots\n");
    out:=OutputTextFile(Concatenation(REVIEW_ROOT,"/result.json"),false);SetPrintFormattingStatus(out,false);
    PrintTo(out,U1JSON(rec(rows:=rows,fullClassificationPerformed:=false)),"\n");CloseStream(out);
  od;
od;
Print("ALL_PRIMARY_CLASS_CHECKS_PASS\n");QUIT_GAP(0);
