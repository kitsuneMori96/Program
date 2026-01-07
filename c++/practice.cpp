//完美立方数 对于任意给定的正整数 N（N<=100），寻找所有的四元组（a,b,c,d），满足 a3= b3+ c3 + d3
//其中 1 < a,b,c,d <=N
#include <bits/stdc++.h>
using namespace std;
/*
int main() {
    int n, a, b, c, d;
    printf("正整数n:");
    scanf("%d", &n);
    
    if (n <= 100) {
        for (a = 2; a <= n; a++) {
            for (b = 2; b < n; b++) {
                for (c = 2; c < n; c++) {
                    for (d = 2; d < n; d++) {
                        if (a * a * a == b * b * b + c * c * c + d * d * d) {
                            printf("%d %d %d %d\n", a, b, c, d);
                        }
                    }
                }
            }
        }
    } else {
        printf("n超出范围\n");
    }
    
    return 0;
}

/*
int main(){
    std::cout<<"输入";
    int shuzu[10]={0};
    int tonji[10]={0};
    for(int i=0;i<10;i++){
        std::cin>>shuzu[i];
        for(int j=0;j<10;j++){
            if(j==shuzu[i]){
                tonji[j]++;
            } 
        }
    }
    for(int i=0;i<10;i++){
        if(tonji[i]==0){
            continue;
        }
        cout<<"数字"<<i<<"出现了"<<tonji[i]<<"次"<<endl;
    }
    return 0;
}
*/
/*
int main(){
    int a,b;
    std::cout<<"输入";
    int laoshi[21][13]={0};
    for(int i=0;i<1000;i++){
        std::cin>>a>>b;
        laoshi[a][b]++;
    }
    for(int i=1;i<=21;i++){
        for(int j=1;j<=13;j++){
            if(laoshi[i][j]==0){
                continue;
            }
            cout<<"院"<<i<<"系"<<j<<"数量"<<laoshi[i][j]<<endl;
        }
    }
    return 0;
}
*/
//已知一个已经从小到大排序的数组，这个数组的一个平台（Plateau）就是连续的一串值相同的元素，并且这一串元素不能再延伸。
//例如，在 1，2，2，3，3，3，4，5，5，6中1，2-2，3-3-3，4，5-5，6都是平台。
//试编写一个程序，接收一个数组，把这个数组最长的平台找出来。在上面的例子中3-3-3就是最长的平台。
//10
//1 2 2 3 3 3 4 5 5 6
/*
int main(){
    // 定义变量size用于存储数组长度
    int size;
    // 定义变量l和r用于遍历数组
    int l,r;
    // 定义变量len用于存储当前连续相同元素的长度
    int len;
    // 定义变量maxlen用于存储最长连续相同元素的长度
    int maxlen;
start:
    // 提示用户输入数组长度
    cout<<"长度:";
    // 从标准输入读取数组长度并赋值给size
    cin>>size;
    // 定义数组pla长度为size，并初始化为0
    int pla[size]={0};
    // 提示用户输入数组元素
    std::cout<<"输入";
    // 循环读取size个整数并存储到数组pla中
    for(int i=0;i<size;i++){
        std::cin>>pla[i];
    }
    // 遍历数组pla以寻找最长连续相同的元素序列
    for(int i=0;i<size;i++){
        // 如果当前元素与起始元素相同，增加右指针r并更新len和maxlen
        if(pla[r]==pla[l]){
            r++;
            len=r-l;
            maxlen=max(maxlen,len);
        }
        // 否则，将左指针l移动到右指针r的位置
        else{
            l=r;
        }
    }
    // 输出最长连续相同元素的长度
    cout<<maxlen;
    // 输出换行符
    cout<<"\n";
    // 使用goto语句循环回到开始位置
    goto start;
    // 返回0作为程序正常结束的标志
    return 0;
}
*/
//给出三维空间中的n个点（不超过10个）,求出n个点两两之间的距离,并按距离由大到小依次输出两个点的坐标及它们之间的距离。
//定义求解距离的函数
/*
double distance(int x1,int y1,int z1,int x2,int y2,int z2){
        return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2));
    }
int main(){
    // 定义点的个数变量
    int n;
    // 程序的起始点，用于循环读取输入
    start:
    // 提示用户输入点的个数
    cout<<"输入点的个数:";
    // 读取用户输入的点的个数
    cin>>n;
    // 将点的个数加1，可用于数组索引从1开始
    n=n+1;
    // 定义一个二维数组存储点的坐标，每点存储4个值，其中第0列未使用
    int coordinate[n][4]={0};
    // 提示用户输入坐标
    std::cout<<"输入坐标:";
    // 循环读取每个点的坐标
    for(int i=1;i<n;i++)
    for(int j=1;j<=3;j++) {
        std::cin>>coordinate[i][j];
    }
    // 计算每两个点之间的距离并输出
    for(int i=1;i<n;i++)
    for(int j=i+1;j<n;j++){
        // 调用distance函数计算两点之间的距离
        double dis=distance(coordinate[i][1],coordinate[i][2],coordinate[i][3],coordinate[j][1],coordinate[j][2],coordinate[j][3]);
        // 输出两点的坐标及其之间的距离
        cout<<coordinate[i][1]<<" "<<coordinate[i][2]<<" "<<coordinate[i][3]<<" - "<<coordinate[j][1]<<" "<<coordinate[j][2]<<" "<<coordinate[j][3]<<"距离等于"<<dis<<endl;
    }
    // 使用goto语句跳转到程序的起始点，形成循环
    goto start;
    // 返回0，表示程序正常结束
    return 0;
}
*/
/*
描述
给定n*n由0和1组成的矩阵，如果矩阵的每一行和每一列的1的数量都是偶数，则认为符合条件。
你的任务就是检测矩阵是否符合条件，或者在仅改变一个矩阵元素的情况下能否符合条件。
"改变矩阵元素"的操作定义为0变成1或者1变成0。

输入
输入n + 1行，第1行为矩阵的大小n(0 < n < 100)，以下n行为矩阵的每一行的元素，元素之间以一个空格分开。

输出
如果矩阵符合条件，则输出OK；
如果矩阵仅改变一个矩阵元素就能符合条件，则输出需要改变的元素所在的行号和列号，以一个空格分开。
如果不符合以上两条，输出Corrupt。
*/
/*
int main(){
    // 主函数开始，用于处理矩阵输入和错误校验
    int n;
    start:
    // 提示用户输入矩阵大小
    cout<<"输入矩阵的大小:";
    cin>>n;
    // 检查输入的矩阵大小是否在有效范围内（大于0且小于100），如果不在则提示重新输入
    if (n<=0||n>=100){
        cout<<"重新输入";
        goto start;
    }
    // 矩阵大小加1，用于处理边界情况
    n=n+1;
    int matrix[n][n]={0};
    // 循环读取用户输入的矩阵值
    for(int i=1;i<n;i++){
        cout<<"输入数值";
        for(int j=1;j<n;j++){
            std::cin>>matrix[i][j];
        }
    }
    int row[n]={0};
    int col[n]={0};
    int countr=0;
    int countc=0;
    // 计算每一行的元素和，并将结果对2取模存储在row数组中
    for(int i=1;i<n;i++){
        int countr = 0;
        for(int j=1;j<n;j++){
            countr += matrix[i][j];
        }
        row[i] = countr % 2;
    }
    // 计算每一列的元素和，并将结果对2取模存储在col数组中
    for(int j=1;j<n;j++){
        int countc = 0;
        for(int i=1;i<n;i++){
            countc += matrix[i][j];
        }
        col[j] = countc % 2;
    }
    int countrow=0;
    int countcol=0;
    int coordinaterow,coordinatecol;
    // 统计行和列中对2取模后为1的数量，并记录其坐标
    for(int i=1;i<n;i++){
        if(row[i]){
            countrow++;
            coordinaterow=i;
        }
        else if(col[i]){
            countcol++;
            coordinatecol=i;
        }
    }
    // 根据行和列中对2取模后为1的数量判断矩阵的状态
    if(countrow == 0 && countcol == 0){
        cout<<"OK";
    }
    else if(countrow==1&&countcol==1){
        cout<<"行"<<coordinaterow<<"列"<<coordinatecol;
    }
    else{
        cout<<"Corrupt";
    }
    cout<<"\n";
    // 循环回到开始，继续处理新的矩阵输入
    goto start;
    return 0;
}
*/
/*
给定一个5*5的矩阵，每行只有一个最大值，每列只有一个最小值，寻找这个矩阵的鞍点。
鞍点指的是矩阵中的一个元素，它是所在行的最大值，并且是所在列的最小值。
例如：在下面的例子中（第4行第1列的元素就是鞍点，值为8 ）。
11 3 5 6 9
12 4 7 8 10
10 5 6 9 11
8 6 4 7 2
15 10 11 20 25
*/
/*
int main(){
    // 定义标签 start，用于循环控制
    start:
    int rowmax=1;
    int colmin=1;
    // 初始化计数矩阵和输入矩阵
    int countmat[6][6]={0};
    int matrix[6][6]={0};
    // 输入矩阵的值
    for(int i=1;i<6;i++){
        cout<<"输入矩阵:";
        for(int j=1;j<6;j++){
            std::cin>>matrix[i][j];
        }
    }
    // 初始化测试矩阵
    int testmat[6][6]={0};
    // 遍历矩阵，寻找每行的最大值和每列的最小值，并更新计数矩阵
    for(int i=1;i<6;i++){
        for(int j=1;j<6;j++){
            if(matrix[i][j]>=matrix[i][rowmax]){
                rowmax=j;
            }
            if(matrix[j][i]<=matrix[colmin][i]){
                colmin=j;
            }
        }
        countmat[i][rowmax]++;
        countmat[colmin][i]++;
    }    
    // 检查计数矩阵，寻找既是每行最大值又是每列最小值的元素
    for(int i=1;i<6;i++)
    for(int j=1;j<6;j++){
        if(countmat[i][j]==2){
            // 输出满足条件的元素及其位置，并返回到 start 标签处重新开始
            cout<<i<<" "<<j<<" "<<matrix[i][j]<<endl;
            goto start;
            return 0;
        }
    }
    // 如果未找到满足条件的元素，输出 "not found" 并返回到 start 标签处重新开始
    cout<<"not found"<<endl;
    goto start;
    return 0;
}
}
*/
//简单版的立方数 1到一千
/*
int main(){
    int n;
    int a;
    int b=0;
kaishi:
    printf("输入一到一千数字\n输入0结束程序:");
    scanf("%d",&n);
    if(n==0){
        goto jieshu;
    }
    if(n<1||n>1000){
        printf("输入错误，请重新输入！\n");
        goto kaishi;
    }
    for(a=1;a<=n;a++){
        if(a*a*a==n){
            printf("Yes");
            int b=1;
            printf("\n");
            goto kaishi;
            return 0;
        }
    }
    if(b==0){
        printf("No");
        printf("\n");
        goto kaishi;
    }
jieshu:
    return 0;
}
*/
/*3个人比饭量，每人说了两句话：
A说：B比我吃的多，C和我吃的一样多
B说：A比我吃的多，A也比C吃的多
C说：我比B吃得多，B比A吃的多。
事实上，饭量和正确断言的个数是反序的关系。
请编程按饭量的大小输出3个人的顺序
*/
/*
int main(){
    int a;
    int b;
    int c;
    for (a=1;a<=3;a++){
        for(b=1;b<=3;b++){
            for(c=1;c<=3;c++){
                int da=(b>a)+(c==a);
                int db=(a>b)+(a>c);
                int dc=(c>b)+(b>a);
                if(a+da==b+db && b+db==c+dc){
                    if(a>b>c){
                        printf("ABC");
                    }
                    else if(a>c&&c>b){
                        printf("ACB");
                        printf("\n");
                        printf("da%d db%d dc%d\na%d b%d c%d\n",da,db,dc,a,b,c);
                    }
                    else if(b>a&&a>c){
                        printf("BAC");
                    }
                    else if(c>a&&a>b){
                        printf("CAB");
                    }
                    else if(b>c&&c>a){
                        printf("BCA");
                    }
                    else if(c>b&&b>a){
                        printf("CBA");
                    }
                }
            }
        }
    }
    return 0;
}
*/
/*
int main()
{
	int a, b, c;
	for(a = 1; a <= 3; ++a)
	for(b = 1; b <= 3; ++b)
	for(c = 1; c <= 3; ++c)
	{
		if(a != b && a != c && b != c)
		{
			if(a + (b > a) + (c == a) == 3 && 
				b + (a > b) + (a > c) == 3 && 
				c + (c > b) + (b > a) == 3)
			{
				if(a < b && a < c && b < c)
					printf("ABC\n");
				else if(a < b && a < c && c < b)
					printf("ACB\n");  
				else if(b < a && b < c && a < c)
					printf("BAC\n");
				else if(b < a && b < c && c < a)
					printf("BCA\n");
				else if(c < a && c < b && a < b)
					printf("CAB\n");
				else if(c < a && c < b && b < a)
					printf("CBA\n");	
				return 0;	
			}
		}
	}
	return 0;
}
*/
//实例：有三只小猪ABC，请分别输入三只小猪的体重，并且判断哪只小猪最重？
/*
int main(){
    int  a,b,c;
kaishi:
    printf("a:");
    scanf("%d",&a);
    printf("b:");
    scanf("%d",&b);
    printf("c:");
    scanf("%d",&c);
    if(a>b){
        if(c>a){
            printf("c 是 the heaviest\n");
        }
        else{
            printf("a 是 the heaviest\n");
        }
    }
    else{
        if(c>b){
            printf("c 是 the heaviest\n");
        }
        else{
            printf("b 是 the heaviest\n");
        }
    }
    goto kaishi;
    return 0;
}
*/
//洛谷题目
/*
int main(){
    int a,b;
    cin>>a;
    cin>>b;
    int c=a+b;
    cout<<c<<endl;
    return 0;
}
int main(){
    cout<<"Hello,World!";
    return 0;
}
int main(){
    cout<<"  *\n";
    cout<<" ***\n";
    cout<<"*****\n";
    cout<<" ***\n";
    cout<<"  *\n";
}
    int main(){
    cout<<"                ********\n";
    cout<<"               ************\n";
    cout<<"               ####....#.\n";
    cout<<"             #..###.....##....\n";
    cout<<"             ###.......######              ###            ###\n";
    cout<<"                ...........               #...#          #...#\n";
    cout<<"               ##*#######                 #.#.#          #.#.#\n";
    cout<<"            ####*******######             #.#.#          #.#.#\n";
    cout<<"           ...#***.****.*###....          #...#          #...#\n";
    cout<<"           ....**********##.....           ###            ###\n";
    cout<<"           ....****    *****....\n";
    cout<<"             ####        ####\n";
    cout<<"           ######        ######\n";
    cout<<"##############################################################\n";
    cout<<"#...#......#.##...#......#.##...#......#.##------------------#\n";
    cout<<"###########################################------------------#\n";
    cout<<"#..#....#....##..#....#....##..#....#....#####################\n";
    cout<<"##########################################    #----------#\n";
    cout<<"#.....#......##.....#......##.....#......#    #----------#\n";
    cout<<"##########################################    #----------#\n";
    cout<<"#.#..#....#..##.#..#....#..##.#..#....#..#    #----------#\n";
    cout<<"##########################################    ############\n";
}
int main(){
    char a;
    cin>>a;
    cout<<"  "<<a<<endl;
    cout<<" "<<a<<a<<a<<endl;
    cout<<a<<a<<a<<a<<a<<endl;
    return 0;
}
int main(){
    int a,b;
    cin>>a;
    cin>>b;
    cout<<a*b<<endl;
    return 0;
}
int main(){
    double a,c;
    int b,d;
    cin>>a;
    cin>>b;
    d=2*b;
    c=a/b;
    printf("%.3f\n",c);
    cout<<d;
    return 0;
}
int main(){
    double a,b,c;
    cin>>a;
    cin>>b;
    cin>>c;
    double p=(a+b+c)/2;
    double s=sqrt(p*(p-a)*(p-b)*(p-c));
    printf("%.1f",s);
    return 0;
}
int main(){
    double s,v;
    cin>>s;
    cin>>v;
    int time=s/v;
    double ftime=s/v;
    if(time<ftime){
        time++;
    }
    time=time+10;
    int departime=480-time;
    if(departime<0){
        departime+=24*60;
    }
    int hour=departime/60;
    int minute=departime%60;
    printf("%02d:%02d",hour,minute);
    return 0;
}
int main(){
    int h,r;
    cin>>h>>r;
    double v=3.14*r*r*h;
    double n1=20000/v;
    int n2=20000/v;
    if(n2<n1){
        n2++;
    }
    cout<<n2;
    return 0;
}
int main(){
    int a,b,c,d;
    cin>>a>>b>>c>>d;
    int st=a*60+b;
    int et=c*60+d;
    int time=et-st;
    int hour=time/60;
    int minute=time%60;
    cout<<hour<<" "<<minute;

}
int main(){
    int a,b;
    cin>>a>>b;
    double c=a+b*0.1;
    int d1=c/1.9;
    cout<<d1;
    return 0;
    
}
int main(){
    int a,b,c;
    cin>>a>>b>>c;
    int d=0.2*a+0.3*b+0.5*c;
    cout<<d;
    return 0;
}
int main(){
    int a;
    cin>>a;
    switch(a){
        case 1:cout << "I love Luogu!" << endl; break;
        case 2:cout << 2+4 << " " << 10-2-4 << endl;break;
        case 3:{int apples = 14, stu = 4;
            cout << apples / stu << endl;
            cout<< (apples / stu) * stu << endl;
            cout<< apples % stu << endl;
            break;}
        case 4:cout << fixed << setprecision(6) << 500.0/3 << endl;break;
        case 5:cout << (260 + 220) / (12 + 20) << endl; break;
        case 6:cout << sqrt(6*6 + 9*9) << endl; break;
        case 7:{int money = 100;
            money += 10; cout << money << endl;
            money -= 20; cout << money << endl;
            money = 0;   cout << money << endl;break;}
        case 8: {const double PI = 3.141593;
            double r = 5;
            cout << 2 * PI * r << endl;
            cout << PI * r * r << endl;
            cout<< 4.0/3 * PI * r*r*r << endl;break;}      case 9:
        case 10:
        case 11:
        case 12:
        case 13:
        case 14:
        default:cout << "No such problem!" << endl; break;
    }
    return 0;
}
int main(){
    int m,t,s;
    cin>>m>>t>>s;
    if(t==0){
        cout<<0;
        return 0;
    }
    int ttime=m*t;
    int stime=ttime-s;
    if(stime<0){
        cout<<0;
        return 0;
    }
    int n=stime/t;
    cout<<n;
    return 0;
}
int main(){
    int n;
    cin>>n;
    int a=0,b=0;
    if(n%2==0){
        a=1;
    }
    if(n>4&&n<=12){
        b=1;
    }
    if(a==1&&b==1){
        cout<<"1 ";
    }
    else{
        cout<<"0 ";
    }
    if(a==1||b==1){
        cout<<"1 ";
    }
    else{
        cout<<"0 ";
    }
    if(a+b==1){
        cout<<"1 ";
    }
    else{
        cout<<"0 ";
    }
    if(a+b==0){
        cout<<"1";
    }
    else{
        cout<<"0";
    }
    return 0;
}
int main(){
    int a;
    cin>>a;
    if(a>1){
        cout<<"Today, I ate "<<a<<" apples.";
    }
    else{
        cout<<"Today, I ate "<<a<<" apple.";
    }
}
int main(){
    int a;
    cin>>a;
    int local=a*5;
    int luogu=11+a*3;
    if(local>luogu){
        cout<<"Luogu";
    }
    else{
        cout<<"Local";
    }
}
int main(){
    int a[3];
    for(int i=0;i<3;i++){
        cin>>a[i];
    }
    sort(a,a+3);
    for(int i=0;i<3;i++){
        cout<<a[i]<<" ";
    } 
    return 0;
}
int main(){
    int year,month;
    cin>>year>>month;
    if(year%4==0&&year%100!=0||year%400==0){
        if(month==2){
            cout<<29;
        }
        else if(month==1||month==3||month==5||month==7||month==8||month==10||month==12){
            cout<<31;
        }
        else{
            cout<<30;
        
        }
    }
    else{
        if(month==2){
            cout<<28;
        }
        else if(month==1||month==3||month==5||month==7||month==8||month==10||month==12){
            cout<<31;
        }
        else{
            cout<<30;
        }
    
    }
    return 0;
}

int main(){
    double n,a1,a2,b1,b2,c1,c2;
    cin>>n>>a1>>a2>>b1>>b2>>c1>>c2;
    double n11=n/a1;
    int n1=n/a1;
    if(n11>n1){
        n1++;
    }
    double n21=n/b1;
    int n2=n/b1;
    if(n21>n2){
        n2++;
    }
    double n31=n/c1;
    int n3=n/c1;
    if(n31>n3){
        n3++;
    }
    int price1=n1*a2;
    int price2=n2*b2;
    int price3=n3*c2;
    int price[3]={price1,price2,price3};
    sort(price,price+3);
    cout<<price[0];
    return 0;

}
int main(){
    int time[8]={0};
    for(int i=1;i<=7;i++){
        int clas,extral;
        cin>>clas>>extral;
        time[i]=clas+extral;
        cout<<time[i]<<" ";

    }
    int maxday=1;
    int max=time[1];
    for(int i=1;i<=7;i++){
        if(max<time[i]){
            maxday=i;
            max=time[i];
        }
    }
    if(max<9){
        cout<<"0";
        return 0;
    }
    cout<<maxday;
    return 0;
}
int main(){
    int a,b,c;
    cin>>a>>b>>c;
    int trangle[3]={a,b,c};
    sort(trangle,trangle+3);
    if(trangle[0]+trangle[1]<=trangle[2]){
        cout<<"Not triangle\n";
        return 0;
    }
    if(trangle[0]*trangle[0]+trangle[1]*trangle[1]==trangle[2]*trangle[2]){
        cout<<"Right triangle\n";
    }
    if(trangle[0]*trangle[0]+trangle[1]*trangle[1]>trangle[2]*trangle[2]){
        cout<<"Acute triangle\n";
    }
    if(trangle[0]*trangle[0]+trangle[1]*trangle[1]<trangle[2]*trangle[2]){
        cout<<"Obtuse triangle\n";
    }
    if(trangle[0]==trangle[1]||trangle[1]==trangle[2]){
        cout<<"Isosceles triangle\n";
        if(trangle[0]==trangle[1]&&trangle[1]==trangle[2]){
            cout<<"Equilateral triangle\n";
        }
    }
}
int main(){
    int a;
    double price;
    cin>>a;
    if(a>400){
        double b=a-400;
        price=b*0.5663+150*0.4463+250*0.4663;
        printf("%.1f",price);
        return 0;
    }
    if(a>150){
        double b=a-150;
        price=b*0.4663+150*0.4463;
        printf("%.1f",price);
        return 0;
    }
    else{
        price=a*0.4463;
        printf("%.1f",price);
        return 0;
    }
}
int main(){
    int x,n;
    int a=0;
    int b=0;
    cin>>x>>n;
    for(int i=0;i<n;i++){
        if((x+i)%7==0||(x+i)%7==6){
            b++;
        }
    }
    a=n-b;
    a=a*250;
    cout<<a;
    return 0;
}
int main(){
    int a,b,c;
    cin>>a>>b>>c;
    int triangle[3]={a,b,c};
    sort(triangle,triangle+3);
    int d=__gcd(triangle[0], triangle[2]);
    cout<<triangle[0]/d<<"/"<<triangle[2]/d;
    return 0;
}
int main(){
    int apple[11];
    for(int i=1;i<11;i++){
        cin>>apple[i];
    }
    int tao;
    cin>>tao;
    tao+=30;
    sort(apple,apple+11);
    int sum=0;
    for(int i=1;i<11;i++){
        if(apple[i]<=tao){
            sum++;
        }
    }
    cout<<sum;
    return 0;

}
int main(){
    int a,b,c;
    cin>>a>>b>>c;
    int d[3]={a,b,c};
    sort(d,d+3);
    string e;
    cin>>e;
    if(e=="ABC"){
        cout<<d[0]<<" "<<d[1]<<" "<<d[2];
    }
    if(e=="ACB"){
        cout<<d[0]<<" "<<d[2]<<" "<<d[1];
    }
    if(e=="BAC"){
        cout<<d[1]<<" "<<d[0]<<" "<<d[2];
    }
    if(e=="BCA"){
        cout<<d[1]<<" "<<d[2]<<" "<<d[0];
    }
    if(e=="CAB"){
        cout<<d[2]<<" "<<d[0]<<" "<<d[1];
    }
    if(e=="CBA"){
        cout<<d[2]<<" "<<d[1]<<" "<<d[0];
    }
    return 0;   
}
int main(){
    string isbn;
    cin>>isbn;
    vector<int> digits;
    for(char c:isbn){
        if(isdigit(c)){
            digits.push_back(c-'0');
        }
        if(c=='X'){
            digits.push_back(88);
        }
    }
    
    int sum=0;
    for(int i=0;i<9;i++){
        sum+=digits[i]*(i+1);
    }
    int id=sum%11;
    if(id==10){
        id=88;
    }
    if(digits[9]==id){
        cout<<"Right";
        return 0;
    }
    if(id=88){
        cout<<digits[0]<<"-"<<digits[1]<<digits[2]<<digits[3]<<"-"<<digits[4]<<digits[5]<<digits[6]<<digits[7]<<digits[8]<<"-"<<'X';

    }
    else{
        cout<<digits[0]<<"-"<<digits[1]<<digits[2]<<digits[3]<<"-"<<digits[4]<<digits[5]<<digits[6]<<digits[7]<<digits[8]<<"-"<<id;

    }
    return 0;

}

int main(){
    int n;
    cin>>n;
    int a[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    sort(a,a+n);
    cout<<a[0];
    return 0;
}
    int main(){
    int n,k;
    cin>>n>>k;
    int a[n+1]={0};
    int b[n+1]={0};
    for(int i=1;i<=n;i++){
        if(i%k==0){
            a[i]=i;
        }
        else{
            b[i]=i;
        }
    }
    double asum=0;
    double bsum=0;
    double anum=0;
    double bnum=0;
    for(int i=1;i<=n;i++){
        if(a[i]!=0){
            asum+=a[i];
            anum++;
        }
        if(b[i]!=0){
            bsum+=b[i];
            bnum++;
        }
        
    }
    double aave=asum/anum;
    double bave=bsum/bnum;
    printf("%.1f %.1f",aave,bave);
    return 0;
}
int main(){
    int a=0;
    int b=1;
    cin>>a;
    if(a==1){
        cout<<1;
        return 0;
    }
    while(a!=1){
        a=a/2;
        b++;
       
    }
    cout<<b;
    return 0;
}
int main(){
    int n;
    int a=0;
    cin>>n;
    for(int i=n;i>=1;i--){
        for(int j=1;j<=n;j++){
            a++;
            cout<<setw(2)<<setfill('0')<<a;
        }
        n--;
        cout<<"\n";
    }
    return 0;
    
}
int fac(int n){
    int fac=1;
    for(int i=1;i<=n;i++){
        fac*=i;
    }
    return fac;
}
int main(){
    int n;
    cin>>n;
    int sum=0;
    for(int i=1;i<=n;i++){
        sum+=fac(i);
    }
    cout<<sum;
    return 0;
}
int main(){
    int n,x;
    cin>>n>>x;
    int b=1;
    int sta=0;
    for (int i=1;i<=n;i++){
        b=i;
        while(b!=0){
            if(b%10==x){
                sta++;
            }
            b=b/10;
        }
    }
    cout<<sta;
    return 0;

}

double last(double n){
    double a=1/n;
    return a;
}
int main(){
    int k;
    cin>>k;
    int a=0;
    double sn=0.0;
    int i=1;
    while(sn<=k){
        sn+=last(i);
        i++;
        a++;
    }
    cout<<a;
    return 0;
}

int comulative(int n){
    int sumday;
    for(int i=1;i<=n;i++){
        sumday+=i;
    }
    return sumday;
}
int digitsum(int n){
    int sum;
    for(int i=1;i<=n;i++){
        sum+=(i*i);
    }
    return sum;
}
int main(){
    int k;
    int a=0;
    int sum=0;
    int besum;
    int digsum;

    cin>>k;
    int i=1;
    if(k==1){
        cout<<1;
        return 0;
    }
    while (sum<=k){
        sum+=comulative(i);
        i++;
    }
    for (int i=1;i<=k;i++){
        digsum+=digitsum(i);
    }
    if(sum==k){
        
        cout<<digsum;
        return 0;
    }
    else{
        besum=i*(sum-k);
        digsum=digsum-besum*i;
        cout<<digsum;
        return 0;
    }
    return 0;
}
int main(){
    int k;
    int coin=0;
    int day=0;
    cin>>k;
    for(int i=1;i<=k;i++){
        for(int j=1;j<=i;j++){
            day++;
            coin+=i;
            if(day==k){
                cout<<coin;
                return 0;
            }
            
        }
    }
    return 0;
}

int main(){
    int n;
    int sum=0;
    cin>>n;
    for(int i=1;i<=n;i++){
        sum+=i;
    }
    cout<<sum;
    return 0;
}
int main(){
    int l;
    cin>>l;
    int r[20000]={0};
    r[2]=2;
    r[3]=3;
    r[5]=5;
    r[7]=7;
    for(int i=8;i<=20000;i++){
        double a=sqrt(i);
        int b=sqrt(i);

        if(i%2==0||i%3==0||i%5==0||i%7==0||a==b){
            r[i]=0;
        }
        
        else{
            r[i]=i;
        }
    }
    int prime[20000]={0};
    int count=0;
    int sum=0;
    for(int i=1;i<=20000;i++){
        sum+=r[i];
        if(r[i]!=0&&sum<=l){
            prime[count++]=r[i];
            cout<<r[i]<<"\n";
        }
        if(sum>=l){
            cout<<count;
            return 0;
        }
    }
    return 0;


}
int main(){
    char a[10000];
    while(cin.getline(a,10000)){
        for(int i=0;a[i]!='\0';i++){
            if(a[i]=='Z'){
                a[i]='A';
                continue;
            }
            if(a[i]=='z'){
                a[i]='a';
                continue;
            }
            if(a[i]==' '){
                continue;
            }
            a[i]++;
            
        }
    }
    cout<<a;
    return 0;
}
int main(){
    string input;
    getline(cin,input);
    int i=0;
    for(int j=0;j<input.length();j++){
        if(input[j]==' '){
            continue;
        }
        if(input[j]=='z'){
            input[j]='a';
            continue;
        }
        input[j]+=1;

    }
    cout<<input;
    return 0;
}
int main(){
    start:
    string s1;
    string s2;
    getline(cin,s1);
    getline(cin,s2);
    if(s1.length()>20||s2.length()>20){
        cout<<"大于20 重新输入";
        goto start;
    }
    if(s1.length()>=s2.length()){
        s1+=s2;
        cout<<s1;
        return 0;
    }
    else{
        s1=s2+s1;
        cout<<s1;
        return 0;
    }
    return 0;

}
int main(){
    string s;
    getline(cin,s);
    int sta=1;
    for(int i=0;i<s.length();i++){
        if(s[i]==' '){
            sta++;
        }
    }
    cout<<sta;
    return 0;
}
int main(){
    string input;
    getline(cin,input);
    stringstream ss(input);
    string word;
    while(ss>>word){
        reverse(word.begin(),word.end());
        cout<<word<<endl;
    }
    return 0;

}
int main(){
    char a;
    int b;
    float c;
    double d;
    cin>>a>>b>>c>>d;
    printf("%c %d %.6f %.6f",a,b,c,d);
}
int main(){
    string input;
    getline(cin,input);
    stringstream ss(input);
    string word;
    string output;
    while(ss>>word){
        int len=output.length();
        if(len==0){
            output=word;
            continue;
        }
        if(output[len-1]=='.'||output[len-1]=='?'||output[len-1]=='!'||output[len-1]==','){
            output+=word;
        }
        else{
            output=output+' '+word;
        }
    }
    cout<<output;
    return 0;
}
int main(){
    string in;
    getline(cin,in);
    stringstream ss(in);
    set<string> words;
    string word;
    while(ss>>word){
        words.insert(word);
    }
    for(auto word:words){
        cout<<word<<endl;
    }
    return 0;

}
int main(){
    string in;
    getline(cin,in);
    stringstream ss(in);
    string word;
    vector<string> words;
    int i=0;
    while(ss>>word){
        int n=word.length()-1;
        if(word[n]=='.'){
            word.erase(n);
        }
        words.push_back(word);
    }
    string max;
    int maxlen;
    int len;
    for(auto word:words){
        len=word.length();
        if(len>maxlen){
            maxlen=len;
            max=word;
        }
    }
    cout<<max;
    return 0;
}
int main(){
    start:
    vector <string> words;
    string input;
    getline(cin,input);
    int sta;
    string s;
    string s1;
    string s2;
    for(int i=0;i<input.length();i++){
        if(input[i]!=','){
            s+=input[i];
        }
        else{
            sta=i;
            break;
        }
    }
    for(int i=sta+1;i<input.length();i++){
        if(input[i]!=','){
            s1+=input[i];
        }
        else{
            sta=i;
            break;
        }
        
    }
    for(int i=sta+1;i<input.length();i++){
        if(input[i]!=','){
            s2+=input[i];
        }

        else{
            break;
        }
    }
    cout<<s<<endl;
    cout<<s1<<endl;
    cout<<s2<<endl;
    s.find(s1);
    s.rfind(s2);
    if(s.length()>300){
        cout<<"输入过长"<<endl;
        cout<<"重新输入";
        goto start;
    }
    else if(s.length()==0){
        cout<<"输入内容";
        goto start;
    }
    
    
    if(s1.length()>s.length()||s2.length()>s.length()){
        cout<<"输入过长"<<endl;
        cout<<"重新输入";
        goto start;
    }
    else if(s1.length()==0||s2.length()==0){
        cout<<"输入内容";
        goto start;
    }
    int locations1;
    int locations2;
    bool result1=false;
    bool result2=false;
    for(int i=0;i<=s.length()-s1.length();i++){
        string check;
        check+=s[i];
        check+=s[i+1];
        if(check==s1){
            result1=true;
            locations1=i+2;
            break;
        }
    } 
    for(int i=0;i<=s.length()-s2.length();i++){
        string check;
        check+=s[i];
        check+=s[i+1];
        if(check==s2){
            result2=true;
            locations2=i;
        }
    } 
    if(!result1||!result2){
        cout<<"-1"<<endl;
        return 0;
    }
    int distance=locations2-locations1;
    cout<<distance;
    return 0;

}

int main(){
    vector<string> input;
    string tmpinput;
    getline(cin,tmpinput);
    stringstream ss(tmpinput);
    string a;
    while(ss>>a){
        input.push_back(a);
    }
    string check;
    getline(cin,check);
    int count;
    string replace;
    getline(cin,replace);
    for(auto word:input){
        if(check==word){
            input.erase(input.begin()+count);
            input.insert(input.begin()+count,replace);
        }
        else{
            count++;
        }
    }
    int count1=0;
    for(auto word:input){
        count1++;
        if(count1<input.size()){
            cout<<word<<" ";

        }
        else{
            cout<<word;
        }
        
    }
    return 0;
    
}

int main(){
    int n,m;
    cin>>n;
    cin>>m;
    char a[m][n]={""};
    for(int i=0;i<m;i++){
        for(int j=0;j<n;j++){
            cin>>a[i][j];
        }
    }
    int sum[m]={0};
    for(int k=0;k<m;k++){
        for(int i=0;i<n-1;i++){
            for(int j=i+1;j<n;j++){
                if(a[k][i]>a[k][j]){
                    sum[k]++;
                }
            }
        }
    }
    int count=0;
    int maxlocation=0;
    int out[m]={0};
    for(int j=0;j<m;j++){
        int max=0;
        for(int i=0;i<m;i++){
            if(sum[i]>max){
                max=sum[i];
                maxlocation=i;
            }
        }
        out[j]=maxlocation;
        sum[maxlocation]=0;
    }
    for(int i=m-1;i>=0;i--){
        for(int j=0;j<n;j++){
            cout<<a[out[i]][j];

        }
        cout<<"\n";
    }
    return 0;
}

int main(){
    double s;
    cin>>s;
    double distance=2;
    double sum=0;
    int count=0;
    while(sum<s){
        sum+=distance;
        count++;
        distance*=0.98;
    }
    cout<<count<<endl;
    return 0;
}

int main(){
    string n;
    getline(cin,n);
    if(n.empty()){
        return 0;
    }
    if(n[0]=='-'){
        reverse(n.begin(),n.end());
        n.erase(n.end()-1);
        n.insert(n.begin(),'-');
        int coordinate=0;
        for(int i=1;i<n.length();i++){
            if(n[i]=='0'){
                coordinate++;
            }
            else{
                break;
            }
        }
        if(coordinate!=0){
            n.erase(n.begin()+1,n.begin()+coordinate+1);
        }
    }
    else{
        reverse(n.begin(),n.end());
        int coordinate=0;
        for(int i=0;i<n.length();i++){
            if(n[i]=='0'){
                coordinate++;
            }
            else{
                break;
            }
        }
        if(coordinate!=0){
            n.erase(n.begin(),n.begin()+coordinate);
        }
    }
    cout<<n;
    return 0;


}
int main(){
    int n;
    cin>>n;
    cin.ignore();
    set<string> input;
    string sinput;
    getline(cin,sinput);
    stringstream ss(sinput);
    string temp;
    while(ss>>temp){
        input.insert(temp);
    }
    int min;
    int max;
    for(int i=0;i<1001;i++){
        if(input[input.begin()]=='i')
    }

}
int main(){
    int n;
    cin>>n;
    if(n==1){
        cout<<0;
        return 0;
    }
    cin.ignore();
    set<int> input;
    for(int i=0;i<n;i++){
        int temp;
        cin>>temp;
        input.insert(temp);
    
    }
    int count=-(*input.begin()-*prev(input.end()));
    cout<<count;
    return 0;
        
}
int main(){
    int n;
    cin>>n;
    if(n==1){
        cout<<1;
        return 0;
    }
    int a[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    int count[n]={0};
    for(int i=0;i<n-1;i++){
        for(int j=i+1;j<n;j++){
            if(a[j]==a[j-1]+1){
                count[i]++;
            }
            else{
                break;
            }
        }
    }
    int max=0;
    int maxlocation=0;
    for(int i=0;i<n;i++){
        cout<<count[i]<<"\n";
        if(count[i]>max){
            max=count[i];
            maxlocation=i;
        
        }
    }
    cout<<max+1;
    return 0;
}

int main(){
    int n;
    cin>>n;
    multiset<int> input;
    for(int i=0;i<n;i++){
        int temp;
        cin>>temp;
        input.insert(temp);
    }
    input.erase(input.begin());
    input.erase(prev(input.end()));
    double sum=0;
    double result;
    double count=0;
    for(auto temp:input){
        sum+=temp;
        count++;
    }
    result=sum/count;
    printf("%.2f",result);
    return 0;
}
int main(){
    int n;
    cin>>n;
    n/=364;
    for(int i=100;i>=1;i--){
        for(int j=1;j<=100;j++){
            if(i+3*j==n){
                cout<<i<<endl;
                cout<<j<<endl;
                return 0;
            }
        }
    }
    return 0;
}

int main(){
    int n;
    cin>>n;
    if(n==1){
        cout<<0;
        return 0;
    }
    int cute[n];
    for(int i=0;i<n;i++){
        cin>>cute[i];
    }
    int fish[n]={0};
    for(int i=1;i<n;i++){
        for(int j=0;j<i;j++){
            if(cute[j]<cute[i]){
                fish[i]++;
            }
        }
    }
    for(int i=0;i<n;i++){
        if(i!=n-1){
            cout<<fish[i]<<" ";
        }
        else{
            cout<<fish[i];
        }
    }
    return 0;
}

int main(){
    vector<int> input;
    string sinput;
    getline(cin,sinput);
    stringstream ss(sinput);
    int temp;
    while(ss>>temp){
        input.push_back(temp);
    }
    input.erase(prev(input.end()));
    reverse(input.begin(),input.end());
    int count=0;
    for(auto output:input){
        count++;
        if(count==input.size()){
            cout<<output;
        }
        else{
            cout<<output<<" ";
        }
    }
    return 0;

}
int main(){
    int n;
    cin>>n;
    if(n==1){
        cout<<1;
        return 0;
    }
    vector<int> output;
    output.push_back(n);
    while (n!=1){
        if(n%2==0){
            n/=2;
        }
        else{
            n=3*n+1;
        }
        output.push_back(n);
    }
    int count=0;
    reverse(output.begin(),output.end());
    for(auto temp:output){
        count++;
        if(count==output.size()){
            cout<<temp;
        }
        else{
            cout<<temp<<" ";
        }
    }
    return 0;
    
}
int main(){
    int l;
    int m;
    cin>>l>>m;
    if(l==1){
        if(m==1){
            cout<<0;
            return 0;
        
        }
        else{
            cout<<1;
            return 0;
        }
    }
    vector<int> length(l+1,1);
    for(int i=0;i<m;i++){
        int u,v;
        cin>>u>>v;
        for(int j=u;j<=v;j++){
            length[j]=0;
        }
    }
    int sum=0;
    for(int i=0;i<l+1;i++){
        sum+=length[i];
    }
    cout<<sum;
    return 0;
}
int main(){
    int n;
    cin>>n;
    int winning[7];
    for(int i=0;i<7;i++){
        cin>>winning[i];
    }
    int mywin[n][7];
    for(int i=0;i<n;i++){
        for(int j=0;j<7;j++){
            cin>>mywin[i][j];
        }
    }
    int count[n]={0};
    for(int i=0;i<n;i++){
        for(int j=0;j<7;j++){
            for(int k=0;k<7;k++){
                if(mywin[i][j]==winning[k]){
                    count[i]++;
                }
            }
        }
    }
    int prize[8]={0};
    for(int i=1;i<=7;i++){
        for(int j=0;j<n;j++){
            if(count[j]==i){
                prize[i]++;
            }
        }
    }
    for(int i=7;i>=1;i--){
        cout<<prize[i]<<" ";
    }
    return 0;
}
int main(){
    int n;
    cin>>n;
    if(n==1){
        cout<<1;
        return 0;
    }
    int magic[40][40]={0};
    int coordinate[(n*n)+1][2]={0};
    magic[1][(n/2)+1]=1;
    coordinate[1][0]=1;
    coordinate[1][1]=(n/2)+1;
    int k=1;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            k++;
            if(coordinate[k-1][0]==1&&coordinate[k-1][1]!=n){
                magic[n][coordinate[k-1][1]+1]=k;
                coordinate[k][0]=n;
                coordinate[k][1]=coordinate[k-1][1]+1;
            }
            else if(coordinate[k-1][0]!=1&&coordinate[k-1][1]==n){
                magic[coordinate[k-1][0]-1][1]=k;
                coordinate[k][0]=coordinate[k-1][0]-1;
                coordinate[k][1]=1;
            }
            else if(coordinate[k-1][0]==1&&coordinate[k-1][1]==n){
                magic[coordinate[k-1][0]+1][coordinate[k-1][1]]=k;
                coordinate[k][0]=coordinate[k-1][0]+1;
                coordinate[k][1]=coordinate[k-1][1];
            }
            else if(magic[coordinate[k-1][0]-1][coordinate[k-1][1]+1]==0){
                magic[coordinate[k-1][0]-1][coordinate[k-1][1]+1]=k;
                coordinate[k][0]=coordinate[k-1][0]-1;
                coordinate[k][1]=coordinate[k-1][1]+1;
            }
            else{
                magic[coordinate[k-1][0]+1][coordinate[k-1][1]]=k;
                coordinate[k][0]=coordinate[k-1][0]+1;
                coordinate[k][1]=coordinate[k-1][1];
            }
        }
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            cout<<magic[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}
    int main(){
    int n;
    cin>>n;
    char tv[6][500]={'.'};
    char num[101]={' '};
    for(int i=1;i<=n;i++){
        cin>>num[i];
    }
    for(int i=1;i<=n;i++){
        if(num[i]=='1'){
            tv[1][4*i]='.';
            tv[1][4*i-1]='X';
            tv[1][4*i-2]='.';
            tv[1][4*i-4]='.';
        }
        else if(num[i]=='4'){
            tv[1][4*i]='.';
            tv[1][4*i-1]='X';
            tv[1][4*i-2]='.';
            tv[1][4*i-4]='X';
        }
        else{
            tv[1][4*i]='.';
            tv[1][4*i-1]='X';
            tv[1][4*i-2]='X';
            tv[1][4*i-4]='X';
        }
    }
    cout<<tv[1][0];
    return 0;
}
    int main(){
    int n;
    cin>>n;
    int array[101]={0};
    for(int i=1;i<=n;i++){
        cin>>array[i];
    }
    int sum=0;
    int history[101]={0};
    for(int i=1;i<n;i++){
        for(int j=i+1;j<=n;j++){
            for(int k=1;k<=n;k++){
                if(array[i]+array[j]==array[k]){
                    sum++;
                    history[k]++;
                    if(history[k]>1){
                        sum--;
                    }
                    break;
                }
            }
        }
    }
    cout<<sum;
    return 0;
}
    int main(){
    int n;
    cin>>n;
    int lanter[2000000000]={0};
    for(int i=1;i<=3;i++){
        int t;
        double a;
        cin>>a>>t;
        for(int j=1;j<=t;j++){
            int temp=a*j;
            if(lanter[temp]==0){
                lanter[temp]=1;
            }
            else{
                lanter[temp]=0;
            }
        }
    }
    for(int i=1;i<=2000000000;i++){
        if(lanter[i]==1){
            cout<<i;
            return 0;
        }
    }
    return 0;
}
#include<bits/stdc++.h>
using namespace std;
int main(){
    int n;
    cin>>n;
    long long x=0;
    for(int i=1;i<=3;i++){
        int t;
        double a;
        cin>>a>>t;
        for(int j=1;j<=t;j++){
            long long temp;
            temp=(int)floor(a*j);
            x^=temp;
        }
    }
    cout<<x;
    return 0;
}
int main(){
    int n;
    cin>>n;
    int count=2;
    int x,y;
    x=1;
    y=1;
    int out[10][10]={0};
    out[1][1]=1;
    while(count<n*n){
        while(x<n&&out[x+1][y]==0){
            out[x+1][y]=count++;
            x++;
        }
        while(y<n&&out[x][y+1]==0){
            out[x][y+1]=count++;
            y++;
        }
        while(x>1&&out[x-1][y]==0){
            out[x-1][y]=count++;
            x--;
        }
        while(y>1&&out[x][y-1]==0){
            out[x][y-1]=count++;
            y--;
        }
        
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            if(out[i][j]==0){
                out[i][j]=n*n;
            }
        }
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            cout<<setw(3)<<out[j][i];
        }
        cout<<"\n";
    }
    return 0;
}
    int main(){
    int n;
    cin>>n;
    int trangle[21][21]={0};
    for(int i=1;i<=n;i++){
        for(int j=1;j<=i;j++){
            if(j!=1&&j!=i){
                trangle[i][j]=trangle[i-1][j-1]+trangle[i-1][j];
            }
            else{
                trangle[i][j]=1;
            }
            cout<<trangle[i][j]<<" ";
        }
        cout<<"\n";
    }
    return 0;
}
#include<bits/stdc++.h>
using namespace std;
int main(){
    int n,m,k;
    cin>>n>>m>>k;
    int phalanx[106][106]={0};
    for(int i=1;i<=m;i++){
        int x,y;
        cin>>x>>y;
        x+=2;
        y+=2;
        phalanx[x][y]=1;
        phalanx[x-1][y]=1;
        phalanx[x-2][y]=1;
        phalanx[x+1][y]=1;
        phalanx[x+2][y]=1;
        phalanx[x-1][y-1]=1;
        phalanx[x-1][y+1]=1;
        phalanx[x+1][y+1]=1;
        phalanx[x+1][y-1]=1;
        phalanx[x][y-2]=1;
        phalanx[x][y+2]=1;
        phalanx[x][y-1]=1;
        phalanx[x][y+1]=1;
    }
    for(int i=0;i<k;i++){
        int x,y;
        cin>>x>>y;
        x+=2;
        y+=2;
        for(int j=x-2;j<=x+2;j++){
            for(int k=y-2;k<=y+2;k++){
                phalanx[j][k]=1;
            }
        }
    }
    int count=0;
    for(int i=3;i<=n+2;i++){
        for(int j=3;j<=n+2;j++){
            if(phalanx[i][j]==0){
                count++;
            }
        }
    }
    cout<<count;
    return 0;
}
int main(){
    int n;
    cin>>n;
    int count=1;
    int zero=0;
    for(int i=1;i<=n*n;i++){
        int temp;
        cin>>temp;
        for(int j=1;j<=temp;j++){
            if(zero%2==0){
                cout<<"0";
                if(count++%n==0){
                    if(count==n*n+1){
                        return 0;
                    }
                    else{
                        cout<<"\n";
                    }
                    
                }
            }
            else{
                cout<<"1";
                if(count++%n==0){
                    if(count==n*n+1){
                        return 0;
                    }
                    else{
                        cout<<"\n";
                    }
                }
            }
        }
        zero++;
        

    }
    return 0;
}
int main(){
    string in;
    getline(cin,in);
    int n=in.length();
    for(int i=0;i<n;i++){
        string temp;
        getline(cin,temp);
        in+=temp;

    }
    vector<int> out;
    int count=0;
    set<int> temp;
    for(int i=0;i<in.length();i++){
        if(in[i]==in[i+1]){
            
            temp.insert(i);
            temp.insert(i+1);
        }
        else{
            int temp_size=temp.size();
            if(temp_size==0){
                temp_size=1;
            }
            out.push_back(temp_size);
            temp.clear();
        }
    }
    cout<<n<<" ";
    if(in[0]=='1'){
        cout<<0<<" ";
    }
    for(auto temp:out){
        
        cout<<temp<<" ";
    }
    return 0;
}
#include<cctype>
int main(){
    string s;
    getline(cin,s);
    for(auto temp:s){
        temp=toupper(temp);
        cout<<temp;
    }
    return 0;
    
}
    
    
int main(){
    string in;
    getline(cin,in);
    for(int i=0;i<in.length()-1;i++){
        char temp;
        temp=in[i];
        if(temp==in[i+1]){
            
        }
    }
}
    int main(){
    double sum=0;
    double distance[4][3]={0};
    for(int i=1;i<=3;i++){
       double x,y;
       cin>>x>>y;
       distance[i][1]=x;
       distance[i][2]=y;
    }
    for(int i=1;i<=2;i++){
        for(int j=i+1;j<=3;j++){
            sum+=sqrt((distance[i][1]-distance[j][1])*(distance[i][1]-distance[j][1])+(distance[i][2]-distance[j][2])*(distance[i][2]-distance[j][2]));
        }
    }
    printf("%.2f",sum);
    return 0;
}

int main(){
    int n;
    int out;
    cin>>n;
    for(int i=1;i<=n;i++){
        int temp;
        cin>>temp;
        if(temp==1){
            continue;
        }
        for(int j=2;j<=sqrt(temp);j++){
            if(temp%j==0){
                temp=0;
            }
        }
        if(temp!=0){
            cout<<temp<<" ";
        }
    }
    return 0;
}
#include<bits/stdc++.h>
using namespace std;
int n;
string in;
string num[10][5]={"XXX","X.X","X.X","X.X","XXX",
				  	 "..X","..X","..X","..X","..X",
				 	 "XXX","..X","XXX","X..","XXX",
				   	 "XXX","..X","XXX","..X","XXX",
				   	 "X.X","X.X","XXX","..X","..X",
				   	 "XXX","X..","XXX","..X","XXX",
				  	 "XXX","X..","XXX","X.X","XXX",
				   	 "XXX","..X","..X","..X","..X",
				  	 "XXX","X.X","XXX","X.X","XXX",
				  	 "XXX","X.X","XXX","..X","XXX"};
int main(){
	cin>>n>>in;
	for(int i=0;i<5;i++){
		for(int j=0;j<n;j++){
			cout<<num[in[j]-'0'][i];
			if(j!=n-1)cout<<".";
		}
		cout<<"\n";
	}
	return 0;
}

int main(){
    int m,n;
    cin>>m>>n;
    int count=0;
    vector<int> out;
    for(int i=m;i<=n;i++){
        int temp=i;
        if(temp%4==0&&temp%100!=0||temp%400==0){
            count++;
            out.push_back(i);
        }
    }
    cout<<count<<endl;
    for(auto temp:out){
        cout<<temp<<" ";
    }
    return 0;
    
}
    int main(){
    double n,m;
    cin>>n>>m;
    set<double> out;
    double itemp;
    for(int i=1;i<=n;i++){
        multiset<double> temp;
        double tsum=0;
        for(int j=1;j<=m;j++){
            cin>>itemp;
            temp.insert(itemp);
        }
        temp.erase(temp.begin());
        temp.erase(prev(temp.end()));
        for(auto it:temp){
            tsum+=it;
        }
        out.insert(tsum);
    }
    printf("%.2f",*prev(out.end())/(m-2));
    return 0;
}
int factorio(int n){
    if(n==1){
        return 1;
    }
    else{
        return n*factorio(n-1);
    }
}
int main(){
    int n;
    cin>>n;
    cout<<factorio(n);
    return 0;
}
int main(){
    long long n,m,k,t;
    cin>>n>>m>>k>>t;
    multiset<long long> tshade;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            cin>>t;
            tshade.insert(t);
        }
    }
    long long shadecount=0;
    vector<long long> shade;
    for(auto it:tshade){
        shade.push_back(it);
    }
    reverse(shade.begin(),shade.end());
    long long tcount=0;
    long long scount=0;
    for(auto it:shade){
        if(t>0){
            scount+=it;
            tcount+=it;
            if(tcount>=k){
                t+=tcount/k;
                tcount%=k;
            }
            t--;
        }
    }
    cout<<scount;
    return 0;

}
    #include <stdio.h>

int main() {
    int result = 0101; // 八进制数 0101，十进制值为 65（不是注释中的10）
    printf("按位与结果:\n");
    
    // 注意：%b 不是标准C语言的格式说明符，在某些编译器可能不支持
    printf("二进制：%b\n", result);
    
    printf("八进制：%o\n", result);
    printf("十进制：%d\n", result);
    printf("十六进制：%x\n", result);
    
    return 0;
}
int cheter[1025][1025]={0};
void padon(int l,int x,int y){
    if(l==2){
        cheter[x][y]=0;
    }
    else{
        l=l/2;
        for(int i=x;i<x+l;i++){
            for(int j=y;j<y+l;j++){
                cheter[i][j]=0;
            }
        }
        padon(l,x+l,y+l);
        padon(l,x,y+l);
        padon(l,x+l,y);
    }
}
int main(){
    int l;
    cin>>l;
    l=1<<l;
    int x=1;
    int y=1;
    fill(&cheter[1][1],&cheter[1024][1024]+1,1);
    padon(l,x,y);
    for(int i=1;i<=l;i++){
        for(int j=1;j<=l;j++){
            cout<<cheter[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}
    struct Students{
    char name[10];
    int chinese;
    int math;
    int english;
    int index;
};
bool grade(const Students& a,const Students& b){
    if(a.chinese+a.math+a.english==b.chinese+b.math+b.english){
        return a.index<b.index; 
    }
    else{
        return (a.chinese+a.math+a.english)>(b.chinese+b.math+b.english);
    }
}
int main(){
    int n=0;
    cin>>n;
    vector<Students> stu;
    for(int i=0;i<n;i++){
        Students temp;
        temp.index=i;
        cin>>temp.name>>temp.chinese>>temp.math>>temp.english;
        stu.push_back(temp);
    }
    sort(stu.begin(),stu.end(),grade);
    cout<<(*stu.begin()).name<<" "<<(*stu.begin()).chinese<<" "<<(*stu.begin()).math<<" "<<(*stu.begin()).english<<endl;
    return 0;
    
}
    int main(){
    int n;
    cin>>n;
    vector<int> prime;
    vector<int> reprime;
    prime.push_back(2);
    reprime.push_back(2);
    for(int i=3;i<=n;i+=2){
        bool temp=1;
        for(int j=2;j<=sqrt(i);j++){
            if(i%j==0){
                temp=0;
                break;
            }
        }
        if(temp){
            prime.push_back(i);
            reprime.push_back(i);
        }
    }
    reverse(reprime.begin(),reprime.end());
    for(int i=1;i<=(n/2-1);i++){
        int temp=2*i+2;
        bool ntemp=0;
        while(!ntemp){
            for(auto it:prime){
                for(auto ti:reprime){ 
                    if(temp==it+ti){
                        cout<<temp<<"="<<it<<"+"<<ti<<endl;
                        ntemp=1;
                        break;
                    }
                }
                if(ntemp){
                    break;
                }
            }
        }
    }
    return 0;
}
int ass[31]={0};
long long sum(int n,int size){
    long long temp=0;
    if(n==1){
        for(int i=1;i<=size;i++){
            temp+=ass[i];
        }
        return temp;
    }
    else{
        for(int i=1;i<=size-n+1;i++){
            for(int j=i;j<=i+n-1;j++){
                temp+=ass[j];
            }
        }   
        return temp+sum(n-1,size);
    }

}
int main(){
    int size=0;
    int i=1;
    string in;
    getline(cin,in);
    string temp;
    stringstream ss(in);
    while(ss>>temp){
        ass[i]=stoi(temp);
        i++;
        size++;
    }
    long long out=sum(size,size);
    cout<<out;
    return 0;
}
void multip(vector<int>& factor,int n){
    int remender=0;
    for(int i=0;i<factor.size();i++){
        int temp=factor[i]*n+remender;
        factor[i]=temp%10;
        remender=temp/10;
    }
    while(remender){
        factor.push_back(remender%10);
        remender/=10;
    }
}
void factorial(vector<int>& factor,int n){
    for(int i=2;i<=n;i++){
        multip(factor,i);
    }
}
void add(vector<int>&factor,vector<int>&temp){
    int size=max(factor.size(),temp.size());
    if(factor.size()>temp.size()){
        temp.resize(factor.size(),0);
    }
    int remender=0;
    for(int i=0;i<factor.size();i++){
        int itemp=factor[i]+temp[i]+remender;
        temp[i]=itemp%10;
        remender=itemp/10;
    }
    while(remender){
        temp.push_back(remender%10);
        remender/=10;
    }
}
int main(){
    int n;
    cin>>n;
    vector<int> factor;
    vector<int> temp;
    factor.push_back(1);
    for(int i=1;i<=n;i++){
        factorial(factor,i);
        add(factor,temp);
        factor.clear();
        factor.push_back(1);
    }
    reverse(temp.begin(),temp.end());
    for(auto it:temp){
        cout<<it;
    }
    return 0;
}
int main(){
    string in;
    char s;
    int length=0;
    while(cin>>s){
        if(s=='E'){
            break;
        }
        in+=s;
        length++;
    }
    int n11=length/11+1;
    int n21=length/21+1;
    
    for(int i=1;i<=n11;i++){
        int me=0;
        int rival=0;
        for(int j=11*(i-1);j<11*i;j++){
            if(in[j]=='W'){
                me++;
            }
            else if(in[j]=='L'){
                rival++;
            }
            else{
                break;
            }
        }
        cout<<me<<":"<<rival<<endl;
    }
    cout<<"\n";
    for(int i=1;i<=n21;i++){
        int me=0;
        int rival=0;
        for(int j=21*(i-1);j<21*i;j++){
            if(in[j]=='W'){
                me++;
            }
            else if(in[j]=='L'){
                rival++;
            }
            else{
                break;
            }
        }
        cout<<me<<":"<<rival<<endl;
    }
    return 0;
} 
int main(){
    char s;
    int me=0;
    int rival=0;
    string in;
    while(cin>>s){
        if(s=='E'){
            break;
        }
        in+=s;
    }
    for(char s:in){
        if(s=='W'){
            me++;
        }
        if(s=='L'){
            rival++;
        }
        if(max(me,rival)>=11&&abs(me-rival)>=2){
            cout<<me<<':'<<rival<<endl;
            me=0;
            rival=0;
        }
    }
    if(me!=0||rival!=0){
        cout<<me<<':'<<rival<<endl;
        me=0;
        rival=0;
    }
    cout<<"\n";
    for(char s:in){
        if(s=='W'){
            me++;
        }
        if(s=='L'){
            rival++;
        }
        if(max(me,rival)>=21&&abs(me-rival)>=2){
            cout<<me<<":"<<rival<<endl;
            me=0;
            rival=0;
        }
    }
    if(me!=0||rival!=0){
        cout<<me<<":"<<rival<<endl;
    }
    return 0;
}
struct hidos{
    int facing;
    string name;
};
int main(){
    int n,m,x=0;
    cin>>n>>m;
    vector<hidos> hido(n);
    for(int i=0;i<n;i++){
        cin>>hido[i].facing>>hido[i].name;
    }
    for(int i=0;i<m;i++){
        int director,distance;
        cin>>director>>distance;
        if(director==0){
            if(hido[x].facing){
                x+=distance;
                if(x>n-1){
                    x%=n;
                }
            }
            else{
                x-=distance;
                if(x<0){
                    x=n-abs(x)%n;
                }
            }
        }
        else{
            if(hido[x].facing){
                x-=distance;
                if(x<0){
                    x=n-abs(x)%n;
                }
            }
            else{
                x+=distance;
                if(x>n-1){
                    x%=n;
                }
            }
        }
    }
    cout<<hido[x].name;
    return 0;
}
vector<int> result;
void add(vector<int>& a,vector<int>& b){
    int carry=0;
    result.resize(max(a.size(),b.size()),0);
    if(a.size()<b.size()){
        a.resize(b.size(),0);
    }
    else{
        b.resize(a.size(),0);
    }
    for(int i=0;i<max(a.size(),b.size());i++){
        int temp=a[i]+b[i]+carry;
        result[i]=temp%10;
        carry=temp/10;
    }
    while(carry){
        result.push_back(carry%10);
        carry/=10;
    }
}
int main(){
    vector<int> a;
    vector<int> b;
    string sa;
    string sb;
    cin>>sa>>sb;
    reverse(sa.begin(),sa.end());
    reverse(sb.begin(),sb.end());
    for(char s:sa){
        a.push_back(s-'0'); 
    }
    for(char s:sb){
        b.push_back(s-'0');
    }
    add(a,b);
    reverse(result.begin(),result.end());
    for(auto it:result){
        cout<<it;
    }
    return 0;
}
vector<int> multip(vector<int>& a,vector<int>& b){
    int n = a.size();
    int m = b.size();
    vector<int> result(n + m, 0);
    for(int i=0;i<n;i++){
        int carry=0;
        for(int j=0;j<m;j++){
            int temp=a[i]*b[j]+result[i+j]+carry;
            result[i+j]=temp%10;
            carry=temp/10;
        }
        if(carry){
        result[m+i]+=carry;
        }
    }
    while (result.size() > 1 && result.back() == 0) {
        result.pop_back();
    }
    return result;

}
int main(){
    vector<int> a;
    vector<int> b;
    string sa;
    string sb;
    cin>>sa>>sb;
    reverse(sa.begin(),sa.end());
    reverse(sb.begin(),sb.end());
    for(char s:sa){
        a.push_back(s-'0'); 
    }
    for(char s:sb){
        b.push_back(s-'0');
    }
    vector<int> result=multip(a,b);
    reverse(result.begin(),result.end());
    for(auto it:result){
        cout<<it;
    }
    return 0;
}
int main(){
    int n,m;
    cin>>n>>m;
    int a[502][502];
    int temp[502][502];
    int temp1=1;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            a[i][j]=temp1++;
        }
    }
    for(int i=1;i<=m;i++){
        int x,y,r,z;
        cin>>x>>y>>r>>z;
        if(!r){
            continue;
        }
        for(int j=x-r;j<=x+r;j++){
            for(int k=y-r;k<=y+r;k++){
                temp[j-x+r][k-y+r]=a[j][k];
            }
        }
        if(z){
            for(int j=0;j<=2*r;j++){
                for(int k=0;k<=2*r;k++){
                    a[x+r-k][y-r+j]=temp[j][k];
                }
            }
        }
        else{
            for(int j=0;j<=2*r;j++){
                for(int k=0;k<=2*r;k++){
                    a[x-r+k][y+r-j]=temp[j][k];
                }
            }
        }
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            cout<<a[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}
int main(){
    char map[12][12];
    int xf,yf,xc,yc,ff=0,fc=0;
    for(int i=1;i<=10;i++){
        for(int j=1;j<=10;j++){
            cin>>map[i][j];
            if(map[i][j]=='F'){
                xf=i;
                yf=j;
            }
            if(map[i][j]=='C'){
                xc=i;
                yc=j;
            }
        }
    }
    int xf0=xf,yf0=yf,xc0=xc,yc0=yc,count=0,endf=0,endc=0;
    while(1){
        count++;
        if(count>10000){
            count=0;
            break;
        }
        if(ff%4==0){
            xf--;
            if(xf<1||xf>10||yf<1||yf>10||map[xf][yf]=='*'){
                ff++;
                xf++;
            }
        }
        else if(ff%4==1){
            yf++;
            if(xf<1||xf>10||yf<1||yf>10||map[xf][yf]=='*'){
                ff++;
                yf--;
            }
        }
        else if(ff%4==2){
            xf++;
            if(xf<1||xf>10||yf<1||yf>10||map[xf][yf]=='*'){
                ff++;
                xf--;
            }
        }
        else{
            yf--;
            if(xf<1||xf>10||yf<1||yf>10||map[xf][yf]=='*'){
                ff++;
                yf++;
            }
        }
        if(fc%4==0){
            xc--;
            if(xc<1||xc>10||yc<1||yc>10||map[xc][yc]=='*'){
                fc++;
                xc++;
            }
        }
        else if(fc%4==1){
            yc++;
            if(xc<1||xc>10||yc<1||yc>10||map[xc][yc]=='*'){
                fc++;
                yc--;
            }
        }
        else if(fc%4==2){
            xc++;
            if(xc<1||xc>10||yc<1||yc>10||map[xc][yc]=='*'){
                fc++;
                xc--;
            }
        }
        else{
            yc--;
            if(xc<1||xc>10||yc<1||yc>10||map[xc][yc]=='*'){
                fc++;
                yc++;
            }
        }
        if(xf==xf0&&yf==yf0&&ff%4==0){

            endf=1;
        }
        if(xc==xc0&&yc==yc0&&fc%4==0){
            endc=1;
        }
        if(endf&&endc){
            count=0;
            break;
        }
        if(xf==xc&&yf==yc){
            break;
        }
    }
    cout<<count;
    return 0;
}
int main(){
    int n;
    cin>>n;
    string num[n+1];
    for(int i=0;i<n+1;i++){
        cin>>num[i];
    }
    for(int i=0;i<n+1;i++){
        if(i==n&&i!=0){
            if(num[i][0]=='-'){
                cout<<num[i];
            }
            else{
                cout<<'+'<<num[i];
            }
            break;
        }
        if(num[i]=="0"){
            continue;
        }
        else{
            if(i==0){
                if(num[i][0]=='1'){
                    cout<<"x^"<<n-1;
                }
                else{
                    cout<<num[i]<<"x^"<<n-i;
                }
            }
            else{
                if(!(num[i][0]=='-')){
                    if(num[i][0]=='1'){
                        cout<<"+"<<"x^"<<n-i;
                    }
                    else{
                        cout<<"+"<<num[i]<<"x^"<<n-i;
                    }
                }
                else{
                    if(num[i][1]=='1'){
                        cout<<"-"<<"x^"<<n-i;
                    }
                    else{
                        cout<<num[i]<<"x^"<<n-i;
                    }    
                }
            }
        }
    }
    return 0;
}
int main(){
    int n;
    cin>>n;
    string a[n+1];
    string out;
    for(int i=0;i<n+1;i++){
        cin>>a[i];
    }
    for(int i=0;i<n+1;i++){
        if(a[i]=="0"){
            continue;
        }
        out=a[i];
        if(i==0){
            cout<<out;
            if(n-i>0){
                cout<<"x^"<<n-i;
            }
        }
    }
}

int main(){
    int n,a;
    cin>>n; 
    for(int i=n;i>=0;i--){
        cin>>a;
        if(a){
            if(i!=n&&a>0) cout<<"+";
            if(a<1) cout<<'-';
            if(abs(a)>1||i==0) cout<<abs(a);
            if(i>0) cout<<'x';
            if(i>1) cout<<'^'<<i;
        }
    }
    return 0;
}
    int main(){
    int p1,p2,p3;
    string s;
    cin>>p1>>p2>>p3>>s;
    for(int i=0;i<s.size();i++){
        if(s[i]=='-'){
            if(isdigit(s[i-1])&&isdigit(s[i+1])&&s[i+1]-s[i-1]>0||islower(s[i-1])&&islower(s[i+1])&&s[i+1]-s[i-1]>0){
                if(s[i+1]-s[i+1]==1){
                    s.erase(i);
                    continue;
                }
                string temp;
                s.erase(i);
                if(p1==1){
                    for(int j=1;j<=s[i+1]-s[i-1];j++){
                        char it=s[i-1]+j;
                        for(int k=0;k<p2*(s[i+1]-s[i-1]);k++){
                            temp.push_back(it);
                        }
                    }
                    if(p3==2){
                        reverse(temp.begin(),temp.end());
                    }
                s.insert(i,temp);
                }
                if(p1==2){
                    for(int j=1;j<=s[i+1]-s[i-1];j++){
                        char it=s[i-1]+j;
                        it=toupper(it);
                        for(int k=0;k<p2*(s[i+1]-s[i-1]);k++){
                            temp.push_back(it);
                        }
                    }
                    if(p3==2){
                        reverse(temp.begin(),temp.end());
                    }
                } 
                if(p1==3){
                    for(int j=1;j<=s[i+1]-s[i-1];j++){
                        char it='*';
                        for(int k=0;k<p2*(s[i+1]-s[i-1]);k++){
                            temp.push_back(it);
                        }
                    }
                    if(p3==2){
                        reverse(temp.begin(),temp.end());
                    }
                }
            s.insert(i,temp);
            }  
        }
    }
    cout<<s;
    return 0;
}
int main(){
    int p1,p2,p3;
    string s,result;
    cin>>p1>>p2>>p3>>s;
    for(int i=0;i<s.size();i++){
        result+=s[i];
        if(s[i]=='-') if(isdigit(s[i-1])&&isdigit(s[i+1])&&s[i+1]-s[i-1]>0||islower(s[i-1])&&islower(s[i+1])&&s[i+1]-s[i-1]>0){
            if(s[i+1]-s[i+1]==1){
                s.erase(i);
                continue;
            }
            result.pop_back();
            if(p3==1){
                for(char it=s[i-1]+1;it<s[i+1];it++){
                    char temp=it;
                    if(p1==1) temp=tolower(temp);
                    if(p1==2) temp=toupper(temp);
                    if(p1==3) temp='*';
                    for(int j=1;j<=p2;j++){
                        result+=temp;
                    }
                }
            }
            else{
                for(char it=s[i+1]-1;it>s[i-1];it--){
                    char temp=it;
                    if(p1==1) temp=tolower(temp);
                    if(p1==2) temp=toupper(temp);
                    if(p1==3) temp='*';
                    for(int j=1;j<=p2;j++){
                        result+=temp;
                    }
                }
            }
        }
    }
    cout<<result;
    return 0;
}
struct banhui{
    string name;
    string szhiwei;
    int zhiwei;
    int bangon;
    int denji;
    int sunxv;
};

bool abshi(const banhui& a,const banhui& b){
    if(a.bangon!=b.bangon) return a.bangon>b.bangon;
    else return a.sunxv<b.sunxv;
}

bool redou(const banhui& a,const banhui& b){
    if(a.zhiwei!=b.zhiwei) return a.zhiwei<b.zhiwei;
    else if(a.denji!=b.denji) return a.denji>b.denji;
    else return a.sunxv<b.sunxv;
}

bool banzu(const banhui& a,const banhui& b){
    if(a.zhiwei!=b.zhiwei) return a.zhiwei<b.zhiwei;
    else return a.sunxv<b.sunxv;
}

int main(){
    int n;
    cin>>n;
    vector<banhui> b(n);
    for(int i=0;i<n;i++){
        string temp;
        cin>>b[i].name>>temp>>b[i].bangon>>b[i].denji;
        b[i].sunxv=i;
        if(temp=="BangZhu") b[i].zhiwei=1;
        else if(temp=="FuBangZhu") b[i].zhiwei=2;
        else if(temp=="HuFa") b[i].zhiwei=3;
        else if(temp=="ZhangLao") b[i].zhiwei=4;
        else if(temp=="TangZhu") b[i].zhiwei=5;
        else if(temp=="JingYing") b[i].zhiwei=6;
        else b[i].zhiwei=7;
    }
    vector<banhui> leder;
    vector<banhui> follower;
    for(auto it:b){
        if(it.zhiwei==1||it.zhiwei==2) leder.push_back(it);
        else follower.push_back(it);
    }
    sort(leder.begin(),leder.end(),banzu);
    sort(follower.begin(),follower.end(),abshi);
    b.clear();
    for(auto it:leder){
        b.push_back(it);
    }
    for(auto it:follower){
        b.push_back(it);
    }
    int count=-1;
    for(auto it:b){
        count++;
        if(count<=4&&count>=3) b[count].zhiwei=3;
        if(count<=8&&count>=5) b[count].zhiwei=4;
        if(count<=15&&count>=9) b[count].zhiwei=5;
        if(count<=40&&count>=16) b[count].zhiwei=6;
        if(count>=41) b[count].zhiwei=7;
    }
    sort(b.begin(),b.end(),redou);
    int count1=-1;
    for(auto it:b){
        count1++;
        if(it.zhiwei==1) b[count1].szhiwei="BangZhu";
        else if(it.zhiwei==2) b[count1].szhiwei="FuBangZhu";
        else if(it.zhiwei==3) b[count1].szhiwei="HuFa";
        else if(it.zhiwei==4) b[count1].szhiwei="ZhangLao";
        else if(it.zhiwei==5) b[count1].szhiwei="TangZhu";
        else if(it.zhiwei==6) b[count1].szhiwei="JingYing";
        else b[count1].szhiwei="BangZhong";
    }
    for(auto it:b){
        cout<<it.name<<' '<<it.szhiwei<<' '<<it.denji<<endl;
    }
    return 0;
}
vector<int> multiply(vector<int>& a,int b){
    vector<int> result;
    int carry=0;
    for(int i=0;i<a.size();i++){
        int temp=a[i]*b+carry;
        carry=temp/10;
        result.push_back(temp%10);
    }
    while(carry){
        result.push_back(carry%10);
        carry/=10;
    }
    return result;
}
vector<int> factorial(int n){
    vector<int> temp;
    temp.push_back(1);
    if(n==0||n==1)  return temp;
    for(int i=2;i<=n;i++){
        temp=multiply(temp,i);
    }
    return temp;
}
int main(){
    int t;
    cin>>t;
    for(int i=1;i<=t;i++){
        int n,a;
        cin>>n>>a;
        vector<int> result;
        result=factorial(n);
        int count=0;
        for(int it:result) if(it==a) count++;
        cout<<count<<endl;
    }
    return 0;
}
int main(){
    int n;
    cin>>n;
    set<int> s;
    if(n<=4) cout<<n<<endl; cout<<n; return 0;
    int temp=n/2;
    int temp2=n-temp;
    s.insert(temp2);
    s.insert(temp);
    int size=s.size();
    while(*prev(s.end())>=5){
        temp=*prev(s.end())/2;
        temp2=n-temp;
        if(temp2==temp) temp++; temp2--;
        s.insert(temp2);
        s.insert(temp);
        if(s.size()==size) break;
        s.erase(prev(s.end()));
    }
    int sum=1;
    for(auto it:s){
        cout<<it<<' ';
        sum*=it;
    }
    cout<<endl;
    cout<<sum<<endl;
    return 0;
}
vector<int> multip(const vector<int>& a,int b){
    vector<int> result;
    int carry=0;
    for(int i=0;i<a.size();i++){
        int temp=a[i]*b+carry;
        carry=temp/10;
        result.push_back(temp%10);
    }
    while(carry){
        result.push_back(carry%10);
        carry/=10;
    }
    return result;
}

int main(){
    int n;
    cin>>n;
    int in=n;
    vector<int>temp;
    for(int i=2;i<n;i++){
        in-=i;
        if(in>=0){
            temp.push_back(i);
        }
        else{
            in+=i;
            break;
        }
    }
    int size=temp.size();
    int itemp=0;
    while(in){
        itemp++;
        if(size-itemp<0){
            itemp=1;
        }
        temp[size-itemp]++;
        in--;
    }
    vector<int> result;
    result.push_back(1);
    for(int it:temp){
        cout<<it<<' ';
        result=multip(result,it);
    }
    cout<<endl;
    reverse(result.begin(),result.end());
    for(auto it:result){
        cout<<it;
    }
    return 0;
}
vector<int> multip(vector<int>& a,int b){
    vector<int> result;
    int carry=0;
    for(int i=0;i<a.size();i++){
        int temp=a[i]*b+carry;
        carry=temp/10;
        result.push_back(temp%10);
    }
    while(carry){
        result.push_back(carry%10);
        carry/=10;
    }
    return result;
}

vector<int> subtuaction(vector<int>& a,int b){
    int borrow=0;
    vector<int> result;
    vector<int> vb;
    vb.push_back(b);
    vb.resize(a.size(),0);
    for(int i=0;i<a.size();i++){
        int temp=a[i]-vb[i]-borrow;
        if(temp<0){
            temp+=10;
            borrow=1;
        }
        else{
            borrow=0;
        }
        result.push_back(temp);
    }
    while(result.size()>0&&result.back()==0){
        result.pop_back();
    }
    return result;
}

int main(){
    int n;
    cin>>n;
    vector<int> result;
    result.push_back(2);
    for(int i=0;i<n-1;i++){
        result=multip(result,2);
    }
    result=subtuaction(result,1);
    int count=0;
    for(auto it:result){
        count++;
    }
    cout<<count<<endl;
    int count2=0;
    int count3=0;
    if(result.size()<=500){
        reverse(result.begin(),result.end());
        for(int i=0;i<10;i++){
            for(int j=0;j<50;j++){
                if(++count2<501-result.size()){
                    cout<<0;
                }
                else{
                    cout<<result[count3++];
                }
            }
            cout<<endl;
        }
    }
    else{
        vector<int> result500;
        for(int i=0;i<500;i++){
            result500.push_back(result[i]);
        }
        reverse(result500.begin(),result500.end());
        int count4=0;
        for(int i=0;i<10;i++){
            for(int j=0;j<50;j++){
                cout<<result500[count4++];
            }
            cout<<endl;
        }
    }
    return 0;
}
vector<int> multip(vector<int>& a,vector<int>& b){
    int carry=0;
    vector<int> result;
    result.resize(a.size()+b.size(),0);
    if(a.size()>b.size()) b.resize(a.size(),0);
    else a.resize(b.size(),0);
    for(int i=0;i<a.size();i++){
        for(int j=0;j<b.size();j++){
            result[i+j]+=a[i]*b[j];
            }
    }
    for(int i=0;i<result.size();i++){
        while(result[i]>9){
            result[i+1]+=result[i]/10;
            result[i]%=10;
        }
    }
    while(result.back()==0){
        result.pop_back();
    }
    return result;
}

int main(){
    int p;
    cin>>p;
    vector<int> dishu;
    vector<int> zhishu;
    vector<int> result;
    zhishu.push_back(p);
    dishu.push_back(2);
    result.push_back(1);
    while(p){
        if(p&1) result=multip(result,dishu);
        dishu=multip(dishu,dishu);
        p>>=1;
    }
    result[0]-=1;
    cout<<result.size()<<endl;
    int count2=0;
    int count3=0;
    if(result.size()<=500){
        reverse(result.begin(),result.end());
        for(int i=0;i<10;i++){
            for(int j=0;j<50;j++){
                if(++count2<501-result.size()){
                    cout<<0;
                }
                else{
                    cout<<result[count3++];
                }
            }
            cout<<endl;
        }
    }
    else{
        vector<int> result500;
        for(int i=0;i<500;i++){
            result500.push_back(result[i]);
        }
        reverse(result500.begin(),result500.end());
        int count4=0;
        for(int i=0;i<10;i++){
            for(int j=0;j<50;j++){
                cout<<result500[count4++];
            }
            cout<<endl;
        }
    }
    return 0;
}
int main(){
    int n,m;
    cin>>n>>m;
    multiset<int> s;
    for(int i=0;i<m;i++){
        int temp;
        cin>>temp;
        s.insert(temp);
    }
    for(auto it:s){
        cout<<it<<" ";
    }
    return 0;
}
int main(){
    int n;
    cin>>n;
    multiset<long long> a;
    for(int i=0;i<n;i++){
        long long t;
        cin>>t;
        a.insert(t);
    }
    int s=0;
    for(auto it:a){
        s++;
        if(s==a.size()) cout<<it<<endl;
        else cout<<it<<" "; 
    }
    return 0;
}
int main(){
    int n;
    cin>>n;
    int s[105];
    for(int i=0;i<n;i++){
        cin>>s[i];
    }
    set<int> t;
    for(int i=0;i<n;i++){
        t.insert(s[i]);
    }
    cout<<t.size()<<endl;
    for(auto it:t){
        cout<<it<<" ";
    }
    return 0;
}
int main(){
    int n,k,t;
    cin.tie(nullptr);
    ios::sync_with_stdio(false);
    int b=5000050;
    int r[b];
    cin>>n>>k;
    for(int i=0;i<n;i++){
        cin>>t;
        r[i]=t;
    }
    nth_element(r,r+k,r+n);
    cout<<r[k]<<endl;
    return 0;
}
struct student{
    int chinese;
    int math;
    int englishi;
    int id;
};

bool cmp(student& a,student& b){
    if(a.chinese+a.math+a.englishi!=b.chinese+b.math+b.englishi) return a.chinese+a.math+a.englishi>b.chinese+b.math+b.englishi;
    else if(a.chinese!=b.chinese) return a.chinese>b.chinese;
    else return a.id<b.id;
}

int main(){
    int n;
    cin>>n;
    student s[n];
    for(int i=0;i<n;i++){
        cin>>s[i].chinese>>s[i].math>>s[i].englishi;
        s[i].id=i+1;
    }
    sort(s,s+n,cmp);
    for(int i=0;i<5;i++){
        cout<<s[i].id<<" "<<s[i].chinese+s[i].math+s[i].englishi<<endl;
    }
    return 0;
}

struct pri{
    int order;
    string size;
};

int compare(string& a,string& b){
    int t=0;
    if(a.size()>b.size()) return 1;
    else if(a.size()<b.size()) return 0;
    for(int i=0;i<a.size();i++){
        if(a[i]!=b[i]){
            if(a[i]>b[i]) return 1;
            else return 0;
        } 
    }
    return 1;
}

bool cmp(pri& a,pri& b){
    if(compare(a.size,b.size)) return true;
    else return false;
}

int main(){
    int n;
    cin>>n;
    pri prizen[21];
    for(int i=0;i<n;i++){
        cin>>prizen[i].size;
        prizen[i].order=i+1;
    }
    sort(prizen,prizen+n,cmp);
    cout<<prizen[0].order<<endl;
    cout<<prizen[0].size<<endl;
    return 0;

}
bool cmp(int& a,int& b){
    return a>b;
}

int main(){
    int n,b;
    vector<int> s;
    cin>>n>>b;
    for(int i=0;i<n;i++){
        int t;
        cin>>t;
        s.push_back(t);
    }
    sort(s.begin(),s.end(),cmp);
    int count=0;
    int sum=0;
    for(int i=0;i<n;i++){
        sum+=s[i];
        if(sum<b){
            count++;
        }
    }
    cout<<count+1<<endl;
    return 0;
}
struct hido{
    int id;
    int grade;
};

bool cmp(hido& a,hido& b){
    if(a.grade!=b.grade) return a.grade>b.grade;
    else return a.id<b.id;
}
int main(){
    int n,m;
    cin>>n>>m;
    int mian=m*15/10;
    hido hido[n];
    for(int i=0;i<n;i++){
        cin>>hido[i].id>>hido[i].grade;
    }
    sort(hido,hido+n,cmp);
    int t,now,c=1,s=0;
    t=hido[0].grade;
    for(int i=mian-1;i<n;i++){
        if(hido[i].grade==hido[i+1].grade) mian++;
        else break;
    }
    cout<<hido[mian-1].grade<<" "<<mian<<endl;
    for(int i=0;i<mian;i++){
        cout<<hido[i].id<<" "<<hido[i].grade<<endl;
    }
    return 0;
}
struct student{
    string name;
    int year;
    int month;
    int day;
    int id;
};

bool cmp(student& a,student& b){
    if(a.year!=b.year) return a.year<b.year;
    else if(a.month!=b.month) return a.month<b.month;
    else if(a.day!=b.day) return a.day<b.day;
    else return a.id>b.id;
}

int main(){
    int n;
    cin>>n;
    student s[n];
    for(int i=0;i<n;i++){
        cin>>s[i].name>>s[i].year>>s[i].month>>s[i].day;
        s[i].id=i;
    }
    sort(s,s+n,cmp);
    for(int i=0;i<n;i++){
        cout<<s[i].name<<endl;
    }
    return 0;
}
bool cmp(string& a,string& b){
    return a+b>b+a;
}

int main(){
    int n;
    cin>>n;
    vector<string> s;
    for(int i=0;i<n;i++){
        string t;
        cin>>t;
        s.push_back(t);
    }
    sort(s.begin(),s.end(),cmp);
    for(auto it:s){
        cout<<it;
    }
    return 0;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n,q;
    map<pair<int,int>,int> mp;
    cin>>n>>q;
    for(int i=0;i<q;i++){
        int opration,x,y,k;
        cin>>opration;
        cin>>x>>y;
        if(opration==1){
            cin>>k;
            mp[{x,y}]=k;
        }
        else cout<<mp[{x,y}]<<endl;
    }
    return 0;
}
int main(){
    int n,m;
    cin>>n>>m;
    vector<int> a;
    for(int i=1;i<=n;i++){
        a.push_back(i);
    }
    int count=0;
    int count2=0;
    int pe=n;
    while(a.size()){
        count++;
        count2++;
        if(count2%m==0){
            cout<<count<<" ";
        }
    }
    return 0;
}
int main(){
    int n,m,k=0;
    cin>>n>>m;
    bool pe[101]={0};
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            k++;
            if(k>m) k=1;
            if(pe[k]==1){
                j--;
                k++;
                if(k>m) k=1;
            }
            if(j==m){
                cout<<k<<" ";
                pe[k]=1;
            }
        }
    }
    return 0;
}
int main(){
    int n,m;
    cin>>n>>m;
    bool pe[101]={0};
    int now=0,count=0,al=0;
    while(al<n){
        now=(now%n)+1;
        if(!pe[now]){
            count++;
            if(count==m){
                cout<<now<<" ";
                pe[now]=1;
                count=0;       
                al++;
            }
        }
    }
    return 0;
}

typedef struct Link{
    int id;
    struct Link* next;
    struct Link* prev;
}link;

int main(){
    int n,k,p;
    cin>>n;
    link* student[n+1]={nullptr};
    link* head=new link{1,nullptr,nullptr};
    student[1]=head;
    for(int i=2;i<=n;i++){
        cin>>k>>p;
        link* target=student[k];
        link* newlink=new link{i,nullptr,nullptr};
        if(p==1){
            newlink->prev=target;
            newlink->next=target->next;
            if(target->next!=nullptr) target->next->prev=newlink;
            target->next=newlink;
        }
        else{
            newlink->next=target;
            newlink->prev=target->prev;
            if(target->prev==nullptr){
                target->prev=newlink;
                head=newlink;
            }
            else{
                target->prev->next=newlink;
                newlink->prev=target->prev;
                target->prev=newlink;
            }
        }
        student[i]=newlink;
    }    
    int m,x;
    cin>>m;
    for(int i=1;i<=m;i++){
        cin>>x;
        if(student[x]==nullptr){
            continue;
        }
        if(student[x]->prev==nullptr){
            student[x]->next->prev=nullptr;
            head=student[x]->next;
        }
        else{
            student[x]->prev->next=student[x]->next;
            if(student[x]->next!=nullptr) student[x]->next->prev=student[x]->prev;
            else student[x]->prev->next=nullptr;
        }
        student[x]=nullptr;
    }
    link* now=head;
    while(now!=nullptr){
        cout<<now->id<<" ";
        now=now->next;
    }
    return 0;
}

int main() {
    int n,k,p;
    cin >> n;
    list<int> students;
    vector<list<int>::iterator> pos(n+1,students.end()); 
    students.push_back(1);
    pos[1] = students.begin();
    for(int i=2;i<=n;i++){
        cin>>k>>p;
        auto target=pos[k];
        if(p){
            auto newpos=students.insert(next(target),i);
            pos[i]=newpos;
        }
        else{
            auto newpos=students.insert(target,i);
            pos[i]=newpos;
        }
    }
    int m;
    cin>>m;
    for(int i=1;i<=m;i++){
        int x;
        cin>>x;
        if(pos[x]==students.end()){
            continue;
        }
        else{
            students.erase(pos[x]);
            pos[x]=students.end();
        }
    }
    for(auto it:students){
        cout<<it<<" ";
    }
    return 0;
}
int main(){
    int m,n,t;
    cin>>m>>n;
    queue<int> q;
    int count=0;
    for(int i=1;i<=n;i++){
        cin>>t;
        bool flag=1;
        queue<int> temp(q);
        while(!temp.empty()){
            int t2=temp.front();
            temp.pop();
            if(t2==t) {
                flag=0;
                break;
            }
        }
        if(flag){
            count++;
            if(q.size()<m) q.push(t);
            else{
                q.push(t);
                q.pop();
            }
        }
    }
    cout<<count<<endl;
    return 0;
}
int main(){
    int n;
    cin>>n;
    vector<int> s;
    int t[n+1]={0};
    for(int i=1;i<=n;i++){
        int k,start;
        cin>>t[i]>>k;
        start=t[1];
        for(int j=1;j<=k;j++){
            int t;
            cin>>t;
            s.push_back(t);
        }

    }
}
int main() {
    int n,ans=0;
    cin>>n;
    int country[100050]={0};
    struct pasenger{
        int country;
        int time;
    };
    queue<pasenger> q;
    for(int i=1;i<=n;i++){
        int t,n1;
        cin>>t>>n1;
        for(int j=1;j<=n1;j++){
            int tc;
            cin>>tc;
            q.push({tc,t});
            if(++country[tc]==1){
                ans++;
            }
        }
        while(!q.empty()){
            if(q.front().time+86400>t) break;
            else{
                if(--country[q.front().country]==0) ans--;
                q.pop(); 
            }
        }
        cout<<ans<<endl;
    }

    
    return 0;
}    
bool cmp(int a,int b){
        return a>b;
}

int main(){
    stack<char> l;
    stack<int> locationstact;
    vector<int> location;
    string s;
    cin>>s;
    int locationi=-1;
    
    for(char it:s){
        locationi++;
        if(it=='('||it=='['){
            l.push(it);
            locationstact.push(locationi);
        } 
        if(it==')'){
            if(l.empty()) location.push_back(locationi);
            else if(l.top()=='('){
                l.pop();
                locationstact.pop();
            }
            else location.push_back(locationi);
        }
        if(it==']'){
            if(l.empty()) location.push_back(locationi);
            else if(l.top()=='['){
                l.pop();
                locationstact.pop();
            }
            else location.push_back(locationi);
        }
    }
    while(!locationstact.empty()){
        int it=locationstact.top();
        location.push_back(it);
        locationstact.pop();
    }
    sort(location.begin(),location.end(),cmp);
    for(int it:location){
        if(s[it]==')') s.insert(it,"(");
        else if(s[it]==']') s.insert(it,"[");
        else if(s[it]=='(') s.insert(it+1,")");
        else if(s[it]=='[') s.insert(it+1,"]");
    }
    cout<<s<<endl;
    return 0;
}
int main(){
    int q;
    cin>>q;
    for(int i=0;i<q;i++){
        int n;
        bool f=0;
        cin>>n;
        stack<int> in;
        for(int i=1;i<=n;i++){
            int t;
            cin>>t;
            in.push(t);
        }
        for(int i=1;i<=n;i++){
            int t;
            cin>>t;
            if(t==in.top()){
                in.pop();
            }
            else{
                f=1;
                break;
            }
        }
        if(f==0) cout<<"Yes"<<endl;
        else cout<<"No"<<endl;
    }
    return 0;
}
    
int main(){
    int q;
    cin>>q;
    for(int i=1;i<=q;i++){
        int n;
        cin>>n;
        queue<int> in;
        stack<int> sin;
        for(int j=0;j<n;j++){
            int t;
            cin>>t;
            in.push(t);
        }
        queue<int> temp=in;
        bool flag=true;
        for(int j=0;j<n;j++){
            int t;
            cin>>t;
            if(sin.empty()){
                sin.push(temp.front());
                temp.pop();
            }
            while(t!=sin.top()){
                if(temp.empty()){
                    flag=false;
                    break;
                }
                sin.push(temp.front());
                temp.pop();
            }
            if(t==sin.top()){
                sin.pop();
            }
        }
        if(flag){
            cout<<"Yes"<<endl;
        }else{
            cout<<"No"<<endl;
        }
    }
}
int main(){
    int n,sum;
    cin>>n>>sum;
    multiset<int> s;
    s.insert(sum);
    for(int i=1;i<n;i++){
        int a;
        cin>>a;
        auto it=s.insert(a);
        if(it==prev(s.end())) sum+=abs(a-*prev(it));
        else if(it==s.begin()) sum+=abs(a-*next(it));
        else{
            int minin=min(abs(a-*prev(it)),abs(a-*next(it)));
            sum+=minin;
        }
    }
    cout<<sum<<endl;
    return 0;
}
struct num{
    int nums;
    int id;
    bool operator==(int x)const{
        return nums==x;
    }
    bool operator<(int x)const{
        return nums<x;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int n,m;
    cin>>n>>m;
    vector<num> a;
    for(int i=1;i<=n;i++){
        int t;
        cin>>t;
        a.push_back({t,i});
    }
    for(int i=1;i<=m;i++){
        int t;
        cin>>t;
        auto it=lower_bound(a.begin(),a.end(),t);
        if(it!=a.end()){
            if(*it==t) cout<<it->id<<" ";
            else cout<<-1<<" ";
        } 
        else cout<<-1<<" ";
    }
    return 0;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int n,c;
    cin>>n>>c;
    multiset<int> s;
    for(int i=0;i<n;i++){
        int t;
        cin>>t;
        s.insert(t);
    }
    auto it=lower_bound(s.begin(),s.end(),c);
    auto it2=lower_bound(s.begin(),s.end(),*it-c);
    int ans=0;
    while(it!=s.end()){
        int cnt=0;
        while(*it-*it2>c) it2=next(it2);
        while(*it-*it2==c){
        ans++;
        cnt++;
        it2=next(it2);
        }
        advance(it2,-cnt);
        it=next(it);
    }
    cout<<ans<<endl;
    return 0;
}
int main(){
    int n,c;
    int a[200001]={0};
    cin >> n >> c;
    map<int,int> mp;
    int cnt=0;
    for(int i=0;i<n;i++){
        cin>>a[i];
        mp[a[i]]++;
        a[i]-=c;
    }
    for(int i=0;i<n;i++){
        cnt+=mp[a[i]];
    }
    cout << cnt << endl;
    return 0;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int n,m,longest;
    ll ans=0;
    cin>>n>>m;
    int a[n]={0};
    for(int i=0;i<n;i++){
        cin>>a[i];
        longest=max(longest,a[i]);
    }
    int h=longest/2;
    while(ans!=m){
        ans=0;
        for(int i=0;i<n;i++){
            if(a[i]>h) ans+=a[i]-h;
        }
        if(ans<m) h/=2;
        else if(ans>m) h=3*h/2;
    }
    cout<<h;
    return 0;
}
int main() {
    ll n,m,longest=0;
    cin >> n >> m;
    ll a[n];
    for(int i=0;i<n;i++){
        cin >> a[i];
        longest=max(a[i],longest);
    }
    ll left,right,mid,result;
    left=0;
    right=longest;
    while(left<=right){
        mid=(left+right)>>1;
        ll count=0;
        for(int i=0;i<n;i++){
            if(a[i]>=mid){
                count+=a[i]-mid;
            }
        }
        if(count>=m){
            left=mid+1;
            result=mid;
        }else{
            right=mid-1;
        }
    }
    cout<<result;
    return 0;
}
double a,b,c,d;

double f(double x){
    return a*x*x*x+b*x*x+c*x+d;
}

int main(){
    cin>>a>>b>>c>>d;
    int count=0;
    for(int i=-100;i<100;i++){
        double l=i,m;
        double r=l+1;
        double x1=f(l);
        double x2=f(r);
        if(!x1){
            printf("%.2f ",l);
            count++;
        }
        if(x1*x2<0){
            while(r-l>=0.001){
                m=(l+r)/2;
                if(f(m)*f(r)<=0) l=m;
                else r=m;
            }
            printf("%.2f ",r);
            count++;
        }
        if(count==3) break;
    }
    return 0;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    int m,n;
    ll result=0;
    cin >> m >> n;
    multiset<int> sch;
    for(int i=1;i<=m;i++){
        int x;
        cin >> x;
        sch.insert(x);
    }
    for(int i=1;i<=n;i++){
        int x;
        cin >> x;
        int t;
        if(lower_bound(sch.begin(),sch.end(),x)==sch.begin()){
            t=abs(x-*sch.begin());
        }
        else if(lower_bound(sch.begin(),sch.end(),x)==sch.end()){
            t=abs(x-*(prev(sch.end())));
        }
        else{
            t=min(abs(x-*lower_bound(sch.begin(),sch.end(),x)),abs(x-*(prev(lower_bound(sch.begin(),sch.end(),x)))));
        }
        result+=t;
    }
    cout << result << endl;
    return 0;

}

int main(){
    int m, n;
    ll result=0;
    cin >> m >> n;
    int a[m];
    for(int i = 0; i < m; i++){
        cin>>a[i];
    }
    sort(a, a+m);
    for(int i = 0; i < n; i++){
        int t;
        cin>>t;
        int p=lower_bound(a, a+m, t)-a;
        if(p==m){
            result+=abs(t-a[m-1]);
        }
        else if(p==0){
            result+=abs(t-a[0]);
            
        }
        else result+=min(abs(t-a[p]), abs(t-a[p-1]));
    }    
    cout<<result<<endl;
    return 0;
}
int main() {
    ll n,k,ans=0,result;
    cin >> n >> k;
    int tr[n];
    for(int i=0;i<n;i++){
        cin >> tr[i];
    }
    sort(tr,tr+n);
    int l,r,m;
    l=0;
    r=tr[n-1];
    while(l<=r){
        m=(l+r)/2;
        if(!m){
            cout<<0;
            return 0;
        }
        for(int i=0;i<n;i++){
            ans+=tr[i]/m;
        }
        if(ans>=k){
            result=m;
            l=m+1;
        }
        else {
            r=m-1;
        }
        ans=0;
    }
    cout << result << endl;
    return 0;
}
int main() {
    int l,le,r,n,m,mid,result;
    cin >> le >> n >> m;
    l=1;
    r=le;
    int a[n+2];
    a[0]=0;
    a[n+1]=le;
    for(int i=1;i<=n;i++) cin>>a[i];
    while(l<=r){
        int ans=0;
        mid=(l+r)/2;
        int now=0;
        for(int i=1;i<=n+1;i++){
            if(a[i]-a[now]<mid) {
                ans++;
            }
            else{
                now=i;
            }
        }
        if(ans>m) r=mid-1;
        else {
            result=mid;
            l=mid+1;
        }
    }
    cout<<result;
    return 0;
}
int main(){
    int le,n,k,l,r,ans=0;
    cin>>le>>n>>k;
    l=1;
    r=le;
    int a[n];
    for(int i=0;i<n;i++) cin>>a[i];
    while(l<=r){
        int mid=(l+r)/2;
        int cnt=0;
        int now=0;
        for(int i=1;i<n;i++){
            int b=1;
            int distance=a[i]-a[i-1];
            if(distance>mid){
                cnt+=(distance-1)/mid;
            }
        }
        if(cnt<=k){
            ans=mid;
            r=mid-1;
        }
        else l=mid+1;
    }
    cout<<ans<<endl;
    return 0;
}
int main() {
    int n, m;
    ll sum=0;
    ll maxin=0;
    cin >> n >> m;
    ll a[100000]={0},result;
    for(int i = 0; i < n; i++){
        cin >> a[i];
        maxin=max(maxin, a[i]);
        sum += a[i];
    }
    ll l,r,mid;
    l=maxin;
    r=sum;
    while(l<=r){
        mid=(l+r)/2;
        int cnt=1;
        ll tmp=0;
        int now=0;
        for(int i = 0; i < n; i++){
            if(tmp+a[i]<=mid){
                tmp+=a[i];
            }
            else{
                cnt++;
                tmp=a[i];
            }
        }
        if(cnt<=m){
            result=mid;
            r=mid-1;
        }
        else l=mid+1;
    }
    cout<<result<<endl;
    return 0;
}
int main(){
    double w0,w,m,t;
    cin >> w0 >> w >> m;
    double r=310,l=0,mid,result;
    while(l<r-0.0001){
        mid=(l+r)/2;
        double w1=w0;
        for(int i=1;i<=m;i++){
            w1 = w1 - w + w1 * (mid/100);
        }
        if(w1>0.0001){
            r=mid;
        }
        else{
            result=mid;
            l=mid;
        }
    }
    printf("%.1lf",round(result*10)/10);
    return 0;
}
int main(){
    string a,b;
    cin >> a >> b;
    cout<<a[1]<<b[0]<<a[0]<<b[1]<<endl;
    return 0;
}

int main(){
    cout<<'M'<<endl;
    cout<<"MMM"<<endl;
    cout<<"MMMMM"<<endl;
    cout<<"MMM"<<endl;
    cout<<"M"<<endl;
    return 0;
}
int main(){
    int a=5,b=4,c=3,d=0,e,f,g;
    e=a>b>c;
    f=a&&b||c;
    g=c&&d&&a++;
    cout<<"a="<<a<<",e="<<e<<",f="<<f<<",g="<<g<<endl;
    return 0;
}
int sum(int x,int y){
    return x+y;
}

int main(){
    int a,b,c;
    cin>>a>>b;
    c=sum(a,b);
    cout<<a<<"+"<<b<<"="<<c<<endl;
    return 0;
}
int main(){
    int n,p;
    cin>>n>>p;
    double a[n+1],b[n+1];
    double t=0;
    for(int i=1;i<=n;i++){
        cin>>a[i]>>b[i]; 
        t+=a[i];
    }
    if(t<=p){
        cout<<-1<<endl;
        return 0;
    } 
    double l,r,mid;
    l=0;
    r=1e10;

    while(r-l>1e-6){
        double sum=0;
        mid=(l+r)/2;
        for(int i=1;i<=n;i++){
            if(a[i]*mid<=b[i]){
                continue;
            }
            else{
                sum+=mid*a[i]-b[i];
            }
        }
        if(sum<=p*mid){
            l=mid;
        }
        else r=mid;
    }
    cout<<fixed<<setprecision(10)<<l<<endl;
    return 0;
}
struct county{
    int id;
    int grade;
};

bool cmp(const county& a, const county& b){
    return a.grade<b.grade;
}

int main(){
    int n;
    cin>>n;
    int a=pow(2,n);
    county arr[a+1];
    for(int i=1;i<=a;i++){
        cin>>arr[i].grade;
        arr[i].id=i;
    }
    sort(arr+1,arr+a/2+1,cmp);
    sort(arr+a/2+1,arr+a+1,cmp);
    if(arr[a/2].grade>arr[a].grade){
        cout<<arr[a].id<<endl;
    }
    else cout<<arr[a/2].id<<endl;
    return 0;
}
struct node{
    int left=0;
    int right=0;
};

const int sizein=1e6+10;
int result=0;
node tree[sizein];

void read(int i,int deep){
    deep++;
    result=max(result,deep);
    if(tree[i].left==0&&tree[i].right==0) return;
    read(tree[i].left,deep);
    read(tree[i].right,deep);
}

int main(){
    int n;
    cin>>n;
    for(int i=1;i<n;i++){
        cin>>tree[i].left>>tree[i].right;
    }
    read(1,0);
    cout<<result<<endl;
    return 0;
}
void work(string front, string mid){
    if(front.empty()) return;
    char o=front[0];
    front.erase(0,1);
    int p=mid.find(o);
    string lfront=front.substr(0,p);
    string rfront=front.substr(p);
    string lmid=mid.substr(0,p);
    string rmid=mid.substr(p+1);
    work(lfront,lmid);
    work(rfront,rmid);
    cout<<o;
}

int main() {
    string front, mid;
    cin >> mid >> front;
    work(front, mid);
    cout<<'\n';
    return 0;
}
const int treenum=1e6+10,INT=0x7fffffff;
int cnt=0;

struct node{
    int val,ls,rs,siz;
}tree[treenum];

void init() {
    for (int i = 0; i <= treenum; i++) {
        tree[i] = {0, 0, 0, 0};
    }
}

void add(int x, int v){
    tree[x].siz++;
    if(cnt==0){
        tree[1]={v,0,0,1};
        cnt++;
        return;
    }
    if(tree[x].val>v){
        if(tree[x].ls==0){
            tree[x].ls=++cnt;
            tree[cnt]={v,0,0,1};
        }
        else{
            add(tree[x].ls,v);
        }
    }
    else{
        if(tree[x].rs==0){
            tree[x].rs=++cnt;
            tree[cnt]={v,0,0,1};
        }
        else{
            add(tree[x].rs,v);
        }
    }
}

int findfront(int x,int v,int ans){
    if(!x) return ans;
    if(tree[x].val>=v){
        return findfront(tree[x].ls,v,ans);
    }
    else{
        ans=max(ans,tree[x].val);
        return findfront(tree[x].rs,v,ans);
    }
    return ans;
}

int findback(int x,int v,int ans){
    if(!x) return ans;
    if(tree[x].val>v){
        ans=min(ans,tree[x].val);
        return findback(tree[x].ls,v,ans);
    }
    else{
            return findback(tree[x].rs,v,ans);
    }
    return ans;
}

int findrank(int x,int v){
    if(!x) return 0;
    if(tree[x].val>v){
        return findrank(tree[x].ls,v);
    }
    else if(tree[x].val<v){
        return tree[tree[x].ls].siz+1+findrank(tree[x].rs,v);
    }
    else{
        return tree[tree[x].ls].siz;
    }
    return 0;
}

int findvalue(int x,int rank){
    if(!x) return INT;
    if(tree[tree[x].ls].siz+1>rank){
        return findvalue(tree[x].ls,rank);
    }
    else if(tree[tree[x].ls].siz+1==rank){
        return tree[x].val;
    }
    else{
        return findvalue(tree[x].rs,rank-tree[tree[x].ls].siz-1);
    }
    return INT;
}

int main() {
    int q;
    cin>>q;
    for(int i=0;i<q;i++){
        int op,x;
        cin>>op>>x;
        switch(op){
            case 1:cout<<findrank(1,x)+1<<endl; break; 
            case 2:cout<<findvalue(1,x)<<endl; break;
            case 3:cout<<findfront(1,x,-INT)<<endl; break;
            case 4:cout<<findback(1,x,INT)<<endl; break;
            case 5:add(1,x); break;
        }
    }
}
int main(){
    int n,m;
    ll cansum=0,fansum=0;
    cin>>n>>m;
    int shortin=min(n,m);
    for(int i=1;i<=shortin;i++){
        fansum+=(n-i+1)*(m-i+1);
    }
    cout<<fansum<<" ";
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            cansum+=(n-i+1)*(m-j+1);
        }
    }
    cout<<cansum-fansum;
    return 0;
}

int main(){
    int n,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,sum=0;
    cin>>n;
    for(a1=1;a1<=3;a1++){
        for(a2=1;a2<=3;a2++){
            for(a3=1;a3<=3;a3++){
                for(a4=1;a4<=3;a4++){
                    for(a5=1;a5<=3;a5++){
                        for(a6=1;a6<=3;a6++){
                            for(a7=1;a7<=3;a7++){
                                for(a8=1;a8<=3;a8++){
                                    for(a9=1;a9<=3;a9++){
                                        for(a10=1;a10<=3;a10++){
                                            if(a1+a2+a3+a4+a5+a6+a7+a8+a9+a10==n) sum++;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    cout<<sum<<endl;
    for(a1=1;a1<=3;a1++){
        for(a2=1;a2<=3;a2++){
            for(a3=1;a3<=3;a3++){
                for(a4=1;a4<=3;a4++){
                    for(a5=1;a5<=3;a5++){
                        for(a6=1;a6<=3;a6++){
                            for(a7=1;a7<=3;a7++){
                                for(a8=1;a8<=3;a8++){
                                    for(a9=1;a9<=3;a9++){
                                        for(a10=1;a10<=3;a10++){
                                            if(a1+a2+a3+a4+a5+a6+a7+a8+a9+a10==n){
                                                cout<<a1<<" "<<a2<<" "<<a3<<" "<<a4<<" "<<a5<<" "<<a6<<" "<<a7<<" "<<a8<<" "<<a9<<" "<<a10<<endl;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return 0;
}
int main(){
    double a,b,c;
    
    bool flag=false;
    cin>>a>>b>>c;
    if(!a){
        cout<<"No!!!"<<endl;
        return 0;
    }
    double aa,bb,cc;
    int aaa,bbb,ccc;
    for(int i=123;i<=987;i++){
        bool t=0;
        aa=i;  
        bb=(b/a)*aa;
        cc=(c/a)*aa;
        aaa=aa;
        bbb=bb;
        ccc=cc;
        if(bb>987||cc>987) continue;
        int num[10]={0};
        for(int j=1;j<=3;j++){
            num[aaa%10]++;
            aaa/=10;
            num[bbb%10]++;
            bbb/=10;
            num[ccc%10]++;
            ccc/=10;
        }
        for(int i=1;i<=9;i++){
            if(num[i]>1||num[0]>0){
                t=1;
            }
        }
        if(t) continue;
        else{
            flag=true;
            cout<<aa<<" "<<bb<<" "<<cc<<endl;
        }
    }
    if(!flag){
        cout<<"No!!!"<<endl;
    }
    return 0;
}

int a[25]={0},k,ans=0,n;

bool isprime(int x){
    if(x<4){
        return x>1;
    }
    else if(x%6!=1&&x%6!=5){
        return false;
    }
    for(int i=5;i*i<=x;i+=6){
        if(x%i==0||x%(i+2)==0){
            return false;
        }
    }
    return true;
}

void dfs(int start,int count,int curentsum){
    if(count==k){
        if(isprime(curentsum)){
            ans++;
        }
        return;
    }
    if(start>=n) return;
    for(int i=start;i<n;i++){
        dfs(i+1,count+1,curentsum+a[i]);
    }
    return;
}

int main(){
    cin>>n>>k;
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    dfs(0,0,0);
    cout<<ans<<endl;
    return 0;
}

bool cmp(int a,int b){
    return a>b;
}

int main(){
    int n;
    cin>>n;
    for(int i=1;i<=n;i++){
        int t;
        cin>>t;
        int a[2*t];
        ll nailon=0,ren=0;
        for(int j=0;j<2*t;j++){
            cin>>a[j];
        }
        sort(a,a+2*t,cmp);
        nailon+=a[0];
        for(int j=1;j<2*t;j++){
            if(pow(-1,((j+1)/2))==-1){
                ren+=a[j];
            }
            else nailon+=a[j];
        }
        cout<<nailon<<"\n";
        if(nailon>=ren) cout<<"Yes"<<"\n";
        else cout<<"No"<<"\n";
    }
    return 0;
}                  
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n,q;
    cin>>n>>q;
    int a[n+1]={0};
    int aqian[n+1]={0};
    for(int i=1;i<=n;i++){
        cin>>a[i];
        aqian[i]=aqian[i-1]^a[i];
    } 
    for(int i=0;i<q;i++){
        int l,r;
        cin>>l>>r;
        int t=aqian[r]^aqian[l-1];
        cout<<t<<endl;
    }
    return 0;
}

int main(){
    int l,r,now=5,cnt=0;
    cin>>l>>r;
    if(2>=l&&2<=r) cnt++;
    if(3>=l&&3<=r) cnt++;
    while(now<l){
        now+=6;
    }
    if(now>r){
        cout<<cnt;
        return 0;
    }
    for(int i=now;i<=r;i+=6){
        bool flag=1;
        for(int j=5;j*j<=i;j+=6){
            if(i%j==0||i%(j+2)==0) flag=0;
        }
        if(flag) cnt++;
    }
    for(int i=now+2;i<=r;i+=6){
        bool flag=1;
        for(int j=5;j*j<=i;j+=6){
            if(i%j==0||i%(j+2)==0) flag=0;
        }
        if(flag) cnt++;
    }
    cout<<cnt<<endl;
    return 0;
}
bool prime(int n){
    if(n<=3){
        return n>1;
    }
    if(n%6!=1&&n%6!=5) return false;
    int a=sqrt(n);
    for(int i=5;i<=a;i+=6){
        if(n%i==0||n%(i+2)==0) return false;
    }
    return true;
}

int main(){
    int l,r,cnt=0;
    cin>>l>>r;
    for(int i=l;i<=r;i++){
        if(prime(i)) cnt++;
    }
    cout<<cnt<<endl;
    return 0;
}
int gcd(int a,int b){
    if(b==0) return a;
    return gcd(b,a%b);
}

int main(){
    int n,q;
    cin>>n>>q;
    int siz=n+10;
    int a[siz]={0};
    for(int i=1;i<=n;i++) cin>>a[i];
    for(int i=0;i<q;i++){
        int l,r;
        cin>>l>>r;
        int t=a[l];
        for(int j=l+1;j<=r;j++){
            t=gcd(t,a[j]);
        }
        cout<<t<<endl;
    }
    return 0;
}
int main(){
    ll n;
    cin>>n;
    if(n==1){
        cout<<4.5<<endl;
        return 0;
    }
    ll a= n/3;
    int b=n%3;
    ll price=10*a;
    if(b==1){
        price+=4;
    }
    else if(b==2){
        price+=7;
    }
    double dprice=price;
    printf("%.1f\n",dprice);
    return 0;
}
int main(){
    int t;
    cin>>t;
    while(t--){
        int n,l,r;
        string s,result,s1,s2;
        cin>>n>>s;
        bool flag=1;
        while(flag){
            int cnt=0;
            for(int i=0;i<s.size()-1;i++){
                if(s[i]=='A'&&s[i+1]=='B'){
                    if(s.size()==2){
                        s.clear();
                        cnt=0;
                        break;
                    }
                    s1=s.substr(0,i);
                    s2=s.substr(i+2);
                    s=s1+s2;
                    i--;
                    cnt++;
                }
                else if(s[i]=='B'&&s[i+1]=='B'){
                    if(s.size()==2){
                        s.clear();
                        cnt=0;
                        break;
                    }
                    s1=s.substr(0,i);
                    s2=s.substr(i+2);
                    s=s1+s2;
                    i--
                    cnt++;
                }
            }
            if(cnt==0){
                flag=0;
            }
        }
        cout<<s.size()<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        string s;
        cin>>n>>s;
        int b=0;
        int a=0;
        for(int i=n-1;i>=0;i--){
            if(s[i]=='B') b++;
            if(s[i]=='A'){
                if(b>0){
                    b--;
                }
                else a++;
            }
        }
        cout<<a+b%2<<endl;
    }
    return 0;
}
            
int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        string s;
        cin>>s;
        stack<char> l;
        for(char c:s){
            if(!l.empty()){
                if((l.top()=='A'&&c=='B')||(l.top()=='B'&&c=='B')){
                    l.pop();
                    continue;
                } 
            }
            l.push(c);
        }
        cout<<l.size()<<endl;
    }
    return 0;
}

bool cmp(int a,int b){
    return a>b;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,le;
        cin>>n>>le;
        int c[siz]={0};
        int qc[siz]={0};
        int maxin=0;
        for(int i=1;i<=n;i++){
            cin>>c[i];
            maxin=max(maxin,c[i]);
        }
        if(maxin==0&&le==0){
            cout<<0<<endl;
            continue;
        }
        sort(c+1,c+n+1,cmp);
        int l=1,r=n,mid,result;
        while(l<=r){
            mid=(l+r)/2;
            int minin=min(c[mid-le],c[mid]+1);
            if(minin>=mid){
                result=mid;
                l=mid+1;
            }
            else r=mid-1;
        }
        cout<<result<<endl;
    }
    return 0;
}
// a
int main(){
    int t;
    cin>>t;
    for(int j=1;j<=t;j++){
        int n;
        bool flag=0;
        cin>>n;
        int a[101]={0};
        for(int i=1;i<=n;i++){
            int t;
            cin>>t;
            a[t]++;
            if(a[t]>=2){
                flag=1;
            }
        }
        if(!flag) cout<<"no"<<endl;
        else cout<<"yes"<<endl;
    }
    return 0;
}
// b
int main(){
    ll n,m,x;
    cin>>n>>m>>x;
    ll out=pow(2,n-m+1)+1;
    cout<<out-x<<endl;
    return 0;
}
// c
int main(){
    int t;
    cin>>t;
    while(t--){
        int x,y,n;
        cin>>x>>y>>n;
        int minin=min(x-1,n);
        cout<<minin<<endl;
    }
    return 0;
}
// d
int main(){
    ll n,ans=0,cnt=0;
    cin>>n;
    for(int i=1;i<=n;i++){
        int t=i;
        while(t%5==0){
            cnt++;
            t/=5;
        }
        ans+=cnt;
    }
    cout<<ans<<endl;
    return 0;
}

bool prime(ll x){
    if(x<=3) return x>1;
    if(x%6!=1&&x%6!=5) return false;
    ll a=sqrt(x);
    for(ll i=5;i<=a;i+=6) if(x%i==0||x%(i+2)==0) return false;
    return true;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        bool a=1;
        ll x;
        cin>>x;
        for(int i=1;i<x;i++){
            if((i^x) >= 2 && !prime(i^x)){
                cout<<i<<endl;
                a=0;
                break;
            }
        }
        if(a) cout<<-1<<endl;
    }
    return 0;
}

int main(){
    int n;
    cin>>n;
    if(n==1){
        cout<<-1<<endl;
    }
    else cout<<floor((log(n)/log(2)))+1<<endl;
    return 0;
}

int main(){
    string l,temp;
    int st;
    cin>>l>>st;
    for(auto it:l){
        int t=st+it-'A';
        temp+=to_string(t);
    }
    while(temp.size()>2){
        if((temp[0]=='1'&&temp[1]=='0'&&temp[2]=='0')&&temp.size()==3) break;
        string temp2=temp;
        for(int i=1;i<=temp.size()-1;i++){
            temp[i]=(temp2[i-1]-'0'+temp2[i]-'0')%10+'0';
        }
        temp.erase(0,1);
    }
    if(temp.size()==3) cout<<100<<endl;
    else if(temp[0]=='0') cout<<temp[1]-'0'<<endl;
    else cout<<temp[0]-'0'<<temp[1]-'0'<<endl;
    return 0;
}

struct train{
    int up;
    int ans;
};

int main(){
    int a,n,m,x;
    cin>>a>>n>>m>>x;
    if(x<=2){
        cout<<a<<endl;
        return 0;
    }
    int l,r,mid,result;
    l=0;
    r=2e4;
    train huo[25];
    huo[1]={a,a};
    while(l<=r){
        mid=(l+r)/2;
        huo[2]={mid,a};
        for(int i=3;i<=n;i++){
            if(i==n){
                huo[i]={0,huo[i-1].ans};
            }
            else{
                huo[i].up=huo[i-2].up+huo[i-1].up;
                huo[i].ans=huo[i-1].ans+huo[i-2].up;
            }
        }
        if(huo[n].ans>=m){
            result=mid;
            r=mid-1;
        }
        else{
            l=mid+1;
        }
    }
    huo[2]={result,a};
    for(int i=3;i<=n;i++){
        if(i==n){
            huo[i]={0,huo[i-1].ans};
        }
        else{
            huo[i].up=huo[i-2].up+huo[i-1].up;
            huo[i].ans=huo[i-1].ans+huo[i-2].up;
        }
    }
    if(x==n){
        cout<<0<<endl;
    }
    else{
        cout<<huo[x].ans<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        set<int> a;
        for(int i=1;i<=n;i++){
            int t;
            cin>>t;
            a.insert(t);
        }
        cout<<2*a.size()-1<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,m,su=0;
        cin>>n>>m;
        if(n==1){
            int t;
            for(int i=0;i<m;i++) cin>>t;
            cout<<1<<endl;
            continue;
        }
        int a[n+1][m+1]={0};
        bool flag=0;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                cin>>a[i][j];
            }
            sort(a[i],a[i]+m);
            for(int j=0;j<m-1;j++){
                if(a[i][j+1]-a[i][j]<n){
                    flag=1;
                }
            }
        }
        if(flag){
            cout<<-1;
        }
        else{
            for(int i=0;i<n;i++){
                 for(int j=0;j<n;j++){
                    if(a[j][0]==i){
                        cout<<j+1<<" ";
                    }
                 }
            }
        }
        cout<<endl;
    }
    return 0;
}

int a[siz]={0},sum=0,n=0,k;

void dfs(int x,int ans,int cnt,int k){
    if(x>n) return;
    if(cnt==2){
        if(ans==k) sum++;
        return;
    }
    for(int i=x;i<=n;i++) dfs(i+1,ans+a[i+1],cnt+1,k);
    return;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        sum=0;
        cin>>n>>k;
        for(int i=1;i<=n;i++) cin>>a[i];
        dfs(0,0,0,k);
        cout<<endl;
        cout<<sum<<endl;
        cout<<endl;
    }
}
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int siz=2e5+10;

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,k,ans=0;
        cin>>n>>k;
        list<int> a;
        for(int i=0;i<n;i++){
            int t;
            cin>>t;
            a.push_back(t);
        }
        while(!a.empty()){
            int ain=*a.begin();
            a.erase(a.begin());
            for(auto it=a.begin();it!=a.end();it++){
                if(ain+*it==k){
                    ans++;
                    a.erase(it);
                    break;
                }
            }
        }
        cout<<ans<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,k,ans=0;
        cin>>n>>k;
        map<int,int> mp;
        for(int i=0;i<n;i++){
            int t;
            cin>>t;
            mp[t]++;
        }
        for(auto it=mp.begin();it!=mp.end();it++){
            if(mp[k-(it->first)]>0){
                if((k-(it->first))==(it->first)){
                    int t=floor(it->second/2.0);
                    ans+=t;
                    it->second-=(2*t);
                }
                else{
                    int t=min(it->second,mp[k-(it->first)]);
                    ans+=t;
                    mp[k-(it->first)]-=t;
                    mp[it->first]-=t;
                }
            }
        }
        cout<<ans<<endl;
    }
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,k;
        cin>>n>>k;
        if(n*n-k==1){
            cout<<"no"<<endl;
            continue;
        }
        cout<<"yes"<<endl;
        int a=(n*n)-k;
        int cnt=0;
        for(int i=1;i<=n;i++){
            for(int j=1;j<=n;j++){
                if(cnt==0&&i==1&&cnt<=a-1){
                    cout<<'R';
                    cnt++;
                }
                else if(i==1&&cnt<=a-1){
                    cout<<"L";
                    cnt++;
                }
                else if(i!=1&&cnt<=a-1){
                    cout<<"U";
                    cnt++;
                }
                else cout<<'D';
            }
            cout<<endl;
        }
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,m,ans=0,flag=1;
        cin>>n>>m;
        string x,s;
        cin>>x>>s;
        if(x.find(s)!=string::npos){
            cout<<0<<endl;
            continue;
        }
        while(n<26*m){
            x+=x;
            ans++;
            n*=2;
            int t=0;
            if(n>=m){
                if(x.find(s)!=string::npos){
                    cout<<ans<<endl;
                    flag=0;
                    t=1;
                }
            }
            if(t) break;
        }
        if(x.find(s)!=string::npos&&flag){
            cout<<ans<<endl;
            flag=0;
            break;
        }
        if(flag){
            cout<<-1<<endl;
        }
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int x,y;
        cin>>x>>y;
        if(x<y) cout<<2<<endl;
        else if(x==y) cout<<-1<<endl;
        else{
            if(y==1) cout<<-1<<endl;
            else if(x-y==1) cout<<-1<<endl;
            else cout<<3<<endl;
        }
    }
    return 0;
}

struct city{
    ll x,y;
};

int main(){
    int t;
    cin>>t;
    while(t--){
        ll n,k,a,b;
        cin>>n>>k>>a>>b;
        city c[n+1];
        for(int i=1;i<=n;i++) cin>>c[i].x>>c[i].y;
        if(a<=k&&b<=k){
            cout<<0<<endl;
            continue;
        }
        ll dd=abs(c[a].x-c[b].x)+abs(c[a].y-c[b].y);
        ll minlla=LONG_LONG_MAX,minllb=LONG_LONG_MAX;
        for(int i=1;i<=k;i++){
            ll t=abs(c[i].x-c[a].x)+abs(c[i].y-c[a].y);
            minlla=min(minlla,t);
        }
        for(int i=1;i<=k;i++){
            ll t=abs(c[i].x-c[b].x)+abs(c[i].y-c[b].y);
            minllb=min(minllb,t);
        }
        if(a<=k) cout<<min(dd,minllb)<<endl;
        else if(b<=k) cout<<min(dd,minlla)<<endl;
        else{
            if(k==0) cout<<dd<<endl;
            else cout<<min(dd,minlla+minllb)<<endl;
        } 
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,m,minx=INT_MAX,maxx=-INT_MAX;
        cin>>n>>m;
        vector<int> a(n),b(m),aa(n);
        for(int i=1;i<=n;i++){
            int t;
            cin>>t;
            a.push_back(t);
        }
        for(int i=1;i<=m;i++){
            int t;
            cin>>t;
            a.push_back(t);
        }
        for(int i=0;i<m;i++){
            int x=0;
            for(int j=0;j<n;j++){
                int t=a[j];
                t|=b[i];
                x^=t;
            }
            minx=min(x,minx);
            maxx=max(x,maxx);
        }
        cout<<minx<<" "<<maxx<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,m;
        cin>>n>>m;
        vector<int> a(n),b(m);
        for(int i=0;i<n;i++) cin>>a[i];
        for(int i=0;i<m;i++) cin>>b[i];
        int u=0,minre=0,maxre=0;
        int cnt[31]={0};
        for(int it:b) u|=it;
        for(int it:a){
            for(int i=0;i<31;i++){
                if(it&(1<<i)) cnt[i]++;
            }
        }
        int base=1;
        for(int i=0;i<31;i++){
            int obite=cnt[i]%2;
            int allbite=n%2;
            if(u&(1<<i)){
                minre+=min(obite,allbite)*base;
                maxre+=max(obite,allbite)*base;
            }
            else{
                maxre+=obite*base;
                minre+=obite*base;
            }
            base*=2;
        }
        cout<<minre<<' '<<maxre<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        int a[siz][siz]={0};
        for(int i=1;i<=n;i++){
            for(int j=1;j<=n-1;j++) cin>>a[i][j];
        }
        queue<int> b;
        for(int j=1;j<=n-1;j++){   
            int cnt[siz]={0};
            if(j==1){
                for(int i=1;i<=n;i++){
                    cnt[a[i][j]]++;
                    if(i==1) b.push(a[i][j]);
                    else{
                        if(b.size()==1){
                            if(a[i][j]!=b.front()){
                                b.push(a[i][j]);
                            }
                        } 
                    }
                }
            }
            for(int i=1;i<=n;i++){
                if(j==1){
                    if(cnt[b.back()]==1){
                        cout<<b.front()<<" "<<b.back()<<" ";
                        b.pop();
                    }
                    else{
                        cout<<b.back()<<" "<<b.front()<<" ";
                        b.push(b.front());
                        b.pop();
                        b.pop();
                    } 
                    break;
                }
                else{
                    if(a[i][j]!=b.front()){
                        cout<<a[i][j]<<" ";
                        b.push(a[i][j]);
                        b.pop();
                        break;
                    }
                }
            }
        }
        cout<<endl;
    }
    return 0;
}


struct arry{
    vector<ll> a;
    ll sum=0;
    bool const operator>(const arry& b) const{
        if(sum!=b.sum){
            return sum>b.sum;
        }
        return 0;
    }
};

int main(){
    int t;
    cin>>t;
    while(t--){
        ll n,m,sum=0,temp=0;
        cin>>n>>m;
        vector<arry> v(n);
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                int x;
                cin>>x;
                v[i].a.push_back(x);
            }
            v[i].sum=accumulate(v[i].a.begin(),v[i].a.end(),0);
        }        
        sort(v.begin(),v.end(),greater<arry>());
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                temp+=v[i].a[j];
                sum+=temp;
            }
        }
        cout<<sum<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        ll k;
        cin>>k;
        ll a=sqrtl(k);
        while(a!=(ll)sqrtl(k+a)){
            a=(ll)sqrtl(k+a);
        }
        cout<<k+a<<endl;
    }
    return 0;
}


int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        set<int> arrlen, arrsum;
        int minin=INT_MAX;
        for(int i=1;i<=n;i++){
            int k;
            cin>>k;
            arrlen.insert(k); 
            int startlen=arrsum.size();
            for(int j=1;j<=k;j++){
                int t;
                cin>>t;
                arrsum.insert(t);
            }
            int endlen=arrsum.size();
            if(endlen-startlen==0) continue;
            minin=min(minin,endlen-startlen);
        }
        if(n==1) cout<<0<<endl;
        else cout<<arrsum.size()-minin-1<<endl;
    }
    return 0;
}

struct aarr{
    vector<int> a;
    int unic=0;
    bool operator <(const aarr& b){
        return unic<b.unic;
    }
};

int main(){
    int t;
    cin>>t;
    for(int i=1;i<=t;i++){
        int n;
        cin>>n;
        aarr arr[siz];
        unordered_map<int,int>mp;
        for(int j=1;j<=n;j++){
            int x;
            cin>>x;
            for(int k=1;k<=x;k++){
                int t1;
                cin>>t1;
                arr[j].a.push_back(t1);
                mp[t1]++;
            }
        }
        for(int j=1;j<=n;j++){
            for(auto it:arr[j].a){
                if(mp[it]==1){
                    arr[j].unic++;
                }
            }
        }
        sort(arr,arr+n);
        int cnt=0;
        for(auto it:arr){
            if(it.unic==0){
                continue;
            }
            else{
                cnt=it.unic;
                break;
            } 
        }
        cout<<endl;
        cout<<mp.size()-cnt<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    for(int i=1;i<=t;i++){
        int n;
        cin>>n;
        vector<int> a[siz];
        unordered_set<int> allsize;
        for(int j=1;j<=n;j++){
            int x;
            cin>>x;
            for(int k=1;k<=x;k++){
                int t1;
                cin>>t1;
                allsize.insert(t1);
                a[j].push_back(t1);
            }
        }
        int maxx=0;
        unordered_set<int> used;
        for(int it:allsize){
            for(int j=1;j<=n;j++){
                if(find(a[j].begin(),a[j].end(),it)==a[j].end()){
                    for(auto it:a[j]){
                        used.insert(it);
                    }
                }
            }
            int cnt=used.size();
            maxx=max(maxx,cnt);
            used.clear();
        }
        cout<<maxx<<endl;
    }
    return 0;
}

int main(){
    ll n,k,ans=0;
    cin>>n>>k;
    ll kk=k;
    ll a[n+1]={0};
    ll bb[n+1]={0};
    unordered_map<ll,ll> b;
    for(int i=1;i<=n;i++){
        cin>>a[i];
        bb[i]=bb[i-1]+a[i];
    }
    for(int i=1;i<=n;i++){
        b[bb[i]]=1;
    }
    while(k<bb[n]){
        for(int i=0;i<=n;i++){
            ll f=bb[i];
            if(k+f>bb[n]) break;
            if(b[f+k]==1){
                ans++;
            }
        }
        k+=kk;
    }
    cout<<ans;
    return 0;
}

int main(){
    ll n,k,ans=0;
    cin>>n>>k;
    unordered_map<ll,ll> cnt;
    ll a[n+1]={0};
    ll b[n+1]={0};
    b[0]=0;
    cnt[0]++;
    for(int i=1;i<=n;i++){
        cin>>a[i];
        b[i]=b[i-1]+a[i];
        ans+=cnt[b[i]%k];
        cnt[b[i]%k]++;
    }
    cout<<ans;
    return 0;
}

struct matrix{
    int x,y,val;
    bool operator > (const matrix& b){
        return val>b.val;
    }
};

int main(){
    int n;
    cin>>n;
    int iszz=(n+1)*(n+1);
    matrix a[n+1][n+1],b[iszz];
    int isd=0;
    for(int x=1;x<=n;x++){
        for(int y=1;y<=n;y++){
            cin>>a[x][y].val;
            a[x][y].x=x;
            a[x][y].y=y;
        }
    }
    sort(a+1,a+n+1,);
    int ans=-INT_MAX;
    int x1=a[1].x,y1=a[1].y,ans1=a[1].val;
    for(int i=2;i<=isd;i++){
        int x2=a[i].x,y2=a[i].y,ans=0;
        for(int )
    }

}

int main(){
    int n,maxin=0;
    cin>>n;
    int a[n+1][n+1]={0};
    int b[n+1][n+1]={0};
    int c[n+1]={0};
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            cin>>a[i][j];
            b[i][j]=b[i-1][j]+a[i][j];
        }
    }
    for(int up=1;up<=n;up++){
        for(int down=up;down<=n;down++){
            for(int j=1;j<=n;j++){
                c[j]=b[down][j]-b[up-1][j];
            }
            int sum=c[1];
            int now=c[1];
            for(int j=2;j<=n;j++){
                now=max(now+c[j],c[j]);
                sum=max(sum,now);
            }
            maxin=max(maxin,sum);
        }
    }
    cout<<maxin<<endl;
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n,m;
        cin>>n>>m;
        vector<ll> a(n),b(m);
        for(int i=0;i<n;i++) cin>>a[i];
        for(int i=0;i<m;i++) cin>>b[i];
        if(n==1){
            cout<<"yes"<<endl;
            continue;
        }
        sort(b.begin(),b.end());
        a[0]=min(a[0],b[0]-a[0]);
        bool flag=true;
        for(int i=1;i<n;i++){
            auto bb=lower_bound(b.begin(),b.end(),a[i]+a[i-1]);
            if(a[i]>=a[i-1]){
                if(bb!=b.end()) a[i]=min(a[i],*bb-a[i]);
            }
            else if(bb!=b.end()) a[i]=*bb-a[i];
            if(a[i]<a[i-1]){
                cout<<"no"<<endl;
                flag=0;
                break;
            } 
        }
        if(flag) cout<<"yes"<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        if(n%2==0) cout<<2*n-1<<endl;
        else cout<<2*n-2<<endl;
        for(int i=2;i<=n;i++){
            cout<<i<<" "<<"1 "<<n<<endl;
            if(n%2==0){
                if(i!=n/2+1){
                    if(((double)i-1)/((double)n-1)<=0.5){
                        cout<<i<<" "<<i<<" "<<n<<endl;
                    }
                    else cout<<i<<" 1"<<" "<<i-1<<endl;
                }
                else{
                    cout<<i<<" "<<"1 "<<i-1<<endl;
                    cout<<i<<" "<<i<<" "<<n<<endl;
                }
            }
            else{
                if(((double)i-1)/((double)n-1)<=0.5){
                    cout<<i<<" "<<i<<" "<<n<<endl;
                }
                else cout<<i<<" 1"<<" "<<i-1<<endl;
            }
        }
    }
    return 0;
}

int main(){
    ll n;
    ll d;
    cin>>n>>d;
    ll a[n]={0},b[n]={0},qb[n+1]={0};
    for(int i=1;i<n;i++){
        cin>>b[i];
        qb[i]=qb[i-1]+b[i];
    } 
    for(int i=1;i<=n;i++){
        cin>>a[i];
    } 
    ll nowlen=0;
    ll am=a[1];
    ll sum=0;
    for(int i=2;i<=n;i++){
        if(am>a[i]){
            while(nowlen<qb[i-1]){
                nowlen+=d;
                sum+=am;
            }
            am=a[i];
        }
        else{
            while(nowlen<qb[i-1]){
                nowlen+=d;
                sum+=am;
            }
        }
    }
    cout<<sum<<endl;
    return 0;
}

int main(){
    int x;
    cin>>x;
    int a,b,c;
    c=x%10;
    b=x/10%10;
    a=x/100;
    cout<<x<<"="<<a<<"*100+"<<b<<"*10+"<<c<<endl;
    return 0;
}

int main(){
    double f;
    cin>>f;
    double c=5*(f-32)/9;
    cout<<setprecision(2)<<fixed<<c<<endl;
}

int main(){
    double a,b,c,d;
    cout<<"Enter 3 numbers: ";
    cin>>a>>b>>c;
    double e=1/a+1/b+1/c;
    cout<<"电阻:"<< fixed << setprecision(2) << 1/e << endl;
}
int main() {
    const double G = 6.67e-11;
    const double M = 6e24;
    const double R = 6.371e6;     
    const double PI = M_PI;     
    double T;                    
    cin >> T;
    double r = cbrt( (G * M * T * T) / (4 * PI * PI) );
    double h = r - R;
    cout<<setprecision(2)<<fixed<<h<<endl;
    return 0;
}

int main(){
    double a,b,c;
    cin>>a>>b>>c;
    double d=b*b-4*a*c;
    double x1=(-b+sqrt(d))/(2*a);
    double x2=(-b-sqrt(d))/(2*a);
    cout<<"x1="<<x1<<",x2="<<x2<<endl;
    return 0;
}

struct tree{
    ll x;
    ll h;
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin>>n;
    tree tree[n+1];
    for(int i=1;i<=n;i++){
        cin>>tree[i].x>>tree[i].h;
    }
    if(n<=2){
        cout<<n<<endl;
        return 0;
    }
    ll ans=2;
    for(int i=2;i<=n-1;i++){
        if(tree[i].x-tree[i].h>tree[i-1].x){
            ans++;
        }
        else if(tree[i].x+tree[i].h<tree[i+1].x){
            ans++;
            tree[i].x=tree[i].x+tree[i].h;
        }
    }
    cout<<ans<<endl;
    return 0;
}

struct node{
    int x;
    bool mark=0;
};

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        vector<node> nodea(n+1);
        vector<node> nodeb(n+1);
        string s;
        cin>>s;
        for(int i=1;i<=n;i++){
            nodea[i].x=s[i-1]-'0';
            nodeb[i].x=s[i-1]-'0';
        }
        ll ansa=0,cnta=0,ansb=0,cntb=0;
        for(int i=n;i>=1;i--){
            if((nodea[i].x==1&&nodea[cnta+1].x!=1)||(nodea[i].x==1&&nodea[cnta+1].x==1&&nodea[cnta+1].mark==1)){
                ansa+=i-cnta;
                cnta++;
                nodea[i].mark=1;
            }
            else if(nodea[cnta+1].x==1&&nodea[cnta+1].mark==0){
                ansa++;
                nodea[cnta+1].mark=1;
            }
        }
        for(int i=n;i>=1;i--){
            if((nodeb[i].x==0&&nodeb[cnta+1].x!=0)||(nodeb[i].x==0&&nodeb[cnta+1].x==0&&nodeb[cnta+1].mark==1)){
                ansb+=i-cntb;
                cntb++;
                nodeb[i].mark=1;
            }
            else if(nodeb[cntb+1].x==0&&nodeb[cntb+1].mark==0){
                ansb++;
                nodeb[cntb+1].mark=1;
            }
        }
        cout<<endl;
        cout<<ansa<<endl;
        cout<<ansb<<endl;
        cout<<min(ansa,ansb)<<endl;
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        int a[n+1]={0};
        string s;
        cin>>s;
        vector<int> a1(1,0),a2(1,0);
        for(int i=1;i<=n;i++){
            a[i]=s[i-1]-'0';
            if(a[i]==1) a1.push_back(i);
            else a2.push_back(i);
        }
        ll ans1=0,ans2=0;
        int m1=a1.size()-1,m2=a2.size()-1;
        int i1=1,i2=1,cnt1=1,cnt2=1;
        while(i1<=m1){
            if(a1[i1]==cnt1){
                ans1++;
                i1++;
            }
            else{
                ans1+=a1[m1]-cnt1+1;
                m1--;
                cnt1++;
            }
        }
        while(i2<=m2){
            if(a2[i2]==cnt2){
                ans2++;
                i2++;
            }
            else{
                ans2+=a2[m2]-cnt2+1;
                m2--;
                cnt2++;
            }
        }
        cout<<min(ans1,ans2)<<endl;
    }
    return 0;
}

int main(){
    int n,a=10000;
    cin>>n;
    int fn,fn1,fn2,gn,gn1;
    fn2=1;fn1=2;gn1=1;gn=2;
    if(n<=2){
        cout<<n<<endl;
        return 0;
    }
    for(int i=3;i<=n;i++){
        fn=(fn1+fn2+2*gn1)%a;
        gn=(fn2+gn1)%a;
        fn2=fn1;
        fn1=fn;
        gn1=gn;
    }
    cout<<fn<<endl;
    return 0;
}

struct node{
    int val;
    int boo=0;
    int x;
    bool operator <(node& n){
        return val<n.val;
    }
};

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        set<int> s;
        multiset<int> ms;
        node node[n+1];
        for(int i=1;i<=n;i++){
            int xx;
            cin>>xx;
            s.insert(xx);
            node[i].val=xx;
            node[i].x=i;
        }
        if(s.size()==1){
            cout<<"NO"<<endl;
            continue;
        }
        else cout<<"YES"<<endl;
        sort(node+1,node+n+1);
        node[1].boo=1;
        for(int i=2;i<=n;i++){
            if(node[i].val!=node[1].val){
                cout<<node[1].x<<" "<<node[i].x<<endl;
                node[i].boo=1;
            }
        }
        for(int i=1;i<=n;i++){
            if(node[i].boo==0&&node[i].val!=node[n].val){
                cout<<node[n].x<<" "<<node[i].x<<endl;
            }
        }
    }
    return 0;
}

int main(){
    int t;
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        map<ll,ll> mp;
        ll a[n+1],qa[n+1]={0};
        for(int i=1;i<=n;i++){
            cin>>a[i];
            qa[i]=a[i]+qa[i-1];
        }
        ll maxll=0;
        mp[0]=1;
        for(int i=1;i<=n;i++){
            mp[qa[i]]++;
            maxll=max(maxll,mp[qa[i]]);
        }
        cout<<maxll-1<<endl;
    }    
}

struct node{
    int l,r;
};

int main(){
    int n;
    cin>>n;
    node node[n+1];
    for(int i=1;i<=n;i++){
        cin>>node[i].l>>node[i].r;
    }
    int maxin=1;
    for(int i=1;i<=n;i++){
        int t=node[i].r,tmax=1;
        for(int j=1;j<=n;j++){
            if(node[j].l<=t&&t<=node[j].r&&j!=i) tmax++;
        }
        maxin=max(maxin,tmax);
    }
    cout<<maxin<<endl; 
    return 0;
}

int main(){
    int n;
    cin>>n;
    vector<pair<int,int>> v;
    for(int i=0;i<n;i++){
        int l,r;
        cin>>l>>r;
        v.push_back(make_pair(l,1));
        v.push_back(make_pair(r,-1));
    }
    int sum=0;
    sort(v.begin(),v.end());
    int maxin=1;
    for(pair it:v){
        sum+=it.second;
        maxin=max(maxin,sum);
    }
    cout<<maxin<<endl;
    return 0;
}

int c1,c2,c3;

void fan(long n){
    c1=c2=c3=0;
    while(n){
        switch(n%10){
            case 1:c1++;break;
            case 2:c2++;break;
            case 3:c3++;
        }
        n/=10;
    }
}
main(){
    long n=123114350l;
    fan(n);
    printf("\nthe result\n");
    printf("c1=%d\n",c1);
    printf("c2=%d\n",c2);
    printf("c3=%d\n",c3);
    return 0;
}


int main() {
    int t,x;
    cin>>t;
    while(t--){
        cin>>x;
        if(x<-1) cout<<pow(x,3)-1<<endl;
        else if(-1<=x&&x<=1) cout<<-3*x+1<<endl;
        else if(1<=x&&x<=10) cout<<3*exp(2*x-1)+5<<endl;
        else cout<<5*x+3*log10(2*x*x-1)-13<<endl;
    }
    return 0;
}

int main(){
    double a,b,c;
    cin>>a>>b>>c;
    vector<double> v={a,b,c};
    sort(v.begin(),v.end());
    if(v[0]+v[1]<=v[2]){
        cout<<"error"<<endl;
        return 0;
    }
    else{
        double s=(v[0]+v[1]+v[2])/2.0;
        double area=pow(s*(s-a)*(s-b)*(s-c),1.0/2.0);
        cout<<area<<endl;
    }
    return 0;
}

int main(){
    int n;
    cin>>n;
    if(n%4==0&&n%100!=0||n%400==0) cout<<"yes"<<endl;
    else cout<<"no"<<endl;
    return 0;
}
 
ll dp[23] = {0};
bool isBlocked[23][23] = {false}; 

void markHorse(ll x, ll y, ll maxX, ll maxY) {
    int dx[9] = {0, -2, -1, 1, 2, 2, 1, -1, -2};
    int dy[9] = {0, 1, 2, 2, 1, -1, -2, -2, -1};
    for (int i = 0; i < 9; i++) {
        ll nx = x + dx[i];
        ll ny = y + dy[i];
        if (nx >= 1 && nx <= maxX && ny >= 1 && ny <= maxY) {
            isBlocked[nx][ny] = true;
        }
    }
}

int main() {
    ll bx, by, mx, my;
    cin >> bx >> by >> mx >> my;
    bx++; by++; mx++; my++;
    markHorse(mx, my, bx, by);
    if (!isBlocked[1][1]) dp[1] = 1;
    for (int i = 1; i <= bx; i++) {
        for (int j = 1; j <= by; j++) {
            if (isBlocked[i][j]) dp[j] = 0;
            else if (j > 1) dp[j]+=dp[j-1];
        }
    }
    cout << dp[by] << endl;
    return 0;
}

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


ll dp[20][20]={0};

int main(){
    int n;
    cin>>n;
    for(int i=0;i<=n;i++){
        for(int j=0;j<=n;j++){
            if(!i) dp[i][j]=1;
            else if(!j) dp[i][j]=dp[i-1][j+1];
            else dp[i][j]=dp[i-1][j+1]+dp[i][j-1];
        }
    }
    cout<<dp[n][0]<<endl;
    return 0;
}

int main(){
    ll n;
    cin>>n;
    ll f[n+2]={0};
    for(int i=1;i<=n;i++){
        for(int j=1;j<=i/2;j++){
            f[i]+=f[j];
        }
        f[i]++;
    }
    cout<<f[n]<<endl;
    return 0;
}


ll dp[22][22][22]={0};

ll w(ll a,ll b,ll c){
    if(a<=0||b<=0||c<=0) return 1;
    else if(a>20||b>20||c>20){
        if(dp[20][20][20]==0) dp[20][20][20]=w(20,20,20);
        return dp[20][20][20]; 
    }
    else if(a<b&&b<c){
        if(dp[a][b][c-1]==0) dp[a][b][c-1]=w(a,b,c-1);
        if(dp[a][b-1][c-1]==0) dp[a][b-1][c-1]=w(a,b-1,c-1);
        if(dp[a][b-1][c]==0) dp[a][b-1][c]=w(a,b-1,c);
        return dp[a][b][c-1]+dp[a][b-1][c-1]-dp[a][b-1][c];
    }
    else{
        if(dp[a-1][b][c]==0) dp[a-1][b][c]=w(a-1,b,c);
        if(dp[a-1][b-1][c]==0) dp[a-1][b-1][c]=w(a-1,b-1,c);
        if(dp[a-1][b][c-1]==0) dp[a-1][b][c-1]=w(a-1,b,c-1);
        if(dp[a-1][b-1][c-1]==0) dp[a-1][b-1][c-1]=w(a-1,b-1,c-1);
        return dp[a-1][b][c]+dp[a-1][b-1][c]+dp[a-1][b][c-1]-dp[a-1][b-1][c-1];
    }
}

int main(){
    ll a,b,c;
    while(cin>>a>>b>>c){
        if(a==-1&&b==-1&&c==-1) return 0;
        else cout<<"w("<<a<<", "<<b<<", "<<c<<") = "<<w(a,b,c)<<endl;
    }
    return 0;
}


string work(){
    int k;
    char c;
    string l="",r="";
    while(cin>>c){
        if(c=='['){
            cin>>k;
            r=work();
            while(k--){
                l+=r;
            }
        }
        else if(c==']') return l;
        else l+=c;
    }
    return l;
}

int main(){
    cout<<work()<<endl;
    return 0;
}


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
    int n,m;
    cin>>m>>n;
    int x=n-m+1;
    vector<int> a,b,c;
    a.push_back(1);
    b.push_back(1);
    if(x<=2){
        cout<<1<<endl;
        return 0;
    }
    x-=2;
    while(x){
        c=add(a,b);
        a=b;
        b=c;
        x--;
    }
    for(auto i=c.rbegin();i!=c.rend();i++) cout<<*i;
    return 0;
}


int main(){
    int n,m;
    cin>>n>>m;
    int a[101];
    for(int i=1;i<=n;i++) cin>>a[i];
    int b[101][10001]={0};
    b[0][0]=1;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            if(a[i]==j) b[i][j]=b[i-1][j]+1;
            if(a[i]>j) b[i][j]=b[i-1][j];
            if(a[i]<j) b[i][j]=b[i-1][j]+b[i-1][j-a[i]];
        }
    }
    cout<<b[n][m];
    return 0;
}


int main(){
    string s;
    ll n;
    cin>>s>>n;
    ll l=s.size();
    while(n>l){
        string s2=s.substr(0,l-1);
        s+=s[l-1];
        s+=s2;
        l*=2;
    }
    cout<<s[n-1]<<endl;
    return 0;
}

int main(){
    string s;
    ll n;
    cin>>s>>n;
    ll l=s.size();
    ll e=l;
    if(n<=l){
        cout<<s[n-1]<<endl;
        return 0;
    }
    while(n>e) e*=2;
    while(e>l){
        ll m=e/2;
        if(n<=m) e=m;
        else if(n==m+1){
            n=m;
            e=m;
        } 
        else{
            n=n-m-1;
            e=m;
        } 
    }
    cout<<s[n-1]<<endl;
    return 0;
}


char c[205];
int x,sp;

void print(){
    for(int i=1;i<=2*x+2;i++) cout<<c[i];
    cout<<endl;
}

void init(int n){
    for(int i=1;i<=n;i++) c[i]='o';
    for(int i=n+1;i<=2*n;i++) c[i]='*';
    for(int i=2*n+1;i<=2*n+2;i++) c[i]='-';
    print();
}

void move(int n){
    for(int i=0;i<=1;i++){
        c[sp+i]=c[n+i];
        c[n+i]='-';
    } 
    sp=n;
    print();
}

void work(int n){
    if(n==4){
        move(4);
        move(8);
        move(2);
        move(7);
        move(1);
    }
    else{
        move(n);
        move(2*n-1);
        work(n-1);
    }
}

int main(){
    cin>>x;
    sp=2*x+1;
    init(x);
    work(x);
    return 0;
}


int main(){
    int x;
    multiset<int> s;
    while(cin>>x){
        if(x==0) break;
        s.insert(x);
    }
    cout<<*s.rbegin()<<endl;
    return 0;
}


double f(double x){
    for(int i=x;i>=1;i--){
        if(i==x) continue;
        else x*=i;
    }
    return x;
}

int main(){
    double n,r=0;
    cin>>n;
    for(int i=n;i>=1;i--){
        r+=f(i);
    }
    cout<<r<<endl;
    return 0;
}


int main(){
    for(int i=1;i<=19;i++){
        for(int j=1;j<=33;j++){
            for(int k=1;k<=99;k++){
                if(5*i+3*j+k==100){
                    cout<<"鸡公"<<i<<"只"<<"鸡婆"<<j<<"只"<<"小鸡"<<k<<"只"<<endl;
                    return 0;
                }
            }
        }
    }
    return 0;
}


int main(){
    double r;
    for(double i=1;i<=20;i++){
        r+=1.0/((i)*(i+1));
    }
    cout<<r<<endl;
    return 0;
}


int main(){
    int a,n,r=0;
    cin>>a>>n;
    string s1,s;
    s1=to_string(a);
    for(int i=1;i<=n;i++){
        if(i==1) s=s1;
        else s=s+s1;
        int x=stoi(s);
        r+=x;
    }
    cout<<r<<endl;
    return 0;
}


vector<int> se(int n){
    int base=1,cnt=0;
    vector<int> v;
    while(n){
        if(n&1==1){
            v.push_back(cnt);
        }
        cnt++;
        n>>1;
    }
    return v;
}

void work(int n){
    char c;
    while(cin>>c){
        if(c=='('){
            int x;
            cin>>x;
            if(x!=0&&x!=2){
                work(x);
            }
        }
        else if(c==')'){
            return;
        }
        else{
            
        }
    }
}

int main(){
    int n;
    cin>>n;

}

void solve(int n){
    bool a=0;
    while(n){
        int x=log2(n);
        if(a) cout<<"+";
        if(x==1) cout<<"2";
        else if(x==0) cout<<"2(0)";
        else {
            cout<<"2(";
            solve(x);
            cout<<")";
        }
        n-=pow(2,x);
        a=1;
    }
}

int main(){
    int n;
    cin>>n;
    solve(n);
    return 0;
}


char s[2048][4096];

void print(int x,int y){
    s[x][y]=' ';
    s[x][y+1]='/';
    s[x][y+2]='\\';
    s[x][y+3]=' ';
    s[x+1][y]='/';
    s[x+1][y+1]='_';
    s[x+1][y+2]='_';
    s[x+1][y+3]='\\';
}

/*
   /\   
  /__\  
 /\  /\ 
/__\/__\

*/
/*
void solve(int x,int y,int l,int w,int n){
    if(n==1){
        print(x,y);
        return;
    }
    else{
        solve(x,y+(1/4.0)*w,l/2,w/2,n-1);
        solve(x+(1/2.0)*l,y,l/2,w/2,n-1);
        solve(x+(1/2.0)*l,y+(1/2.0)*w,l/2,w/2,n-1);
    }
}

int main(){
    int n;
    cin>>n;
    for(int i=0;i<2048;i++){
        for(int j=0;j<4096;j++){
            s[i][j]=' ';
        }
    }
    solve(0,0,pow(2,n),pow(2,n+1),n);
    for(int i=0;i<pow(2,n);i++){
        for(int j=0;j<pow(2,n+1);j++){
            cout<<s[i][j];
        }
        cout<<endl;
    }
    return 0;
}


struct goden{
    double m,v;
    double p=v/m;
    bool operator > (const goden& b) const{
        return p>b.p;
    }
}; 

int main(){
    vector<goden> a;
    double n,t;
    cin>>n>>t;
    for(int i=1;i<=n;i++){
        double x,y;
        cin>>x>>y;
        a.push_back({x,y});
    }
    sort(a.begin(),a.end(),greater<goden>());
    double ans=0;
    auto it=a.begin();
    while(t&&it!=a.end()){
        if(it->m<=t){
            t-=it->m;
            ans+=it->v;
            it++;
        }
        else{
            ans+=t*(it->p);
            t=0;
        }
    }
    cout<<setprecision(2)<<fixed<<ans<<endl;
    return 0;
}


struct node{
    int t,i;
    bool operator<(const node& b) const{
        if(t!=b.t) return t<b.t;
        else return i<b.i;
    }
};

int main(){
    double n;
    cin>>n;
    vector<node> a(n+1);
    for(int i=1;i<=n;i++){
        int t;
        cin>>t;
        a[i]={t,i};
    }
    vector<int> b(n+1);
    sort(a.begin(),a.end());
    b[0]=0;
    for(int i=1;i<=n;i++){
        b[i]=b[i-1]+a[i].t;
    }
    double ans=accumulate(b.begin(),prev(b.end()),0.0)/n;
    for(auto it=a.begin();it!=a.end();it++){
        if(it->i!=0) cout<<it->i<<" ";
    }
    cout<<endl;
    cout<<setprecision(2)<<fixed<<ans<<endl;
    return 0;
}


struct node{
    int l,r;
    bool operator<(const node& b)const{
        return r<b.r;
    }
};

int main(){
    int n;
    cin>>n;
    vector<node> v(n);
    for(int i=0;i<n;i++){
        cin>>v[i].l>>v[i].r;  
    }
    sort(v.begin(),v.end());
    int ans=1,nr=v[0].r;
    for(int i=1;i<n;i++){
        if(v[i].l>=nr){
            ans++;
            nr=v[i].r;
        } 
    }
    cout<<ans<<endl;
    return 0;
}

int main(){
    int n;
    cin>>n;
    ll a[siz],b[siz],c[siz];
    a[0]=0;
    b[0]=0;
    c[0]=0;
    c[1]=0;
    for(int i=1;i<=n;i++){
        cin>>a[i];
    }
    sort(a,a+n+1);
    for(int i=1;i<=n;i++){
        b[i]=a[i]+b[i-1];
        if(i>=2){
            c[i]=b[i]+c[i-1];
        }
    }
    cout<<c[n];
    return 0;
}


int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n;
    cin>>n;
    multiset<ll> s;
    for(int i=1;i<=n;i++){
        int t;
        cin>>t; 
        s.insert(t);
    }
    ll ans=0;
    while(s.size()>1){
        auto it=s.begin();
        auto it2=next(it);
        ans+=*it+*it2;
        s.insert(*it+*it2);
        s.erase(it);
        s.erase(it2);
    }
    cout<<ans<<endl;
    return 0;
}


int main(){
    ll n,x,ans=0;
    cin>>n>>x;
    ll a[siz];
    for(int i=0;i<n;i++) cin>>a[i];
    for(int i=0;i<n-1;i++){
        if(a[i]+a[i+1]>x){
            if(i==0){
                if(a[0]>=x){
                    ans+=a[0]-x;
                    a[0]=x;
                    if(a[1]>0){
                        ans+=a[1];
                        a[1]=0;
                    }
                }
                else{
                    ans+=a[0]+a[1]-x;
                    a[1]=x-a[0];
                }
            }
            else if(i==n-2){
                if(a[n-1]>=x){
                    ans+=a[n-1]-x;
                    a[n-1]=x;
                    if(a[n-2]>0){
                        ans+=a[n-2];
                        a[n-2]=0;
                    }
                }
                else{
                    ans+=a[n-1]+a[n-2]-x;
                    a[n-2]=x-a[n-1];
                }
            }
            else{
                if(a[i]+a[i+1]>x){
                    ans+=a[i]+a[i+1]-x;
                    a[i+1]=x-a[i];
                }
            }
        }
    }
    cout<<ans<<endl;
    return 0;
}


int main(){
    string s;
    cin>>s;
    int k;
    cin>>k;
    list<int> l;
    vector<int> a(250,0);
    for(int i=0;i<s.size();i++){
        l.push_back(s[i]-'0');
    }
    while(k){
        int maxin=0;
        for(auto it=l.begin();it!=l.end();it++){
            maxin=max(maxin,*it);
        }
        for(auto it=l.begin();it!=l.end();it++){
            if(*it==maxin){
                l.erase(it);
                break;
            }
        }
        k--;
    }
    for(auto it:l){
        cout<<it;
    }
    return 0;
}

int main(){
    string s;
    int k;
    cin>>s>>k;
    list<int> a;
    for(int i=0;i<s.size();i++){
        int t=s[i]-'0';
        a.push_back(t);
    }
    for(auto it=a.begin();it!=a.end();it++){
        auto it2=next(it);
        if(*it>*it2){
            a.erase(it);
            k--;
        }
    }
    while(k){
        a.pop_back();
        k--;
    }
    for(auto it=a.begin();it!=a.end();it++){
        cout<<*it;
    }
    return 0;
}

int main(){
    string s;
    int k;
    cin>>s>>k;
    vector<int> v;
    v.push_back(-1);
    for(auto c:s){
        while(!v.empty()&&v.back()>c-'0'&&k>0){
            v.pop_back();
            k--;
        }
        v.push_back(c-'0');
    }
    while(k){
        v.pop_back();
        k--;
    }
    for(auto x:v){
        if(x!=-1) cout<<x;
    }
    cout<<endl;
    return 0;
}


int main(){
    string s;
    int k;
    cin>>s>>k;
    vector<int> v;
    for(auto c:s){
        if(v.empty()){
            v.push_back(c-'0');
            continue;
        }
        while(!v.empty()&&v.back()>c-'0'&&k>0){
            v.pop_back();
            k--;
        }
        v.push_back(c-'0');
    }
    while(k){
        v.pop_back();
        k--;
    }
    bool flag=true;
    bool first=1;
    for(auto x:v){ 
        if(x==0&&flag){
            continue;
        }
        if(x!=0){
            flag=false;
            cout<<x;
            first=0;
        }
        if(x==0&&!flag){
            cout<<0;
            first=0;
        }
    }
    if(first) cout<<0;
    return 0;
}


struct app{
    int x,y;
    bool operator < (const app& a) const{
        return y<a.y;
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    int n,s,a,b;
    cin>>n>>s>>a>>b;
    app app[5000];
    for(int i=0;i<n;i++) cin>>app[i].x>>app[i].y;
    sort(app,app+n);
    int ans=0;
    int i=0;
    while(s>0){
        if(app[i].x<=a+b&&app[i].y<=s){
            ans++;
            s-=app[i].y;
        }
        i++;
        if(i>=n) break;
    }
    cout<<ans<<endl;
    return 0;
}

int main(){
    int n;
    cin>>n;
    vector<int> a(n+1);
    vector<ll> dp(n+1);
    dp[0]=0;
    a[0]=0;
    for(int i=1;i<=n;i++) cin>>a[i];
    dp[1]=a[1];
    for(int i=2;i<=n;i++){
        if(a[i]>a[i-1]){
            dp[i]=dp[i-1]+a[i]-a[i-1];
        }
        else{
            dp[i]=dp[i-1];
        }
    }
    cout<<dp[n]<<endl;
    return 0;
}


struct mk{
    int p,a;
    bool operator < (const mk& b) const{
        return p<b.p;
    }
};

int main(){
    int n,m;
    cin>>n>>m;
    vector<mk> a(m);
    for(int i=0;i<m;i++) cin>>a[i].p>>a[i].a;
    sort(a.begin(),a.end());
    int ans=0;
    int i=0;
    while(n){
        if(a[i].a<=n){
            n-=a[i].a;
            ans+=a[i].p*a[i].a;
        }
        else{
            ans+=n*a[i].p;
            n=0;
        }
        i++;
    }
    cout<<ans<<endl;
    return 0;
}

int main(){
    int w,n,ans=0;
    cin>>w>>n;
    vector<int> a(n);
    deque<int> b;
    for(int i=0;i<n;i++) cin>>a[i];
    sort(a.begin(),a.end(),greater());
    for(int i=0;i<n;i++) b.push_back(a[i]);
    while(!b.empty()){
        int l=b.front(),r=b.back();
        if(l+r<=w&&b.size()>=2){
            b.pop_back();
            b.pop_front();
        }
        else if(l+r>w&&b.size()>=2){
            b.pop_front();
        }
        else b.pop_back();
        ans++;
    }
    cout<<ans<<endl;
    return 0;
}

int main(){
    int n;
    ll ans=0;
    cin>>n;
    vector<int> a(n);
    deque<int> b;
    for(int i=0;i<n;i++) cin>>a[i];
    sort(a.begin(),a.end());
    for(int i=0;i<n;i++) b.push_back(a[i]);
    int now=0,i=0,nx;
    while(n){
        if(i%2){
            nx=b.front();
            ans+=pow(now-nx,2);
            b.pop_front();
        }
        else{
            nx=b.back();
            ans+=pow(now-nx,2);
            b.pop_back();
        }
        now=nx;
        n--;
        i++;
    }
    cout<<ans<<endl;
    return 0;
}

int main(){
    int n;
    cin>>n;
    cout<<n<<endl;
    return 0;
}

int fan(int n){
    if(n==1) return 10;
    else return fan(n-1)+2;
}

int main(){
    int t=2;
    while(t--){
        int n;
        cin>>n;
        cout<<fan(n)<<endl;
    }
}

double sum(double n){
    double res=0;
    for(int i=1;i<=n;i++) res+=1.0/(i*(i+1));
    return res;
}

int main(){
    double n;
    cin>>n;
    cout<<sum(n)<<endl;
    return 0;
}


bool fan(ll x){
    if(x<=3) return x>1;
    if(x%6!=1&&x%6!=5) return false;
    ll a=sqrt(x);
    for(ll i=5;i<=a;i+=6) if(x%i==0||x%(i+2)==0) return false;
    return true;
}

int main(){
    int t=2;
    while(t--){
        int n;
        cin>>n;
        cout<<fan(n)<<endl;
    }
    return 0;
}


int gcd(int x,int y){
    if(y==0) return x;
    return gcd(y,x%y);
}

int main(){
    int n,m;
    cin>>n>>m;
    cout<<gcd(n,m)<<endl;
    return 0;
}


int main(){
    int n=10;
    int a[10];
    for(int i=0;i<n;i++) cin>>a[i];
    for(int i=0;i<n;i++) cout<<a[i]<<" ";
    cout<<endl;
    sort(a,a+n);
    for(int i=0;i<n;i++) cout<<a[i]<<" ";
    cout<<endl;
    return 0;
}


int main(){
    int n=10;
    int a[n];
    for(int i=0;i<n;i++) cin>>a[i];
    sort(a,a+n);
    double sum=0;
    for(int i=1;i<n-1;i++){
        sum+=a[i];
    }
    cout<<sum/8<<endl;
    return 0;
}


#define N 5

int fun(int a[][N], int n)
{
    for(int i=0;i<N;i++) for(int j=0;j<=i;j++) a[i][j]*=n;
    return 0;
}

int main()
{
    int a[N][N], n, i, j;
    printf("****** The array *******\n");
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++)
        {
            a[i][j] = rand() % 10; printf("%4d", a[i][j]);
        }
        printf("\n");
    }
    do n = rand() % 10; while (n >= 3);
    printf("n = %4d\n", n);
    fun(a, n);
    printf("******** THE RESULT ********\n");
    for (i = 0; i < N; i++)
    {
        for (j = 0; j < N; j++) printf("%4d", a[i][j]);
        printf("\n");
    }
    return 0;
}


int fun(int score[], int m, int below[])
{
    int sum = 0;
    for(int i = 0; i < m; i++) {
        sum += score[i];
    }
    double avg = (double)sum / m;
    int i = 0, j = 0;
    for(; i < m; i++) {
        if(score[i] < avg) {
            below[j++] = score[i];
        }
    }
    return j;
}

int main()
{
    int score[] = {10, 20, 30, 40, 50, 60, 70, 80, 90};
    int below[9];
    int n = fun(score, 9, below);
    printf("低于平均分的人数: %d\n", n);
    printf("低于平均分的成绩: ");
    for (int i = 0; i < n; i++)
        printf("%d ", below[i]);
    printf("\n");
    return 0;
}


int main() {
    char text[5][100];
    int capital[5] = {0}; 
    int lower[5] = {0};   
    int number[5] = {0};  
    int space[5] = {0};   
    int other[5] = {0};   
    printf("请输入5行文字：\n");
    for (int i = 0; i < 5; i++) {
        printf("第%d行: ", i + 1);
        fgets(text[i], sizeof(text[i]), stdin);
    }
    
    for (int i = 0; i < 5; i++) {
        for (int j = 0; text[i][j] != '\0'; j++) {
            char c = text[i][j];
            if (isupper(c)) capital[i]++;
            else if (islower(c)) lower[i]++;
            else if (isdigit(c)) number[i]++;
            else if (c == ' ') space[i]++;
            else if (c != '\n' && c != '\r') other[i]++;
        }
    }

    printf("\n各行字符统计结果：\n");
    for (int i = 0; i < 5; i++) {
        printf("第%d行: 大写字母=%d, 小写字母=%d, 数字=%d, 空格=%d, 其他=%d\n", 
               i + 1, capital[i], lower[i], number[i], space[i], other[i]);
    }
    return 0;
}


int main(){
    int n=1;
    string s;
    getline(cin, s);
    for(int i=0;i<s.length();i++) if(s[i]==' ') n++;
    cout<<n<<endl;
    return 0;
}


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


int main() {    
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= i; j++) {
            printf("%d*%d=%-2d  ", j, i, i * j);
        }
        printf("\n");
    }
    
    return 0;
}


int main() {
    printf("Prime numbers within 100:\n");
    
    int count = 0; 
    
    for (int i = 2; i <= 100; i++) {
        int is_prime = 1;  
        
        for (int j = 2; j < i; j++) {
            if (i % j == 0) {
                is_prime = 0;  
                break;
            }
        }
        
        if (is_prime) {
            printf("%3d ", i);
            count++;
            
            if (count % 10 == 0) {
                printf("\n");
            }
        }
    }
    
    printf("\n\nThere are %d prime numbers under 100.\n", count);
    
    return 0;
}

void fun(char *s,char t[ ])
{
    int i=0, j=0;
    while(s[i] != '\0'){
        if(s[i] % 2 != 0){
            t[j] = s[i];
            j++;
        }
        i++;
    }
    t[j] ='\0'; 
}

int main()
{
    char s[100], t[100];
    printf("\nPlease enter string S：");
    scanf("%s", s);
    fun(s, t);
    printf("\n%s", t);
    return 0;
}


int main(){
    int a[10]={0,1,2,3,4,5,6,7,8,9};
    int b[10];
    for(int i=0,j=9;i<10;i++,j--){
        b[i]=a[j];
    }
    for(int i=0;i<10;i++){
        cout<<b[i]<<" ";
    }
    return 0;
}


int main(){
    int a[4][5];
    for(int i=0;i<4;i++){
        for(int j=0;j<5;j++) cin>>a[i][j];
    }
    int max=INT32_MIN;
    int maxi=-1;
    int maxj=-1;
    for(int i=0;i<4;i++){
        for(int j=0;j<5;j++){
            if(a[i][j]>max){
                max=a[i][j];
                maxi=i;
                maxj=j;
            }
        }   
    }
    cout<<max<<"最大"<<maxi+1<<"行"<<maxj+1<<"列"<<endl;
}


#define N 80

int fun(char *str) {
    int i = 0, j = 0;
    
    while (str[j] != '\0') j++;
    j--;
    
    while (i < j) {
        if (str[i] != str[j]) return 0;  
        i++;
        j--;
    }
    return 1;
}

int main() {
    char s[N];
    
    printf("Enter a string: ");
    gets(s);
    
    printf("\n\n");
    puts(s);
    
    if (fun(s)) {
        printf("YES\n");
    } else {
        printf("NO\n");
    }
    return 0;
}


int gcd (int a, int b){
    return b==0 ? a : gcd (b,a%b);
} 

int isPrime(int x){
    if(x<2) return 0;
    if(x==2) return 1;
    int limit = sqrt(x);
    for(int i=2;i<=limit;i++) if(x%i==0) return 0;
    return 1;
}

int main(){
    cout<<gcd(12,24)<<endl;
    cout<<isPrime(17)<<endl;
    return 0;
}

*/