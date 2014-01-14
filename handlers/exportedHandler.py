#-*- coding: UTF-8 -*-


import os
import setting
import common
from persistence import fileMgr
import failedHandler

logger = common.getLogger(__name__)

class Handler(object):
	"""Hanlder for moving parsing successed file to exported folder"""
	def __init__(self):
		super(Handler, self).__init__()
		cfgExportedHandler = setting.app['handlers']['exported']
		self.folder = cfgExportedHandler['folder']

		fileMgr.verifyExists(self.folder)
		

	def handle(self,passedFile):
		fileMgr.moveFile(passedFile,self.folder)
		logger.info(u'the file {} has been moved into {} folder'.format(passedFile,self.folder))

		pair = os.path.split(passedFile)
		fileName = pair[1]
		logger.debug(u'the exported file name {}'.format(fileName))
		failedHandler.removeFile(fileName)

	def close(self):
		logger.info('exported handler closed')
		return
		