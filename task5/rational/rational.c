#include <stdio.h>
#include <stdlib.h>
#include "rational.h"

// Нахождение НОД алгоритмом Эвклида
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}


rational_t rational(long n, long d) {
   
    if (d == 0) {
        printf("Ошибка: деление на ноль.\n");
        exit(1);
    }

   
    if (n == 0) {
        return (rational_t){0, 1}; 
    }
    
   
    int sign = (n < 0) ^ (d < 0 ? -1 : 1);
    n = abs(n);
    d = abs(d);
    
    int divisor = gcd(n, d);
    
    return (rational_t){sign * (n / divisor), (unsigned int)(d / divisor)};
}

// Возвращает числ
long rat_num(rational_t r) {
    return r.num;
}

// Возвращает знам
long rat_denom(rational_t r) {
    return r.denom;
}
