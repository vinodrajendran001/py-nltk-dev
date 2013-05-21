import nltk, data, summarize, pickle, ner, config, training, sys, utils, action, references
from nltk.tree import Tree

def print_to_screen_and_file(text):
	print text
	if type(text) == list:
		for index, item in enumerate(text):
			print index, item
	else:
		fp.write(text)
		fp.write("\n")

def run(path):
	global fp 
	MAX_SENTENCES = config.MAX_SENTENCES	

	if len(path) == 0:
		path = "db/ivonyte-aiste/2011-7-8-1.txt" 
	# load article text

	article = data.Article(path)
	utils.load_data(article.text)
	
	fp = file("results.txt", "wb")

	# show article text
	print_to_screen_and_file("-"*80)
	print_to_screen_and_file("Original article:")
	print_to_screen_and_file(article.text)
	print_to_screen_and_file("-"*80)

	# make the summary & show in console
	print_to_screen_and_file("I Summary:")
	instance = summarize.SimpleSummarizer()
	print_to_screen_and_file(instance.summarize(article.text, MAX_SENTENCES))
	print_to_screen_and_file("-"*80)

	print_to_screen_and_file("II Summary:")
	print_to_screen_and_file("Will be done soon :) ")
	print_to_screen_and_file("-"*80)

	print_to_screen_and_file("People and their actions:")
	work = action.Actions().find(utils.tagged_words, utils.tagged_sentences, utils.people)
	# print the updated info with people actions
	for i, (key, value) in enumerate(work.items()):
		print_to_screen_and_file("[%d] - %s = %s"%(i+1, key, value))
	print_to_screen_and_file("-"*80)

	print_to_screen_and_file("Anaphoras:")
	refs = references.References().find(utils.people, utils.sentences, utils.tagged_sentences)
	print_to_screen_and_file(refs)
	print_to_screen_and_file("-"*80)

	print_to_screen_and_file("People interactions:")
	print_to_screen_and_file("-"*80)

	fp.close()

# script start spot
if __name__ == "__main__":
	#path = sys.argv[1]
	#print path

	path = "db/ivonyte-aiste/2011-7-8-1.txt" 
	run(path)

	#else:
	