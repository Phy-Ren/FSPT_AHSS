#!/usr/bin/env python3
"""Build a reviewed public snapshot without copying private Git history or references.

No GitHub/network operation, commit, or push is performed. Read committed source
bytes only; this script is also included as an explicitly recorded tooling overlay.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

ALLOWED_ROOT_FILES = {'.gitattributes', '.gitignore', 'README.md', 'requirements-report.txt'}
ALLOWED_DIRS = {'fspt', 'gap', 'scripts', 'tests'}
PUBLIC_DOCS = {'docs/CLUSTER_RUN.md'}
INTERNAL_TOOLS = {'scripts/report_upper_carry_scope.py', 'scripts/audit_c4_pullback_calibration.py'}
OWN_RESULTS = {'classification_frozen', 'space_groups', 'space_groups_spinless',
               'pip_diagnostics', 'optimization_validation', 'performance_environment',
               'point_groups'}
POLICY = 'fspt-public-snapshot-v1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def allowed(path):
    parts = Path(path).parts
    if not parts or any(p in ('.git', '..') for p in parts):
        return False
    if parts[0] in {'internal_notes', 'publication', 'notes'} or path in INTERNAL_TOOLS:
        return False
    if len(parts) == 1:
        return path in ALLOWED_ROOT_FILES
    if parts[0] == 'docs':
        return path in PUBLIC_DOCS
    if parts[0] in ALLOWED_DIRS:
        return True
    if parts[0] != 'results' or len(parts) < 3:
        return False
    if parts[1] in {'space_groups', 'space_groups_spinless', 'point_groups'} and parts[2] == 'report':
        return False
    # Research discussions stay in the private workspace. Original payloads
    # named by retained archive manifests are handled explicitly in build().
    if Path(path).suffix in {'.md', '.tex'}:
        return False
    if parts[1] in OWN_RESULTS:
        return True
    # Detailed third-party answer tables and original comparison payloads are
    # deliberately omitted. Our prose, hashes, statistics and finite controls remain.
    if parts[1] == 'boss_layers':
        return len(parts) == 3 and path.endswith('.md')
    if parts[1] == 'external_comparison':
        return path in {
            'results/external_comparison/inputs/manifest.json',
            'results/external_comparison/inputs/finite_c2_controls.json',
        }
    return False


def scan_credentials(files):
    rules = {
        'private-key': rb'-----BEGIN (?:RSA |DSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----',
        'github-token': rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
        'aws-access-key': rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
        'api-token': rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}\b',
        'slack-token': rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
        'credential-url': rb'https?://[^\s/:@]{2,}:[^\s/@]{5,}@',
    }
    findings = []
    for path, data in files.items():
        for name, pattern in rules.items():
            if re.search(pattern, data):
                findings.append({'path': path, 'rule': name})
    if findings:
        raise ValueError('Credential-pattern review required (values redacted): ' + json.dumps(findings))


def read_commit(source, ref):
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', ref+'^{commit}'], text=True).strip()
    blob = subprocess.check_output(['git', '-C', str(source), 'archive', '--format=tar', commit])
    files, modes = {}, {}
    with tarfile.open(fileobj=io.BytesIO(blob)) as archive:
        for member in archive.getmembers():
            if member.isdir():
                continue
            if not member.isfile() or Path(member.name).is_absolute() or '..' in Path(member.name).parts:
                raise ValueError('Unsupported source entry: '+member.name)
            files[member.name] = archive.extractfile(member).read()
            modes[member.name] = member.mode
    return commit, files, modes


def summaries(source_files):
    boss = json.loads(source_files['results/boss_layers/current_reference_comparison.json'])
    ext = json.loads(source_files['results/external_comparison/comparison.json'])
    boss_keys = ('schema', 'scope', 'chronology', 'compared_at', 'total_entries', 'counts', 'counts_by_layer',
                 'current', 'frozen', 'reference', 'preserved_original_report_sha256',
                 'free_lattice_comparison', 'full_stacking_comparison')
    boss_summary = {k: boss[k] for k in boss_keys}
    boss_summary.update(public_release_scope='Aggregate comparison evidence; reference tables and manuscript text not distributed.',
                        full_private_report_sha256=sha(source_files['results/boss_layers/current_reference_comparison.json']))
    ext_keys = ('scope', 'chronology', 'frozen', 'computed', 'complete_witnesses_required',
                'required_formula_convention', 'independent_classification_count', 'current_classification_count',
                'independent_full_stack_count', 'draft_reference_kind', 'draft_reference_sha256', 'draft_categories',
                'geometric_reference_sha256', 'finite_reference_sha256', 'finite_controls_sha256',
                'finite_distinct_inputs', 'finite_reference_scope', 'finite_reference_certified_ko', 'boss_initial_cohomology')
    ext_summary = {k: ext[k] for k in ext_keys}
    for field in ('geometric', 'finite'):
        rows = ext[field+'_rows']
        ext_summary[field+'_comparison'] = {'rows': len(rows), 'matches': sum(bool(r.get('match')) for r in rows)}
    ext_summary.update(public_release_scope='Aggregate comparison evidence; complete third-party reference rows not distributed.',
                       full_private_report_sha256=sha(source_files['results/external_comparison/comparison.json']))
    return {'results/boss_layers/public_summary.json': (json.dumps(boss_summary, indent=2, sort_keys=True)+'\n').encode(),
            'results/external_comparison/public_summary.json': (json.dumps(ext_summary, indent=2, sort_keys=True)+'\n').encode()}


def build(source, ref):
    commit, original, modes = read_commit(source, ref)
    public = {p: b for p, b in original.items() if allowed(p)}
    # Keep every original byte needed by a published numerical archive.
    for path, raw in original.items():
        if Path(path).name != 'archive.json' or not allowed(path):
            continue
        manifest = json.loads(raw)
        entries = manifest['files']
        entries = entries.items() if isinstance(entries, dict) else [(e['path'], e) for e in entries]
        for name, entry in entries:
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe archived payload path')
            payload_path = str(Path(path).parent/relative)
            payload = original[payload_path]
            if sha(payload) != entry['sha256'] or len(payload) != entry['bytes']:
                raise ValueError('Original archive payload differs: '+payload_path)
            public[payload_path] = payload
    table_sources = {}
    for path, raw in original.items():
        if path.startswith('publication/group_tables/'):
            target = 'results/group_tables/'+path[len('publication/group_tables/'):]
            public[target] = raw
            table_sources[target] = path
    # Internal notes, including their paths and hashes, are not exported.
    excluded = {p: {'sha256': sha(b), 'bytes': len(b)} for p, b in original.items()
                if p not in public and not p.startswith('internal_notes/')}
    public.update(summaries(original))
    public['scripts/publish_snapshot.py'] = Path(__file__).read_bytes()
    test_path = Path(__file__).resolve().parents[1]/'tests/test_publish_snapshot.py'
    if test_path.is_file():
        public['tests/test_publish_snapshot.py'] = test_path.read_bytes()
    release = '''# Public release scope

This repository is a clean public snapshot of the project's independently
implemented code, computed group structures, and reproducibility records.
It starts a separate Git history. The complete local working history
and private comparison archive are retained by the author and are not pushed.

The source checkout is `/home/xingyu/FSPT_AHSS`; the separate publishing checkout
is `/home/xingyu/FSPT_AHSS_public`. These are author-local paths, not installation
requirements. `PUBLICATION_MANIFEST.json` identifies the source commit, copied
file hashes, publication-only documentation changes, and excluded-file hashes.
The snapshot-builder script and its isolated tests are explicit tooling overlays
from the reviewed publishing workspace; their exact hashes are recorded too.
The original working repository has no publishing remote. The numerical GAP
source and result archives retain their accepted bytes. The public Python
launcher additionally accepts `AFS_GAP` or a `gap` executable on `PATH`, with
the original cluster path as fallback; its GAP arguments are unchanged.

## Private comparison materials

Unpublished collaborator PDFs, their text/glyph transcriptions, recovered draft
answer tables, original legacy logs, and full reference-row comparison payloads
are not distributed. Aggregate comparison statistics, source hashes, and
independently computed finite controls remain available. The
reference-input manifest records provenance only; it does not contain the input
bytes. Additional research and comparison reports remain in the private
workspace. Commands requiring optional reference materials need separately supplied
authorized copies. Production classification, stacking, saved-result audits and
reports do not require them.

The generated obstruction/product coefficients are mathematical inputs evaluated
by this implementation. No SptSet or collaborator implementation is included or
loaded by production. No license grant for omitted third-party material is
implied by publication of this repository.

## Reproduce and synchronize

Install the GAP packages and Python environment described in `README.md`. Run
`scripts/run_group.py` for one complete classification/stacking calculation, or
follow `docs/CLUSTER_RUN.md` to create fresh compute allocations for all 230.
The accepted results and exact source snapshots are in `results/space_groups`
(crystalline spin-half, internal spinless) and `results/space_groups_spinless`
(crystalline spinless, internal spin-half). Their archived bytes are unchanged
in this release. Public tables in `results/group_tables` present the four
decoration layers and the final abstract stacking groups. Original machine
records and their certificate fields are preserved without rewriting.
Internal research notes and working discussions are not published.

Run self-contained saved-result, scheduling and publication tests without private
reference inputs:

```sh
PYTHONPATH=tests python3 -m unittest test_stacking test_stack_result_cli \\
  test_audit_run test_report_results test_collect_performance \\
  test_archive_campaign test_comparison_archive test_boss_current \\
  test_external_comparison test_deadline_archive test_deadline_evidence \\
  test_deadline_guard test_submit_campaign test_worker_input test_publish_snapshot
PYTHONPATH=tests python3 -m unittest test_audit_background_run \\
  test_report_background_results test_background_performance \\
  test_background_provenance_review test_pip_diagnostics test_stack_result_background \\
  test_compare_background_runs test_report_physical_conventions
PYTHONPATH=tests python3 -m unittest test_boss_parser test_c4_pip_square_cf \\
  test_closed_cf_phase test_free_pip_universal test_pip_incoming_formula
PYTHONPATH=tests python3 -m unittest test_point_group_audit test_point_group_marked_controls
```

An unrestricted `unittest discover` also selects optional unchanged-reference
oracle tests, which require the omitted `vendor/` formula bundles and collaborator
modules. Missing reference imports in those tests do not affect production or
the self-contained suite above; no such test is counted as passed without its
original input.

For a subsequent public release, first commit and review the intended changes
in the source checkout, then prepare the separate clean publishing checkout:

```sh
python3 /home/xingyu/FSPT_AHSS/scripts/publish_snapshot.py \\
  --source /home/xingyu/FSPT_AHSS --ref HEAD \\
  --output /home/xingyu/FSPT_AHSS_public --update
```

The script refuses an unclean publishing checkout, copies only committed source
bytes within its explicit allowlist, reapplies the reference exclusions, scans
common credential signatures, and does not commit or push. Review the generated
manifest and `git diff` in the publishing checkout before committing and pushing
there. Never attach this public remote to the full local working repository.
New result directories require an explicit publication-policy review; they are
excluded until added to the allowlist.
'''
    public['PUBLIC_RELEASE.md'] = release.encode()
    readme = public['README.md'].decode()
    old = 'This is a local Git repository; no GitHub remote has\nbeen published.'
    new = ('This public repository is a clean release snapshot. See\n'
           '[publication scope and synchronization](PUBLIC_RELEASE.md) for the retained\n'
           'local history and omitted private reference materials.')
    readme = readme.replace(old, new)
    readme = readme.replace('Run the complete pipeline with:', 'Set `AFS_GAP=/path/to/gap` if GAP is not on your `PATH`. Run the complete pipeline with:')
    public['README.md'] = readme.encode()
    runner = public['scripts/run_gap.py'].decode()
    runner = runner.replace('import argparse\n', 'import argparse\nimport os\nimport shutil\n')
    runner = runner.replace('cmd = ["/home/user/xyren/software/gap-4.13.1/gap",', 'gap = os.environ.get("AFS_GAP") or shutil.which("gap") or "/home/user/xyren/software/gap-4.13.1/gap"\ncmd = [gap,')
    public['scripts/run_gap.py'] = runner.encode()
    public['results/external_comparison/README.md'] = b'''# External comparison evidence in the public release

The comparisons below concern crystalline spin-half / internal spinless.
The accepted independent results are in `results/space_groups`. The independent
classification freeze is preserved in `results/classification_frozen`.
For the other spin convention, see [the reference scope](../../docs/SPINLESS_REFERENCE_SCOPE.md)
and [the two-convention report](../optimization_validation/background_v3/physical_conventions/README.md).
No supplied external affine-230 table is available for that second convention.

- All 920 current graded-layer entries match both the original independent
  freeze and the supplied current reference PDF.
- Of 204 populated historical full-stacking rows, 179 agree, 21 differ already
  in graded layers, and four differ with identical graded layers (68, 81, 82,
  101). Another 26 reference rows are blank.
- Nine geometric examples, 687 initial mod-two cohomology dimensions, all 230
  signed H1 groups, and four finite-model labels (two distinct inputs) agree.
- The supplied current PDF has no full-stacking table. The available Weicheng
  materials have no affine-230 full-stacking table. SG219 has no historical
  full-stacking value to compare.

`public_summary.json` retains statistics and hashes. `inputs/manifest.json`
identifies the privately retained reference bytes; those bytes and detailed
reference-row transcriptions are not distributed. The independent finite C2
controls remain in `inputs/finite_c2_controls.json`.

The comparison tools are included for use with separately supplied authorized
reference copies. They are optional and never feed production results. See
[public release scope](../../PUBLIC_RELEASE.md#private-comparison-materials),
[comparison analysis](../../docs/COMPARISON_WEICHENG.md), and
[graded-layer comparison](../../docs/BOSS_LAYER_COMPARISON.md).
'''
    # Keep public links valid without fabricating omitted reference artifacts.
    link = re.compile(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)')
    import os
    for path in list(public):
        if not path.endswith('.md'):
            continue
        text = public[path].decode()
        def repair(match):
            target = match.group(2)
            clean = target.split('#', 1)[0].strip('<>')
            if not clean or '://' in clean or clean.startswith(('mailto:', '#', '/')):
                return match.group(0)
            normalized = os.path.normpath(str(Path(path).parent / clean))
            if normalized == 'runs/classification_frozen/manifest.json':
                return '['+match.group(1)+']('+os.path.relpath('results/classification_frozen/manifest.json', str(Path(path).parent))+')'
            if normalized in excluded or normalized.startswith(('reference/', 'vendor/')):
                destination = os.path.relpath('PUBLIC_RELEASE.md', str(Path(path).parent))
                return '['+match.group(1)+']('+destination+'#private-comparison-materials)'
            return match.group(0)
        text = link.sub(repair, text)
        if path.startswith('docs/') and any(x in path for x in ('COMPARISON', 'HISTORICAL', 'FINAL_ARCHIVE')):
            destination = os.path.relpath('PUBLIC_RELEASE.md', str(Path(path).parent))
            text = ('> Public release: this document describes the complete local audit. '
                    '[Private reference inputs]('+destination+'#private-comparison-materials) '
                    'are not distributed; production and independent result audits remain reproducible.\n\n') + text
        public[path] = text.encode()
    scan_credentials(public)
    manifest = {'schema': POLICY, 'source_commit': commit,
                'scope': 'Separate public history; no private Git objects or omitted reference payloads copied.',
                'allowlist': {'root_files': sorted(ALLOWED_ROOT_FILES), 'directories': sorted(ALLOWED_DIRS),
                              'public_documents': sorted(PUBLIC_DOCS), 'own_result_directories': sorted(OWN_RESULTS),
                              'group_table_sources': table_sources},
                'files': {p: {'sha256': sha(b), 'bytes': len(b),
                              'source_sha256': sha(original[p]) if p in original else None,
                              'publication_modified': p not in original or b != original[p]}
                          for p, b in sorted(public.items())},
                'excluded_source_files': excluded,
                'credential_signature_scan': 'passed; signature checks are supplemented by manual publication review'}
    public['PUBLICATION_MANIFEST.json'] = (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()
    return public, modes, manifest


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--ref', default='HEAD')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--update', action='store_true')
    a = p.parse_args(argv)
    source, output = a.source.resolve(), a.output.absolute()
    if output.is_symlink() or source == output.resolve() or source in output.resolve().parents or output.resolve() in source.parents:
        p.error('source and output must be separate, non-overlapping checkouts without an output symlink')
    old_paths = set()
    if output.exists():
        if not a.update or not (output/'.git').is_dir() or not (output/'PUBLICATION_MANIFEST.json').is_file():
            p.error('existing output requires --update and a previous public Git checkout')
        status = subprocess.check_output(['git', '-C', str(output), 'status', '--porcelain'], text=True)
        if status:
            p.error('public checkout must be clean before synchronization')
        previous = json.loads((output/'PUBLICATION_MANIFEST.json').read_text())
        if previous.get('schema') != POLICY:
            p.error('publication manifest policy mismatch')
        old_paths = set(previous['files']) | {'PUBLICATION_MANIFEST.json'}
        for name in old_paths:
            item = Path(name)
            if item.is_absolute() or '..' in item.parts or '.git' in item.parts:
                p.error('unsafe path in previous publication manifest')
    elif a.update:
        p.error('--update requires an existing public checkout')
    public, modes, manifest = build(source, a.ref)
    for name in old_paths | set(public):
        item = output/name
        if item.is_symlink() or any(parent.is_symlink() for parent in item.parents if parent != output.parent):
            p.error('refusing symlink in public output path: '+name)
    # All source selection/validation precedes mutation. Never touch .git.
    output.mkdir(parents=True, exist_ok=True)
    for name in sorted(old_paths-set(public)):
        path = output/name
        if path.is_file() or path.is_symlink():
            path.unlink()
    for name, data in public.items():
        path = output/name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_symlink():
            raise ValueError('refusing public output symlink: '+name)
        path.write_bytes(data)
        path.chmod(0o755 if modes.get(name, 0)&0o111 else 0o644)
    print(json.dumps({'source_commit': manifest['source_commit'], 'output': str(output),
                      'files': len(public), 'bytes': sum(map(len, public.values())),
                      'excluded_files': len(manifest['excluded_source_files']),
                      'manifest_sha256': sha(public['PUBLICATION_MANIFEST.json'])}, indent=2))


if __name__ == '__main__':
    main()
