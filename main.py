import nltk, data, pickle
import ner, config, training, sys, utils, action, references, ph_reduction, interactions

from summarize import SimpleSummarizer

fp = None

def print_to_screen_and_file(text):
	print text
	fp.write(str(text)+"\n")
	fp.flush()

def run(path):
	global fp

	# load article text
	article = data.Article(path)
	utils.load_data(article.text)

	fp = file("results.txt", "w")

	# show article text
	print_to_screen_and_file("-"*80)
	print_to_screen_and_file("Original article:\n")
	print_to_screen_and_file(article.text)
	print_to_screen_and_file("-"*80)
	print_to_screen_and_file("Categories:\n")
	print_to_screen_and_file(article.cats)
	print_to_screen_and_file("-"*80)

	# make the summary & show in console
	print_to_screen_and_file("I Summary:\n")
	
	instance = SimpleSummarizer()
	# shorten the original article by one third
	print_to_screen_and_file(instance.summarize(article.text, len(utils.sentences) / 3))
	print_to_screen_and_file("-"*80)

	print_to_screen_and_file("II Summary:\n")
	print_to_screen_and_file(" ".join(ph_reduction.PhraseReductor().find(utils.tagged_sentences)))
	print_to_screen_and_file("-"*80)
	
	# classification
	print_to_screen_and_file("Multiclass classification:\n")
	stemmer = nltk.stem.WordNetLemmatizer()
	words = nltk.tokenize.wordpunct_tokenize(article.text)
	feats = utils.bag_of_words(words, article.text, stemmer)
	
	classifier = pickle.load(file(config.BAYES_CLASSIFIER_FILE, 'r'))
	print_to_screen_and_file("BayesClassifier class: " + classifier.classify(feats))
	
	classifier = pickle.load(file(config.MAXENT_CLASSIFIER_FILE, 'r'))
	print_to_screen_and_file("MaxEntClassifier class: " + classifier.classify(feats))
	
	classifier = pickle.load(file(config.DTREE_CLASSIFIER_FILE, 'r'))
	print_to_screen_and_file("DecisionTreeClassifier class: " + classifier.classify(feats))
	print_to_screen_and_file("-"*80)
	
	print_to_screen_and_file("Binary classification:\n")
	title = ["BayesClassifier: ", "MaxEntClassifier: ", "DecisionTreeClassifier: "]
	classifiers = [config.BAYES_CLASSIFIER_FILE_PATTERN, config.MAXENT_CLASSIFIER_FILE_PATTERN, config.DTREE_CLASSIFIER_FILE_PATTERN]
	tags = ["A", "B", "C", "D", "E", "OTHER"]
	for index, typename in enumerate(classifiers):
		results = {}
		for tag in tags:
			fname = typename%(tag)
			classifier = pickle.load(file(fname, 'r'))
			results[tag] = classifier.classify(feats)
		print_to_screen_and_file(title[index] + str(results))
	print_to_screen_and_file("-"*80)

	# people actions
	print_to_screen_and_file("People and their actions:\n")
	work = action.Actions().find(utils.tagged_words, utils.tagged_sentences, utils.people)
	# print the updated info with people actions
	for i, (key, value) in enumerate(work.items()):
		print_to_screen_and_file("[%d] - %s = %s"%(i+1, key, value))
	print_to_screen_and_file("-"*80)

	# anaphora
	print_to_screen_and_file("Anaphoras:\n")
	refs = references.References().find(utils.people, utils.sentences, utils.tagged_sentences)
	for ref, fullname, index in refs:
		print_to_screen_and_file("Sentence["+str(index+1)+"]: " + ref + " - "+ fullname)
	print_to_screen_and_file("-"*80)

	# interactions
	print_to_screen_and_file("People interactions:\n")
	inter = interactions.Interactor().find(refs, utils.tagged_sentences)
	for index, item in enumerate(inter):
		who, prp, what = item['who'], item['prp'], item['what']
		s = "["+str(index+1)+"]:"
		for i in xrange(len(who)):
			if prp[i] and who[i]: s += " " + who[i] + "(" + prp[i] + "), "
			elif prp[i]: s += prp[i] + ", "
			elif who[i]: s += " " + who[i] + ", "
		s += " - " + ", ".join(what)
		print_to_screen_and_file(s)

	print_to_screen_and_file("-"*80)
	print "Finished."

	fp.close()

# script start spot
if __name__ == "__main__":
	if len(sys.argv) > 2 and sys.argv[1] == "-f":
		run(sys.argv[2])
	else:
		print "No args specified, usage:\n\tpython main.py -f db/klementavicius-rimvydas/2011-12-03-1.txt"