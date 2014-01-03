#-*- coding: UTF-8 -*-

import common

# get the cotent in () of string
# @content the string to find in {}
# @return string
def find_content_in_bracket(content):
    index_begin = content.find(u'(')
    index_end = content.find(u')')

    if (index_begin == -1 or index_end == -1):
        return "empty"

    return content[index_begin + 1:index_end]


# get the contact information from html string
# eg. mobile:{} email:{}
# @str_contacts string to parse
# @return dictionary
def parse_contact(str_contacts):
    contacts = {}
    key = ''
    value = ''
    # indicate what recording content is, 0:key 1:value
    tp = 0

    for c in str_contacts:
        if c == u'：':
            tp = 1
        elif tp == 0:
            # escape all whitespace and newline chars in front of key
            if key == '' and(c == '\n' or c == ' '):
                continue
            else:
                key += c
        elif tp == 1:
            # escape all whitespace and new line chars in front of value
            if (c == '\n' or c == ' ') and value == '':
                continue
            # when encounter whitespace,then stop appending str to vlaue
            elif c == ' ':
                # store the contact and reset state
                contacts[key] = value.strip()
                tp = 0
                key = ''
                value = ''
            else:
                value += c

    # store last contact entry
    if not key == '':
        contacts[key] = value.strip()

    return contacts

# get the content from position until first ecounters
# the indicated terminal charater
# @strSource original string
# @position the from position
# @strTer the termianl charater
# @isReverse true:from end to start ,false:form start to end
# @return string
def strGetUnitl(strSource, position, strTer,isReverse=False):
    strLen = len(strSource)
    result=''
    c = ''

    istart=position
    iend=strLen
    interval=1

    if isReverse:
        istart = position - strLen
        iend = 0-strLen
        interval = -1
    

    for x in xrange(istart, iend,interval):
        c = strSource[x]
        if c == strTer:
            break
        elif c in common.ESC_CHARS:
            continue
        elif not isReverse:
            result += c
        else:
            result = u'{}{}'.format(c,result)
        
    return result
