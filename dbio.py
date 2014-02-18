# File: dbio.py
# Chat database reader/writer.
# Version: 1.2

import sqlite3
import pylogger
import sys
import chatconfig

databasePath = chatconfig.databasePath


def databaseInitialize():
    pylogger.logEvent("trace", "++Enter databaseInitialize")
    try:
        with open(databasePath) as DataBaseCheck: pass
        conn = sqlite3.connect(databasePath)
        pylogger.logEvent("debug", "Found database file.")
    except IOError as Exception:
        pylogger.logEvent("warning", "No database file found. Creating new database.")
        conn = sqlite3.connect(databasePath)
        conn.commit()
        c = conn.cursor()
        c.execute('''create table chatSlate(messageId, unixTime, timeStamp, userName, message)''')
        conn.commit()
        pylogger.logEvent("information", "Database successfully created.")
    pylogger.logEvent("trace", "--Exit database Initialize")


def writeToDatabase(user, message):
    pylogger.logEvent("trace", "++Enter writeToDatabase")
    try:
        databaseInitialize()
        conn = sqlite3.connect(databasePath)
        c = conn.cursor()
        pylogger.logEvent("debug", "Writing a message to database.")
        chatTuple = (columnCount(), pylogger.getUnixTime(), pylogger.getTime(), user, message)
        c.execute('insert into chatSlate values (?,?,?,?,?)', (chatTuple),)
        conn.commit()
    except:
        err = "An error occurred during save. " + str(sys.exc_info()[0])
        pylogger.logEvent("error", err)
    pylogger.logEvent("trace", "--Exit writeToDatabase")

def readFromDatabase(requestType, *args):
    pylogger.logEvent("trace", "++Enter readFromDatabase")
    conn = sqlite3.connect(databasePath)
    c = conn.cursor()
    pylogger.logEvent("debug", "Reading from database.")
    try:
        if requestType == "topFifty":
            q = "select * from chatSlate limit 50 offset " + str(columnCount() - 50)
            c.execute(q)
        elif requestType == "allRows":
            c.execute('select * from chatSlate')
        elif requestType == "lastMessageFromUser":
            for ar in args:
                theUser = ar
            query = "select * from chatSlate where userName = '" + theUser + "' order by messageId desc limit 1"
            c.execute(query)
        else:
            pylogger.logEvent("error", "Did not understand requestType.")
    except Exception as e:
        err = "Failed to read database, exception: " + str(sys.exc_info()[0]) + " " + str(e)
        pylogger.logEvent("error", err)
    pylogger.logEvent("trace", "--Exit readFromDatabase")
    return c.fetchall()

def columnCount():
    pylogger.logEvent("trace", "++Enter columnCount")
    count = 1
    pylogger.logEvent("debug", "Getting column count.")
    rows = readFromDatabase("allRows")
    for eachMessage in rows:
        count = count + 1
    pylogger.logEvent("trace", "--Exit columnCount")
    return count


def test():
    pylogger.logEvent("trace", "++Enter dbio tests")
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
    pylogger.logEvent("trace", "--Exit dbio tests")

#test()
