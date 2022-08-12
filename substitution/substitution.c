#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    string key = argv[1];
    //checks if the correct amount of arguments are put in
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    //checks if the key is the correct size
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    //converts "key" to lowercase sot that their is always a reliable foundation
    //then checks if it has any invalid keys
    for (int i = 0; i < 26; i++)
    {
        key[i] = tolower(key[i]);

        if (key[i] < 97 || key[i] > 122)
        {
            printf("invalid characters in key.");
            return 1;
        }
    }
    //checks if the key has any duplicates.
    for (int i = 0; i < 25; i++)
    {
        for (int j = (i + 1); j < 26; j++)
        {
            if (key[i] == key[j])
            {
                printf("no duplicate letters are allowed.");
                return 1;
            }
        }
    }

    //gets the word to be converted.
    string text = get_string("plaintext:  ");
    //encrypts the message
    int convers_index;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        //calculates the correct key index
        convers_index = tolower(text[i]) - 97;
        //if the character is lowercase
        if (text[i] >= 97 && text[i] <= 122)
        {
            text[i] = key[convers_index];
        }
        //if the character is an uppercase
        else if (text[i] >= 65 && text[i] <= 90)
        {
            text[i] = toupper(key[convers_index]);
        }
    }
    printf("ciphertext: ");
    printf("%s\n", text);
    return 0;
}