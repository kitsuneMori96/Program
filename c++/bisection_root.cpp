#include <bits/stdc++.h>
using namespace std;

double f(double x){ return x * x * x - x - 1.0; }

int main() {
    double left = 0.0;
    double right = 1.0;
    double ass = 1e-6;

    if (f(left) * f(right) > 0) {
        cout<<"没有根"<<endl;
        return 0;
    }

    int k = 0;
    double mid = 0.0;

    while ((right - left) / 2.0 > ass) {
        mid = (left + right) / 2.0;
        ++k;

        if (f(mid) == 0.0) break;

        if (f(left) * f(mid) < 0) right = mid;
        else left = mid;
    }

    double x = (left + right) / 2.0;

    cout << "近似根 x = " << x << endl;
    cout << "二分次数 = " << k << endl;

    return 0;
}
