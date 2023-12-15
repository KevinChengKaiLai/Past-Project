#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "helpers.h"


int main(void)
{
    int a = 5;
    int *Red = &a;
    *Red = 7 ;
    printf("Red is %p\n", &Red);


}