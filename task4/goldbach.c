#include <stdio.h>
#include <stdlib.h>
#include "calculate_primes.h"

int main() {
    int lower, upper;
    int max_limit = 10000000; // 10 миллионов
    int *primes = (int *)malloc((max_limit + 1) * sizeof(int));
    calculate_primes(primes, max_limit);

    printf("Введите пару четных чисел (до 10,000,000): ");
    while (scanf("%d %d", &lower, &upper) == 2) {
        if (lower < 4 || upper > 10000000 || lower % 2 != 0 || upper % 2 != 0) {
            printf("Введите корректные четные числа от 4 до 10,000,000.\n");
            continue;
        }

        for (int i = lower; i <= upper; i += 2) {
            int count = 0;
            int first = -1, second = -1;
            for (int j = 2; j <= i / 2; j++) {
                if (primes[j] && primes[i - j]) {
                    count++;
                    if (first == -1) {
                        first = j;
                        second = i - j;
                    }
                }
            }
            if (count > 0) {
                printf("%d %d %d %d\n", i, count, first, second);
            }
        }
    }

    free(primes);
    return 0;
}
