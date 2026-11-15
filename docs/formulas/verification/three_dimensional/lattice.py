"""Effective Majorana zero modes of the 3+1D p+ip decoration on the lattice.

This module builds the two complete Majorana pairings of an F move and of a
stacking (P) move, as described in Secs. V and VI of the 3+1D stacking paper,
and counts the change of fermion parity from their transition loops.  No
formula for O_4 or E_3 is used here; the checks compare the counts with the
formulas afterwards.

Conventions
-----------
* Inputs are the physical fields of docs/formulas/THREE_DIMENSIONAL.md:
  n1 (signed integer, Z_s1), n2 (binary, dn2 = (omega2 + s1 s1)[n1]_2),
  omega2 and s1.  Faces are increasing vertex tuples.
* Layers of p-ip type are traded for p+ip layers by adding 4K(j-i) trivial
  layers on the edge <ij>, after expressing the integer relative to the first
  vertex (Appendix E of the paper).
* Effective Majorana zero modes of a tetrahedron are listed in the order
  (<013>B, <123>B, psi..., <012>A, <023>A) and consecutive entries are paired.
* A directed pair [u, v] means -i chi_u chi_v = +1.
"""
from __future__ import annotations

from itertools import combinations


def face(cell, j):
    return cell[:j] + cell[j + 1:]


def _check_input(nv, n1, n2, omega, s):
    for name, values, degree, binary in (('n1', n1, 1, False), ('n2', n2, 2, True),
                                         ('omega2', omega, 2, True), ('s1', s, 1, True)):
        if set(values) != set(combinations(range(nv), degree + 1)):
            raise ValueError(f'{name}: give every face of degree {degree}')
        if any(type(v) is not int or (binary and v not in (0, 1)) for v in values.values()):
            raise ValueError(f'{name}: invalid value')
    for f in combinations(range(nv), 3):
        if sum(s[e] for e in combinations(f, 2)) % 2:
            raise ValueError(f'ds1 is nonzero on {f}')
        i, j, k = f
        if (-1) ** s[i, j] * n1[j, k] - n1[i, k] + n1[i, j]:
            raise ValueError(f'd_s1 n1 is nonzero on {f}')
    for f in combinations(range(nv), 4):
        if sum(omega[g] for g in combinations(f, 3)) % 2:
            raise ValueError(f'domega2 is nonzero on {f}')
        i, j, k, l = f
        source = (omega[i, j, k] + s[i, j] * s[j, k]) * (n1[k, l] % 2)
        if (source + sum(n2[g] for g in combinations(f, 3))) % 2:
            raise ValueError(f'dn2 differs from (omega2+s1 s1)[n1]_2 on {f}')


