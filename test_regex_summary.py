import nltk, data, summarize, pickle, ner, config, training, sys, utils, regexp
from nltk.tree import Tree

# show commandline arguments
print "CLI:", sys.argv

path = "db/barkauskas-povilas/2011-04-11-5.txt"
article = data.Article(path)
print "-"*80
print article.text
print "-"*80

def create_summary(tree, summary):
  if tree.node == "VEIKSNYS" or tree.node == "TARINYS" or tree.node == "OBJEKTAS" \
  or tree.node == "IVARDIS" or tree.node == "APLINKYBES":
    summary.append([e[0] for e in tree])
  else:
    for ent in tree:
      if type(ent) == Tree:
        create_summary(ent, summary)

def check_gender(tag, gender):
  if (tag.lower() == 'she' and gender == 'female') or (tag.lower() == 'he' and gender == 'male'):
    return True
  else:
    return False

def anaphora_finder(tagged_sentences, people):
  
  names = {}

  for i, (fullname, data) in enumerate(people.items()):
    for short in data['shortnames']:
      names[short] = data['sex']
    names[fullname] = data['sex']
  print names

  for i in range(len(tagged_sentences)):
    sentence = tagged_sentences[i]
    for word, tag in sentence:
      for single_name in names.items():
        if word in single_name.split(" "):
          person =  word
        else:
          if tag == 'PRP' or tag == 'PRP$':
            print "Here is the tag you were looking for", word
      #if (tag == 'PRP' or tag == 'PRP$'):
      #  if len(word) < 5 and len(person) > 0: #and check_gender(tag, gender):
      #    print "Found it!!!", word, person
          


# we give parameter to load everything from file and to save some time :) 
if "-f" in sys.argv:
  # tokenize & tag all words in article
  print "Tokenizing & tagging words..."
  tokens = nltk.tokenize.wordpunct_tokenize(article.text)
  tagged_words = nltk.pos_tag(tokens)
  pickle.dump(tagged_words, file('tagged_words.txt', 'w'))

  # extract & tokenize each sentence separately
  print "Tokenizing & tagging sentences..."
  sentences = nltk.tokenize.sent_tokenize(article.text)
  pickle.dump(sentences, file('sentences.txt', 'w'))
  tokenized_sentences = [nltk.tokenize.wordpunct_tokenize(s) for s in sentences]
  tagged_sentences = [nltk.pos_tag(s) for s in tokenized_sentences]
  pickle.dump(tagged_sentences, file('tagged_sentences.txt', 'w'))
  instance  = ner.NERFinder()
  people = instance.find(tagged_words, sentences, tagged_sentences)
  pickle.dump(people, file('people.txt', 'w'))
else:
  tagged_sentences =  pickle.load(file('tagged_sentences.txt', 'r'))
  tagged_words =  pickle.load(file('tagged_words.txt', 'r'))
  sentences =  pickle.load(file('sentences.txt', 'r'))
  people =  pickle.load(file('people.txt', 'r'))

# show the output
print utils.join_tagged(tagged_words)
print "-"*80
print tagged_sentences
print "-"*80


# WDT - with, CD - number, CC - and, PRP - she;I, POS - `, MD - will, PRP$ - his, JJ - crucial;political, RB - even, not
# IN - at/in, DT - a, the, those, NN - noun(sun, dog, ...)
# TODO: revise grammar & regexp
grammar = r"""
  APLINKYBES: {<IN><DT|CD|NN.*|POS|:>+<IN>*}
  VIETA: {<NNP><NN..>+}
  VEIKSNYS: {<DT><JJ>*<NN.*>*<:>*<NN.>*} # Chunk sequences of DT, JJ, NN
  TARINYS: {<EX>*<MD>*<RB>?<V.|V..>+<IN>*<NP|PP>*<TO>?<RB>?<JJ|NN>?<V.|V..>*} # Chunk verbs and their arguments
  OBJEKTAS: {<NN.>*<:|C.>*<NN.>*}
  PAPILDINYS: {<RB>*<IN>*<DT>*<JJ>*<NN?>*}
  JUNGTUKAS: {<CC>}
  IVARDIS: {<PRP.*><PRP.*>*}
  """

''' old backup grammar:
grammar = r"""
  APLINKYBES: {<IN><DT|CD|NN.*|POS|:>+}
  VIETA: {<NNP><NN..>+}
  VEIKSNYS: {<DT><JJ>*<NN.*>+}        # Chunk sequences of DT, JJ, NN
  TARINYS: {<MD>*<V.|V..>*<IN*><NP|PP>*<TO>?} # Chunk verbs and their arguments
  PAPILDINYS: {<IN>*<DT>*<JJ><NN?>*}
  SAKINYS: {<APLINKYBES><VEIKSNYS><TARINYS><APLINKYBES>*}
  BRAND: {<NN.>*<:|CD>*<NN.>*}
  """
'''

# do our custom chunking, because regular one is too mainstream :D
cp = nltk.RegexpParser(grammar) 

#anaphora_finder(tagged_sentences, people)
summary = []

start = 5
end = 35
for index, sentence in enumerate(tagged_sentences):
  chunked_sentence = cp.parse(sentence) 
  if index < end and index >= start:
	 print "[",index,"] oooo", sentences[index]
	 print
	 print "[",index,"] ####", chunked_sentence
  create_summary(chunked_sentence, summary)
  summary.append(".")

#TODO: make it nice looking text
print "Summary:"
for item in summary:
  bag = ""
  for element in item:
    bag += "".join(element)
  #print bag #type(item), item #bag #" ".join(bag)