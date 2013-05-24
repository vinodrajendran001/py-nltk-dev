import nltk, data, pickle
import ner, config, training, sys, utils, action, references, ph_reduction

from summarize import SimpleSummarizer

def print_to_screen_and_file(text):
	print text
	if type(text) == list:
		for index, item in enumerate(text):
			print index, item
	else:
		fp.write(text+"\n")
		fp.flush()

def get_categories(article):
	categories = []
	#lets get all the categories from the article

def run(path):
	global fp 

	#if len(path) == 0:
	#	path = "db/ivonyte-aiste/2011-7-8-1.txt" 
	
	# load article text
	article = data.Article(path)
	utils.load_data(article.text)

	fp = file("results.txt", "w")

	# show article text
	print_to_screen_and_file("-"*80)
	print_to_screen_and_file("Original article:")
	print_to_screen_and_file("")
	print_to_screen_and_file(article.text)
	print_to_screen_and_file("-"*80)

	# make the summary & show in console
	print_to_screen_and_file("I Summary:")
	print_to_screen_and_file("")
	instance = SimpleSummarizer()
	print_to_screen_and_file(instance.summarize(article.text, len(utils.sentences) / 3))
	print_to_screen_and_file("-"*80)

	#TODO: summary from phrase reduction
	print_to_screen_and_file("II Summary:")
	print_to_screen_and_file("")
	#print_to_screen_and_file(test_regex_summary.get_summary(path))
	print "".join(ph_reduction.PhraseReductor().find(utils.tagged_sentences))
	print_to_screen_and_file("-"*80)
	
	# classification
	stemmer = nltk.stem.WordNetLemmatizer()
	words = nltk.tokenize.wordpunct_tokenize(article.text)
	feats = utils.bag_of_words(words, article.text, stemmer)
	
	classifier = pickle.load(file(config.BAYES_CLASSIFIER_FILE))
	print_to_screen_and_file("BayesClassifier class: " + classifier.classify(feats))
	
	classifier = pickle.load(file(config.MAXENT_CLASSIFIER_FILE))
	print_to_screen_and_file("MaxEntClassifier class: " + classifier.classify(feats))
	
	classifier = pickle.load(file(config.DTREE_CLASSIFIER_FILE))
	print_to_screen_and_file("DecisionTreeClassifier class: " + classifier.classify(feats))
	print_to_screen_and_file("-"*80)
	
	print_to_screen_and_file("Actual categories of the article:")
	print "To come..."

	# people actions
	print_to_screen_and_file("People and their actions:")
	work = action.Actions().find(utils.tagged_words, utils.tagged_sentences, utils.people)
	# print the updated info with people actions
	for i, (key, value) in enumerate(work.items()):
		print_to_screen_and_file("[%d] - %s = %s"%(i+1, key, value))
	print_to_screen_and_file("-"*80)

	# anaphora
	print_to_screen_and_file("Anaphoras:")
	refs = references.References().find(utils.people, utils.sentences, utils.tagged_sentences)
	for ref, fullname, index in refs:
		fp.write("Sentence["+str(index+1)+"]: " + ref + " - "+fullname+"\n")
	print_to_screen_and_file("-"*80)

	# interactions
	print_to_screen_and_file("People interactions:")
	print_to_screen_and_file("-"*80)

	fp.close()

# script start spot
if __name__ == "__main__":
	#path = sys.argv[1]
	#print path

	path = "db/kubilius-algirdas/2010-02-05-8.txt" 
	run(path)