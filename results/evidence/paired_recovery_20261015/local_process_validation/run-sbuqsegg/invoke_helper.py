import importlib.util,json,os,signal,sys
from pathlib import Path
helper,trace,mode,target=sys.argv[1:5];sys.argv=[helper]+sys.argv[5:]
spec=importlib.util.spec_from_file_location('owned_stop',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for name in ('kill','killpg'):
    original=getattr(m.os,name)
    def wrapped(pid,sig,original=original,name=name):
        with open(trace,'a') as out: out.write(json.dumps({'call':name,'pid':pid,'signal':int(sig)})+'\n')
        return original(pid,sig)
    setattr(m.os,name,wrapped)
if mode=='missing_argv':
    original=m.scan_owned
    def scan(uid):
        rows=original(uid)
        if int(target) in rows: rows[int(target)]['argv']=[]
        return rows
    m.scan_owned=scan
if mode=='after_freeze_failure':
    original=m.validate_tree
    calls=[0]
    def validate(*a,**k):
        calls[0]+=1
        if calls[0]>1: raise RuntimeError('Synthetic post-freeze validation failure')
        return original(*a,**k)
    m.validate_tree=validate
m.main()
