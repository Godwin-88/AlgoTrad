#include <stdio.h>

// Define the Article structure
struct Article {
    int articleNumber;
    int quantity;
    char description[21];  // 20 characters plus one for the null terminator
};

// Function to print the contents of an Article
void Print(struct Article *p) {
    printf("Article Number: %d\n", p->articleNumber);
    printf("Quantity: %d\n", p->quantity);
    printf("Description: %s\n", p->description);
}

int main() {
    // Initialize an Article structure
    struct Article myArticle = {12345, 100, "Widget"};

    // Call the Print function to print the contents of the Article
    Print(&myArticle);

    return 0;
}
