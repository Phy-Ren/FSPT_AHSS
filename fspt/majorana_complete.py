"""Closed-Majorana source and stacking laws through 4+1 spacetime dimensions.

This is an independent transcription of the displayed cochain formulas. The
input Majorana degree q is 1, 2, or 3. Phases are exact integer numerators over
eight. The CA and operator coordinates are transported together; neither is
silently identified with the integer-layer publication coordinate.
"""
from functools import lru_cache

from .formulas import (cup, field, gamma as old_gamma, majorana_product,
                       majorana_source, phase, square, stacking as old_stacking,
                       word, zero)


def second_carry(a):
    p = a.beta()
    return (p + p.reduce().lift()).divide(2)


def gamma(a, w, s):
    q = a.degree
    if q in (1, 2):
        return old_gamma(a, w, s)
    if q != 3:
        raise ValueError("Majorana degree must be one, two, or three")
    p = a.beta()
    r = p.reduce()
    intrinsic = cup(r, r, 2)
    for label in ("1213243142", "1213431412", "1232431421", "1234314212"):
        intrinsic = intrinsic + word(label, a, a, a, a)
    sq, wa, sr = cup(a, a, 1), w*a, s*r
    binary = (word("12313434", w, w, a, a) + intrinsic
              + cup(sq, wa, 4) + cup(sq, sr, 4) + cup(wa, sr, 4)
              + word("12314343", s, s, r, r) + cup(w, s, 1)*r
              + s*sq + s*s*second_carry(a).reduce())
    return phase((4, binary), (2, cup(w, p, integer=True)),
                 (2, cup(p, p, 2, integer=True)))


def operator_gauge(c):
    return phase((4, cup(c, c.differential(), c.degree)))


def obstruction(a, c, w, s, coordinate="ca"):
    result = phase((4, square(c, 2) + w*c)) + gamma(a, w, s)
    if coordinate == "operator":
        result = result + operator_gauge(c).twisted_differential(s)
    elif coordinate != "ca":
        raise ValueError(coordinate)
    return result.reduce(8)


def intrinsic(a, b):
    """The grouped displayed intrinsic polynomial and its cone-last descent."""
    q = a.degree
    if q not in (2, 3):
        raise ValueError("The stable intrinsic polynomial starts in degree two")
    n = a+b
    u, t = cup(a, b, q), cup(a, b, q-1)
    r, rp = a.beta().reduce(), b.beta().reduce()
    result = zero(q+2)
    groups = (
        (("12131432412", "12343213431", "23412342324"), (a, b, b, b)),
        (("12123434123", "12131412324", "12134131234", "12312412423",
          "12314324123", "12314342413", "13242412314", "13412321341",
          "13412321413", "13413142134", "13432412314", "31214124324"),
         (a, a, b, b)),
        (("12413432312",), (a, a, a, b)),
        (("12131432412",), (b, a, a, n)),
        (("12131432412",), (n, a, a, b)),
        (("12131432412", "12134341321"), (n, b, b, a)),
        (("1212312",), (n, b, u)),
        (("12313123",), (b, a, t)),
        (("12131232",), (r, b, b)),
        (("123131212",), (cup(b, b, q-2), a, n)),
        (("123131212",), (cup(n, n, q-2), b, a)),
    )
    for labels, inputs in groups:
        for label in labels:
            # A vanished desuspension must have the final output degree,
            # including groups whose first argument has degree q+1 or q+2.
            label_out = label
            for _ in range(3-q):
                arity = len(inputs)
                if len(set(label_out[-arity:])) != arity:
                    label_out = None
                    break
                reduced = label_out[:-(arity-1)]
                if set(reduced) != set(label_out):
                    label_out = None
                    break
                label_out = reduced
            if label_out is not None:
                result = result + word(label_out, *inputs)
    return (result + cup(t, b, q-1) + cup(r+rp, u, q-1)
            + cup(u, r+rp+cup(b, a, q-1), q-1)
            + cup(t, cup(a, a, q-2)+cup(b, b, q-2), q+1)
            + cup(b, cup(a, t, q-1), q) + cup(rp, r, q))


def pure_stacking(a, b, w, s):
    q = a.degree
    if q == 1:
        return old_stacking(a, zero(2), b, zero(2), w, s)
    if q not in (2, 3):
        raise ValueError("Majorana degree must be one, two, or three")
    n = a+b
    p, qp, rp = a.beta(), b.beta(), n.beta()
    r, rb = p.reduce(), qp.reduce()
    u, t = cup(a, b, q), cup(a, b, q-1)
    m = t+s*u
    b2 = cup(b, b, q-2)
    carry = (second_carry(n)-second_carry(a)-second_carry(b)).reduce()
    binary = (intrinsic(a, b) + cup(w*n, m, q+1)
              + cup(t.differential(), w*n, q+2) + cup(b2, w*a, q+2)
              + cup(b2+w*b, s*r, q+2) + cup(w, s, 1)*u
              + cup(t, s*(r+rb), q+1) + cup(cup(n, n, q-2), s*u, q+1)
              + cup(t, s*u, q)
              + s*(m+cup(r, rb, q+1)+cup(u, u, q-1)
                   + cup(r+rb, s*u, q+1)+cup(s*u, u, q)+carry))
    ulift = u.lift()
    quarter = (cup(p, qp, q, integer=True).scale((-1)**(q+1))
               + cup(p+qp, ulift, q-1, integer=True).scale((-1)**q)
               - cup(ulift, rp, q-1, integer=True)
               + cup(ulift, ulift, q-2, integer=True)
               - cup(w, ulift, integer=True))
    return phase((4, binary), (2, quarter))


def stacking(a, c, b, cp, w, s, coordinate="ca"):
    q = a.degree
    m = majorana_product(a, b, s)
    gw = phase((4, cup(c, cp, q) + cup(c.differential(), cp, q+1)
                + cup(c+cp, m, q)))
    result = pure_stacking(a, b, w, s) + gw
    if coordinate == "operator":
        result = (result + operator_gauge(c+cp+m)
                  - operator_gauge(c) - operator_gauge(cp))
    elif coordinate != "ca":
        raise ValueError(coordinate)
    return result.reduce(8)


@lru_cache(None)
def expression(operation, q, coordinate="ca"):
    if q not in (1, 2, 3):
        raise ValueError("Majorana degree must be one, two, or three")
    a, b = field("a", q), field("b", q)
    c, cp = field("c", q+1), field("cp", q+1)
    w, s = field("w", 2), field("s", 1)
    if operation == "majorana_source":
        return majorana_source(a, w, s)
    if operation == "majorana_product":
        return majorana_product(a, b, s)
    if operation == "obstruction":
        return obstruction(a, c, w, s, coordinate)
    if operation == "stacking":
        return stacking(a, c, b, cp, w, s, coordinate)
    raise ValueError(operation)
