// Majorana dimer states of the seven stages of the 4+1D superfusion heptagon (six-simplex
// 0123456, one layer).  Majorana labels: face index i of the 4-subsets of {0..6}, faces
// containing 0 first (20 of them, lexicographic), then the other 15; A_i = i, B_i = 100+i.
// A pair {phase, a, b, stage} is the projector (1 + i^phase g_a g_b)/2.  Extracted from
// 4DFSPT_Para/Evaluation.hpp; only the state definitions are kept, with the interior
// Majorana list of stage 6 aligned with its n3 list.
#pragma once
#include <bitset>
#include <stdexcept>
#include <vector>

namespace heptagon {
using namespace std;

bitset<35> n3;
bitset<3> omega2;
bitset<2> s1;

void input_parameters(const bitset<25> free_variables) {
    for (int i = 0; i < 20; i++) {
        n3[i] = free_variables[i];
    }
    n3[20] = n3[0] ^ n3[1] ^ n3[4] ^ n3[10];
    n3[21] = n3[0] ^ n3[2] ^ n3[5] ^ n3[11];
    n3[22] = n3[0] ^ n3[3] ^ n3[6] ^ n3[12];
    n3[23] = n3[1] ^ n3[2] ^ n3[7] ^ n3[13];
    n3[24] = n3[1] ^ n3[3] ^ n3[8] ^ n3[14];
    n3[25] = n3[2] ^ n3[3] ^ n3[9] ^ n3[15];
    n3[26] = n3[4] ^ n3[5] ^ n3[7] ^ n3[16];
    n3[27] = n3[4] ^ n3[6] ^ n3[8] ^ n3[17];
    n3[28] = n3[5] ^ n3[6] ^ n3[9] ^ n3[18];
    n3[29] = n3[7] ^ n3[8] ^ n3[9] ^ n3[19];
    n3[30] = n3[10] ^ n3[11] ^ n3[13] ^ n3[16];
    n3[31] = n3[10] ^ n3[12] ^ n3[14] ^ n3[17];
    n3[32] = n3[11] ^ n3[12] ^ n3[15] ^ n3[18];
    n3[33] = n3[13] ^ n3[14] ^ n3[15] ^ n3[19];
    n3[34] = n3[16] ^ n3[17] ^ n3[18] ^ n3[19];

    omega2[0] = free_variables[20];
    omega2[1] = free_variables[21];
    omega2[2] = free_variables[22];

    s1[0] = free_variables[23];
    s1[1] = free_variables[24];
}

const int gamma_A[35] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                         26, 27,
                         28, 29, 30, 31, 32, 33, 34};
const int gamma_B[35] = {100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
                         119,
                         120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134};
const int gamma_inner_legs[21] = {1, 2, 5, 6, 8, 10, 11, 13, 14, 15, 16, 18, 21, 22, 24, 26, 27, 28, 29, 31, 33};

inline int mod4(const int num) {
    int res = num;

    while (res >= 4) {
        res -= 4;
    }

    while (res < 0) {
        res += 4;
    }

    return res;
}

/*Find all Majorana dimer configurations*/

