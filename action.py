
class Actions:
	# fills people data with actions that they did according to article text
	def find(self, tagged_words, tagged_sentences, people):
		print "-"*80
		for i, (fullname, data) in enumerate(people.items()):
			names = set()
			for short in data['shortnames']:
				names.update(short.lower().split(" "))
				names.add(short.lower())
			names.update(fullname.lower().split(" "))
			names.add(fullname.lower())
			
			data['actions'] = [] # empty action list
			for index, sentence in enumerate(tagged_sentences):
				found = False
				verb = False
				act = []
				for word, tag in sentence:
					if word.lower() in names: 
						found = True
						#print "found", word, "in sentence", index
						continue
					elif found:
						# reached end of name, so scan now for verbs
						if tag.startswith('V'):
							#print "adding action:", word
							verb = True
							act.append(word.lower())
						elif verb: # all verbs collected & this word found is a non verb
							# ok, we're done here, so bail out of sentence
							#print "all verbs collected, so bail out!"
							break
				if len(act) > 0: # dont include empty actions
					data['actions'].append(" ".join(act));
		return people