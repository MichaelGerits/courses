import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit('Usage: python dna.py data.csv sequence.txt')
    # TODO: Read database file into a variable
    people_data = []
    csv_file = sys.argv[1]

    # get the namesof each kind of STR type
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        dict_from_csv = dict(list(reader)[0])
        # making a list from the keys of the dict
        column_names = list(dict_from_csv.keys())
        # pops 'name'from the type list
        column_names.pop(0)

    # dynamically fill in the people_data list from the csv regardless of the "width"
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for person in reader:
            for i in column_names:
                person[i] = int(person[i])
            people_data.append(person)

    # TODO: Read DNA sequence file into a variable
    txt_file = sys.argv[2]
    with open(txt_file) as sequence_string:
        sequence = sequence_string.readline()

    # TODO: Find longest match of each STR in DNA sequence
    STR_lengths = {}
    for i in column_names:
        STR_lengths[i] = longest_match(sequence, i)

    # TODO: Check database for matching profiles
    for person in people_data:
        if matching(column_names, person, STR_lengths) == True:
            name = person['name']
            print(f'{name}')
            return
    print('No match')
    return


def longest_match(sequence, subsequence):
    '''Returns length of longest run of subsequence in sequence.'''

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def matching(list, person, STR_dict):
    # for each STR type checks per person if the amount is the same
    # if each one is the same returns true, else returns false
    match_amount = 0
    for i in list:
        if STR_dict[i] == person[i]:
            match_amount += 1
    if match_amount == len(list):
        return True
    else:
        return False


main()
