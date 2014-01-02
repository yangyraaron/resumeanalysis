#-*- coding: UTF-8 -*-


import common
from zhilian import util

logger = common.getLogger(__name__)


class Template(object):

    """zhilian default template"""

    def __init__(self, soup):
        super(Template, self).__init__()
        self.soup = soup

    def isSupport(self):
        head = self.soup.find('div', class_='resume-preview-head')

        return (head is not None) and len(head) > 0

    def parse(self):
        self._setUsername()
        self._setBirthday()
        self._setContacts()
        self._setEducation()
        self._setWorkExperiences()

        # return self._merge()

    def getUserName(self):
        return self.username

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

    def _setUsername(self):
        """set user name from resume"""

        logger.debug('parsing and setting user name')

        self.username = None

        title = self.soup.find_all(
            "div", class_="resume-preview-main-title")[0]
        self.username = common.strip(title.div.string)

    # html content format: sex | birthday | years been work | education |  marriage
    # eg: 				   女    24岁(1989年8月)    2年工作经验    本科    未婚
    def _setBirthday(self):
        """set birthday from resume"""

        logger.debug('parsing and setting birthday and degree')

        self.birthday = None

        summary_top = self.soup.find_all(
            "div", class_="summary-top")[0].span
        summary_top_contents = summary_top.string.split(
            u'\xa0\xa0\xa0\xa0')
        self.birthday = common.strip(util.find_content_in_bracket(
            summary_top_contents[1]))
        # self.degree = summary_top_contents[3]

    def _setContacts(self):
        """set contacts json from resume"""

        logger.debug('parsing and setting contacts')

        self.contacts = None

        summary_bottom = self.soup.find_all("div", class_="summary-bottom")[0]
        str_contacts = summary_bottom.get_text(u' ')
        contacts = util.parse_contact(str_contacts)

        self.contacts={}
        pairs = contacts.items()

        for pair in pairs:
        	self.contacts[common.strip(pair[0])] = common.strip(pair[1])


    def _setEducation(self):
        """set education array from resume"""

        logger.debug('parsing and setting education')
        self.education = {}
        self.degree = None

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

        self.degree = common.strip(arrEd[3])

    # get work experiences
    def _setWorkExperiences(self):
        """get work exprience array from resume"""

        workexs = []
        self.workexs = workexs

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

            workexs.append(workex)

            self.workexs = workexs
