import nltk, data, summarize, pickle, ner, config, training, sys, utils, action
from nltk.tree import Tree

WORDS_PICKLE = 'tagged_words.pickle'
SENTENCES_PICKLE = 'tagged_sentences.pickle'

# load article
print "CLI:",sys.argv
path = "db/barkauskas-povilas/2011-04-02-4.txt"#"db/ivonyte-aiste/2011-7-3-1.txt"
article = data.Article(path)

print "-"*80
print article.text
print "-"*80

if "-w" in sys.argv:
	print "Tokenizing article words..."
	
	# tokenize & tag all words in article
	tokens = nltk.tokenize.wordpunct_tokenize(article.text)
	tagged_words = nltk.pos_tag(tokens)
	pickle.dump(tagged_words, file('tagged_words.pickle', 'w'))

	# extract & tokenize each sentence separately
	print "Tokenizing sentences..."
	sentences = nltk.tokenize.sent_tokenize(article.text)
	tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences] 
	tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]
	pickle.dump(tagged_sentences, file('tagged_sentences.pickle', 'w'))
	
	# do the magic - find named entities
	instance  = ner.NERFinder()
	people = instance.find(tagged_words, sentences, tagged_sentences)
	pickle.dump(people, file('people.pickle', 'w'))
else:
	print "Loading words from pickle..."
	tagged_words = pickle.load(file('tagged_words.pickle', 'r'))
	tagged_sentences = pickle.load(file('tagged_sentences.pickle', 'r'))
	people = pickle.load(file('people.pickle', 'r'))

# show the output
print utils.join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80

# show people in the article
for i, (key, value) in enumerate(people.items()):
	print i+1,":",key, value

print "Searching for people actions..."
work = action.Actions().find(tagged_words, tagged_sentences, people)

# print the updated info with people actions
for i, (key, value) in enumerate(work.items()):
	print i+1,":",key, "=", value
