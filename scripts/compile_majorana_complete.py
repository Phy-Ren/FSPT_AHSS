#!/usr/bin/env python3
"""Compile the independent closed-Majorana transcription to native programs."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas_fast_compile import compile_expression
from fspt.formulas_pip_compile import Scalar
from fspt.full_formula.compiler import atomic_write_bytes, compact_program
from fspt.majorana_complete import expression


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--degree", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    provenance = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (ROOT/"fspt/majorana_complete.py", ROOT/"fspt/formulas.py",
                            ROOT/"fspt/formulas_fast_compile.py")}
    for operation in ("majorana_source", "majorana_product", "obstruction", "stacking"):
        for coordinate in (("ca", "operator") if operation in ("obstruction", "stacking") else ("ca",)):
            started = time.monotonic()
            expr = expression(operation, args.degree, coordinate)
            builder, result, _ = compile_expression(expr, ())
            name = "majorana_%d_%s_%s" % (args.degree, operation, coordinate)
            data = compact_program(builder, [Scalar(builder, result)], dict(
                name=name, coordinate=coordinate, majorana_degree=args.degree,
                top_degree=expr.degree, denominator=8 if expr.modulus == 8 else 1,
                source_sha256=provenance))
            target = args.output/(name+".json")
            atomic_write_bytes(target, (json.dumps(data, separators=(",", ":"))+"\n").encode())
            print(json.dumps(dict(name=name, nodes=len(data["program"]),
                                  elapsed_seconds=time.monotonic()-started)), flush=True)


if __name__ == "__main__":
    main()
