#-*- coding: UTF-8 -*-


import common

logger = common.getLogger(__name__)

class Template(object):
	"""template for parse 51job resume"""
	def __init__(self, soup):
		super(Template, self).__init__()
		self.soup = soup
		self.userName=None
		self.birthday=None
		self.degree = None
		self.contacts={}
		self.education = {}
		self.workexs = None

	def isSupport(self):
	    return True

	def parse(self):
		self._initialize()
		self._setBasicInfo()
		self._setEducation()
		self._setWorkExperiences()

	def getUserName(self):
	    return self.userName

	def getBirthday(self):
	    return self.birthday

	def getDegree(self):
	    return self.degree

	def getContacts(self):
	    return self.contacts

	def getEducations(self):
	    return self.education

	def getWorkExpriences(self):
	    return self.workexs

	def _initialize(self):
		table = self.soup.body.contents[4]

		contentTable = table.tbody.tr.td.contents[3]
		# head table contains user name contacts birthday
		self.headTable = contentTable.tbody.tr.td.table
		# info table contains education 
		self.infoTable = self.headTable.next_sibling.next_sibling

	def _setBasicInfo(self):
		rows = self.headTable.find_all('tr')
		spans = rows[0].find_all('span')
		strong = spans[1].find('strong')
		#refactor
		strBasic = common.strip(self.headTable.get_text())
		strBasic = strBasic.replace('\n','#')
		print(strBasic)

		self.userName = strong.string
		logger.debug(u'user name:{}'.format(self.userName))

		infoRows = rows[1].find_all('tr')
		# basic info contains  birthday in 1st row
		basicInfo = common.strip(infoRows[0].td.get_text())
		ibirth = basicInfo.find(u'日)')
		self.birthday = common.strGetUnitl(basicInfo,ibirth+1,'|',True)
		self.birthday = common.find_content_in_bracket(self.birthday)
		logger.debug(u'birthday:{}'.format(self.birthday))

		#contact
		for x in xrange(1,len(infoRows)):
			row = infoRows[x]
			info = common.strip(row.get_text())
			self._substractMobile(info)
			self._substractEmail(info)

		logger.debug(u"mobile:{}".format(self.contacts['mobile']))
		logger.debug(u"email:{}".format(self.contacts['email']))
	
	def _substractMobile(self,strSource):
		strIndex = u'（手机）'
		self.contacts['mobile'] = common.getStrByIndexUtil(strIndex,strSource,u'：',True)

	def _substractEmail(self,strSource):
		strIndex = u'E-mail：'
		self.contacts['email'] = common.getStrByIndexUtil(strIndex,strSource,'')

	def _setEducation(self):
		strEd = common.strip(self.infoTable.get_text())
		strEd = strEd.replace('\n','|')

		strIndex = u'学　历：|'
		self.education['degree'] = common.getStrByIndexUtil(strIndex,strEd,'|')

		strIndex = u'学　校：|'
		self.education['college'] = common.getStrByIndexUtil(strIndex,strEd,'|')

		strIndex = u'专　业：|'
		self.education['speciality'] = common.getStrByIndexUtil(strIndex,strEd,'|')


		logger.debug(u'degree:{}'.format(self.education['degree']))
		logger.debug(u'college:{}'.format(self.education['college']))
		logger.debug(u'speciality:{}'.format(self.education['speciality']))

	def _getStrByIndex(self,strIndex,strSource,strTer,isReverse=False):
		index = strSource.find(strIndex)
		if index!=-1:
			if isReverse:
				index -= 1
			else:
				index += len(strIndex)
			strValue = common.strGetUnitl(strSource,index,strTer,isReverse)
			return common.strip(strValue)

		return ''


