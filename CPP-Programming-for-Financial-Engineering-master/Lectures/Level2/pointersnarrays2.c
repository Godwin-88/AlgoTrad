#include <stdio.h>
#define MAXLINE 30

// Function to calculate the length of a string
int Length(char str[]) {//This function takes a character array (str) as an argument and returns the length of the string.
    int length = 0;

    // Iterate through the string until the null terminator is found
    while (str[length] != '\0') {
        length++;
    }

    return length;
}

int main() {
    char string[MAXLINE + 1]; // Line of maximum 30 chars + \0
    int c; // The input character
    int i = 0; // The counter

    // Print intro text
    printf("Type up to %d chars. Exit with ^Z\n", MAXLINE);

    // Get the characters
    while ((c = getchar()) != EOF && i < MAXLINE) {
        // Append entered character to string
        string[i++] = (char)c;
    }

    string[i] = '\0'; // String must be closed with \0

    // Call the Length function and print the string length
    printf("String length is %d\n", Length(string));

    return 0;
}
