#include <bits/stdc++.h>
using namespace std;

void jacobi(double A[3][3], double b[3], double x[3], double tol, int maxi) {
    double xNew[3];
    for (int k = 0; k < maxi; k++) {
        for (int i = 0; i < 3; i++) {
            double sum = 0.0;
            for (int j = 0; j < 3; j++) {
                if (i != j) sum += A[i][j] * x[j];
            }
            xNew[i] = (b[i] - sum) / A[i][i];
        }
        double err = 0.0;
        for (int i = 0; i < 3; i++) {
            double diff = fabs(xNew[i] - x[i]);
            if (diff > err) err = diff;
        }
        for (int i = 0; i < 3; i++) x[i] = xNew[i];
        if (err < tol) break;
    }
}

void gauss(double A[3][3], double b[3], double x[3], double tol, int maxi) {
    for (int k = 0; k < maxi; k++) {
        double x_old[3];
        for (int i = 0; i < 3; i++) x_old[i] = x[i];
        
        for (int i = 0; i < 3; i++) {
            double sum = 0.0;
            for (int j = 0; j < 3; j++) {
                if (i != j) sum += A[i][j] * x[j];
            }
            x[i] = (b[i] - sum) / A[i][i];
        }
        
        double err = 0.0;
        for (int i = 0; i < 3; i++) {
            double diff = fabs(x[i] - x_old[i]);
            if (diff > err) err = diff;
        }
        if (err < tol) break;
    }
}

void jacobi2(double A[2][2], double b[2], double x[2], double tol, int max_iter) {
    double x_new[2];
    for (int k = 0; k < max_iter; k++) {
        for (int i = 0; i < 2; i++) {
            double sum = 0.0;
            for (int j = 0; j < 2; j++) {
                if (i != j) sum += A[i][j] * x[j];
            }
            x_new[i] = (b[i] - sum) / A[i][i];
        }
        double err = 0.0;
        for (int i = 0; i < 2; i++) {
            double diff = fabs(x_new[i] - x[i]);
            if (diff > err) err = diff;
        }
        for (int i = 0; i < 2; i++) x[i] = x_new[i];
        if (err < tol) break;
    }
}

void gauss_seidel2(double A[2][2], double b[2], double x[2], double tol, int max_iter) {
    for (int k = 0; k < max_iter; k++) {
        double x_old[2];
        for (int i = 0; i < 2; i++) x_old[i] = x[i];
        
        for (int i = 0; i < 2; i++) {
            double sum = 0.0;
            for (int j = 0; j < 2; j++) {
                if (i != j) sum += A[i][j] * x[j];
            }
            x[i] = (b[i] - sum) / A[i][i];
        }
        
        double err = 0.0;
        for (int i = 0; i < 2; i++) {
            double diff = fabs(x[i] - x_old[i]);
            if (diff > err) err = diff;
        }
        if (err < tol) break;
    }
}

int main() {
    double A1[3][3] = {{6, 2, -1}, {1, 4, -2}, {-3, 1, 4}};
    double b11[3] = {-3, 2, 4};
    double b12[3] = {100, -200, 345};
    double A2[2][2] = {{1, 3}, {-7, 1}};
    double b2[2] = {4, -6};
    
    double tol = 1e-6;
    int max_iter = 1000;
    
    double x0_list[3][3] = {{0, 0, 0}, {1, 1, 1}, {-1, -1, -1}};
    
    cout << "Part (1):\n";
    for (int i = 0; i < 3; i++) {
        double x0[3];
        for (int j = 0; j < 3; j++) x0[j] = x0_list[i][j];
        
        cout << "Initial x0: ";
        for (int j = 0; j < 3; j++) cout << x0[j] << " ";
        cout << endl;
        
        double res_j1[3];
        for (int j = 0; j < 3; j++) res_j1[j] = x0[j];
        jacobi(A1, b11, res_j1, tol, max_iter);
        cout << "Jacobi for b1: ";
        for (int j = 0; j < 3; j++) cout << res_j1[j] << " ";
        cout << endl;
        
        double res_gs1[3];
        for (int j = 0; j < 3; j++) res_gs1[j] = x0[j];
        gauss(A1, b11, res_gs1, tol, max_iter);
        cout << "Gauss-Seidel for b1: ";
        for (int j = 0; j < 3; j++) cout << res_gs1[j] << " ";
        cout << endl;
        
        double res_j2[3];
        for (int j = 0; j < 3; j++) res_j2[j] = x0[j];
        jacobi(A1, b12, res_j2, tol, max_iter);
        cout << "Jacobi for b2: ";
        for (int j = 0; j < 3; j++) cout << res_j2[j] << " ";
        cout << endl;
        
        double res_gs2[3];
        for (int j = 0; j < 3; j++) res_gs2[j] = x0[j];
        gauss(A1, b12, res_gs2, tol, max_iter);
        cout << "Gauss-Seidel for b2: ";
        for (int j = 0; j < 3; j++) cout << res_gs2[j] << " ";
        cout << endl;
    }
    
    double x0_small[2] = {0, 0};
    double res_j_small[2] = {0, 0};
    double res_gs_small[2] = {0, 0};
    for (int i = 0; i < 2; i++) res_j_small[i] = x0_small[i];
    for (int i = 0; i < 2; i++) res_gs_small[i] = x0_small[i];
    
    cout << "\nFor small A:\nJacobi: ";
    jacobi2(A2, b2, res_j_small, tol, max_iter);
    for (int i = 0; i < 2; i++) cout << res_j_small[i] << " ";
    cout << endl;
    
    cout << "Gauss-Seidel: ";
    gauss_seidel2(A2, b2, res_gs_small, tol, max_iter);
    for (int i = 0; i < 2; i++) cout << res_gs_small[i] << " ";
    cout << endl;
    
    cout << "\nPart (2):\n";
    double fixed_x0[3] = {0, 0, 0};
    double fixed_b[3];
    for (int i = 0; i < 3; i++) fixed_b[i] = b11[i];
    
    for (int factor = 1; factor <= 5; factor++) {
        double A_mod[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                A_mod[i][j] = A1[i][j];
            }
        }
        
        for (int i = 0; i < 3; i++) {
            A_mod[i][i] = A1[i][i] * factor;
        }
        
        double res[3];
        for (int i = 0; i < 3; i++) res[i] = fixed_x0[i];
        jacobi(A_mod, fixed_b, res, tol, max_iter);
        cout << "Factor " << factor << ": ";
        for (int i = 0; i < 3; i++) cout << res[i] << " ";
        cout << endl;
    }
    
    return 0;
}