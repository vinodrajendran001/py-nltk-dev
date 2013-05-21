# --------------------------------------------------------------------------------------------
# Code below resolves references based on simple mentioned male/female entity memory scheme:
# 	1. parse every sentence for person & PRP 
#   2. determine person's sex & store him/her as last one mentioned (separate for male/female)
#   3. if PRP is found, then based on sex & last memorized person the PRP is assigned to the person name
# --------------------------------------------------------------------------------------------

class References:
	def get_gender(self, word):
		if word.lower() in ("she", "her"): return "female"	
		if word.lower() in ("he", "him", "his"): return "male"
		return "?"
	
	def find(self, people, sentences, tagged_sentences):
		# create a all possible lowercase names & drink beer later :P
		names = {}
		for i, (fullname, data) in enumerate(people.items()):
			for shortname in data['shortnames']:
				for s in shortname.lower().split(" "):
					names[s] = data
				names[shortname.lower()] = data
			for shortname in fullname.lower().split(" "):
				names[shortname] = data
			names[fullname.lower()] = data

		# find names in text and mark them with special symbols & append additional data
		new_tagged_sentences = []
		for index, sentence in enumerate(tagged_sentences):
			sent = [] 
			for word, tag in sentence:
				key = word.lower() 
				if key in names:
					sent.append((word.lower(), tag, '+', names[key])) # add `+` to a name & include data
				else:
					sent.append((word.lower(), tag, 'o', None)) # not a name - mark as `o`
			new_tagged_sentences.append(sent)

		# show debug texts
		#print new_tagged_sentences
		#print "-"*80
		#print article.text
		#print "-"*80
		
		# store references as: PRP, fullname, sentence_index
		refs = []

		# store last he & she while scanning sentences, 
		# if unknown sex name is found - store it also (determine type on first PRP found)
		last_he = [None, 0] # store as: [people_data, word_index_in_text]
		last_she = [None, 0]
		last_unknown = [None, 0]
		word_index = 0
		for index, sentence in enumerate(new_tagged_sentences):	
			for element in sentence:
				word, tag, flag, data = element # unpack all data
				word_index += 1 # increase processed words index
				
				if tag.startswith("PRP") and len(word) <= 5 and (word not in ("it", "our", "their", "us", "its", "we", "they")): # a determined reference was found!
					### unknown sex resolver
					if last_unknown[0]: # if we have an unknown name without sex, then assign the next first found sex to it
						gender = self.get_gender(word)
						print "Last unknown person -", last_unknown[0]['fullname'], "- was assigned sex:", gender
						last_unknown[0]['sex'] = gender
						
						# the hack has been fixed :P
						if gender == "male":
							if last_he[0]: # last `he` exists
								if last_he[1] < last_unknown[1]: # override if unknown is newer 
									last_he = last_unknown
							else:
								last_he = last_unknown # override as no `he` exists
						elif gender == "female":
							if last_she[0]:
								if last_she[1] < last_unknown[1]:
									last_she = last_unknown
							else:
								last_she = last_unknown

						if gender in ("male", "female"): # clear only if actualy determined
							last_unknown = [None, 0] # clear
					
					#### determine the person mentioned
					print "*"*80
					matched = None
					if word in ("he", "his", "him") and last_he[0]: # male
						matched = last_he
					elif word in ("she", "her") and last_she[0]: # female
						matched = last_she
					elif word in ("i", "me", "our"): # cannot determine sex - as multi
						if last_he[0] and last_she[0]: # we have both sex types in memory, choose the last one mentioned
							if last_he[1] > last_she[1]: # he is more fresh
								matched = last_he
							else: # she is more fresh
								matched = last_she
						elif last_he[0]: # we have only `he` in memory
							matched = last_he
						elif last_she[0]: # we have only `she` in memory
							matched = last_she
					
					if matched: # refresh index - this person has been just mentioned
						matched[1] = word_index
						print "REF[", word, "] is -", matched[0]['fullname'], "- in sentence Nr.", index
						refs.append([word, matched[0]['fullname'], index])
					else:
						print "REF[", word, "] is", "UNKNOWN", "in sentence Nr.", index
						refs.append([word, "?", index])
					print "\t", sentences[index] # show the corresponding sentence with the match
					
				elif flag == "+": # a word is a name, so put it into memory
					if data["sex"] == "male":
						last_he = [data, word_index]
					elif data["sex"] == "female":
						last_she = [data, word_index]
					elif data['sex'] == "?":
						last_unknown = [data, word_index]
						
		return refs