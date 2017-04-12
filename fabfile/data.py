import app_config

from fabric.api import hide, local, settings, shell_env, task
from fabric.state import env

@task
def create_db():
    with settings(warn_only=True), hide('output', 'running'):
        if env.get('settings'):
            execute('servers.stop_service', 'uwsgi')

        with shell_env(**app_config.database):
            local('dropdb --if-exists %s' % app_config.database['PGDATABASE'])

        if not env.get('settings'):
            local('psql -c "DROP USER IF EXISTS %s;"' % app_config.database['PGUSER'])
            local('psql -c "CREATE USER %s WITH SUPERUSER PASSWORD \'%s\';"' % (app_config.database['PGUSER'], app_config.database['PGPASSWORD']))

        with shell_env(**app_config.database):
            local('createdb %s' % app_config.database['PGDATABASE'])

        if env.get('settings'):
            execute('servers.start_service', 'uwsgi')