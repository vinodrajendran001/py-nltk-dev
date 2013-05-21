import data, sys, utils, references, regexp

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

'''
	Asmenu saveikos (ATVEJAI):
		1) Ivardis, Tarinys, Ivardis
		2) Ivardis (THEY), Tarinys (anksciau pamineti vardaI)
		3) Objektas, Tarinys, Aplinkybe (su vardu)
'''

# find the references
refs = references.References().find(utils.people, utils.sentences, utils.tagged_sentences)
print refs # [PRP, fullname, sentence_index]

chunked = regexp.CustomChunker().parse(utils.tagged_words)
#print chunked

#TODO: parse chunked text for PRP and - 3, 
# find PRP, VRB, PRP for - 1
# memory for people (they) - 2
# utility to check if person is mentioned in sentence & find it (see references.py)
for index, sentence in enumerate(utils.tagged_sentences):
	prp = [] # gather PRP into a list
	for word, tag in sentence:
		if tag.startswith("PRP"):
			print word
			prp.append([word, tag])
	print prp
		
	
		