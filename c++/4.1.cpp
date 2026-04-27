#include <bits/stdc++.h>
using namespace std;
void columnMain(double A[4][4], double b[4], double x[4]) {
    double a[4][5];
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) a[i][j] = A[i][j];
        a[i][4] = b[i];
    }
    
    for (int k = 0; k < 3; k++) {
        int m = k;
        for (int i = k + 1; i < 4; i++) {
            if (fabs(a[i][k]) > fabs(a[m][k])) m = i;
        }
        if (m != k) {
            for (int j = k; j <= 4; j++) {
                double t = a[k][j];
                a[k][j] = a[m][j];
                a[m][j] = t;
            }
        }
        
        for (int i = k + 1; i < 4; i++) {
            double f = a[i][k] / a[k][k];
            for (int j = k; j <= 4; j++) a[i][j] -= f * a[k][j];
        }
    }
    
    for (int i = 3; i >= 0; i--) {
        x[i] = a[i][4];
        for (int j = i + 1; j < 4; j++) x[i] -= a[i][j] * x[j];
        x[i] /= a[i][i];
    }
}

void noMain(double A[4][4], double b[4], double x[4]) {
    double a[4][5];
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) a[i][j] = A[i][j];
        a[i][4] = b[i];
    }
    
    for (int k = 0; k < 3; k++) {
        for (int i = k + 1; i < 4; i++) {
            double f = a[i][k] / a[k][k];
            for (int j = k; j <= 4; j++) a[i][j] -= f * a[k][j];
        }
    }
    
    for (int i = 3; i >= 0; i--) {
        x[i] = a[i][4];
        for (int j = i + 1; j < 4; j++) x[i] -= a[i][j] * x[j];
        x[i] /= a[i][i];
    }
}

int main() {
    double A[4][4] = {
        {0.3e-15, 59.14, 3, 1},
        {5.291, -6.130, -1, 2},
        {11.2, 9, 5, 2},
        {1, 2, 1, 1}
    };
    double b[4] = {59.17, 46.78, 1, 2};
    double x1[4], x2[4];
    
    noMain(A, b, x1);
    columnMain(A, b, x2);
    
    cout<<"不选主元：" << endl;
    for (int i = 0; i < 4; i++) cout << "x" << i+1 << " = " << x1[i] << endl;
    
    cout<< "\n列主元：" << endl;
    for (int i = 0; i < 4; i++) cout << "x" << i+1 << " = " << x2[i] << endl;
    
    return 0;
}