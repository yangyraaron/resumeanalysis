#-*- coding: UTF-8 -*-


import common
import pymongo
from pymongo import MongoClient

logger = common.getLogger(__name__)


class ResumeMgr(object):

    """resume manager class for mongodb"""

    def __init__(self, host='localhost', port='27017'):
        super(ResumeMgr, self).__init__()
        self.db = None
        self.isConnected = False
        self.host = host
        self.port = port
        self.url = 'mongodb://{}:{}/'.format(host, port)

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
            self.isConnected = False
            logger.error('can not connect ot mongodb {}'.format(self.url),exc_info=True)
            #logger.error('exception:{}'.format(str(e)))

        else:
            self.isConnected = True

        return self.isConnected

    def _has(self, userInfo):
    	userName = userInfo['userName']
        mobile = userInfo['mobile']

        try:
            users = self.db.users
            user = users.find_one({'mobile': mobile})

            return user is not None
        except pymongo.errors.ConnectionFailure as ce:
            self.isConnected = False
            logger.error('connecton is lost')
        except Exception as e:
            logger.error(u'check if user {} has been exist error!'.format(userName),exc_info=True)
            #logger.error('exception:{}'.format(str(e)))

    def addUser(self, userInfo):
        userName = userInfo['userName']
        logger.debug(u'add user {}'.format(userName))

        if self._verifyConnection():
            if self._has(userInfo):
                logger.info(
                    u'the user {} is already in database'.format(userName))
                return 2

            try:
                users = self.db.users
                users.insert(userInfo)
            except pymongo.errors.ConnectionFailure as ce:
                self.isConnected = False
                logger.error('connecton is lost',exc_info=True)
                return 1
            except Exception as e:
                logger.error(u'add user {} error!'.format(userName),exc_info=True)
                #logger.error('exception:{}'.format(str(e)))
                return 1

            return 0
