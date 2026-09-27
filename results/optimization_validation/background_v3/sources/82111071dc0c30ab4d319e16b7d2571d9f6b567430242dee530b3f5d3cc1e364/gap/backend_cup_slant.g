# Evaluate the fixed right cochain during the higher-diagonal recursion.
# All chains here are native chains modulo two; no cohomology assumptions.
BindGlobal("AFSSlantRecord",function(c,q,b)
 local key,T;
 if not IsBound(c.slantCache) then c.slantCache:=NewDictionary([1],true);fi;
 key:=Concatenation([q],List(b,x->x mod 2));T:=LookupDictionary(c.slantCache,key);
 if T=fail then
  T:=rec(ctx:=c,q:=q,b:=List(b,x->x mod 2),D0:=[],D1:=[],transpose:=[],alpha:=NewDictionary([1],true));
  AddDictionary(c.slantCache,key,T);
 fi;
 return T;
end);
BindGlobal("AFSSlantReduce",function(terms)
 return List(Filtered(AFSCombineChain(terms,false),t->t[1] mod 2=1),t->[1,t[2],t[3]]);
end);
BindGlobal("AFSSlantAlpha",function(T,i,g)
 local key,v,x;
 key:=Concatenation([i],AFSKey([g]));v:=LookupDictionary(T.alpha,key);
 if v=fail then
  v:=0;
  for x in AFSDiagonalContract(T.ctx.bar,T.q-1,i,g) do v:=v+x[1]*T.b[x[2]];od;
  v:=v mod 2;AddDictionary(T.alpha,key,v);
 fi;
 return v;
end);
DeclareGlobalFunction("AFSD0Slant");
InstallGlobalFunction(AFSD0Slant,function(T,p,i)
 local c,terms,w,t,g,v;
 c:=T.ctx;
 if not IsBound(T.D0[p+1]) then T.D0[p+1]:=[];fi;
 if IsBound(T.D0[p+1][i]) then return T.D0[p+1][i];fi;
 terms:=[];
 if p=0 then
  v:=Sum(AFSDiagonalAugmentation(c,T.q,i),t->t[1]*T.b[t[2]]) mod 2;
  if v=1 then terms:=[[1,1,Identity(c.G)]];fi;
 else
  for w in BoundaryMap(c.R)(p+T.q,i) do
   g:=c.R!.elts[w[2]];
   for t in AFSD0Slant(T,p-1,AbsInt(w[1])) do Add(terms,[1,t[2],g*t[3]]);od;
  od;
  terms:=AFSDiagonalContractWord(c.bar,p-1,AFSSlantReduce(terms));
 fi;
 T.D0[p+1][i]:=terms;return terms;
end);
BindGlobal("AFSD0TransposeSlant",function(T,p,i)
 local c,terms,w,t,g,cap;
 c:=T.ctx;
 if not IsBound(T.transpose[p+1]) then T.transpose[p+1]:=[];fi;
 if IsBound(T.transpose[p+1][i]) then return T.transpose[p+1][i];fi;
 terms:=[];cap:=Maximum(T.q-1,p);
 for w in BoundaryMap(c.R)(T.q+p,i) do
  g:=c.R!.elts[w[2]];
  for t in AFSHigherDiagonalCapped(c,0,T.q+p-1,AbsInt(w[1]),cap) do
   if t[1]=T.q-1 and t[4]=p and AFSSlantAlpha(T,t[2],g*t[3])=1 then
    Add(terms,[1,t[5],g*t[6]]);
   fi;
  od;
 od;
 terms:=AFSSlantReduce(terms);T.transpose[p+1][i]:=terms;return terms;
end);
DeclareGlobalFunction("AFSD1Slant");
InstallGlobalFunction(AFSD1Slant,function(T,p,i)
 local c,terms,w,t,g;
 if p=0 then return [];fi;c:=T.ctx;
 if not IsBound(T.D1[p+1]) then T.D1[p+1]:=[];fi;
 if IsBound(T.D1[p+1][i]) then return T.D1[p+1][i];fi;
 terms:=Concatenation(AFSD0Slant(T,p-1,i),AFSD0TransposeSlant(T,p-1,i));
 for w in BoundaryMap(c.R)(p+T.q-1,i) do
  g:=c.R!.elts[w[2]];
  for t in AFSD1Slant(T,p-1,AbsInt(w[1])) do Add(terms,[1,t[2],g*t[3]]);od;
 od;
 terms:=AFSDiagonalContractWord(c.bar,p-1,AFSSlantReduce(terms));
 T.D1[p+1][i]:=terms;return terms;
end);
BindGlobal("AFSNativeCup1Slant",function(c,p,a,q,b)
 local T,i,out;
 T:=AFSSlantRecord(c,q,b);out:=[];
 for i in [1..Dimension(c.R)(p+q-1)] do
  Add(out,Sum(AFSD1Slant(T,p,i),t->t[1]*a[t[2]]) mod 2);
 od;
 return out;
end);
