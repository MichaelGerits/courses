// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100000;// more buckets take more space, but use less time

// Hash table
node *table[N];
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)//done and not fucked
{
    // TODO
    //hashes the word
    unsigned int hash_val = hash(word);
    node *cursor = table[hash_val];
    //follows the cursor through the linked list
    while (cursor != NULL)
    {
        //checks if we found the word
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)//done and not fucked
{
    // TODO: Improve this hash function
    unsigned int hash_val = 0;
    //adds all the ascii values of the upper case variants together
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash_val += (tolower(word[i]) - 'a');
    }
    hash_val %= N;
    return hash_val;
}
//func for adding a node to the hash table
bool add_node(char *word, int hash_val)//done and not fucked
{
    node *n = malloc(sizeof(node));
    if (n != NULL)
    {
        //adds node to the top of the stack
        strcpy(n->word, word);
        n->next = table[hash_val];
        table[hash_val] = n;
        return true;
    }
    return false;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)//done and not fucked
{
    //open dictionary
    FILE *dic = fopen(dictionary, "r");
    if (dic != NULL)
    {
        //read dic word by word
        char buffer[LENGTH + 1];
        while (fscanf(dic, "%s", buffer) != EOF)
        {
            //get the hash value of the word
            int placement = hash(buffer);
            //add the word in the right spot
            add_node(buffer, placement);
            word_count++;
        }
        fclose(dic);
        return true;
    }
    return false;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)//done and not fucked
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //loops through the hash table
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;
        while (cursor != NULL)
        {
            tmp = cursor;
            //sets cursor to the next node as not to lose it
            cursor = cursor->next;
            free(tmp);
        }
        free(cursor);
    }
    return true;
}


