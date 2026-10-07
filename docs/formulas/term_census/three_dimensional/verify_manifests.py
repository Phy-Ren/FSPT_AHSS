#!/usr/bin/env python3
"""Verify physical terminal MS manifests using Python's standard library only.

This evaluates normalized interval cuts literally. Before targets are complete
explicit scalar polynomials, not hashes or numerical test samples. Repeated
binary scalar factors are idempotent; equal monomials cancel modulo two.
Integer-phase ASTs are outside this binary identity check.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter
import json, hashlib, sys, time

@lru_cache(maxsize=100000)
def interval_faces(word,degrees):
    length=len(word);arity=len(degrees)
    if set(word)!=set(range(1,arity+1))or any(a==b for a,b in zip(word,word[1:])):return ()
    output_degree=sum(degrees)-length+arity
    multiplicity=Counter(word)
    target=[degrees[j]+1-multiplicity[j+1]for j in range(arity)]
    if output_degree<0 or any(x<0 for x in target):return ()
    # Each occurrence contributes one endpoint plus its interval length.
    # Distribute each input's remaining degree over its occurrences, then
    # reject repeated vertices in the concatenated normalized input face.
    result=[];partial=[[]for _ in degrees]
    def visit(position,vertex,remaining):
        if position==length:
            if vertex==output_degree and not any(remaining):result.append(tuple(tuple(x)for x in partial))
            return
        label=word[position]-1
        tail=word[position+1:]
        lengths=(remaining[label],)if label+1 not in tail else range(remaining[label]+1)
        for size in lengths:
            face=tuple(range(vertex,vertex+size+1))
            if partial[label] and partial[label][-1]>=vertex:continue
            partial[label].extend(face);remaining[label]-=size
            visit(position+1,vertex+size,remaining)
            remaining[label]+=size;del partial[label][-len(face):]
    visit(0,0,target)
    return tuple(result)

def polynomial(rows,alphabet,expected_degree):
    result=set()
    for row in rows:
        word=tuple(row['word']);inputs=tuple(row['input_indices']);degrees=tuple(alphabet[i]['degree']for i in inputs)
        assert sum(degrees)-len(word)+len(inputs)==expected_degree
        for faces in interval_faces(word,degrees):
            mon=tuple(sorted(set((i,face)for i,face in zip(inputs,faces))))
            if mon in result:result.remove(mon)
            else:result.add(mon)
    return result

def run(directory):
    start=time.time();index=json.loads((directory/'INDEX.json').read_text());reports=[]
    for entry in index['files']:
        path=directory/entry['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
        data=json.loads(path.read_text());half=data['half_phase'];alphabet=half['input_cochains']
        assert all(x['coefficients']=='F2'for x in alphabet)
        target={tuple((i,tuple(face))for i,face in mon)for mon in half['before_scalar_polynomial']}
        result=polynomial(half['ms_terms'],alphabet,data['degree']);assert target==result,(entry['file'],len(target^result))
        assert len(half['ms_terms'])==half['collected_word_count'];assert len(target)==half['scalar_monomial_count']
        extra=data['physical_binary_face_polynomial']
        if extra:
            terms=[tuple(t)for t in extra['monomials']];assert len(set(terms))==len(terms)==extra['collected_count']
            assert all(tuple(sorted(set(t)))==t and all(0<=i<len(extra['factor_alphabet'])for i in t)for t in terms)
        reports.append({'file':entry['file'],'status':'PASS exact scalar coefficient identity','before_ms':half['before_word_count'],'after_ms':half['collected_word_count'],'scalar_coefficients':len(target)})
        interval_faces.cache_clear()
    receipt={'status':'PASS','sectors':len(reports),'seconds':round(time.time()-start,3),'checks':reports,'scope':'All12 selected MS sums equal the explicit before scalar polynomial on arbitrary typed normalized binary cochains. Integer carry ASTs and physical face tables are present but are not re-derived by this binary comparison.'}
    print(json.dumps(receipt,indent=2));return receipt
if __name__=='__main__':run(Path(sys.argv[1])if len(sys.argv)>1 else Path(__file__).resolve().parent)
