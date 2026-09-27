if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
Read(Concatenation(AFS_ROOT,"/gap/backend.g"));;
Read(Concatenation(AFS_ROOT,"/gap/backend_smith_transfer.g"));;
for sg in [7,47] do
  c:=AFSBackend(sg);;
  for k in [1..5] do
    # Arbitrary, generally nonclosed normalized phase cochain.
    f:=function(xs...)
      local j,value;
      if One(c.G) in xs then return 0;fi;
      value:=3;
      for j in [1..Length(xs)] do value:=value*(Sum(xs[j]!.exponents)^2+j)+Sum(xs[j]!.exponents);od;
      return AFSMod1(value/8);
    end;;
    old:=AFSNative(c,k,"U1s",f);;new:=AFSNativeU1Smith(c,k,f);;
    if old<>new then Error("complete Smith-basis native transfer differs on arbitrary phase cochain");fi;
    if AFSSolveNative(c,k,"U1s",old)<>AFSSolveNative(c,k,"U1s",new) then Error("canonical Smith primitive differs");fi;
    if AFSNativeU1Smith(c,k,AFSZero)<>List(old,x->0) then Error("Smith transfer zero shortcut");fi;
  od;
  Print("SMITH_NATIVE_ARBITRARY_PASS sg=",sg," degrees=1..5\n");
od;
Print("AFS_SMITH_NATIVE_TEST_PASS\n");QUIT_GAP(0);
