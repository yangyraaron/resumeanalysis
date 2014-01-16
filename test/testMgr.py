#-*- coding: UTF-8 -*-


import os
import shutil
import common 

logger = common.getLogger(__name__)

def createExportsEnv(exportedFolder,dest):
	try:
		shutil.copytree(exportedFolder,dest)
	except Exception:
		logger.error('create exported env with error',exc_info=True)

def createFailedEnv():
	pass

def clean(path):

	try:
		shutil.rmtree(path)
	except OSError:
		logger.error('clean {} with error'.format(path),exc_info=True)
		

