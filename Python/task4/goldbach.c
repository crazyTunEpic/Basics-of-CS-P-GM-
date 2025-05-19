#include <stdlib.h>
#include <math.h>
#include "goldbach.h"

void calculate_primes(int limit, int **primes, int *count) {
    if (limit < 2) {
        *primes = NULL;
        *count = 0;
        return;
    }
    
    // решето Эратосфена
    char *is_prime = (char *)malloc((limit + 1) * sizeof(char));
    for (int i = 0; i <= limit; i++) {
        is_prime[i] = 1;
    }
    is_prime[0] = is_prime[1] = 0;
    
    for (int i = 2; i * i <= limit; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= limit; j += i) {
                is_prime[j] = 0;
            }
        }
    }
    
    // подсчет простых чисел
    *count = 0;
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            (*count)++;
        }
    }
    
    // заполнение массива
    *primes = (int *)malloc(*count * sizeof(int));
    int index = 0;
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            (*primes)[index++] = i;
        }
    }
    
    free(is_prime);
}