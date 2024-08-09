// TestVariables.cpp
//
// Using variables, operators and expressions. We focus on double precision:
//
//	1. Declaring and initialising variables
//	2. Using operators
//	3. Postfix/prefix operators
//	4. Expressions and precedence
//
// DJD
//


#include <iostream> //For input/ouput operations
using namespace std;

int main()
{
	double d1 = 3.1415; double d2 = -2.0; double d3 = 2.71;
	double d4; 

//	cout << d4 << endl; // Will give a run-time error

	d4 = d1 + d2/d3; cout << d4 << endl;
	d4 = (d1 + d2)/d3; cout << d4 << endl;

	// Combined assignment operators
	d4 += d1; // d4 = d4 + d1
	d3 *= d2; // d4 = d4 * d1

	// Prefix/postfix
	int i = 3;
	int j = ++i; cout << j << ", " << i << endl; // 4,4
	//The pre-increment operator (++i) increments i before it is used in the assignment to j.
    //After the operation, both i and j are 4.
    //Therefore, the output of the cout statement is 4, 4.
	i = 3;
	int k = i++; cout << k << ", " << i << endl; // 3,4
    //The post-increment operator (i++) increments i after its value is used in the assignment to k.
    //After the operation, k is 3 (the original value of i before increment), and i is 4 (after increment).
    //Therefore, the output of the cout statement is 3, 4.



	// Comma operator
	int y = 5;
	int c;

	c = y +=4, y + 5; 

	cout << "Value of c: " << c << endl; // 9
	//The comma operator in this context causes the left-hand expression (y += 4) to be evaluated and its result assigned to c.
    //The right-hand expression (y + 5) is evaluated but not used.
    //Therefore, the value of c is 9, and the output of the cout statement is 9.
    //This code illustrates that while the comma operator can evaluate multiple expressions,
	// only the leftmost expression's result is used in assignments when used in this context.

	y = 5; // Reset
	int c2 = (y +=4, y + 5); 
	cout << "Value of c2: " << c2 << endl; // 14

    //The comma operator in the expression (y += 4, y + 5) evaluates both y += 4 and y + 5, but the result of the last expression (y + 5) is returned.
    //After y is incremented to 9, y + 5 equals 14, so c2 is assigned the value 14.
    //The output of the cout statement is 14.



	// Replacing , by ;
	y = 5; // Reset
	int d = y += 4; y + 5;

	cout << "Value of d: " << d << endl; // ??
//The semicolon (;) acts as a statement terminator, so the expression int d = y += 4; is one complete statement, and y + 5; is another.
//int d = y += 4; increments y to 9 and assigns this value to d.
//The expression y + 5; is evaluated but its result is not used or stored.
//Therefore, the value of d remains 9, and the output of the cout statement is 9.
	return 0;
//return 0; in the main() function signals to the operating system that the program has completed successfully.
//It provides a way for the program to communicate its execution status to external environments, which can be crucial for debugging, scripting, and process management.
//While it is optional in modern C++ standards, explicitly including return 0; is a good habit to make your code's intent clear.


}
