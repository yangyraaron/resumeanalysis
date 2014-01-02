#-*- coding: UTF-8 -*-



# get the cotent in () of string
def find_content_in_bracket(content):
    index_begin = content.find(u'(')
    index_end = content.find(u')')

    if (index_begin == -1 or index_end == -1):
        return "empty"

    return content[index_begin + 1:index_end]


# get the contact information from html array
# format: key: value key: value
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
