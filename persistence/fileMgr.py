#-*- coding: UTF-8 -*-


import os
import setting
import json
import common
import os
import shutil

logger = common.getLogger()


def saveJson(dic):
    logger.debug(u'save json to file {}'.format(dic['userName']))

    filePath = u'{}/{}.json'.format(setting.app['dataFolder'], dic['userName'])

    with open(filePath, 'w') as f:
        _dumpJson(f, dic)


def _dumpJson(fd, dic):
    # json.dump(dic,fd,ensure_ascii=False).encoding('UTF-8')
    strData = json.dumps(dic, ensure_ascii=False).encode('UTF-8')
    fd.write(strData)


def getResumes(source='zhilian/default'):
    resumes = []

    if source is not None or source.strip() != '':
        directory = setting.app['resumesFolder'] + '/' + source
    try:
        for fd in os.listdir(directory):
            resumes.append(u'{}/{}'.format(directory, unicode(fd,'utf-8')))
    except IOError as e:
        logger.error(
            u'open the resume folder {} error'.format(directory), exc_info=True)

    return resumes


def moveFile(fd, destDir):
	try:
		shutil.move(fd, destDir)
	except Exception as e:
		logger.error(u'move file {} to {} failed'.foramt(fd, destDir), exc_info=True)


# def moveToExported(fd):
#     moveFile(fd, setting.app['exportedFolder'])
#     logger.info(u'file {} has been moved to  exported folder'.format(fd))


# def moveToFailed(fd):
#     moveFile(fd, setting.app['failedFolder'])
#     logger.info(u'file {} has been moved to failed folder'.format(fd))


def verifyExists(dirPath):
    try:
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
    except Exception as e:
		logger.error('make directory {} failed!'.format(dirPath),exc_info=True)
