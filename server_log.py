#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Geekbrains - Python Level 2 - Homework Messenger
# Author: Kardash Vadim
# https://github.com/kardvv/GB_messenger
# logger for messenger

import logging
import logging.config
import datetime

today = datetime.datetime.today().strftime("%Y-%m-%d-")

ServerLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": today + "server.log"
        }
    },
    "loggers": {
        "server": {
             "handlers": ["fileHandler"],
             "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
        }
    }
}  

# start logger
logging.config.dictConfig(ServerLogConfig)
logger = logging.getLogger('server')
logger.info('Server started!')
