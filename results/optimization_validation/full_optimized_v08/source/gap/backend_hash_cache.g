# Optional exact memoization using GAP's official sparse hash dictionary.
# Hashes select buckets only; LookupDictionary still compares full keys.
# Plain immediate-integer lists have canonical payload bytes. Large integers
# use a residue hash (collisions remain exact); other key types use a constant
# hash rather than hashing object addresses or converting keys to strings.
BindGlobal("AFSExactKeyHash",function(key)
  local values;
  if not IsList(key) or not ForAll(key,IsInt) then return 0;fi;
  if ForAll(key,IsSmallIntRep) then
    if IsPlistRep(key) then values:=key;else values:=List(key,x->x);fi;
  else values:=List(key,x->x mod 268435399);fi;
  return HashKeyBag(values,193,GAPInfo.BytesPerVariable,Length(values)*GAPInfo.BytesPerVariable);
end);
DeclareRepresentation("IsAFSExactHashCacheRep",IsComponentObjectRep,["hash"]);
BindGlobal("AFSExactHashCacheType",NewType(DictionariesFamily,
  IsAFSExactHashCacheRep and IsLookupDictionary and IsMutable));
BindGlobal("AFSNewHashCache",function(arg...)
  local hashfun;
  hashfun:=AFSExactKeyHash;if Length(arg)>0 then hashfun:=arg[1];fi;
  return Objectify(AFSExactHashCacheType,rec(hash:=SparseHashTable(hashfun)));
end);
InstallMethod(LookupDictionary,"AFS exact sparse cache",true,
  [IsAFSExactHashCacheRep and IsLookupDictionary,IsObject],0,function(cache,key)
    local entry;
    entry:=LookupDictionary(cache!.hash,key);
    if entry=fail then return fail;fi;
    return entry[1];
  end);
InstallOtherMethod(AddDictionary,"AFS exact sparse cache with replacement",true,
  [IsAFSExactHashCacheRep and IsLookupDictionary and IsMutable,IsObject,IsObject],0,
  function(cache,key,value)
    local entry;
    entry:=LookupDictionary(cache!.hash,key);
    if entry=fail then AddDictionary(cache!.hash,Immutable(key),[value]);
    else entry[1]:=value;fi;
  end);
InstallMethod(KnowsDictionary,"AFS exact sparse cache including fail values",true,
  [IsAFSExactHashCacheRep and IsLookupDictionary,IsObject],0,
  function(cache,key) return LookupDictionary(cache!.hash,key)<>fail;end);
BindGlobal("AFSHashMemo",function(f)
  local cache;
  cache:=AFSNewHashCache();
  return function(xs...)
    local key,value;
    key:=AFSKey(xs);value:=LookupDictionary(cache,key);
    if value=fail then
      value:=CallFuncList(f,xs);
      AddDictionary(cache,key,value);
    fi;
    return value;
  end;
end);
