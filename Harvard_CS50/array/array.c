#include <cs50.h>
#include <stdio.h>


int main(void)
{
    int size;
    do
    {
        size = get_int("Size: ");
    }
    while (size < 1);

    int twice[size];
    twice[0] = 1;
    printf("%i\n", twice[0]);

    for (int i = 1; i < size; i++)
    {
        twice[i] = 2 * twice[i - 1];
        printf("%i\n", twice[i]);
    }
}
