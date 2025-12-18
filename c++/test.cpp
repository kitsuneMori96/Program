#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const int siz=1e5+15;


int main() {    
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= i; j++) {
            printf("%d*%d=%-2d  ", j, i, i * j);
        }
        printf("\n");
    }
    
    return 0;
}
