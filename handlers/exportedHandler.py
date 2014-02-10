#-*- coding: UTF-8 -*-


import os
import setting
import context
import common
from persistence import fileMgr
import failedHandler

logger = common.getLogger(__name__)

class Handler(object):
	"""Hanlder for moving parsing successed file to exported folder"""
	def __init__(self):
		super(Handler, self).__init__()
		#cfgExportedHandler = setting.app['handlers']['exported']
		
		self.folder = context.exportedHandler['folder']
		self.targetFolder = context.exportedHandler['targetFolder']

		fileMgr.verifyExists(self.folder)
		fileMgr.verifyExists(self.targetFolder)

	def _buildTargetFile(self,fileName):
		if self.soup is None:
			logger.debug('the soup is None')
			return

		target = u'{}/{}'.format(self.targetFolder,fileName)
		try:
			f = open(target,'w+')
			content = str(self.soup)
			f.write(content)

			logger.info(u'target file {} has been build'.format(target))
		except Exception, e:
			logger.error(u'build target file {} failed!'.format(target),exc_info=True)
		finally:
			f.close()
		

	def handle(self,passedFile,soup):
		self.soup = soup

		fileMgr.moveFile(passedFile,self.folder)
		logger.info(u'the file {} has been moved into {} folder'.format(passedFile,self.folder))

		pair = os.path.split(passedFile)
		fileName = pair[1]

		logger.debug(u'build target file for {}'.format(fileName))
		self._buildTargetFile(fileName)

		logger.debug(u'the exported file name {}'.format(fileName))
		failedHandler.removeFile(fileName)

	def close(self):
		logger.info('exported handler closed')
		return
		