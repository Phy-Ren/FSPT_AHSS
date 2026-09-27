# Optional specialization valid only for a closed degree-three F2 cochain C.
# At omega=0 and Majorana layer zero, O5(C)=1/2 (C cup_1 C).
# General/nonclosed C must continue to use the complete obstruction formula.
BindGlobal("AFSClosedCFObstruction",function(c)
  local cup;
  if c=AFSZero then return AFSZero;fi;
  cup:=AFSCup(1,3,c,3,c);
  return AFSMemo(function(xs...)
    if Length(xs)<>5 then Error("closed CF obstruction takes five increments");fi;
    return CallFuncList(cup,xs)/2;
  end);
end);

# The same cup_1 expression without generic face construction. This separate
# entry point keeps the reference implementation above available for checks.
BindGlobal("AFSClosedCFObstructionDirect",function(c)
  if c=AFSZero then return AFSZero;fi;
  return AFSMemo(function(g,h,j,l,m)
    local one,x,y,z,value;
    one:=One(g);
    if one in [g,h,j,l,m] then return 0;fi;
    x:=g*h*j;y:=h*j*l;z:=j*l*m;value:=0;
    if x<>one then value:=value+c(x,l,m)*c(g,h,j);fi;
    if y<>one then value:=value+c(g,y,m)*c(h,j,l);fi;
    if z<>one then value:=value+c(g,h,z)*c(j,l,m);fi;
    return (value mod 2)/2;
  end);
end);

# Evaluate the three short, consecutive faces first. A zero factor makes
# the corresponding composed-increment callback unnecessary. Reduction of
# arbitrary integer callback values modulo two preserves cup_1 exactly.
BindGlobal("AFSClosedCFObstructionLazy",function(c)
  if c=AFSZero then return AFSZero;fi;
  return AFSMemo(function(g,h,j,l,m)
    local one,x,value;
    one:=One(g);
    if one in [g,h,j,l,m] then return 0;fi;
    value:=0;
    if c(g,h,j) mod 2=1 then
      x:=g*h*j;if x<>one then value:=value+c(x,l,m);fi;
    fi;
    if c(h,j,l) mod 2=1 then
      x:=h*j*l;if x<>one then value:=value+c(g,x,m);fi;
    fi;
    if c(j,l,m) mod 2=1 then
      x:=j*l*m;if x<>one then value:=value+c(g,h,x);fi;
    fi;
    return (value mod 2)/2;
  end);
end);
