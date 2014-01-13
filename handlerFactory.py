#-*- coding: UTF-8 -*-


from handlers import exportedHandler
from handlers import failedHandler
from handlers import duplicateHandler

# log a failed record and move failed file into failed folder
def getFailedHandler():
	return failedHandler.Handler()

# move succeed file into exported folder only
def getExportedHandler():
	return exportedHandler.Handler()

# make a duplicate record only
def getDuplicateHandler():
	return duplicateHandler.Handler()
	