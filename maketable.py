#!/usr/bin/env python
#
# Script to build a table for fast lookup of anagrams
#
# TODO: Make a class for the anagram table maker with the table as a member variable
#
# TODO: Add support for JSON format

from nltk.corpus import words
import yaml
import json
import os


class AnagramTable():
    """Table of anagrams supporting fast lookup to quickly determine whether a word is an anagram."""

    def __init__(self):
        self.anagram_dict = {}

    @staticmethod
    def canonical(string):
        """Return the string in canonical format: Lowercase without leading or trailing whitespace."""
        return string.strip().lower()

    @staticmethod
    def stringify(list):
        """Convert a list of characters into a canonical string."""
        return AnagramTable.canonical(''.join(list))

    @staticmethod
    def anagram_key(word):
        """Return the anagram dictionary key for the specified word."""
        return AnagramTable.stringify(sorted(word))

    def make_anagram_table(self, limit=0):
        """Make a table of anagrams indexed by the anagram key."""

        self.anagram_dict.clear()

        for word in words.words():

            # Terminate if the dictionary limit has been reached
            if limit > 0 and len(anagram_dict) >= limit: break

            # Anagram keys and words are lowercase
            word = self.canonical(word)

            key = self.anagram_key(word)
            if key in self.anagram_dict:
                # Is this word already in the anagram table?
                if not word in self.anagram_dict[key]:
                    # Append the new word onto the list of words with this key
                    self.anagram_dict[key].append(word)
            else:
                # Create a new list in the anagram dictionary for this key
                self.anagram_dict[key] = [word]

    def print_anagram_table(self):
        """Print the anagram table."""

        for key, word_list in self.anagram_dict.items():
            print(key, word_list)

    def save_anagram_table(self, pathname):
        """Save the anagram table to the specified file."""

        filetype = os.path.splitext(pathname)[1][1:].lower()

        with open(pathname, 'w') as output:
            if filetype == 'yaml':
                output.write(yaml.dump(self.anagram_dict))
            elif filetype == 'json':
                output.write(json.dumps(self.anagram_dict, indent=2) + '\n')
            else:
                exit("Unknown filetype: %s" % filetype)

    def load_anagram_table(self, pathname):
        """Load the anagram table from the specified file."""

        filetype = os.path.splitext(pathname)[1][1:].lower()

        with open(pathname) as input:
            if filetype == 'yaml':
                self.anagram_dict = yaml.load(input, Loader=yaml.FullLoader)
            elif filetype == 'json':
                self.anagram_dict = json.load(input)
            else:
                exit("Unknown filetype: %s" % filetype)

if __name__ == "__main__":

    # Create an anagram table
    anagram_table = AnagramTable()

    # Make the anagram table with no limit in the number of entries
    anagram_table.make_anagram_table()

    # Save the anagram table
    anagram_table.save_anagram_table("anagram.json")
