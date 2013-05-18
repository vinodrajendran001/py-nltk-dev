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
  pickle.dump(tagged_words, file('tagged_words.txt', 'w'))

  # extract & tokenize each sentence separately
  print "Tokenizing & tagging sentences..."
  sentences = nltk.tokenize.sent_tokenize(article.text)
  pickle.dump(sentences, file('sentences.txt', 'w'))
  tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences]
  tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]
  pickle.dump(tagged_sentences, file('tagged_sentences.txt', 'w'))
else:
  tagged_sentences =  pickle.load(file('tagged_sentences.txt', 'r'))
  tagged_words =  pickle.load(file('tagged_words.txt', 'r'))
  sentences =  pickle.load(file('sentences.txt', 'r'))

# show the output
print utils.join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80

instance  = ner.NERFinder()
people = instance.find(tagged_words, sentences, tagged_sentences)

# chunk the sentences
cp = regexp.CustomChunker()
start, end = 0, 15 # show sentences indexed from start to end
for index, sentence in enumerate(tagged_sentences):
	chunked_sentence = cp.parse(sentence) # nltk.chunk.ne_chunk(sentence)
	if index < end and index >= start:
		print "[",index,"] oooo", sentences[index]
		print
		print "[",index,"] ####", chunked_sentence
	
