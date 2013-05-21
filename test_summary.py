# example of using the simple summarizer

import nltk, data, summarize, pickle, ner, config, training, sys
from nltk.tree import Tree

MAX_SENTENCES = config.MAX_SENTENCES

# load article text
path = "db/ivonyte-aiste/2011-7-8-1.txt" 
article = data.Article(path)

# show article text
print "-"*80
print article.text
print "-"*80

# make the summary & show in console
print "Summary:"
instance = summarize.SimpleSummarizer()
print instance.summarize(article.text, MAX_SENTENCES)