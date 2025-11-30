#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

vector<int> add(vector<int>& a, vector<int>& b){
    int carry=0;
    int maxin=max(a.size(),b.size());
    vector<int> res(maxin,0);
    for(int i=0;i<maxin;i++){
        int x=i<a.size()?a[i]:0;
        int y=i<b.size()?b[i]:0;
        res[i]=x+y+carry;
        carry=res[i]/10;
        res[i]%=10;
    }
    if(carry) res.push_back(carry);
    return res;
}

int main(){
    int n;
    cin>>n;
    vector<int> a1,a2,a3;
    a1.push_back(1);
    a2.push_back(2);
    if(n<=2){
        cout<<n<<endl;
        return 0;
    }
    for(int i=3;i<=n;i++){
        a3=add(a1,a2);
        a1=a2;
        a2=a3;
    }
    for(auto it=a3.rbegin();it!=a3.rend();it++){
        cout<<*it;
    }
    return 0;
}