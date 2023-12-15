#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <cs50.h>



int main(int argc ,char *argv[])
{
    char *card_number = argv[1];
    int len = strlen(card_number);
    int sum = 0;
    bool double_digit = false;
    for (int i = len - 1; i >= 0; i--)
    {
        int digit = card_number[i] - '0';

        if (double_digit)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit = digit % 10 + 1;
            }
        }

        sum += digit;
        double_digit = !double_digit;
    }

    printf("%d\n", sum);
    return (sum % 10 == 0);
}


    //

