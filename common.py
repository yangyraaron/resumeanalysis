#-*- coding: UTF-8 -*-


import logging
import setting

def getLogger(name=''):
	if name.strip()=='':
		return logging.getLogger(setting.app['name'])

	return logging.getLogger(setting.app['name']+'.'+name)

def strIfNoneOrEmpty(value,defalutValue=''):
	if value is None or (value==''):
		return defalutValue
	return value

def listIfNoneOrEmpty(list,defalutValue=[]):
	if len(list)==0 or list is None:
		return defalutValue
	return list

def dicIfNone(dic,defalutValue={}):
	if dic is None:
		return defalutValue
	return dic

def strip(str):
	return str.strip().strip('\r\n').strip('\t')
