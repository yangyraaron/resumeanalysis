#-*- coding: UTF-8 -*-

app = {'name': 'resumeAnalyser',
       'dataFolder': 'jsons',
       'resumesFolder': 'files'
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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        app['name']: {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        }
    }
}
