OnBreak:=function() Where(10);QUIT_GAP(1);end;;
U1_ROOT:="/home/xingyu/FSPT_AHSS_insulator";;Read(Concatenation(U1_ROOT,"/gap/load.g"));
# Exercise projected Smith kernels independently of classified groups.
kernelChecks:=0;;
for M in [[[2,3],[3,2]],[[1,2],[4,1]],[[2,0],[0,3]],[[0,0],[0,0]]] do
 for orders in [[4,6],[3,5],[2,8]] do
  K:=U1MapKernel(M,orders,2);;Ki:=Inverse(K);;
  for x in [-12..12] do for y in [-12..12] do
   v:=[x,y];;image:=v*M;;
   belongs:=ForAll([1,2],i->image[i] mod orders[i]=0);;
   if belongs<>ForAll(v*Ki,IsInt) then Error("Unsaturated obstruction kernel");fi;
   kernelChecks:=kernelChecks+1;
  od;od;
 od;
od;
Print("SATURATED_KERNEL_CHECKS=",kernelChecks,"\n");
# Catalog indexing must intertwine the nonabelian table and the actual group.
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_12_spinless.g"));;
c:=U1CatalogContext(U1_INPUT,6);;
es:=List([1..U1_INPUT.order],i->First(Elements(c.G),g->c.elementIndex(g)=i));;
for i in [1..Length(es)] do for j in [1..Length(es)] do
 if c.elementIndex(es[i]*es[j])<>U1_INPUT.multiplication[i][j]+1 then Error("Finite catalog product indexing");fi;
od;od;
Print("NONABELIAN_TABLE_CHECKS=",Length(es)^2,"\n");
# A repeated state object across backgrounds must not inherit the previous source.
c0:=U1CyclicContext(2,0,0,0);;c1:=U1NewContext(c0.G,c0.R,c0.s,c0.rho,function(g,h) return QuoInt(g!.exponents[1]+h!.exponents[1],2)/2;end,0);;
q:=function(g,h) if IsOne(g) or IsOne(h) then return 0;fi;return 1;end;;a:=rec(sheet:=U1Zero,charge:=q,phase:=U1Zero);;
f0:=U1Source(c0,2,a);;f1:=U1Source(c1,2,a);;
fresh:=U1Source(c1,2,rec(sheet:=U1Zero,charge:=q,phase:=U1Zero));;
g:=GeneratorsOfGroup(c1.G)[1];;
Print("SOURCE_CACHE_REUSE=",[f1(g,g,g,g),fresh(g,g,g,g)],"\n");
# Charge stabilizer gauges must give the same incoming image on nonzero roots.
for spin in ["spinless","spin_half"] do
 Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_05_",spin,".g"));;
 c:=U1CatalogContext(U1_INPUT,6);;result:=U1Classify(c,3);;
 HP:=U1Cohomology(c,4,"U1s");;HL:=U1Cohomology(c,2,"Zr");;
 states:=Concatenation(c.classificationStates.charge,c.classificationStates.sheet);;
 comparisons:=[];;
 barChecks:=0;;es:=Filtered(Elements(c.G),g->not IsOne(g));;
 tuples:=List([0..11],i->List([0..4],j->es[((i+1)*(j+1)+QuoInt(i,3)) mod Length(es)+1]));;
 for a in states do
  da:=U1Coboundary(c,"U1s",a.phase);;source:=U1Source(c,3,a);;
  for xs in tuples do
   if U1Mod1(CallFuncList(da,xs)-CallFuncList(source,xs))<>0 then Error("Completed bar source closure failed");fi;
   barChecks:=barChecks+1;
  od;
 od;
 Print("COMPLETED_BAR_CHECKS_",spin,"=",barChecks,"\n");
 for z in HL.generators do
  v:=U1Bar(c,2,"Zr",z);;vac:=U1Gauge(c,3,U1Vacuum(),U1Zero,v);;
  vacCo:=HP.coordinates(U1Native(c,4,"U1s",vac.phase));;
  for a in states do
   ga:=U1Gauge(c,3,a,U1Zero,v);;diff:=U1Product(c,3,ga,U1Inverse(c,3,a));;
   co:=HP.coordinates(U1Native(c,4,"U1s",diff.phase));;
   Add(comparisons,rec(vacuum:=vacCo,onRoot:=co));;
   if co<>vacCo then Error("Nonzero root stabilizer differs from vacuum incoming image");fi;
  od;
 od;
 Print("ROOT_STABILIZER_",spin,"=",U1JSON(comparisons),"\n");
od;
QUIT_GAP(0);
