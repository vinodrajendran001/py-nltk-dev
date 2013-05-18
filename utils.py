# A bunch of utils to make the life easier

def join_tagged(tagged):
	s = ""
	for text, tag in tagged:
		s += " "+text+"/"+tag
	return s