#-*- coding: UTF-8 -*-

import os
from bs4 import BeautifulSoup
from zhilian import parser
import logging
import logging.config
import setting
import common
import fileMgr

# initialize log
logging.config.dictConfig(setting.logging)
logger = common.getLogger(setting.app['name'])

# print josn data
def print_data(dicObj):
    print(u'username : {}'.format(dicObj['username']))
    print(u'birthday : {}'.format(dicObj['birthday']))
    print(u'degree : {}'.format(dicObj['degree']))

    print('contacts : ')
    contacts = dicObj['contacts']
    c_keys = contacts.viewkeys()
    for ck in c_keys:
        print(u'{} : {}'.format(ck, contacts[ck]))

    print('education : ')
    ed = dicObj['education']
    ed_keys = ed.viewkeys()
    for ed_key in ed_keys:
        print(u'{} : {}'.format(ed_key, ed[ed_key]))

    print('experiences : ')
    exs = dicObj['experiences']
    for ex in exs:
        print('-------------------')
        ex_keys = ex.viewkeys()
        for ex_key in ex_keys:
            print(u'{} : {}'.format(ex_key, ex[ex_key]))

#initilize variables
dataFolder = setting.app['dataFolder']
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)


resumes = fileMgr.getResumes()

for r in resumes:
	soup = BeautifulSoup(open(r))
	parser = parser.ResumeParser()

	logger.info('parsing resume {} ...'.format(r))

	data = parser.parse(soup)

	logger.info('save data')

	fileMgr.saveJson(data)
	

