"""Immutable source snapshots and provenance for complete-formula campaigns."""
from __future__ import annotations

import hashlib
import errno
import json
import os
from pathlib import Path
import shutil
import tempfile
import time


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def publish_result(path, result):
    """Publish complete JSON atomically, without replacing an existing result.

    A unique staging file prevents writers from truncating each other's data.
    Hard-link publication is exclusive, including across NFS clients; readers
    see either no final file or a fully written, fsynced result.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        # Do not use replace/rename here: completed scientific records are
        # immutable even if a faulty scheduler launches a duplicate command.
        os.link(temporary, str(path))
    finally:
        os.unlink(temporary)


def freeze_runtime(root):
    """Copy one content-addressed runtime once, shared by all identical jobs."""
    root = Path(root).resolve()
    files = set(root.glob("gap/*.g"))
    files.update(root.glob("fspt/full_formula/*.py"))
    files.update(root.glob("fspt/full_formula/*.so"))
    files.update(root.glob("fspt/full_formula/*.cpp"))
    files.update(root.glob("fspt/data/full_formula/*.json"))
    files.update(root.glob("fspt/majorana*.py"))
    files.add(root / "scripts/full_formula_worker.py")
    if (root / "scripts/closed_majorana_worker.py").exists():
        files.add(root / "scripts/closed_majorana_worker.py")
    if (root / "fspt/__init__.py").is_file():
        files.add(root / "fspt/__init__.py")
    hashes = {str(path.relative_to(root)): sha256(path) for path in sorted(files)}
    source_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    parent = root / "runs/full_source_snapshots"
    parent.mkdir(parents=True, exist_ok=True)
    destination = parent / source_id

    def confirm_published_snapshot():
        # A different compute node may have atomically renamed the snapshot
        # while this client's negative NFS lookup is still cached. The server
        # rename error is authoritative; wait for the manifest rather than
        # immediately asking is_dir() about that same stale negative entry.
        deadline = time.monotonic() + 60
        while True:
            try:
                published = json.loads((destination / "source_manifest.json").read_text())
            except (FileNotFoundError, NotADirectoryError):
                if time.monotonic() >= deadline:
                    raise RuntimeError("Published runtime snapshot is not visible after 60 seconds: " + source_id)
                # Re-read the parent directory to encourage NFS revalidation.
                with os.scandir(str(parent)) as entries:
                    for entry in entries:
                        if entry.name == source_id:
                            break
                time.sleep(0.2)
                continue
            if published.get("source_id") != source_id or published.get("sha256") != hashes:
                raise RuntimeError("Published runtime snapshot has a different manifest: " + source_id)
            return

    if not destination.is_dir():
        temporary = Path(tempfile.mkdtemp(prefix=source_id[:12] + "-", dir=str(parent)))
        try:
            for relative, expected in hashes.items():
                path = temporary / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(root / relative, path)
                if sha256(path) != expected:
                    raise RuntimeError("Runtime changed while being frozen: " + relative)
            (temporary / "source_manifest.json").write_text(json.dumps(
                {"source_id": source_id, "sha256": hashes}, indent=2, sort_keys=True) + "\n")
            try:
                os.rename(str(temporary), str(destination))
            except OSError as error:
                if error.errno not in (errno.EEXIST, errno.ENOTEMPTY):
                    raise
                confirm_published_snapshot()
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    else:
        confirm_published_snapshot()
    return destination, {"source_id": source_id, "source_sha256": hashes,
                         "source_snapshot": str(destination)}
