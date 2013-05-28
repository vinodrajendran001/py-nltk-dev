import os, datetime, operator, math, random, pickle, config

invalid = ['published', 'archived', 'featured article', 'original reporting'] # invalid catagories in lowercase
cat_freq = {} # categories frequency stored

# remove bad chars from text
def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

class Article:
	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, "rt") as fp:
			lines = fp.readlines()
		
		self.url = lines[0].strip()
		self.title = lines[1].strip()
		self.date = lines[2].strip()
		self.year, self.month, self.day = self.date.split("-")
		self.no = self.filename[:-4].split("-")[-1]
		self.cats = lines[3].split(",")
		
		date = datetime.datetime(int(self.year), int(self.month), int(self.day))
		self.monthname = date.strftime("%B").lower() # month name string
		
		# cleanup categories
		cleaned = []
		for cat in self.cats:
			cat = cat.strip().lower()
			if cat in invalid: continue
			if cat.find(str(int(self.day))) != -1: continue
			if cat.find(self.monthname) != -1: continue
			if cat == self.year: continue
			if cat == "": continue
			cleaned.append(cat)
			# count the frequency of all categories
			if cat in cat_freq:
				cat_freq[cat] += 1
			else:
				cat_freq[cat] = 1
			
		self.cats = cleaned
		self.text = (" ".join(lines[4:])).strip() # join all left text lines to a single line string
		self.text = removeNonAscii(self.text)

	def show(self):
		print "-"*80
		print self.text
		print "-"*80
		
# assigns the class to an article by analyzing its categories
def determine_classes(article, top5):
	tag_list = []
	for (catname, count, class_tag) in top5:	
		if catname in article.cats:
			tag_list.append(class_tag)
	return tag_list

def run():
	# parse all articles & count catagories
	articles = []
	for root, dirs, files in os.walk(config.DIRECTORY):
		for fp in files:
			if fp.endswith('.txt'):
				articles.append(Article(root+"/"+fp))
	print "Total articles parsed:", len(articles)
	
	# compute the number of training set size
	t_needed = int(len(articles) * config.TRAINING_SET_SIZE / 100)
	print "Actual count needed for training set ("+str(config.TRAINING_SET_SIZE)+" percent):", t_needed
	
	# write all categories frequency file
	s = sorted(cat_freq.iteritems(), key=operator.itemgetter(1), reverse=True)
	with open(config.OUTPUT_CATEGORIES, "wt") as fp:
		fp.write(pickle.dumps(s))
	
	# top 5 categories file
	top = s[0:5]
	
	# assign each top5 category a unique identifier (i.e. class/tag)
	tags = ["A","B","C","D","E"]
	for i, (catname, count) in enumerate(top):
		top[i] = [catname, count, tags[i]]
	
	print "-"*80
	print "Top 5 categories: Name, frequency and tag assigned:"
	for i, item in enumerate(top):
		#print "\t%d. %s ="%(i+1, fullname), data
		print "\t%d. %s"%(i+1, item)
	print "-"*80

	with open(config.TOP5_CATEGORIES, "wt") as fp:
		fp.write(pickle.dumps(top));
		
	# count the available articles in the 'top 5'
	num_top5 = 0
	for article in articles:
		for (catname, count, class_tag) in top:
			if catname in article.cats:
				num_top5 += 1
				break
	print "Articles having at least one Top 5 cat:", num_top5
	
	# add some randomness to improve testing/training data generation & robustness
	random.shuffle(articles)
	classmap = {}
	
	# sort all articles by their class/tag
	multiclass = []
	for article in articles:
		tags_list = determine_classes(article, top)
		tag = "OTHER"
		if len(tags_list) == 1:
			tag = tags_list[0]
		elif len(tags_list) > 1:
			tag = "MULTI" # more than one class
			
		if tag in classmap: # count all articles in each class
			classmap[tag].append(article)
		else:
			classmap[tag] = [article]
			
		if tag == "MULTI": # save to split later
			multiclass.append([article, tags_list])
			
	# make positive - negative examples by each class
	for key in classmap.keys():
		if key in config.DUMP_FILES:
			temp = []
			for article in classmap[key]:
				temp.append([article.filename, key])
			for article, tags_list in multiclass: # include multiclass article too (do split)
				if key in tags_list:
					temp.append([article.filename, key])
			fname = config.DUMP_FILES[key]
			print "Dumping " + key + " articles to: " + fname, "found:", len(temp)
			pickle.dump(temp, file(fname, 'w'))
		else:
			print "Dumping " + key + " articles to: skipped"

	print "Articles in each class (class = count):"
	total = 0
	allowed = {}
	tagged_articles = classmap.items()
	for tag, members in tagged_articles:
		count = len(members)
		# ensure that required percent of each class articles is chosen for training & testing
		allowed[tag] = max(int(math.ceil(count * config.TRAINING_SET_SIZE / 100.0)), 1)
		print "\t",tag,"=",count
		total += count
	print "Total:",total

	print "Allowed to use of each class (%d percent):"%(config.TRAINING_SET_SIZE)
	print "\t",sum([allowed[k] for k in allowed.keys()]), "total, items of each class:", allowed
	
	# try filling the training set in iterations 
	# in each iteration add at least one example of each class/tag article (if available - be fair)
	test_set = []
	train_set = []
	index = 0
	while len(train_set) < t_needed: # need to fill the training set first
		tag, article = None, None
		while True:
			tag, members = tagged_articles[index]
			index = (index + 1) % len(tagged_articles)
			if len(members) == 0: continue
			if allowed[tag] == 0: continue
			allowed[tag] -= 1
			article = members.pop()
			break	
		train_set.append([article.filename, tag])
	print "Training set size:", len(train_set)
	
	debug = {}
	for f, tag in train_set:
		if tag in debug:
			debug[tag] += 1
		else:
			debug[tag] = 1
	print "Used for training set:"
	print "\t", len(train_set), "total, items of each class:", debug
	
	# everything left - to testing set
	for tag, members in tagged_articles:
		for article in members:
			test_set.append([article.filename, tag])
	print "Testing set size:", len(test_set)
			
	with open(config.TRAIN_FILE, "wt") as ftrain:
		ftrain.write(pickle.dumps(train_set))
	with open(config.TEST_FILE, "wt") as ftest:
		ftest.write(pickle.dumps(test_set))
		
	print "Training set list written to:", config.TRAIN_FILE
	print "Testing set list written to:", config.TEST_FILE

if __name__ == "__main__":
	run()
	print "Done."