def layer_numbers(n1, s):
    """Nonnegative layer numbers relative to the first vertex.

    The integer is multiplied by (-1)^{s1(0i)} at its first vertex i, and
    4K(j-i) trivial layers are added on <ij> with the smallest K >= 0.
    """
    t = {i: s[0, i] if i else 0 for i in {v for e in n1 for v in e}}
    signed = {e: (-1) ** t[e[0]] * n for e, n in n1.items()}
    K = max([0] + [max(0, (-n + 4 * (e[1] - e[0]) - 1) // (4 * (e[1] - e[0])))
                   for e, n in signed.items()])
    return {e: n + 4 * K * (e[1] - e[0]) for e, n in signed.items()}


def loops(dimers_in, dimers_out, count):
    """Parity change between two directed perfect matchings.

    Each alternating transition loop with M arrows against the direction of
    traversal changes the parity by 1 + M modulo two.  The second value is
    an independent count: the inversion parity of the two ordered words of
    paired operators.  Both are returned.
    """
    def matching(dimers):
        partner, forward = {}, set()
        for u, v in dimers:
            if u == v or u in partner or v in partner:
                raise ValueError('every mode needs exactly one partner')
            partner[u], partner[v] = v, u
            forward.add((u, v))
        if set(partner) != set(range(count)):
            raise ValueError('the matching does not cover every mode')
        return partner, forward

    states = [matching(dimers_in), matching(dimers_out)]
    remaining, parity = set(range(count)), 0
    while remaining:
        start = node = min(remaining)
        color = against = 0
        while True:
            partner, forward = states[color]
            nxt = partner[node]
            against += (node, nxt) not in forward
            remaining.discard(node)
            node, color = nxt, color ^ 1
            if node == start and color == 0:
                break
        parity ^= (1 + against) % 2
    word = 0
    for partner, forward in states:
        seen = 0
        for u in range(count):
            v = partner[u]
            if u < v:
                for x in ((u, v) if (u, v) in forward else (v, u)):
                    word ^= bin(seen >> (x + 1)).count('1') & 1
                    seen |= 1 << x
    return parity, word


# F move ------------------------------------------------------------------

IN3 = ((1, 2, 3, 4), (0, 1, 3, 4), (0, 1, 2, 3))
OUT3 = ((0, 1, 2, 4), (0, 2, 3, 4))


def f_move(n1, n2, omega, s):
    """Parity change of the F move (1234,0134,0123) -> (0124,0234) on Delta^4.

    Returns the transition-loop count and the independent word count.
    """
    _check_input(5, n1, n2, omega, s)
    L = layer_numbers(n1, s)
    w = {f: omega[f] ^ (s[f[:2]] * s[f[1:]]) for f in omega}
    modes, ids = [], {}
    triangles = tuple(combinations(range(5), 3))
    for f in triangles:
        ids[f] = len(modes)
        modes += [('chain', f, 'A'), ('chain', f, 'B')]

    def array(cell, height, width):
        out = []
        for _ in range(height):
            out.append(list(range(len(modes), len(modes) + width)))
            modes.extend(('projective', cell) for _ in range(width))
        return out

    references = {'in': [], 'out': []}
    rows_0124 = array((0, 1, 2, 4), w[0, 1, 2], L[2, 4])
    rows_0234 = array((0, 2, 3, 4), w[0, 2, 3], L[3, 4])
    x = L[3, 4]
    rows = [row[:x] for row in rows_0124] + rows_0234
    parked = [row[x:] for row in rows_0124]
    needed = w[1, 2, 3] + w[0, 1, 3]
    if len(rows) != needed:
        if {len(rows), needed} != {0, 2}:
            raise ValueError('only a pair of projective rows can appear or disappear')
        if len(rows) == 2:
            references['in'] += list(zip(rows[0], rows[1]))
            rows = []
        else:
            rows = array(None, 2, x)
            references['out'] += list(zip(rows[0], rows[1]))
    flat = lambda a: [q for row in a for q in row]
    k = w[1, 2, 3]
    projective = {'in': {(1, 2, 3, 4): flat(rows[:k]), (0, 1, 3, 4): flat(rows[k:]),
                         (0, 1, 2, 3): flat(parked)},
                  'out': {(0, 1, 2, 4): flat(rows_0124), (0, 2, 3, 4): flat(rows_0234)}}
    exterior = len(modes) if len(modes) % 2 else None
    if exterior is not None:
        modes.append(('exterior',))
    matchings = {}
    for side, order in (('in', IN3), ('out', OUT3)):
        dimers, incidence = [], {f: [] for f in triangles}
        for cell in order:
            listed, polarity = [], {}
            for j in (2, 0):
                f = face(cell, j)
                incidence[f].append(j)
                if n2[f]:
                    listed.append(ids[f] + 1)
                    polarity[ids[f] + 1] = 1
            for mode in projective[side][cell]:
                listed.append(mode)
                polarity[mode] = 1
            for j in (3, 1):
                f = face(cell, j)
                incidence[f].append(j)
                if n2[f]:
                    listed.append(ids[f])
                    polarity[ids[f]] = 0
            if len(listed) % 2:
                raise ValueError(f'odd number of modes in {cell}')
            for u, v in zip(listed[::2], listed[1::2]):
                flip = 0
                if cell[0] == 1:
                    flip = omega[0, 1, 2] * ((ids[cell[1:]] + 1) in (u, v))
                    flip ^= s[0, 1] * (1 ^ polarity[u] ^ polarity[v])
                dimers.append((v, u) if flip else (u, v))
        dimers += references[side]
        ports = []
        for f, js in incidence.items():
            if not n2[f] or not js:
                dimers.append((ids[f], ids[f] + 1))
            elif len(js) == 1:
                ports.append(ids[f] + js[0] % 2)
        if exterior is not None:
            ports.append(exterior)
        ports.sort()
        dimers += list(zip(ports[::2], ports[1::2]))
        matchings[side] = dimers
    return loops(matchings['in'], matchings['out'], len(modes))


# P move ------------------------------------------------------------------

ORDER = ((0, 1, 3), (1, 2, 3), (0, 1, 2), (0, 2, 3))


def p_move(n1, n2, m1, m2, omega, s):
    """Parity change of stacking two states on one tetrahedron (0123).

    The lower state (m1, m2) is moved into the upper state (n1, n2).  The
    initial pairing pairs each state by its own rule and adds the exchange
    chains; the final pairing pairs the chains on every dual line and the
    surviving modes by the rule of a single state.  Returns the
    transition-loop count and the independent word count.
    """
    _check_input(4, n1, n2, omega, s)
    _check_input(4, m1, m2, omega, s)
    N, K = layer_numbers(n1, s), layer_numbers(m1, s)
    t = {0: 0, 1: s[0, 1], 2: s[0, 2], 3: s[0, 3]}
    w012 = omega[0, 1, 2] ^ (s[0, 1] * s[1, 2])
    modes, ordinary, initial = [], {}, []

    def new(bit):
        modes.append(bit)
        return len(modes) - 1

    residual = {}
    for state, layers, bits in (('upper', N, n2), ('lower', K, m2)):
        for j, f in enumerate(ORDER):
            if bits[f]:
                ordinary[state, f] = new(int(j < 2))
        residual[state] = [new(1) for _ in range(w012 * layers[2, 3])]
        listed = ([ordinary[state, f] for f in ORDER[:2] if bits[f]] + residual[state]
                  + [ordinary[state, f] for f in ORDER[2:] if bits[f]])
        if len(listed) % 2:
            raise ValueError('odd number of modes in a single state')
        initial += list(zip(listed[::2], listed[1::2]))
    chains = {f: [[new(b % 2) for b in range(K[f[1:]])] for _ in range(N[f[:2]])]
              for f in ORDER}
    for a in range(N[1, 2]):
        for b in range(K[2, 3]):
            initial.append((chains[1, 2, 3][a][b], chains[0, 2, 3][a][b]))
    for a in range(N[0, 1]):
        for b in range(K[2, 3]):
            initial.append((chains[0, 1, 3][a][b], chains[0, 2, 3][N[1, 2] + a][b]))
        for b in range(K[1, 2]):
            initial.append((chains[0, 1, 3][a][K[2, 3] + b], chains[0, 1, 2][a][b]))
    final, survivors = [], {}
    for j, f in enumerate(ORDER):
        listed = ([ordinary[g, f] for g, bits in (('upper', n2), ('lower', m2)) if bits[f]]
                  + [q for row in chains[f] for q in row])
        odd = len(listed) % 2
        paired = listed[:-1] if odd else listed
        for a, b in zip(paired[::2], paired[1::2]):
            flip = int(j < 2) ^ (t[f[0]] * (1 ^ modes[a] ^ modes[b]))
            final.append((b, a) if flip else (a, b))
        if odd:
            a = listed[-1]
            survivors[f] = (a, t[f[0]] * (modes[a] ^ int(j < 2)))
    core = ([survivors[f] for f in ORDER[:2] if f in survivors]
            + [(r, 0) for r in residual['upper'] + residual['lower']]
            + [survivors[f] for f in ORDER[2:] if f in survivors])
    if len(core) % 2:
        raise ValueError('odd number of modes in the stacked state')
    for (a, ea), (b, eb) in zip(core[::2], core[1::2]):
        final.append((b, a) if ea ^ eb else (a, b))
    return loops(initial, final, len(modes))
