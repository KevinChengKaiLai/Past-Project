#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)

{
    string text = get_string("Text: ");

    // count letter
    float letter_count = count_letters(text);
    // printf("the letter number is %i\n", letter_count);

    // count word
    float words_count = count_words(text);
    // printf("the words number is %i\n", words_count);

    // count sentence
    float st_count = count_sentences(text);
    // printf("the sentences number is %i\n", st_count);

    // do calculation
    float L = letter_count / words_count *100;
    float S = st_count / words_count *100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);

    // output score
    // printf("SCORE : %f\n", index);
    if (index >= 16)
    {
    printf("Grade 16+\n");
    }
    else if (index >=1)
    {
        printf("Grade %i\n", (int) index);
    }
    else
    {
        printf("Before Grade 1\n");
    }
    return 0;
}


int count_letters(string text)
{
    int LetterCount = 0;
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        if (isupper(text[i]) || islower(text[i]))
        {
            LetterCount += 1;
        }
        else
        {
            LetterCount += 0;
        }
    }
    return LetterCount;
}

int count_words(string text)
{
    int WordCount = 1;
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        if ( isblank(text[i]) )
        {
            WordCount += 1;
        }
        else
        {
            WordCount += 0;
        }
    }
    return WordCount;
}

int count_sentences(string text)
{
    int StCount = 0;
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))
        {
            StCount += 1;
        }
        else
        {
            StCount += 0;
        }
    }
    return StCount;
}
