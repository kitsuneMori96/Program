#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define EPS 5e-8  // 绝对误差要求 1/2 × 10^{-7}
#define MAX_ITER 30  // 最大迭代次数，防止无限循环

// 积分1的被积函数: ∫ from 2 to 3 of 1/(x^2-1) dx
double f1(double x) {
    return 1.0 / (x * x - 1.0);
}

// 积分2的被积函数: ∫ from 1 to 2 of x * e^x dx
double f2(double x) {
    return x * exp(x);
}

// 复合梯形公式
double composite_trapezoidal(double (*f)(double), double a, double b, int n) {
    double h = (b - a) / n;
    double sum = 0.5 * (f(a) + f(b));
    for (int i = 1; i < n; i++) {
        sum += f(a + i * h);
    }
    return sum * h;
}

// 复合Simpson公式，n需为偶数
double composite_simpson(double (*f)(double), double a, double b, int n) {
    if (n % 2 != 0) n++;  // 确保n为偶数
    double h = (b - a) / n;
    double sum = f(a) + f(b);
    for (int i = 1; i < n; i++) {
        if (i % 2 == 0) {
            sum += 2 * f(a + i * h);
        } else {
            sum += 4 * f(a + i * h);
        }
    }
    return sum * h / 3.0;
}

// 龙贝格公式，通过外推加速收敛
double romberg(double (*f)(double), double a, double b, double eps, int *iter_used) {
    double R[MAX_ITER][MAX_ITER];  // 龙贝格表，假设最大迭代为MAX_ITER
    double h = b - a;
    R[0][0] = 0.5 * h * (f(a) + f(b));
    *iter_used = 0;

    for (int i = 1; i < MAX_ITER; i++) {
        h /= 2.0;
        double sum = 0.0;
        for (int k = 1; k <= (1 << (i-1)); k++) {  // 2^{i-1}个点
            sum += f(a + (2*k - 1) * h);
        }
        R[i][0] = 0.5 * R[i-1][0] + h * sum;
        for (int j = 1; j <= i; j++) {
            R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1]) / (pow(4, j) - 1);
        }
        *iter_used = i;
        // 检查对角线元素的差值是否小于eps
        if (i > 0 && fabs(R[i][i] - R[i-1][i-1]) < eps) {
            return R[i][i];
        }
    }
    return R[MAX_ITER-1][MAX_ITER-1];  // 返回最后一次迭代值
}

// 自适应复合梯形公式，迭代直到误差小于eps
double trapezoidal_adaptive(double (*f)(double), double a, double b, double eps, double exact, int *n_used) {
    int n = 1;
    double integral, error;
    do {
        integral = composite_trapezoidal(f, a, b, n);
        error = fabs(integral - exact);
        if (error < eps) {
            *n_used = n;
            return integral;
        }
        n *= 2;
        if (n > 1 << 20) {  // 防止n过大，设置上限
            printf("警告：复合梯形公式未在误差范围内收敛。\n");
            *n_used = n;
            return integral;
        }
    } while (1);
}

// 自适应复合Simpson公式，迭代直到误差小于eps
double simpson_adaptive(double (*f)(double), double a, double b, double eps, double exact, int *n_used) {
    int n = 2;  // Simpson要求n为偶数
    double integral, error;
    do {
        integral = composite_simpson(f, a, b, n);
        error = fabs(integral - exact);
        if (error < eps) {
            *n_used = n;
            return integral;
        }
        n *= 2;
        if (n > 1 << 20) {
            printf("警告：复合Simpson公式未在误差范围内收敛。\n");
            *n_used = n;
            return integral;
        }
    } while (1);
}

int main() {
    // 积分1的参数
    double a1 = 2.0, b1 = 3.0;
    double exact1 = (log(3.0) - log(2.0)) / 2.0;  // 精确解: (ln3 - ln2)/2

    // 积分2的参数
    double a2 = 1.0, b2 = 2.0;
    double exact2 = exp(2.0);  // 精确解: e^2

    printf("积分1: ∫ from %.1f to %.1f of 1/(x^2-1) dx\n", a1, b1);
    printf("精确解: %.15f\n\n", exact1);

    printf("积分2: ∫ from %.1f to %.1f of x*e^x dx\n", a2, b2);
    printf("精确解: %.15f\n\n", exact2);

    printf("误差要求: 绝对误差 < %.2e\n\n", EPS);

    // 用于存储结果的变量
    double result;
    int n_used, iter_used;
    double error;

    // 积分1的计算
    printf("=== 积分1计算 ===\n");
    // 复合梯形公式
    result = trapezoidal_adaptive(f1, a1, b1, EPS, exact1, &n_used);
    error = fabs(result - exact1);
    printf("复合梯形公式: 数值解 = %.15f, 区间数 = %d, 绝对误差 = %.2e\n", result, n_used, error);

    // 复合Simpson公式
    result = simpson_adaptive(f1, a1, b1, EPS, exact1, &n_used);
    error = fabs(result - exact1);
    printf("复合Simpson公式: 数值解 = %.15f, 区间数 = %d, 绝对误差 = %.2e\n", result, n_used, error);

    // 龙贝格公式
    result = romberg(f1, a1, b1, EPS, &iter_used);
    error = fabs(result - exact1);
    printf("龙贝格公式: 数值解 = %.15f, 外推迭代次数 = %d, 绝对误差 = %.2e\n\n", result, iter_used, error);

    // 积分2的计算
    printf("=== 积分2计算 ===\n");
    // 复合梯形公式
    result = trapezoidal_adaptive(f2, a2, b2, EPS, exact2, &n_used);
    error = fabs(result - exact2);
    printf("复合梯形公式: 数值解 = %.15f, 区间数 = %d, 绝对误差 = %.2e\n", result, n_used, error);

    // 复合Simpson公式
    result = simpson_adaptive(f2, a2, b2, EPS, exact2, &n_used);
    error = fabs(result - exact2);
    printf("复合Simpson公式: 数值解 = %.15f, 区间数 = %d, 绝对误差 = %.2e\n", result, n_used, error);

    // 龙贝格公式
    result = romberg(f2, a2, b2, EPS, &iter_used);
    error = fabs(result - exact2);
    printf("龙贝格公式: 数值解 = %.15f, 外推迭代次数 = %d, 绝对误差 = %.2e\n\n", result, iter_used, error);

    return 0;
}