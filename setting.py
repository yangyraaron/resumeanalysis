#-*- coding: UTF-8 -*-

app = {'name': 'resumeAnalyser',
       'dataFolder': 'jsons',
       'resumesFolder': 'files'
       }
db = {
    'mongodb': {
        'host': 'localhost',
        'port': '27017'
    }
}

logging = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        app['name']: {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}
