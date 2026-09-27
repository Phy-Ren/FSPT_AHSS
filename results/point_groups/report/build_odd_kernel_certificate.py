#!/usr/bin/env python3
"""Exact finite-table retractions and background gauges from archived inputs.

This uses no classification value to select a group map. It is a finite
algebra check on the already archived geometric symmetry data, not a GAP run.
"""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def gf2_solve(rows, size):
    basis = {}
    for mask, value in rows:
        while mask:
            bit = mask.bit_length()-1
            if bit not in basis:
                basis[bit] = (mask, value)
                break
            old, rhs = basis[bit]
            mask ^= old
            value ^= rhs
        if not mask and value:
            return None
    answer = [0]*size
    for bit in sorted(basis):
        mask, value = basis[bit]
        answer[bit] = value ^ (sum(answer[i] for i in range(bit) if mask >> i & 1) % 2)
    if any((sum(answer[i] for i in range(size) if mask >> i & 1) % 2) != value for mask,value in rows):
        raise ValueError('GF2 certificate failed')
    return answer


def order(table, identity, x):
    t = identity
    for n in range(1,len(table)+1):
        t = table[t][x]
        if t == identity:
            return n
    raise ValueError('not a finite multiplication table')


def certify(large_number, small_number):
    lp = ROOT/f'spinless_pg{large_number}.json'
    sp = ROOT/f'spinless_pg{small_number}.json'
    large = json.loads(lp.read_text()); small = json.loads(sp.read_text())
    lg = large['point_group']; sg = small['point_group']
    T = [[x-1 for x in row] for row in lg['multiplication']]
    U = [[x-1 for x in row] for row in sg['multiplication']]
    le = lg['identityIndex']-1; se = sg['identityIndex']-1
    n,m = len(T),len(U)
    kernel = {x for x in range(n) if order(T,le,x) in (1,3)}
    if len(kernel) != 3:
        raise ValueError('expected canonical normal C3')
    if any(T[x][y] not in kernel for x in kernel for y in kernel):
        raise ValueError('odd elements do not form subgroup')
    if any({T[g][x] for x in kernel}!={T[x][g] for x in kernel} for g in range(n)):
        raise ValueError('C3 not normal')
    other = [i for i in range(m) if i != se]
    signs = lg['signTable']; signsmall = sg['signTable']
    # The quotient complements here are elementary abelian of order2 or4.
    candidates = [x for x in range(n) if x != le and order(T,le,x)==2]
    W = large['crystalline_background']['omegaTable']
    V = small['crystalline_background']['omegaTable']
    chosen = None
    for images in itertools.permutations(candidates,len(other)):
        section = [le]*m
        for h,g in zip(other,images): section[h] = g
        if any(signs[section[x]]!=signsmall[x] for x in range(m)):
            continue
        if any(T[section[x]][section[y]] != section[U[x][y]] for x in range(m) for y in range(m)):
            continue
        projection = [None]*n
        valid = True
        for h in range(m):
            for k in kernel:
                g = T[k][section[h]]
                if projection[g] is not None and projection[g] != h:
                    valid = False
                projection[g] = h
        if not valid or None in projection: continue
        if any(projection[T[x][y]] != U[projection[x]][projection[y]] for x in range(n) for y in range(n)):
            continue
        if any(signs[x] != signsmall[projection[x]] for x in range(n)):
            continue
        rows = [(1 << le,0)]
        for x in range(n):
            for y in range(n):
                mask = (1 << x) ^ (1 << y) ^ (1 << T[x][y])
                rows.append((mask,W[x][y]^V[projection[x]][projection[y]]))
        gauge = gf2_solve(rows,n)
        if gauge is not None:
            chosen = (section,projection,gauge)
            break
    if chosen is None:
        raise ValueError('no sign/background preserving split quotient')
    section,projection,gauge = chosen
    restricted_gauge = [gauge[x] for x in section]
    # This section gauge and projection gauge compose to ZERO because the
    # restriction is the same one-cochain; thus the retraction is strict at
    # the level of central extensions, not just at the level of H2 classes.
    if any(projection[section[x]] != x for x in range(m)):
        raise ValueError('not a retraction')
    for g in range(n):
        for h in range(n):
            if (W[g][h]^V[projection[g]][projection[h]]) != (gauge[g]^gauge[h]^gauge[T[g][h]]):
                raise ValueError('background gauge failed')
    return {
        'large':lg['schoenflies'],'large_hm':lg['hermannMauguin'],
        'small':sg['schoenflies'],'small_hm':sg['hermannMauguin'],
        'physical_convention':'crystalline-spinless/internal-spin-half, s=det, omega=w2+w1^2',
        'large_file':lp.name,'large_sha256':digest(lp),
        'small_file':sp.name,'small_sha256':digest(sp),
        'source_id':large['source_id'],
        'normal_odd_kernel_indices':[x+1 for x in sorted(kernel)],
        'projection_to_small_indices':[x+1 for x in projection],
        'section_to_large_indices':[x+1 for x in section],
        'background_projection_gauge':gauge,
        'background_section_gauge':restricted_gauge,
        'identity_index_large':le+1,'identity_index_small':se+1,
        'equation':'omega_G(g,h)+omega_H(qg,qh)=lambda(g)+lambda(h)+lambda(gh) mod2',
        'central_extension_maps':'Q(a,g)=(a+lambda(g),qg); J(a,h)=(a+lambda(jh),jh); QJ=id',
        'checked':{'all_multiplication_products':True,'normal_kernel_order3':True,
            'qj_identity':True,'all_sign_values':True,'all_background_pairs':True,
            'central_extension_retraction':True},
        'no_classification_value_used_to_select_maps':True,
        'consequence':'Naturality makes q* a split injection on the full classification and all filtered subgroups. Thus any known element order in the small input must occur in the large input.',
        'scope':'This certificate alone proves the split injection. The equality of complete classifications additionally uses odd-kernel/2-primary reasoning.'}


def main():
    out=Path(__file__).with_name('odd_kernel_retractions.json')
    if out.exists(): raise ValueError('refuse overwrite')
    records=[certify(22,4),certify(20,5)]
    out.write_text(json.dumps({'schema':1,'derived_from_frozen_inputs_only':True,
        'classification_calculations_executed':False,'records':records},indent=2,sort_keys=True)+'\n')
    print(out, digest(out))


if __name__=='__main__':main()