vector<vector<int>>
nontrivial_pairs_4simplex(const int n3_selected[5], const int gamma_selected[5], int omega2_selected, int s1_selected,
                          int P_selected) {
    vector<vector<int>> nontrivial_pair_set;
    int n3_sum = n3_selected[0] + n3_selected[1] + n3_selected[2] + n3_selected[3] + n3_selected[4];
    if (n3_sum == 2) {
        if (n3_selected[0] + n3_selected[1] == 2) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * omega2_selected), gamma_selected[0], gamma_selected[1], P_selected});
        } else if (n3_selected[0] + n3_selected[2] == 2) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * (omega2_selected + s1_selected)), gamma_selected[2], gamma_selected[0],
                                P_selected});
        } else if (n3_selected[0] + n3_selected[3] == 2) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * omega2_selected), gamma_selected[0], gamma_selected[3], P_selected});
        } else if (n3_selected[0] + n3_selected[4] == 2) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * (omega2_selected + s1_selected)), gamma_selected[4], gamma_selected[0],
                                P_selected});
        } else if (n3_selected[1] + n3_selected[2] == 2) {
            nontrivial_pair_set.push_back(vector<int>{3, gamma_selected[2], gamma_selected[1], P_selected});
        } else if (n3_selected[1] + n3_selected[3] == 2) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * s1_selected), gamma_selected[3], gamma_selected[1], P_selected});
        } else if (n3_selected[1] + n3_selected[4] == 2) {
            nontrivial_pair_set.push_back(vector<int>{3, gamma_selected[4], gamma_selected[1], P_selected});
        } else if (n3_selected[2] + n3_selected[3] == 2) {
            nontrivial_pair_set.push_back(vector<int>{3, gamma_selected[2], gamma_selected[3], P_selected});
        } else if (n3_selected[2] + n3_selected[4] == 2) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * s1_selected), gamma_selected[4], gamma_selected[2], P_selected});
        } else if (n3_selected[3] + n3_selected[4] == 2) {
            nontrivial_pair_set.push_back(vector<int>{3, gamma_selected[4], gamma_selected[3], P_selected});
        } else {
            throw std::logic_error("err1: unexpected Majorana configuration");
        }
    } else if (n3_sum == 4) {
        if (n3_selected[0] + n3_selected[1] + n3_selected[2] + n3_selected[3] == 4) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * (omega2_selected + s1_selected)), gamma_selected[2], gamma_selected[0],
                                P_selected});
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * s1_selected), gamma_selected[3], gamma_selected[1], P_selected});
        } else if (n3_selected[0] + n3_selected[1] + n3_selected[2] + n3_selected[4] == 4) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * (omega2_selected + s1_selected)), gamma_selected[2], gamma_selected[0],
                                P_selected});
            nontrivial_pair_set.push_back(vector<int>{3, gamma_selected[4], gamma_selected[1], P_selected});
        } else if (n3_selected[0] + n3_selected[1] + n3_selected[3] + n3_selected[4] == 4) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * omega2_selected), gamma_selected[0], gamma_selected[3], P_selected});
            nontrivial_pair_set.push_back(vector<int>{3, gamma_selected[4], gamma_selected[1], P_selected});
        } else if (n3_selected[0] + n3_selected[2] + n3_selected[3] + n3_selected[4] == 4) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * omega2_selected), gamma_selected[0], gamma_selected[3], P_selected});
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * s1_selected), gamma_selected[4], gamma_selected[2], P_selected});
        } else if (n3_selected[1] + n3_selected[2] + n3_selected[3] + n3_selected[4] == 4) {
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * s1_selected), gamma_selected[3], gamma_selected[1], P_selected});
            nontrivial_pair_set.push_back(
                    vector<int>{mod4(3 + 2 * s1_selected), gamma_selected[4], gamma_selected[2], P_selected});
        } else {
            throw std::logic_error("err2: unexpected Majorana configuration");
        }
    }
    return nontrivial_pair_set;
}

vector<vector<int>> trivial_pairs_six_4simplex(const int n3_selected[8], const int gamma_selected[8], int P_selected) {
    vector<vector<int>> trivial_pair_set;
    for (auto gamma_inner_leg: gamma_inner_legs) {
        int count = 0;
        for (int j = 0; j < 8; j++) {
            if (gamma_inner_leg == gamma_selected[j] && n3_selected[j] == 1) {
                count = 1;
            }
        }
        if (count == 0) {
            trivial_pair_set.push_back(vector<int>{3, gamma_inner_leg, gamma_inner_leg + 100, P_selected});
        }
    }

    return trivial_pair_set;
}

