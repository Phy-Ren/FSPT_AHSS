U1_ROOT:="/home/user/xyren/AllFSPT_insulator/runs/abelian4p1_batch2_20261016/native_benchmark/source";;
U1_FORMULA_PYTHON:="/home/user/xyren/AllFSPT_insulator/runtime4p1-v015/bin/python3";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
Read(Concatenation(U1_ROOT,"/gap/abelian4p1.g"));;
result:=U1AbelianFourData([2,2,2],"compare");;
out:=OutputTextFile("/home/user/xyren/AllFSPT_insulator/runs/abelian4p1_batch2_20261016/native_benchmark/compare/internal_abelian_2x2x2_4p1/native.json",false);;
SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(result));;CloseStream(out);;QUIT_GAP(0);
