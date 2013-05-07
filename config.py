# USED CONFIGURATION PARAMETERS

OUTPUT_CATEGORIES = "categories.dat"  # all categories frequencies export file
TOP5_CATEGORIES = "category_top5.dat" # top 5 most frequent categories export file
TRAIN_FILE = "training_set.dat"		  # list of article filenames for training
TEST_FILE = "testing_set.dat"		  # list of article filenames for testing
DIRECTORY = "db" 					  # root directory to parse for files
TRAINING_SET_SIZE = 20 				  # percentage of training set size
MAX_TRAINING_ITERS = 5				  # number of MaxEntClassifier iteration before stopping
CLASSIFIER_FILE = 'classifier.pickle' # dump pickled classifier to this file
MALE_NAME_FILE = "names/male.txt"
FEMALE_NAME_FILE = "names/female.txt"
CITY_FILE = "cities/world_cities.txt"