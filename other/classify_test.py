import nltk, pickle, config, data, random

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
	["ruduo", "du gyvenotjai be kepuriu sedejo valgymo istaigoje ir skaniai cepsejo"],
	["ruduo", "mama pakviete mane pavalgyti, nors norejau jau lekti i Biciulius, bet neteko nusivilti"],
	["ruduo", "raudonikiai, baravykai ir kiti grybai man labai patinka, ypac rudeni prie bulviu"],
	["ruduo", "patyres grybautojas Rimas sako, jog reiketu perdaryti visa rudens ir valgymo sezono skrajuciu pateikima"],
	["ruduo", "sakoma, jog vandens bus iki kaklo, kai prades lyti"],
	["ruduo", "aplink ruda dabar visur, gal sutems greitai"], 
	["ruduo", "visur styrojo vienos balos ir pageltusiu lapu kruvos"]
]

def bag_of_words(wordlist, stemmer):
	return dict([(stemmer.lemmatize(word.lower()), True) for word in wordlist if len(word) > 1])
	
def load_samples(sample_list, stemmer):
	data_set = []
	for cat, text in sample_list:
		tokens = nltk.tokenize.wordpunct_tokenize(text)
		data_set.append((bag_of_words(tokens, stemmer), cat))
	random.shuffle(data_set)
	return data_set
	
def run():
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

	
if __name__ == "__main__":
	run()
