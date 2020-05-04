# Record of work done on the Python project for anagrams

## Tasks

1. Continue work on anagram algorithms.


## Notes



## Logbook

### 2020-05-03

Modified the `anagrams.py` script to use a pre-built dictionary of word from the NLTK corpus indexed by anagram key.
The anagram key is formed from a word by sorting the letters in the word.
The `maketable.py` script reads the NLTK corpus and writes the anagram table to a YAML or JSON file.
The preferred file format is JSON because it provides a more readable representation of lists of words for each anagram key.
This seems to make the code run much faster.


### 2020-05-04

Created Visual Studio 2017 solution for the anagram.py script to use the debugger.

Visual Studio found the NLTK package even though it was installed in `$HOME\AppData\Roaming\Python\Python36\site-packages`
instead of `C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\lib\site-packages`

Was able to step through the code.

