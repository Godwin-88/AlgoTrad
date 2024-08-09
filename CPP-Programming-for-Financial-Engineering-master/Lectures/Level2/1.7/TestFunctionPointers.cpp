// TestFunctionPointers.cpp
//
// Sample code to show the use of function pointer syntax to promote
// reusability and flexibility.
//
// DJD

#include <math.h>
#include <iostream>
using namespace std;

double LeonardoPisa(double x)
{ // x = F(x), this is a contraction

	// Solves x^3 + 2x^2 + 10x = 20 by rewriting in the form x = f(x)

	return 20.0 / (x*x + 2.0*x + 10);
}

double SquareRoot(double x)
{ // Square root of 2
//This function computes an approximation of the square root of 2 using the iterative method 
//𝑥_𝑛+1=0.5*(X+2/X)
	return 0.5 * (x + 2.0/x);
}


double FPSolver(double (*f) (double x), double x0, double TOL)//This is a general-purpose fixed-point iteration solver. It iteratively applies a function 𝑓f to approximate the fixed point of the function 𝑓f.
{ // General 1 solver for a contraction mapping f in form x = f(x)
//Parameters:
//double (*f) (double x): A function pointer that points to the function used in the iteration.
//double x0: The initial guess for the fixed-point iteration.
//double TOL: The tolerance level for convergence.

	double xnp1;
	double diff = 10.0 * TOL;

	while (diff >= TOL)
	{ // You should have a break if algorithm does not converge

		xnp1 = (*f)(x0);
		diff = fabs(xnp1 - x0);
		x0 = xnp1;
	}
//The function iterates, applying the function f to the current approximation x0.
//It calculates the difference between the new approximation xnp1 and the previous one.
//The loop continues until the difference is smaller than the tolerance TOL.
//The final approximation is returned as the fixed point.
	return x0;
}

int main()
{
//The FPSolver function is called multiple times with different functions passed as arguments using function pointers.

	cout << "Cosine fixed point solver: " <<  FPSolver(cos, 0.12, 1.0e-2) << endl;	// 'cos' is system delivered function
	
	// Square roots
	double tol = 1.0e-10; double x0 = 100.0;
	cout << "Square root: " <<  cout.precision(16) << FPSolver(SquareRoot, x0, tol) << endl;	
	
	tol = 1.0e-3;
	x0 = 31.2;
	cout << "Root of cubic equation: " <<  cout.precision(4) << FPSolver(LeonardoPisa, x0, tol) << endl;	
	
	// Extra level of indirection
	double (*myFunc)(double x);
	myFunc = SquareRoot;
	cout << "Square root, again: " <<  cout.precision(16) << FPSolver(myFunc, x0, tol) << endl;	

	myFunc = ::sin; // C library function
	cout << "Sine fixed point solver: " <<  FPSolver(myFunc, 0.12, 1.0e-2) << endl;	

	return 0;
}
//Function Pointers: The program demonstrates how function pointers can be used to pass different functions to a solver, making the code more flexible and reusable.
//Fixed-Point Iteration: The FPSolver function uses fixed-point iteration to find the roots or fixed points of the provided functions.
//Reusability: By using function pointers, the FPSolver function can solve a variety of problems with different functions, as shown by its application to the cosine function, square root approximation, and a cubic equation.
//Precision Control: The program also demonstrates how to control the precision of the output using cout.precision().