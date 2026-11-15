"""Exact test data: solutions of the lower 3+1D equations on an ordered simplex."""
from itertools import combinations

import formulas as F
from formulas import C, cup, ds


def faces(N, q):
    return list(combinations(range(N + 1), q + 1))


def frozen(c, N):
    return C(c.deg, values={f: c(f) for f in faces(N, c.deg)}, mod=c.mod)


def random_cochain(N, q, rng, low=None, high=None):
    if low is None:
        return C(q, values={f: rng.randrange(2) for f in faces(N, q)})
    return C(q, values={f: rng.randint(low, high) for f in faces(N, q)}, mod=None)


def cone(z, N):
    """A primitive of a closed cochain z on Delta^N: x(f) = z(0f) off vertex 0."""
    return frozen(C(z.deg - 1, fun=lambda f: 0 if 0 in f else z((0,) + f), mod=z.mod), N)


def background(N, rng):
    s = frozen(random_cochain(N, 0, rng).d(), N)
    w = frozen(random_cochain(N, 1, rng).d(), N)
    return s, w


def state(N, rng, s, w, pip=True, n1=None):
    """Random n1, n2, n3 with d_s1 n1 = 0, dn2 = O_3 and dn3 = O_4."""
    if n1 is None:
        n1 = frozen(ds(random_cochain(N, 0, rng, -4, 4), s), N) if pip else C(1, mod=None)
    n2 = frozen(cone(frozen(F.O3(n1, w, s), N), N) + random_cochain(N, 1, rng).d(), N)
    n3 = frozen(cone(frozen(F.O4(n1, n2, w, s), N), N) + random_cochain(N, 2, rng).d(), N)
    assert all(F.O3(n1, w, s)(f) % 2 == n2.d()(f) for f in faces(N, 3))
    assert all(F.O4(n1, n2, w, s)(f) % 2 == n3.d()(f) for f in faces(N, 4))
    return dict(n1=n1, n2=n2, n3=n3)


def torsion_state(free):
    """The torsion branch n1 = s1 on Delta^4 from its independent face values.

    free maps ('s_1', (0,i)), ('omega_2', (0,i,j)), ('n_2', (0,i,j)) and
    ('n_3', (0,i,j,k)) to bits.  These are the values on faces containing the
    vertex 0; all other faces follow from the lower equations.
    """
    N = 4

    def closed(name, q):
        values = {f: free[name, f] for f in faces(N, q) if f[0] == 0}
        for f in faces(N, q):
            if f[0]:
                values[f] = sum(values[(0,) + f[:j] + f[j + 1:]] for j in range(len(f))) % 2
        return C(q, values=values)
    s, w = closed('s_1', 1), closed('omega_2', 2)
    n1 = frozen(s.lift(), N)
    o3 = F.O3(n1, w, s)
    base2 = closed('n_2', 2)
    n2 = C(2, values={f: (base2(f) + (o3((0,) + f) if f[0] else 0)) % 2 for f in faces(N, 2)})
    o4 = F.O4(n1, n2, w, s)
    base3 = closed('n_3', 3)
    n3 = C(3, values={f: (base3(f) + (o4((0,) + f) if f[0] else 0)) % 2 for f in faces(N, 3)})
    assert all(o3(f) % 2 == n2.d()(f) for f in faces(N, 3))
    assert all(o4(f) % 2 == n3.d()(f) for f in faces(N, 4))
    return s, w, dict(n1=n1, n2=n2, n3=n3)


TORSION_VARIABLES = ([('s_1', f) for f in faces(4, 1) if f[0] == 0]
                     + [('omega_2', f) for f in faces(4, 2) if f[0] == 0]
                     + [('n_2', f) for f in faces(4, 2) if f[0] == 0]
                     + [('n_3', f) for f in faces(4, 3) if f[0] == 0])


def phase_difference(fn, N, s):
    """(d_s1 phi)(01...N) for a phase phi given on the faces of Delta^N."""
    top = tuple(range(N + 1))
    total = 0
    for j in range(N + 1):
        sign = (1 - 2 * s((0, 1))) if j == 0 else (-1) ** j
        total += sign * fn(top[:j] + top[j + 1:])
    return total % 1
