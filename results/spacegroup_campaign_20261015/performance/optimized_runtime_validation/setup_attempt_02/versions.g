U1_ROOT:="/home/user/xyren/AllFSPT_insulator/validations/gap_o2_80d565d_20261015/source";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;
info:=rec(gapVersion:=GAPInfo.Version,architecture:=GAPInfo.Architecture,packages:=rec());;
for name in ["HAP","Cryst","CrystCat","Polycyclic"] do
 package:=PackageInfo(name)[1];;info.packages.(name):=rec(version:=package.Version,path:=package.InstallationPath);;
od;
out:=OutputTextFile("/home/user/xyren/AllFSPT_insulator/validations/gap_o2_80d565d_20261015/validation_o2/versions.json",false);;SetPrintFormattingStatus(out,false);;
WriteLine(out,U1JSON(info));;CloseStream(out);;QUIT_GAP(0);
