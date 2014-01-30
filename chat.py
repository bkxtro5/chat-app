# File: chat.py
# Core chat application code which build the page, returns it, and handles new messages.
# Version pre-2.0

# Initializing pageError as False.
pageError = False

try:
	import cgi
	import pylogger
	import dbio
	import verifymessage
except:
	print("SUM TING WONG")
	pageError = True

# ===Configuration===	
showDebugPageOnFailure = False
numberOfPastMessages = "topFifty"
# ===Configuration===

pylogger.logEvent("debug", "Import successful. Starting to build page.")

debugFailurePage = """
<html>
<header>
<title>An error has occurred</title>
</header>
<body>
<h1>An error occurred while trying to build this page.</h1>
<br>
<br>
Check your logs. If the log level is not set to "debug", change it. This may reveal the issue.
<br>
Also, try checking the sever error logs, printed in the startserver.py window.
</body>
"""

regularFailurePage = """
<html>
<header>
<title>Oops!</title>
</header>
<body>
<h1>Something went wrong.</h1>
<br>
<br>
Something must have failed. Let me know and I'll look into it and/or try refreshing the page.
</body>
"""

goodPagePartA = """
<html>
<header>
<title>Chat</title>
</header>
<body>
"""

goodPagePartB = """
<textarea rows="40" cols="100">
"""

goodPagePartC = """
</textarea>
<br>
<br>
"""

goodPagePartD = """
</body>
</html>
"""

pylogger.logEvent("debug", "Attempting to get userName and message from GET request.")
form = cgi.FieldStorage()
userName = form.getvalue('usr')
message = form.getvalue('msg')

def userNamePersistance():
	if userName is not None:
		dataFields = """
<form action="chat.py">\nUSR: <input type="text" name="usr" value="
"""
		dataFields = dataFields + userName + """
"><br>\nMSG: <input type="text" size="100" name="msg"value=""><br>\n<input type="submit" value="Submit">		
"""
		return dataFields
	else:
		dataFields = """
<form action="chat.py">\nUSR: <input type="text" name="usr" value=""><br>\nMSG: <input type="text" size="100" name="msg"value=""><br>\n<input type="submit" value="Submit">
"""
	return dataFields
		

def getContent():
	pylogger.logEvent("debug", "++Enter getContent")
	chats = dbio.readFromDatabase(numberOfPastMessages)
	pylogger.logEvent("debug", "--Exit getContent")
	return chats
	
def makeMessages():
	allMessages = ""
	for message in getContent():
		messagePart = str(message[2]) + " - " + str(message[3]) + " - " + str(message[4]) + "\n"
		allMessages = allMessages + messagePart
	return allMessages
	
def buildPage():
	totalPage = goodPagePartA + goodPagePartB + str(makeMessages()) + goodPagePartC + str(userNamePersistance()) + goodPagePartD
	return totalPage

if userName is not None and message is not None:
	if verifymessage.validateMessage(userName, message) == False:
		pylogger.logEvent("debug", "Saving message to database.")
		dbio.writeToDatabase(userName, message)
	else:
		pylogger.logEvent("debug", "Validation failed. Not saving to database.")
else:
	pylogger.logEvent("debug", "New page request. Nothing to save to database.")
	
if pageError == True and showDebugPageOnFailure == True:
	pylogger.logEvent("error", "Building page failed. Returned debug error page to client.")
	print(debugFailurePage)
elif pageError == True and showDebugPageOnFailure == False:
	pylogger.logEvent("error", "Building page failed. Returned regular error page to client.")
	print(regularFailurePage)
else:
	print(buildPage())
