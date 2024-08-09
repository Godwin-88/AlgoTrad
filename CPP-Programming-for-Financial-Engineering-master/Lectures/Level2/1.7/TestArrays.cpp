// TestArrays.cpp
//
// Some mathematical operations on fixed-sixed arrays and matrices.
//
// DJD
//

#include <iostream>
using namespace std;

// Preprocessor directives
#define NX 4//represents the size of the vector and the number of rows in the matrices
#define NY 3//represents the number of culumns in the  matrices

// Handy shorthannd notation
typedef double Vector[NX];//Defines a type alias Vector for an array of double with NX elements.
typedef double NumericMatrix[NX][NY];//Defines a type alias NumericMatrix for a 2D array (matrix) of double with NX rows and NY columns.

double innerProduct(Vector v1, Vector v2)//This function calculates the inner product (dot product) of two vectors.
{ // Call by value! copies of v1 and v2 created in code body

	double result = v1[0]*v2[0];//The function initializes result with the product of the first elements of v1 and v2.

	for (int j = 1; j < NX; ++j)
	{
		result += v1[j]*v2[j];//It then iterates over the remaining elements of the vectors, multiplying corresponding elements and adding the result to result.
	}

	return result;//Finally, the function returns the computed inner product.

}

void print(NumericMatrix m)//This function prints the elements of a matrix in a structured format.
{ // Print elements of a matrix

	for (int i = 0; i < NX; ++i)
	{
	//The function iterates over the rows of the matrix.
    //For each row, it prints the elements in a comma-separated format enclosed in parentheses.
    //It uses nested loops: the outer loop iterates over the rows (i), and the inner loop iterates over the columns (j).
		cout << endl << "(";
		for (int j = 0; j < NY; ++j)
		{
			cout << m[i][j] << ",";
		}
		cout << ")";
	}
	cout << endl;
}

int main()
{

	Vector v1, v2;
	for (int i = 0; i < NX; ++i)
	{
		v1[i] = i;
		v2[i] = NX - i;
	}

	cout << "Inner product: " << innerProduct(v1, v2) << endl;

	NumericMatrix m1, m2, result;
	
	for (int i = 0; i < NX; ++i)
	{
		for (int j = 0; j < NY; ++j)
		{
			m1[i][j] = i; m2[i][j] = j;
			result[i][j] = m1[i][j] + m2[i][j];
		}
	}

	print(m1); print(m2); print(result);

	return 0;
}
