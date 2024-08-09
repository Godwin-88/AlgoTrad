#include "Defs.h"

int main()
{
    int a = 5;
    int b = 10;
    int c = 7;

    // Using the PRINT1 and PRINT2 macros
    PRINT1(a);
    PRINT2(a, b);

    // Using the MAX2 macro to find the maximum of two values
    int max2 = MAX2(a, b);
    printf("Maximum of %d and %d is: %d\n", a, b, max2);

    // Using the MAX3 macro to find the maximum of three values
    int max3 = MAX3(a, b, c);
    printf("Maximum of %d, %d, and %d is: %d\n", a, b, c, max3);

    return 0;
}
