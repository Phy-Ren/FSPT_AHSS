// Dense linear system over Z/8 (Gauss-Jordan, pivots of minimal 2-adic valuation).
// stdin: m n, then m rows "k  col val  col val ... rhs" ; stdout: "OK" + n values, or "NO".
#include <cstdint>
#include <cstdio>
#include <vector>
int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 1;
    std::vector<uint8_t> A((size_t)m * (n + 1), 0);
    for (int i = 0; i < m; i++) {
        int k;
        if (scanf("%d", &k) != 1) return 1;
        for (int t = 0; t < k; t++) { int c, v; if (scanf("%d %d", &c, &v) != 2) return 1; A[(size_t)i * (n + 1) + c] = (A[(size_t)i * (n + 1) + c] + v) & 7; }
        int b;
        if (scanf("%d", &b) != 1) return 1;
        A[(size_t)i * (n + 1) + n] = b & 7;
    }
    auto at = [&](int i, int j) -> uint8_t & { return A[(size_t)i * (n + 1) + j]; };
    std::vector<int> pc, pv;
    std::vector<char> used(n, 0);
    int r = 0;
    for (int v = 0; v < 3 && r < m; v++) {
        bool progress = true;
        while (progress && r < m) {
            progress = false;
            // find any entry with valuation exactly v in rows >= r, unused columns
            int pi = -1, pj = -1;
            for (int i = r; i < m && pi < 0; i++)
                for (int j = 0; j < n; j++)
                    if (!used[j] && at(i, j) && (at(i, j) & ((1 << (v + 1)) - 1)) == (1 << v)) { pi = i; pj = j; break; }
            if (pi < 0) break;
            if (pi != r) for (int j = 0; j <= n; j++) std::swap(at(r, j), at(pi, j));
            int u = (at(r, pj) >> v) & 7;   // odd, self-inverse
            for (int i = 0; i < m; i++) {
                if (i == r || !at(i, pj)) continue;
                if (i < r && (at(i, pj) & ((1 << v) - 1))) continue;   // left to back-substitution
                int f = ((at(i, pj) >> v) * u) & 7;
                uint8_t *ri = &at(i, 0), *rr = &at(r, 0);
                for (int j = 0; j <= n; j++) ri[j] = (ri[j] - f * rr[j]) & 7;
            }
            pc.push_back(pj); pv.push_back(v); used[pj] = 1; r++; progress = true;
        }
    }
    for (int i = r; i < m; i++) {
        bool nz = false;
        for (int j = 0; j < n; j++) if (at(i, j)) { nz = true; break; }
        if (!nz && at(i, n)) { printf("NO\n"); return 0; }
        if (nz) { fprintf(stderr, "residual row with nonzero coefficients\n"); printf("NO\n"); return 0; }
    }
    std::vector<int> x(n, 0);
    for (int k = r - 1; k >= 0; k--) {
        int c = pc[k], v = pv[k];
        int rhs = at(k, n);
        for (int j = 0; j < n; j++) if (j != c) rhs -= at(k, j) * x[j];
        rhs &= 7;
        if (rhs % (1 << v)) { printf("NO\n"); return 0; }
        x[c] = ((rhs >> v) * ((at(k, c) >> v) & 7)) & 7;
    }
    printf("OK");
    for (int j = 0; j < n; j++) printf(" %d", x[j]);
    printf("\n");
}
