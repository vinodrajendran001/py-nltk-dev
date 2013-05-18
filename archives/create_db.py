import struct, sqlite3, os

DB_FILE = 'temp.db'
NEW_DB_FILE = 'city.db'
INPUT_FILE = 'worldcitiespop.txt'

try:
	# delete all .db files
	filelist = [ f for f in os.listdir(".") if f.endswith(".db") ]
	for f in filelist: 
		print "Deleting:", f
		os.remove(f)
except:
	pass
	
print "Creating SQL tables..."
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''CREATE TABLE cities (name VARCHAR(300));''')

print "Filling tables with info..."
index = 0
fp = file(INPUT_FILE, "r")
for line in fp:
	index += 1
	if index == 1: continue # skip header line
	chunk = line.split(",")
	conn.execute("INSERT INTO cities VALUES (?);", (unicode(chunk[1], errors='ignore'),))
	if index % 10000 == 0: # inform about status
		conn.commit()
		print "inserted", index, "values"

print "Load done, cleaning up..."
fp.close()
conn.commit()

# now some entries in the temp DB have duplicate values, remove them!
print "Creating unique SQL tables..."
new_conn = sqlite3.connect(NEW_DB_FILE)
new_c = new_conn.cursor()
new_c.execute('''CREATE TABLE cities (name VARCHAR(300));''')

print "Selecting unique cities..."
for row in c.execute('''select distinct name from cities;'''):
	new_c.execute("INSERT INTO cities VALUES (?);", row)
new_conn.commit()

conn.close()
new_conn.close()

print "Job done. You can have your beer now."