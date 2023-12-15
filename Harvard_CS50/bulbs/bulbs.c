#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdlib.h>


const int BITS_IN_BYTE = 8;

void print_bulb(int bit);
// int* ToBinary(int ASCII);

int main(void)
{
    string message = get_string("Message: ");
    int length = strlen(message);

    for (int i = 0; i < length; i++)
    {
        int ASCII =  message[i];

        int BinaryArray[8] = {0,0,0,0,0,0,0,0} ;

        for (int j = 0; j < 8; j++)
        {
            BinaryArray[j] = ASCII % 2;
            ASCII = ASCII / 2;
        }
        for (int j = 0; j < 8; j++)
        {
            print_bulb(BinaryArray[7-j]);
        }

        printf("\n");
    }

}

// int* ToBinary(int number)
// {
//     int BinaryArray[8] = {0,0,0,0,0,0,0,0} ;

//     for (int i = 0; i < 8; i++)
//     {
//         BinaryArray[i] = number % 2;
//         number = number / 2;
//     }

//     return BinaryArray;
// }




void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
