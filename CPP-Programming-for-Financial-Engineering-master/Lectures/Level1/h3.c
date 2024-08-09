/* Operators */
#include <stdio.h>

int main()
{
    int x;

    // Expression: -3 + 4 * 5 - 6
    // According to operator precedence:
    // 4 * 5 = 20
    // -3 + 20 - 6
    // -3 + 20 = 17
    // 17 - 6 = 11
    x = -3 + 4 * 5 - 6;
    printf("x=%d\n", x); // Output: x=11

    // Expression: 3 + 4 % 5 - 6
    // According to operator precedence:
    // 4 % 5 = 4 (modulus of 4 divided by 5 is 4)
    // 3 + 4 - 6
    // 3 + 4 = 7
    // 7 - 6 = 1
    x = 3 + 4 % 5 - 6;
    printf("x=%d\n", x); // Output: x=1

    // Expression: -3 * 4 % -6 / 5
    // According to operator precedence:
    // -3 * 4 = -12
    // -12 % -6 = 0 (because -12 is evenly divisible by -6)
    // 0 / 5 = 0
    x = -3 * 4 % -6 / 5;
    printf("x=%d\n", x); // Output: x=0

    // Expression: (7 + 6) % 5 / 2
    // Parentheses first:
    // 7 + 6 = 13
    // 13 % 5 = 3 (modulus of 13 divided by 5 is 3)
    // 3 / 2 = 1 (integer division, so the result is 1)
    x = (7 + 6) % 5 / 2;
    printf("x=%d\n", x); // Output: x=1

    return 0;
}
