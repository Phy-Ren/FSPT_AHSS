#!/usr/bin/env python3
"""Compile the supplied full O5 with its arbitrary extension background.

Uses the same corrected AW edge transport and exact scalar instructions as
the accepted omega-zero compiler. No space-group answer or group is an input.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas_pip_compile import compile_pip_o5
from compile_pip_o5_straight import compile_gap


def main():
    program = compile_pip_o5(omega_zero=False)
    raw = (json.dumps(program, separators=(',', ':'))+'\n').encode()
    source = ROOT/'gap/pip_o5_background.json'
    source.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    output = compile_gap(program, digest).replace('AFSPipO5General', 'AFSPipO5Background')
    (ROOT/'gap/pip_o5_background.g').write_text(output)
    print(json.dumps(dict(operations=len(program['program']), sha256=digest,
                         omega_zero=False, output='gap/pip_o5_background.g')))


if __name__ == '__main__':
    main()
