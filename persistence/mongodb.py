#-*- coding: UTF-8 -*-


import common
from pymongo import MongoClient

logger = common.getLogger(__name__)

class ResumeMgr(object):
	"""resume manager class for mongodb"""
	def __init__(self,host='localhost',port='27017'):
		super(ResumeMgr, self).__init__()
		self.db = None
		self.isConnected = False
		self.host = host
		self.port = port
		self.url = 'mongodb://{}:{}/'.format(host,port)

	def _connect(self):
		client = MongoClient(self.url)
		logger.info('connecting to {}'.format(self.url))

		self.db = client.resume

	def _verifyConnection(self):
		if self.isConnected:
			return self.isConnected

		try:
			self._connect()
		except Exception as e:
			logger.error('can not connect ot mongodb {}'.format(self.url))
			logger.error('exception:{}'.format(str(e)))

		else:
			self.isConnected = True

		return self.isConnected

	def addUser(self,userInfo):
		userName = userInfo['userName']
		logger.debug(u'add user {}'.format(userName))

		if self._verifyConnection():
			try:
				users = self.db.users
				users.insert(userInfo)
			except Exception as e:
				logger.error('add user {} errors!'.format(userName))
				logger.error('exception:{}'.format(str(e)))







	
