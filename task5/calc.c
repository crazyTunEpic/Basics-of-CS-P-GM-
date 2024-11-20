#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "rational.h"

rational_t rat_add(rational_t a, rational_t b);
rational_t rat_sub(rational_t a, rational_t b);
rational_t rat_mul(rational_t a, rational_t b);
rational_t rat_div(rational_t a, rational_t b);

rational_t string_to_rational(const char *str);
void print_rational(rational_t r);

int main() {
    char input[100];
    rational_t last_result = {0, 1}; // хранит последний результат

    while (fgets(input, sizeof(input), stdin)) {
        char op;
        char op1[20], op2[20];

        if (sscanf(input, "%s %c %s", op1, &op, op2) != 3) {
            printf("Ошибка ввода, попробуйте снова.\n");
            continue;
        }

        rational_t a, b;

        if (strcmp(op1, "last") == 0) {
            a = last_result;
        } else {
            a = string_to_rational(op1);
        }

        if (strcmp(op2, "last") == 0) {
            b = last_result;
        } else {
            b = string_to_rational(op2);
        }

        rational_t result;

        // Выполняем арифметическую операцию
        switch (op) {
            case '+':
                result = rat_add(a, b);
                break;
            case '-':
                result = rat_sub(a, b);
                break;
            case '*':
                result = rat_mul(a, b);
                break;
            case '/':
                result = rat_div(a, b);
                break;
            default:
                printf("Неизвестная операция: %c\n", op);
                continue;
        }

        last_result = result; // сохраняем последний результат
        printf("= ");
        print_rational(result);
    }
    return 0;
}
