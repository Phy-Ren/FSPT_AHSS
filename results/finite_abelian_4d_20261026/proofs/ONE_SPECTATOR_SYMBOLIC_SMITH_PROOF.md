# Uniform Smith reduction for one spectator

Derived independently from the exact Gysin presentation, 2026-10-26.
This proves all four closed cases for arbitrary powers of two m,N >= 2.
No bounded grid of parameter values is used.

## 1. Newton coefficients of the exact relation lattice

Put q0=2t+1 and write q=q1.
The six index coordinates become

    v = (2t+1, t(t+1)(2t+1)/6, q, (q^3-q)/6,
         t(t+1)q/2, t q^2+(q^2-q)/2).

The two periodicities are t -> t+m and q -> q+N.
Expand their differences in the integral Newton basis

    1, t, binom(t,2), q, binom(q,2), t q.

The resulting rows are:

    A00 = (2m, a, 0, 0, 0, 0),  a=m(m+1)(2m+1)/6;
    A10 = (0, m(m+2), 0, 0, 0, 0);
    A20 = (0, 2m, 0, 0, 0, 0);
    A01 = (0, 0, 0, 0, b, m),   b=m(m+1)/2;
    A02 = (0, 0, 0, 0, 0, 2m);
    A11 = (0, 0, 0, 0, m, 0);

    B00 = (0, 0, N, c, 0, d),   c=N(N^2-1)/6, d=N(N-1)/2;
    B10 = (0, 0, 0, 0, N, N^2);
    B20 = (0, 0, 0, 0, N, 0);
    B01 = (0, 0, 0, e, 0, N),   e=N(N+1)/2;
    B02 = (0, 0, 0, N, 0, 0);
    B11 = (0, 0, 0, 0, 0, 2N).

Finite differences express every Newton row as an integral combination of the original 3×3 evaluation rows.
Conversely, every evaluation row is an integral combination of these Newton rows.
Thus this replacement preserves the exact integer relation lattice.

A10=((m+2)/2)A20 is redundant.
B10=B20+(N/2)B11 is redundant.
The first two columns now separate completely, with presentation

    [2m  a ]
    [ 0  2m].

Since a has 2-adic valuation v2(m)-1, its Smith factors are m/2 and 8m.
This is exactly the distinguished cyclic direct summand.

## 2. The remaining four-generator presentation

Use generators (a0,b0,c0,z) for the remaining columns.
Set g=gcd(m,N).
The relations m c0=N c0=0 combine into g c0=0.
The relations 2m z=2N z=0 combine into 2g z=0.
The mixed block therefore has presentation

    b c0 + m z = 0,
    g c0 = 0,
    2g z = 0,
    N a0 + c b0 + d z = 0,
    e b0 + N z = 0,
    N b0 = 0.

All groups under consideration are 2-primary, so Smith reduction over Z_(2) determines their complete invariant factors.
In this local ring, every odd integer is a unit.

First, N b0=0 is redundant: twice the relation e b0+N z=0 is

    N(N+1)b0+2N z=0,

and 2N z=0 follows from 2g z=0.
Because N+1 is odd, this is equivalent to N b0=0.

Next,

    c/e = (N-1)/3.

Subtract this multiple of e b0+N z=0 from the relation containing a0.
The result is

    N a0 + (N/2)((N-1)/3)z = 0.

The coefficient (N-1)/3 is an odd unit, so rescaling a0 gives

    N a + (N/2)z = 0.

No other relation uses a.

The relation e b0+N z=0 can be written

    (N/2)((N+1)b0+2z)=0.

Replace b0 by the new generator b1=(N+1)b0+2z.
No other surviving relation uses b0, so this splits off Z_(N/2).

Similarly, the first relation is

    (m/2)((m+1)c0+2z)=0.

Set c1=(m+1)c0+2z.
Since 2g z=0, the relation g c0=0 is equivalent to g c1=0.
The c1 generator therefore splits off

    Z_h,   h=gcd(m/2,g)=gcd(m/2,N).

The remaining two generators a,z have the matrix

    [N  N/2]
    [0  2g ].

Its first determinantal divisor is

    k=gcd(N/2,2g),

and its determinant is 2Ng.
The two Smith factors are k and 2Ng/k.

Thus the complete one-spectator contribution is

    Z_(N/2) × Z_gcd(m/2,N) × Z_k × Z_(2Ng/k),
    g=gcd(m,N),  k=gcd(N/2,2g).

## 3. The four stated cases

For powers of two the gcd formula reduces uniformly as follows.

1. N<m: g=N, h=N, k=N/2, giving
   Z_(N/2)^2 × Z_N × Z_(4N).
2. N=m: g=m, h=m/2, k=m/2, giving
   Z_(m/2)^3 × Z_(4m).
3. m<N<4m: necessarily N=2m, so g=m, h=m/2, k=m=N/2, giving
   Z_(m/2) × Z_(N/2)^2 × Z_(4m).
4. N>=4m: g=m, h=m/2, k=2m, giving
   Z_(m/2) × Z_(2m) × Z_(N/2) × Z_N.

These are precisely the four cases in the manuscript.
The derivation is a symbolic row-and-column reduction for arbitrary exponents.
