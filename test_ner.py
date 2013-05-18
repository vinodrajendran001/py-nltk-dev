import nltk, data, summarize, pickle, ner, config, training, sys
from nltk.tree import Tree

WORDS_PICKLE = 'tagged_words.pickle'
SENTENCES_PICKLE = 'tagged_sentences.pickle'

# load article
print "CLI:",sys.argv
path = "db/ivonyte-aiste/2011-7-3-1.txt"
article = data.Article(path)

print "-"*80
print article.text
print "-"*80

print "Tokenizing article words..."
# tokenize & tag all words in article
tokens = nltk.tokenize.wordpunct_tokenize(article.text)
tagged_words = nltk.pos_tag(tokens)

# extract & tokenize each sentence separately
print "Tokenizing sentences..."
sentences = nltk.tokenize.sent_tokenize(article.text)
tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences] 
tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]


def join_tagged(tagged):
	s = ""
	for text, tag in tagged:
		s += " "+text+"/"+tag
	return s
	
# show the output
print join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80

# do the magic - find named entities
instance  = ner.NERFinder()
people = instance.find(tagged_words, sentences, tagged_sentences)