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

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
//setup----------------------------------------------
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
//----------------------------------------------------------
    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes (goes through each voter)
    for (int i = 0; i < voter_count; i++)
    {
        // initiates a new ranks array for each voter
        int ranks[candidate_count];

        // fills in the voter's ranks array
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        //uses the voter's ranks array to update the preferences matrix
        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
//checks if it's a valid vote then stores "candidates[i]"'s index in ranks[i]
bool vote(int rank, string name, int ranks[])// checked
{
    for (int can = 0; can < candidate_count; can++)
    {
        if (strcmp(name, candidates[can]) == 0)
        {
            ranks[rank] = can;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])// checked
{
    int row_ranks[candidate_count];
    int collumn_ranks[candidate_count];
    //finds the rank of each candidate in the voter's list
    for (int can = 0; can < candidate_count; can++)
    {
        //goes through ranks[] and returns the index of that array where the candidate is stored or their "rank"
        for (int rank = 0; rank < candidate_count; rank++)
        {
            if (ranks[rank] == can)
            {
                //stores the candidate's rank in two arrays which will e used to fill in the preference matrix
                row_ranks[can] = rank;
                collumn_ranks[can] = rank;
            }
        }
    }

    //loops through each row of the matrix
    for (int row = 0; row < candidate_count; row++)
    {
        //loops through each collumn of the row
        for (int collumn = 0; collumn < candidate_count; collumn++)
        {
            //if the candidate of the row is a higher rank than the collumn's => adds 1 to the selected element.
            if (row_ranks[row] < collumn_ranks[collumn])
            {
                preferences[row][collumn]++;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void) //(checked)
{
    //loops through each row of the matrix except for the last one
    for (int row = 0; row < candidate_count - 1; row++)
    {
        //loops through the collumns, but with each row skips one more in order to prevent checking the same pair again.
        for (int collumn = 1 + row; collumn < candidate_count; collumn++)
        {
            //checks wich candidate of the pair has the highest preference and stores their candidates[] index accordingly
            if (preferences[row][collumn] > preferences[collumn][row])
            {
                pair_count++;
                pairs[pair_count - 1].winner = row;
                pairs[pair_count - 1].loser = collumn;
            }
            else if (preferences[row][collumn] < preferences[collumn][row])
            {
                pair_count++;
                pairs[pair_count - 1].loser = row;
                pairs[pair_count - 1].winner = collumn;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        for (int j = 0; j < pair_count - 1; j++)
        {
            //gets the preference values of this and the next pair.
            int win_val_current = preferences[pairs[j].winner][pairs[j].loser];
            int loss_val_current = preferences[pairs[j].loser][pairs[j].winner];

            int win_val_next = preferences[pairs[j + 1].winner][pairs[j + 1].loser];
            int loss_val_next = preferences[pairs[j + 1].loser][pairs[j + 1].winner];
            //checks which pair had the strongest win and put's that one more foreward.
            if ((win_val_current - loss_val_current) < (win_val_next - loss_val_next))
            {
                pair temp_val = pairs[j];
                pairs[j] = pairs[j + 1];
                pairs[j + 1] = temp_val;

            }
        }
    }
    return;
}

// Test for cycle by checking arrow coming into each candidate
bool cycle(int end, int cycle_start)
{
    // Return true if there is a cycle created (Recursion base case)
    if (end == cycle_start)
    {
        return true;
    }
    // Loop through candidates (Recursive case)
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[end][i])
        {
            if (cycle(i, cycle_start))
            {
                return true;
            }
        }
    }
    return false;
}
// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Loop through pairs
    for (int i = 0; i < pair_count; i++)
    {
        // If cycle function returns false, lock the pair
        if (!cycle(pairs[i].loser, pairs[i].winner))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int collumns = 0; collumns < candidate_count; collumns++)
    {
        int false_count = 0;
        for (int rows = 0; rows < candidate_count; rows++)
        {
            if (locked[rows][collumns] == false)
            {
                false_count++;
            }
        }
        if (false_count == candidate_count)
        {
            printf("%s\n", candidates[collumns]);
            return;
        }
    }
    printf("FUCK\n");
    return;
}