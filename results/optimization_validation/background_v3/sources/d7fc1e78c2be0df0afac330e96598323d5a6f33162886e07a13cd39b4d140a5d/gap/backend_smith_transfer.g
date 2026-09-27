# Optional exact U1_s native transfer in a complete unimodular Smith basis.
# If U D_(k-1) V=S, evaluate every column of V before reconstructing the
# canonical native vector a=mod1(w V^-1). No closedness/exactness assumption.
# In particular, dividing the wrapped w directly would choose a different
# torsion branch and is deliberately not done here.
BindGlobal("AFSNativeU1Smith",function(c,k,f)
  local n,s,columns,w,i,chain,t,value,start;
  if k<1 then Error("Smith native transfer requires degree >= 1");fi;
  n:=Dimension(c.R)(k);
  if f=AFSZero or n=0 then return List([1..n],i->0);fi;
  s:=AFSDifferentialSmith(c,k-1,"Zs");columns:=TransposedMat(s.V);
  w:=List([1..n],i->0);start:=Runtime();
  for i in [1..n] do
    chain:=AFSChainToBarCombination(c.bar,k,columns[i]);value:=0;
    for t in chain do
      value:=value+t[1]*c.sign(t[2])*CallFuncList(f,t[3]);
    od;
    w[i]:=AFSMod1(value);
    if IsBound(c.smithTransferProgress) then
      c.smithTransferProgress(k,i,n,Length(chain),Runtime()-start);
    fi;
  od;
  return List(w*s.Vi,AFSMod1);
end);
