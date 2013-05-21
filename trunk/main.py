import nltk, data, summarize, pickle, ner, config, training, sys, utils, action

from nltk.tree import Tree

MAX_SENTENCES = config.MAX_SENTENCES

# load article text
path = "db/ivonyte-aiste/2011-7-8-1.txt" 
article = data.Article(path)
utils.load_data(article.text)

# show article text
print "-"*80
print article.text
print "-"*80

# make the summary & show in console
print "I Summary:"
instance = summarize.SimpleSummarizer()
print instance.summarize(article.text, MAX_SENTENCES)
print "-"*80

print "II Summary:"
print "Will be done soon :) "
print "-"*80

#print "Tokenizing article words..."
# tokenize & tag all words in article
#tokens = nltk.tokenize.wordpunct_tokenize(article.text)
#tagged_words = nltk.pos_tag(tokens)

# extract & tokenize each sentence separately
#print "Tokenizing sentences..."
#sentences = nltk.tokenize.sent_tokenize(article.text)
#tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences] 
#tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]

print "People and their actions:"
#instance  = ner.NERFinder()
#people = instance.find(utils.tagged_words, utils.sentences, utils.tagged_sentences)
work = action.Actions().find(utils.tagged_words, utils.tagged_sentences, utils.people)
# print the updated info with people actions
for i, (key, value) in enumerate(work.items()):
	print "[%d] - %s = %s"%(i+1, key, value)
print "-"*80

print "People interactions:"
print "Will be done soon too ! "
print "-"*80

