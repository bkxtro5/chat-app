# File: chat.py
# Core chat application code which build the page, returns it, and handles new messages.
# Version: 1.1

try:
	import cgi
	import pylogger
	import dbio
except:
	pageFail = True

pageFail = False
	
form = cgi.FieldStorage()
userName = form.getvalue('usr')
message = form.getvalue('msg')

def getLastMessage(userName):
	lastMessage = ' '
	pylogger.logEvent("debug", "++Enter getLastMessage")
	try:
		lastEntry = dbio.readFromDatabase("lastMessageFromUser", userName)
		for entry in lastEntry:
			lastMessage = str(entry[3])
	except UnboundLocalError:
		pylogger.logEvent("debug", "Unknown user in chat.")
		pass
	pylogger.logEvent("debug", "--Exit getLastMessage")
	pageFail = True
	return lastMessage

if userName is not None and message is not None:
	if getLastMessage(userName) != message:
		dbio.writeToDatabase(userName, message)
	
def getContent():
	pylogger.logEvent("debug", "++Enter getContent")
	chats = dbio.readFromDatabase("topFifty")
	pylogger.logEvent("debug", "--Exit getContent")
	return chats


def pageBuilder(pageType):
	pylogger.logEvent("debug", "++Enter pageBuilder")
	pageToServe = ""
	if pageType == "error":
		pageToServer = pageToServe + """
		<html>
		<header>
		<title>An error has occurred.</title>
		</header>
		<body>
		<b><center>An Error as occurred while trying to serve this webpage.</center></b>\n
		</body>
		</html>"""
		pylogger.logEvent("warning", "Returning error page.")
	else:
		pageToServe = pageToServe + """
		<html>
		<header>
		<title>Chat</title>
		</header>
		<body>
		<textarea rows="40" cols="100">"""
		for message in getContent():
			messageParts = str(message[1]) + " - " + str(message[2]) + " - " + str(message[3]) + "\n"
			pageToServe = pageToServe + messageParts
		pageToServe = pageToServe + """
		</textarea>
		<br>
		<br>
		<form action="chat.py">\nUSR: <input type="text" name="usr" value=""><br>\nMSG: <input type="text" size="100" name="msg"value=""><br>\n<input type="submit" value="Submit">
		</body>
		</html>"""
	pylogger.logEvent("debug", "--Exit pageBuilder")
	print(pageToServe)

if pageFail == True:
	pageBuilder(error)
else:
	pageBuilder("else")
