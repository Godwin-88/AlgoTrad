// TestAggregates.cpp
//
// Defining aggregate structures. We model data that pertains to
// plain options. The struct can be used in pricing algorithms as a 
// simple data store.
//
// DJD
//

#include <stdlib.h>
#include "OptionData.hpp"
//Includes the stdlib.h for memory management functions and OptionData.hpp for the OptionData structure.
int main()
{

	// Create a single object on the heap
	int n = 1;
	OptionData* myData = (OptionData*)malloc(n * sizeof(OptionData)); // cast void* to OptionData*
	
	(*myData).K = 100.0;
	(*myData).T = 1.0;
	(*myData).r = 0.12;
	(*myData).sig = 0.1;
	(*myData).D = 0.03;
	(*myData).beta = 0.1;
	(*myData).type = +1;

	//print(*myData);

	// Create multiple objects on the heap
	n = 4;
	//OptionData* myDataArray = (OptionData*)malloc(n * sizeof(OptionData));
	OptionData* myDataArray = new OptionData[n];

	// Initialise the array
	for (int j = 0; j < n; ++j)
	{
		myDataArray[j] = *myData;

		// Modify expiry
		myDataArray[j].T = double (j) + 0.5;
	}

	// Print the array
	for (int j = 0; j < n; ++j)
	{
	//	print(myDataArray[j]);
	}

	// Deallocate memory
	free(myData);//The memory allocated for the single object is deallocated using free. This should not call the destructor since free does not invoke the destructor in C++.
//	free(myDataArray);
	delete [] myDataArray;//The memory allocated for the array of objects is deallocated using delete[]. This correctly calls the destructor for each object in the array, ensuring proper cleanup

	//double d = 1/2;
	//cout << d;

	return 0;
}
//Important Points
//Destructor Usage:

//The destructor ~OptionData() outputs a message when an OptionData object is destroyed. This is useful for tracking when objects are deleted, especially when using dynamic memory allocation.
//Memory Management:

//The program demonstrates two methods for dynamic memory management:
//malloc/free: A C-style approach to memory allocation that does not call constructors or destructors.
//new/delete: A C++-style approach that correctly calls constructors when allocating and destructors when deallocating memory.
//Potential Issues:

//If you were to uncomment the free(myDataArray);, it would be incorrect because free does not call destructors. Instead, delete[] should be used for memory allocated with new.
//Printing and Commenting:

//The print statements are commented out, but when uncommented, they would print the contents of each OptionData object in the array.