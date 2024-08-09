// TestFibonacci.cpp
// 
// Showing the use of recursive functions by implementing 
// Fibonacci sequences.
//
// DJD
//


#include <algorithm>
#include <iostream>
using namespace std;//allows the use of standard library functions such as cout without the need of the prefix std::

long Fibonacci(long n)
{ // Recursive function

        if(n == 0)
		{
			return 0;
		}

		if(n == 1)
		{
			return 1;
		}

		return Fibonacci(n-1) + Fibonacci(n-2);
}
//Function Definition:
//long Fibonacci(long n): This function takes an integer n and returns the nth Fibonacci number.
//Base Cases:
//The function has two base cases:
//If n == 0, it returns 0 (the first number in the Fibonacci sequence).
//If n == 1, it returns 1 (the second number in the Fibonacci sequence).
//Recursive Case:
//If n is greater than 1, the function calls itself recursively as Fibonacci(n-1) + Fibonacci(n-2).
//This is the key part of the Fibonacci sequence definition, where each term is the sum of the two preceding terms.

int main()
{ // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765 . . .


    int N = 40; // How many Fibonacci numbers to compute

	for (int n = 0; n < N; ++n)
	{ 
		cout << Fibonacci(n) << ",";
	}

    return 0;

	// N = 30000??
}
//Variable Declaration:
//int N = 40;: This sets the number of Fibonacci numbers to compute to 40.
//For Loop:
//The loop runs from n = 0 to n < 40.
//In each iteration, it calls the Fibonacci(n) function to calculate the nth Fibonacci number and prints it, followed by a comma.
//Return Statement:
//return 0;: This indicates that the program has executed successfully.
//Commented-Out Code:
// N = 30000??: This is a comment suggesting the idea of calculating the 30,000th Fibonacci number, but it’s commented out.
//Recursive Function Explanation
//Recursive Nature:
//The function uses a classic recursive approach to calculate Fibonacci numbers. For each call to Fibonacci(n), the function calls itself twice: once to compute Fibonacci(n-1) and once to compute Fibonacci(n-2).
//Efficiency:
//This recursive approach is straightforward but inefficient for large values of n because it involves a lot of redundant calculations. For example, Fibonacci(40) will recursively calculate Fibonacci(38) twice, Fibonacci(37) multiple times, and so on, leading to exponential time complexity.
//This inefficiency makes it impractical to compute very large Fibonacci numbers, like Fibonacci(30000), using this method. The comment // N = 30000?? suggests the idea of computing such a large Fibonacci number, which would be extremely slow and could cause stack overflow errors due to deep recursion.