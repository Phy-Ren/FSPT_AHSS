# Opt-in wrapper; the ordinary campaign entry point remains unchanged.
Read(Concatenation(AFS_ROOT,"/gap/full_resolution.g"));;
AFS_FINITE_RESOLUTION_OVERRIDE:=function(G,depth)
  return AFSFullTensorAbelianResolution(G,depth);
end;;
Read(Concatenation(AFS_ROOT,"/gap/run_full_finite.g"));;
