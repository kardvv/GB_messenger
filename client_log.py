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

ClientLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": "client.log"
        }
    },
    "loggers": {
        "client": {
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
logging.config.dictConfig(ClientLogConfig)
logger = logging.getLogger('client')
logger.info('Client started!')
