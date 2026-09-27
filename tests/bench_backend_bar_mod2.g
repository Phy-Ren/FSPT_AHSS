if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_mod2_contraction.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_bar_mod2.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formula_data.g"));;
Read(Concatenation(AFS_ROOT,"/gap/formulas.g"));;
if not IsBound(AFS_SG) then AFS_SG:=219;fi;
c:=AFSBackend(AFS_SG);;H:=AFSCohomology(c,3,"F2");;
if Length(H.generators)=0 then Error("benchmark needs H3 generator");fi;
if not IsBound(AFS_BASIS_INDEX) then AFS_BASIS_INDEX:=1;fi;
v:=H.generators[AFS_BASIS_INDEX];;
# The same native generator, same formula, and same degree-five F map.
# Only the G map used by the F2 callback differs.
cb:=AFSBarMod2(c,3,v);;
ob:=AFSFormula("obstruction",c,rec(p:=2,a:=AFSZero,c:=cb));;
t:=Runtime();;nv:=AFSNative(c,5,"U1s",ob);;
Print("MOD2_G_CF_PHASE sg=",AFS_SG," index=",AFS_BASIS_INDEX," cpu_ms=",Runtime()-t," vector=",nv,"\n");
cb:=AFSBar(c,3,"F2",v);;
ob:=AFSFormula("obstruction",c,rec(p:=2,a:=AFSZero,c:=cb));;
t:=Runtime();;iv:=AFSNative(c,5,"U1s",ob);;
Print("INTEGRAL_G_CF_PHASE sg=",AFS_SG," index=",AFS_BASIS_INDEX," cpu_ms=",Runtime()-t," vector=",iv,"\n");
if nv<>iv then Error("mod2/integer G full CF phase native vectors differ");fi;
Print("AFS_MOD2_G_CF_PHASE_PASS sg=",AFS_SG,"\n");
QUIT_GAP(0);
