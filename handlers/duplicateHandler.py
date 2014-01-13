#-*- coding: UTF-8 -*-

#-*- coding: UTF-8 -*-


import setting
from datetime import datetime
import common
from persistence import fileMgr
from string import Template

logger = common.getLogger(__name__)

cfgFailedHandler = setting.app['handlers']['duplicate']
rootFolder = cfgFailedHandler['folder']
extension = cfgFailedHandler['extension']
template = Template(cfgFailedHandler['template'])

fileMgr.verifyExists(rootFolder)


class Handler(object):

    """the handler for moving parsing failed file into failed folder and log failed record"""

    def __init__(self):
        super(Handler, self).__init__()
        self.fName = ''
        self.fd = None

    def _verify(self,):
        if self.fd is None or self.fd.closed:
            strTime = common.strDefaultNow()

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

    def handle(self, duplicateFile):
        if duplicateFile is None:
            logger.error(
                'doesn\'t provide failed source file,can not handle failed exporting')
        elif template is None:
            logger.error('template is none', exc_info=True)
        else:
            if self._verify():
                dicContent = {
                    'time': common.strDefaultNow(), 'file': u'{}'.format(duplicateFile)}
                strMsg = template.substitute(dicContent)

                try:
                    self.fd.write(strMsg.encode('UTF-8'))
                    self.fd.write('\n')
                    self.fd.flush()
                except (IOError, Exception) as e:
                    logger.error(
                        u'write msg to file {} failed'.format(self.fName), exc_info=True)

                logger.info(
                    u'make a dupliate record for {}'.format(duplicateFile))

    def close(self):
        if self.fd is None or self.fd.closed:
            logger.info('the duplidate handler closed!')
            return

        try:
            self.fd.close()
            logger.info(u'the file {} is closed'.format(self.fName))
        except (IOError, Exception) as e:
            logger.error(
                u'try to close file {} faild'.format(self.fName), exc_info=True)
