// Majorana dimer states of the 4+1D stacking loop (one five-simplex 012345, two layers).
//
// Majorana labels: face index i of the 4-subsets of {0..5} in lexicographic order
// (0:0123 1:0124 2:0125 3:0134 4:0135 5:0145 6:0234 7:0235 8:0245 9:0345
//  10:1234 11:1235 12:1245 13:1345 14:2345); upper layer A_i = i, B_i = 20+i,
// lower layer A'_i = 40+i, B'_i = 60+i.  A pair {phase, a, b, label} is the projector
// (1 + i^phase g_a g_b)/2; phase 3 means the pairing arrow a -> b.  The label is the
// stage of the loop (see README.md).  Extracted from 4DFSPT/Stacking.hpp; only the state
// definitions are kept, with the first-step label of the in-plane branch corrected.
#pragma once
#include <bitset>
#include <stdexcept>
#include <utility>
#include <vector>

namespace stacking {
using namespace std;

int n3[15];
int n3p[15];
int N3[15];
int omega2;
int s1[2];

constexpr int PATH_LEN_MAX = 60; // PATH_MAX already used in Mac command line tools
constexpr int GAM_MAX = 75;
constexpr auto NO_EDGE = bitset<PATH_LEN_MAX>(0);
constexpr int STACKING_MAX_WO_OMEGA2_S1 = 1048576; // 2^20
constexpr int STACKING_MAX = 8388608; // 2^23

inline bool have_overlap(const bitset<PATH_LEN_MAX> & a, const bitset<PATH_LEN_MAX> & b) {
    for (int i = 0; i < PATH_LEN_MAX; i++) {
        if ((a[i] && b[i])) {
            return true;
        }
    }
    return false;
}

void input_parameters(const bitset<23> free_variables) {
    for (int i = 0; i < 10; i = i + 1) {
        n3[i] = free_variables[i];
    }
    n3[10] = n3[0] ^ n3[1] ^ n3[3] ^ n3[6];
    n3[11] = n3[0] ^ n3[2] ^ n3[4] ^ n3[7];
    n3[12] = n3[1] ^ n3[2] ^ n3[5] ^ n3[8];
    n3[13] = n3[3] ^ n3[4] ^ n3[5] ^ n3[9];
    n3[14] = n3[6] ^ n3[7] ^ n3[8] ^ n3[9];

    for (int i = 0; i < 10; i = i + 1) {
        n3p[i] = free_variables[i + 10];
    }
    n3p[10] = n3p[0] ^ n3p[1] ^ n3p[3] ^ n3p[6];
    n3p[11] = n3p[0] ^ n3p[2] ^ n3p[4] ^ n3p[7];
    n3p[12] = n3p[1] ^ n3p[2] ^ n3p[5] ^ n3p[8];
    n3p[13] = n3p[3] ^ n3p[4] ^ n3p[5] ^ n3p[9];
    n3p[14] = n3p[6] ^ n3p[7] ^ n3p[8] ^ n3p[9];

    for (int i = 0; i < 15; i = i + 1) {
        N3[i] = n3[i] ^ n3p[i];
    }

    omega2 = free_variables[20];//omega2(012)

    s1[0] = free_variables[21];//s1(01)
    s1[1] = free_variables[22];//s1(02)

}

int gamma_A[15] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};
int gamma_B[15] = {20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34};
int gamma_Ap[15] = {40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54};
int gamma_Bp[15] = {60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74};
int gamma_inner_legs[12] = {1, 4, 6, 8, 11, 13, 41, 44, 46, 48, 51, 53};

inline int mod4(int num) {
    while (num >= 4) {
        num = num - 4;
    }
    return num;
}

inline int mod8(int num) {
    while (num >= 8) {
        num = num - 8;
    }
    return num;
}


/*Find all Majorana dimer configurations*/
//This part can be changed when consider other problems

