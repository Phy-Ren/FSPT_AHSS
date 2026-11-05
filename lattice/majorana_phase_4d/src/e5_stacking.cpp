// Stacking Majorana phase E_5^gamma of the 4+1D FSPT (loop of README.md, Sec. "Stacking loop").
//
// Configuration index (23 bits, least significant first): n3 on the ten faces of 012345
// containing 0 (0123, 0124, 0125, 0134, 0135, 0145, 0234, 0235, 0245, 0345), the same for
// n3', then omega2(012), s1(01), s1(02).
//
// usage: e5_stacking first last out.bin
//   writes one int8 per configuration: E_5^gamma in units of 1/8 (-1 would mean a vanishing
//   loop, which does not occur); prints the diagnostics of the dimer-state tracker.
#include <cstdio>
#include <cstdlib>
#include <vector>

#include "loop_word.hpp"
#include "stacking_states.hpp"

using loopword::Move;
using loopword::Pair;
namespace S = stacking;

// Majorana of the four-simplex simp on its face opposite to the local vertex j
// (B side for even j, A side for odd j), upper or lower layer.
static int majorana(const std::vector<int> &simp, int j, bool lower) {
    std::vector<int> f;
    for (int t = 0; t < 5; t++) if (t != j) f.push_back(simp[t]);
    int idx = 0, k = 0;
    for (int a = 0; a < 6; a++)
        for (int b = a + 1; b < 6; b++)
            for (int c = b + 1; c < 6; c++)
                for (int d = c + 1; d < 6; d++, k++)
                    if (std::vector<int>{a, b, c, d} == f) idx = k;
    return idx + (j % 2 == 0 ? 20 : 0) + (lower ? 40 : 0);
}

// F(012345): 2345B, 1234B, 0123B, 1235A.
static Move fmove(bool lower, bool forward) {
    int off = lower ? 40 : 0;
    Move m;
    m.priority = {S::gamma_B[14] + off, S::gamma_B[10] + off, S::gamma_B[0] + off, S::gamma_A[11] + off};
    m.forward = forward;
    return m;
}

// P(01234): 1234B', 0134B', 0124A' (local labels of the four-simplex).
static Move pmove(const std::vector<int> &simp, bool forward) {
    Move m;
    m.priority = {majorana(simp, 0, true), majorana(simp, 2, true), majorana(simp, 3, true)};
    m.forward = forward;
    return m;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: e5_stacking first last out.bin\n"); return 2; }
    long first = atol(argv[1]), last = atol(argv[2]);
    std::vector<int8_t> out;
    out.reserve(last - first);
    loopword::Diagnostics dg;
    for (long idx = first; idx < last; idx++) {
        S::input_parameters(std::bitset<23>(idx));
        // dimer states grouped by stage (label)
        std::vector<std::vector<Pair>> st(8);
        auto add = [&](const std::vector<std::vector<int>> &v) {
            for (auto &p : v) st[p[3]].push_back({p[1], p[2], p[0] & 3});
        };
        auto p01 = S::all_pairs_Pmove_0_1();
        add(p01.first); add(p01.second);
        add(S::all_pairs_Fmove_2()); add(S::all_pairs_Fmove_3());
        auto p45 = S::all_pairs_Pmove_4_5();
        add(p45.first); add(p45.second);
        add(S::all_pairs_Fmove_6()); add(S::all_pairs_Fmove_7());

        loopword::Builder B(80, dg);
        B.start(st[7]);                                   // |psi>: N3 on 01234, 01245, 02345
        // Pbar_02345, Pbar_01245, Pbar_01234 (02345 acts first)
        B.project(st[0], &st[2]);
        B.project(st[1], &st[2]);
        B.insert(st[2], {pmove({0, 2, 3, 4, 5}, false), pmove({0, 1, 2, 4, 5}, false),
                         pmove({0, 1, 2, 3, 4}, false)});
        B.project(st[2]);                                 // two layers n3, n3' on the old simplices
        // F'_012345 then F_012345
        B.insert(st[3], {fmove(true, true), fmove(false, true)});
        B.project(st[3]);                                 // two layers on 01235, 01345, 12345
        // P_12345 (nonstandard, U(g_1)), P_01345, P_01235 (12345 acts first)
        Move p12345 = pmove({1, 2, 3, 4, 5}, true);
        p12345.sign = {{S::gamma_Bp[14], 2 * ((S::omega2 + S::s1[0]) & 1)}, {S::gamma_Bp[12], 2 * S::s1[0]}};
        B.insert(st[4], {p12345, pmove({0, 1, 3, 4, 5}, true), pmove({0, 1, 2, 3, 5}, true)}, &st[6]);
        B.project(st[4], &st[6]);
        B.project(st[5], &st[6]);
        B.project(st[6]);                                 // one layer N3 on the new simplices
        // Fbar^tot_012345
        B.insert(st[7], {fmove(false, false)});
        B.close(st[7]);
        out.push_back((int8_t)B.evaluate());
    }
    FILE *f = fopen(argv[3], "wb");
    fwrite(out.data(), 1, out.size(), f);
    fclose(f);
    long zero = 0;
    for (auto v : out) zero += v < 0;
    printf("configurations %ld vanishing_loops %ld vanishing_projections %ld no_candidate %ld insertion_on_outside_mode %ld\n",
           last - first, zero, dg.vanishing, dg.no_candidate, dg.insertion_free);
    return (zero || dg.vanishing || dg.no_candidate) ? 1 : 0;
}
