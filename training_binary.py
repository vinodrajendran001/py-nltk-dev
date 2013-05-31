import nltk, pickle, config, data, random, sys, utils

def load_samples(sample_list, tag, stemmer, max_words):
	data_set = []
	for (filename, category) in sample_list:
		# extract article words
		words = nltk.tokenize.wordpunct_tokenize(data.Article(filename).text)
		all_words = nltk.FreqDist(words)
		
		tokens = all_words.keys()
		if len(tokens) > max_words: # limit to max most frequent words per article
			tokens = tokens[:max_words]
		
		data_set.append((utils.bag_of_words(tokens, words, stemmer, True), tag))
	random.shuffle(data_set)
	return data_set
	
# ok, do some work here - train the classifier using training set & test it against test set
def run(classifier, max_words):
	print "Classifier:", classifier,"max words:", max_words

	print "Importing pickled data lists"
	data = {}
	total = 0
	for key, fname in config.DUMP_FILES.items():
		if key == "MULTI": continue # skip this type as multiclass articles are already included
		data[key] = pickle.load(file(fname, "r"))
		total += len(data[key])
		
	print "Shuffling data for better randomness..."
	for key in data.keys():
		random.shuffle(data[key])
	
	stemmer = nltk.stem.WordNetLemmatizer()
	print "Generating",len(data.keys()),"classifiers..."
	
	# for each class generate a classifier
	classif = {}
	for key in data.keys():
		# need positive(the current class) & negative examples(all other classes)
		positive = data[key]
		
		# limit training size
		pos_total = len(positive)
		max_pos = pos_total * config.TRAINING_SET_SIZE / 100
		
		negative = []
		neg_total = total - pos_total
		max_neg = neg_total * config.TRAINING_SET_SIZE / 100
		
		print ">>> Classifier",key,"training size - pos:",max_pos,"of",pos_total,"/ neg:",max_neg,"of",neg_total
		
		# build negative examples
		for k in data.keys():
			if k == key: continue
			negative.extend(data[k])
		
		# split the sets
		positive_train = positive[:max_pos]
		positive_test = positive[max_pos:]
		negative_train = negative[:max_neg]
		negative_test = negative[max_neg:]
		
		print "Loading training & testing data"
		# TODO: optimize speed/loading - preload all articles into map & just select from it on every request
		pos_training_set = load_samples(positive_train, "yes", stemmer, max_words)
		pos_testing_set = load_samples(positive_test, "yes", stemmer, max_words)
		neg_training_set = load_samples(negative_train, "no", stemmer, max_words)
		neg_testing_set = load_samples(negative_test, "no", stemmer, max_words)
		print "Positive - train on %d samples, test on %d samples" % (len(pos_training_set), len(pos_testing_set))
		print "Negative - train on %d samples, test on %d samples" % (len(neg_training_set), len(neg_testing_set))
		
		# merge
		training_set = []
		training_set.extend(pos_training_set)
		training_set.extend(neg_training_set)
		
		testing_set = []
		testing_set.extend(pos_testing_set)
		testing_set.extend(neg_testing_set)
		
		print "Starting training..."
		
		# do the actual classifier training
		instance = None
		if classifier == nltk.classify.NaiveBayesClassifier:
			instance = nltk.classify.NaiveBayesClassifier.train(training_set)
			picklename = config.BAYES_CLASSIFIER_FILE_PATTERN % (key)
		elif classifier == nltk.classify.MaxentClassifier:
			instance = nltk.classify.MaxentClassifier.train(training_set, max_iter=config.MAX_TRAINING_ITERS)
			picklename = config.MAXENT_CLASSIFIER_FILE_PATTERN % (key)
		elif classifier == nltk.classify.DecisionTreeClassifier:
			instance = nltk.classify.DecisionTreeClassifier.train(training_set, binary=False)
			picklename = config.DTREE_CLASSIFIER_FILE_PATTERN % (key)
		
		print "Training complete."
		
		# serialize the classifer to file (for later use)
		with file(picklename, 'wb') as fp:
			pickle.dump(instance, fp)
		print "Classifier saved to file:", picklename

		# test classifier accuracy with the test set
		print "Evaluating classifier accuracy..."
		accuracy = nltk.classify.util.accuracy(instance, testing_set)
		print "Classifier accuracy:", accuracy

if __name__ == "__main__":
	#print "CLI arguments:", sys.argv
	if "-m" in sys.argv: 
		print "Using MaxentClassifier classifer"
		run(nltk.classify.MaxentClassifier, 100)
	elif "-d" in sys.argv:
		print "Using DecisionTreeClassifier"
		run(nltk.classify.DecisionTreeClassifier, 10)
	else:
		print "Using default NaiveBayesClassifier classifer"
		run(nltk.classify.NaiveBayesClassifier, 1000)