import data, sys, utils, action, regexp
from nltk.tree import Tree

# load all required data
print "CLI:",sys.argv
path = "db/barkauskas-povilas/2011-04-11-5.txt"
article = data.Article(path)
article.show()
utils.load_data(article.text)

# show the output
print utils.join_tagged(utils.tagged_words)
print "-"*80
print utils.tagged_sentences
print "-"*80

def create_summary(tree, summary):
  if tree.node == "VEIKSNYS" or tree.node == "TARINYS" or tree.node == "OBJEKTAS" \
  or tree.node == "IVARDIS" or tree.node == "APLINKYBES":
    summary.append([e[0] for e in tree])
  else:
    for ent in tree:
      if type(ent) == Tree:
        create_summary(ent, summary)

# do our custom chunking, because regular one is too mainstream :D
chk = regexp.CustomChunker()

start = 5
end = 35
for index, sentence in enumerate(utils.tagged_sentences):
	chunked_sentence = chk.parse(sentence)
	if index < end and index >= start:
		print "[",index,"] oooo", utils.sentences[index]
		print
		print "[",index,"] ####", chunked_sentence
	summary = []
	create_summary(chunked_sentence, summary)
	summary.append(".")
	
	bag = []
	for elem in summary:
		bag.append(" ".join(elem))
	print " ".join(bag)
