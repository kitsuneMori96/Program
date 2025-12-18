#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const int siz=1e5+15;

int main() {
    long long sum = 0;  
    long long factorial = 1;  
    
    for (int i = 1; i <= 20; i++) {
        factorial *= i;  
        sum += factorial;  
    }
    
    printf("1! + 2! + 3! + ... + 20! = %lld\n", sum);
    
    return 0;
}
