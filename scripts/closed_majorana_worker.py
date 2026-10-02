#!/usr/bin/env python3
"""Independent CA/operator worker for an explicitly restricted Majorana fiber."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fspt.majorana_backend import ClosedMajoranaBackend
from full_formula_worker import arrays


def respond(backend, request):
    dimension, stage, operation = request["dimension"], request["stage"], request["operation"]
    if dimension not in (2, 3, 4):
        raise ValueError("Closed-Majorana degrees one through three are implemented")
    if operation == "source":
        fields = arrays(request["fields"])
        if any(fields["n"]):
            raise ValueError("A closed-Majorana coordinate cannot evaluate a nonzero integer field")
        value = 0 if stage == "majorana" else backend.source(dimension, stage, fields)
    elif operation == "product":
        left, right, background = arrays(request["left"]), arrays(request["right"]), arrays(request["background"])
        if any(left["n"]) or any(right["n"]):
            raise ValueError("A closed-Majorana coordinate cannot multiply a nonzero integer field")
        value = 0 if stage == "majorana" else backend.product(dimension, stage, left, right, background)
    else:
        raise ValueError(operation)
    if stage == "bosonic":
        return dict(ok=True, numerator=value.numerator, denominator=value.denominator)
    return dict(ok=True, value=int(value), modulus=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coordinate", required=True, choices=("ca", "operator"))
    args = parser.parse_args()
    backend = ClosedMajoranaBackend(coordinate=args.coordinate)
    for line in sys.stdin:
        try:
            request = json.loads(line)
            result = respond(backend, request)
            if "id" in request:
                result["id"] = request["id"]
        except Exception as error:
            result = dict(ok=False, error=type(error).__name__, message=str(error))
        print(json.dumps(result, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
