import nltk, data, summarize, pickle, ner
import config, training, sys, utils, regexp, references
from nltk.tree import Tree

# show commandline arguments
print "CLI:", sys.argv

path = "db/uktveris-tomas/2010-12-20-10.txt"
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
	
# show people in the article
for i, (key, value) in enumerate(people.items()):
	print "[%d] - %s = %s"%(i+1, key, value)

# find the references
refs = references.References().find(people, sentences, tagged_sentences)
print refs