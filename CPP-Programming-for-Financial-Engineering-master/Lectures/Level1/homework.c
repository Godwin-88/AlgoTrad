#include <stdio.h>

int main()
{
    // Use printf() to print the required text on the screen
    printf("My first C-program\n");
    printf("is a fact!\n");
    printf("Good, isn’t it?\n");

    float base, height, surface_area;

    // Prompt the user to enter the base of the triangle
    printf("Enter the base of the triangle: ");
    scanf("%f", &base);

    // Prompt the user to enter the height of the triangle
    printf("Enter the height of the triangle: ");
    scanf("%f", &height);

    // Calculate the surface area of the triangle
    surface_area = 0.5 * base * height;

    // Output the result
    printf("The surface area of the triangle is: %.2f\n", surface_area);
    return 0;
}






