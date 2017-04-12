#!/usr/bin/env python

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
See get_secrets() below for a fast way to access them.
"""

import logging
import os

"""
NAMES
"""
# Project name to be used in urls
# Use dashes, not underscores!
PROJECT_SLUG = '$NEW_PROJECT_SLUG'

# Project name to be used in file paths
PROJECT_FILENAME = '$NEW_PROJECT_FILENAME'

# The name of the repository containing the source
REPOSITORY_NAME = '$NEW_REPOSITORY_NAME'
GITHUB_USERNAME = 'nprapps'
REPOSITORY_URL = 'git@github.com:%s/%s.git' % (GITHUB_USERNAME, REPOSITORY_NAME)
REPOSITORY_ALT_URL = None # 'git@bitbucket.org:nprapps/%s.git' % REPOSITORY_NAME'

"""
DEPLOYMENT
"""
PRODUCTION_S3_BUCKET = 'apps.npr.org'

STAGING_S3_BUCKET = 'stage-apps.npr.org'

DEFAULT_MAX_AGE = 20

PRODUCTION_SERVERS = ['cron.nprapps.org']
STAGING_SERVERS = ['cron-staging.nprapps.org']

# Should code be deployed to the web/cron servers?
DEPLOY_TO_SERVERS = True

SERVER_USER = 'ubuntu'
SERVER_PYTHON = 'python3'
SERVER_PROJECT_PATH = '/home/%s/apps/%s' % (SERVER_USER, PROJECT_FILENAME)
SERVER_REPOSITORY_PATH = '%s/repository' % SERVER_PROJECT_PATH
SERVER_VIRTUALENV_PATH = '%s/virtualenv' % SERVER_PROJECT_PATH

# Should the crontab file be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_CRONTAB = False

# Should the service configurations be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_SERVICES = True

UWSGI_SOCKET_PATH = '/run/uwsgi/%s.uwsgi.sock' % PROJECT_FILENAME

# Services are the server-side services we want to enable and configure.
# A three-tuple following this format:
# (service name, service deployment path, service config file extension)
SERVER_SERVICES = [
    ('app', '/etc/uwsgi/sites', 'ini'),
    ('uwsgi', '/etc/init', 'conf'),
    ('nginx', '/etc/nginx/sites-available', 'conf'),
]

# These variables will be set at runtime. See configure_targets() below
S3_BUCKET = None
S3_BASE_URL = None
S3_DEPLOY_URL = None
SERVERS = []
SERVER_BASE_URL = None
SERVER_LOG_PATH = None
DEBUG = True

"""
Logging
"""
LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'


"""
Utilities
"""
def get_secrets():
    """
    A method for accessing our secrets.
    """
    secrets_dict = {}

    for k,v in os.environ.items():
        if k.startswith(PROJECT_FILENAME):
            k = k[len(PROJECT_FILENAME) + 1:]
            secrets_dict[k] = v

    return secrets_dict


def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKET
    global S3_BASE_URL
    global S3_DEPLOY_URL
    global SERVERS
    global SERVER_BASE_URL
    global SERVER_LOG_PATH
    global DEBUG
    global DEPLOYMENT_TARGET
    global LOG_LEVEL
    global database

    secrets = get_secrets()

    database = {
        'PGDATABASE': PROJECT_FILENAME,
        'PGUSER': secrets.get('POSTGRES_USER', PROJECT_FILENAME),
        'PGPASSWORD': secrets.get('POSTGRES_PASSWORD', PROJECT_FILENAME),
        'PGHOST': secrets.get('POSTGRES_HOST', 'localhost'),
        'PGPORT': secrets.get('POSTGRES_PORT', '5432')
    }

    if deployment_target == 'production':
        S3_BUCKET = PRODUCTION_S3_BUCKET
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKET, PROJECT_SLUG)
        S3_DEPLOY_URL = 's3://%s/%s' % (S3_BUCKET, PROJECT_SLUG)
        SERVERS = PRODUCTION_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        SERVER_LOG_PATH = '/var/log/%s' % PROJECT_FILENAME
        LOG_LEVEL = logging.WARNING
        DEBUG = False
    elif deployment_target == 'staging':
        S3_BUCKET = STAGING_S3_BUCKET
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKET, PROJECT_SLUG)
        S3_DEPLOY_URL = 's3://%s/%s' % (S3_BUCKET, PROJECT_SLUG)
        SERVERS = STAGING_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        SERVER_LOG_PATH = '/var/log/%s' % PROJECT_FILENAME
        LOG_LEVEL = logging.DEBUG
        DEBUG = True
    else:
        S3_BUCKET = None
        S3_BASE_URL = 'http://127.0.0.1:8000'
        S3_DEPLOY_URL = None
        SERVERS = []
        SERVER_BASE_URL = 'http://127.0.0.1:8001/%s' % PROJECT_SLUG
        SERVER_LOG_PATH = '/tmp'
        LOG_LEVEL = logging.DEBUG
        DEBUG = True

    DEPLOYMENT_TARGET = deployment_target

"""
Run automated configuration
"""
DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)