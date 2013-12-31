#-*- coding: UTF-8 -*-

import os
from bs4 import BeautifulSoup
from zhilian import parser
import logging
import logging.config
import setting

## initialization ##
logging.config.dictConfig(setting.logging)
logger = logging.getLogger('resumeAnalyser')

def print_data(dicObj):
	print(u'username : {}'.format(dicObj['username']))
	print(u'birthday : {}'.format(dicObj['birthday']))
	print(u'degree : {}'.format(dicObj['degree']))

	print('contacts : ')
	contacts = dicObj['contacts']
	c_keys = contacts.viewkeys()
	for ck in c_keys:
		print(u'{} : {}'.format(ck,contacts[ck]))

	print('education : ')
	ed = dicObj['education']
	ed_keys = ed.viewkeys()
	for ed_key in ed_keys:
		print(u'{} : {}'.format(ed_key,ed[ed_key]))

	print('experiences : ')
	exs = dicObj['experiences']
	for ex in exs:
		print('-------------------')
		ex_keys = ex.viewkeys()
		for ex_key in ex_keys:
			print(u'{} : {}'.format(ex_key,ex[ex_key]))


cur_dir = os.path.dirname(os.path.abspath(__file__))

filename = cur_dir + ur'/files/智联招聘_许建梅_java开发工程.html'
soup = BeautifulSoup(open(filename))
parser = parser.ResumeParser(soup)

logger.info('parsing resume...')
json = parser.parse()

print_data(json)

	

