#-*- coding: UTF-8 -*-

import util
import setting
import common

logger = common.getLogger(__name__)


class ResumeParser(object):

    """parse the resume html and output information"""

    def __init__(self):
        super(ResumeParser, self).__init__()

    def parse(self,soup):
        """parse the html file and generate json structure"""

        self.soup = soup
        
        if not self.isSupport():
            logger.warning('the file isn\'t supprt by zhilian parser')
        else:
            self._setUsername()
            self._setBirthday()
            self._setContacts()
            self._setEducation()
            self._setWorkExperiences()

            return self._parse()

    def isSupport(self):
        """indicate if the resume is from zhilian
           @return ture : false"""

        return self.soup.head.title.string == u'智联简历'

    def _setUsername(self):
        """set user name from resume"""

        logger.debug('parsing and setting user name')

        title = self.soup.find_all(
            "div", class_="resume-preview-main-title")[0]
        self.username = title.div.string

    def _setBirthday(self):
        """set birthday from resume"""

        logger.debug('parsing and setting birthday and degree')

        summary_top = self.soup.find_all("div", class_="summary-top")[0].span
        summary_top_contents = summary_top.string.split(u'\xa0\xa0\xa0\xa0')
        self.birthday = util.find_content_in_bracket(summary_top_contents[1])
        self.degree = summary_top_contents[3]

    def _setContacts(self):
        """set contacts json from resume"""

        logger.debug('parsing and setting contacts')

        summary_bottom = self.soup.find_all("div", class_="summary-bottom")[0]
        str_contacts = summary_bottom.get_text(u' ')
        self.contacts = util.parse_contact(str_contacts)

    def _setEducation(self):
        """set education array from resume"""

        logger.debug('parsing and setting education')

        ed_title = self.soup.find('h3', text=u'教育经历')
        # because a string:comma and new line between two elements
        # use 2 sibling to get the next element
        ed_container = ed_title.next_sibling.next_sibling
        str_ed = ed_container.contents[0]
        self.education = str_ed.split(u'\xa0\xa0')

    # get work experiences
    def _setWorkExperiences(self):
        """get work exprience array from resume"""

        workexs = []
        wkex_title = self.soup.find('h3', text=u'工作经历')
        wkex_heads = wkex_title.parent.find_all('h2')

        for hd in wkex_heads:
            workex = {}
            str_hd = hd.string.split(u'\xa0\xa0')
            workex['time'] = str_hd[0].strip().strip('\n')
            workex['company'] = str_hd[1].strip().strip('\n')

            po = hd.next_sibling.next_sibling
            pos = po.string.split(u'|')
            workex['position'] = pos[1].strip().strip('\n')

            workexs.append(workex)

        self.workexs = workexs

    def _parse(self):
        result = {}

        result['username'] = self.username.strip().strip('\n')
        result['birthday'] = self.birthday.strip().strip('\n')
        result['degree'] = self.degree.strip().strip('\n')
        result['contacts'] = {
            'mobile': self.contacts[u'手机'].strip().strip('\n'),
            'email': self.contacts['E-mail'].strip().strip('\n')}
        result[
            'education'] = {'graduatedTime': self.education[0].strip().strip('\n'),
                            'university': self.education[1].strip().strip('\n'),
                            'speciality': self.education[2].strip().strip('\n')}
        result['experiences'] = self.workexs

        return result
