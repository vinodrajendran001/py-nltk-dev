import sys
sys.path.append("..") # allow to include `config` from parent directory

import nltk, pickle, config, data, random

# samples: text_tag/class, text
train = [
	["ruduo", "obuoliai buvo skanus, taciau jais megautis galima tik rudeni"], 
	["ruduo", "rudens gerybes neuzilgo prades rodyti savo pintines"],
	["pietauti", "skanulis isiverze i savo valgykla ir tare - duokit edalo"],
	["pietauti", "valgykloje valge keturi miesteciai ir du is ju buvo su kepure"],
	["grybauti", "rudens miskas slepia ypatingus skanumynus tiesiog po berzo keru, paimi gryba ir dziaugiesi!"],
	["grybauti", "grybavimas gali buti labai malonus uzsiemimas"]
]

test = [
	["ruduo", "kriauses, obuoliai ir siaip, geltoni klevo lapai parodo, kad jau nebe vasara"], 
	["ruduo", "kas zino, gal visos balos, kurios atsiranda rudeni isnyks vos tik pakelsime pintines"],
	["pietauti", "du gyventojai be kepuriu sedejo valgymo istaigoje ir skaniai cepsejo"],
	["pietauti", "mama pakviete mane pavalgyti, nors norejau jau lekti i Biciulius, bet neteko nusivilti"],
	["grybauti", "raudonikiai, baravykai ir kiti grybai man labai patinka, ypac rudeni prie bulviu"],
	["ruduo", "patyres grybautojas Rimas sako, jog reiketu perdaryti visa rudens sezono skrajuciu pateikima"],
	["ruduo", "sakoma, jog vandens bus iki kaklo, kai prades lyti"],
	["ruduo", "aplink rudeneja dabar visur, gal sutems greitai"], 
	["ruduo", "visur telksojo vienos balos ir pageltusiu lapu kruvos"]
]

# generate a dictionary of all words (features)
def bag_of_words(wordlist, stemmer):
	return {stemmer.lemmatize(word.lower()):True for word in wordlist if len(word) > 1}


def load_samples(sample_list, stemmer):
	data_set = []
	for cat, text in sample_list:
		tokens = nltk.tokenize.wordpunct_tokenize(text) # chop sentence into words/tokens
		data_set.append((bag_of_words(tokens, stemmer), cat)) # make directory from the words & assign category
	random.shuffle(data_set) # randomly shuffle the data
	return data_set
	
def run():
	# stemmer converts words to their base form, e.g. cats -> cat (only works for english vocabulary now)
	stemmer = nltk.stem.WordNetLemmatizer() 

	print "Loading training & testing data"
	training_set = load_samples(train, stemmer)
	testing_set = load_samples(test, stemmer)
	
	print "Train on %d instances, Test on %d instances" % (len(training_set), len(testing_set))
	 
	classifier = nltk.classify.NaiveBayesClassifier.train(training_set)
	accuracy = nltk.classify.util.accuracy(classifier, testing_set)
	print "Classifier accuracy:", accuracy
	classifier.show_most_informative_features(10)
	
	print "-"*80


# if we launch this script by double-click, then execute code below
if __name__ == "__main__": 
	run()
