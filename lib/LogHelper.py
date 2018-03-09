__author__ = 'Kim'

import logging
import logging.config
import os
import traceback

if not os.path.exists('Logs'):
    os.mkdir('Logs')


def LogInit(file=None):
    # try:
    #     if not file:
    #         return
    logging.config.fileConfig(file, disable_existing_loggers=False)
    # except:
    #     f = open('Logs/traceback.txt', 'a')
    #     traceback.print_exc()
    #     traceback.print_exc(file=f)
    #     f.flush()
    #     f.close()
