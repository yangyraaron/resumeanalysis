#-*- coding: UTF-8 -*-

import common
from templates import default

logger = common.getLogger(__name__)

def isSupport(soup):
	imgs = soup.find(alt='前程无忧')
	
	return imgs is not None 

def getTemplate(soup):
	return default.Template(soup)