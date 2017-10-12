import re, csv, yaml
from nltk.corpus import wordnet
from nltk.metrics import edit_distance

##################################################
## Replacing Words Matching Regular Expressions ##
##################################################

replacement_patterns = [
	(r'won\'t', 'will not'),
	(r'can\'t', 'cannot'),
	(r'i\'m', 'i am'),
	(r'ain\'t', 'is not'),
	(r'(\w+)\'ll', '\g<1> will'),
	(r'(\w+)n\'t', '\g<1> not'),
	(r'(\w+)\'ve', '\g<1> have'),
	(r'(\w+)\'s', '\g<1> is'),
	(r'(\w+)\'re', '\g<1> are'),
	(r'(\w+)\'d', '\g<1> would'),
]

class RegexpReplacer(object):
	""" Replaces regular expression in a text.
	>>> replacer = RegexpReplacer()
	>>> replacer.replace("can't is a contraction")
	'cannot is a contraction'
	>>> replacer.replace("I should've done that thing I didn't do")
	'I should have done that thing I did not do'
	"""
	def __init__(self, patterns=replacement_patterns):
		self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
	
	def replace(self, text):
		s = text
		
		for (pattern, repl) in self.patterns:
			s = re.sub(pattern, repl, s)
		
		return s