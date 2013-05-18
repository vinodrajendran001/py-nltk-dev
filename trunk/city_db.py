import sqlite3

CITY_DB_FILE = 'archives/city.db'
COUNTRY_FILE = 'archives/country.txt'

class CityChecker:
	def __init__(self):
		self.conn = sqlite3.connect(CITY_DB_FILE)
		self.c = self.conn.cursor()
		self.countries = set()
		for index, country in enumerate(file(COUNTRY_FILE, 'r')):
			if index % 2 == 0: continue # skip every first line - the id
			self.countries.add(country.strip().lower())
		
	def hasCity(self, name):
		for row in self.c.execute('''SELECT 1 FROM cities WHERE name=?;''', (name.lower(),)):
			return True
		return False
		
	def hasCountry(self, name):
		return (name.lower() in self.countries)
		
	def close(self):
		self.conn.close()
		
if __name__ == "__main__":
	# testing
	print "Running tests..."
	cc = CityChecker()
	print cc.hasCity("Vilnius")==True
	print cc.hasCity("riga")==True
	print cc.hasCity("non-existing")==False
	print cc.hasCity("Riga")==True
	print cc.hasCountry("l")==False
	print cc.hasCountry("russia")==True
	print cc.hasCountry("Lithuania")==True
	print cc.hasCountry("Vilnius")==False
	cc.close()