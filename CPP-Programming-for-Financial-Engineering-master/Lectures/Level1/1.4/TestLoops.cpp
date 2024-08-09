// TestLoops.cpp
//
// Comparing the different ways to loop and make decisions in code. We 
// take the example of solving a scalar nonlinear equation x = f(x) by the fixed point
// method (contraction mapping):
//
//		x(n+1) = f(x(n)), x(0) given.
//
//	We iterate until either fabs(x(n+1) - x(n)) < TOL or n >= MAXITER. The fixed point method
//  converges if fabs(df/dx) < 1. Variants are Brouwer and Banach fixed point theorems.
//
// In this version we examine x = exp(-x). Later you can generalise the code by defining f(x) using 
// function pointers. 
//
// DJD
//

#include <math.h>//includes the mathe function library.
#include <iostream>
using namespace std;

//f(x)=exp(-x) in code form is written bel
double f(double x)
{
	return exp(-x);
}

double ftp_I(double x_0, double tol, long maxiter)
{ // Solution using goto

	double xcurrent;
	long counter = 0;

L1:
	xcurrent = f(x_0);

	if (counter >= maxiter)
	{
		cout << "Max iterations exceeded, method not converging\n";
		return xcurrent;
	}

	if (fabs(xcurrent - x_0) >= tol)
	{
		x_0 = xcurrent;
		counter++;
		goto L1;
	}
	
	cout << "Method I has converged in " << counter << " iterations\n";

	return xcurrent;
}
//Parameters:
//x_0: Initial guess for the fixed-point iteration.
//tol: The tolerance level for the difference between successive approximations.
//maxiter: Maximum number of iterations allowed.
//Logic:
//The iteration starts with the initial guess x_0.
//The function f(x) is evaluated, and the result is stored in xcurrent.
//If the maximum number of iterations is reached (counter >= maxiter), the loop exits, and a message is printed indicating non-convergence.
//If the difference between xcurrent and x_0 is greater than or equal to tol, the loop continues with the updated value of x_0.
//The loop uses goto L1 to jump back to the start of the loop.
//If the loop converges, a message is printed, and the final value is returned.




double ftp_II(double x_0, double tol, long maxiter)
{ // Solution using a hard-code for loop and a break

	double xcurrent;
	long counter;

	for (counter = 0; counter < maxiter; ++counter)
	{

		xcurrent = f(x_0);

		if (fabs(xcurrent - x_0) < tol)
		{ // Convergence has occurred, so we are finished

			break; // stop execution of loop
		}
	
		x_0 = xcurrent;
	}

	// Broke out!

	if (counter < maxiter)
	{
		cout << "Method II has converged in " << counter << " iterations\n";
	}
	else
	{
		cout << "Method II has NOT converged in " << counter << " iterations\n";
	}
//Logic:
//A for loop is used to iterate up to maxiter times.
//Each iteration evaluates the function f(x) and checks if the result is within the tolerance level.
//If convergence is achieved (fabs(xcurrent - x_0) < tol), the loop breaks.
//After the loop, a message is printed to indicate whether convergence was achieved or not.
//The final value of xcurrent is returned.
	return xcurrent;
}

double ftp_III(double x_0, double tol, long maxiter)
{ // Solution using a while 'forever' for loop and a break

	double xcurrent;
	long counter = 0;
	
	while (true)
	{

		xcurrent = f(x_0); counter++;

		if (counter >= maxiter)
		{
			cout << "Method III has NOT converged in " << counter << " iterations\n";
			break;
		}

		if (fabs(xcurrent - x_0) < tol)
		{ // Convergence has occurred

			cout << "Method III has converged in " << counter << " iterations\n";
			break; // stop execution of loop
		}
	
		x_0 = xcurrent;
	}
//Logic:
//A while (true) loop is used to create an infinite loop that continues until a break condition is met.
//The loop iterates, evaluating f(x) and checking if the result is within the tolerance level.
//If the maximum number of iterations is reached, or if convergence occurs, the loop breaks and prints a message.
//The final value of xcurrent is returned.
	return xcurrent;
}




int main()
{
	// Input parameters
	double xInit = 0.5;
	long maxIter = 10000;
	double tol = 1.0e-5; // 0.000001

	// The implementations of the solvers
	cout << "Fixed point (method I) is: " << ftp_I(xInit, tol, maxIter) << endl;
	cout << "Fixed point (method II) is: " << ftp_II(xInit, tol, maxIter) << endl;
	cout << "Fixed point (method III) is: " << ftp_III(xInit, tol, maxIter) << endl;


	// Testing scope of a variable
	int j=10;
	{
		cout << "j: " << j << endl;
	}

	// j does not exist anymore
	cout << "j: " << j << endl;

	return 0;
}

//Parameters:
//xInit: Initial guess for the fixed-point iteration (0.5).
//maxIter: Maximum number of iterations (10000).
//tol: Tolerance level for convergence (1.0e-5 or 0.00001).
//Solvers:
//The main function calls each of the three fixed-point iteration methods and prints the results.
//Testing Scope of a Variable:
//The variable j is declared inside a block and printed.
//The second cout statement will cause a compilation error because j is out of scope. (We discussed this issue earlier.)
//Summary:
//Fixed-Point Iteration:

//The code implements three methods to solve the equation 𝑥=exp⁡(−𝑥)using fixed-point iteration.
//Each method demonstrates a different looping construct (goto, for, and while (true)).
//Scope of Variables:

//The code also illustrates the concept of variable scope, showing that variables declared within a block are not accessible outside that block.
//Practical Application:

//This code could be expanded to solve other equations by modifying the function f(x).
//It could also be enhanced by using function pointers or lambda expressions to pass different functions into the solver methods.
//This code is a good example of how different control structures can be used in C++ to achieve the same objective, and it also highlights the importance of understanding variable scope.	