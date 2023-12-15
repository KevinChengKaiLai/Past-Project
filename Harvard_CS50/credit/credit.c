#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>


bool ValidTest(char *num_char);

int main(void)
{
    // prompt for card number

    string number = get_string("Number: ");
    char num_char[strlen(number) + 1];;
    for (int i = 0; i < strlen(number); i++)
    {
        num_char[i] = number[i];
        // printf("%c\n", num_char[i]);
    }

    // test the valid number
    if(ValidTest(num_char))
    {
        if (number[0] =='3' && (number[1]=='4' || number[1]=='7' ))
        {
            printf("AMEX\n");
        }
        else if(number[0] =='5' && (number[1]=='1' || number[1]=='2'|| number[1]=='3'
                                    || number[1]=='4'|| number[1]=='5' ))
        {
            printf("MASTERCARD\n");
        }
        else if(number[0] =='4')
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}


bool ValidTest(char *num_char)
{
    int len = strlen(num_char);
    int sum = 0;
    bool double_digit = false;
    for (int i = len - 1; i >= 0; i--)
    {
        int digit = num_char[i] - '0';
        // printf("i = %i\n", i);
        // printf("char = %c\n", num_char[i] );
        // printf("digit = %i\n", digit);

        if (double_digit)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit = digit % 10 + 1;
            }
        }
        // printf("digit = %i\n\n" ,digit);
        sum += digit;

        double_digit = !double_digit;
    }
    // printf("%d\n",sum);
    return (sum % 10 == 0);
}

