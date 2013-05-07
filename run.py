import nltk, data, summarize, pickle, ner, config, training
from nltk.tree import Tree

# load demo article
path = "db/uktveris-tomas/2010-12-01-1.txt"
article = data.Article(path)
print "-"*80

# show the text in console
print article.text
print "-"*80

# tokenize the text (split into words)
tokens = nltk.tokenize.wordpunct_tokenize(article.text)
tagged = nltk.pos_tag(tokens)

# extract features & try to classify the article (classifier is loaded from serialized pickle file)
features = training.bag_of_words(tokens, tokens, nltk.stem.WordNetLemmatizer())
classifier = pickle.load(file(config.CLASSIFIER_FILE, "rb"))
print "Category of text:",classifier.classify(features)