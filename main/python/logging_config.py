import logging
from logging.config import dictConfig

conf = dict(
    version=1,
    formatters={
        'f': {'format':
                  '%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%('
                  'process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
    },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)


def load_config():
    dictConfig(conf)
