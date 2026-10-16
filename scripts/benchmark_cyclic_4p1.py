#!/usr/bin/env python3
"""Bounded reference/cache comparison of every retained cyclic witness."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator.cyclic4p1 import calculate
from scripts.audit_cyclic_4p1 import bar_root_relations
from scripts.classify_cyclic_4p1 import manifest
from scripts.classify import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--order', type=int, action='append')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    orders = args.order or [3, 6]
    if args.output.exists() or any(n < 1 for n in orders) or len(set(orders)) != len(orders):
        parser.error('Use a new output and distinct positive orders')
    source = manifest()
    rows = []
    for order in orders:
        start = time.monotonic()
        baseline = bar_root_relations(order)
        old_seconds = time.monotonic() - start
        outputs, measurements = [], []
        for cached in (False, True):
            start = time.monotonic()
            classification, evidence, stats = calculate(order, cache=cached)
            measurements.append({'cache': cached, 'seconds': round(time.monotonic()-start, 6), 'stats': stats})
            outputs.append((classification, evidence))
        if outputs[0] != outputs[1] or outputs[0][0]['presentation'] != baseline['presentation']:
            raise ArithmeticError('Cache/reference or previous audit presentation mismatch')
        payload = json.dumps(outputs[0], sort_keys=True, separators=(',', ':')).encode()
        rows.append({'order': order, 'status': 'PASS', 'completeWitnessesLiterallyEqual': True,
                     'previousAuditPresentationEqual': True, 'previousAuditSeconds': round(old_seconds, 6),
                     'mathematicalOutputSHA256': hashlib.sha256(payload).hexdigest(), 'runs': measurements})
        print(json.dumps(rows[-1]), flush=True)
    if manifest() != source:
        raise RuntimeError('Source changed during benchmark')
    write_json(args.output, {'status': 'PASS', 'cases': rows, 'source': source,
        'hostTimingScope': 'Same host/process, reference then cache; existing geometry-plan caches are warm. No universal speed factor inferred.'})


if __name__ == '__main__':
    main()
