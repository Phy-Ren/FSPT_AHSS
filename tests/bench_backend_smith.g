AFS_ROOT:="/home/user/xyren/AllFSPT";;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=230; fi;
c:=AFSBackend(AFS_SG);;
for k in [4,5] do
 t:=Runtime();; D:=AFSDifferential(c,k,"Zs");;
 Print("SMITH_DIFF ",k," ",Runtime()-t," shape=",Length(D),",",Length(D[1]),"\n");
 t:=Runtime();; S:=SmithNormalFormIntegerMatTransforms(D);;
 Print("SMITH_NORMAL ",k," ",Runtime()-t,"\n");
 t:=Runtime();; Ui:=Inverse(S.rowtrans);;
 Print("SMITH_UI ",k," ",Runtime()-t,"\n");
 t:=Runtime();; Vi:=Inverse(S.coltrans);;
 Print("SMITH_VI ",k," ",Runtime()-t,"\n");
od;
Print("AFS_SMITH_BENCH_PASS\n");QUIT_GAP(0);
