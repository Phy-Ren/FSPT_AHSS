// Exact evaluation of Majorana words  Tr( F_1 F_2 ... F_L ) up to a positive factor.
//
// A factor is either a fixed Majorana monomial  i^phase * g_1 g_2 ... g_r  (written order),
// or a projector  (1 + i^phase g_a g_b)  (the factor 1/2 is dropped).
// Expanding every projector gives a sum over x in F_2^m (x_k = 1 selects the bilinear of
// projector k).  A term has nonzero trace iff every Majorana occurs an even number of times
// (linear constraints over F_2), and then equals i^{Phi(x)} with
//     Phi(x) = sum of phases + 2 * (number of inversions of the selected word)   (mod 4),
// because sorting the word with adjacent transpositions of distinct Majoranas gives one
// sign per transposition and the sorted word is a product of squares gamma^2 = 1.
// The inversion number is additive over pairs of factors, so Phi is a Z_4-valued quadratic
// form in x.  The constrained sum of i^Phi is a quadratic Gauss sum, evaluated exactly by
// eliminating one variable at a time.  The result is 0 or 2^{mag/2} e^{i pi phase8/4}.
#pragma once
#include <bitset>
#include <cstdint>
#include <stdexcept>
#include <vector>

namespace gauss {

constexpr int MAXV = 512;
using Row = std::bitset<MAXV>;

struct Factor {
    bool proj;            // true: (1 + i^phase g[0] g[1]); false: i^phase g[0] g[1] ...
    int phase;            // exponent of i, mod 4
    std::vector<int> g;   // Majorana labels in written order
};

struct Result {
    bool zero = false;
    int phase8 = 0;       // argument in units of pi/4
    int mag = 0;          // |value| = 2^{mag/2} up to the dropped positive factors
};

struct Form {             // Phi = c0 + sum a_k x_k + 2 sum_{k<l} B_kl x_k x_l  (mod 4)
    int n = 0;
    std::vector<uint8_t> a;
    std::vector<Row> B;   // symmetric, zero diagonal
    int c0 = 0;
    Row freev;
};

template <class F>
inline void for_bits(const Row &r, F f) {
    for (size_t k = r._Find_first(); k < MAXV; k = r._Find_next(k)) f((int)k);
}

// Substitute x_j = e XOR (XOR_{k in R} x_k), R a set of free variables not containing j.
inline void subst(Form &F, int j, int e, const Row &R) {
    const int aj = F.a[j];
    Row S = F.B[j];
    for_bits(S, [&](int k) { F.B[k].reset(j); });
    F.B[j].reset();
    F.a[j] = 0;
    F.freev.reset(j);
    // a_j x_j with the integer lift  x_j = e + sum_R x - 2 e sum_R x - 2 sum_{k<l in R} x_k x_l
    F.c0 = (F.c0 + aj * e) & 3;
    const int lin = (aj + ((aj & 1) ? 2 * e : 0)) & 3;
    for_bits(R, [&](int k) { F.a[k] = (F.a[k] + lin) & 3; });
    if (aj & 1) {
        for_bits(R, [&](int k) {
            F.B[k] ^= R;
            F.B[k].reset(k);
        });
    }
    // 2 x_j sum_{k in S} x_k with x_j = e + sum_R x (mod 2)
    if (e) for_bits(S, [&](int k) { F.a[k] = (F.a[k] + 2) & 3; });
    Row SR = S & R;
    for_bits(SR, [&](int k) { F.a[k] = (F.a[k] + 2) & 3; });
    for_bits(S, [&](int k) { F.B[k] ^= R; });
    for_bits(R, [&](int m) { F.B[m] ^= S; });
}

inline Result evaluate(const std::vector<Factor> &word) {
    Result res;
    // compact Majorana labels
    int maxlab = 0;
    for (auto &f : word)
        for (int g : f.g) maxlab = std::max(maxlab, g);
    std::vector<int> lab(maxlab + 1, -1);
    int nm = 0;
    for (auto &f : word)
        for (int g : f.g)
            if (lab[g] < 0) lab[g] = nm++;

    const int L = (int)word.size();
    std::vector<int> var(L, -1);
    int m = 0;
    for (int u = 0; u < L; u++)
        if (word[u].proj) {
            if (word[u].g.size() != 2) throw std::runtime_error("projector needs two Majoranas");
            var[u] = m++;
        }
    if (m > MAXV) throw std::runtime_error("too many projectors");

    Form F;
    F.n = m;
    F.a.assign(m, 0);
    F.B.assign(m, Row());
    for (int k = 0; k < m; k++) F.freev.set(k);

    // internal inversions and phases
    for (int u = 0; u < L; u++) {
        const auto &g = word[u].g;
        int inv = 0;
        for (size_t p = 0; p < g.size(); p++)
            for (size_t q = p + 1; q < g.size(); q++) inv += g[p] > g[q];
        const int t = (word[u].phase + 2 * (inv & 1)) & 3;
        if (word[u].proj) F.a[var[u]] = (F.a[var[u]] + t) & 3;
        else F.c0 = (F.c0 + t) & 3;
    }
    // cross inversions between factors u < v
    for (int u = 0; u < L; u++) {
        const auto &gu = word[u].g;
        for (int v = u + 1; v < L; v++) {
            const auto &gv = word[v].g;
            int c = 0;
            for (int x : gu)
                for (int y : gv) c += x > y;
            if (!(c & 1)) continue;
            if (word[u].proj && word[v].proj) {
                F.B[var[u]].flip(var[v]);
                F.B[var[v]].flip(var[u]);
            } else if (word[u].proj) {
                F.a[var[u]] = (F.a[var[u]] + 2) & 3;
            } else if (word[v].proj) {
                F.a[var[v]] = (F.a[var[v]] + 2) & 3;
            } else {
                F.c0 = (F.c0 + 2) & 3;
            }
        }
    }
    // parity constraints: every Majorana occurs an even number of times
    std::vector<Row> rows(nm);
    std::vector<int> rhs(nm, 0);
    for (int u = 0; u < L; u++)
        for (int g : word[u].g) {
            if (word[u].proj) rows[lab[g]].flip(var[u]);
            else rhs[lab[g]] ^= 1;
        }
    for (int c = 0; c < nm; c++) {
        Row R = rows[c];
        const int e = rhs[c];
        if (R.none()) {
            if (e) { res.zero = true; return res; }
            continue;
        }
        const int j = (int)R._Find_first();
        Row Rj = R;
        Rj.reset(j);
        for (int d = c + 1; d < nm; d++)
            if (rows[d][j]) { rows[d] ^= R; rhs[d] ^= e; }
        subst(F, j, e, Rj);
    }
    // Gauss sum over the remaining free variables
    while (F.freev.any()) {
        const int v = (int)F.freev._Find_first();
        Row Lr = F.B[v];
        const int av = F.a[v];
        for_bits(Lr, [&](int k) { F.B[k].reset(v); });
        F.B[v].reset();
        F.a[v] = 0;
        F.freev.reset(v);
        if (av & 1) {
            res.mag += 1;
            res.phase8 += (av == 1) ? 1 : 7;
            for_bits(Lr, [&](int k) { F.a[k] = (F.a[k] + 4 - av) & 3; });
            for_bits(Lr, [&](int k) {
                F.B[k] ^= Lr;
                F.B[k].reset(k);
            });
        } else {
            res.mag += 2;
            if (Lr.none()) {
                if (av == 2) { res.zero = true; return res; }
            } else {
                const int j = (int)Lr._Find_first();
                Row R = Lr;
                R.reset(j);
                subst(F, j, av / 2, R);
            }
        }
    }
    res.phase8 = (res.phase8 + 2 * F.c0) & 7;
    return res;
}

}  // namespace gauss
