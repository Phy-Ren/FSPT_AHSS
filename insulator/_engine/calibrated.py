"""The sole adopted convention: sheet-linear calibration, cubic 1/6, epsilon 0."""
from .simplex import O4d, F, bin0, background, Fopen
from .product4d import E5, lower_gauge
from .gauge4d import gauge_phase
from .transgression import O3canonical, E4canonical
from .prism import gauge3 as cylinder_gauge3


def calibration(a, sheet, s, r):
    return bin0(r).cup(bin0(background(a, s)[1]), 0, True).cup(bin0(sheet), 0, True).sc(F(1, 2)).ret(s.tw)


def source4(a, k, n, s, r):
    if not k.maxabs() and not n.d().maxabs():
        return (a.cup(n) + bin0(n).sq(2).sc(F(1, 2))).ret(s.tw)
    return O4d(a, k, n, s, r, F(1, 6)) + calibration(a, k, s, r)


def product4(a, k, n, l, m, s, r):
    if not k.maxabs() and not l.maxabs():
        return Fopen(n, m).ret(s.tw)
    return E5(a, k, n, l, m, s, r, F(1, 6))


def gauge4(a, k, n, s, r, u, v):
    return gauge_phase(a, k, n, s, r, u, v, F(1, 6)) + calibration(a, u, s, r)


def source3_base(a, k, n, s, r):
    if not k.maxabs() and not n.d().maxabs():
        return (a.cup(n) + bin0(n).sq(2).sc(F(1, 2))).ret(s.tw)
    return O3canonical(a, k, n, s, r)


def source3(a, k, n, s, r):
    return source3_base(a, k, n, s, r) + calibration(a, k, s, r)


def product3(a, k, n, l, m, s, r):
    if not k.maxabs() and not l.maxabs() and not n.d().maxabs() and not m.d().maxabs():
        return Fopen(n, m).ret(s.tw)
    return E4canonical(a, k, n, l, m, s, r)


def gauge3(a, k, n, s, r, u, v):
    return cylinder_gauge3(a, k, n, s, r, u, v, phase_formula=source3_base) + calibration(a, u, s, r)
