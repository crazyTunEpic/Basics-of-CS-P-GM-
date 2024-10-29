#include <stdio.h>
#include <stdlib.h>
#include "calculate_primes.h"

int main() {
    int n;

    printf("Введите максимальное число (до 10,000,000): ");
    scanf("%d", &n);

    if (n < 2 || n > 10000000) {
        printf("Введите число в диапазоне от 2 до 10,000,000.\n");
        return 1;
    }

    int *primes = (int *)malloc((n + 1) * sizeof(int));
    
    calculate_primes(primes, n);

    for (int i = 2; i <= n; i++) {
        if (primes[i]) {
            printf("%d\n", i);
        }
    }

    free(primes);
    return 0;
}
