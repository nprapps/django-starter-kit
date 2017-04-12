import app_config

from fabric.api import execute, local, settings, task
from fabric.state import env

@task
def collect_static():
    local('python manage.py collectstatic')
    
@task
def setup_django():
    execute('data.create_db')
    local('python manage.py makemigrations')
    local('python manage.py migrate')
    local('python manage.py createsuperuser')

@task
def migrate_db():
    local('python manage.py makemigrations')
    local('python manage.py migrate')