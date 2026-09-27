# Exact integer unit-pivot preconditioning for large differential matrices.
# Every elementary operation updates its inverse simultaneously.
InstallGlobalFunction(AFSSmithUnits,function(M,n,m)
  local A,U,Ut,Vt,Vi,k,p,q,i,j,row,weight,best,cand,a,tmp,r,
        S,lo,hi,small,diag;
  if n=0 or m=0 then return AFSSmith(M,n,m); fi;
  A:=List(M,ShallowCopy); U:=IdentityMat(n); Ut:=IdentityMat(n);
  Vt:=IdentityMat(m); Vi:=IdentityMat(m); k:=1;
  while k<=Minimum(n,m) do
    p:=fail; q:=fail; best:=m+1;
    for i in [k..n] do
      cand:=fail; weight:=0;
      for j in [k..m] do
        if A[i][j]<>0 then
          weight:=weight+1;
          if cand=fail and AbsInt(A[i][j])=1 then cand:=j; fi;
        fi;
      od;
      if cand<>fail and weight<best then p:=i; q:=cand; best:=weight; fi;
      if best=1 then break; fi;
    od;
    if p=fail then break; fi;
    if p<>k then
      tmp:=A[k]; A[k]:=A[p]; A[p]:=tmp;
      tmp:=U[k]; U[k]:=U[p]; U[p]:=tmp;
      tmp:=Ut[k]; Ut[k]:=Ut[p]; Ut[p]:=tmp;
    fi;
    if q<>k then
      for row in A do tmp:=row[k]; row[k]:=row[q]; row[q]:=tmp; od;
      tmp:=Vt[k]; Vt[k]:=Vt[q]; Vt[q]:=tmp;
      tmp:=Vi[k]; Vi[k]:=Vi[q]; Vi[q]:=tmp;
    fi;
    if A[k][k]=-1 then
      A[k]:=-A[k]; U[k]:=-U[k];
      Ut[k]:=-Ut[k];
    fi;
    for i in [k+1..n] do
      a:=A[i][k];
      if a<>0 then
        A[i]:=A[i]-a*A[k]; U[i]:=U[i]-a*U[k]; Ut[k]:=Ut[k]+a*Ut[i];
      fi;
    od;
    for j in [k+1..m] do
      a:=A[k][j];
      if a<>0 then
        A[k][j]:=0; Vt[j]:=Vt[j]-a*Vt[k]; Vi[k]:=Vi[k]+a*Vi[j];
      fi;
    od;
    k:=k+1;
  od;
  r:=k-1;
  if r<Minimum(n,m) then
    lo:=[r+1..n]; hi:=[r+1..m]; small:=List(lo,i->A[i]{hi});
    S:=AFSSmith(small,n-r,m-r);
    U{lo}:=S.U*U{lo};
    # Ut=(U^-1)^T and Vt=V^T, so composition remains row operations.
    Ut{lo}:=TransposedMat(S.Ui)*Ut{lo};
    Vt{hi}:=TransposedMat(S.V)*Vt{hi};
    Vi{hi}:=S.Vi*Vi{hi};
    for i in lo do A[i]{hi}:=S.D[i-r]; od;
    r:=r+S.rank;
  fi;
  diag:=List([1..Minimum(n,m)],i->A[i][i]);
  return rec(U:=U,V:=TransposedMat(Vt),Ui:=TransposedMat(Ut),Vi:=Vi,
    D:=A,rank:=r,diag:=diag);
end);
