// Assembly of a closed loop of moves into one Majorana operator word.
//
// The loop is described in acting order (the first operation acts first on the initial
// dimer state) by projections onto dimer states and by inserted Majoranas.  Insertions
// are chosen by the selection rule: on every parity-changing transition loop of the next
// projection, the first candidate of the move's priority list lying on the loop is
// inserted.  In a forward move the selected Majoranas act in priority order; the inverse
// move inserts Gamma^dagger, i.e. the reverse order.  The tracker checks that every
// projection is nonzero.  The written word is the reverse of the acting sequence.
#pragma once
#include <algorithm>
#include <cstdint>
#include <stdexcept>
#include <vector>

#include "gauss.hpp"
#include "tracker.hpp"

namespace loopword {

using trk::Pair;

struct Move {
    std::vector<int> priority;             // selection priority (candidate Majoranas)
    bool forward = true;                   // forward: act in priority order
    std::vector<std::pair<int, int>> sign; // (Majorana, i^phase) carried by an inserted mode
};

struct Diagnostics {
    long vanishing = 0;        // projections with a non-Kasteleyn loop after the insertions
    long no_candidate = 0;     // parity-changing loops without a candidate
    long insertion_free = 0;   // insertions on a Majorana paired outside the region
};

class Builder {
public:
    Builder(int modes, Diagnostics &d) : st_(modes), modes_(modes), dg_(d) {}

    // Set the initial dimer state.  Its projector enters the word once, at the end of the
    // loop (close); the trace then equals <psi| loop |psi> up to a positive factor.
    void start(const std::vector<Pair> &T) { trk::project(st_, T); }

    // Project onto the pairs T.  Pairs implied by the projection scheme (a Majorana whose
    // partner is re-paired by T takes its partner in the reference state R if that partner
    // is also left unpaired) are tracked as part of the state; as projectors they are
    // redundant and are not written into the word.
    void project(const std::vector<Pair> &T, const std::vector<Pair> *R = nullptr) {
        auto C = complete(T, R);
        for (auto &l : trk::loops(st_, C))
            if (l.closed && !l.kasteleyn) { dg_.vanishing++; break; }
        trk::project(st_, C);
        for (auto &p : T) acting_.push_back({true, p.phase & 3, {p.a, p.b}});
    }

    // Final projection back onto the initial state.
    void close(const std::vector<Pair> &T) { project(T); }

    // Insert the Majoranas of a group of moves (given in acting order) for the coming
    // projection T.
    void insert(const std::vector<Pair> &T, const std::vector<Move> &moves,
                const std::vector<Pair> *R = nullptr) {
        auto C = complete(T, R);
        std::vector<std::vector<int>> sel(moves.size());
        for (auto &l : trk::loops(st_, C)) {
            if (!l.closed || l.kasteleyn) continue;
            int found = -1, fm = -1;
            for (size_t m = 0; m < moves.size() && found < 0; m++)
                for (int c : moves[m].priority) {
                    if (std::find(l.modes.begin(), l.modes.end(), c) != l.modes.end()) {
                        found = c; fm = (int)m; break;
                    }
                }
            if (found < 0) { dg_.no_candidate++; continue; }
            sel[fm].push_back(found);
        }
        for (size_t m = 0; m < moves.size(); m++) {
            std::vector<int> s;
            for (int c : moves[m].priority)
                if (std::find(sel[m].begin(), sel[m].end(), c) != sel[m].end()) s.push_back(c);
            if (!moves[m].forward) std::reverse(s.begin(), s.end());
            for (int g : s) {
                int ph = 0;
                for (auto &q : moves[m].sign) if (q.first == g) ph = (ph + q.second) & 3;
                if (!trk::insert(st_, g)) dg_.insertion_free++;
                acting_.push_back({false, ph, {g}});
            }
        }
    }

    // Exact phase of the loop: phase8 in units of pi/4, or -1 if the loop vanishes.
    int evaluate() const {
        std::vector<gauss::Factor> w(acting_.rbegin(), acting_.rend());
        auto r = gauss::evaluate(w);
        return r.zero ? -1 : r.phase8;
    }

private:
    std::vector<Pair> complete(const std::vector<Pair> &T0, const std::vector<Pair> *R) const {
        std::vector<Pair> T = T0;
        if (!R) return T;
        std::vector<int> rp(modes_, -1), ri(modes_, -1);
        for (size_t q = 0; q < R->size(); q++) {
            rp[(*R)[q].a] = (*R)[q].b; rp[(*R)[q].b] = (*R)[q].a;
            ri[(*R)[q].a] = ri[(*R)[q].b] = (int)q;
        }
        bool changed = true;
        while (changed) {
            changed = false;
            std::vector<char> inT(modes_, 0);
            for (auto &p : T) inT[p.a] = inT[p.b] = 1;
            auto orphan = [&](int x) { int o = st_.partner[x]; return !inT[x] && o >= 0 && inT[o]; };
            for (int x = 0; x < modes_ && !changed; x++) {
                if (!orphan(x)) continue;
                int q = rp[x];
                if (q < 0 || inT[q]) continue;
                if (orphan(q) || st_.partner[q] < 0) { T.push_back((*R)[ri[x]]); changed = true; }
            }
        }
        return T;
    }

    trk::State st_;
    int modes_;
    Diagnostics &dg_;
    std::vector<gauss::Factor> acting_;
};

}  // namespace loopword
