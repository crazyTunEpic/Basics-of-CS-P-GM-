#include <stdio.h>
#include <stdlib.h>
#include "rational.h"

// Функция для нахождения НОД
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Конструктор рационального числа
rational_t rational(long n, long d) {
    if (d == 0) {
        fprintf(stderr, "Ошибка: деление на ноль.\n");
        exit(EXIT_FAILURE);
    }
    
    if (n == 0) {
        return (rational_t){0, 1}; // каноническое представление 0
    }

    int sign = (n < 0 ^ d < 0) ? -1 : 1;
    n = abs(n);
    d = abs(d);
    
    int divisor = gcd(n, d);
    
    return (rational_t){sign * (n / divisor), (unsigned int)(d / divisor)};
}

// Функции для получения числителя и знаменателя
long rat_num(rational_t r) {
    return r.num;
}

long rat_denom(rational_t r) {
    return r.denom;
}
