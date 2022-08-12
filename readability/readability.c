#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //gets the text from the user.
    string text = get_string("Text: ");

    //counts the number of words, letters and sentences.
    int letter_amount = count_letters(text);
    int word_amount = count_words(text);
    int sentence_amount = count_sentences(text);

    //calculates the necessary variables for the formula
    double L = (float) letter_amount / (float) word_amount * 100;
    double S = (float) sentence_amount / (float) word_amount * 100;

    //calculates the Coleman-Liau index
    int CL_index = round(0.0588 * L - 0.296 * S - 15.8);

    //set response if the index is above 16
    if (CL_index >= 16)
    {
        printf("Grade 16+\n");
    }

    //set response if index is below 1
    else if (CL_index < 1)
    {
        printf("Before Grade 1\n");
    }

    //output index(grade)
    else
    {
        printf("Grade %i\n", CL_index);
    }

}

//function to calculate the amount of letters by counting the amunt of letters ascii
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if ((text[i] >= 97 && text[i] <= 122) || (text[i] >= 65 && text[i] <= 90))
        {
            letters++;
        }
    }
    return letters;
}

//function to calculate the amount of words by counting the amount of spaces + 1
//this func also checks for any rouge spaces
int count_words(string text)
{
    int words = 1;
    if (text[0] == 32 || text[strlen(text) - 1] == 32)
    {
        printf("ERROR: be mindfull to have the right amount of spaces.");
        return -1;
    }
    else
    {
        for (int i = 0, n = strlen(text); i < n; i++)
        {
            if (text[i] == 32)
            {
                words++;
            }
        }
        return words;
    }
}

//function to calculate the amount of sentences by counting the amount of ".","!" and "?"
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}