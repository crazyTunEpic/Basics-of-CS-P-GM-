#include <stdio.h>
#include <stdlib.h>
#include "rational.h"

// Сложение двух дробей
rational_t rat_add(rational_t a, rational_t b) {
    long num = rat_num(a) * rat_denom(b) + rat_num(b) * rat_denom(a);
    long denom = rat_denom(a) * rat_denom(b);
    return rational(num, denom);
}

// Вычитание дробей
rational_t rat_sub(rational_t a, rational_t b) {
    long num = rat_num(a) * rat_denom(b) - rat_num(b) * rat_denom(a);
    long denom = rat_denom(a) * rat_denom(b);
    return rational(num, denom);
}

// Умножение дробей
rational_t rat_mul(rational_t a, rational_t b) {
    long num = rat_num(a) * rat_num(b);
    long denom = rat_denom(a) * rat_denom(b);
    return rational(num, denom);
}

// Деление дробей
rational_t rat_div(rational_t a, rational_t b) {
    if (rat_num(b) == 0) {
        fprintf(stderr, "Ошибка: деление на ноль.\n");
        exit(EXIT_FAILURE);
    }
    return rational(rat_num(a) * rat_denom(b), rat_denom(a) * rat_num(b));
}
