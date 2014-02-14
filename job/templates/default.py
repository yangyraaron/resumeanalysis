#-*- coding: UTF-8 -*-


import common

logger = common.getLogger(__name__)


class Template(object):

    """template for parse 51job resume"""

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
        imgs = self.soup.find_all('img',alt=u'前程无忧')
        return imgs is not None and len(imgs)>0

    def parse(self):
        self._initialize()
        self._setBasicInfo()
        self._setSex()
        self._setEducation()
        self._setWorkExperiences()

    def getSource(self):
        return u'51Job'

    def getUserName(self):
        return self.userName

    def getSex(self):
        return self.sex

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
        title = self.soup.find(u'strong')
        self.headTable = title.parent.parent.parent.parent.parent
        self.infoTable = self.headTable.next_sibling.next_sibling

    def _setSex(self):
        title = self.headTable.find('b').get_text()
        contents = title.split('|')
        self.sex = common.strip(contents[1])

        logger.debug(u'sex:{}'.format(self.sex))

    def _setBasicInfo(self):
        strBasic = common.strip(self.headTable.get_text())
        strBasic = strBasic.replace('\n', '|')

        self.userName = common.strGetUnitl(strBasic, 0, '|')
        logger.debug(u'user name:{}'.format(self.userName))

        # basic info contains  birthday in 1st row
        ibirth = strBasic.find(u'日)')
        self.birthday = common.strGetUnitl(strBasic, ibirth + 1, '|', True)
        self.birthday = common.find_content_in_bracket(self.birthday)
        logger.debug(u'birthday:{}'.format(self.birthday))

        self._substractMobile(strBasic)
        self._substractEmail(strBasic)

        logger.debug(u"mobile:{}".format(self.contacts['mobile']))
        logger.debug(u"email:{}".format(self.contacts['email']))

    def _substractMobile(self, strSource):
        strIndex = u'（手机）'
        mobile = common.getStrByIndexUtil(strIndex, strSource, u'|', True)
        self.contacts['mobile'] = mobile

    def _substractEmail(self, strSource):
        strIndex = u'E-mail：'
        email = common.getStrByIndexUtil(strIndex, strSource, '')
        self.contacts['email'] = email.strip('|')

    def _setEducation(self):
        title = self.soup.find('td',text=u'教育经历')
        if title is None:
            return

        tdEdContainer = common.indexNextSibling(title.parent,3)
        #not default template
        if tdEdContainer is None:
            tdEdContainer = common.indexNextSibling(title.parent.parent.parent,1)
            row = tdEdContainer.find('tr')
        else:
            row = tdEdContainer.td.table.find('tr')
        
        strEd = common.strip(row.get_text('|'))

        strIndex = u'--'
        graduateTime = common.getStrByIndexUtil(strIndex,strEd,'|')
        self.education['graduateTime'] = graduateTime

        strEd = common.strip(self.infoTable.get_text())
        strEd = strEd.replace('\n', '|')

        strIndex = u'学　历：|'
        degree = common.getStrByIndexUtil(strIndex, strEd, '|')
        self.education['degree'] = degree.strip('|')

        strIndex = u'学　校：|'
        college = common.getStrByIndexUtil(strIndex, strEd, '|')
        self.education['college'] = college.strip('|')

        strIndex = u'专　业：|'
        speciality = common.getStrByIndexUtil(strIndex, strEd, '|')
        self.education['speciality'] = speciality.strip('|')

        logger.debug(u'graduateTime:{}'.format(self.education['graduateTime']))
        logger.debug(u'degree:{}'.format(self.education['degree']))
        logger.debug(u'college:{}'.format(self.education['college']))
        logger.debug(u'speciality:{}'.format(self.education['speciality']))

    def _setWorkExperiences(self):
        title = self.soup.find('td', text='工作经验')
        if title is None:
            logger.warning('the work experience section can not be found')
            return

        wkRow = common.indexNextSibling(title.parent, 3)

        # not default template
        if wkRow is None:
            wkRow = common.indexNextSibling(title.parent.parent.parent, 1)
            rows = wkRow.find_all('tr')
        else:
            rows = wkRow.td.table.find_all('tr')

        track = 0  # track a start of new work experience
        count = len(rows)
        strCompany = ''
        strPosition = ''
        workex = {}
        for x in xrange(0, count):
            if track == 0:
                strCompany = rows[x].get_text()
                workex['company'] = common.getStrByIndexUtil(
                    u'：', strCompany, [u'（', u'['])
                workex['time'] = common.getStrByIndexUtil(
                    u'：', strCompany, '', True)
            elif track == 2:
                strPosition = rows[x].get_text()
                workex['position'] = common.getStrByIndexUtil(
                    '\n', strPosition.strip(), '')
            elif rows[x].find('hr') is not None:
                track = 0
                self.workexs.append(workex)
                workex = {}
                continue

            track += 1

        if workex:
            self.workexs.append(workex)
