#!/usr/bin/env python


"""
Bootstrap the app-template. This module disables itself
after execution.
"""

import app_config
import logging
import os

from . import utils
from fabric.api import execute, local, task

logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)

@task(default=True)
def go(github_username=app_config.GITHUB_USERNAME, repository_name=None):
    """
    Execute the bootstrap tasks for a new project.
    """

    
    config_files = ' '.join(['PROJECT_README.md', 'app_config.py', 'crontab'])

    config = {}
    config['$NEW_PROJECT_SLUG'] = os.getcwd().split('/')[-1]
    config['$NEW_REPOSITORY_NAME'] = repository_name or config['$NEW_PROJECT_SLUG']
    config['$NEW_PROJECT_FILENAME'] = config['$NEW_PROJECT_SLUG'].replace('-', '_')

    for k, v in config.items():
        local('sed -i "" \'s|%s|%s|g\' %s' % (k, v, config_files))

    logger.info('Setting up Django')
    execute(django.setup_django)

    utils.confirm("Have you created a Github repository named \"%s\"?" % config['$NEW_REPOSITORY_NAME'])

    local('rm -rf .git')
    local('git init')
    local('mv PROJECT_README.md README.md')
    local('rm LICENSE')
    local('git add .')
    local('git commit -am "Initial import from app-template."')
    local('git remote add origin git@github.com:%s/%s.git' % (github_username, config['$NEW_REPOSITORY_NAME']))
    local('git push -u origin master')