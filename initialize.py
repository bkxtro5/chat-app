# File: initialize.py
# Prepares a new instance of Chat by creating the database and log.
# NEEDS TO BE RUN BEFORE STARTING THE SERVER FOR THE FIRST TIME!
# Version 1.0

import pylogger
import dbio
from time import sleep

print("Creating log file.")
pylogger.createLog()
print("Done.")
print("Creating database.")
dbio.databaseInitialize()
print("Done.")
print("You can start the server by running startserver.py.")
pylogger.logEvent("information","Initialization completed.")
sleep(30)

