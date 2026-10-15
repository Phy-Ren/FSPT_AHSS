OnBreak:=function() Where(8);QUIT_GAP(1);end;;
U1_ROOT:="/home/xingyu/AllFSPT_reviews/sg221_native_dag_20261015/source";;U1_USE_KOSZUL:=true;;Read(Concatenation(U1_ROOT,"/gap/load.g"));;
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/spacegroup_221_spinless.g"));;
c:=U1CatalogContext(U1_INPUT,6);;
r:=rec(sheetD1:=U1Differential(c,1,"Zs"),chargeD3:=U1Differential(c,3,"Zr"),phaseD4:=U1Differential(c,4,"Zs"),phaseD5:=U1Differential(c,5,"Zs"));;
o:=OutputTextFile("/home/xingyu/AllFSPT_reviews/sg221_native_dag_20261015/differentials.json",false);;SetPrintFormattingStatus(o,false);;PrintTo(o,U1JSON(r),"\n");;CloseStream(o);;QUIT_GAP(0);
