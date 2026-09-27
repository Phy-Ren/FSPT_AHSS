"""Replay native GAP lower-tower exports through unchanged formula code."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor/p_ip_d4_normalized_package/code'))
from cochains import C,parity,ds,sq,cup

tested=0
for sg in (29,41,45,110,120,219):
    data=json.loads((ROOT/'runs'/('pip_samples_sg%d.json'%sg)).read_text())
    assert data[0]==sg
    for nvalues,bvalues,svalues,expected in data[1]:
        n=C(1,values={tuple(f):v for f,v in nvalues},mod=None)
        b=C(2,values={tuple(f):v for f,v in bvalues})
        s=C(1,values={tuple(f):v for f,v in svalues});w=C(2)
        actual=parity(n,b,w,s)((0,1,2,3,4))
        assert actual==expected,(sg,actual,expected)
        # A native primitive must solve the source on BAR faces as well.
        from itertools import combinations
        for f in combinations(range(5),4):
            assert (b.d()+cup(s,sq(n.reduce(2),1)))(f)==0,(sg,f,'lower equation')
        tested+=1
print('PASS',tested,'native space-group p+ip parity replays across six disputed groups')
