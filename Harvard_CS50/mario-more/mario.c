#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height : ");
    }
    while (height < 1 || height > 8);

    for (int i = height; i > 0; i--)
    {
        // print the space
        for (int j = i - 1; j > 0; j--)
        {
            printf(" ");
        }
        // print first section of "#"
        for (int j = i; j < height + 1; j++)
        {
            printf("#");
        }

        //middle bridge
        printf("  ");

        // print final "#"
        for (int j = i; j < height + 1; j++)
        {
            printf("#");
        }
        // next row
        printf("\n");
    }
}