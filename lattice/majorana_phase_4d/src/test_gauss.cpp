// Brute-force check of gauss::evaluate against the direct projector expansion.
#include <complex>
#include <cstdio>
#include <random>
#include "gauss.hpp"
using namespace gauss;

static std::complex<long double> brute(const std::vector<Factor> &w) {
    std::vector<int> pr;
    for (size_t u = 0; u < w.size(); u++) if (w[u].proj) pr.push_back((int)u);
    const int m = (int)pr.size();
    std::complex<long double> tot = 0;
    const std::complex<long double> I(0, 1);
    for (long x = 0; x < (1L << m); x++) {
        std::vector<int> s;
        int ph = 0, k = 0;
        for (size_t u = 0; u < w.size(); u++) {
            bool take = !w[u].proj || ((x >> k) & 1);
            if (w[u].proj) k++;
            if (!take) continue;
            ph += w[u].phase;
            for (int g : w[u].g) s.push_back(g);
        }
        // bubble sort, -1 per swap of distinct elements
        int sw = 0;
        for (size_t i = 0; i + 1 < s.size(); i++)
            for (size_t j = 0; j + 1 < s.size() - i; j++)
                if (s[j] > s[j + 1]) { std::swap(s[j], s[j + 1]); sw++; }
        bool ok = true;
        for (size_t i = 0; i < s.size();) {
            size_t j = i;
            while (j < s.size() && s[j] == s[i]) j++;
            if ((j - i) & 1) { ok = false; break; }
            i = j;
        }
        if (!ok) continue;
        ph = (ph + 2 * (sw & 1)) & 3;
        std::complex<long double> t = 1;
        for (int q = 0; q < ph; q++) t *= I;
        tot += t;
    }
    return tot;
}

int main() {
    // the four-Majorana example of the paper: (1+i)
    std::vector<Factor> ex = {
        {true, 3, {0, 1}}, {true, 3, {2, 3}}, {true, 3, {0, 2}}, {true, 3, {3, 1}},
        {false, 0, {2}},   {true, 3, {3, 0}}, {true, 3, {1, 2}}, {false, 0, {1}}};
    auto r = evaluate(ex);
    auto b = brute(ex);
    printf("paper example: zero=%d phase8=%d mag=%d  brute=(%Lg,%Lg)\n", r.zero, r.phase8, r.mag,
           b.real(), b.imag());

    std::mt19937 rng(12345);
    int bad = 0, nz = 0, tests = 200000;
    for (int t = 0; t < tests; t++) {
        int nmaj = 2 + rng() % 7, L = 1 + rng() % 16;
        std::vector<Factor> w;
        for (int u = 0; u < L; u++) {
            Factor f;
            f.proj = rng() % 3 != 0;
            f.phase = rng() % 4;
            if (f.proj) {
                int a = rng() % nmaj, c;
                do c = rng() % nmaj; while (c == a);
                f.g = {a, c};
                if (rng() % 2) f.phase = (f.phase | 1);  // mostly Hermitian projectors
            } else {
                int r = rng() % 3;
                for (int q = 0; q < r; q++) f.g.push_back(rng() % nmaj);
            }
            w.push_back(f);
        }
        auto e = evaluate(w);
        auto bb = brute(w);
        bool bz = std::abs(bb) < 1e-9;
        bool ok;
        if (bz || e.zero) ok = bz && e.zero;
        else {
            long double ang = std::arg(bb) / (M_PI / 4);
            long double d = ang - e.phase8;
            while (d > 4) d -= 8;
            while (d < -4) d += 8;
            long double mag = std::pow(2.0L, e.mag / 2.0L);
            ok = std::fabs(d) < 1e-6 && std::fabs(std::abs(bb) / mag - std::round(std::abs(bb) / mag)) < 1e-6;
            // magnitude up to a power of two from dropped factors: check ratio is a power of 2
            long double ratio = std::abs(bb) / mag;
            long double l2 = std::log2(ratio);
            ok = std::fabs(d) < 1e-6 && std::fabs(l2 - std::round(l2)) < 1e-6;
            nz++;
        }
        if (!ok) {
            if (bad < 5) printf("mismatch: zero=%d ph=%d brute=(%Lg,%Lg)\n", e.zero, e.phase8, bb.real(), bb.imag());
            bad++;
        }
    }
    printf("random tests: %d, nonzero %d, mismatches %d\n", tests, nz, bad);
    return bad != 0;
}
