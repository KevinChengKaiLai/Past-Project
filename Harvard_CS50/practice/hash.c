#include <stdio.h>
#include <stdlib.h>


typedef struct stack
{
    int* cap;
    int top;
}stack;



int main(void)
{

    stack s;
    s.top = 1;
    s->cap = 5;
    return 0;
}

// quene FIFO -> First in First out
// stack LIFO -> Last in First out