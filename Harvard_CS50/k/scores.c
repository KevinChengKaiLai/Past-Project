#include <stdio.h>

int main(void)
{
    // int score1 = 72;
    // int score2 = 73;
    // int score3 = 33;

    int scores[3];
    scores[0] = 1 ;
    scores[1] = 2 ;
    scores[2] = 3 ;
    printf("Average: %f\n", (scores[1]+ scores[2]+ scores[0])/(float)3.0);
}