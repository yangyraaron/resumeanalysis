#-*- coding: UTF-8 -*-


import setting
import os

rootPath = os.path.split(os.path.realpath(__file__))[0]

appName = setting.app.get('name')

dataFolder = setting.app.get('dataFolder')
if dataFolder is not None:
	dataFolder = u'{}/{}'.format(rootPath, dataFolder)

resumesFolder = setting.app.get('resumesFolder')
if setting.app.get('resumesFolder'):
	resumesFolder = u'{}/{}'.format(rootPath, setting.app['resumesFolder'])

exportedHandler = None
failedHandler = None
duplicateHandler = None
_handlers = setting.app.get('handlers')

if _handlers is not None:
	handler = _handlers.get('exported')
	if handler is not None:
		exportedHandler = {'folder':u'{}/{}'.format(rootPath,handler.get('folder'))}

	handler = _handlers.get('failed')
	if handler is not None:
		failedHandler = {'folder':u'{}/{}'.format(rootPath,handler.get('folder')),
			'extension':handler.get('extension'),'template':handler.get('template')}

	handler = _handlers.get('duplicate')	
	if handler is not None:
		duplicateHandler = {'folder':u'{}/{}'.format(rootPath,handler.get('folder')),
			'extension':handler.get('extension'),'template':handler.get('template')}

logging = setting.logging

handler = logging['handlers']['info_file_handler']
handler['filename'] = u'{}/{}'.format(rootPath,handler['filename'])

handler = logging['handlers']['error_file_handler']
handler['filename'] = u'{}/{}'.format(rootPath,handler['filename'])

mongodb = setting.db.get('mongodb')
