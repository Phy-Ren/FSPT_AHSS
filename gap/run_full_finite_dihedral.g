# Diagnostic alternate resolution, with unchanged symmetry and background.
Read(Concatenation(AFS_ROOT,"/gap/full_resolution.g"));;
AFS_FINITE_RESOLUTION_OVERRIDE:=AFSFullDihedralPermutationResolution;;
Read(Concatenation(AFS_ROOT,"/gap/run_full_finite.g"));;
