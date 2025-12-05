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

*/