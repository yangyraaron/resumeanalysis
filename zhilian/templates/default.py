#-*- coding: UTF-8 -*-


import common
from zhilian import util

logger = common.getLogger(__name__)


class Template(object):

    """zhilian default template"""

    def __init__(self, soup):
        super(Template, self).__init__()
        self.soup = soup
        self.userName=''
        self.sex=''
        self.birthday=''
        self.contacts={}
        self.education = {}
        self.workexs = []

    def isSupport(self):
        head = self.soup.find('div', class_='resume-preview-head')

        return head is not None

    def parse(self):
        self._setUserName()
        self._setBirthday()
        self._setContacts()
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
        """set user name from resume"""

        logger.debug('parsing and setting user name')

        title = self.soup.find_all(
            "div", class_="resume-preview-main-title")[0]
        self.userName = common.strip(title.div.string)

        logger.debug(u'username:{}'.format(self.userName))

    # html content format: sex | birthday | years been work | education |  marriage
    # eg: 				   女    24岁(1989年8月)    2年工作经验    本科    未婚
    def _setBirthday(self):
        """set birthday from resume"""

        logger.debug('parsing and setting birthday and degree')

        strSummaryTop = common.strip(self.soup.find_all(
            "div", class_="summary-top")[0].span.get_text());

        self.sex = strSummaryTop[0];
        self.birthday = common.getStrByIndexUtil(u'(',strSummaryTop,')')

        logger.debug(u'birthday:{}'.format(self.birthday))
        logger.debug(u'sex:{}'.format(self.sex))


    def _setContacts(self):
        """set contacts json from resume"""

        logger.debug('parsing and setting contacts')

        summaryBottom = self.soup.find_all("div", class_="summary-bottom")[0]
        strContacts = summaryBottom.get_text(u'|')
        strMobile = common.getStrByIndexUtil(u'手机：',strContacts,'|')
        strEmail = common.getStrByIndexUtil(u'E-mail：|',strContacts,'|')

        self.contacts['mobile'] = strMobile
        self.contacts['email'] = strEmail

        logger.debug(u'mobile:{}'.format(strMobile))
        logger.debug(u'email:{}'.format(strEmail))


    def _setEducation(self):
        """set education array from resume"""

        logger.debug('parsing and setting education')

        ed_title = self.soup.find('h3', text=u'教育经历')
        # doesn't have any educations
        if ed_title is None:
            return

        # because a string:comma and new line between two elements
        # use 2 sibling to get the next element
        ed_container = ed_title.next_sibling.next_sibling

        str_ed = ed_container.contents[0]
        arrEd= str_ed.split(u'\xa0\xa0')

        seg = arrEd[0].split('-')
        self.education['graduateTime'] = common.strip(seg[1])
        self.education['college'] = common.strip(arrEd[1])
        self.education['sepcialty'] = common.strip(arrEd[2])

        self.education['degree'] = common.strip(arrEd[3])

    # get work experiences
    def _setWorkExperiences(self):
        """get work exprience array from resume"""

        wkex_title = self.soup.find('h3', text=u'工作经历')
        # if does't have any work expriences
        if wkex_title is None:
            return

        wkex_heads = wkex_title.parent.find_all('h2')

        for hd in wkex_heads:
            workex = {}
            str_hd = hd.string.split(u'\xa0\xa0')
            workex['time'] = common.strip(str_hd[0])
            workex['company'] = common.strip(str_hd[1])

            po = hd.next_sibling.next_sibling
            pos = po.string.split(u'|')

            if len(pos) == 1:
                workex['position'] = common.strip(pos[0])
            else:
                workex['position'] = common.strip(pos[1])

            self.workexs.append(workex)
