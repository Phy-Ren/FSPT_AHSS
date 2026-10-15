#!/usr/bin/env python3
"""Verify an approved ordinary singleton while preserving its incomplete parent."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

BASE = Path(__file__).resolve().parent
sha = lambda value: hashlib.sha256(value).hexdigest()
read = lambda name: json.loads((BASE / name).read_bytes())


def verify(repository):
    files = read('manifest.json')['filesSHA256']
    assert set(files) == {str(p.relative_to(BASE)) for p in BASE.rglob('*')
                          if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    for name, expected in files.items():
        assert sha((BASE / name).read_bytes()) == expected, name
    proof, approval = read('provenance.json'), read('approval.json')
    archive = (BASE / 'raw.tar.gz').read_bytes()
    assert sha(archive) == proof['rawArchiveSHA256'] and len(archive) == proof['rawArchiveBytes']
    raw = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            assert member.isfile() and not path.is_absolute() and '..' not in path.parts
            assert member.name not in raw
            raw[member.name] = tar.extractfile(member).read()
    assert sha(raw['manifest.json']) == proof['stagedManifestSHA256'] == approval['stagedManifestSHA256']
    assert approval['ordinaryCaseApproved'] is True
    assert approval['approvedCases'] == ['spacegroup_230_spinless']
    assert approval['originalParentCompleteClaimed'] is False and approval['complete460Claimed'] is False
    for key, path in [('ciResultSHA256', 'ci_view/spacegroup_230_spinless/result.json'),
                      ('e8ResultSHA256', 'e8_view/spacegroup_230_spinless/result.json'),
                      ('acceptedCollectionSHA256', 'staged_accepted/collection.json'),
                      ('subsetProvenanceSHA256', 'ci_view/subset_provenance.json')]:
        assert sha(raw[path]) == approval[key]
    with tempfile.TemporaryDirectory(prefix='u1-approved-singleton-') as tmp:
        temp = Path(tmp)
        stage, helper = temp / 'stage', temp / 'helper'
        for name, value in raw.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(value)
        helper_manifest = json.loads(raw['helper_manifest.json'])
        assert helper_manifest['commit'] == proof['ordinaryInspectorCommit']
        for name, expected in helper_manifest['files'].items():
            value = subprocess.check_output(['git', 'show', proof['ordinaryInspectorCommit'] + ':' + name], cwd=repository)
            assert sha(value) == expected['sha256'] and len(value) == expected['bytes']
            target = helper / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(value)
        # Exact retained verifier with only its three filesystem roots translated.
        program = raw['verify_view.py'].decode()
        substitutions = {
            'BASE=Path(__file__).resolve().parent': 'BASE=Path(sys.argv[1])',
            "REPO=Path('/home/xingyu/FSPT_AHSS_insulator')": 'REPO=Path(sys.argv[2])',
            "HELPER=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/accelerated_gate/preservation-helper-c26f3de')": 'HELPER=Path(sys.argv[3])',
        }
        for old, new in substitutions.items():
            assert program.count(old) == 1
            program = program.replace(old, new)
        checker = temp / 'check_translated_paths.py'
        checker.write_text(program)
        result = subprocess.run([sys.executable, str(checker), str(stage), str(repository), str(helper)],
                                check=True, stdout=subprocess.PIPE, text=True)
        checks = json.loads(result.stdout)
        assert checks['verified'] is True and checks['originalParentCompleteClaimed'] is False
        assert checks['exactOriginalCaseBytes'] is True and checks['stagedCollectorAccepted'] is True
        assert all((stage / name).read_bytes() == value for name, value in raw.items())
    return {'verified': True, 'approvedOrdinaryCases': approval['approvedCases'],
            'originalParentCompleteClaimed': False, 'complete460Claimed': False,
            'sourceFilesCheckedAgainstGit': checks['sourceFilesCheckedAgainstGit'],
            'pinnedHelperFilesReconstructed': len(helper_manifest['files']),
            'exactOriginalCaseBytes': True, 'independentScientificChecks': checks['scientificChecks'],
            'archiveSHA256': proof['rawArchiveSHA256'], 'retainedStageFiles': len(raw),
            'CIClassificationRecomputed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path,
                        default=next((p for p in BASE.parents if (p / '.git').exists()), Path.cwd()))
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
