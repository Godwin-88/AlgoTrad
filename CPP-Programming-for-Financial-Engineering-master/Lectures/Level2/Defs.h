#ifndef DEFS_H//prevent multiple inclusions of this header file.
#define DEFS_H//prevent multiple inclusions of this header file.

#include <stdio.h>

// Macro to print one variable
#define PRINT1(a) printf("Value of " #a ": %d\n", a)

// Macro to print two variables
#define PRINT2(a, b) printf("Values of " #a " and " #b ": %d, %d\n", a, b)
//Macros:
//pRINT1(a): This macro takes one argument (a) and prints its value.
//#a converts the variable name a into a string, which is useful for labeling the output.
//printf is used to print the value of a.
//PRINT2(a, b): This macro takes two arguments (a and b) and prints their values similarly.
//It prints both variable names and their corresponding values.




// Macro to find the maximum of two values
#define MAX2(x, y) ((x) > (y) ? (x) : (y))
//This macro compares two values x and y and returns the larger one.
//The ternary operator ((x) > (y) ? (x) : (y)) is used to compare x and y.
//Parentheses around the arguments ensure that expressions passed to the macro 
//are evaluated correctly, avoiding unexpected behavior due to operator precedence.




// Macro to find the maximum of three values using MAX2
#define MAX3(x, y, z) (MAX2(MAX2((x), (y)), (z)))

//This macro finds the maximum of three values x, y, and z.
//It does this by calling the MAX2 macro twice: first to find the maximum of x and y, and then to compare the result with z.
//The macro uses MAX2(MAX2((x), (y)), (z)) to achieve this.

#endif // DEFS_H.closes the conditional directive.

