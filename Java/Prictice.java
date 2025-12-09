package Java;
/**
public class practice {
    public static void main(String[] args) {
        String a="*",t="*";
        System.out.println(a);
        int n=4;
        for(int i=0;i<n;i++){
            a+=t;
            System.out.println(a);
        }
    }
    public static int max (int a[]){
        int max=a[0];
        for(int i=0;i<a.length;i++){
            if(a[i]>max){
                max=a[i];
            }
        }
        return max;
    }
    public static void main(String[] args) {
        int[] numbers = new int[]{9, 2, 15, 2, 22, 10, 6};
        int r=max(numbers);
        System.out.println(r);
    }
}

public class text {

    public static void windowPosSum(int[] a, int n) {
        for(int i = 0; i < a.length; i++) {
            if(a[i]>=0) {
                for (int j = i + 1; j <= i + n; j++) {
                    if (j < a.length) {
                        a[i] += a[j];
                    } else break;
                }
            }
        }
    }

    public static void main(String[] args) {
        int[] a = {1, 2, -3, 4, 5, 4};
        int n = 3;
        windowPosSum(a, n);

        // Should print 4, 8, -3, 13, 9, 4
        System.out.println(java.util.Arrays.toString(a));
    }
}
// 1. 定义类
class Person {
    // 2. 定义属性（成员变量）
    String name;
    int age;

    // 3. 定义构造方法
    public Person(String personName, int personAge) {
        name = personName;
        age = personAge;
    }

    // 4. 定义成员方法
    public void introduce() {
        System.out.println("Hello, my name is " + name + " and I am " + age + " years old.");
    }
}

// 使用类
public class Main {
    public static void main(String[] args) {
        // 5. 实例化对象（创建对象）
        Person person1 = new Person("Alice", 25);

        // 6. 访问对象的方法
        person1.introduce(); // 输出: Hello, my name is Alice and I am 25 years old.
    }
}
    
class intlist{
    int value;
    intlist next;
    public intlist(int v,intlist n){
        value=v;
        next=n;
    }
    public int size(){
        if(this.next==null){
            return 1;
        }
        else return 1+this.next.size();
    }
    public int iterationsize(){
        int i=0;
        intlist p=this;
        while(p!=null){
            i++;
            p=p.next;
        }
        return i;
    }
    public int get(int i){
        int n=0;
        intlist p=this;
        while(p!=null){
            if(n==i){
                return p.value;
            }
            n++;
            p=p.next;
        }
        return -1;  
    }
}

public class Main{
    public static void main(String[] args){
        intlist l=new intlist(15,null);
        l=new intlist(10,l);
        l=new intlist(5,l);
        System.out.println(l.size());
        System.out.println(l.iterationsize());
        System.out.println(l.get(2));
    }
}

public class Main {
    
    public static int fib(int n){
        int x1=0,x2=1,x3=1;
        if(n<2) return n>1?1:0;
        for(int i=2;i<n;i++){
            x3=x1+x2;
            x1=x2;
            x2=x3;
        }
        return x3;
    }

    public static void main(String[] args) {
        int[] num=new int[]{1,2,3,4,5,6,7,8,9,10};
        for(int it:num) System.out.println(fib(it));
    }
}

*/