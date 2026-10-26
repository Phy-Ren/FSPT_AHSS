#!/usr/bin/env python3
"""Exact rank-two odd-charge cubic lattice; see proofs/TWO_FACTOR_GYSIN_PROOF.md.

The six coordinates form an integral lattice basis of odd cubic polynomials
on (q0,q1) with q0 odd. Only finite-group periodicity relations are imposed.
"""
from itertools import product
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form


def coordinates(q0, q1):
    assert q0 % 2
    return [q0, (q0**3-q0)//24, q1, (q1**3-q1)//6,
            ((q0*q0-1)*q1)//8, (q0*q1*q1-q1)//2]


def presentation(m, n):
    rows=[]
    for t,q1 in product(range(3), repeat=2):
        q0=2*t+1
        v=coordinates(q0,q1)
        for p0,p1 in [(q0+2*m,q1),(q0,q1+n)]:
            rows.append([a-b for a,b in zip(coordinates(p0,p1),v)])
    return Matrix(rows)


def factors(m,n):
    matrix=smith_normal_form(presentation(m,n), domain=ZZ)
    return [abs(int(matrix[i,i])) for i in range(6) if abs(matrix[i,i])!=1]


if __name__=='__main__':
    for m,n in product([2,4,8,16,32],repeat=2):
        print(m,n,factors(m,n))
