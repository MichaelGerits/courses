# TODO
import sys


def main():
    while True:
        number = input("enter card number: ")
        if int(number) > 0:
            break

    if luhn_algo(number) == False:
        sys.exit("INVALID")

    card_type = int(number)
    while card_type >= 100:
        card_type = card_type // 10

    if (card_type == 34 or card_type == 37) and len(number) == 15:
        # americanexpress
        print("AMEX")
    elif (card_type == 51 or card_type == 52 or card_type == 53 or card_type == 54 or card_type == 55) and len(number) == 16:
        # mastercard
        print("MASTERCARD")
    elif card_type // 10 == 4 and (len(number) == 13 or len(number) == 16):
        # visa
        print("VISA")
    else:
        # invalid
        print("INVALID")


def luhn_algo(number):
    sum = 0
    length = len(number)

    for i in range(length):
        digit = int(number[i])
        # adds up every other number starting from the last one
        if (length - (i + 1)) % 2 == 0:
            sum += digit
        # dubbles every other number starting from the second last one and adds their digits to sum.
        else:
            x = str(digit * 2)
            # splits the product and adds their igits to sum.
            for j in range(len(x)):
                sum += int(x[j])
    if sum % 10 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    main()