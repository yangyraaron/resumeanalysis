#-*- coding: UTF-8 -*-


import logging
import setting

ESC_CHARS=[' ','\n','\t','\r']

def getLogger(name=''):
	if name.strip()=='':
		return logging.getLogger(setting.app['name'])

	return logging.getLogger(setting.app['name']+'.'+name)

def strIfNoneOrEmpty(value,defalutValue=''):
	if value is None or (value==''):
		return defalutValue
	return value

def listIfNoneOrEmpty(list,defalutValue=[]):
	if list is None or len(list)==0:
		return defalutValue
	return list

def dicIfNone(dic,defalutValue={}):
	if dic is None:
		return defalutValue
	return dic

def strip(strValue):
	#return str.strip().strip('\r').strip('\n').strip('\t')
	for c in ESC_CHARS:
		strValue = strValue.strip(c)

	return strValue
