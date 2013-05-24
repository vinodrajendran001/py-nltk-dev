import data, sys, utils, references, regexp, interactions

# show commandline arguments
print "CLI:", sys.argv

# load all data
path = "db/demo.txt"
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
print refs

# find people interactions
interact = interactions.Interactor().find(refs, utils.tagged_sentences)

print "-"*80
print "Interactions:"
print "-"*80

for index, item in enumerate(interact):
	who, prp, what = item['who'], item['prp'], item['what']
	s = "["+str(index+1)+"]:"
	for i in xrange(len(who)):
		if prp[i] and who[i]: s += " " + who[i] + "(" + prp[i] + "), "
		elif prp[i]: s += prp[i] + ", "
		elif who[i]: s += " " + who[i] + ", "
	s += " - " + ", ".join(what)
	print s