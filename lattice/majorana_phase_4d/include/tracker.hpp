// Dimer-state tracker: follows the Majorana pairing through a sequence of projections and
// insertions, finds the transition loops of every projection step, and decides by the
// Kasteleyn rule whether the step is nonzero.  Used to choose the inserted Majoranas from
// the paper's rule and to locate any step that would annihilate the state.
#pragma once
#include <stdexcept>
#include <string>
#include <vector>

namespace trk {

struct Pair { int a, b, phase; };   // projector (1 + i^phase g_a g_b): direction a->b iff phase == 3

struct Loop {
    std::vector<int> modes;
    bool closed;
    bool kasteleyn;   // parity preserved (only meaningful for closed loops)
};

struct State {
    std::vector<int> partner;   // -1: not paired inside the region (outer or free)
    std::vector<char> from;     // 1 if the mode is the tail of its pairing arrow
    explicit State(int n = 0) : partner(n, -1), from(n, 0) {}
};

inline bool is_tail(const Pair &p, int x) { return (p.phase & 3) == 3 ? x == p.a : x == p.b; }

// Transition loops of the projection onto the pairs T from the current state.
inline std::vector<Loop> loops(const State &s, const std::vector<Pair> &T) {
    const int n = (int)s.partner.size();
    std::vector<int> np(n, -1);
    std::vector<char> nf(n, 0);
    for (auto &p : T) {
        if (np[p.a] >= 0 || np[p.b] >= 0) throw std::runtime_error("overlapping pairs in one stage");
        np[p.a] = p.b; np[p.b] = p.a;
        nf[p.a] = is_tail(p, p.a); nf[p.b] = is_tail(p, p.b);
    }
    std::vector<char> seen(n, 0);
    std::vector<Loop> out;
    for (auto &p : T) {
        int u = p.a;
        if (seen[u]) continue;
        // walk: new edge, old edge, new edge, ...
        Loop L;
        L.closed = false;
        int M = 0;
        int x = u;
        std::vector<int> fw;
        while (true) {
            if (fw.size() > 400) throw std::runtime_error("walk did not terminate");
            fw.push_back(x); seen[x] = 1;
            int y = np[x];
            M += nf[x] ? 0 : 1;               // traverse x->y along the new bond
            fw.push_back(y); seen[y] = 1;
            int z = s.partner[y];
            if (z < 0) break;                  // path leaves the region
            M += s.from[y] ? 0 : 1;            // traverse y->z along the old bond
            if (z == u) { L.closed = true; break; }
            if (np[z] < 0) { fw.push_back(z); break; }   // old partner not re-paired: released
            x = z;
        }
        if (!L.closed) {
            // extend backwards from u along its old bond
            int z = s.partner[u];
            std::vector<int> bw;
            while (z >= 0) {
                if (bw.size() > 400) throw std::runtime_error("backward walk did not terminate");
                bw.push_back(z);
                if (np[z] < 0) break;
                seen[z] = 1;
                int y = np[z];
                bw.push_back(y); seen[y] = 1;
                z = s.partner[y];
            }
            std::vector<int> all(bw.rbegin(), bw.rend());
            all.insert(all.end(), fw.begin(), fw.end());
            L.modes = all;
            L.kasteleyn = true;
        } else {
            L.modes = fw;
            // fw lists every site of the loop once
            L.kasteleyn = (M & 1) == 1;
        }
        out.push_back(L);
    }
    return out;
}

inline void project(State &s, const std::vector<Pair> &T) {
    for (auto &p : T) {
        for (int x : {p.a, p.b}) {
            int o = s.partner[x];
            if (o >= 0) { s.partner[o] = -1; }
        }
    }
    for (auto &p : T) {
        s.partner[p.a] = p.b; s.partner[p.b] = p.a;
        s.from[p.a] = is_tail(p, p.a); s.from[p.b] = is_tail(p, p.b);
    }
}

// A Majorana acting on a dimer state reverses the arrow of the pair containing it.
inline bool insert(State &s, int g) {
    int o = s.partner[g];
    if (o < 0) return false;
    s.from[g] ^= 1; s.from[o] ^= 1;
    return true;
}

}  // namespace trk
