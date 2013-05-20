import nltk, data, summarize, pickle, ner, config, training, sys, utils, regexp
from nltk.tree import Tree

# show commandline arguments
print "CLI:", sys.argv

path = "db/ivonyte-aiste/2011-7-3-1.txt"
article = data.Article(path)
print "-"*80
print article.text
print "-"*80

# we give parameter to load everything from file and to save some time :) 
if "-f" in sys.argv:
  # tokenize & tag all words in article
  print "Tokenizing & tagging words..."
  tokens = nltk.tokenize.wordpunct_tokenize(article.text)
  tagged_words = nltk.pos_tag(tokens)
  pickle.dump(tagged_words, file('tagged_words.pickle', 'w'))

  # extract & tokenize each sentence separately
  print "Tokenizing & tagging sentences..."
  sentences = nltk.tokenize.sent_tokenize(article.text)
  pickle.dump(sentences, file('sentences.pickle', 'w'))
  
  tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences]
  tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]
  pickle.dump(tagged_sentences, file('tagged_sentences.pickle', 'w'))
  
  print "Searching for people..."
  instance  = ner.NERFinder()
  people = instance.find(tagged_words, sentences, tagged_sentences)
  pickle.dump(people, file('people.pickle', 'w'))
else:
  tagged_sentences =  pickle.load(file('tagged_sentences.pickle', 'r'))
  tagged_words =  pickle.load(file('tagged_words.pickle', 'r'))
  sentences =  pickle.load(file('sentences.pickle', 'r'))
  people =  pickle.load(file('people.pickle', 'r'))

# show the output
print utils.join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80

def get_gender(word):
	if word.lower() in ("she", "her"): return "female"	
	if word.lower() in ("he", "him", "his"): return "male"
	return "?"
	
# show people in the article
for i, (key, value) in enumerate(people.items()):
	print "[%d] - %s = %s"%(i+1, key, value)

# --------------------------------------------------------------------------------------------
# Code below resolves references based on simple mentioned male/female entity memory scheme:
# 	1. parse every sentence for person & PRP 
#   2. determine person's sex & store him/her as last one mentioned (separate for male/female)
#   3. if PRP is found, then based on sex & last memorized person the PRP is assigned to the person name
# --------------------------------------------------------------------------------------------
	
# create a all possible lowercase names & drink beer later :P
names = {}
for i, (fullname, data) in enumerate(people.items()):
	for shortname in data['shortnames']:
		for s in shortname.lower().split(" "):
			names[s] = data
		names[shortname.lower()] = data
	for shortname in fullname.lower().split(" "):
		names[shortname] = data
	names[fullname.lower()] = data

# find names in text and mark them with special symbols & append additional data
new_tagged_sentences = []
for index, sentence in enumerate(tagged_sentences):
	sent = [] 
	for word, tag in sentence:
		key = word.lower() 
		if key in names:
			sent.append((word.lower(), tag, '+', names[key])) # add `+` to a name & include data
		else:
			sent.append((word.lower(), tag, 'o', None)) # not a name - mark as `o`
	new_tagged_sentences.append(sent)

# show debug texts
print new_tagged_sentences
print "-"*80
print article.text
print "-"*80

# store last he & she while scanning sentences, 
# if unknown sex name is found - store it also (determine type on first PRP found)
last_he = [None, 0] # store as: [people_data, word_index_in_text]
last_she = [None, 0]
last_unknown = [None, 0]
word_index = 0
for index, sentence in enumerate(new_tagged_sentences):	
	for element in sentence:
		word, tag, flag, data = element # unpack all data
		word_index += 1 # increase processed words index
		
		if tag.startswith("PRP") and len(word) <= 5: # reference was found!
			### unknown sex resolver
			if last_unknown[0]: # if we have an unknown name without sex, then assign the next first found sex to it
				gender = get_gender(word)
				print "Last unknown person -", last_unknown[0]['fullname'], "- was assigned sex:", gender
				last_unknown[0]['sex'] = gender
				
				# the hack has been fixed :P
				if gender == "male":
					if last_he[0]: # last `he` exists
						if last_he[1] < last_unknown[1]: # override if unknown is newer 
							last_he = last_unknown
					else:
						last_he = last_unknown # override as no `he` exists
				elif gender == "female":
					if last_she[0]:
						if last_she[1] < last_unknown[1]:
							last_she = last_unknown
					else:
						last_she = last_unknown

				if gender in ("male", "female"): # clear only if actualy determined
					last_unknown = [None, 0] # clear
			
			#### determine the person mentioned
			print "*"*80
			matched = None
			if word in ("he", "his", "him") and last_he[0]: # male
				matched = last_he
			elif word in ("she", "her") and last_she[0]: # female
				matched = last_she
			elif word in ("i", "me", "our"): # cannot determine sex - as multi
				if last_he[0] and last_she[0]: # we have both sex types in memory, choose the last one mentioned
					if last_he[1] > last_she[1]: # he is more fresh
						matched = last_he
					else: # she is more fresh
						matched = last_she
				elif last_he[0]: # we have only `he` in memory
					matched = last_he
				elif last_she[0]: # we have only `she` in memory
					matched = last_she
			
			if matched: # refresh index - this person has been just mentioned
				matched[1] = word_index
				print "REF[",word, "] is -", matched[0]['fullname'], "- in sentence Nr.", index+1
			else:
				print "REF[",word, "] is", "UNKNOWN", "in sentence Nr.", index+1
			print "\t", sentences[index] # show the corresponding sentence with the match
			
		elif flag == "+": # a word is a name, so put it into memory
			if data["sex"] == "male":
				#print "last_he =", data['fullname']
				last_he = [data, word_index]
			elif data["sex"] == "female":
				#print "last_she =", data['fullname']
				last_she = [data, word_index]
			elif data['sex'] == "?":
				#print "last_unknown =", data['fullname']
				last_unknown = [data, word_index]