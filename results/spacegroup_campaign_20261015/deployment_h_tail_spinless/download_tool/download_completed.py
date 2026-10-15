#!/usr/bin/env python3
"""Read-only remote completion polling; exact downloads and frozen local acceptance."""
import argparse
import base64
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = Path('/home/xingyu/FSPT_AHSS_insulator')
DOWNLOAD = Path('/home/xingyu/insulator-campaign-download')
REMOTE = '/home/user/xyren/AllFSPT_insulator'
TAGS = ['sgfull-20261015-g-n02', 'sgfull-20261015-g-n03', 'sgfull-20261015-h-n08']
COMMIT = 'c07c6e5d4a69d79c9c2aeb0739ae1e189029f824'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.partial')
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    os.replace(tmp, path)


def read(path):
    return json.loads(path.read_bytes())


def remote_reports():
    code = 'import pathlib,json,base64\nb=pathlib.Path(%r)\ntags=%r\n' % (REMOTE, TAGS)
    code += "print(json.dumps({tag:base64.b64encode((b/'runs'/(tag+'-finalization.json')).read_bytes()).decode() for tag in tags}))\n"
    result = subprocess.run(['ssh', '-o', 'BatchMode=yes', 'cuhk-cluster3', 'bash -s'],
                            input="python3 - <<'REMOTE_PY'\n" + code + 'REMOTE_PY\n',
                            text=True, capture_output=True, timeout=45, check=True)
    return {tag: base64.b64decode(raw) for tag, raw in json.loads(result.stdout).items()}


def safe_members(tar, allowed=None):
    members = tar.getmembers()
    names = [m.name for m in members]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate archive member')
    for m in members:
        p = Path(m.name)
        if p.is_absolute() or '..' in p.parts or not (m.isfile() or m.isdir()):
            raise ValueError('Unsafe archive member: ' + m.name)
        if allowed and (not p.parts or p.parts[0] not in allowed):
            raise ValueError('Unexpected archive prefix: ' + m.name)
    return members


def frozen_source():
    target = HERE / ('postprocessor-' + COMMIT[:7])
    if target.exists():
        return target
    raw = subprocess.check_output(['git', 'archive', COMMIT, 'insulator', 'scripts', 'docs/e8/3p1.md'], cwd=REPO)
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        safe_members(archive)
        archive.extractall(target)
    write(target / '_export.json', {'commit': COMMIT, 'gitArchiveSHA256': sha(raw)})
    return target


def verify_existing(target, final_raw):
    proof = read(target / 'download_verification.json')
    if proof.get('finalizationSHA256') != sha(final_raw) or not proof.get('frozenCollectorExactReplay'):
        raise ValueError('Existing download has different or incomplete verification')
    final = json.loads(final_raw)
    if sha((target / Path(final['archive']).name).read_bytes()) != final['archiveSHA256']:
        raise ValueError('Existing downloaded archive changed')
    return proof


