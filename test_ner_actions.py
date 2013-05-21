import data, sys, utils, action

# load all required data
print "CLI:",sys.argv
path = "db/ivonyte-aiste/2011-7-3-1.txt"
article = data.Article(path)
article.show()
utils.load_data()

# show the output
print utils.join_tagged(utils.tagged_words)
print "-"*80
print utils.tagged_sentences
print "-"*80

# show people in the article
for i, (key, value) in enumerate(utils.people.items()):
	print "[%d] - %s = %s"%(i+1, key, value)

print "Searching for people actions..."
work = action.Actions().find(utils.tagged_words, utils.tagged_sentences, utils.people)

print "-"*80
print "Actions found:"

# print the updated info with people actions
for i, (key, value) in enumerate(work.items()):
	print "[%d] - %s = %s"%(i+1, key, value)
