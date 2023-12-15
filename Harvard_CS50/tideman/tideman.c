#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count ;
int candidate_count;
int voter_count;
int iter_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
            if (vote(j, name, ranks))
            {
                continue;
            }
        }
        // for (int k = 0; k < candidate_count; k++)
        // {
        //     printf("%i\n",ranks[k]);
        // }

        record_preferences(ranks);

        printf("\n");
    }
    // for (int a = 0; a < candidate_count; a++)
    // {
    //     for (int b = 0; b < candidate_count; b++)
    //     {
    //         printf("%i ", preferences[a][b] );
    //     }
    //     printf("\n");
    // }

    add_pairs();
    sort_pairs();
    // for (int k = 0; k < pair_count; k++)
    // {
    //     printf("winner_after : %i\n" ,pairs[k].winner);
    //     printf("loser_after : %i\n" ,pairs[k].loser);
    // }
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name,candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        //  3 = ranks[i] 0 = ranks[j]
        {
            preferences[ranks[i]][ranks[j]] += 1;
        }
    }
    return;

}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (i == j)
            {
                continue;
            }
            //（認為i > j的人)  > (認為 j > i的人)
            else if (preferences[i][j] >  preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count += 1;
            }
        }
        iter_count = pair_count;
    }
    // for (int k = 0; k < pair_count; k++)
    // {
    //     printf("winner : %i\n" ,pairs[k].winner);
    //     printf("loser : %i\n" ,pairs[k].loser);
    // }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // dead function
    if (iter_count == 1)
        return;
    // create a space to store value temperary
    pair temp;
    // pairs[pair_count]
    // check the strength of each pair
    for (int i = 0; i < iter_count - 1; i++)
    {
        int win = pairs[i].winner;
        int lose = pairs[i].loser;
        int win2 = pairs[i+1].winner;
        int lose2 = pairs[i+1].loser;
        if (preferences[win][lose] < preferences[win2][lose2])
        {
            temp = pairs[i];
            pairs[i] = pairs[i+1];
            pairs[i+1] = temp;
        }
    }
    iter_count = iter_count - 1;
    sort_pairs();

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // printf("%d\n", pair_count);
    // pairs[big to small]
    // bool locked[MAX][MAX];
    for (int i = 0; i < pair_count; i++)
    {
        int win = pairs[i].winner;
        int lose = pairs[i].loser;
        locked[win][lose] = true;
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int compare[candidate_count] ;
    for (int i = 0; i < candidate_count; i++)
    {
        compare[i] = 0;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j] == 1)
            {
                compare[i] += 1;
            }
            // printf("%d ", locked[i][j]);
        }
        // printf("\n");
        // printf("Compare %d = %d\n", i,compare[i]);
    }
    int biggest = 0;
    int index = 0;
    for (int i = 0; i < candidate_count ; i++)
    {
        if (compare[i] > biggest)
        {
            biggest = compare[i];
        }
    }
    for (int j = 0; j < candidate_count ; j++)
    {
        if (compare[j] == biggest)
        {
            printf("%s\n", candidates[j] );
        }
    }

    // int length = candidate_count;
    // int temp;
    // for (int i = 0; i < candidate_count - 1; i++)
    // {
    //     if (compare[i] < compare[i + 1])
    //     {
    //         temp = compare[i];
    //         compare[i] = compare[i + 1];
    //         compare[i + 1] = temp;
    //     }
    // }


    return;
}