# File: chat.py
# Core chat application code which build the page, returns it, and handles new messages.
# Version: 1.0

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

if userName is not None and message is not None:
	dbio.writeToDatabase(userName, message)
	
def getContent():
	pylogger.logEvent("debug", "++Enter getContent")
	chats = dbio.readFromDatabase("topFifty")
	pylogger.logEvent("debug", "--Exit getContent")
	return chats

def pageBuilder(pageType):
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
	print(pageToServe)

if pageFail == True:
	pageBuilder(error)
else:
	pageBuilder("else")
