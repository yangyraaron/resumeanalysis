#-*- coding: UTF-8 -*-


import common

logger = common.getLogger(__name__)


def construct(template):
    result = {}

    try:
        template.parse()
    except Exception, e:
        logger.error("some thing wrong when parsing html file")
    else:
        userName = template.getUserName()
        result['userName'] = common.strIfNoneOrEmpty(userName)
        birthday = template.getBirthday()
        result['birthday'] = common.strIfNoneOrEmpty(birthday)
        contacts = template.getContacts()
        result['contacts'] = common.dicIfNone(contacts)
        education = template.getEducations()
        result['education'] = common.dicIfNone(education)
        expriences = template.getWorkExpriences()
        result['experiences'] = common.listIfNoneOrEmpty(expriences)

    return result
