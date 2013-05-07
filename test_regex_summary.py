import nltk, data, summarize, pickle, ner, config, training, sys
from nltk.tree import Tree

# show commandline arguments
print "CLI:",sys.argv

# helper function to aggregate all tags into one place
def join_tagged(tagged):
	s = ""
	for text, tag in tagged:
		s += " "+text+"/"+tag
	return s

path = "db/ivonyte-aiste/2011-7-8-1.txt"
article = data.Article(path)
print "-"*80
print article.text
print "-"*80

# tokenize & tag all words in article
print "Tokenizing & tagging words..."
tokens = nltk.tokenize.wordpunct_tokenize(article.text)
tagged_words = nltk.pos_tag(tokens)

# extract & tokenize each sentence separately
print "Tokenizing & tagging sentences..."
sentences = nltk.tokenize.sent_tokenize(article.text)
tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences] 
tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]

# show the output
print join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80

# WDT - with, CD - number, CC - and, PRP - she;I, POS - `, MD - will, PRP$ - his, JJ - crucial;political, RB - even, not
# IN - at/in, DT - a, the, those, NN - noun(sun, dog, ...)
# TODO: revise grammar & regexp
grammar = r"""
  APLINKYBES: {<IN><DT|CD|NN.*|POS|:>+}
  VIETA: {<NNP><NN..>+}
  VEIKSNYS: {<DT><JJ>*<NN.*>+}        # Chunk sequences of DT, JJ, NN
  TARINYS: {<MD>*<V.|V..>*<NP|PP>*<TO>?} # Chunk verbs and their arguments
  PAPILDINYS: {<IN>*<DT>*<JJ><NN?>*}
  SAKINYS: {<APLINKYBES><VEIKSNYS><TARINYS><APLINKYBES>*}
  BRAND: {<NN.>*<:|CD>*<NN.>*}
  """
cp = nltk.RegexpParser(grammar) 

'''
def find(node, s, flags):
	if flags['stop']: return
	if node.node == "NP": # and not flags['v']:
		#flags['n'] = True
		s.append([e[0] for e in node if e[1].startswith("N")]) # drop the tag, get only names
	else:
		for child in node:
			if flags['stop']: return
			if type(child) == Tree:
				find(child, s, flags)
			else:
				value, tag = child
				if tag in (".", ",", "IN", "CD", "PRP", "PRP$", "CC", "POS") or tag[0] in ("V", "W"):
					# CD - numbers, CC - and, ` - POS, V - verb, W - and
					if tag == "VBG" and flags['v']: # gerund
						flags['stop'] = True
						
					if tag.startswith("V"):
						flags['n'] = False
						flags['v'] = True
						
					s.append(value)
					if flags['stop']:
						s.append('.')
						return
'''

# do our custom chunking
b = 0
for index, sentence in enumerate(tagged_sentences):
	chunked_sentence = cp.parse(sentence) # nltk.chunk.ne_chunk(sentence)
	if b < 3:
		print "oooo", sentences[index]
		print
		print "####", chunked_sentence
		b += 1

'''b = 3
for sentence in tagged_sentences:
	state = "who"
	found = False
	complete = []
	for word, tag in sentence:
		if state == "who":
			if tag.startswith("N") or tag in (",", ".", ":", "IN", "PRP", "POS", "CD", "MD", "PRP$"):
				complete.append(word)
			elif tag.startswith("V"):
				state = "did"
				complete.append(word)
		elif state == "did":
			if tag.startswith("V") or tag in (".", ",", ":", "IN", "CC", "CD", "PRP", "WDT", "POS"):
				complete.append(word);
				if tag == "VBG": 
					complete.append(".");
					break
			elif tag.startswith("N") or tag in (".", ","):
				#if not found:
				#	found = True
				#	complete.append(word)
				#elif found:
				complete.append(word)
				
	if b == 0: break
	b -= 1
	print "oooo", sentence
	print
	print " ".join(complete)
	print "%"*100'''

#TODO: use or remove!
# Stemming
#stemmer = nltk.stem.WordNetLemmatizer()
#print stemmer.lemmatize("cats")