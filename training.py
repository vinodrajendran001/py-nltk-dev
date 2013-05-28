import nltk, pickle, config, data, random, sys, utils

def load_samples(sample_list, stemmer, max_words):
	data_set = []
	for (filename, category) in sample_list:
		# extract article words
		words = nltk.tokenize.wordpunct_tokenize(data.Article(filename).text)
		all_words = nltk.FreqDist(words)
		
		tokens = all_words.keys()
		if len(tokens) > max_words: # limit to max most frequent words per article
			tokens = tokens[:max_words]
		
		data_set.append((utils.bag_of_words(tokens, words, stemmer), category))
	random.shuffle(data_set)
	return data_set
	
# ok, do some work here - train the classifier using training set & test it against test set
def run(classifier, max_words):
	print "Classifier:", classifier,"max words:", max_words

	# unserialize data
	print "Importing pickled data lists"
	train_list = pickle.load(file(config.TRAIN_FILE, "r"))
	test_list = pickle.load(file(config.TEST_FILE, "r"))
	
	# prepare text & extract features
	print "Loading training & testing data"
	stemmer = nltk.stem.WordNetLemmatizer()
	training_set = load_samples(train_list, stemmer, max_words)
	testing_set = load_samples(test_list, stemmer, max_words)
	print "Train on %d samples, Test on %d samples" % (len(training_set), len(testing_set))
	
	# do the actual classifier training
	instance = None
	if classifier == nltk.classify.NaiveBayesClassifier:
		instance = nltk.classify.NaiveBayesClassifier.train(training_set)
		# serialize the classifer to file (for later use)
		with file(config.BAYES_CLASSIFIER_FILE, 'wb') as fp:
			pickle.dump(instance, fp)
	elif classifier == nltk.classify.MaxentClassifier:
		instance = nltk.classify.MaxentClassifier.train(training_set, max_iter=config.MAX_TRAINING_ITERS)
		# serialize the classifer to file (for later use)
		with file(config.MAXENT_CLASSIFIER_FILE, 'wb') as fp:
			pickle.dump(instance, fp)
	elif classifier == nltk.classify.DecisionTreeClassifier:
		instance = nltk.classify.DecisionTreeClassifier.train(training_set, binary=False)
		# serialize the classifer to file (for later use)
		with file(config.DTREE_CLASSIFIER_FILE, 'wb') as fp:
			pickle.dump(instance, fp)

	# test classifier accuracy with the test set
	print "Evaluating classifier accuracy..."
	accuracy = nltk.classify.util.accuracy(instance, testing_set)
	print "Classifier accuracy:", accuracy
	
	if  classifier != nltk.classify.DecisionTreeClassifier:
		instance.show_most_informative_features(10)
	else:
		print instance.pp(width=70, prefix=u'', depth=4)
	print "-"*80
	
	# manual classification test 
	'''	
		test_data = test_list
		num = 0
		for f,tag in test_data:
			article = data.Article(f)
			feats = bag_of_words(nltk.tokenize.wordpunct_tokenize(article.text), stemmer)
			got = classifier.classify(feats)
			result = (got == tag)
			if result: num += 1
			print f, "-", result, "-", "expected: ", tag, "got:", got
		print "Passed:", num, "of", len(test_data), "-", num*100/len(test_data), "percent"
	'''
	
# script start spot
if __name__ == "__main__":
	#print "CLI arguments:", sys.argv
	elif "-m" in sys.argv: 
		print "Using MaxentClassifier classifer"
		run(nltk.classify.MaxentClassifier, 100)
	elif "-d" in sys.argv:
		print "Using DecisionTreeClassifier"
		run(nltk.classify.DecisionTreeClassifier, 10)
	else:
		print "Using default NaiveBayesClassifier classifer"
		run(nltk.classify.NaiveBayesClassifier, 1000)