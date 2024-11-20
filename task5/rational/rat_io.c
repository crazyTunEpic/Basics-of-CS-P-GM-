#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "rational.h"

// Преобразование строки в дробь
rational_t string_to_rational(const char *str) {
    long n = 0, d = 1;
    if (sscanf(str, "%ld/%ld", &n, &d) == 2) {
        return rational(n, d);
    } else {
        sscanf(str, "%ld", &n);
        return rational(n, d);
    }
}

// Вывод дроби
void print_rational(rational_t r) {
    if (rat_denom(r) == 1) {
        printf("%ld\n", rat_num(r)); // выводим только числитель, если знаменатель равен 1
    } else {
        printf("%ld/%u\n", rat_num(r), (unsigned int)rat_denom(r)); // Правильный формат для unsigned
    }
}
