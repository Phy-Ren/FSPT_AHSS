# Same finite input and operations, with its supplied small generating set.
Read(Concatenation(AFS_ROOT,"/gap/full_resolution.g"));;
AFS_FINITE_RESOLUTION_OVERRIDE:=function(P,depth)
  return AFSFullInputGeneratorsResolution(P,depth,AFSFULL_MODEL);
end;;
Read(Concatenation(AFS_ROOT,"/gap/run_full_finite.g"));;
