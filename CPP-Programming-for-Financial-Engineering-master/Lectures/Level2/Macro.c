#include "Defs.h"//directive includes the Defs.h file that contains the macro definitions.


int main()
{
    int a = 5;
    int b = 10;

    // Using the PRINT1 macro to print the value of a
    PRINT1(a);//The PRINT1(a) macro is called to print the value of a.

    // Using the PRINT2 macro to print the values of a and b
    PRINT2(a, b);//The PRINT2(a, b) macro is called to print the values of both a and b.

    return 0;//The program returns 0 to indicate successful execution.
}
