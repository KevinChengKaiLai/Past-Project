// Implements a dictionary's functionality
#include <stddef.h>
#include <ctype.h>
#include <stdbool.h>
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[26];




// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = toupper(word[0]) - 'A';
    node * cursor = table[index] ;

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;

}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    char dict_word[LENGTH+1];
    // TODO
    // load alphabet into hash table
//    for (int i = 0; i < N; i++)
//     {
//         table[i] = malloc(sizeof(node));
//         if (table[i] == NULL) {
//             // Handle memory allocation failure
//             return 1; // Exit with an error code
//         }
//         table[i]->next = NULL;
//     }

    // read dictionary
    FILE *dict = fopen(dictionary, "r");
    if (!dict)
    {
        printf("Error opening dictionary file!\n");
        return false;
    }

    // Add words to the hash table
    while (fscanf(dict, "%s", dict_word) == 1)
    {
        unsigned int index = hash(dict_word);
        node *new_word = malloc(sizeof(node));
        if (new_word == NULL)
        {
            printf("not enough memory for new words!");
            return false;
        }
        strcpy(new_word -> word, dict_word);
        new_word->next = table[index];
        table[index] = new_word;
    }
// WORDS MISSPELLED:     955
// WORDS IN DICTIONARY:  143091
// WORDS IN TEXT:        17756
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int count = 0;
    for (int i = 0; i < 26; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            count++;
            ptr = ptr->next;
        }
    }
    return count;


}

// Unloads dictionary from memory, returning true if successful, else false
void unload_node(node *cursor)
{
    if (cursor == NULL)
    {
        return;
    }
    unload_node(cursor->next); // Recursively free the next node
    free(cursor); // Free the current node
}

bool unload(void)
{
    for (int i = 0; i < 26; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        table[i] = NULL; // Set the head to NULL after unloading the list
    }
    return true;
}









// bool unload(void)
// {
//     // TODO
//     for (int i = 0; i < 26; i++)
//     {
//         node *cursor = table[i];
//         if (cursor == NULL)
//         {
//             return;
//         }
//         else if (cursor->next != NULL)
//         {
//             cursor = cursor->next;
//             unload();
//         }

//     }
//     return true;
// }





// int main(void)
// {
//     return 0;
// }