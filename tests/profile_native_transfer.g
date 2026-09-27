if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_smith_transfer.g"));;
if not IsBound(AFS_SG) then AFS_SG:=219;fi;
c:=AFSBackend(AFS_SG);;t:=Runtime();;terms:=0;;
for i in [1..Dimension(c.R)(5)] do
  chain:=AFSChainToBar(c.bar,5,i);;terms:=terms+Length(chain);
  if i mod 10=0 or i=Dimension(c.R)(5) then
    Print("F5_ONLY_PROGRESS sg=",AFS_SG," cell=",i," cpu_ms=",Runtime()-t," terms=",terms,"\n");
  fi;
od;
Print("F5_ONLY_COMPLETE cpu_ms=",Runtime()-t," terms=",terms,"\n");
f:=function(xs...) local z;z:=Length(xs);return z-z;end;;
if f=AFSZero then Error("profile callback must avoid canonical-zero shortcut");fi;
t:=Runtime();;v:=AFSNative(c,5,"U1s",f);;
Print("F5_ZERO_TRAVERSAL cpu_ms=",Runtime()-t,"\n");
c.smithTransferProgress:=function(k,i,n,nt,ms)
  if i mod 10=0 or i=n then Print("SMITH_F_ONLY_PROGRESS column=",i,"/",n," terms=",nt," cpu_ms=",ms,"\n");fi;
end;;
t:=Runtime();;w:=AFSNativeU1Smith(c,5,f);;
if v<>w then Error("zero native transfer differs");fi;
Print("SMITH_F_ONLY_COMPLETE cpu_ms=",Runtime()-t,"\n");
Print("AFS_NATIVE_TRANSFER_PROFILE_PASS\n");QUIT_GAP(0);
