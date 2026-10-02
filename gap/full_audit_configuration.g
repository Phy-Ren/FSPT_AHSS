# Validate configured names after the marked generators exist, before any
# power relations, incoming gauges or coherence reductions are evaluated.
# These are the same strict membership checks used by the audit routines.
BindGlobal("AFSFullValidateAuditSelectors",function(C)
  local names,indices;
  if IsBoundGlobal("AFS_FULL_COHERENCE_SHARDS") then
    if not AFSStackAuditEnabled() or not IsBoundGlobal("AFS_FULL_COHERENCE_SHARD_INDEX") then
      Error("coherence sharding requires an enabled audit and an explicit index");
    fi;
    AFSFullCoherenceShardPlan(C,ValueGlobal("AFS_FULL_COHERENCE_SHARDS"),
      ValueGlobal("AFS_FULL_COHERENCE_SHARD_INDEX"));
  fi;
  if IsBoundGlobal("AFS_FULL_AUDIT_GENERATORS") then
    names:=ValueGlobal("AFS_FULL_AUDIT_GENERATORS");
    indices:=Filtered([1..Length(C.generators)],i->C.generators[i].name in names);
    if Length(indices)<>Length(Set(names)) then Error("unknown named coherence-audit generator");fi;
  fi;
  if IsBoundGlobal("AFS_FULL_BAR_AUDIT_SAMPLES") then
    names:=ValueGlobal("AFS_FULL_BAR_AUDIT_GENERATORS");
    indices:=Filtered([1..Length(C.generators)],i->C.generators[i].name in names);
    if Length(indices)<>Length(Set(names)) then Error("unknown marked generator in seeded bar audit");fi;
  fi;
end);

BindGlobal("AFSFullStackingWithValidatedAuditSelectors",function(C)
  AFSFullValidateAuditSelectors(C);
  return AFSFullStackingClassification(C);
end);
