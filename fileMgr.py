#-*- coding: UTF-8 -*-


import os
import setting
import json
import common
import os

logger = common.getLogger()

def saveJson(dic):
	logger.debug(u'save json to file {}'.format(file))

	filePath = u'{}/{}.json'.format(setting.app['dataFolder'], dic['userName'])

	# if not os.path.exists(filePath):
	# 	with open(filePath,'x') as f:
	# 		_dumpJson(f,dic)
	# else:
	with open(filePath,'w') as f:
		_dumpJson(f,dic)

def _dumpJson(fd,dic):
	#json.dump(dic,fd,ensure_ascii=False).encoding('UTF-8')
	strData = json.dumps(dic,ensure_ascii=False).encode('UTF-8')
	fd.write(strData)

def getResumes(source='zhilian/default'):
	resumes=[]
	directory = setting.app['resumesFolder']+'/'+source
	for fd in os.listdir(directory):
		resumes.append('{}/{}'.format(directory,fd))

	return resumes
