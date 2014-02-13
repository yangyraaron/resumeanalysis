#-*- coding: UTF-8 -*-

import common

logger = common.getLogger(__name__)


class Template(object):

    """Template for exported 51 resume"""

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
        table = self.soup.find(id='divResume')

        if table is None:
            logger.info('divResume table can not be found')
            return False

        return True

    def parse(self):
        self._initialize()
        self._setBasicInfo()
        self._setEducationInfo()
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
        if self.isSupport():
            span = self.soup.find(id='spanProcessStatusHead')

            self._infoTable = span.parent.parent.parent
            self._educationTable = self._infoTable.next_sibling

    def _setBasicInfo(self):
        strBasic = self._infoTable.get_text()

        self.userName = common.getStrByIndexUtil(u'流程状态：',strBasic,' ')
        logger.debug(u'name:{}'.format(self.userName))

        self.sex = common.getStrByIndexUtil(u'|',strBasic,'|')
        logger.debug(u'sex:{}'.format(self.sex))

        ibirth = strBasic.find(u'日）')
        self.birthday = common.strGetUnitl(strBasic, ibirth, u'（', True)
        logger.debug(u'birthday:{}'.format(self.birthday))

        mobile = common.getStrByIndexUtil(u'（手机）', strBasic, u'：', True)
        self.contacts['mobile'] = mobile
        logger.debug(u'mobile:{}'.format(self.contacts['mobile']))

        email = common.getStrByIndexUtil(u'E-mail：', strBasic, '')
        self.contacts['email'] = email.strip('\n')
        logger.debug(u'email:{}'.format(self.contacts['email']))

    def _setEducationInfo(self):
        title = self.soup.find('td',text=u'教育经历')
        if title is None:
            logger.warning('can not find education section')
            return

        tdEdContainer = title.parent.next_sibling.next_sibling.next_sibling
        row = tdEdContainer.td.table.find('tr')
        strEd = common.strip(row.get_text('|'))

        strIndex = u'--'
        graduateTime = common.getStrByIndexUtil(strIndex,strEd,'|')
        self.education['graduateTime'] = graduateTime

        strEd = self._educationTable.get_text('|')
        
        degree = common.getStrByIndexUtil(u'学　历：|',strEd,'|')
        self.education['degree'] = degree.strip('|')
        college = common.getStrByIndexUtil(u'学　校：|',strEd,'|')
        self.education['college'] = college.strip('|')
        speciality = common.getStrByIndexUtil(u'专　业：|',strEd,'|')
        self.education['speciality'] = speciality.strip('|')

        logger.debug(u'graduateTime:{}'.format(self.education['graduateTime']))
        logger.debug(u'degree:{}'.format(self.education['degree']))
        logger.debug(u'college:{}'.format(self.education['college']))
        logger.debug(u'speciality:{}'.format(self.education['speciality']))

    def _setWorkExperiences(self):
        title = self.soup.find('td', text='工作经验')

        if title is None:
            logger.warning('work experience section can not be found')
            return

        wkRow = title.parent.next_sibling.next_sibling.next_sibling#common.indexNextSibling(title.parent, 3)

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
                    u'：', strCompany, [u'(',u'（', u'['])
                workex['time'] = common.getStrByIndexUtil(
                    u'：', strCompany, '', True)
            elif track == 2:
                strPosition = rows[x].get_text('|')
                workex['position'] = common.getStrByIndexUtil(
                    '|', strPosition.strip(), '')
            elif rows[x].find('hr') is not None:
                track = 0
                self.workexs.append(workex)
                workex = {}
                continue

            track += 1

        if workex:
            self.workexs.append(workex)


    

