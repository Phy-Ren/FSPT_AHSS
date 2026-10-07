"""Restrict the completed physical I5 tables to identical external inputs.

The input is the published completed coefficient expression, including all
transfer, tensor and integer terms. No kernel is restricted before taking
its primitive. Every standard-operation argument and nonlinear numerator
is substituted recursively before exact binary collection.
"""
from pathlib import Path
from collections import Counter
import argparse,json,gzip,hashlib,time,resource

def read(path):
    with (gzip.open(path,'rt')if path.suffix=='.gz'else path.open())as f:return json.load(f)

class Restriction:
    def __init__(self):
        self.factors=[];self.intern={};self.alias=[];self.reasons=Counter()
    def monomial(self,ids):
        result=[]
        for i in ids:
            value=self.alias[i]
            if value is None:return None
            result.extend(value)
        return tuple(sorted(set(result)))
    def polynomial(self,rows,modulus):
        out={}
        for coefficient,ids in rows:
            monomial=self.monomial(ids)
            if monomial is not None:out[monomial]=(out.get(monomial,0)+coefficient)%modulus
        return [[c,list(m)]for m,c in sorted(out.items())if c]
    def factor(self,row):
        kind=row['kind'];out={k:v for k,v in row.items()if k!='id'}
        if kind=='physical_face':out['cochain']=out['cochain'].replace("'",'').replace('\\\\','\\')
        elif kind.startswith('standard_'):
            args=[]
            for a in row['arguments']:
                args.append({**a,'cochain':a['cochain'].replace('\\\\','\\'),'terms':self.polynomial(a['terms'],1<<a['precision_bits'])})
            out['arguments']=args;out['operation']=out['operation'].replace('\\\\','\\')
            majorana=[a for a in args if a['cochain'] in (r'\check n_3',r"\check n'_3")]
            if out['operation']=='B_4' and majorana and all(not a['terms'] for a in majorana):
                out['operation']=r'B_4^\psi'
                out['arguments']=[a for a in args if a['cochain'] not in (r'\check n_3',r"\check n'_3")]
                args=out['arguments'];self.reasons['B_zero_Majorana_equals_Bpsi']+=1
            # Each existing lower operation is normalized when all its
            # decoration inputs vanish. Background arguments may remain.
            decorations=[a for a in args if a['cochain']not in (r'\omega_2',r's_1')]
            if decorations and all(not a['terms']for a in decorations):
                self.alias.append(None);self.reasons['normalized_zero_operation']+=1;return
        else:
            terms=self.polynomial(row['numerator'],row['modulus']);out['numerator']=terms
            if not terms:
                self.alias.append(None);self.reasons['zero_numerator']+=1;return
            if len(terms)==1:
                coefficient,monomial=terms[0]
                self.alias.append(tuple(monomial)if(coefficient//row['divisor'])%2 else None)
                self.reasons['single_monomial_digit']+=1;return
        key=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).digest()
        if key in self.intern:
            index=self.intern[key];self.reasons['identical_factor']+=1
        else:
            index=len(self.factors);self.intern[key]=index;self.factors.append({'id':index,**out})
        self.alias.append((index,))

def write_chunks(directory,rows,prefix,compressed=False,max_rows=300000):
    files=[];batch=[]
    def save():
        if not batch:return
        name=f'{prefix}_{len(files):03}.json'+('.gz'if compressed else '')
        raw=(json.dumps(batch,separators=(',',':'))+'\n').encode()
        payload=gzip.compress(raw,mtime=0)if compressed else raw
        (directory/name).write_bytes(payload)
        entry={'file':name,'kind':prefix,'rows':len(batch),'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
        if compressed:entry['uncompressed_sha256']=hashlib.sha256(raw).hexdigest()
        files.append(entry)
        batch.clear()
    for row in rows:
        batch.append(row)
        if len(batch)>=max_rows:save()
    save();return files

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('destination',type=Path)
    args=p.parse_args();start=time.monotonic();index=read(args.source/'INDEX.json');R=Restriction();source_hashes={};terms=set();seen=0
    args.destination.mkdir(parents=True,exist_ok=True)
    for entry in index['files']:
        if entry['kind']!='factors':continue
        path=args.source/entry['file'];source_hashes[path.name]=entry['sha256']
        for row in read(path):
            assert row['id']==len(R.alias);R.factor(row)
    print('factors',len(R.alias),'to',len(R.factors),dict(R.reasons),flush=True)
    for entry in index['files']:
        if entry['kind']!='terms':continue
        path=args.source/entry['file'];source_hashes[path.name]=entry['sha256']
        for row in read(path):
            m=R.monomial(row);seen+=1
            if m is None:continue
            if m in terms:terms.remove(m)
            else:terms.add(m)
        print('input_terms',seen,'collected',len(terms),'seconds',round(time.monotonic()-start,2),flush=True)
    assert seen==index['term_count']
    # Prune factors that were only used by canceled output monomials.
    used={i for term in terms for i in term};pending=list(used)
    while pending:
        i=pending.pop();row=R.factors[i]
        rows=row.get('numerator',[])
        if row['kind'].startswith('standard_'):
            rows=[term for arg in row['arguments']for term in arg['terms']]
        for _,ids in rows:
            for j in ids:
                if j not in used:used.add(j);pending.append(j)
    remap={old:new for new,old in enumerate(sorted(used))}
    final=[]
    for old in sorted(used):
        row=R.factors[old];out={**row,'id':remap[old]}
        def poly(rows):return [[c,[remap[i]for i in ids]]for c,ids in rows]
        if 'numerator'in row:out['numerator']=poly(row['numerator'])
        if 'arguments'in row:out['arguments']=[{**a,'terms':poly(a['terms'])}for a in row['arguments']]
        final.append(out)
    files=write_chunks(args.destination,final,'factors',compressed=True,max_rows=1500)
    files+=write_chunks(args.destination,([remap[i]for i in m]for m in sorted(terms)),'terms',True)
    report={'status':'PASS_EXACT_COMPLETED_EXPRESSION_SPECIALIZATION','dimension':'4+1D','coefficient_sum':index['coefficient_sum'],
            'coefficient_system':'F2','phase_prefactor':'1/2','input_terms':seen,'term_count':len(terms),'factor_count':len(final),'source_factor_count':index['factor_count'],
            'substitution':'Exact integral identity B4[n,0]=B4psi[n], including every retained digit and ordinary differential; all existing arguments and whole nonlinear scopes preserved.',
            'factor_rules':dict(R.reasons),'files':files,'source_files_sha256':source_hashes,
            'nonlinear_interior_terms':sum(len(r.get('numerator',[]))for r in final),
            'lower_argument_terms':sum(len(a['terms'])for r in final for a in r.get('arguments',[])),
            'includes_complete_y6':index['includes_complete_y6'],'includes_tensor_coefficients':index['includes_tensor_coefficients'],
            'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (args.destination/'INDEX.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('files','source_files_sha256')},indent=2),flush=True)

if __name__=='__main__':main()
