# File: dbio.py
# Chat database reader/writer.
# Version: 1.1

import sqlite3
import pylogger
import sys

databasePath = ".\db\chat.db"


def databaseInitialize():
	pylogger.logEvent("debug", "++Enter databaseInitialize")
	try:
		with open(databasePath) as DataBaseCheck: pass
		conn = sqlite3.connect(databasePath)
		pylogger.logEvent("information", "Found database file.")
	except IOError as Exception:
		pylogger.logEvent("warning", "No database file found. Creating new database.")
		conn = sqlite3.connect(databasePath)
		conn.commit()
		c = conn.cursor()
		c.execute('''create table chatSlate(messageId, timeStamp, userName, message)''')
		conn.commit()
		pylogger.logEvent("information", "Database successfully created.")
	pylogger.logEvent("debug", "--Exit database Initialize")
	

def writeToDatabase(user, message):
	pylogger.logEvent("debug", "++Enter writeToDatabase")
	databaseInitialize()
	conn = sqlite3.connect(databasePath)
	c = conn.cursor()
	pylogger.logEvent("debug", "Writing a message to database.")
	chatTuple = (columnCount(), pylogger.getTime(), user, message)
	c.execute('insert into chatSlate values (?,?,?,?)', (chatTuple),)
	conn.commit()
	pylogger.logEvent("debug", "--Exit writeToDatabase")
	
def readFromDatabase(requestType, *args):
	pylogger.logEvent("debug", "++Enter readFromDatabase")
	conn = sqlite3.connect(databasePath)
	c = conn.cursor()
	pylogger.logEvent("debug", "Reading from database.")
	try:
		if requestType == "topFifty":
			c.execute('select * from chatSlate order by messageId limit 50')
		elif requestType == "allRows":
			c.execute('select * from chatSlate')
		elif requestType == "lastMessageFromUser":
			for ar in args:
				theUser = ar
			query = "select * from chatSlate where userName = '" + theUser + "' order by messageId desc limit 1"
			c.execute(query)
		else:
			pylogger.logEvent("error", "Did not understand requestType.")
	except:
		err = "Failed to read database, exception: " + str(sys.exc_info()[0]) 
		pylogger.logEvent("error", err)
	pylogger.logEvent("debug", "--Exit readFromDatabase")
	return c
	
def columnCount():
	pylogger.logEvent("debug", "++Enter columnCount")
	count = 1
	pylogger.logEvent("debug", "Getting column count.")
	rows = readFromDatabase("allRows")
	for eachMessage in rows:
		count = count + 1
	return count
	

def test():
	pylogger.logEvent("debug", "++Enter dbio tests")
	print("1. Database creation.")
	databaseInitialize()
	print("2. Database confirm.")
	databaseInitialize()
	print("3. Sample chat message.")
	writeToDatabase("Test", "Test Message.")
	print("4. Read from database.")
	results = readFromDatabase("allRows")
	for eachMessage in results:
		print(eachMessage)
	print("Do you see messages above?")
	print("Tests complete.")
	print("Check logs to confirm logging is working.")
	pylogger.logEvent("debug", "--Exit dbio tests")

#test()
