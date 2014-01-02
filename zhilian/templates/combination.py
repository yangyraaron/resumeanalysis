#-*- coding: UTF-8 -*-

import common

logger = common.getLogger(__name__)


class Template(object):

    """template contains chinese and english content"""

    def __init__(self, soup):
        super(Template, self).__init__()
        self.soup = soup

    def isSupport(self):
        head = self.soup.find('div', _class='zpResumeS')

        return (head is not None) and len(head) > 0

    def parse(self):
        pass


    def getUserName(self):
     	return self.username

    def getBirthday(self):
     	return self.birthday

    def getDegree(self):
     	return self.degree

    def getContacts(self):
     	return self.contacts

    def getEducations(self):
     	return self.educations

    def getWorkExpriences(self):
     	return self.workexs
