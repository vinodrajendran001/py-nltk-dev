import utils, regexp

'''
	Asmenu saveikos (ATVEJAI):
		1) Ivardis, Tarinys, Ivardis
		2) Ivardis (THEY), Tarinys (anksciau pamineti vardaI)
		3) Objektas, Tarinys, Aplinkybe (su vardu)
'''

class Interactor:
	def find(self, refs, tagged_sentences):
		ref_dict = {} # reference map by sentence index
		for prp, fullname, index in refs:
			if index not in ref_dict:
				ref_dict[index] = [prp, fullname, index]
			else:
				ref_dict[index].append([prp, fullname, index])

		names = utils.get_names_dict(utils.people)

		# TODO: 
		# 		find PRP/name, VRB, PRP/name for - 1
		# 		memory for people: name/name/name/... (they did) - 2

		interact = []
		for index, sentence in enumerate(tagged_sentences):
			chunked_sentence = regexp.CustomChunker().parse(sentence)
			retaged_sentence = utils.retag_chunked(chunked_sentence)
			new_tagged_sentence = utils.mark_sentence_names(retaged_sentence, names)
			
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
				elif piece in ('TARINYS'): #TODO: add some details to extracted actions
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
				
		return interact 