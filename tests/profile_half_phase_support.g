if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
if not IsBound(AFS_SG) then AFS_SG:=219;fi;
c:=AFSBackend(AFS_SG);;t:=Runtime();;totalTerms:=0;;oddTerms:=0;;
for i in [1..Dimension(c.R)(5)] do
  chain:=AFSChainToBar(c.bar,5,i);;
  totalTerms:=totalTerms+Length(chain);oddTerms:=oddTerms+Number(chain,t->t[1] mod 2=1);
  if i mod 10=0 or i=Dimension(c.R)(5) then
    Print("HALF_SUPPORT_PROGRESS sg=",AFS_SG," cell=",i," total=",totalTerms," odd=",oddTerms," cpu_ms=",Runtime()-t,"\n");
  fi;
od;
Print("AFS_HALF_SUPPORT_PROFILE_PASS\n");QUIT_GAP(0);
