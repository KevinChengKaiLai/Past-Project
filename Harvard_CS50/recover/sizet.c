#include <stdio.h>

int main() {
    size_t array_size = 10; // Represents the size of an array
    size_t element_size = sizeof(int); // Represents the size of an integer in bytes

    printf("Array size: %zu\n", array_size);
    printf("Size of int: %zu bytes\n", element_size);

    return 0;
}
