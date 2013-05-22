import data, sys, utils, ph_reduction 

# load all required data
print "CLI:",sys.argv
path = "db/barkauskas-povilas/2011-04-11-5.txt"
article = data.Article(path)
article.show()
utils.load_data(article.text)

# show the output
print utils.join_tagged(utils.tagged_words)
print "-"*80
print utils.tagged_sentences
print "-"*80

# make the summary!
summary = ph_reduction.PhraseReductor().find(utils.tagged_sentences)
print "\n".join(summary)