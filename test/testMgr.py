#-*- coding: UTF-8 -*-


import os
import shutil
import logging
import context 

logger = logging.getLogger('testEnv.'+__name__)

def createExportsEnv(exportedFolder,dest):
	try:
		shutil.copytree(exportedFolder,dest)
	except Exception:
		logger.error('create exported env with error',exc_info=True)


def cleanFolder(path):

	try:
		shutil.rmtree(path)
	except OSError:
		logger.error('clean {} with error'.format(path),exc_info=True)

def _cleanLog():
	logger.info('cleaning files....')
	cleanFolder(context.resumesFolder)
	cleanFolder(context.exportedHandler['folder'])
	cleanFolder(context.failedHandler['folder'])
	cleanFolder(context.duplicateHandler['folder'])

def clean():
	_cleanLog()


def build():
	logger.info('build export env')

	exoportResumesFolder = u'{}/test/{}'.format(context.rootPath, 'resumes')

	_cleanLog()

	logger.info('copy files...')

	createExportsEnv(exoportResumesFolder, context.resumesFolder)


def buildFailed():
	logger.info('build failed env')
	failedResumesFolder = u'{}/test/{}'.format(context.rootPath, 'failed')

	_cleanLog()
	
	logger.info('copy files...')
	createExportsEnv(failedResumesFolder, context.resumesFolder)
		

