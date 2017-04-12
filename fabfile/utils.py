#!/usr/bin/env python

import app_config
import logging

from fabric.api import local, task

logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)

"""
Utilities used by multiple commands.
"""

from fabric.api import prompt

def confirm(message):
    """
    Verify a users intentions.
    """
    answer = prompt(message, default="Not at all")

    if answer.lower() not in ('y', 'yes', 'buzz off', 'screw you'):
        exit()