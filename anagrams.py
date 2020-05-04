#!/usr/bin/env python
#
# Program for computing permutations of letters in words

from itertools import permutations
#from nltk.corpus import wordnet
from nltk.corpus import words
import random
from maketable import AnagramTable


# debug_count = 10

# Set of words that have been checked and are not anagrams
not_anagram_word_set = set()


def stringify(list):
    """Convert list of characters into a string."""
    return ''.join(list)


def indentation(level):
    """Return a string that indents output according to the recursion level."""
    #two_spaces = ' ' * 2
    two_periods = '.' * 2
    return two_periods * level
    

def lookup(word):
    """Return true if the word is in the dictionary.
    
    The anagram table contains all words in the dictionary, indexed by anagram key.
    If there is an entry in the anagram table for the anagram of the specified word,
    then the word is present in the dictionary. Usig the anagram table appears to be
    faster than looking up the word in the dictionary used to create the anagram table.
    """
    #return word in words.words()
    return anagram_table.is_anagram(word)
    

def randomize_string(string):
    """Return a random permutation of the input string."""
    characters = list(string)
    random.shuffle(characters)
    return stringify(characters)
    

def prefix_algorithm(phrase, verbose=False, debug=False, level=0):
    """Brute force algorithm that finds a prefix of the phrase in the dictionary.
    The verbose and debug flags control output. The level is the depth of the recusrion.
    """
    
    if verbose: print("%sprefix(phrase: %s)" % (indentation(level), phrase))
    
    # Initialize the list for collecting the anagrams found at this level in the recursion
    anagram_result_list = []
    
    # Initialize the list of prefix words for this level in the recursion
    prefix_word_list = []
    
    # Check each permutation of the input phrase
    for p in permutations(phrase):
        
        # Convert the list of permuted letters into a string
        string = stringify(p)
        if debug: print("%sprefix string: %s" % (indentation(level), string))
        
        # global debug_count
        # if debug_count == 0: return
        # debug_count -= 1
        
        # Look for a prefix of the permutation that is a valid word
        for length in reversed(range(len(string))):
            # Split the string into two words
            (word, remainder) = (stringify(string[:length+1]), stringify(string[length+1:]))
            
            if debug: print("%s(word: %s, remainder: %s)" % (indentation(level), word, remainder))
            
            # Found this word already?
            if not word in prefix_word_list:
                # Find anagram phrases (one or more words) in the remainder
                partial_anagram_list = suffix_algorithm(word, remainder, verbose, debug, level)
                
                if debug: print("%spartial anagram list: %s" % (indentation(level), partial_anagram_list))
                
                # Found any anagrams in the word and remainder?
                if partial_anagram_list:
                    anagram_result_list.append(partial_anagram_list)
                    
                # Add this word to the list of words already processed
                prefix_word_list.append(word)
                
    if verbose: print("%sprefix(phrase %s) -> %s" % (indentation(level), phrase, anagram_result_list))
    
    return anagram_result_list


def suffix_algorithm(word, remainder, verbose=False, debug=False, level=0):
    """Look for anagrams in the remainder if the specified word is a anagram."""

    # Skip words that have already been checked and are not anagrams
    if word in not_anagram_word_set: return None
    
    if lookup(word):
        if remainder:
            # Apply the prefix algorithm to the remaining characters in the permutation
            #partial_anagram_list = prefix_algorithm(remainder, verbose, debug, level+1)
            partial_anagram_list = single_word_anagram(remainder, verbose, debug)
            
            # Did the recursion return anything?
            if partial_anagram_list:
                # Prepend the word onto each anagrams found in the remainder
                return ['%s %s' % (word, stringify(partial_anagram)) for partial_anagram in partial_anagram_list]
        else:
            return [word]
            
    else:
        # Remember that this word is not an anagram
        not_anagram_word_set.add(word)
        
    return None


def single_word_anagram(phrase, verbose=False, debug=False):
    """Compute the single-word anagrams of the input word."""
    
    anagram_list = []
    
    for p in permutations(phrase):
        # Convert the list of permuted letters into a string
        word = stringify(p)
        
        # Skip this word if it is the input word or has already been found
        if word == phrase or word in anagram_list:
            if debug: print("Skipped word: %s" % word)
            continue
            
        if lookup(word):
            if debug: print("Add new word: %s" % word)
            anagram_list.append(word)
            
    if debug: print("*** Returning anagram list: %s" % anagram_list)
    
    return anagram_list


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser('Compute anagrams of phrase entered on the command line')
    parser.add_argument('phrase', nargs='+', help='phrase to check for anagrams (words separated by spaces')
    parser.add_argument('-t', '--table', default='anagram.json', help='table of anagrams')
    parser.add_argument('-w', '--word', action='store_true', help='each anagram is a single word')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
    parser.add_argument('-e', '--debug', action='store_true', help='enable debugging output')
    args = parser.parse_args()
    
    anagram_table = AnagramTable(args.table)
    
    phrase = stringify(args.phrase).lower()
    if args.verbose: print("Original phrase: %s" % phrase)
    
    # Randomize the original phrase (the anagram does not likely start with a prefix of the original phrase)
    phrase = randomize_string(phrase)
    if args.debug: print("Shuffled phrase: %s" % phrase)
    
    if args.word:
        # Use a simpler algorithm to find all anagrams of one word
        anagram_list = single_word_anagram(phrase, args.verbose, args.debug)
    else:
        # Find all anagrams of a phrase
        anagram_list = prefix_algorithm(phrase, args.verbose, args.debug)

    print("Anagrams: %s" % anagram_list)
    
