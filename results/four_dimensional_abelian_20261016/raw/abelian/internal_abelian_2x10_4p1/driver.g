U1_ROOT:="/home/user/xyren/AllFSPT_insulator/runs/abelian4p1_batch2_20261016/campaign/source";;
U1_FORMULA_PYTHON:="/home/user/xyren/AllFSPT_insulator/runtime4p1-v015/bin/python3";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
Read(Concatenation(U1_ROOT,"/gap/abelian4p1.g"));;
result:=U1AbelianFourData([2,10]);;
out:=OutputTextFile("/home/user/xyren/AllFSPT_insulator/runs/abelian4p1_batch2_20261016/campaign/output/internal_abelian_2x10_4p1/native.json",false);;
SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(result));;CloseStream(out);;QUIT_GAP(0);
