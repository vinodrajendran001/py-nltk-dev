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

article.show()

names = utils.get_names_dict(utils.people)

# TODO: parse chunked text for PRP - 3
# 		find PRP/name, VRB, PRP/name for - 1
# 		memory for people: name/name/name/... (they did) - 2
print "Interactions:" 

for index, sentence in enumerate(utils.tagged_sentences):
	chunked_sentence = regexp.CustomChunker().parse(sentence)
	retaged_sentence = utils.retag_chunked(chunked_sentence)
	what = []
	who = []
	for (word, tag, piece) in retaged_sentence:
		w = word.lower()
		if tag.startswith("PRP"): # this is a reference
			if (w in ("he", "she", "they", "them", "his", "her", "their", "our", "i", "we")):
				who.append(word)
		elif w in names: # this word belongs to a person name
			who.append(word)
		elif piece in ('TARINYS'):
			what.append(word)
		
		#TODO: concatenate multi tarinys to one
		#TODO: full name recognition
		#TODO: replace PRP with fullnames, check if same  & only person is not used >1 in same sentence, if so - don't print
		#TODO: add some details to extracted actions
		
	if len(who) > 1  and len(what) > 0: # only show people & interactions that include an action 
		print ", ".join(who), "-", ", ".join(what)
	
		
		
		