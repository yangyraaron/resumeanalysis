#-*- coding: UTF-8 -*-


import os
import setting
from datetime import datetime
import common
from persistence import fileMgr
from string import Template

logger = common.getLogger(__name__)

cfgFailedHandler = setting.app['handlers']['failed']
rootFolder = cfgFailedHandler['folder']
extension = cfgFailedHandler['extension']
template = Template(cfgFailedHandler['template'])

fileMgr.verifyExists(rootFolder)


def removeFile(fileName):
    try:
        for d in os.listdir(rootFolder):
            if os.path.isdir(d):
                for fd in os.listdir(d):
                    if os.path.isfile(fd):
                        pair = os.path.split(fd)
                        if pair[1] == fileName:
                            os.remove(fd)
                            logger.info(
                                u'the failed file {} has been removed'.format(fd))
                            break

    except Exception as e:
        logger.error(
            u'remove file from failed folder failed', exc_info=True)


class Handler(object):

    """the handler for moving parsing failed file into failed folder and log failed record"""

    def __init__(self):
        super(Handler, self).__init__()
        self.folder = ''
        self.fName = ''
        self.fd = None

    def _verify(self):
        if self.sourceFile is None:
            logger.error(
                'doesn\'t provide failed source file,can not handle failed exporting')
            return False

        if self.fd is None or self.fd.closed:
            strTime = common.strDefaultNow()
            # create the failure folder and move the sourcefile into this
            # folder
            self.folder = u'{}/{}'.format(rootFolder, strTime)
            fileMgr.verifyExists(self.folder)

            # create the log file to record
            self.fName = u'{}/{}.{}'.format(rootFolder, strTime, extension)
            try:
                self.fd = open(self.fName, 'a')
                logger.info(u'the file {} is opened'.format(self.fName))
            except (IOError, Exception) as e:
                logger.error(
                    u'open file {} to log is failed'.format(self.fName), exc_info=True)
                return False

            return True
        else:
            return True

    def open(self):
        if self._verify():
            return True
        return False

    def handle(self, failedFile):
        if failedFile is None:
            logger.error(
                'doesn\'t provide failed source file,can not handle failed exporting')            
        elif template is None:
            logger.error('template is none', exc_info=True)
        else:
            if self._verify():
                dicContent = {
                    'time': common.strDefaultNow(), 'file': u'{}'.format(failedFile)}
                strMsg = template.substitute(dicContent)
                # move source file to failed relavant folder
                fileMgr.moveFile(failedFile, self.folder)
                logger.info(
                    u'the file {} has been moved into {} folder'.format(failedFile, self.folder))
                # log the failed log
                try:
                    self.fd.write(strMsg)
                    self.fd.write('\n')
                    self.fd.flush()
                except (IOError, Exception) as e:
                    logger.error(
                        u'write msg to file {} failed'.format(self.fName), exc_info=True)

    def close(self):
        if self.fd is None or self.fd.closed:
            logger.info('the failed handler closed')
            return

        try:
            self.fd.close()
            logger.info(u'the file {} is closed'.format(self.fName))
        except (IOError, Exception) as e:
            logger.error(
                u'try to close file {} faild'.format(self.fName), exc_info=True)
