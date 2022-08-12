#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int get_length(long c_number);
    int get_digit(long num, int placement);

    //get a valid input
    long number = 0;
    do
    {
        number = get_long("enter card number: ");
    }
    while (number < 1);

    //assigns the length of the number and sets the sum to 0
    int number_length = get_length(number);
    int sum = 0;

    //executes Luhn's algorithm.
    for (int i = number_length; i > 0; i--)
    {
        //adds up every other number starting from the last one
        if ((number_length - i) % 2 == 0)
        {
            sum += get_digit(number, i);
        }
        //dubbles every other number starting from the second last one and adds their digits to sum.
        else
        {
            int x = get_digit(number, i) * 2;
            int x_length = get_length(x);
            //splits the product and adds their igits to sum.
            for (int j = x_length; j > 0; j--)
            {
                sum += get_digit(x, j);
            }
        }
    }
    //checks for a valid number and hen type
    if (sum % 10 == 0)
    {
        int first_digit = get_digit(number, 1);
        int scnd_digit = get_digit(number, 2);
        int card_type = 10 * first_digit + scnd_digit;

        if ((card_type == 34 || card_type == 37) && number_length == 15)
        {
            //americanexpress
            printf("AMEX\n");
        }
        else if ((card_type == 51 || card_type == 52 || card_type == 53 || card_type == 54 || card_type == 55) && number_length == 16)
        {
            //mastercard
            printf("MASTERCARD\n");
        }
        else if (first_digit == 4 && (number_length == 13 || number_length == 16))
        {
            //visa
            printf("VISA\n");
        }
        else
        {
            //invalid
            printf("INVALID\n");
        }
    }
    else
    {
        //invalid
        printf("INVALID\n");
    }
}








int get_length(long c_number)
{
    int length = 0;
    //divides by 10 until the number becomes 0 (thanks to truncation) this way we know how many powers of 10 there are and so the length of the number.
    while (c_number > 0)
    {
        length++;
        c_number = c_number / 10;
    }
    //returns the found length of the number.
    return length;
}
//function to find the value of a specific digit, counting from left to right.
int get_digit(long num, int placement)
{
    int num_length = get_length(num);
    /*divides the number by 10 untill the desired digit is the unit. since it truncates that, everything behind "." becomes zero.
      afterwards it does the same untill it reaches the number before the desired digit, after truncation multiplies that by 10 and subtracts the two outputs.
    */
    long behind_digit = num / (long) pow(10, num_length - placement);
    long before_digit = (num / (long) pow(10, num_length - (placement - 1))) * 10;
    return behind_digit - before_digit;
}