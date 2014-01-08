#-*- coding: UTF-8 -*-

import common
from zhilian import util

logger = common.getLogger(__name__)


class Template(object):

    """template contains chinese and english content"""

    def __init__(self, soup):
        super(Template, self).__init__()
        self.soup = soup
        self.userName = ''
        self.sex = ''
        self.birthday = ''
        self.contacts = {}
        self.education = {}
        self.workexs = []

    def isSupport(self):
        head = self.soup.find('div', class_='zpResumeS')
        return head is not None

    def parse(self):
        self._setUserName()
        self._setBasic()
        self._setEducation()
        self._setWorkExperiences()

    def getSource(self):
        return u'智联'

    def getUserName(self):
        return self.userName

    def getSex(self):
        return self.sex

    def getBirthday(self):
        return self.birthday

    def getContacts(self):
        return self.contacts

    def getEducations(self):
        return self.education

    def getWorkExpriences(self):
        return self.workexs

    def _setUserName(self):
        div = self.soup.find('div', class_='name')
        self.userName = div.string

    def _setBasic(self):
    	div = self.soup.find('div',class_='baseinfo')
    	strInfo = common.strip(div.get_text())

        self.sex = strInfo[0]
        logger.debug(u'sex:{}'.format(self.sex))

        strBirth = common.getStrByIndexUtil(u'月生',strInfo,'|',True)
        self.birthday = strBirth

        logger.debug(u"birth:{}".format(strBirth))

        strMobile = common.getStrByIndexUtil(u'(手机)',strInfo,'\n',True)
        self.contacts['mobile'] = strMobile

        logger.debug(u'mobile:{}'.format(strMobile))

        iemail = strInfo.find(u'E-mail:')
        iemail = iemail+len(u'E-mail:')
        strEmail = common.getStrByIndexUtil(u'E-mail:',strInfo,'|')
        self.contacts['email'] = strEmail

        logger.debug(u'email:{}'.format(strEmail))

    def _setEducation(self):
        span = self.soup.find('span',text=u'教育经历')

        if span is None:
            logger.warning('{} doesn\'t have any education information'.format(self.userName))
            return

        divInfo = span.parent.next_sibling.next_sibling
        strEdInfo = common.strip(divInfo.get_text())
        edInfos = strEdInfo.split('|')

        self.education['speciality']=common.strip(edInfos[1])
        self.education['degree'] = common.strip(edInfos[2])
        logger.debug(u'degree:{}'.format(self.education['degree']))

        headInfo = edInfos[0].split(u'：')
        self.education['college'] = common.strip(headInfo[1])
        time = headInfo[0].split('--')
        self.education['graduatedTime'] = common.strip(time[1])

        logger.debug(u'education:{}'.format(self.education))

    def _setWorkExperiences(self):
        span = self.soup.find('span',text=u'工作经历')

        if span is None:
            logger.warning('{} doesn\'t have any work experiences'.format(self.userName))
            return

        divInfo = span.parent.next_sibling.next_sibling
        rows = divInfo.find_all('tr')

        for row in rows:
            workex = self._createWorkEx(row)
            if workex is not None:
                self.workexs.append(workex)
        
    def _createWorkEx(self,row):
        workex={}

        strTime = common.strip(row.contents[0].get_text())
        #escape empty row
        if strTime=='':
            return None

        workex['time'] = strTime.rstrip(u'：')

        strhead = row.contents[1].contents[0]
        heads = strhead.split('|')
        workex['company'] = common.strip(heads[0])
        workex['position'] = common.strip(heads[1])

        return workex
        

        



