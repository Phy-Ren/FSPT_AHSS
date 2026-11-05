// Heptagon Majorana phase O_6^gamma of the 4+1D FSPT (loop of README.md, Sec. "Heptagon loop").
//
// Configuration index (25 bits, least significant first): n3 on the twenty faces of 0123456
// containing 0 (lexicographic: 0123, 0124, ..., 0456), omega2(012), omega2(013), omega2(023),
// s1(01), s1(02).
//
// usage: o6_heptagon first last out.bin   (one int8 per configuration, units of 1/8)
#include <cstdio>
#include <cstdlib>
#include <vector>

#include "heptagon_states.hpp"
#include "loop_word.hpp"

using loopword::Move;
using loopword::Pair;
namespace H = heptagon;

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: o6_heptagon first last out.bin\n"); return 2; }
    long first = atol(argv[1]), last = atol(argv[2]);
    using H::gamma_A;
    using H::gamma_B;
    // selection priority of the seven F moves, local labels 2345B, 1234B, 0123B, 1235A:
    // F012345, F012356, F013456, F123456 (nonstandard), F012346, F012456, F023456
    const int prio[7][4] = {{gamma_B[30], gamma_B[20], gamma_B[0], gamma_A[21]},
                            {gamma_B[32], gamma_B[21], gamma_B[0], gamma_A[22]},
                            {gamma_B[34], gamma_B[26], gamma_B[4], gamma_A[27]},
                            {gamma_B[34], gamma_B[30], gamma_B[20], gamma_A[31]},
                            {gamma_B[31], gamma_B[20], gamma_B[0], gamma_A[22]},
                            {gamma_B[33], gamma_B[23], gamma_B[1], gamma_A[24]},
                            {gamma_B[34], gamma_B[30], gamma_B[10], gamma_A[31]}};
    std::vector<int8_t> out;
    out.reserve(last - first);
    loopword::Diagnostics dg;
    for (long idx = first; idx < last; idx++) {
        H::input_parameters(std::bitset<25>(idx));
        std::vector<std::vector<std::vector<int>>> raw = {
            H::all_pairs_six_4simplex_0(), H::all_pairs_six_4simplex_1(), H::all_pairs_six_4simplex_2(),
            H::all_pairs_six_4simplex_3(), H::all_pairs_six_4simplex_4(), H::all_pairs_six_4simplex_5(),
            H::all_pairs_six_4simplex_6()};
        std::vector<std::vector<Pair>> st(7);
        for (int j = 0; j < 7; j++)
            for (auto &p : raw[j]) st[j].push_back({p[1], p[2], p[0] & 3});
        const int w0 = H::omega2[0], w1 = H::omega2[1], s0 = H::s1[0];
        loopword::Builder B(140, dg);
        B.start(st[6]);
        // move j acts on state j and projects onto state j-1 (move 0: onto state 6).
        // Moves 6, 5, 4 (F023456, F012456, F012346) are forward; 3, 2, 1, 0 are inverse.
        for (int j = 6; j >= 0; j--) {
            Move m;
            m.priority.assign(prio[j], prio[j] + 4);
            m.forward = j >= 4;
            if (j == 3)   // U(g_1) signs of the inserted Majoranas of the nonstandard F(123456)
                m.sign = {{gamma_B[34], 2 * ((w1 + s0) & 1)}, {gamma_B[30], 2 * ((w0 + s0) & 1)},
                          {gamma_B[20], 2 * s0}, {gamma_A[31], 2 * w0}};
            const auto &next = st[(j + 6) % 7];
            B.insert(next, {m});
            if (j > 0) B.project(next);
            else B.close(next);
        }
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
