#-*- coding: UTF-8 -*-


import logging
import setting

def getLogger(name=''):
	if name.strip()=='':
		return logging.getLogger(setting.app['name'])

	return logging.getLogger(setting.app['name']+'.'+name)
