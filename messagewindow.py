# File: messagewindow.py
# Creates the message window page used within chat.py
# Version 1.0

import chatconfig
import dbio
import pylogger
import verifymessage

numberOfPastMessages = chatconfig.numberOfPastMessages

pylogger.logEvent("debug", "Starting to make subpage.")

messageSubPagePartA = """
<html>
<header>
<script type="text/javascript"
    src="http://code.jquery.com/jquery-latest.js">
</script>

<script type="text/javascript">
    setTimeout(function(){
        window.location.reload(1);
    }, 5000);
</header>
<body>
<textarea rows="40" cols="100">
"""

messageSubPagePartB = """
</textarea>
</body>
</html>
"""
def getContent():
    pylogger.logEvent("trace", "++Enter getContent")
    chats = dbio.readFromDatabase(numberOfPastMessages)
    pylogger.logEvent("trace", "--Exit getContent")
    return chats

def makeMessages():
    pylogger.logEvent("trace", "++Enter makeMessages")
    pylogger.logEvent("debug", "Putting messages together for page.")
    allMessages = ""
    for message in getContent():
        messagePart = str(message[2]) + " - " + str(message[3]) + " - " + str(message[4]) + "\n"
        allMessages = allMessages + messagePart
    pylogger.logEvent("trace", "--Exit makeMessages")
    return allMessages

def makeSubPage():
    totalSubPage = messageSubPagePartA + makeMessages() + messageSubPagePartB
    pylogger.logEvent("debug", "Finished making subpage.")
    return totalSubPage
