import sqlite3

class io:
	def __init__(self, db):
		self.con = sqlite3.connect(db)
		self.cur = self.con.cursor()

	def makeStorage(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS storage(id TEXT,email TEXT,password TEXT);")
		self.con.commit()

	def writeStorage(self, queries):
		self.cur.execute("INSERT INTO storage VALUES(?,?,?);", queries)
		self.con.commit()
	
	def readStorage(self, attr="*"):
		self.cur.execute(f"SELECT {attr} FROM storage")
		result = self.cur.fetchall()
		return result

	def closeStorage(self):
		self.con.close()

class todosIO(io):
	def makeStorage(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS todos(path TEXT, location TEXT, time TEXT);")
		self.con.commit()

	def writeStorage(self, queries):
		self.cur.execute("INSERT INTO todos VALUES(?,?,?);", queries)
		self.con.commit()
	
	def readStorage(self, attr="*"):
		self.cur.execute(f"SELECT {attr} FROM todos")
		result = self.cur.fetchall()
		return result