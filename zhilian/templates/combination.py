#-*- coding: UTF-8 -*-

import common
from zhilian import util

logger = common.getLogger(__name__)


class Template(object):

    """template contains chinese and english content"""

    def __init__(self, soup):
        super(Template, self).__init__()
        self.soup = soup
        self.soup = soup
        self.userName = None
        self.birthday = None
        self.degree = None
        self.contacts = None
        self.education = None
        self.workexs = None

    def isSupport(self):
        head = self.soup.find('div', class_='zpResumeS')
        return (head is not None) and len(head) > 0

    def parse(self):
        self._setUserName()
        self._setBirthday()
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

    def _setUserName(self):
        div = self.soup.find('div', class_='name')
        self.userName = div.string

    def _setBirthday(self):
    	div = self.soup.find('div',class_='baseinfo')
    	strInfo = common.strip(div.get_text())

        ibirth = strInfo.find(u'月生')
        strBirth = common.strip(util.strGetUnitl(strInfo,ibirth,'|',True))
        self.birthday = strBirth

        logger.info(u"birth:{}".format(strBirth))

        self.contacts = {}
        imobile = strInfo.find(u'(手机)')-1
        strMobile = common.strip(util.strGetUnitl(strInfo,imobile,'\n',True))
        self.contacts['mobile'] = strMobile

        logger.info(u'mobile:{}'.format(strMobile))

        iemail = strInfo.find(u'E-mail:')
        iemail = iemail+len(u'E-mail:')
        strEmail = common.strip(util.strGetUnitl(strInfo,iemail,'|'))
        self.contacts['email'] = strEmail

        logger.info(u'email:{}'.format(strEmail))

    def _setEducation(self):
        span = self.soup.find('span',text=u'教育经历')

        if span is None:
            logger.warning('{} doesn\'t have any education information'.format(self.userName))
            return

        divInfo = span.parent.next_sibling.next_sibling
        strEdInfo = common.strip(divInfo.get_text())
        edInfos = strEdInfo.split('|')

        self.education={}

        self.education['speciality']=common.strip(edInfos[1])
        self.degree = common.strip(edInfos[2])
        logger.info(u'degree:{}'.format(self.degree))

        headInfo = edInfos[0].split(u'：')
        self.education['college'] = common.strip(headInfo[1])
        time = headInfo[0].split('--')
        self.education['graduatedTime'] = common.strip(time[1])

        logger.info(u'education:{}'.format(self.education))

    def _setWorkExperiences(self):
        span = self.soup.find('span',text=u'工作经历')

        if span is None:
            logger.warning('{} doesn\'t have any work experiences'.format(self.userName))
            return

        divInfo = span.parent.next_sibling.next_sibling
        rows = divInfo.find_all('tr')
        self.workexs = []

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
        

        



