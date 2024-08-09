#include <stdio.h>

// Function to print the day name given a day number (1-7)
void DayName(int dayNumber) {
    // Array of strings where each string represents a day of the week
    const char *daysOfWeek[7] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

    // Check if the day number is within the valid range
    if (dayNumber < 1 || dayNumber > 7) {
        printf("Invalid day number. Please enter a number between 1 and 7.\n");
    } else {
        // Print the corresponding day name
        printf("Day %d is a %s\n", dayNumber, daysOfWeek[dayNumber - 1]);
    }
}

int main() {
    int dayNumber;

    // Ask the user to enter a day number
    printf("Enter a day number (1-7): ");
    scanf("%d", &dayNumber);

    // Call the DayName function with the input day number
    DayName(dayNumber);

    return 0;
}
