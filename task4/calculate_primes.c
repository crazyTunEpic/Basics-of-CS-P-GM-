#include <stdio.h>
#include "calculate_primes.h"

void calculate_primes(int primes[], int n) {
    for (int i = 0; i <= n; i++) primes[i] = 1; // Инициализируем массив
    primes[0] = primes[1] = 0; // 0 и 1 не являются простыми числами
    for (int i = 2; i * i <= n; i++) { 
        if (primes[i]) {
            for (int j = i * i; j <= n; j += i) primes[j] = 0; // Помечаем составные числа
        }
    }
}
