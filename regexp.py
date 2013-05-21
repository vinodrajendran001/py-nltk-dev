import nltk

class CustomChunker:
	def __init__(self):
		# tag examples:
		# WDT - with, CD - number, CC - and, PRP - she/he/I, POS - `, MD - will, PRP$ - his/her, JJ - crucial;political, RB - even, not
		# IN - at/in/of, DT - a/the/those, NN - noun(sun, dog, ..., etc.), RP - over
		
		# Grammar rules (more info @ http://en.wikipedia.org/wiki/Regular_expression):
		# TITLE: <tag_name>, * - 0 or more repetitions, ? - 0 or 1 repetition, . - missing char, | - or, + - 1 or more repetitions
		
		grammar = r"""
		  IVARDIS: {<PRP.*><PRP.*>*}
		  APLINKYBES: {<IN><DT|CD|NN.*|POS|:>*<JJ|NN>*}
		  VIETA: {<NNP><NN..>+}
		  TARINYS: {<EX>*<MD>*<RB>?<V.|V..>+<RP>*<IN>*<NP|PP>*<TO>?<RB>?<JJ|NN.*>?<V.|V..>*}
		  VEIKSNYS: {<DT>?<PRP.*>*<JJ>*<NN.*>+<:>*<POS>*<NN.*>*}
		  OBJEKTAS: {<NN.>*<:|CD>*<NN.*>*}
		  PAPILDINYS: {<RB>*<IN>*<DT>*<JJ>*<NN.*>*}
		  JUNGTUKAS: {<CC>}
		  S_SAK: {<WRB|WDT>}
		  """
		self.parser = nltk.RegexpParser(grammar)
		
	def parse(self, tagged_words):
		return self.parser.parse(tagged_words)