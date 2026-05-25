#include <stdio.h>
#include <math.h>

// 函数定义
double f1(double x) { return 5.0 / (1.0 + x*x); }
double f2(double x) { return atan(x); }
double f3(double x) { return x / (1.0 + x*x*x*x); }

// 拉格朗日插值
double lagrange(double x_nodes[], double y_nodes[], int n, double x) {
    double result = 0.0;
    for (int i = 0; i < n; i++) {
        double term = y_nodes[i];
        for (int j = 0; j < n; j++) {
            if (i != j) {
                term *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j]);
            }
        }
        result += term;
    }
    return result;
}

// 牛顿插值
double newton(double x_nodes[], double y_nodes[], int n, double x) {
    double diff_table[11][11];
    for (int i = 0; i < n; i++) {
        diff_table[i][0] = y_nodes[i];
    }
    
    for (int j = 1; j < n; j++) {
        for (int i = 0; i < n - j; i++) {
            diff_table[i][j] = (diff_table[i+1][j-1] - diff_table[i][j-1]) / (x_nodes[i+j] - x_nodes[i]);
        }
    }
    
    double result = diff_table[0][0];
    double product = 1.0;
    for (int k = 1; k < n; k++) {
        product *= (x - x_nodes[k-1]);
        result += diff_table[0][k] * product;
    }
    return result;
}

// 分段线性插值
double piecewise(double x_nodes[], double y_nodes[], int n, double x) {
    for (int i = 0; i < n-1; i++) {
        if (x_nodes[i] <= x && x <= x_nodes[i+1]) {
            double x0 = x_nodes[i], x1 = x_nodes[i+1];
            double y0 = y_nodes[i], y1 = y_nodes[i+1];
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0);
        }
    }
    return 0.0;
}

int main() {
    // 定义节点
    double x_nodes[11];
    double f1_nodes[11], f2_nodes[11], f3_nodes[11];
    
    for (int i = 0; i < 11; i++) {
        x_nodes[i] = -5.0 + i;
        f1_nodes[i] = f1(x_nodes[i]);
        f2_nodes[i] = f2(x_nodes[i]);
        f3_nodes[i] = f3(x_nodes[i]);
    }
    
    // 定义测试点
    double x_test[100];
    for (int i = 0; i < 100; i++) {
        x_test[i] = -5.0 + i * 10.0 / 99.0;
    }
    
    // 定义函数指针数组
    double (*funcs[3])(double) = {f1, f2, f3};
    const char* func_names[3] = {"y=5/(1+x²)", "y=arctanx", "y=x/(1+x⁴)"};
    
    // 定义插值方法名称
    const char* interp_names[3] = {"拉格朗日", "牛顿", "分段线性"};
    
    for (int func_idx = 0; func_idx < 3; func_idx++) {
        printf("\n===== 函数：%s =====\n", func_names[func_idx]);
        
        for (int interp_idx = 0; interp_idx < 3; interp_idx++) {
            printf("\n--- %s 插值 ---\n", interp_names[interp_idx]);
            printf("x\t原函数值\t插值值\t\t误差\n");
            
            double max_error = 0.0;
            
            for (int i = 0; i < 100; i++) {
                double x = x_test[i];
                double true_val = funcs[func_idx](x);
                double interp_val = 0.0;
                
                // 选择插值方法
                if (interp_idx == 0) {
                    interp_val = lagrange(x_nodes, func_idx==0?f1_nodes:(func_idx==1?f2_nodes:f3_nodes), 11, x);
                } else if (interp_idx == 1) {
                    interp_val = newton(x_nodes, func_idx==0?f1_nodes:(func_idx==1?f2_nodes:f3_nodes), 11, x);
                } else {
                    interp_val = piecewise(x_nodes, func_idx==0?f1_nodes:(func_idx==1?f2_nodes:f3_nodes), 11, x);
                }
                
                double error = fabs(true_val - interp_val);
                if (error > max_error) max_error = error;
                
                // 输出前5个和后5个测试点
                if (i < 5 || i >= 95) {
                    printf("%.2f\t%.6f\t%.6f\t%.6f\n", x, true_val, interp_val, error);
                }
                
                // 中间省略
                if (i == 4) printf("...\t...\t...\t...\n");
            }
            
            printf("最大误差：%.6f\n", max_error);
        }
    }
    
    return 0;
}