inline vector<vector<int>>
nontrivial_pairs_4simplex(const int n3_selected[5], int gamma_selected[5], int omega2_selected, int s1_selected,
                          int P_selected) {
    //Get all the nontrivial Majorana pairs in a 4-simplex
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


inline vector<vector<int>> trivial_pairs_Fmove_2layers(vector<int> &n3_selected, vector<int> &gamma_selected, int P_selected) {
    //Get all the trivial Majorana pairs in all the (at most) six 4-simplexes, (at least) three 4-simplexes
    vector<vector<int>> trivial_pair_set;
    for (int i = 0; i < 12; i++) {
        int count = 0;
        for (size_t j = 0; j < n3_selected.size(); j++) {
            if (gamma_inner_legs[i] == gamma_selected[j] && n3_selected[j] == 1) {
                count = 1;
            }
        }
        if (count == 0) {
            trivial_pair_set.push_back(vector<int>{3, gamma_inner_legs[i], gamma_inner_legs[i] + 20, P_selected});
        }
    }

    return trivial_pair_set;
}


inline vector<int> one_dimer(int gam1[2], int gam2[2],int gamma_slt[5] , int omega2, int s1, int P) {
    //gam = (gamma_index, top or down) top = 0, down = 1
    if (gam1[0] == 0) {
        if (gam2[0] == 1) {
            return vector<int>{mod4(3 + 2 * omega2), gamma_slt[0] + gam1[1]*40, gamma_slt[1] + gam2[1]*40, P};
        } else if (gam2[0] == 2) {
            return vector<int>{mod4(3 + 2 * (omega2 + s1)), gamma_slt[2] + gam2[1]*40, gamma_slt[0] + gam1[1]*40, P};
        } else if (gam2[0] == 3) {
            return vector<int>{mod4(3 + 2 * omega2), gamma_slt[0] + gam1[1]*40, gamma_slt[3] + gam2[1]*40, P};
        } else if (gam2[0] == 4) {
            return vector<int>{mod4(3 + 2 * (omega2 + s1)), gamma_slt[4] + gam2[1]*40, gamma_slt[0] + gam1[1]*40, P};
        }
    } else if (gam1[0] == 1) {
        if (gam2[0] == 0) {
            return vector<int>{mod4(3 + 2 * omega2), gamma_slt[0] + gam2[1]*40, gamma_slt[1] + gam1[1]*40, P};
        } else if (gam2[0] == 2) {
            return vector<int>{3, gamma_slt[2] + gam2[1]*40, gamma_slt[1] + gam1[1]*40, P};
        } else if (gam2[0] == 3) {
            return vector<int>{mod4(3 + 2 * s1), gamma_slt[3] + gam2[1]*40, gamma_slt[1] + gam1[1]*40, P};
        } else if (gam2[0] == 4) {
            return vector<int>{3, gamma_slt[4] + gam2[1]*40, gamma_slt[1] + gam1[1]*40, P};
        }
    } else if (gam1[0] == 2) {
        if (gam2[0] == 0) {
            return vector<int>{mod4(3 + 2 * (omega2 + s1)), gamma_slt[2] + gam1[1]*40, gamma_slt[0] + gam2[1]*40, P};
        } else if (gam2[0] == 1) {
            return vector<int>{3, gamma_slt[2] + gam1[1]*40, gamma_slt[1] + gam2[1]*40, P};
        } else if (gam2[0] == 3) {
            return vector<int>{3, gamma_slt[2] + gam1[1]*40, gamma_slt[3] + gam2[1]*40, P};
        } else if (gam2[0] == 4) {
            return vector<int>{mod4(3 + 2 * s1), gamma_slt[4] + gam2[1]*40, gamma_slt[2] + gam1[1]*40, P};
        }
    } else if (gam1[0] == 3) {
        if (gam2[0] == 0) {
            return vector<int>{mod4(3 + 2 * omega2), gamma_slt[0] + gam2[1]*40, gamma_slt[3] + gam1[1]*40, P};
        } else if (gam2[0] == 1) {
            return vector<int>{mod4(3 + 2 * s1), gamma_slt[3] + gam1[1]*40, gamma_slt[1] + gam2[1]*40, P};
        } else if (gam2[0] == 2) {
            return vector<int>{3, gamma_slt[2] + gam2[1]*40, gamma_slt[3] + gam1[1]*40, P};
        } else if (gam2[0] == 4) {
            return vector<int>{3, gamma_slt[4] + gam2[1]*40, gamma_slt[3] + gam1[1]*40, P};
        }
    } else if (gam1[0] == 4) {
        if (gam2[0] == 0) {
            return vector<int>{mod4(3 + 2 * (omega2 + s1)), gamma_slt[4] + gam1[1]*40, gamma_slt[0] + gam2[1]*40, P};
        } else if (gam2[0] == 1) {
            return vector<int>{3, gamma_slt[4] + gam1[1]*40, gamma_slt[1] + gam2[1]*40, P};
        } else if (gam2[0] == 2) {
            return vector<int>{mod4(3 + 2 * s1), gamma_slt[4] + gam1[1]*40, gamma_slt[2] + gam2[1]*40, P};
        } else if (gam2[0] == 3) {
            return vector<int>{3, gamma_slt[4] + gam1[1]*40, gamma_slt[3] + gam2[1]*40, P};
        }
    }
    throw std::logic_error("one_dimer: unexpected Majorana pair");
}


inline vector<vector<int>> two_dimer(vector<int> &top, vector<int> &down) {
    //top = {gamma_index top}, down = {gamma_index down}
    int posi[4];
    int layer[4];

    for (int i = 0; i < (int)size(top); i++) {
        posi[i] = top[i];
        layer[i] = 0;
    }
    for (int i = 0; i < (int)size(down); i++) {
        posi[i + size(top)] = down[i];
        layer[i + size(top)] = 1;
    }

    //bubble sort, loop to access each array element
    for (int step = 0; step < 4 -1; step++) {
        // loop to compare array elements
        for (int i = 0; i < 4 - step - 1; i++) {
            // compare two adjacent elements
            // change > to < to sort in descending order
            if (posi[i] > posi[i + 1]) {
                // swapping elements if elements
                // are not in the intended order
                int temp = posi[i];
                posi[i] = posi[i + 1];
                posi[i + 1] = temp;
                temp = layer[i];
                layer[i] = layer[i + 1];
                layer[i + 1] = temp;
            }
        }
    }

    vector<vector<int>> dimers;
    //if top and down are 3-1 or 1-3, put the clined bridge pair in the firt dimer
    if (layer[0] == layer[2]) {
        //first dimer
        dimers.push_back({posi[1],layer[1]});
        dimers.push_back({posi[3],layer[3]});
        //second dimer
        dimers.push_back({posi[0],layer[0]});
        dimers.push_back({posi[2],layer[2]});
    } else {
        //first dimer
        dimers.push_back({posi[0],layer[0]});
        dimers.push_back({posi[2],layer[2]});
        //second dimer
        dimers.push_back({posi[1],layer[1]});
        dimers.push_back({posi[3],layer[3]});
    }
    return dimers;

}


inline pair <vector<vector<int>>, vector<vector<int>>>
bridge_pairs_4simplex(const int n3_slt[5], const int n3p_slt[5], int gamma_slt[5], int gammap_slt[5], int omega2_slt, int s1_slt[2],
                          int P_slt[2]){
    vector<vector<int>> bridge_pair_set0;
    vector<vector<int>> bridge_pair_set1;
    //(1234 ,0234, 0134, 0124, 0123)
    vector<int> top = {};
    vector<int> down = {};
    vector<int> top_dang = {};
    vector<int> down_dang = {};
    for (int i = 0; i < 5; i++) {
        if (n3_slt[i] == 1) {
            top.push_back(i);
            if (n3p_slt[i] == 0) {
                top_dang.push_back(i);
            }
        }
        if (n3p_slt[i] == 1) {
            down.push_back(i);
            if (n3_slt[i] == 0) {
                down_dang.push_back(i);
            }
        }
    }

    if (n3_slt[0]*n3p_slt[0] == 1) {
        bridge_pair_set0.push_back(vector<int>{mod4(3 + 2 * s1_slt[1]), gammap_slt[0], gamma_slt[0], P_slt[0]});
    }
    if (n3_slt[1]*n3p_slt[1] == 1) {
        bridge_pair_set0.push_back(vector<int>{mod4(3 + 2 * s1_slt[0]), gamma_slt[1], gammap_slt[1], P_slt[0]});
    }
    if (n3_slt[2]*n3p_slt[2] == 1) {
        bridge_pair_set0.push_back(vector<int>{mod4(3 + 2 * s1_slt[0]), gammap_slt[2], gamma_slt[2], P_slt[0]});
    }
    if (n3_slt[3]*n3p_slt[3] == 1) {
        bridge_pair_set0.push_back(vector<int>{mod4(3 + 2 * s1_slt[0]), gamma_slt[3], gammap_slt[3], P_slt[0]});
    }
    if (n3_slt[4]*n3p_slt[4] == 1) {
        bridge_pair_set0.push_back(vector<int>{mod4(3 + 2 * s1_slt[0]), gammap_slt[4], gamma_slt[4], P_slt[0]});
    }

    if (size(top_dang) == 0) {
        if (size(down_dang) == 2) {
            int gam0[2] = {down_dang[0], 1};
            int gam1[2] = {down_dang[1], 1};
            int gam2[2] = {down_dang[0], 0};
            bridge_pair_set0.push_back(one_dimer(gam0, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
            bridge_pair_set1.push_back(one_dimer(gam2, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[1]));
        } else if (size(down_dang) == 4) {
            auto gams = two_dimer(top_dang, down_dang);
            int gam0[2] = {gams[0][0], 0};
            int gam1[2] =  {gams[1][0], 1};
            int gam2[2] = {gams[2][0], 0};
            int gam3[2] =  {gams[3][0], 1};
            bridge_pair_set1.push_back(one_dimer(gam0, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[1]));
            bridge_pair_set1.push_back(one_dimer(gam2, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[1]));
        }
    } else if (size(top_dang) == 1) {
        if (size(down_dang) == 1) {
            int gam0[2] = {top_dang[0], 0};
            int gam1[2] = {down_dang[0], 1};
            bridge_pair_set0.push_back(one_dimer(gam0, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
        } else if (size(down_dang) == 3) {
            auto gams = two_dimer(top_dang, down_dang);
            int gam0[2] = {gams[0][0], gams[0][1]};
            int gam1[2] =  {gams[1][0], gams[1][1]};
            int gam2[2] = {gams[2][0], gams[2][1]};
            int gam3[2] =  {gams[3][0], gams[2][1]};
            int gam4[2] = {gams[2][0], 0};
            bridge_pair_set0.push_back(one_dimer(gam0, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
            bridge_pair_set0.push_back(one_dimer(gam2, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
            bridge_pair_set1.push_back(one_dimer(gam4, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[1]));
        } else {
            throw std::logic_error("error3: unexpected Majorana configuration");
        }
    } else if (size(top_dang) == 2) {
        if (size(down_dang) == 2) {
            auto gams = two_dimer(top_dang, down_dang);
            //judge whether two dimers are in-plane or inclined bridge pair
            if (gams[0][1] == gams[1][1]) {
                //in-plane, keep the top layer to be the first dimer
                if (gams[0][1] == 0) {
                    int gam2[2] = {gams[2][0], gams[2][1]};
                    int gam3[2] =  {gams[3][0], gams[2][1]};
                    int gam4[2] = {gams[2][0], 0};
                    bridge_pair_set0.push_back(one_dimer(gam2, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
                    bridge_pair_set1.push_back(one_dimer(gam4, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[1]));
                } else {
                    int gam2[2] = {gams[0][0], gams[0][1]};
                    int gam3[2] =  {gams[1][0], gams[1][1]};
                    int gam4[2] = {gams[0][0], 0};
                    bridge_pair_set0.push_back(one_dimer(gam2, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
                    bridge_pair_set1.push_back(one_dimer(gam4, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[1]));
                }
            } else {
                //inclined bridge pairs
                int gam0[2] = {gams[0][0], gams[0][1]};
                int gam1[2] =  {gams[1][0], gams[1][1]};
                int gam2[2] = {gams[2][0], gams[2][1]};
                int gam3[2] =  {gams[3][0], gams[3][1]};
                bridge_pair_set0.push_back(one_dimer(gam0, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
                bridge_pair_set0.push_back(one_dimer(gam2, gam3, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
            }
        }
    } else if (size(top_dang) == 3) {
        if (size(down_dang) == 1) {
            auto gams = two_dimer(top_dang, down_dang);
            int gam0[2] = {gams[0][0], gams[0][1]};
            int gam1[2] =  {gams[1][0], gams[1][1]};
            bridge_pair_set0.push_back(one_dimer(gam0, gam1, gamma_slt, omega2_slt, s1_slt[0], P_slt[0]));
        } else {
            throw std::logic_error("error5: unexpected Majorana configuration");
        }
    }

    return make_pair(bridge_pair_set0,bridge_pair_set1);
}



pair <vector<vector<int>>, vector<vector<int>>> all_pairs_Pmove_0_1() {
    //Get all the nontrivial bridge Majorana pairs in a specific step
    //P0 and P1, here we only include nontrivial pairs
    vector<vector<int>> bridge_pair_set_0;
    vector<vector<int>> bridge_pair_set_1;
    //4simplex_01234
    int n3_slt_0[5] = {n3[10], n3[6], n3[3], n3[1], n3[0]};
    int n3p_slt_0[5] = {n3p[10], n3p[6], n3p[3], n3p[1], n3p[0]};
    int gamma_slt_0[5] = {gamma_B[10], gamma_A[6], gamma_B[3], gamma_A[1], gamma_B[0]};
    int gammap_slt_0[5] = {gamma_Bp[10], gamma_Ap[6], gamma_Bp[3], gamma_Ap[1], gamma_Bp[0]};
    int s1_slt_0[2] = {0, s1[0]};
    int P_slt[2] = {1, 0};
    auto Pair_0 = bridge_pairs_4simplex(n3_slt_0, n3p_slt_0, gamma_slt_0, gammap_slt_0, 0, s1_slt_0, P_slt);
    auto bridge_pair_set_0_0 = Pair_0.second;
    auto bridge_pair_set_1_0 = Pair_0.first;
    //4simplex_01245
    int n3_slt_1[5] = {n3[12], n3[8], n3[5], n3[2], n3[1]};
    int n3p_slt_1[5] = {n3p[12], n3p[8], n3p[5], n3p[2], n3p[1]};
    int gamma_slt_1[5] = {gamma_B[12], gamma_A[8], gamma_B[5], gamma_A[2], gamma_B[1]};
    int gammap_slt_1[5] = {gamma_Bp[12], gamma_Ap[8], gamma_Bp[5], gamma_Ap[2], gamma_Bp[1]};
    int s1_slt_1[2] = {0, s1[0]};
    auto Pair_1 = bridge_pairs_4simplex(n3_slt_1, n3p_slt_1, gamma_slt_1, gammap_slt_1, 0, s1_slt_1, P_slt);
    auto bridge_pair_set_0_1 = Pair_1.second;
    auto bridge_pair_set_1_1 = Pair_1.first;
    //4simplex_02345
    int n3_slt_2[5] = {n3[14], n3[9], n3[8], n3[7], n3[6]};
    int n3p_slt_2[5] = {n3p[14], n3p[9], n3p[8], n3p[7], n3p[6]};
    int gamma_slt_2[5] = {gamma_B[14], gamma_A[9], gamma_B[8], gamma_A[7], gamma_B[6]};
    int gammap_slt_2[5] = {gamma_Bp[14], gamma_Ap[9], gamma_Bp[8], gamma_Ap[7], gamma_Bp[6]};
    int s1_slt_2[2] = {0, s1[1]};
    auto Pair_2 = bridge_pairs_4simplex(n3_slt_2, n3p_slt_2, gamma_slt_2, gammap_slt_2, 0, s1_slt_2, P_slt);
    auto bridge_pair_set_0_2 = Pair_2.second;
    auto bridge_pair_set_1_2 = Pair_2.first;

    bridge_pair_set_0.insert(bridge_pair_set_0.end(), bridge_pair_set_0_0.begin(), bridge_pair_set_0_0.end());
    bridge_pair_set_0.insert(bridge_pair_set_0.end(), bridge_pair_set_0_1.begin(), bridge_pair_set_0_1.end());
    bridge_pair_set_0.insert(bridge_pair_set_0.end(), bridge_pair_set_0_2.begin(), bridge_pair_set_0_2.end());
    bridge_pair_set_1.insert(bridge_pair_set_1.end(), bridge_pair_set_1_0.begin(), bridge_pair_set_1_0.end());
    bridge_pair_set_1.insert(bridge_pair_set_1.end(), bridge_pair_set_1_1.begin(), bridge_pair_set_1_1.end());
    bridge_pair_set_1.insert(bridge_pair_set_1.end(), bridge_pair_set_1_2.begin(), bridge_pair_set_1_2.end());

    return make_pair(bridge_pair_set_0, bridge_pair_set_1);
}

vector<vector<int>> all_pairs_Fmove_2() {
    //Get all the (tirvial and nontrivial) Majorana pairs in a specific step
    //P2
    vector<vector<int>> all_pair_set;
    //4simplex_01234
    int n3_selected_0[5] = {n3[10], n3[6], n3[3], n3[1], n3[0]};
    int gamma_selected_0[5] = {gamma_B[10], gamma_A[6], gamma_B[3], gamma_A[1], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 2);
    int n3p_selected_0[5] = {n3p[10], n3p[6], n3p[3], n3p[1], n3p[0]};
    int gammap_selected_0[5] = {gamma_Bp[10], gamma_Ap[6], gamma_Bp[3], gamma_Ap[1], gamma_Bp[0]};
    vector<vector<int>> nontrivial_pair_set_0p = nontrivial_pairs_4simplex(n3p_selected_0, gammap_selected_0, 0, 0, 2);
    //4simplex_01245
    int n3_selected_1[5] = {n3[12], n3[8], n3[5], n3[2], n3[1]};
    int gamma_selected_1[5] = {gamma_B[12], gamma_A[8], gamma_B[5], gamma_A[2], gamma_B[1]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 2);
    int n3p_selected_1[5] = {n3p[12], n3p[8], n3p[5], n3p[2], n3p[1]};
    int gammap_selected_1[5] = {gamma_Bp[12], gamma_Ap[8], gamma_Bp[5], gamma_Ap[2], gamma_Bp[1]};
    vector<vector<int>> nontrivial_pair_set_1p = nontrivial_pairs_4simplex(n3p_selected_1, gammap_selected_1, 0, 0, 2);
    //4simplex_02345
    int n3_selected_2[5] = {n3[14], n3[9], n3[8], n3[7], n3[6]};
    int gamma_selected_2[5] = {gamma_B[14], gamma_A[9], gamma_B[8], gamma_A[7], gamma_B[6]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, 0, 0, 2);
    int n3p_selected_2[5] = {n3p[14], n3p[9], n3p[8], n3p[7], n3p[6]};
    int gammap_selected_2[5] = {gamma_Bp[14], gamma_Ap[9], gamma_Bp[8], gamma_Ap[7], gamma_Bp[6]};
    vector<vector<int>> nontrivial_pair_set_2p = nontrivial_pairs_4simplex(n3p_selected_2, gammap_selected_2, 0, 0, 2);

    vector<int> n3_selected_3 = {n3[1], n3[6], n3[8], n3p[1], n3p[6], n3p[8]};
    vector<int> gamma_selected_3 = {gamma_A[1], gamma_A[6], gamma_A[8], gamma_Ap[1], gamma_Ap[6], gamma_Ap[8]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_Fmove_2layers(n3_selected_3, gamma_selected_3, 2);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0p.begin(), nontrivial_pair_set_0p.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1p.begin(), nontrivial_pair_set_1p.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2p.begin(), nontrivial_pair_set_2p.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

vector<vector<int>> all_pairs_Fmove_3() {
    //Get all the (tirvial and nontrivial) Majorana pairs in a specific step
    //P3
    vector<vector<int>> all_pair_set;
    //4simplex_01235
    int n3_selected_0[5] = {n3[11], n3[7], n3[4], n3[2], n3[0]};
    int gamma_selected_0[5] = {gamma_B[11], gamma_A[7], gamma_B[4], gamma_A[2], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(n3_selected_0, gamma_selected_0, 0, 0, 3);
    int n3p_selected_0[5] = {n3p[11], n3p[7], n3p[4], n3p[2], n3p[0]};
    int gammap_selected_0[5] = {gamma_Bp[11], gamma_Ap[7], gamma_Bp[4], gamma_Ap[2], gamma_Bp[0]};
    vector<vector<int>> nontrivial_pair_set_0p = nontrivial_pairs_4simplex(n3p_selected_0, gammap_selected_0, 0, 0, 3);
    //4simplex_01345
    int n3_selected_1[5] = {n3[13], n3[9], n3[5], n3[4], n3[3]};
    int gamma_selected_1[5] = {gamma_B[13], gamma_A[9], gamma_B[5], gamma_A[4], gamma_B[3]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(n3_selected_1, gamma_selected_1, 0, 0, 3);
    int n3p_selected_1[5] = {n3p[13], n3p[9], n3p[5], n3p[4], n3p[3]};
    int gammap_selected_1[5] = {gamma_Bp[13], gamma_Ap[9], gamma_Bp[5], gamma_Ap[4], gamma_Bp[3]};
    vector<vector<int>> nontrivial_pair_set_1p = nontrivial_pairs_4simplex(n3p_selected_1, gammap_selected_1, 0, 0, 3);
    //4simplex_12345, non-standard
    int n3_selected_2[5] = {n3[14], n3[13], n3[12], n3[11], n3[10]};
    int gamma_selected_2[5] = {gamma_B[14], gamma_A[13], gamma_B[12], gamma_A[11], gamma_B[10]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(n3_selected_2, gamma_selected_2, omega2, s1[0], 3);
    int n3p_selected_2[5] = {n3p[14], n3p[13], n3p[12], n3p[11], n3p[10]};
    int gammap_selected_2[5] = {gamma_Bp[14], gamma_Ap[13], gamma_Bp[12], gamma_Ap[11], gamma_Bp[10]};
    vector<vector<int>> nontrivial_pair_set_2p = nontrivial_pairs_4simplex(n3p_selected_2, gammap_selected_2, omega2, s1[0], 3);

    vector<int> n3_selected_3 = {n3[4], n3[11], n3[13], n3p[4], n3p[11], n3p[13]};
    vector<int> gamma_selected_3 = {gamma_A[4], gamma_A[11], gamma_A[13], gamma_Ap[4], gamma_Ap[11], gamma_Ap[13]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_Fmove_2layers(n3_selected_3, gamma_selected_3, 3);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0p.begin(), nontrivial_pair_set_0p.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1p.begin(), nontrivial_pair_set_1p.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2p.begin(), nontrivial_pair_set_2p.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

pair <vector<vector<int>>, vector<vector<int>>> all_pairs_Pmove_4_5() {
    //Get all the nontrivial bridge Majorana pairs in a specific step
    //P4 and P5, here we only include nontrivial pairs
    vector<vector<int>> bridge_pair_set_0;
    vector<vector<int>> bridge_pair_set_1;
    //4simplex_01235
    int n3_slt_0[5] = {n3[11], n3[7], n3[4], n3[2], n3[0]};
    int n3p_slt_0[5] = {n3p[11], n3p[7], n3p[4], n3p[2], n3p[0]};
    int gamma_slt_0[5] = {gamma_B[11], gamma_A[7], gamma_B[4], gamma_A[2], gamma_B[0]};
    int gammap_slt_0[5] = {gamma_Bp[11], gamma_Ap[7], gamma_Bp[4], gamma_Ap[2], gamma_Bp[0]};
    int s1_slt_0[2] = {0, s1[0]};
    int P_slt[2] = {4, 5};
    auto Pair_0 = bridge_pairs_4simplex(n3_slt_0, n3p_slt_0, gamma_slt_0, gammap_slt_0, 0, s1_slt_0, P_slt);
    auto bridge_pair_set_0_0 = Pair_0.second;
    auto bridge_pair_set_1_0 = Pair_0.first;
    //4simplex_01345
    int n3_slt_1[5] = {n3[13], n3[9], n3[5], n3[4], n3[3]};
    int n3p_slt_1[5] = {n3p[13], n3p[9], n3p[5], n3p[4], n3p[3]};
    int gamma_slt_1[5] = {gamma_B[13], gamma_A[9], gamma_B[5], gamma_A[4], gamma_B[3]};
    int gammap_slt_1[5] = {gamma_Bp[13], gamma_Ap[9], gamma_Bp[5], gamma_Ap[4], gamma_Bp[3]};
    int s1_slt_1[2] = {0, s1[0]};
    auto Pair_1 = bridge_pairs_4simplex(n3_slt_1, n3p_slt_1, gamma_slt_1, gammap_slt_1, 0, s1_slt_1, P_slt);
    auto bridge_pair_set_0_1 = Pair_1.second;
    auto bridge_pair_set_1_1 = Pair_1.first;
    //4simplex_12345, non-standard
    int n3_slt_2[5] = {n3[14], n3[13], n3[12], n3[11], n3[10]};
    int n3p_slt_2[5] = {n3p[14], n3p[13], n3p[12], n3p[11], n3p[10]};
    int gamma_slt_2[5] = {gamma_B[14], gamma_A[13], gamma_B[12], gamma_A[11], gamma_B[10]};
    int gammap_slt_2[5] = {gamma_Bp[14], gamma_Ap[13], gamma_Bp[12], gamma_Ap[11], gamma_Bp[10]};
    int s1_slt_2[2] = {s1[0], s1[1]};
    auto Pair_2 = bridge_pairs_4simplex(n3_slt_2, n3p_slt_2, gamma_slt_2, gammap_slt_2, omega2, s1_slt_2, P_slt);
    auto bridge_pair_set_0_2 = Pair_2.second;
    auto bridge_pair_set_1_2 = Pair_2.first;

    bridge_pair_set_0.insert(bridge_pair_set_0.end(), bridge_pair_set_0_0.begin(), bridge_pair_set_0_0.end());
    bridge_pair_set_0.insert(bridge_pair_set_0.end(), bridge_pair_set_0_1.begin(), bridge_pair_set_0_1.end());
    bridge_pair_set_0.insert(bridge_pair_set_0.end(), bridge_pair_set_0_2.begin(), bridge_pair_set_0_2.end());
    bridge_pair_set_1.insert(bridge_pair_set_1.end(), bridge_pair_set_1_0.begin(), bridge_pair_set_1_0.end());
    bridge_pair_set_1.insert(bridge_pair_set_1.end(), bridge_pair_set_1_1.begin(), bridge_pair_set_1_1.end());
    bridge_pair_set_1.insert(bridge_pair_set_1.end(), bridge_pair_set_1_2.begin(), bridge_pair_set_1_2.end());

    return make_pair(bridge_pair_set_0, bridge_pair_set_1);
}

vector<vector<int>> all_pairs_Fmove_6() {
    //Get all the (tirvial and nontrivial) Majorana pairs in a specific step
    //P6
    vector<vector<int>> all_pair_set;
    //4simplex_01235
    int N3_selected_0[5] = {N3[11], N3[7], N3[4], N3[2], N3[0]};
    int gamma_selected_0[5] = {gamma_B[11], gamma_A[7], gamma_B[4], gamma_A[2], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(N3_selected_0, gamma_selected_0, 0, 0, 6);
    //4simplex_01345
    int N3_selected_1[5] = {N3[13], N3[9], N3[5], N3[4], N3[3]};
    int gamma_selected_1[5] = {gamma_B[13], gamma_A[9], gamma_B[5], gamma_A[4], gamma_B[3]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(N3_selected_1, gamma_selected_1, 0, 0, 6);
    //4simplex_12345, non-standard
    int N3_selected_2[5] = {N3[14], N3[13], N3[12], N3[11], N3[10]};
    int gamma_selected_2[5] = {gamma_B[14], gamma_A[13], gamma_B[12], gamma_A[11], gamma_B[10]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(N3_selected_2, gamma_selected_2, omega2, s1[0], 6);

    vector<int> N3_selected_3 = {N3[4], N3[11], N3[13]};
    vector<int> gamma_selected_3 = {gamma_A[4], gamma_A[11], gamma_A[13]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_Fmove_2layers(N3_selected_3, gamma_selected_3, 6);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

vector<vector<int>> all_pairs_Fmove_7() {
    //Get all the (tirvial and nontrivial) Majorana pairs in a specific step
    //P7
    vector<vector<int>> all_pair_set;
    //4simplex_01234
    int N3_selected_0[5] = {N3[10], N3[6], N3[3], N3[1], N3[0]};
    int gamma_selected_0[5] = {gamma_B[10], gamma_A[6], gamma_B[3], gamma_A[1], gamma_B[0]};
    vector<vector<int>> nontrivial_pair_set_0 = nontrivial_pairs_4simplex(N3_selected_0, gamma_selected_0, 0, 0, 7);
    //4simplex_01245
    int N3_selected_1[5] = {N3[12], N3[8], N3[5], N3[2], N3[1]};
    int gamma_selected_1[5] = {gamma_B[12], gamma_A[8], gamma_B[5], gamma_A[2], gamma_B[1]};
    vector<vector<int>> nontrivial_pair_set_1 = nontrivial_pairs_4simplex(N3_selected_1, gamma_selected_1, 0, 0, 7);
    //4simplex_02345
    int N3_selected_2[5] = {N3[14], N3[9], N3[8], N3[7], N3[6]};
    int gamma_selected_2[5] = {gamma_B[14], gamma_A[9], gamma_B[8], gamma_A[7], gamma_B[6]};
    vector<vector<int>> nontrivial_pair_set_2 = nontrivial_pairs_4simplex(N3_selected_2, gamma_selected_2, 0, 0, 7);

    vector<int> n3_selected_3 = {N3[1], N3[6], N3[8]};
    vector<int> gamma_selected_3 = {gamma_A[1], gamma_A[6], gamma_A[8]};
    vector<vector<int>> trivial_pair_set = trivial_pairs_Fmove_2layers(n3_selected_3, gamma_selected_3, 7);

    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_0.begin(), nontrivial_pair_set_0.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_1.begin(), nontrivial_pair_set_1.end());
    all_pair_set.insert(all_pair_set.end(), nontrivial_pair_set_2.begin(), nontrivial_pair_set_2.end());
    all_pair_set.insert(all_pair_set.end(), trivial_pair_set.begin(), trivial_pair_set.end());
    return all_pair_set;
}

}  // namespace stacking
