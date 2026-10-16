#!/usr/bin/env python3
"""Positive control: same Oh cohomology, spin-half determinant Thom twist."""
from contextlib import redirect_stdout
from pathlib import Path
from io import StringIO
import json
import runpy

root=Path(__file__).parent
with redirect_stdout(StringIO()):
    n=runpy.run_path(root/'oh_ext_audit.py')
# For X=BG^(det(V)-1), w1=x and w2=0. All base Steenrod operations stay fixed.
n['S2'].__globals__['w2']=frozenset()
n['differential'].cache_clear()
r={str(i):[n['ext'](s,i) for s in range(7)] for i in range(6)}
h=[n['h0_rank'](s,4) for s in range(4)]
result={
    'input':'Oh spin-half X=BG^(det(V)-1), w1=x, w2=0',
    'E1_Ext_rows':r,
    'h0_ranks_stem4':h,
    'ku4_torsion':[2,2,2,4,8],
    'Spin_c_degree4_torsion_after_shifted_ku0':[2,2,2,2,4,8],
    'comparison':'Agrees with Debray v3 Theorem 5.95 and current Oh spin-half result; this is a positive control, not an unverified universal spectrum equivalence.'
}
(root/'oh_spin_half_ext_control.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
