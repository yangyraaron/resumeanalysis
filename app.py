#-*- coding: UTF-8 -*-

import os
from bs4 import BeautifulSoup
from zhilian import zlFilter
from job import jobFilter
import logging
import logging.config
import setting
import common
import fileMgr
import templateFactory
import constructor

# initialize log
logging.config.dictConfig(setting.logging)
logger = common.getLogger(setting.app['name'])


# initilize variables
dataFolder = setting.app['dataFolder']
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)

# register handlers
templateFactory.registerFilter(zlFilter)
templateFactory.registerFilter(jobFilter)

# exporting
resumes = fileMgr.getResumes('51')

for r in resumes:
    try:
        soup = BeautifulSoup(open(r))
    except Exception, e:
        logger.error('the {} file should be a valid html file'.format(r))
        break # if something exceptional then stop


    template = templateFactory.getTemplate(soup)

    if template is None:
        logger.warning('there is not any template could handle "{}"'.format(r))
        break # if something exceptional then stop

    logger.info('parsing resume {} ...'.format(r))
    data = constructor.construct(template)

    userName = data['userName']
    if userName is not None and userName!='':
        logger.info(u'save json to file {}.json...'.format(userName, userName))
        fileMgr.saveJson(data)
    else:
        logger.warning(u"the resume of {} can not be analized".format(userName))

    break

    
