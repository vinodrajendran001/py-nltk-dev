# USED CONFIGURATION PARAMETERS

OUTPUT_CATEGORIES = "categories.dat"  # all categories frequencies export file
TOP5_CATEGORIES = "category_top5.dat" # top 5 most frequent categories export file
TRAIN_FILE = "training_set.dat"		  # list of article filenames for training
TEST_FILE = "testing_set.dat"		  # list of article filenames for testing
DIRECTORY = "db" 					  # root directory to parse for files
TRAINING_SET_SIZE = 20 				  # percentage of training set size
MAX_TRAINING_ITERS = 5				  # number of MaxEntClassifier iteration before stopping
MAX_SENTENCES = 6					  # max sentences for simple summarizer -> changed to one third of the original article length

# dump pickled classifier to this file
BAYES_CLASSIFIER_FILE = 'bayes_classifier.pickle'
MAXENT_CLASSIFIER_FILE = 'maxent_classifier.pickle'
DTREE_CLASSIFIER_FILE = 'dtree_classifier.pickle'

BAYES_CLASSIFIER_FILE_PATTERN = 'bayes_binary_classifier_%s.pickle'
MAXENT_CLASSIFIER_FILE_PATTERN = 'maxent_binary_classifier_%s.pickle'
DTREE_CLASSIFIER_FILE_PATTERN = 'dtree_binary_classifier_%s.pickle'

MALE_NAME_FILE = "archives/male.txt"
FEMALE_NAME_FILE = "archives/female.txt"
CITY_DB_FILE = 'archives/city.db'
COUNTRY_FILE = 'archives/country.txt'
EN_DICTIONARY = 'archives/en_dictionary_no_names.txt' 
FULL_EN_DICTIONARY = 'archives/en_dictionary.txt'

DUMP_FILES = {
	"A": "articles_A.dat",
	"B": "articles_B.dat",
	"C": "articles_C.dat",
	"D": "articles_D.dat",
	"E": "articles_E.dat",
	"MULTI": "articles_MULTI.dat",
	"OTHER": "articles_OTHER.dat",
}