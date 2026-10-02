# Optional tensor resolution, transported to the unchanged finite input.
Read(Concatenation(AFS_ROOT,"/gap/full_resolution.g"));;
AFS_FINITE_RESOLUTION_OVERRIDE:=function(P,depth)
  return AFSFullDirectProductResolution(P,depth,AFS_FULL_DIRECT_PRODUCT_FAMILY);
end;;
Read(Concatenation(AFS_ROOT,"/gap/run_full_finite.g"));;
