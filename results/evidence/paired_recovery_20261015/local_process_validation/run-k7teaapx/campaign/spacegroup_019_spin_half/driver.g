U1_ROOT:="/home/xingyu/AllFSPT_reviews/stop_helper_local_validation_20261015/run-k7teaapx/snapshot";;
U1_INPUT:=rec(id:="spacegroup_019_spin_half");;
output:=OutputTextFile("/home/xingyu/AllFSPT_reviews/stop_helper_local_validation_20261015/run-k7teaapx/campaign/spacegroup_019_spin_half/native.json",false);;
CloseStream(output);;
Print("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\n");;
U1_INPUT:=rec(id:="spacegroup_019_spinless");;
output:=OutputTextFile("/home/xingyu/AllFSPT_reviews/stop_helper_local_validation_20261015/run-k7teaapx/campaign/spacegroup_019_spinless/native.json",false);;
CloseStream(output);;
Print("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\n");;
