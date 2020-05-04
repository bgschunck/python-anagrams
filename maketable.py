#!/usr/bin/env python
#
# Script to build a table for fast lookup of anagrams
#
# TODO: Make a class for the anagram table maker with the table as a member variable

from nltk.corpus import words
import yaml


# Define global for the anagram dictionary
anagram_dict = {}


def canonical(string):
    """Return the string in canonical format: Lowercase without leading or trailing whitespace."""
    return string.strip().lower()


def stringify(list):
    """Convert a list of characters into a canonical string."""
    return canonical(''.join(list))


def anagram_key(word):
    """Return the anagram dictionary key for the specified word."""
    return stringify(sorted(word))


def make_anagram_table(limit=0):
    """Make a table of anagrams indexed by the anagram key."""

    for word in words.words():

        # Terminate if the dictionary limit has been reached
        if limit > 0 and len(anagram_dict) >= limit: break

        # Anagram keys and words are lowercase
        word = canonical(word)

        key = anagram_key(word)
        if key in anagram_dict:
            # Is this word already in the anagram table?
            if not word in anagram_dict[key]:
                # Append the new word onto the list of words with this key
                anagram_dict[key].append(word)
        else:
            # Create a new list in the anagram dictionary for this key
            anagram_dict[key] = [word]


def print_anagram_table():
    """Print the anagram table."""

    for key, word_list in anagram_dict.items():
        print(key, word_list)


def save_anagram_table(anagram_table, pathname):
    """Save the anagram table to the specified file."""

    with open(pathname, 'w') as output:
        output.write(yaml.dump(anagram_table))


def load_anagram_table(pathname):
    """Load the anagram table from the specified file."""

    with open(pathname) as input:
        return yaml.load(input, Loader=yaml.FullLoader)


if __name__ == "__main__":

    # Start with an enpty anagram table
    anagram_dict.clear()

    # Make the anagram table with no limit in the number of entries
    make_anagram_table()

    # Save the anagram table
    save_anagram_table(anagram_dict, "anagram.yaml")
