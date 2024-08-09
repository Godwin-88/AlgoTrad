#include <stdio.h>

#define MAX_LINE_LENGTH 1024  // Define a maximum line length

int main() {
    int c;  // Variable to store the input character
    char buffer[MAX_LINE_LENGTH];  // Buffer to store the input line
    int index = 0;  // Index for the buffer

    printf("Enter text (Press Ctrl+A to exit):\n");

    while (1) {
        c = getchar();  // Read a character from the keyboard

        // Check for Ctrl+A (ASCII value 1) to terminate the program
        if (c == 1) {
            printf("CTRL + A is a correct ending.\n");
            break;
        }

        // Check for Enter key (newline character) to display the buffered line
        if (c == '\n' || index >= MAX_LINE_LENGTH - 1) {
            buffer[index] = '\0';  // Null-terminate the string
            printf("%s\n", buffer);  // Display the entered line
            index = 0;  // Reset the buffer index for the next line
        } else {
            buffer[index++] = (char)c;  // Store the character in the buffer
        }
    }

    return 0;
}
