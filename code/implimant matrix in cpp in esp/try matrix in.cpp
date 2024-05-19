/*

#include <iostream>
#include <cmath>

int main() {
    double i1[3] = {1, 2, 3};
    double i2[3] = {3, 2, 1};
    double i3[3] = {1, 2, 3};
    double i4[3] = {3, 2, 1};
    double i5[3] = {1, 42, 3};
    double i6[3] = {3, 2, 1};

    double b1[3] = {1, 2, 3};
    double b2[3] = {3, 2, 1};
    double b3[3] = {1, 2, 3};
    double b4[3] = {3, 2, 1};
    double b5[3] = {1, 99, 3};
    double b6[3] = {3, 2, 8};


    double f1 = 546;
    double f2 = 2;
    double f3 = 2;
    double f4 = 42;
    double f5 = 76;
    double f6 = 675;

    double F[6] = {f1, f2, f3, f4, f5, f6};

    double T[6][6] = {0};
    for (int i = 0; i < 6; ++i) {
        T[i][0] = i1[0] * b1[0] - i1[i] * b1[i];
        T[i][1] = i1[1] * b1[0] - i1[i] * b1[i];
        T[i][2] = i1[2] * b1[0] - i1[i] * b1[i];
        T[i][3] = i1[0] * b1[1] - i1[i] * b1[i];
        T[i][4] = i1[1] * b1[1] - i1[i] * b1[i];
        T[i][5] = i1[2] * b1[1] - i1[i] * b1[i];
    }

    double result[6] = {0};
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            result[i] += F[j] * T[j][i];
        }
    }

    std::cout << "Result: " << result[0] << ", " << result[1] << ", " << result[2] << ", " << result[3] << ", " << result[4] << ", " << result[5] << std::endl;

    return 0;
};

*/