/* F012345 */
vector<vector<int>> all_pairs_six_4simplex_0() {
    vector<vector<int>> all_pair_set;
    //4simplex_01235
    int n3_selected_0[5] = {n3[21], n3[11], n3[5], n3[2], n3[0]};
    int gamma_selected_0[5] = {gamma_B[21], gamma_A[11], gamma_B[5], gamma_A[2], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 0);
    //4simplex_01345
    int n3_selected_1[5] = {n3[26], n3[16], n3[7], n3[5], n3[4]};
    int gamma_selected_1[5] = {gamma_B[26], gamma_A[16], gamma_B[7], gamma_A[5], gamma_B[4]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 0);
    //4simplex_12345
    int n3_selected_2[5] = {n3[30], n3[26], n3[23], n3[21], n3[20]};
    int gamma_selected_2[5] = {gamma_B[30], gamma_A[26], gamma_B[23], gamma_A[21], gamma_B[20]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, omega2[0],
                                                                          s1[0], 0);
    //4simplex_01256
    int n3_selected_3[5] = {n3[25], n3[15], n3[9], n3[3], n3[2]};
    int gamma_selected_3[5] = {gamma_B[25], gamma_A[15], gamma_B[9], gamma_A[3], gamma_B[2]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, 0, 0, 0);
    //4simplex_02356
    int n3_selected_4[5] = {n3[32], n3[18], n3[15], n3[12], n3[11]};
    int gamma_selected_4[5] = {gamma_B[32], gamma_A[18], gamma_B[15], gamma_A[12], gamma_B[11]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, 0, 0, 0);
    //4simplex_03456
    int n3_selected_5[5] = {n3[34], n3[19], n3[18], n3[17], n3[16]};
    int gamma_selected_5[5] = {gamma_B[34], gamma_A[19], gamma_B[18], gamma_A[17], gamma_B[16]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, 0, 0, 0);

    int n3_selected_6[8] = {n3[2], n3[5], n3[11], n3[15], n3[16], n3[18], n3[21], n3[26]};
    int gamma_selected_6[8] = {gamma_A[2], gamma_A[5], gamma_A[11], gamma_A[15], gamma_A[16], gamma_A[18], gamma_A[21],
                               gamma_A[26]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 0);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

/* F012356 */
vector<vector<int>> all_pairs_six_4simplex_1() {
    vector<vector<int>> all_pair_set;
    //4simplex_01236
    int n3_selected_0[5] = {n3[22], n3[12], n3[6], n3[3], n3[0]};
    int gamma_selected_0[5] = {gamma_B[22], gamma_A[12], gamma_B[6], gamma_A[3], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 1);
    //4simplex_01356
    int n3_selected_1[5] = {n3[28], n3[18], n3[9], n3[6], n3[5]};
    int gamma_selected_1[5] = {gamma_B[28], gamma_A[18], gamma_B[9], gamma_A[6], gamma_B[5]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 1);
    //4simplex_12356
    int n3_selected_2[5] = {n3[32], n3[28], n3[25], n3[22], n3[21]};
    int gamma_selected_2[5] = {gamma_B[32], gamma_A[28], gamma_B[25], gamma_A[22], gamma_B[21]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, omega2[0],
                                                                          s1[0], 1);
    //4simplex_03456
    int n3_selected_3[5] = {n3[34], n3[19], n3[18], n3[17], n3[16]};
    int gamma_selected_3[5] = {gamma_B[34], gamma_A[19], gamma_B[18], gamma_A[17], gamma_B[16]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, 0, 0, 1);
    //4simplex_01345
    int n3_selected_4[5] = {n3[26], n3[16], n3[7], n3[5], n3[4]};
    int gamma_selected_4[5] = {gamma_B[26], gamma_A[16], gamma_B[7], gamma_A[5], gamma_B[4]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, 0, 0, 1);
    //4simplex_12345
    int n3_selected_5[5] = {n3[30], n3[26], n3[23], n3[21], n3[20]};
    int gamma_selected_5[5] = {gamma_B[30], gamma_A[26], gamma_B[23], gamma_A[21], gamma_B[20]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, omega2[0],
                                                                          s1[0], 1);

    int n3_selected_6[8] = {n3[5], n3[6], n3[16], n3[18], n3[21], n3[22], n3[26], n3[28]};
    int gamma_selected_6[8] = {gamma_A[5], gamma_A[6], gamma_A[16], gamma_A[18], gamma_A[21], gamma_A[22], gamma_A[26],
                               gamma_A[28]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 1);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

/* F013456 */
vector<vector<int>> all_pairs_six_4simplex_2() {
    vector<vector<int>> all_pair_set;
    //4simplex_01346
    int n3_selected_0[5] = {n3[27], n3[17], n3[8], n3[6], n3[4]};
    int gamma_selected_0[5] = {gamma_B[27], gamma_A[17], gamma_B[8], gamma_A[6], gamma_B[4]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 2);
    //4simplex_01456
    int n3_selected_1[5] = {n3[29], n3[19], n3[9], n3[8], n3[7]};
    int gamma_selected_1[5] = {gamma_B[29], gamma_A[19], gamma_B[9], gamma_A[8], gamma_B[7]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 2);
    //4simplex_13456
    int n3_selected_2[5] = {n3[34], n3[29], n3[28], n3[27], n3[26]};
    int gamma_selected_2[5] = {gamma_B[34], gamma_A[29], gamma_B[28], gamma_A[27], gamma_B[26]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, omega2[1],
                                                                          s1[0], 2);
    //4simplex_01236
    int n3_selected_3[5] = {n3[22], n3[12], n3[6], n3[3], n3[0]};
    int gamma_selected_3[5] = {gamma_B[22], gamma_A[12], gamma_B[6], gamma_A[3], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, 0, 0, 2);
    //4simplex_12356
    int n3_selected_4[5] = {n3[32], n3[28], n3[25], n3[22], n3[21]};
    int gamma_selected_4[5] = {gamma_B[32], gamma_A[28], gamma_B[25], gamma_A[22], gamma_B[21]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, omega2[0],
                                                                          s1[0], 2);
    //4simplex_12345
    int n3_selected_5[5] = {n3[30], n3[26], n3[23], n3[21], n3[20]};
    int gamma_selected_5[5] = {gamma_B[30], gamma_A[26], gamma_B[23], gamma_A[21], gamma_B[20]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, omega2[0],
                                                                          s1[0], 2);

    int n3_selected_6[8] = {n3[6], n3[8], n3[21], n3[22], n3[26], n3[27], n3[28], n3[29]};
    int gamma_selected_6[8] = {gamma_A[6], gamma_A[8], gamma_A[21], gamma_A[22], gamma_A[26], gamma_A[27], gamma_A[28],
                               gamma_A[29]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 2);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

/* F123456 */
vector<vector<int>> all_pairs_six_4simplex_3() {
    vector<vector<int>> all_pair_set;
    //4simplex_12346
    int n3_selected_0[5] = {n3[31], n3[27], n3[24], n3[22], n3[20]};
    int gamma_selected_0[5] = {gamma_B[31], gamma_A[27], gamma_B[24], gamma_A[22], gamma_B[20]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, omega2[0],
                                                                          s1[0], 3);
    //4simplex_12456
    int n3_selected_1[5] = {n3[33], n3[29], n3[25], n3[24], n3[23]};
    int gamma_selected_1[5] = {gamma_B[33], gamma_A[29], gamma_B[25], gamma_A[24], gamma_B[23]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, omega2[0],
                                                                          s1[0], 3);
    //4simplex_23456
    int n3_selected_2[5] = {n3[34], n3[33], n3[32], n3[31], n3[30]};
    int gamma_selected_2[5] = {gamma_B[34], gamma_A[33], gamma_B[32], gamma_A[31], gamma_B[30]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, omega2[2],
                                                                          s1[1], 3);
    //4simplex_01236
    int n3_selected_3[5] = {n3[22], n3[12], n3[6], n3[3], n3[0]};
    int gamma_selected_3[5] = {gamma_B[22], gamma_A[12], gamma_B[6], gamma_A[3], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, 0, 0, 3);
    //4simplex_01346
    int n3_selected_4[5] = {n3[27], n3[17], n3[8], n3[6], n3[4]};
    int gamma_selected_4[5] = {gamma_B[27], gamma_A[17], gamma_B[8], gamma_A[6], gamma_B[4]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, 0, 0, 3);
    //4simplex_01456
    int n3_selected_5[5] = {n3[29], n3[19], n3[9], n3[8], n3[7]};
    int gamma_selected_5[5] = {gamma_B[29], gamma_A[19], gamma_B[9], gamma_A[8], gamma_B[7]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, 0, 0, 3);

    int n3_selected_6[8] = {n3[6], n3[8], n3[22], n3[24], n3[27], n3[29], n3[31], n3[33]};
    int gamma_selected_6[8] = {gamma_A[6], gamma_A[8], gamma_A[22], gamma_A[24], gamma_A[27], gamma_A[29], gamma_A[31],
                               gamma_A[33]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 3);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

/* F012346_inverse */
vector<vector<int>> all_pairs_six_4simplex_4() {
    vector<vector<int>> all_pair_set;
    //4simplex_01234
    int n3_selected_0[5] = {n3[20], n3[10], n3[4], n3[1], n3[0]};
    int gamma_selected_0[5] = {gamma_B[20], gamma_A[10], gamma_B[4], gamma_A[1], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 4);
    //4simplex_02346
    int n3_selected_1[5] = {n3[31], n3[17], n3[14], n3[12], n3[10]};
    int gamma_selected_1[5] = {gamma_B[31], gamma_A[17], gamma_B[14], gamma_A[12], gamma_B[10]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 4);
    //4simplex_01246
    int n3_selected_2[5] = {n3[24], n3[14], n3[8], n3[3], n3[1]};
    int gamma_selected_2[5] = {gamma_B[24], gamma_A[14], gamma_B[8], gamma_A[3], gamma_B[1]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, 0, 0, 4);
    //4simplex_23456
    int n3_selected_3[5] = {n3[34], n3[33], n3[32], n3[31], n3[30]};
    int gamma_selected_3[5] = {gamma_B[34], gamma_A[33], gamma_B[32], gamma_A[31], gamma_B[30]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, omega2[2],
                                                                          s1[1], 4);
    //4simplex_12456
    int n3_selected_4[5] = {n3[33], n3[29], n3[25], n3[24], n3[23]};
    int gamma_selected_4[5] = {gamma_B[33], gamma_A[29], gamma_B[25], gamma_A[24], gamma_B[23]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, omega2[0],
                                                                          s1[0], 4);
    //4simplex_01456
    int n3_selected_5[5] = {n3[29], n3[19], n3[9], n3[8], n3[7]};
    int gamma_selected_5[5] = {gamma_B[29], gamma_A[19], gamma_B[9], gamma_A[8], gamma_B[7]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, 0, 0, 4);

    int n3_selected_6[8] = {n3[1], n3[8], n3[10], n3[14], n3[24], n3[29], n3[31], n3[33]};
    int gamma_selected_6[8] = {gamma_A[1], gamma_A[8], gamma_A[10], gamma_A[14], gamma_A[24], gamma_A[29], gamma_A[31],
                               gamma_A[33]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 4);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

/* F012456_inverse */
vector<vector<int>> all_pairs_six_4simplex_5() {
    vector<vector<int>> all_pair_set;
    //4simplex_01245
    int n3_selected_0[5] = {n3[23], n3[13], n3[7], n3[2], n3[1]};
    int gamma_selected_0[5] = {gamma_B[23], gamma_A[13], gamma_B[7], gamma_A[2], gamma_B[1]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 5);
    //4simplex_02456
    int n3_selected_1[5] = {n3[33], n3[19], n3[15], n3[14], n3[13]};
    int gamma_selected_1[5] = {gamma_B[33], gamma_A[19], gamma_B[15], gamma_A[14], gamma_B[13]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 5);
    //4simplex_01256
    int n3_selected_2[5] = {n3[25], n3[15], n3[9], n3[3], n3[2]};
    int gamma_selected_2[5] = {gamma_B[25], gamma_A[15], gamma_B[9], gamma_A[3], gamma_B[2]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, 0, 0, 5);
    //4simplex_23456
    int n3_selected_3[5] = {n3[34], n3[33], n3[32], n3[31], n3[30]};
    int gamma_selected_3[5] = {gamma_B[34], gamma_A[33], gamma_B[32], gamma_A[31], gamma_B[30]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, omega2[2],
                                                                          s1[1], 5);
    //4simplex_02346
    int n3_selected_4[5] = {n3[31], n3[17], n3[14], n3[12], n3[10]};
    int gamma_selected_4[5] = {gamma_B[31], gamma_A[17], gamma_B[14], gamma_A[12], gamma_B[10]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, 0, 0, 5);
    //4simplex_01234
    int n3_selected_5[5] = {n3[20], n3[10], n3[4], n3[1], n3[0]};
    int gamma_selected_5[5] = {gamma_B[20], gamma_A[10], gamma_B[4], gamma_A[1], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, 0, 0, 5);

    int n3_selected_6[8] = {n3[1], n3[2], n3[10], n3[13], n3[14], n3[15], n3[31], n3[33]};
    int gamma_selected_6[8] = {gamma_A[1], gamma_A[2], gamma_A[10], gamma_A[13], gamma_A[14], gamma_A[15], gamma_A[31],
                               gamma_A[33]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 5);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

/* F023456_inverse */
vector<vector<int>> all_pairs_six_4simplex_6() {
    vector<vector<int>> all_pair_set;
    //4simplex_02345
    int n3_selected_0[5] = {n3[30], n3[16], n3[13], n3[11], n3[10]};
    int gamma_selected_0[5] = {gamma_B[30], gamma_A[16], gamma_B[13], gamma_A[11], gamma_B[10]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 6);
    //4simplex_03456
    int n3_selected_1[5] = {n3[34], n3[19], n3[18], n3[17], n3[16]};
    int gamma_selected_1[5] = {gamma_B[34], gamma_A[19], gamma_B[18], gamma_A[17], gamma_B[16]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 6);
    //4simplex_02356
    int n3_selected_2[5] = {n3[32], n3[18], n3[15], n3[12], n3[11]};
    int gamma_selected_2[5] = {gamma_B[32], gamma_A[18], gamma_B[15], gamma_A[12], gamma_B[11]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, 0, 0, 6);
    //4simplex_01245
    int n3_selected_3[5] = {n3[23], n3[13], n3[7], n3[2], n3[1]};
    int gamma_selected_3[5] = {gamma_B[23], gamma_A[13], gamma_B[7], gamma_A[2], gamma_B[1]};
    vector<vector<int>> nontrivial_pair_set_3 = nontrivial_pairs_4simplex(n3_selected_3, gamma_selected_3, 0, 0, 6);
    //4simplex_01256
    int n3_selected_4[5] = {n3[25], n3[15], n3[9], n3[3], n3[2]};
    int gamma_selected_4[5] = {gamma_B[25], gamma_A[15], gamma_B[9], gamma_A[3], gamma_B[2]};
    vector<vector<int>> nontrivial_pair_set_4 = nontrivial_pairs_4simplex(n3_selected_4, gamma_selected_4, 0, 0, 6);
    //4simplex_01234
    int n3_selected_5[5] = {n3[20], n3[10], n3[4], n3[1], n3[0]};
    int gamma_selected_5[5] = {gamma_B[20], gamma_A[10], gamma_B[4], gamma_A[1], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_5 = nontrivial_pairs_4simplex(n3_selected_5, gamma_selected_5, 0, 0, 6);

    int n3_selected_6[8] = {n3[1], n3[2], n3[10], n3[11], n3[13], n3[15], n3[16], n3[18]};
    int gamma_selected_6[8] = {gamma_A[1], gamma_A[2], gamma_A[10], gamma_A[11], gamma_A[13], gamma_A[15], gamma_A[16], gamma_A[18]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_six_4simplex(n3_selected_6, gamma_selected_6, 6);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_3.begin(), nontrivial_pair_set_3.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_4.begin(), nontrivial_pair_set_4.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_5.begin(), nontrivial_pair_set_5.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

}  // namespace heptagon
