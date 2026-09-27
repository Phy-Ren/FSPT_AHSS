"""Exact C4 phase transport after correcting AW edge-prefix transport.

The corrected obstruction differs by s^5/2.  Since d_s(s^4/4)=-s^5/2,
the marked phase changes by -s^4/4.  Preserve the original artifact and
re-run derive_c4_pip_lift.py against the corrected compiler afterward.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path


def rephase(source, destination):
    raw = source.read_bytes()
    value = json.loads(raw)
    old = [Fraction(*x) for x in value["phase4"]]
    tuples = list(product(range(1, 4), repeat=4))
    assert len(old) == len(tuples) == 81
    new = [v - Fraction(int(all(x % 2 for x in t)), 4)
           for v, t in zip(old, tuples)]
    result = dict(value)
    result.update(
        phase4=[[x.numerator, x.denominator] for x in new],
        transportCorrection="nu_corrected=nu_original-s^4/4",
        obstructionCorrection="O5_corrected=O5_original+s^5/2 mod1",
        originalPhaseSha256=hashlib.sha256(raw).hexdigest(),
        originalPhasePath=str(source),
        phasePrimitiveVerified=False,
        verificationRequired="derive_c4_pip_lift.py --phase-file this-file",
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    rephase(args.source, args.destination)
