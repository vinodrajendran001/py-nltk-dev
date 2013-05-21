import data, sys, utils, action, references

# load all required data
print "CLI:",sys.argv
path = "db/ivonyte-aiste/2011-7-3-1.txt"
article = data.Article(path)
article.show()
utils.load_data(article.text)

# show the output
print utils.join_tagged(utils.tagged_words)
print "-"*80
print utils.tagged_sentences
print "-"*80
	
# show people in the article
for i, (key, value) in enumerate(utils.people.items()):
	print "[%d] - %s = %s"%(i+1, key, value)

# find the references
refs = references.References().find(utils.people, utils.sentences, utils.tagged_sentences)

print "-"*80
print "References found (ref, fullname, sentence_index):"
print refs