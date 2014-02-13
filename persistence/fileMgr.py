#-*- coding: UTF-8 -*-


import os
import setting
import json
import common
import shutil
import context

logger = common.getLogger()


def saveJson(dic):
    logger.debug(u'save json to file {}'.format(dic['userName']))

    filePath = u'{}/{}.json'.format(context.dataFolder, dic['userName'])

    with open(filePath, 'w') as f:
        _dumpJson(f, dic)


def _dumpJson(fd, dic):
    # json.dump(dic,fd,ensure_ascii=False).encoding('UTF-8')
    strData = json.dumps(dic, ensure_ascii=False).encode('UTF-8')
    fd.write(strData)


def getResumes(source):
    resumes = []

    if source is None or source.strip() == '':
        logger.error('the resume folder is not provideed')

    try:
        for fd in os.listdir(source):
            resumes.append(u'{}/{}'.format(source, fd))
    except IOError as e:
        logger.error(
            u'open the resume folder {} error'.format(source), exc_info=True)

    return resumes


def moveFile(fd, destDir):
    try:
        shutil.copy(fd, destDir)
        os.remove(fd)
    except Exception as e:
        logger.error(
            u'move file {} to {} failed'.format(fd, destDir), exc_info=True)


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
        logger.error(
            'make directory {} failed!'.format(dirPath), exc_info=True)
