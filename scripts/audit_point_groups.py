#!/usr/bin/env python3
"""Audit actual finite matrix inputs and saved point-group certificates.

This is an algebraic/geometry audit, not an independent proof of the physical
p+ip product. It reads no external classification or stacking answer table.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fspt.point_group_geometry import expected_spectrum
from audit_run import check_result, check_complete_witnesses, determinant, product
from audit_background_run import check_background_result, rational_matrix
from collect_performance import parse_metrics, stage_intervals


NAMES = [('1','C1',1),('-1','Ci',2),('2','C2',2),('m','Cs',2),
         ('2/m','C2h',4),('222','D2',4),('mm2','C2v',4),('mmm','D2h',8),
         ('4','C4',4),('-4','S4',4),('4/m','C4h',8),('422','D4',8),
         ('4mm','C4v',8),('-42m','D2d',8),('4/mmm','D4h',16),
         ('3','C3',3),('-3','C3i',6),('32','D3',6),('3m','C3v',6),
         ('-3m','D3d',12),('6','C6',6),('-6','C3h',6),('6/m','C6h',12),
         ('622','D6',12),('6mm','C6v',12),('-6m2','D3h',12),
         ('6/mmm','D6h',24),('23','T',12),('m-3','Th',24),('432','O',24),
         ('-43m','Td',24),('m-3m','Oh',48)]
UNITARY = {1,3,6,9,12,16,18,21,24,28,30}
FORMULA = 'normalized-pip-aw-edge-transport-v2'
SCOPE = ('Exact finite geometry, native Pin cocycle and linear algebra certificates are checked. '
         'Stored nonlinear lifts are not independently rebuilt here. Selected p+ip products '
         'remain formula inputs; passing this audit is not a proof of their physical uniqueness. '
         'Abstract-only Ext certificates do not provide marked upper stacking relations.')
GEOMETRY_KEYS = ('index','hermannMauguin','schoenflies','order','unitary','matrices',
                 'multiplication','signTable','identityIndex','matrix_set_sha256',
                 'elementSpectra','representationDimension','translationSubgroupPresent',
                 'finiteH0ZsOrders','finiteH1ZsOrders')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(data):
    return (json.dumps(data, indent=2, sort_keys=True)+'\n').encode()


def check_geometry(d):
    n = d['point_group_index']
    assert type(n) is int and 1 <= n <= 32
    assert 'space_group' not in d, 'affine result mislabeled as a point group'
    p = d['point_group']; hm, sf, order = NAMES[n-1]
    assert (p['index'], p['hermannMauguin'], p['schoenflies'], p['order']) == (n,hm,sf,order)
    assert p['kind'] == 'finite-crystallographic-point-group'
    assert p['representationDimension'] == 3 and p['translationSubgroupPresent'] is False
    assert p['unitary'] is (n in UNITARY)
    matrices, table, signs = p['matrices'], p['multiplication'], p['signTable']
    assert len(matrices) == len(table) == len(signs) == order
    assert all(len(m) == 3 and all(len(r) == 3 and all(type(x) is int for x in r) for r in m) for m in matrices)
    assert len({tuple(x for row in m for x in row) for m in matrices}) == order
    assert all(len(row) == order and all(type(x) is int and 1 <= x <= order for x in row) for row in table)
    assert all(type(x) is int and x in (0,1) for x in signs)
    identity = p['identityIndex']-1
    eye = [[int(i == j) for j in range(3)] for i in range(3)]
    assert 0 <= identity < order and matrices[identity] == eye
    spectra = Counter()
    for i, m in enumerate(matrices):
        det = determinant(m)
        assert det in (-1,1) and signs[i] == (1-det)//2
        assert table[i][identity] == table[identity][i] == i+1
        assert identity+1 in table[i], 'element has no inverse'
        for j, other in enumerate(matrices):
            k = table[i][j]-1
            assert product(m, other) == matrices[k], 'finite multiplication table is not the matrix product'
            assert signs[k] == (signs[i]+signs[j]) % 2
        power, exponent = i, 1
        while power != identity:
            power = table[power][i]-1; exponent += 1
            assert exponent <= order, 'element order exceeds finite group order'
        spectra[(exponent,sum(m[k][k] for k in range(3)),det)] += 1
    assert not any(signs) if n in UNITARY else sum(signs)*2 == order
    assert p['determinantDistribution'] == {'positive':order-sum(signs),'negative':sum(signs)}
    assert p['elementSpectra'] == [[list(k),v] for k,v in sorted(spectra.items())]
    assert p['elementSpectra'] == expected_spectrum(n), 'matrix spectrum does not belong to the named geometric point group'
    assert p['finiteH0ZsOrders'] == ([0] if n in UNITARY else [])
    assert p['finiteH1ZsOrders'] == ([] if n in UNITARY else [2])
    assert d['pip']['free_rank'] == 0 and 0 not in d['pip']['orders']
    assert p['matrixIsomorphismCheckedAllProducts'] is True
    for key in ('pcpGeneratorMatrixIndices','resolutionElementMatrixIndices'):
        assert all(type(x) is int and 1 <= x <= order for x in p[key])
    assert p['matrix_set_sha256'] == digest(json.dumps(sorted(matrices),separators=(',',':')).encode())
    if d['crystalline_spin'] == 'spinless':
        b = d['crystalline_background']
        assert [rational_matrix(m) for m in b['pointElements']] == matrices
        assert b['multiplication'] == table and b['signTable'] == signs and b['identityIndex'] == identity+1
        assert 'finite' in b['cohomologyGroupScope']
    return tuple(sorted(spectra.items()))


def audit_row(d):
    spectrum = check_geometry(d)
    spin = d['crystalline_spin']
    assert spin in ('half','spinless') and d['formula_convention'] == FORMULA
    assert d['scope'] == '3+1D-finite-crystallographic-point-group-associated-graded'
    assert d['stacking']['scope'] == '3+1D-finite-crystallographic-point-group-stacking'
    if spin == 'half':
        kind = check_result(d)
        check_complete_witnesses(d, FORMULA)
        info = dict(kind=kind,full_group=True,marked_witnesses=True,missing_evidence=[])
    else:
        info = check_background_result(d, strict_background=True)
    assert not info['missing_evidence'], 'missing strict certificate evidence'
    s = d['stacking']; p = d['point_group']
    return dict(point_group_index=d['point_group_index'],crystalline_spin=spin,
        hermann_mauguin=p['hermannMauguin'],schoenflies=p['schoenflies'],order=p['order'],
        matrix_set_sha256=p['matrix_set_sha256'],source_id=d['source_id'],
        layers={'pip':d['pip']['orders'],**{k:d[k] for k in ('majorana','complex_fermion','bosonic')}},
        invariants=s.get('invariants'),
        invariant_options=s.get('pipExtensionCertificate',{}).get('invariantOptions'),
        gap_cpu_seconds=d['total_cpu_ms']/1000,
        pip_product_scope=('selected-product-marked-witness' if info['marked_witnesses']
            else 'abstract-only-Ext-family') if 2 in d['pip']['orders'] else 'no-torsion-pip-extension',
        **info), spectrum


def audit(run, source=None, tasks_root=None, allow_partial=False):
    rows, errors, documents, spectra, evidence = [], [], {}, {}, {}
    def read(path):
        raw = path.read_bytes(); evidence[str(path)] = digest(raw); return json.loads(raw)
    sources = {str(p.relative_to(source)):digest(p.read_bytes()) for p in sorted((source/'gap').glob('*.g'))} if source else None
    if sources is not None:
        assert 'gap/run_point_group.g' in sources
        evidence.update({str(source/name):checksum for name,checksum in sources.items()})
    for spin in ('half','spinless'):
        for n in range(1,33):
            path = run/('%s_pg%d.json' % (spin,n))
            if not path.exists():
                continue
            try:
                d = read(path)
                assert (d['crystalline_spin'],d['point_group_index']) == (spin,n)
                row, spectrum = audit_row(d)
                row['result_sha256'] = evidence[str(path)]
                if sources is not None:
                    assert d['source_sha256'] == sources, 'result source differs from actual frozen files'
                raw_path = path.with_suffix('.raw.json')
                if raw_path.exists():
                    raw = read(raw_path)
                    assert all(k in raw for k in ('point_group','pip','stacking','majorana','complex_fermion','bosonic'))
                    for key,value in raw.items():
                        if key == 'point_group':
                            assert all(d[key][k] == v for k,v in value.items()), 'raw/wrapped point geometry differs'
                        else:
                            assert d[key] == value, 'raw/wrapped mathematical result differs: '+key
                elif not allow_partial:
                    raise AssertionError('original GAP result missing')
                checkpoint = run/'classification'/path.name
                if checkpoint.exists():
                    c = read(checkpoint)
                    assert c['source_id'] == d['source_id']
                    for k in ('pip','majorana','complex_fermion','bosonic','resolution_dimensions','cpu_ms','crystalline_spin','point_group_index'):
                        assert c[k] == d[k], 'checkpoint/result differs: '+k
                    check_geometry(c)
                    assert all(c['point_group'][k] == d['point_group'][k] for k in GEOMETRY_KEYS)
                elif not allow_partial:
                    raise AssertionError('classification checkpoint missing')
                rows.append(row); documents[(spin,n)] = d; spectra[(spin,n)] = spectrum
            except (AssertionError,KeyError,TypeError,ValueError,IndexError,ZeroDivisionError,StopIteration) as exc:
                errors.append({'file':path.name,'reason':str(exc) or type(exc).__name__})
    for n in range(1,33):
        if ('half',n) in documents and ('spinless',n) in documents:
            if any(documents['half',n]['point_group'][k] != documents['spinless',n]['point_group'][k] for k in GEOMETRY_KEYS):
                errors.append({'point_group_index':n,'reason':'physical conventions used different finite geometry'})
    for spin in ('half','spinless'):
        group_spectra = [s for (label,n),s in spectra.items() if label == spin]
        if len(set(group_spectra)) != len(group_spectra):
            errors.append({'crystalline_spin':spin,'reason':'two named point groups share the same finite representation spectrum'})
    source_ids = sorted({r['source_id'] for r in rows})
    if len(source_ids) > 1:
        errors.append({'reason':'mixed source versions'})
    performance = None
    if tasks_root is not None and len(rows) == 64 and not errors:
        campaign = read(run/'campaign.json'); tasks = campaign['tasks']
        assert len(tasks) == len({t['id'] for t in tasks}) == 64
        assert {(t['crystalline_spin'],t['point_group_index']) for t in tasks} == set(documents)
        assert campaign['source_id'] == source_ids[0] and campaign['source_sha256'] == sources
        task_rows = []
        for t in tasks:
            ident = t['id']; assert Path(ident).name == ident
            td = tasks_root/ident; status = read(td/'status.json')
            assert status['status'] == 'done' and status['exit_code'] == 0, 'original task is not done/zero: '+ident
            for key in ('id','command','queue','created'):
                assert status[key] == t[key], 'task provenance differs: '+ident+' '+key
            assert status.get('hostname') and status.get('pbs_job'), 'missing compute-node allocation provenance'
            metrics_raw = (td/'metrics.txt').read_bytes(); evidence[str(td/'metrics.txt')] = digest(metrics_raw)
            metrics = parse_metrics(metrics_raw)
            assert metrics is not None and metrics['exit_status'] == 0
            stdout = (td/'stdout.log').read_bytes(); evidence[str(td/'stdout.log')] = digest(stdout)
            d = documents[t['crystalline_spin'],t['point_group_index']]
            assert ('AFS_POINT_GROUP_SAVED %d %s' % (t['point_group_index'],t['crystalline_spin'])).encode() in stdout
            task_rows.append(dict(task_id=ident,crystalline_spin=t['crystalline_spin'],point_group_index=t['point_group_index'],
                stage_intervals=stage_intervals(d),gap_cpu_seconds=d['total_cpu_ms']/1000,**metrics))
        performance = dict(tasks=task_rows,gap_cpu_seconds=sum(t['gap_cpu_seconds'] for t in task_rows),
            process_cpu_seconds=sum(t['process_cpu_seconds'] for t in task_rows),
            peak_task_rss_gib=max(t['maximum_resident_set_size_kib'] for t in task_rows)/1024**2,
            elapsed_result_clock_seconds=max(d['finished'] for d in documents.values())-min(d['started'] for d in documents.values()),
            elapsed_scope='first result runner start to last finish; common allocated-node clock; excludes queue wait')
    missing = [[s,n] for s in ('half','spinless') for n in range(1,33) if (s,n) not in documents]
    tooling = [Path(__file__),Path(__file__).with_name('audit_run.py'),Path(__file__).with_name('audit_background_run.py'),
               Path(__file__).with_name('collect_performance.py'),Path(__file__).resolve().parents[1]/'fspt/point_group_geometry.py']
    return dict(schema='fspt-finite-point-groups-audit-v1',groups_passed=len(rows),rows=rows,errors=errors,
        missing=missing,complete=not errors and not missing,source_ids=source_ids,
        all_abstract_groups_determined=not errors and not missing and all(r['full_group'] for r in rows),
        all_marked_witnesses_present=not errors and not missing and all(r['marked_witnesses'] for r in rows),
        mathematical_scope_limit=SCOPE,external_answers_consulted=False,evidence_sha256=evidence,performance=performance,
        auditor_sha256={str(p.relative_to(Path(__file__).resolve().parents[1])):digest(p.read_bytes()) for p in tooling})


def archive(run, source, tasks_root, output, report):
    assert report['complete'] and report['performance'] is not None
    assert not output.exists() and not output.is_symlink()
    assert source.resolve() == (run/'source').resolve(), 'archive requires its complete frozen source inside run/source'
    material = {}
    for p in sorted(run.rglob('*')):
        assert not p.is_symlink()
        if p.is_file(): material[str(p.relative_to(run))] = (p,p.read_bytes())
    campaign = json.loads((run/'campaign.json').read_bytes())
    for t in campaign['tasks']:
        for name in ('status.json','metrics.txt','stdout.log'):
            p = tasks_root/t['id']/name
            material['tasks/'+t['id']+'/'+('stdout.txt' if name == 'stdout.log' else name)] = (p,p.read_bytes())
    by_original = {str(p):digest(raw) for p,raw in material.values()}
    for p,sha in report['evidence_sha256'].items():
        assert by_original[p] == sha, 'audited input changed before archive: '+p
    assert 'audit.json' not in material
    material['audit.json'] = (None,encoded(report))
    entries = {name:dict(archive_path=name,original_path=str(p) if p else None,sha256=digest(raw),bytes=len(raw))
               for name,(p,raw) in material.items()}
    manifest = dict(schema='fspt-finite-point-groups-archive-v1',archived_at_utc=datetime.now(timezone.utc).isoformat(),
        source_id=campaign['source_id'],files=entries,archive_file_count=len(material)+1,
        payload_bytes=sum(len(raw) for p,raw in material.values()),mathematical_scope_limit=SCOPE,
        external_answers_consulted=False,input_bytes_modified=False)
    output.parent.mkdir(parents=True,exist_ok=True); output.mkdir()
    try:
        for name,(p,raw) in material.items():
            q = output/name; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(raw)
            assert digest(q.read_bytes()) == entries[name]['sha256']
        (output/'archive.json').write_bytes(encoded(manifest))
    except BaseException:
        shutil.rmtree(output); raise
    return dict(output=str(output),archive_sha256=digest(encoded(manifest)),files=len(material)+1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run',type=Path); ap.add_argument('--source',type=Path)
    ap.add_argument('--tasks-root',type=Path); ap.add_argument('--allow-partial',action='store_true')
    ap.add_argument('--report',type=Path); ap.add_argument('--archive',type=Path)
    args = ap.parse_args(argv)
    if not __debug__: ap.error('run without -O or PYTHONOPTIMIZE')
    report = audit(args.run.resolve(),args.source.resolve() if args.source else None,
                   args.tasks_root.resolve() if args.tasks_root else None,args.allow_partial)
    if args.report:
        if args.report.exists(): ap.error('report exists; preserve earlier evidence')
        args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_bytes(encoded(report))
    if args.archive:
        assert args.source and args.tasks_root
        print(json.dumps(archive(args.run.resolve(),args.source.resolve(),args.tasks_root.resolve(),args.archive.resolve(),report)))
    print(json.dumps({k:v for k,v in report.items() if k not in ('rows','evidence_sha256','performance')},indent=2))
    return int(bool(report['errors'] or (report['missing'] and not args.allow_partial)))


if __name__ == '__main__':
    sys.exit(main())
