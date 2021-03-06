# File: chat.py
# Core chat application code which build the page, returns it, and handles new messages.
# Version 2.0

# Application version.
appVersion = "1.3.0"
# Initializing pageError as False.
pageError = False
# Initializing validationFailed as False.
validationFailed = False

try:
    import cgi
    import pylogger
    import dbio
    import verifymessage
    import chatconfig
    import messagewindow
except:
    pageError = True
    pass

showDebugPageOnFailure = chatconfig.showDebugPageOnFailure
showValidationErrors = chatconfig.showValidationErrors

pylogger.logEvent("information", ">>> New GET request. Imports successful.")

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
<iframe>
"""

goodPagePartC = """
</iframe>
<br>
<br>
"""

goodPagePartD = """
<br>
<br>
<br>
<font size=1>v. """ + appVersion + """
</font>
"""

goodPagePartE = """
</body>
</html>
"""

validationResponse = """
<br>
<b><font color=red>Message validation failed, not commiting to database.</font></b>
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

def buildPage():
    pylogger.logEvent("trace", "++Enter buildPage")
    totalPage = goodPagePartA + goodPagePartB + str(messagewindow.makeSubPage()) + goodPagePartC + str(userNamePersistance()) + goodPagePartD
    if showValidationErrors == True and validationFailed == True:
        totalPage = totalPage + validationResponse
    totalPage = totalPage + goodPagePartE
    pylogger.logEvent("trace", "--Exit buildPage")
    return totalPage

if userName is not None and message is not None:
    if verifymessage.validateMessage(userName, message) == False:
        pylogger.logEvent("debug", "Saving message to database.")
        dbio.writeToDatabase(userName, message)
    else:
        pylogger.logEvent("debug", "Not saving to database.")
        validationFailed = True
else:
    pylogger.logEvent("debug", "New page request. Nothing to save to database.")

if pageError == True and showDebugPageOnFailure == True:
    pylogger.logEvent("error", "Building page failed. Generating debug error page for client.")
    print(debugFailurePage)
elif pageError == True and showDebugPageOnFailure == False:
    pylogger.logEvent("error", "Building page failed. Generating regular error page for client.")
    print(regularFailurePage)
else:
    pylogger.logEvent("debug", "Generating regular page for client.")
    print(buildPage())

pylogger.logEvent("information", "<<< Page returned to requestor. END.")
