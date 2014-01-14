#-*- coding: UTF-8 -*-


import common

logger = common.getLogger(__name__)

def construct(template):
    result = {}

    try:
        template.parse()
    except Exception, e:
        logger.error("some thing wrong when parsing html file",exc_info=True)
        return result
    else:
        userName = template.getUserName()
        result['userName'] = common.strIfNoneOrEmpty(userName)

        sex = template.getSex()
        result['sex'] = common.strIfNoneOrEmpty(sex)

        birthday = template.getBirthday()
        result['birthday'] = common.strIfNoneOrEmpty(birthday)

        contacts = template.getContacts()
        result['mobile'] = common.strIfNoneOrEmpty(contacts['mobile'])
        result['email'] = common.strIfNoneOrEmpty(contacts['email'])

        education = template.getEducations()
        result['education'] = common.dicIfNone(education)

        expriences = template.getWorkExpriences()
        result['experiences'] = common.listIfNoneOrEmpty(expriences)
        
        source = template.getSource()
        result['source'] = common.strIfNoneOrEmpty(source)


    return result
