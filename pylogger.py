# File: pylogger.py
# Basic, reusable logging engine for Python 3.3.
# Version: 1.2

import time
from os import path
import sys

loggingLevel = "debug"
logFileName = ".\logs\chatapp.log"

dictLogLevel = {"trace":6,"debug":5,"information":4,"warning":3,"error":2,"fatal":1}

def createLog():
	if path.isfile(logFileName) == True:
		logEvent("information", "Log file found.")
	else:
		log = open(logFileName, "w")
		log.write("==========BEGINNING OF LOG FILE==========\n")
		log.close()
		logEvent("information", "Log file created successfully.")

def getTime():
	theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	return theTime
	
def getUnixTime():
	uTime = time.time()
	return uTime

def logEvent(eventSeverity, eventData):
	if dictLogLevel[eventSeverity] <= dictLogLevel[loggingLevel]:
		log = open(logFileName, "a")
		dataToLog = getTime() + " - " + eventSeverity + " - " + eventData + "\n"
		log.write(dataToLog)
		return True
	else:
		return False

def test():
	logEvent("debug", "++Enter testMethod.")
	a = 2 + 2
	logEvent("information", "Successfully added two numbers together.")
	try:
		2 / 0
	except:
		e = sys.exc_info()[0]
		logEvent("error", str(e))
	logEvent("debug", "--Exit testMethod.")

#test()
