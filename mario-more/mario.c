#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;
    do
    {
        height = get_int("how high do you want the pyramid?: ");
    }
    while (height < 1 || height > 8);

    //new row per loop
    for (int i = 1; i <= height; i++)
    {
        //make indentation for first half
        for (int j = height; j > i; j--)
        {
            printf(" ");
        }
        //draw first half
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }
        //make seperation space
        printf("  ");
        //draw second half
        for (int l = 1; l <= i; l++)
        {
            printf("#");
        }
        //switch to next row
        printf("\n");
    }
}