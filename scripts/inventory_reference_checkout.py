#!/usr/bin/env python3
"""Read-only inventory of every locally available reference Git branch/tree.

This records availability/provenance, not a claim about unpublished files or
unfetched upstream revisions. No external program from the checkout is run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def inventory(root):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    refs = {}
    for line in git('for-each-ref', '--format=%(refname) %(objectname)',
                    'refs/heads', 'refs/remotes', 'refs/tags').decode().splitlines():
        name, commit = line.split()
        refs[name] = commit
    head = git('rev-parse', 'HEAD').decode().strip()
    commits = sorted(set(refs.values()) | {head})
    pattern = re.compile(r'space.?group|space_group|crystall|crystcat', re.I)
    trees = []
    for commit in commits:
        entries = []
        for row in git('ls-tree', '-r', '-z', commit).split(b'\0'):
            if not row:
                continue
            left, filename = row.split(b'\t', 1)
            mode, kind, object_id = left.decode().split()
            path = filename.decode()
            if kind != 'blob':
                entries.append(dict(path=path, kind=kind, object_id=object_id))
                continue
            raw = git('cat-file', 'blob', object_id)
            entry = dict(path=path, bytes=len(raw), git_blob=object_id,
                         sha256=hashlib.sha256(raw).hexdigest())
            text = raw.decode('utf-8', errors='replace')
            matches = []
            for line_number, line in enumerate(text.splitlines(), 1):
                match = pattern.search(line)
                if match:
                    matches.append(dict(line=line_number,
                        excerpt=line[max(0, match.start()-70):match.end()+170]))
            if matches:
                entry['space_group_text_mentions'] = matches
            if path.endswith('.json'):
                try:
                    value = json.loads(text)
                    entry['json_type'] = type(value).__name__
                    if isinstance(value, dict):
                        entry['json_top_keys'] = sorted(value)
                    elif isinstance(value, list):
                        entry['json_length'] = len(value)
                except ValueError:
                    entry['json_parse_error'] = True
            entries.append(entry)
        trees.append(dict(commit=commit, tracked_files=len(entries), files=entries))
    untracked = git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0')
    return dict(repository=str(root), head=head, locally_available_refs=refs,
        is_shallow=git('rev-parse', '--is-shallow-repository').decode().strip() == 'true',
        trees=trees, untracked_files=[x.decode() for x in untracked if x],
        scope='all locally referenced branches/tags plus HEAD; no upstream fetch',
        interpretation='Availability inventory; coefficient tables and literature mentions are not affine space-group answer tables.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inventory(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(head=result['head'], refs=result['locally_available_refs'],
        trees=[dict(commit=x['commit'], tracked_files=x['tracked_files']) for x in result['trees']],
        is_shallow=result['is_shallow'], output=str(args.output))))
