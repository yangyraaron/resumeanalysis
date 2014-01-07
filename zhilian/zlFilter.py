#-*- coding: UTF-8 -*-

import common
from templates import default
from templates import combination

logger = common.getLogger(__name__)


def isSupport(soup):
    """indicate if the resume is from zhilian
        @return true : false"""

    return soup.head is not None and soup.head.title is not None and soup.head.title.string.find(u'智联') != -1


def getTemplate(soup):
    template = default.Template(soup)

    if template.isSupport():
        logger.info('template is zhilian default')
        return template

    template = combination.Template(soup)

    if template.isSupport():
        logger.info('template is zhilian combination')
        return template

    logger.warning(
        'there isn\'t any zhilian templates could parse the resume correctly')
    return None
