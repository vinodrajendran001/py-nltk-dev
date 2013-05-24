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

ref_dict = {} # reference map by sentence index
for prp, fullname, index in refs:
	if index not in ref_dict:
		ref_dict[index] = [prp, fullname, index]
	else:
		ref_dict[index].append([prp, fullname, index])

article.show()

names = utils.get_names_dict(utils.people)

# TODO: 
# 		find PRP/name, VRB, PRP/name for - 1
# 		memory for people: name/name/name/... (they did) - 2

interact = []
for index, sentence in enumerate(utils.tagged_sentences):
	chunked_sentence = regexp.CustomChunker().parse(sentence)
	
	retaged_sentence = utils.retag_chunked(chunked_sentence)
	new_tagged_sentence = utils.mark_sentence_names(retaged_sentence, names)
	
	#TODO: add some details to extracted actions
	# find prepositions, replace with real names and print what they did
	who, what, prp, seq = [], [], [], []
	prp_counter = 0
	for (word, tag, piece, pt) in new_tagged_sentence:
		reset = True
		w = word.lower()
		if tag.startswith("PRP"): # this is a reference
			if (w in ("he", "she", "his", "him", "her", "i", "me", "our")):
				if index in ref_dict[index]:
					who.append(ref_dict[index][1]) # PRP-person mapping exists
					prp.append(word)
				else:
					who.append(None) # PRP exists without mapped person
					prp.append(word)
		elif w in names: 
			# this word belongs to a person name, there's no PRP for it
			who.append(word)
			prp.append(None)
		elif piece in ('TARINYS'): 
			reset = False
			seq.append(word) 
			
		if reset and len(seq) > 0: # join neighbouring verbs if possible
			what.append(" ".join(seq))
			seq = []
	
	if len(who) > 1 and len(what) > 0: # only show people & their interactions that include an action
		# capitalize each person name/surname first letter
		for i, boo in enumerate(who):
			who[i] = " ".join([part[0].upper()+part[1:] for part in boo.split(" ")])
		interact.append({'who':who, 'prp': prp, 'what':what})

print "Interactions:"
for index, item in enumerate(interact):
	who, prp, what = item['who'], item['prp'], item['what']
	s = "["+str(index+1)+"]:"
	for i in xrange(len(who)):
		if prp[i] and who[i]: s += " " + who[i] + "(" + prp[i] + "), "
		elif prp[i]: s += prp[i] + ", "
		elif who[i]: s += " " + who[i] + ", "
	s += " - " + ", ".join(what)
	print s