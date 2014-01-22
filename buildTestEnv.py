#-*- coding: UTF-8 -*-


import common
import sys
import getopt
import logging
import logging.config
import context
from test import testMgr

# initialize log
logging.config.dictConfig(context.logging)
logger = logging.getLogger('testEnv')


if __name__ == '__main__':
    cmdArgs = {}

    # parse the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:', ["type="])
    except getopt.GetoptError:
        logger.error('the commands is invalid!', exc_info=True)
        sys.exit(2)

    for opt, arg in opts:
        # get the dummy argument
        if opt in ('-t', '--type'):
            cmdArgs['type'] = arg
        else:
            assert False, "unhandled option"

    testType = cmdArgs.get('type')

    if testType is None:
     	testMgr.build()
    elif testType == 'export':
     	testMgr.build()
    elif testType == 'failed':
     	testMgr.buildFailed()
    elif textType == 'clean':
        testMgr.clean()
    
     
     	
     

