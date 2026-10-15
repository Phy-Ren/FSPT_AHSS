#!/usr/bin/env python3
"""Configure a byte-identical completion downloader in an isolated directory."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
config = json.loads((HERE / 'config.json').read_bytes())
engine = HERE / 'download_completed.py'
assert hashlib.sha256(engine.read_bytes()).hexdigest() == config['helperSHA256']
spec = importlib.util.spec_from_file_location('isolated_h_tail_spinless_downloader', engine)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE
module.TAGS = config['tags']
assert module.COMMIT == config['frozenCollectorCommit']
assert str(module.DOWNLOAD) == config['downloadDirectory']
assert module.TAGS == ['sgfull-20261015-h-tail-spinless-n08']
if __name__ == '__main__':
    module.main()
