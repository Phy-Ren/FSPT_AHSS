if not IsBound(AFS_ROOT) then AFS_ROOT:="/home/user/xyren/AllFSPT";fi;
# Select exactly the production scalar obstruction runner; both G variants
# below use it. The original non-compiled vector control remains separate.
Read(Concatenation(AFS_ROOT,"/gap/formula_fast.g"));;
Read(Concatenation(AFS_ROOT,"/tests/bench_backend_bar_mod2.g"));;
