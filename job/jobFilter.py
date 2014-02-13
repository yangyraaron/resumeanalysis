#-*- coding: UTF-8 -*-

import common
from templates import default
from templates import exported

logger = common.getLogger(__name__)

def getTemplate(soup):
	template = default.Template(soup)
	if template.isSupport():
		return template
	else:
		template = exported.Template(soup)
		if template.isSupport():
			return template
		else:
			return None

def isSupport(soup):
	if getTemplate(soup) is None:
		return False
	return True
		
	
		