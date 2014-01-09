#-*- coding: UTF-8 -*-

import os
import sys
import getopt
from bs4 import BeautifulSoup
from zhilian import zlFilter
from job import jobFilter
import logging
import logging.config
import setting
import common
from persistence import fileMgr
import templateFactory
import constructor
from persistence import mongodb

# initialize log
logging.config.dictConfig(setting.logging)
logger = common.getLogger(setting.app['name'])


class Application(object):

    """application class"""

    def __init__(self):
        super(Application, self).__init__()
        self.resumeMgr = None

        self._initialize()

    def _initialize(self):
        # initilize variables
        dataFolder = setting.app['dataFolder']
        if not os.path.exists(dataFolder):
            os.makedirs(dataFolder)

        # register handlers
        templateFactory.registerFilter(zlFilter)
        templateFactory.registerFilter(jobFilter)

    def _exportToFile(self, data):
        userName = data['userName']
        if userName is not None and userName != '':
            logger.info(u'save data to file {}.json...'.format(userName))
            fileMgr.saveJson(data)
        else:
            logger.warning(
                u"the resume of {} can not be analized".format(userName))

    def _getMongoInstance(self):
        if self.resumeMgr is None:
            self.resumeMgr = mongodb.ResumeMgr(
                setting.db['mongodb']['host'], setting.db['mongodb']['port'])

        return self.resumeMgr

    def _exportToDb(self, data):
        userName = data['userName']
        if userName is not None and userName != '':
            logger.info(u'save {} data to db...'.format(userName))

            resumeMgr = self._getMongoInstance()
            resumeMgr.addUser(data)
        else:
            logger.warning(
                u"the resume of {} can not be analized".format(userName))

    # get encodign from html file
    def _getEncoding(self, soup):
        meta = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        if meta is None:
            return None

        content = meta['content']
        charset = meta.get('charset')

        if charset is not None:
            return charset
        elif content is None:
            return None
        else:
            charset = common.strip(
                common.getStrByIndexUtil('charset=', content, ''))

        return charset

    def run(self, args):
        # exporting
        resumes = fileMgr.getResumes('51')
        for r in resumes:
            try:
                f = open(r)
                soup = BeautifulSoup(f)
                encoding = self._getEncoding(soup)

                logger.debug('encoding of file {} is {}'.format(r, encoding))

                if encoding is not None:
                    logger.debug('recreate a new soup with new encoding')
                    # reset the position to start
                    f.seek(0)
                    soup = BeautifulSoup(f, from_encoding=encoding)

            except IOError as ioe:
                logger.error('open file faild!')
                logger.error("detail:{}".format(str(ioe)))
            except Exception as e:
                logger.error(
                    'the {} file should be a valid html file'.format(r))
                logger.error('detail:{}'.format(str(e)))
                break  # if something exceptional then stop
            finally:
                f.close()

            template = templateFactory.getTemplate(soup)

            if template is None:
                logger.warning(
                    'there is not any template could handle "{}"'.format(r))
                break  # if something exceptional then stop

            logger.info('parsing resume {} ...'.format(r))
            data = constructor.construct(template)

            if args > 0:
                dummy = args.get('dummy')
                if dummy is not None and dummy == 'file':
                    self._exportToFile(data)  # export to file
                else:
                    self._exportToDb(data)  # add to database

            #break


def main():
    cmdArgs = {}

    # parse the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:', ["dummy="])
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)

    for opt, arg in opts:
        # get the dummy argument
        if opt in ('-d', '--dummy'):
            cmdArgs['dummy'] = arg
        else:
            assert False, "unhandled option"

    app = Application()
    app.run(cmdArgs)


if __name__ == '__main__':
    main()
