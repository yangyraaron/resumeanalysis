#-*- coding: UTF-8 -*-


import logging
import setting

ESC_CHARS = [' ', '\n', '\t', '\r']


def getLogger(name=''):
    if name.strip() == '':
        return logging.getLogger(setting.app['name'])

    return logging.getLogger(setting.app['name'] + '.' + name)

def strIfNoneOrEmpty(value, defalutValue=''):
    if value is None or (value == ''):
        return defalutValue
    return value

def listIfNoneOrEmpty(list, defalutValue=[]):
    if list is None or len(list) == 0:
        return defalutValue
    return list

def dicIfNone(dic, defalutValue={}):
    if dic is None:
        return defalutValue
    return dic

def strip(strValue):
    # return strValue.strip().strip('\r').strip('\n').strip('\t')
    result = strValue.strip()
    for c in ESC_CHARS:
        result = result.strip(c)

    return result

# get the cotent in () of string
# @content the string to find in {}
# @return string
def find_content_in_bracket(content):
    index_begin = content.find(u'(')
    index_end = content.find(u')')

    if (index_begin == -1 or index_end == -1):
        return "empty"

    return content[index_begin + 1:index_end]


# get the content from position until first ecounters
# the indicated terminal charater
# @strSource original string
# @position the from position
# @strTer the termianl charater
# @isReverse true:from end to start ,false:form start to end
# @return string
def strGetUnitl(strSource, position, strTers, isReverse=False):
    strLen = len(strSource)
    result = ''
    c = ''

    istart = position
    iend = strLen
    interval = 1

    if isReverse:
        istart = position - strLen
        iend = 0 - strLen
        interval = -1

    for x in xrange(istart, iend, interval):
        c = strSource[x]
        if c in strTers:
            break
        elif c in ESC_CHARS:
            continue
        elif not isReverse:
            result += c
        else:
            result = u'{}{}'.format(c, result)

    return result

# get string from source string by index string until terminal string enconters
# @strIndex index string
# @strSource source string
# @strTers a string array contains terminal string
# @isReverse indicate the order in which read the chars 
# @return string
def getStrByIndexUtil(strIndex, strSource, strTers, isReverse=False):
    index = strSource.find(strIndex)
    if index != -1:
        if isReverse:
            index -= 1
        else:
            index += len(strIndex)
        strValue = strGetUnitl(strSource, index, strTers, isReverse)
        return strip(strValue)

    return ''

def indexNextSibling(ele,index=1):
    if ele is None:
        return None

    result = ele
    end = index+1;
    for x in xrange(1,end):
        if result.next_sibling is not None and result.next_sibling.next_sibling is not None:
            result = result.next_sibling.next_sibling
        else: # if index is overflow then return none
            return None

    return result
            

        

