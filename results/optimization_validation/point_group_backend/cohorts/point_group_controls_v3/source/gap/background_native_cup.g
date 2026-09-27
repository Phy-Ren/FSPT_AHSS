# Exact cup_0 on native F2 cochains through the existing D0 marginal.
# Optional module: no global dispatch or existing implementation is replaced.
# A marginal term is [left basis, left group element, right basis]. Both
# group labels act trivially on F2. This is the SAME native D0 as the full
# tensor implementation, not a comparison with the bar Alexander--Whitney map.

BindGlobal("AFSBackgroundNativeCup0Forms",function(ctx,p,q)
  local key,forms,i,pairs,on,index,t,pair,pos;
  if not IsInt(p) or not IsInt(q) or p<0 or q<0 then
    Error("native F2 cup0 requires nonnegative integer degrees");fi;
  key:=Concatenation(String(p),"_",String(q));
  if not IsBound(ctx.backgroundCup0PairCache) then
    ctx.backgroundCup0PairCache:=rec();fi;
  if IsBound(ctx.backgroundCup0PairCache.(key)) then
    return ctx.backgroundCup0PairCache.(key);fi;
  forms:=[];
  for i in [1..Dimension(ctx.R)(p+q)] do
    pairs:=[];on:=[];index:=NewDictionary([1,1],true);
    for t in AFSDiagonalRightComponent(ctx,p,q,i) do
      pair:=[t[1],t[3]];pos:=LookupDictionary(index,pair);
      if pos=fail then
        Add(pairs,pair);Add(on,true);
        AddDictionary(index,pair,Length(pairs));
      else on[pos]:=not on[pos];fi;
    od;
    Add(forms,pairs{Filtered([1..Length(pairs)],j->on[j])});
  od;
  ctx.backgroundCup0PairCache.(key):=forms;
  return forms;
end);

BindGlobal("AFSBackgroundNativeCup0",function(ctx,p,a,q,b)
  local forms,out,pairs,t,value;
  if Length(a)<>Dimension(ctx.R)(p) or Length(b)<>Dimension(ctx.R)(q) then
    Error("native F2 cup0 vector degree mismatch");fi;
  if not ForAll(a,IsInt) or not ForAll(b,IsInt) then
    Error("native F2 cup0 accepts integral representatives only");fi;
  forms:=AFSBackgroundNativeCup0Forms(ctx,p,q);out:=[];
  for pairs in forms do
    value:=0;
    for t in pairs do value:=value+a[t[1]]*b[t[2]];od;
    Add(out,value mod 2);
  od;
  return out;
end);
