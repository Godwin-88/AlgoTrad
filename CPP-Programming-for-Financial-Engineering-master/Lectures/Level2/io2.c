#include <stdio.h>
#include <stdlib.h>

#define MAX_LINE_LENGTH 1024  // Define a maximum line length

int main() {
    int c;  // Variable to store the input character
    char buffer[MAX_LINE_LENGTH];  // Buffer to store the input line
    int index = 0;  // Index for the buffer
    char filename[100];  // Buffer to store the filename
    FILE *file;  // File pointer

    // Ask the user to enter the filename
    printf("Enter the filename to write to: ");
    scanf("%99s", filename);

    // Open the file for writing
    file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    printf("Enter text (Press Ctrl+A to exit):\n");

    while (1) {
        c = getchar();  // Read a character from the keyboard

        // Check for Ctrl+A (ASCII value 1) to terminate the program
        if (c == 1) {
            fprintf(file, "CTRL + A is a correct ending.\n");
            break;
        }

        // Check for Enter key (newline character) to write the buffered line to the file
        if (c == '\n' || index >= MAX_LINE_LENGTH - 1) {
            buffer[index] = '\0';  // Null-terminate the string
            fprintf(file, "%s\n", buffer);  // Write the line to the file
            index = 0;  // Reset the buffer index for the next line
        } else {
            buffer[index++] = (char)c;  // Store the character in the buffer
        }
    }

    // Close the file
    fclose(file);

    return 0;
}
