#-*- coding: UTF-8 -*-


import common
import logging
import logging.config
import context
from test import testMgr

# initialize log
logging.config.dictConfig(context.logging)
logger = logging.getLogger('test')


def build():
    testResumesFolder = u'{}/test/{}'.format(context.rootPath, 'resumes')

    logger.info('cleaning files....')
    testMgr.clean(context.resumesFolder)
    testMgr.clean(context.exportedHandler['folder'])
    testMgr.clean(context.failedHandler['folder'])
    testMgr.clean(context.duplicateHandler['folder'])

    logger.info('copy files...')
    testMgr.createExportsEnv(testResumesFolder, context.resumesFolder)



if __name__ == '__main__':
    build()

