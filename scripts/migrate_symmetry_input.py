#!/usr/bin/env python3
"""Write a separate v2 input from an explicitly selected legacy charge-rho file."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator.notation import migrate_legacy_input, migrate_legacy_request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use a separate output path; historical input is immutable.')
    data = json.loads(args.input.read_text())
    result = migrate_legacy_request(data) if 'op' in data else migrate_legacy_input(data)
    # Exclusive creation prevents an accidental replacement of an existing run.
    with args.output.open('x') as output:
        json.dump(result, output, indent=2, sort_keys=True)
        output.write('\n')


if __name__ == '__main__':
    main()
