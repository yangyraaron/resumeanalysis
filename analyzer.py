#-*- coding: UTF-8 -*-

import os
from bs4 import BeautifulSoup
from zhilian import parser
import logging
import logging.config
import setting

## initialization ##
logging.config.dictConfig(setting.LOGGING)
logger = logging.getLogger('resumeAnalyser')

cur_dir = os.path.dirname(os.path.abspath(__file__))

filename = cur_dir + ur'/files/智联招聘_许建梅_java开发工程.html'
soup = BeautifulSoup(open(filename))
parser = parser.ResumeParser(soup)

logger.info('parsing resume...')


# find birth day degree ##
# summary_top = soup.find_all("div", class_="summary-top")[0].span
# summary_top_contents = summary_top.string.split(u'\xa0\xa0\xa0\xa0')
# birthday = summary_top_contents[1]

# print(u'birthday:{}'.format(parser.find_content_in_bracket(birthday)))
# print(u'degree:{}'.format(summary_top_contents[3]))

# find the contact information ##
# summary_bottom = soup.find_all("div", class_="summary-bottom")[0]
# str_contacts = summary_bottom.get_text(u' ')
# contacts = parser.parse_contact(str_contacts)

# keys = contacts.viewkeys()

# for key in keys:
#     print(u'{} : {}'.format(key, contacts[key]))

# find education info ##

# ed_title = soup.find('h3', text=u'教育经历')
# because a string:comma and new line between two elements
# use 2 sibling to get the next element
# ed_container = ed_title.next_sibling.next_sibling
# str_ed = ed_container.contents[0]
# eds = str_ed.split(u'\xa0\xa0')

# for ed in eds:
#     print(ed)


# find work experience ##
# wkex_title = soup.find('h3', text=u'工作经历')
# wkex_heads = wkex_title.parent.find_all('h2')

# for hd in wkex_heads:
#     hd_details = hd.string.split(u'\xa0\xa0')
#     for hd_detail in hd_details:
#         print(hd_detail)

#     wkex_po = hd.next_sibling.next_sibling
#     wkex_pos = wkex_po.string.split(u'|')

#     for po in wkex_pos:
#         print(po)
