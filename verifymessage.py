# File: verifymessage.py
# Validates against duplicate requests before saving message to database.
# Version 1.1

import dbio
import pylogger
import sys
	
def getLastEntryFromUser(userName):
	pylogger.logEvent("debug", "++Enter getLastEntryForUser")
	logMessage = "Looking up user " + str(userName)
	pylogger.logEvent("debug", logMessage)
	try:
		lastEntry = dbio.readFromDatabase("lastMessageFromUser", userName)
		pylogger.logEvent("debug", "Checking result from database.")
		if lastEntry == []:
			pylogger.logEvent("debug", "No entries found for this user.")
			lastEntry = " "
	except Exception as err:
		pylogger.logEvent("error", err)
		lastEntry = " "
		pass
	pylogger.logEvent("debug", "--Exit getLastEntryForUser")
	return lastEntry
	
	
def checkTimeStamp(entry):
	pylogger.logEvent("debug", "++Enter checkTimeStamp")
	for time in entry:
		lastMessageTime = time[1]
	if (pylogger.getUnixTime() - lastMessageTime) > 15:
		pylogger.logEvent("debug", "False. Last message sent more than 15 seconds ago.")
		pylogger.logEvent("debug", "--Exit checkTimeStamp")
		return False
	else:
		pylogger.logEvent("debug", "True. Last message sent less than 15 seconds ago.")
		pylogger.logEvent("debug", "--Exit checkTimeStamp True.")
		return True
	
def checkLastMessage(entry, message):
	pylogger.logEvent("debug", "++Enter checkLastMessage")
	for lastStoredMessage in entry:
		lastMessage = lastStoredMessage[4]
	if lastMessage == message:
		pylogger.logEvent("debug", "True. Message matches last message.")
		pylogger.logEvent("debug", "--Exit checkLastMessage")
		return True
	else:
		pylogger.logEvent("debug", "False. Message does not match last message.")
		pylogger.logEvent("debug", "--Exit checkLastMessage")
		return False

def validateMessage(userName, message):
	pylogger.logEvent("debug", "++Enter validateMessage")
	if getLastEntryFromUser(userName) == " ":
		pylogger.logEvent("debug", "Message validation passed.")
		return False
	elif checkTimeStamp(getLastEntryFromUser(userName)) == False or checkLastMessage(getLastEntryFromUser(userName), message) == False:
		pylogger.logEvent("debug", "Message validation passed.")
		pylogger.logEvent("debug", "--Exit validateMessage")
		return False
	else:
		pylogger.logEvent("debug", "Message validation failed. Duplicate request.")
		pylogger.logEvent("debug", "--Exit validateMessage")
		return True
