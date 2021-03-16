# Assignment 3: Read a text file and generate the following information:
#   1) Total word count (number of words in the file)
#   2) Total stopword count (number of stopwords in the file)
#   3) List of words, and their frequencies, that occur > 3 times

# this import is needed to reference the punctuation to be removed in the normalize_text function
import string


# Main logic that calls the functions for this program. Do NOT modify.
def main():
    stopwords_list = create_stopwords_list()
    word_frequencies = calculate_word_frequencies(stopwords_list)
    display_results(word_frequencies)


# Open and read the stopwords.txt file.
# Each line in the file contains a stopword to be added to the stopwords list.
def create_stopwords_list():
    try:
        filename = 'stopwords.txt'
        # open file
        sword = open(filename, 'r')
        # create list
        stop_word = []
        # add stopwords to the list
        for word in sword:
            stop_word.append(word.strip())
        # print('This is the list', stop_word)
        sword.close()

        # exception handlers
    except FileNotFoundError as err:
        print('Error: cannot find file.')
        print('Error:', err)
    except OSError as err:
        print('Error: cannot access file.')
        print('Error:', err)
    except ValueError as err:
        print('Error: invalid data found in file.')
        print('Error:', err)
        # catch all error handler, if the above handlers do not apply
    except Exception as err:
        print('An unknown error occurred')
        print('Error:', err)

    return stop_word


# This function creates a word_frequencies dictionary where
#   key = word from the file
#   value = frequency, i.e., the number of times the word appears in the file
# Open and read the LearnToCode_LearnToThink.txt file.
# Call normalize_text for each line in the file to obtain a list of the normalized words in the line.
# For each word, either increment its frequency in the dictionary,
#  or increment the stopword counter if the word is in the stopwords list.
# After reading the file, display the total number of words, and total number of stopwords.
def calculate_word_frequencies(stopwords):
    try:
        filename = 'LearnToCode_LearnToThink.txt'
        input_file = open(filename, 'r', encoding='utf8')
        # initialize counters
        count_total = 0
        count_sword = 0

        # create the word_frequencies dictionary
        word_freq = dict()

        for line in input_file:
            word_list = normalize_text(line)
            # print(line, word_list, '\n')   # Print the list of words to see what the data looks like
            for word in word_list:
                count_total += 1
                # exclude stopwords from frequency-counting
                if word in stopwords:
                    count_sword += 1
                    # count the frequency of keywords
                elif word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1

        # print output
        print('Total word count:', count_total)
        print('Total stopword count:', count_sword)
        # print(word_freq)
        input_file.close()

    # exception handlers
    except FileNotFoundError as err:
        print('Error: cannot find file.')
        print('Error:', err)
    except OSError as err:
        print('Error: cannot access file.')
        print('Error:', err)
    except ValueError as err:
        print('Error: invalid data found in file.')
        print('Error:', err)
        # potential key value errors for word_frequencies dictionary
    except KeyError as err:
        print('Error: invalid key value.')
        print('Error:', err)
        # catch all error handler, if the above handlers do not apply
    except Exception as err:
        print('An unknown error occurred')
        print('Error:', err)
    return word_freq


# Creates a list of words found in line_of_text using the split function.
# Removes leading/trailing punctuation from each word in the list.
# Converts each word to lower case, and returns the list of normalized words
# See assignment description for more information.
# Do NOT modify this function -- just call it, and use the list of words it returns.
def normalize_text(line_of_text):
    normalized_words = []  # Initialize the list
    line_of_text = line_of_text.strip()  # Remove any leading or trailing whitespace
    list_of_words = line_of_text.split()  # Create a list of words from the line_of_text
    for word in list_of_words:
        normalized_word = word.strip(string.punctuation).lower()  # Remove punctuation and lowercase the word
        if normalized_word:  # this statement is True if normalized_word is NOT an empty string ('')
            normalized_words.append(normalized_word)
    return normalized_words


# Sorts the dictionary of word_frequencies in descending order and
# displays those that have frequencies > 3.
# You do not need to change this function, it should work as is.
def display_results(word_frequencies):
    if word_frequencies:
        sorted_by_frequency = ((k, word_frequencies[k]) for k in
                               sorted(word_frequencies, key=word_frequencies.get, reverse=True))
        print("\nWords with frequencies > 3")
        print(format('KEYWORD', '<15'), format('FREQUENCY', '>12'))
        for k, v in sorted_by_frequency:
            if v > 3:
                print(format(k, '<12'), format(v, '>10'))
    else:
        print('No word frequencies found')


main()
