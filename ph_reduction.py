import regexp
from nltk.tree import Tree

# Uses phrase reduction to make a summary from the tagged text (sentences).
# Scan begins by finding VEIKSNYS in every sentences, all words until it are included in summary.
# After finding it, a new search for TARINYS is issued. All words in between ar added to summary also.
# To give some detail to summary an additional APLINKYBE, etc. is appended after TARINYS.

class PhraseReductor:
	def pack_in_bag(self, t, flags, bag, depth):
		if type(t) == Tree:
			if 'xx' in flags:
				#print "bail out"
				return

			if ('x' in flags) and not (t.node in ("OBJEKTAS", "VEIKSNYS", "TARINYS", "PAPILDINYS")):
				flags['xx'] = 1
				#print "totaly end", t
				return
			elif ('v' not in flags) and (t.node in ("OBJEKTAS", "VEIKSNYS", "IVARDIS", "APLINKYBES")):
				flags['v'] = 1
				#print "veiksnys",t
			elif ('v' in flags) and ('t' not in flags) and (t.node in ("TARINYS")):
				flags['t'] = 1
				#print "tarinys",t
			elif ('t' in flags) and ('x' not in flags) and (t.node in ("APLINKYBES", "OBJEKTAS", "TARINYS", "VEIKSNYS")):
				flags['x'] = 1;
				if t.node in ("VEIKSNYS"):
					#print "totaly end - veiksnys", t
					flags['xx'] = 1
				else:
					#print "maybe end", t
					pass
			else:
				#print "unknown",t, flags
				pass
			
			for leaf in t:
				if (depth == 0) and ('xx' in flags):
					return
				else:
					self.pack_in_bag(leaf, flags, bag, depth+1)
		else:
			bag.append(t)

	def create_summary(self, t, flags, summary):
		if type(t) == Tree:
			self.pack_in_bag(t, flags, summary, 0)
		else:
			summary.append(t)
			
	def find(self, tagged_sentences):
		# do our custom chunking, because regular one is too mainstream :D
		chk = regexp.CustomChunker()
		sentences = []
		
		for index, sentence in enumerate(tagged_sentences):
			chunked_sentence = chk.parse(sentence)
			summary, flags = [], {}
			self.create_summary(chunked_sentence, flags, summary)

			# remove dots & commas(if any) at the end of sentence
			summary.reverse()
			count = 0
			for elem in summary:
				if elem[0] not in (".", ",", "\""): break
				count += 1
			del summary[0:count] # strip
			summary.reverse()
			#print summary
			
			bag = []
			for elem in summary:
				bag.append(elem[0])
			sentences.append(" ".join(bag)+".")
		
		return sentences
