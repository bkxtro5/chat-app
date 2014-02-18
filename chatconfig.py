# File: chatconfig.py
# Contains all application configuration in a single file.





# ========== Chat Configuration ==========

# True: Shows a debug page on failure.
# False: Shows regular page on failure.

showDebugPageOnFailure = False

# True: Shows user that their message was not saved.
# False: Message validation fails silently (for user).

showValidationErrors = True

# "topFifty": Shows last 50 messages in database.
# "allRows": Shows ALL messages in database.

numberOfPastMessages = "topFifty"

# ========== Chat Configuration ==========





# ========== Database Configuration ==========

# This is the filename/path to the database file.
# Default value: ".\db\chat.db"

databasePath = ".\db\chat.db"

# ========== Database Configuration ==========





# ========== Server Configuration ==========

# Defines the listening port for server.
# Default value: 9999

port = 9999

# ========== Server Configuration ==========





# ========== Message Verification Configuration ==========


# Defines the minimum number of seconds between duplicate messages.
# Default value: 30

secondsBetweenDuplicateRequests = 30

# ========== Message Verification Configuration ==========





# ========== logging Configuration ==========

# Defines how verbose logging is.
# Options are: trace, debug, information, warning, error
# Default value: information
loggingLevel = "trace"

# This is the filename/path to the log file.
# Default value: ".\logs\chatapp.log"
logFileName = ".\logs\chatapp.log"

# ========== logging Configuration ==========
