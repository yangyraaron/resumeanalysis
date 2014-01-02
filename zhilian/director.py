#-*- coding: UTF-8 -*-

import common
from templates import default
from templates import combination

logger = common.getLogger(__name__)


class ResumeParser(object):

    """parse the resume html and output information"""

    def __init__(self):
        super(ResumeParser, self).__init__()

    def export(self,soup):
        """parse the html file and generate json structure"""

        self.soup = soup

        if not self.isSupport():
            logger.warning('the file isn\'t support by zhilian parser')
            return None
        else:
            template = self._selectTemplate()

            if template is not None:
                template.parse()
                return self.construct(template)

            return None

    def construct(self,template):
        result = {}

        username = template.getUserName()
        result['userName'] = common.strIfNoneOrEmpty(username)
        birthday = template.getBirthday()
        result['birthday'] = common.strIfNoneOrEmpty(birthday)
        degree = template.getDegree()
        result['degree'] = common.strIfNoneOrEmpty(degree)
        contacts = template.getContacts()
        result['contacts'] = common.dicIfNone(contacts)
        education = template.getEducations()
        result['education'] = common.dicIfNone(education)
        expriences = template.getWorkExpriences()
        result['experiences'] = common.listIfNoneOrEmpty(expriences)

        return result


    def isSupport(self):
        """indicate if the resume is from zhilian
           @return ture : false"""

        return self.soup.head.title.string.find(u'智联') !=-1

    def _selectTemplate(self):
        template = default.Template(self.soup)

        if template.isSupport():
            return template

        template = combination.Template(self.soup)

        if template.isSupport():
            return template


        logger.warning('there isn\'t any templates could parse the resume correctly')
        return None
