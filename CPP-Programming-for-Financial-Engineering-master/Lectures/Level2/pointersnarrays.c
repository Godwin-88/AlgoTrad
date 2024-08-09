#include <stdio.h>

// Function to swap the values of two variables using pointers
void Swap(int* a, int* b)//This function takes two pointers to integers as arguments.

{
    int temp = *a;  // Store the value pointed to by a in temp
    *a = *b;        // Assign the value pointed to by b to the location pointed to by a
    *b = temp;      // Assign the value stored in temp to the location pointed to by b
}
//Effect: The values of the integers that a and b point to are swapped.
int main()
{
    int i = 123;
    int j = 456;

    // Print the values before swapping
    printf("Before Swap: i = %d, j = %d\n", i, j);

    // Call the Swap function
    Swap(&i, &j);

    // Print the values after swapping
    printf("After Swap: i = %d, j = %d\n", i, j);

    return 0;
}
