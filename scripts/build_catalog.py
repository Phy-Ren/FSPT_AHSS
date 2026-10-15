#!/usr/bin/env python3
"""Build exact symmetry inputs; never read benchmark answers."""
from pathlib import Path
import argparse
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from insulator_catalog.catalog import catalog, gap_literal


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=["point2", "wallpaper", "point3", "spacegroup"])
    parser.add_argument("--index", action="append", type=int,
                        help="Generate selected one-based catalog indices; repeat as needed")
    parser.add_argument("--output", type=Path, default=Path("insulator_catalog/generated"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.index:
        if not args.family:
            parser.error("--index requires --family")
        from insulator_catalog.catalog import build_group
        inputs = [build_group(args.family, index, spin) for index in sorted(set(args.index))
                  for spin in ("spinless", "spin_half")]
    else:
        inputs = catalog(args.family)
    for record in inputs:
        path = args.output / record["id"]
        path.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
        path.with_suffix(".g").write_text("U1_INPUT := " + gap_literal(record) + ";;\n")
    (args.output / (args.family or "all")).with_suffix(".index.json").write_text(
        json.dumps([row["id"] for row in inputs], indent=2) + "\n")
    print(f"Generated {len(inputs)} exact insulator symmetry inputs in {args.output}")

if __name__ == "__main__":
    main()
