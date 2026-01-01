#include <stdio.h>

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
    
    printf("\n\nThere are %d prime numbers under 100.\n", count)
;
    
    return 0;
}
