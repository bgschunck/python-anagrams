# Program for computing permutations of letters in words

from itertools import permutations
from nltk.corpus import wordnet

if __name__== "__main__":
	import sys
	for word in sys.argv[1:]:
		#print word
		for p in permutations(word):
			string = ''.join(p)
			#print string
			if wordnet.synsets(string): print string
			
