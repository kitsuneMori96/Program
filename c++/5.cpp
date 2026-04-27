#include <stdio.h>
#include <math.h>
#define size 4
#define ass 1e-12
int gauss(int n, double a[][size+2], double x[]) {
    int i, j, k, p;
    double m, temp, maxp;
    
    for (k = 1; k <= n - 1; k++) {
        maxp = 0.0;
        p = k;
        
        for (i = k; i <= n; i++) {
            if (fabs(a[i][k]) > maxp) {
                maxp = fabs(a[i][k]);
                p = i;
            }
        }
        
        if (fabs(maxp) < ass) {
            return 0;
        }
        
        if (p != k) {
            for (j = k; j <= n + 1; j++) {
                temp = a[k][j];
                a[k][j] = a[p][j];
                a[p][j] = temp;
            }
        }
        
        for (i = k + 1; i <= n; i++) {
            m = a[i][k] / a[k][k];
            for (j = k + 1; j <= n + 1; j++) {
                a[i][j] -= m * a[k][j];
            }
        }
    }
    
    if (fabs(a[n][n]) < ass) {
        return 0;
    }
    
    x[n] = a[n][n+1] / a[n][n];
    for (i = n - 1; i >= 1; i--) {
        temp = 0.0;
        for (j = i + 1; j <= n; j++) {
            temp += a[i][j] * x[j];
        }
        x[i] = (a[i][n+1] - temp) / a[i][i];
    }
    
    return 1;
}
int main() {
    int i, n, det;
    double a[size+1][size+2], x[size+1];
    
    printf("please input n：\n");
    scanf("%d", &n);
    if (n > size) {
        printf("n exceeds maximum dimension %d\n", size);
        return 1;
    }
    
    printf("please input A|b：\n");
    for (i = 1; i <= n; i++) {
        for (int j = 1; j <= n + 1; j++) {
            scanf("%lf", &a[i][j]);
        }
    }
    
    det = gauss(n, a, x);
    if (det != 0) {
        for (i = 1; i <= n; i++) {
            printf("x%d = %.6g\n", i, x[i]);
        }
    } else {
        printf("Matrix is singular or ill-conditioned.\n");
    }
    
    return 0;
}
