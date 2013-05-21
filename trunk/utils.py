import sys, pickle, nltk, ner

tagged_words = None
tagged_sentences = None
people = None
sentences = None

# A bunch of utils to make the life easier

def join_tagged(tagged):
	s = ""
	for text, tag in tagged:
		s += " "+text+"/"+tag
	return s

def load_data(article_text):
	global tagged_words, tagged_sentences, people, sentences
	# we give parameter to load everything from file and to save some time :) 
	if "-f" in sys.argv:
	  # tokenize & tag all words in article
	  print "Tokenizing & tagging words..."
	  tokens = nltk.tokenize.wordpunct_tokenize(article_text)
	  tagged_words = nltk.pos_tag(tokens)
	  pickle.dump(tagged_words, file('tagged_words.pickle', 'w'))

	  # extract & tokenize each sentence separately
	  print "Tokenizing & tagging sentences..."
	  sentences = nltk.tokenize.sent_tokenize(article_text)
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