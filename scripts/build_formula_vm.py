#!/usr/bin/env python3
"""Build the optional generic integer DAG VM without touching formula data."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default=os.environ.get('CXX', 'g++'))
    parser.add_argument('--output', type=Path, default=ROOT / 'insulator/_compiled/u1_dag_vm.so')
    parser.add_argument('--metadata', type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'insulator/_compiled/u1_dag_vm.cpp'
    compiler = shlex.split(args.compiler)
    flags = ['-std=c++11', '-O3', '-fPIC', '-shared']
    # A completed library replaces the target atomically; failed compilation
    # never leaves a partial file available to another formula worker.
    with tempfile.TemporaryDirectory(prefix='u1-vm-build-', dir=str(output.parent)) as directory:
        temporary = Path(directory) / output.name
        command = compiler + flags + [str(source), '-o', str(temporary)]
        subprocess.run(command, check=True)
        os.replace(str(temporary), str(output))
    report = {'builtUTC': datetime.now(timezone.utc).isoformat(),
              'compiler': compiler, 'flags': flags,
              'compilerVersion': subprocess.check_output(compiler + ['--version'], text=True),
              'source': str(source), 'sourceSHA256': digest(source),
              'binary': str(output), 'binarySHA256': digest(output),
              'integerDAGs': {name: digest(ROOT / 'insulator/_compiled' / name)
                             for name in ('source3.json', 'product3.json')},
              'genericVMProvenance': 'FSPT_AHSS main0864495 fspt/full_formula/native.cpp; no SC formula data'}
    if args.metadata:
        args.metadata.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
