"""One known native fixture; no classification, SSH or process signaling."""
import copy,hashlib,importlib.util,json,shutil,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pipeline',BASE/'postprocess_g.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
review=Path('/home/xingyu/AllFSPT_reviews/natural_exit_attestation_self_identity_20261015')
fixture=Path(json.loads((review/'local_test_result.json').read_text())['workdir'])
report=fixture/'real_cli_observed_ended/cancellation.json';report_data=m.read(report)
original=fixture/'campaign';source=fixture/'snapshot';original_before=m.tree(original)
work=Path(tempfile.mkdtemp(prefix='pipeline-local-',dir=BASE));(work/'runs').mkdir();(work/'prepared').mkdir();catalog=work/'catalog';catalog.mkdir()
helper=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/accelerated_gate/preservation-helper-c26f3de')
case='spacegroup_019_spin_half';shutil.copyfile(original/case/'input.json',catalog/(case+'.json'))
config=m.read(BASE/'prepared_config.json');config=copy.deepcopy(config)
config['nodes']={'n02':dict(root=str(original),sourceSHA256=report_data['sourceSHA256'],selectionSHA256=m.sha(original/'selection.json'),requiredCases=[case],requiredHashes={case:dict(inputSHA256=m.sha(original/case/'input.json'),nativeSHA256=m.sha(original/case/'native.json'))})}
m.write(work/'prepared/prepared_config.json',config)
m.BASE=work;m.HELPER=helper;m.SOURCE=source;m.CATALOG=catalog;m.HERE=work/'prepared'
# Exact source bytes remain the production candidate; only the synthetic path
# constants/config are rebound in this isolated interpreter.
args=SimpleNamespace(node='n02',report=report)
with mock.patch.object(m.socket,'gethostname',return_value='n02.local'):
    m.remote_run(args,config)
completion=work/'runs/sgfull-20261015-g-n02-preserved-c26f3de-completion.json';final=m.read(completion)
assert final['preservedCount']==1 and final['originalSelectedCount']==3
assert final['requiredCases']==[case] and m.tree(original)==original_before
out=work/'downloaded-and-replayed'
verify=SimpleNamespace(node='n02',archive=Path(final['archive']),completion=completion,output=out,helper=helper,catalog=catalog)
m.offline_verify(verify,config)
proof=m.read(out/'download_verification.json');assert proof['frozenCollectorExactReplay'] and proof['originalExtractedFilesUnchanged']
assert m.tree(original)==original_before
rejections=[]
with mock.patch.object(m.socket,'gethostname',return_value='n02.local'):
    try:m.remote_run(args,config)
    except ValueError:rejections.append('existing-output-rejected')
    else:raise AssertionError('Existing output was overwritten')
bad=work/'corrupt.tar.gz';bad.write_bytes(Path(final['archive']).read_bytes()+b'corrupt')
try:m.offline_verify(SimpleNamespace(**dict(vars(verify),archive=bad,output=work/'bad-download')),config)
except ValueError:rejections.append('corrupt-download-rejected-before-extraction')
else:raise AssertionError('Corrupt archive accepted')
assert not (work/'bad-download').exists()
wrong=dict(final,requiredCases=[]);wrong_path=work/'wrong-completion.json';m.write(wrong_path,wrong)
try:m.offline_verify(SimpleNamespace(**dict(vars(verify),completion=wrong_path,output=work/'wrong-proof')),config)
except ValueError:rejections.append('wrong-required-subset-rejected-before-extraction')
else:raise AssertionError('Wrong required subset accepted')
assert not (work/'wrong-proof').exists()
result=dict(status='PASS',candidateSHA256=m.sha(BASE/'postprocess_g.py'),syntheticFixtureOnly=True,noClusterContact=True,noClassification=True,noSignals=True,
            originalRawBytesUnchanged=True,originalSelectionCount=3,preservedCount=1,requiredCount=1,retryCount=2,
            fullParentCI_E8Validated=True,frozenCollectorExactReplay=True,rejections=rejections,workdir=str(work))
m.write(work/'test_result.json',result);m.write(BASE/'local_test_result.json',result);print(json.dumps(result,indent=2))
