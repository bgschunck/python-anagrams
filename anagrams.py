# Program for computing permutations of letters in words

from itertools import permutations
#from nltk.corpus import wordnet
from nltk.corpus import words
import random


# debug_count = 10


def stringify(list):
    """Convert list of characters into a string."""
    return ''.join(list)


def lookup(word):
    """Return true of the word is in the dictionary."""
    return word in words.words()
    

def prefix_algorithm(phrase, verbose=False, debug=False):
    """Brute force algorithm that finds a prefix of the phrase in the dictionary."""
    
    if verbose: print("Phrase: %s" % phrase)

    # Terminate the recursion and return the anagram phrase?
    #if len(phrase) == 0: return [' '.join(word_list)]
    
    # Initialize the list for collecting the anagrams found at this level in the recursion
    anagram_result_list = []
    
    # Randomize the original phrase (the anagram does not likely start with a prefix of the original phrase)
    # if len(word_list) == 0:
        # phrase_list = list(phrase)
        # random.shuffle(phrase_list)
        # phrase = ''.join(phrase_list)
        # if debug: print("Shuffled: %s" % phrase)
    
    # Initialize the list of prefix words for this level in the recursion
    prefix_word_list = []
    
    # Check each permutation of the input phrase
    for p in permutations(phrase):
        
        # Convert the list of permuted letters into a string
        string = ''.join(p)
        if debug: print("Prefix: %s" % string)
        
        # global debug_count
        # if debug_count == 0: return
        # debug_count -= 1
        
        # Look for a prefix of the permutation that is a valid word
        for length in reversed(range(len(string))):
            # Split the string into two words
            (word, remainder) = (stringify(string[:length+1]), stringify(string[length+1:]))
            
            if debug: print("Word: %s, remainder: %s" % (word, remainder))
            
            # Found this word already?
            if not word in prefix_word_list:
                # Find anagram phrases (one or more words) in the remainder
                partial_anagram_list = suffix_algorithm(word, remainder, verbose, debug)
                
                if debug: print("Partial anagram list: %s" % partial_anagram_list)
                
                # Found any anagrams in the word and remainder?
                if partial_anagram_list:
                    anagram_result_list.append(partial_anagram_list)
                    
                # Add this word to the list of words already processed
                prefix_word_list.append(word)
                    
    return anagram_result_list


def suffix_algorithm(word, remainder, verbose=False, debug=False):
    """Look for anagrams in the remainder if the word is a anagram."""
    if lookup(word):
        if remainder:
            # Apply the prefix algorithm to the remaining characters in the permutation
            #partial_anagram_list = prefix_algorithm(remainder, verbose, debug)
            partial_anagram_list = single_word_anagram(remainder, verbose, debug)
            partial_anagram_list = [[partial_anagram] for partial_anagram in partial_anagram_list]
            
            # Did the recursion return anything?
            if partial_anagram_list:
                # Prepend the word onto each list of anagrams found in the remainder
                return [word + stringify(partial_anagram) for partial_anagram in partial_anagram_list]
        else:
            return [word]
            
    return None


def single_word_anagram(phrase, verbose=False, debug=False):
    """Compute the single-word anagrams of the input word."""
    
    anagram_list = []
    
    for p in permutations(phrase):
        # Convert the list of permuted letters into a string
        word = ''.join(p)
        
        # Skip this word if it is the input word or has already been found
        if word == phrase or word in anagram_list:
            if debug: print("Skipping word: %s" % word)
            continue
            
        if debug:
            print("Candidate word: %s" % word)
            
        if lookup(word):
            anagram_list.append(word)
            
    if debug: print("anagram_list: %s" % anagram_list)
    
    return anagram_list


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser('Compute anagrams of phrase entered on the command line')
    parser.add_argument('phrase', nargs='+', help='phrase to check for anagrams (words separated by spaces')
    parser.add_argument('-w', '--word', action='store_true', help='each anagram is a single word')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
    parser.add_argument('-e', '--debug', action='store_true', help='enable debugging output')
    args = parser.parse_args()
    
    phrase = ''.join(args.phrase).lower()
    if args.verbose: print("Entire phrase: %s" % phrase)
    
    if args.word:
        anagram_list = single_word_anagram(phrase, args.verbose, args.debug)
    else:
        anagram_list = prefix_algorithm(phrase, args.verbose, args.debug)

    print("Anagrams: %s" % anagram_list)
    
