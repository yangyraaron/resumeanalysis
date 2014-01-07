#-*- coding: UTF-8 -*-

import common
from templates import default

logger = common.getLogger(__name__)

def isSupport(soup):
	imgs = soup.find_all(alt=u'前程无忧')

	return imgs is not None 

def getTemplate(soup):
	logger.debug('template is 51job default')

	return default.Template(soup)