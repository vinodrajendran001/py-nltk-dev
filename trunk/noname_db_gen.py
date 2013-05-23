import nltk, config, city_db

# Purpose: generates a words dictionary file by removing people names from full dictionary

OUTPUT = "nonames.txt"

# load names database
with open(config.MALE_NAME_FILE) as fp:
	male = {line.strip().lower():True for line in fp}
with open(config.FEMALE_NAME_FILE) as fp:
	female = {line.strip().lower():True for line in fp}
# load dictionary
with open(config.FULL_EN_DICTIONARY) as fp:
	dictionary = {line.strip().lower():True for line in fp}

i = 0
for key in male.keys():
	if key in dictionary:
		del dictionary[key]
		print "removed",key
		i += 1
	
for key in female.keys():
	if key in dictionary:
		del dictionary[key]
		print "removed",key
		i += 1
	
fp = file(OUTPUT, "w")
keys = dictionary.keys()
keys.sort()
for w in keys:
	if len(w.strip()) > 0:
		fp.write(w+"\n")
fp.close()

print "removed words total =", i
print "done."