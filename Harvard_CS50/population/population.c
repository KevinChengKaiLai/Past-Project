#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    long Start;
    do
    {
        Start = get_long("Start size :");
    }
    while (Start < 9);
    // printf("Start size : %i\n", Start);

    // TODO: Prompt for end size
    long End;
    do
    {
        End = get_long("End size :");
    }
    while (End < Start);
    // printf("End size : %i\n", End);

    // TODO: Calculate number of years until we reach threshold
    long year = 0;
    while(Start < End)
    {
        long grow = Start / 3; // Use floating-point division
        long die = Start / 4;  // Use floating-point division
        Start = Start + grow - die;
        year++;
        // printf("current population : %li\n", Start);
    }
    // TODO: Print number of years
    printf("Years: %li", year);
}