def download_one(tag, final_raw):
    final = json.loads(final_raw)
    if (final.get('state') != 'complete' or final.get('tag') != tag
            or final.get('sourceVerified') is not True or final.get('runtimeVerified') is not True
            or final.get('acceptedCount') != final.get('selectedCount')):
        raise ValueError('Finalization is not a verified complete campaign')
    remote_archive = REMOTE + '/runs/' + tag + '-evidence.tar.gz'
    if final['archive'] != remote_archive:
        raise ValueError('Unexpected remote archive path')
    target = DOWNLOAD / (tag + '-finalized')
    if target.exists():
        return verify_existing(target, final_raw)
    source = frozen_source()
    with tempfile.TemporaryDirectory(prefix='.' + tag + '-download-', dir=DOWNLOAD) as temp:
        staging = Path(temp)
        archive_path = staging / Path(remote_archive).name
        with archive_path.open('wb') as output:
            proc = subprocess.run(['ssh', '-o', 'BatchMode=yes', 'cuhk-cluster3',
                                   'cat ' + shlex.quote(remote_archive)], stdout=output,
                                  stderr=subprocess.PIPE, timeout=180, check=True)
        if archive_path.stat().st_size != final['archiveBytes'] or sha(archive_path.read_bytes()) != final['archiveSHA256']:
            raise ValueError('Archive size or SHA256 mismatch')
        again = remote_reports()[tag]
        if again != final_raw:
            raise ValueError('Finalization changed across download')
        with tarfile.open(archive_path) as archive:
            members = safe_members(archive, {tag, tag + '-e8', tag + '-accepted'})
            archive.extractall(staging)
        (staging / 'finalization.json').write_bytes(final_raw)
        (staging / 'download.stderr.log').write_bytes(proc.stderr)
        collection = read(staging / (tag + '-accepted/collection.json'))
        if sha((source / 'scripts/collect_expansion.py').read_bytes()) != collection['collectorSHA256']:
            raise ValueError('Unexpected collector source')
        for name, digest in read(staging / (tag + '-e8/source.json'))['files'].items():
            if sha((source / name).read_bytes()) != digest:
                raise ValueError('Unexpected E8 source: ' + name)
        raw_dirs = [staging / tag, staging / (tag + '-e8'), staging / (tag + '-accepted')]
        original_hashes = {str(p.relative_to(staging)): sha(p.read_bytes()) for root in raw_dirs
                           for p in root.rglob('*') if p.is_file()}
        output = staging / 'local-rechecked'
        command = [sys.executable, str(source / 'scripts/collect_expansion.py'), '--ci-root', str(staging / tag),
                   '--e8-root', str(staging / (tag + '-e8')), '--output', str(output)]
        proc = subprocess.run(command, text=True, capture_output=True, timeout=120)
        (staging / 'frozen_collector_replay.log').write_text(proc.stdout + proc.stderr)
        if proc.returncode:
            raise ValueError('Frozen collector failed: ' + proc.stderr[-2000:])
        for row in collection['collections']:
            for name in ['results.json', 'ci_results.json', 'validation.json']:
                if sha((output / row['path'] / name).read_bytes()) != row['filesSHA256'][name]:
                    raise ValueError('Frozen collector output differs: ' + name)
        if not all(sha((staging / name).read_bytes()) == digest for name, digest in original_hashes.items()):
            raise ValueError('Original extracted artifact changed during replay')
        proof = {'schema': 'u1-complete-campaign-download-verification-v1', 'verifiedUTC': now(),
                 'archiveSHA256': final['archiveSHA256'], 'archiveBytes': final['archiveBytes'],
                 'finalizationSHA256': sha(final_raw), 'finalizationUnchangedAcrossDownload': True,
                 'requiredCompleteBeforeDownload': True, 'archiveMemberSafetyVerified': True,
                 'sourceVerified': True, 'runtimeVerified': True, 'frozenCollectorExactReplay': True,
                 'frozenCollectorCommit': COMMIT, 'frozenCollectorCommand': command,
                 'frozenCollectorExitCode': proc.returncode, 'originalFilesUnchanged': True,
                 'originalFilesSHA256': original_hashes, 'acceptedCount': final['acceptedCount'],
                 'localExtractedPath': str(target), 'noClassificationOrProcessSignal': True}
        write(staging / 'download_verification.json', proof)
        os.rename(staging, target)
        return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--interval', type=float, default=60)
    parser.add_argument('--maximum-hours', type=float, default=6)
    args = parser.parse_args()
    state = {'pid': os.getpid(), 'startedUTC': now(), 'tags': {}}
    deadline = time.monotonic() + args.maximum_hours * 3600
    while True:
        try:
            reports = remote_reports()
            for tag, raw in reports.items():
                previous = state['tags'].get(tag, {})
                if previous.get('state') in ('downloaded_verified', 'failed'):
                    continue
                report = json.loads(raw)
                stage = report.get('state')
                if stage == 'complete':
                    try:
                        proof = download_one(tag, raw)
                        record = {'state': 'downloaded_verified', 'path': proof['localExtractedPath'],
                                  'acceptedCount': proof['acceptedCount'], 'archiveSHA256': proof['archiveSHA256']}
                    except Exception as exc:
                        record = {'state': 'failed', 'error': type(exc).__name__ + ': ' + str(exc), 'report': report}
                elif stage in ('failed', 'incomplete'):
                    record = {'state': 'failed', 'error': 'Remote finalizer ' + stage, 'report': report}
                else:
                    record = {'state': stage, 'report': report}
                if record != previous:
                    print(json.dumps({'UTC': now(), 'tag': tag, **record}), flush=True)
                state['tags'][tag] = record
            state.pop('pollError', None)
        except Exception as exc:
            state['pollError'] = type(exc).__name__ + ': ' + str(exc)
            print(json.dumps({'UTC': now(), 'pollError': state['pollError']}), flush=True)
        state['updatedUTC'] = now()
        write(HERE / 'status.json', state)
        if args.once or all(x.get('state') in ('downloaded_verified', 'failed') for x in state['tags'].values()) and len(state['tags']) == len(TAGS):
            return
        if time.monotonic() >= deadline:
            state['pollingDeadlineReached'] = True
            write(HERE / 'status.json', state)
            return
        time.sleep(min(args.interval, max(0, deadline - time.monotonic())))


if __name__ == '__main__':
    main()
