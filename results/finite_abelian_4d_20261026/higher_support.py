"""Closed nonsplit spectator blocks with at least two factors."""

def clean(factors):
    return sorted(n for n in factors if n>1)


def closed(m,spectators):
    spectators=sorted(spectators)
    g=spectators[0]
    r=len(spectators)
    if r==2:
        repeated=spectators[1]==g
        if g<=m:
            if repeated:
                return clean([g//2]*3+[g]*2+[2*g])
            if g<m:
                return clean([g//2]*2+[g]*2+[2*g]*2)
            return clean([g//2]*2+[g]*3+[2*g])
        return clean([m//2]+[m]*3+[g//2]+[g if repeated else 2*g])
    if r==3:
        unique=spectators.count(g)==1
        if g<=m:
            return clean([g//2]+[g]*(6-unique)+[2*g]*unique)
        return clean([m]*3+[g]*(4-unique)+[2*g]*unique)
    if r==4:
        return clean([g]*3+[min(m,g) if g<2*m else 2*m])
    if r==5:
        return [g]
    if r>5:
        return []
    raise ValueError('This formula covers spectator support >=2 only')
