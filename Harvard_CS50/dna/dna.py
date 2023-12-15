import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv[:]) != 3:
        print("wrong argument number !!")
        sys.exit(1)

    # TODO: Read database file into a variable
    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        reader = csv.reader(csvfile)
        reader = list(reader)
        people_list = reader[1:]
        STR_list = reader[0][1:]
    # print('STR list = ',STR_list)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as txtfile:
        DnaSeq = txtfile.read()
    # print(DnaSeq)

    # TODO: Find longest match of each STR in DNA sequence
    compare_list = []
    for str in range(len(STR_list)):
        compare_list.append((longest_match(DnaSeq,STR_list[str])))
    # compare_list_str = []
    # for int in compare_list:
    #     compare_list_str.append(str(int))
    # print(compare_list)
    # TODO: Check database for matching profiles

    for people in people_list:
        # print('hihihihih')
        count = 0
        nopeople = True
        for STR_count in people[1:]:
            if int(STR_count) in compare_list:
                count = count + 1
                if count == len(compare_list):
                    nopeople = False
                    print(people[0])
    if nopeople:
        print("No match")ㄎ 
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

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


main()
